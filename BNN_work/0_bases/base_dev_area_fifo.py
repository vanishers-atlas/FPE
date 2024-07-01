# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import functools

# Input Layer types
from _layer_templates.conv  import realise_template as conv
from _layer_templates.pool  import realise_template as pool
from _layer_templates.dense import realise_template as dense
from _layer_templates.acc   import realise_template as acc

def generate_tcl_script(network_name, network_folder, input_dims, network_structure):
    if network_folder.startswith(".\\"):
        fullpath = os.path.dirname(__file__) + "\\" + network_folder[2:]
    else:
        fullpath = os.path.dirname(__file__) + "\\" + network_folder

    # Network script preample
    tcl_script = ""
    tcl_script += "create_bd_design -dir \"%s/measuring\" \"network\"\n\n"%(fullpath.replace("\\", "/"), )

    # Declare commonal ports
    tcl_script += "create_bd_port -dir I -type clk -freq_hz 100000000 clock\n\n"

    # Build the FIFO layer chain there the network
    for layer, layer_details in enumerate(network_structure):
        if len(input_dims) == 1:
            frame_size = input_dims[0]
        else:
            frame_size = functools.reduce(lambda x, y: x * y, input_dims)
        fifo_depth = 2**math.ceil(math.log(frame_size, 2))

        # Declare FIFO
        tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_%i\n"%(layer, )
        tcl_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
        tcl_script += "CONFIG.Input_Data_Width {1} "
        tcl_script += "CONFIG.Input_Depth {%i} "%(fifo_depth, )
        tcl_script += "CONFIG.Output_Data_Width {1} "
        tcl_script += "CONFIG.Output_Depth {%i} "%(fifo_depth, )
        tcl_script += "CONFIG.Reset_Pin {false} "
        tcl_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
        tcl_script += "CONFIG.Use_Dout_Reset {false} "
        tcl_script += "CONFIG.Use_Extra_Logic {true} "
        tcl_script += "CONFIG.Data_Count_Width {10} "
        tcl_script += "CONFIG.Write_Data_Count_Width {10} "
        tcl_script += "CONFIG.Read_Data_Count_Width {10} "
        tcl_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
        tcl_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(frame_size - 1, )
        tcl_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(frame_size - 2, )
        tcl_script += "] [get_bd_cells fifo_%i]\n"%(layer, )

        # Connect FIFO to last layer/network input
        tcl_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_%i/clk]\n"%(layer, )
        if layer == 0: # Connect first fifo to network input
            tcl_script += "create_bd_port -dir I -from 0 -to 0 -type data input_data\n"
            tcl_script += "create_bd_port -dir I input_write\n"
            tcl_script += "create_bd_port -dir O input_ready\n\n"

            tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 input_ready_negate\n"
            tcl_script += "set_property -dict [list CONFIG.C_SIZE {1} "
            tcl_script += "CONFIG.C_OPERATION {not} "
            tcl_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells input_ready_negate]\n\n"

            tcl_script += "connect_bd_net [get_bd_ports input_data] [get_bd_pins fifo_0/din]\n"
            tcl_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins fifo_0/wr_en]\n"
            tcl_script += "connect_bd_net [get_bd_pins fifo_0/full] [get_bd_pins input_ready_negate/Op1]\n"
            tcl_script += "connect_bd_net [get_bd_pins input_ready_negate/Res] [get_bd_ports input_ready] \n"
        else: # Connect fifo to last layer
            tcl_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins fifo_%i/din]\n"%(layer - 1, layer, )
            tcl_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins fifo_%i/wr_en]\n"%(layer - 1, layer, )
        tcl_script += "\n"


        # Generate Program
        if   layer_details["type"] == "conv":
            assert len(input_dims) == 3
            data_rows, data_cols, data_depth = input_dims
            num_kernals = layer_details["kernals"]

            output_dims = conv(network_folder, "layer_%i"%(layer,), data_rows, data_cols, data_depth, num_kernals, use_BRAMs=True)
        elif layer_details["type"] == "pool":
            assert len(input_dims) == 3
            data_rows, data_cols, data_depth = input_dims

            output_dims = pool(network_folder, "layer_%i"%(layer,), data_rows, data_cols, data_depth, use_BRAMs=True)
        elif layer_details["type"] == "dense":
            assert len(input_dims) == 3 or len(input_dims) == 1
            if len(input_dims) == 1:
                input_neurons = input_dims[0]
            else:
                input_neurons = functools.reduce(lambda x, y: x * y, input_dims)
            output_neurons = layer_details["neurons"]

            output_dims =  dense(network_folder, "layer_%i"%(layer,), input_neurons, output_neurons, use_BRAMs=True)
        elif layer_details["type"] == "acc":
            assert len(input_dims) == 1
            input_neurons = input_dims[0]
            output_neurons = layer_details["neurons"]

            output_dims =  acc(network_folder, "layer_%i"%(layer,), input_neurons, output_neurons, use_BRAMs=True)
        else:
            raise ValueError("Unknoen layer type, %s"%(str(layer_details["type"]), ) )

        # Generate layer's toolchain files
        run_toolchain(
            program     = network_folder + "\\layer_%i.fpea"%(layer, ),
            parameters  = network_folder + "\\layer_%i_parameters.json"%(layer, ),
            generics    = network_folder + "\\layer_%i_generics.json"%(layer, ),
            output_dir  = network_folder + "\\toolchain_files",
            processor_name      = "layer_%i"%(layer, ),
            concat_naming       = True,
            force_generation    = True
        )

        # Instancate layer into block daigram
        tcl_script += "create_bd_cell -type module -reference layer_%i_inst layer_%i\n\n"%(layer, layer, )

        # Connect layer to clock and writing tracking port
        tcl_script += "create_bd_port -dir O layer_%i_running\n"%(layer, )
        tcl_script += "connect_bd_net [get_bd_pins /layer_%i/running] [get_bd_ports layer_%i_running]\n"%(layer, layer, )
        tcl_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins layer_%i/clock]\n\n"%(layer, )

        # # Connect layer to input (just created FIFO)
        tcl_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(layer, layer, )
        tcl_script += "connect_bd_net [get_bd_pins layer_%i/GET_FIFO_0_adv] [get_bd_pins fifo_%i/rd_en]\n\n"%(layer, layer, )


        # output for one layer becomes the input of the next
        input_dims = output_dims

    # Handle the final FIFO
    OUTPUT_FIFO = len(network_structure)
    LAST_LAYER = OUTPUT_FIFO - 1
    assert len(output_dims) == 2
    output_width, output_depth = output_dims
    output_depth_pot = 2**math.ceil(math.log(output_depth, 2))

    tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_%i\n"%(OUTPUT_FIFO, )
    tcl_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
    tcl_script += "CONFIG.Input_Data_Width {%i} "%(output_width, )
    tcl_script += "CONFIG.Input_Depth {%i} "%(output_depth_pot, )
    tcl_script += "CONFIG.Output_Data_Width {%i} "%(output_width, )
    tcl_script += "CONFIG.Output_Depth {%i} "%(output_depth_pot, )
    tcl_script += "CONFIG.Reset_Pin {false} "
    tcl_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
    tcl_script += "CONFIG.Use_Dout_Reset {false} "
    tcl_script += "CONFIG.Use_Extra_Logic {true} "
    tcl_script += "CONFIG.Data_Count_Width {10} "
    tcl_script += "CONFIG.Write_Data_Count_Width {10} "
    tcl_script += "CONFIG.Read_Data_Count_Width {10} "
    tcl_script += "] [get_bd_cells fifo_%i]\n\n"%(OUTPUT_FIFO, )


    # Conect output fifo to lasy layer
    tcl_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_%i/clk]\n"%(OUTPUT_FIFO, )
    tcl_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins fifo_%i/din]\n"%(LAST_LAYER, OUTPUT_FIFO, )
    tcl_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins fifo_%i/wr_en]\n"%(LAST_LAYER, OUTPUT_FIFO, )

    # Declare output ports
    tcl_script += "create_bd_port -dir O -from %i -to 0 -type data output_data\n"%(output_width - 1, )
    tcl_script += "create_bd_port -dir I output_read\n"
    tcl_script += "create_bd_port -dir O output_valid\n\n"

    tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 output_valid_negate\n"
    tcl_script += "set_property -dict [list CONFIG.C_SIZE {1} "
    tcl_script += "CONFIG.C_OPERATION {not} "
    tcl_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells output_valid_negate]\n\n"

    tcl_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_ports output_data]\n"%(OUTPUT_FIFO, )
    tcl_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins fifo_%i/rd_en]\n"%(OUTPUT_FIFO, )
    tcl_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins output_valid_negate/Op1]\n"%(OUTPUT_FIFO, )
    tcl_script += "connect_bd_net [get_bd_pins output_valid_negate/Res] [get_bd_ports output_valid]\n\n"


    # Handle the kickoff logic for each of the layers
    # Speacal case first layer
    tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 layer_0_kickoff_concat\n"
    tcl_script += "set_property -dict [list CONFIG.NUM_PORTS {2}] [get_bd_cells layer_0_kickoff_concat]\n"

    tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_reduced_logic:2.0 layer_0_kickoff_reduce\n"
    tcl_script += "set_property -dict [list CONFIG.C_SIZE {2}] [get_bd_cells layer_0_kickoff_reduce]\n\n"

    tcl_script += "connect_bd_net [get_bd_pins fifo_0/prog_full] [get_bd_pins layer_0_kickoff_concat/In0]\n"
    tcl_script += "connect_bd_net [get_bd_pins fifo_1/empty] [get_bd_pins layer_0_kickoff_concat/In1]\n"
    tcl_script += "connect_bd_net [get_bd_pins layer_0_kickoff_concat/dout] [get_bd_pins layer_0_kickoff_reduce/Op1]\n"
    tcl_script += "connect_bd_net [get_bd_pins layer_0_kickoff_reduce/Res] [get_bd_pins layer_0/kickoff]\n"

    # All other layers general case
    for layer in range(1, len(network_structure)):
        tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 layer_%i_kickoff_concat\n"%(layer, )
        tcl_script += "set_property -dict [list CONFIG.NUM_PORTS {3}] [get_bd_cells layer_%i_kickoff_concat]\n\n"%(layer, )

        tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_reduced_logic:2.0 layer_%i_kickoff_reduce\n"%(layer, )
        tcl_script += "set_property -dict [list CONFIG.C_SIZE {3}] [get_bd_cells layer_%i_kickoff_reduce]\n\n"%(layer, )

        tcl_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 layer_%i_running_negate\n"%(layer - 1, )
        tcl_script += "set_property -dict [list CONFIG.C_SIZE {1} "
        tcl_script += "CONFIG.C_OPERATION {not} "
        tcl_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells layer_%i_running_negate]\n\n"%(layer - 1, )

        tcl_script += "connect_bd_net [get_bd_pins layer_%i/running] [get_bd_pins layer_%i_running_negate/Op1]\n"%(layer - 1, layer - 1, )
        tcl_script += "connect_bd_net [get_bd_pins layer_%i_running_negate/Res] [get_bd_pins layer_%i_kickoff_concat/In0]\n"%(layer - 1, layer )
        tcl_script += "connect_bd_net [get_bd_pins fifo_%i/prog_full] [get_bd_pins layer_%i_kickoff_concat/In1]\n"%(layer, layer )
        tcl_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins layer_%i_kickoff_concat/In2]\n"%(layer + 1, layer )
        tcl_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_concat/dout] [get_bd_pins layer_%i_kickoff_reduce/Op1]\n"%(layer, layer )
        tcl_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_reduce/Res] [get_bd_pins layer_%i/kickoff]\n"%(layer, layer )

    # Network script postample
    tcl_script += "save_bd_design\n"
    tcl_script += "close_bd_design [current_bd_design]\n\n"
    tcl_script += "make_wrapper -top -files [get_files %s/measuring/network/network.bd]\n\n"%(fullpath.replace("\\", "/"), )
    tcl_script += "add_files -norecurse %s/measuring/network/hdl/network_wrapper.vhd\n"%(fullpath.replace("\\", "/"), )
    tcl_script += "set_property library work [get_files  %s/measuring/network/hdl/network_wrapper.vhd]\n"%(fullpath.replace("\\", "/"), )

    tcl_script += "set_property top network_wrapper [current_fileset]\n\n"

    # Write network script to file

    with open("%s\\gen_block_diagram.tcl"%(network_folder, ), "w") as f:
        f.write(tcl_script)

    return output_width


def generate_testbench(network_name, network_structure, output_width):
    # Create testbench
    tb = gen_utils.indented_string()

    tb += "library IEEE;\n"
    tb += "use IEEE.std_logic_1164.ALL;\n\n"

    tb += "entity testbench is\n"
    tb += "end testbench;\n\n"

    tb += "architecture arch of testbench is\n@>"
    tb += "signal clock : std_logic := '0';\n\n"

    tb += "signal input_data  : std_logic_vector ( 0 to 0 );\n"
    tb += "signal input_ready : std_logic_vector ( 0 to 0 );\n"
    tb += "signal input_write : std_logic := '0';\n\n"

    for layer in range(len(network_structure)):
        tb += "signal layer_%i_running : std_logic;\n"%(layer, )
        tb += "signal layer_%i_frame : integer := -1;\n"%(layer, )

    tb += "\n"

    tb += "signal output_data  : std_logic_vector (%i downto 0 );\n"%(output_width - 1, )
    tb += "signal output_read  : std_logic := '0';\n"
    tb += "signal output_valid : std_logic_vector ( 0 to 0 );\n"

    tb += "@<begin\n@>"

    tb += "UUT : entity work.network_wrapper(STRUCTURE)\n@>"
    tb += "port map(\n@>"
    tb += "clock => clock,\n\n"

    tb += "input_data  => input_data,\n"
    tb += "input_ready => input_ready,\n"
    tb += "input_write => input_write,\n\n"

    for layer in range(len(network_structure)):
        tb += "layer_%i_running => layer_%i_running,\n"%(layer, layer, )
    tb += "\n"

    tb += "output_data  => output_data,\n"
    tb += "output_read  => output_read,\n"
    tb += "output_valid => output_valid\n"

    tb += "@<);\n@<\n"

    tb += "-- Generate clock\n"
    tb += "process\n@>"
    tb += "@<begin\n@>"
    tb += "wait for 1000 ns;\n"
    tb += "loop\n@>"
    tb += "clock <= '1';\n"
    tb += "wait for 5 ns;\n"
    tb += "clock <= '0';\n"
    tb += "wait for 5 ns;\n"
    tb += "@<end loop;\n"
    tb += "@<end process;\n\n"

    tb += "-- Generate input_data\n"
    tb += "input_data <= \"1\";\n\n"

    tb += "-- Generate input_write\n"
    tb += "process(clock)\n@>"
    tb += "@<begin\n@>"
    tb += "if rising_edge(clock) then\n@>"
    tb += "input_write <= input_ready(0);\n"
    tb += "@<end if;\n"
    tb += "@<end process;\n\n"

    for layer in range(len(network_structure)):
        tb += "-- Track layer_%i_frame\n"%(layer, )
        tb += "process(layer_%i_running)\n@>"%(layer, )
        tb += "@<begin\n@>"
        tb += "if rising_edge(layer_%i_running) then\n@>"%(layer, )
        tb += "report \"layer_%i starting frame \" & integer'Image(layer_%i_frame + 1) severity note;\n"%(layer, layer, )
        tb += "layer_%i_frame <= layer_%i_frame + 1;\n"%(layer, layer, )
        tb += "@<end if;\n"
        tb += "if falling_edge(layer_%i_running) then\n@>"%(layer, )
        tb += "report \"layer_%i finished frame \" & integer'Image(layer_%i_frame) severity note;\n"%(layer, layer, )
        tb += "@<end if;\n"
        tb += "@<end process;\n\n"

    tb += "-- Generate output_read\n"
    tb += "process(clock)\n@>"
    tb += "@<begin\n@>"
    tb += "if rising_edge(clock) then\n@>"
    tb += "output_read <= output_valid(0);\n"
    tb += "@<end if;\n"
    tb += "@<end process;\n\n"

    tb += "@<end arch;\n"

    with open("%s\\testbench.vhd"%(network_folder, ), "w") as f:
        f.write(str(tb))


# If running as a script, create and measure the dev network
if __name__ == "__main__":
    from FPE.BNN_work import _utils as meas_utils

    from FPE.toolchain import utils as tc_utils
    from FPE.toolchain.HDL_generation  import utils as gen_utils
    from FPE.toolchain.HDL_generation  import HDL_generator

    from FPE.toolchain.tests.utils  import run_toolchain

    import os
    import math

    network_name = "base_dev_area_fifo"
    network_folder = ".\\" + network_name
    input_dims = (8, 8, 6)
    network_structure = [
        {
            "type" : "conv",
            "kernals" : 16,
        },
        {
            "type" : "conv",
            "kernals" : 16,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "conv",
            "kernals" : 32,
        },
        {
            "type" : "conv",
            "kernals" : 32,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "conv",
            "kernals" : 64,
        },
        {
            "type" : "conv",
            "kernals" : 64,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "dense",
            "neurons" : 128,
        },
        {
            "type" : "acc",
            "neurons" : 10,
        },
    ]

    # Generate network
    output_width = generate_tcl_script(network_name, network_folder, input_dims, network_structure)

    #Generate testbench
    generate_testbench(network_folder, network_structure, output_width)

    # Measure the generated network's area nad timing
    dir_pathway = os.path.dirname(__file__)
    meas_utils.impl_and_simulate_network(network_name, network_folder, dir_pathway, measure_area=True, measure_timing=True, compute_timing_metrics=True)
