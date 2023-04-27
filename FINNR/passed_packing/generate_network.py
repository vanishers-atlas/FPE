# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain.HDL_generation  import HDL_generator

from FPE.toolchain.tests.utils  import run_toolchain

import os
import math

# input layer types
from _layer_types.conv  import generate_layer as conv
from _layer_types.pool  import generate_layer as pool
from _layer_types.dense import generate_layer as dense
from _layer_types.acc   import generate_layer as acc

def generation_network(network_name, input_dims, layers, use_BRAMs=True):
    FIFO_FULL_MIN = 5 + 2
    FIFO_EMPTY_MIN = 4 + 2

    # Store each network in its own folder
    network_folder = ".\\" + network_name
    try:
        os.makedirs(network_folder + "\\toolchain_files")
    except FileExistsError:
        pass

    network_script = ""

    # Setup interlayer variables
    layer_width  = input_dims["width"]
    layer_height = input_dims["height"]
    layer_depth  = input_dims["depth"]
    word_width = 1
    if layers[0]["input_packing"] == None:
        assert layers[0]["type"] == "conv"
        layers[0]["input_packing"] = conv.compute_max_packing(layer_depth)
    fifo_words = layers[0]["input_packing"]

    fifo_area = layer_width * layer_height * layer_depth
    fifo_width = word_width * fifo_words
    assert fifo_area % fifo_words == 0
    fifo_depth = int(fifo_area/fifo_words)
    if fifo_depth < FIFO_FULL_MIN:
        scaling_fact = math.ceil(FIFO_FULL_MIN/fifo_depth)
        full_flag = scaling_fact * fifo_depth
    else:
        full_flag = fifo_depth

    fifo_depth_pot = 2**math.ceil(math.log(fifo_depth, 2))
    fifo_depth_pot = max(16, fifo_depth_pot)
    assert full_flag <= fifo_depth_pot

    # Store consts used elsewhere in script
    LAST_LAYER = len(layers) - 1
    INPUT_WIDTH = fifo_width

    # Add input FIFO into network
    network_script += "create_bd_design \"network\"\n\n"

    network_script += "create_bd_port -dir I -type clk -freq_hz 100000000 clock\n\n"

    network_script += "create_bd_port -dir I -from %i -to 0 -type data input_data\n"%(fifo_width - 1, )
    network_script += "create_bd_port -dir I input_write\n"
    network_script += "create_bd_port -dir O input_ready\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_0\n"
    network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
    network_script += "CONFIG.Input_Data_Width {%i} "%(fifo_width, )
    network_script += "CONFIG.Input_Depth {%i} "%(fifo_depth_pot, )
    network_script += "CONFIG.Output_Data_Width {%i} "%(fifo_width, )
    network_script += "CONFIG.Output_Depth {%i} "%(fifo_depth_pot, )
    network_script += "CONFIG.Reset_Pin {false} "
    network_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
    network_script += "CONFIG.Use_Dout_Reset {false} "
    network_script += "CONFIG.Use_Extra_Logic {true} "
    network_script += "CONFIG.Data_Count_Width {10} "
    network_script += "CONFIG.Write_Data_Count_Width {10} "
    network_script += "CONFIG.Read_Data_Count_Width {10} "
    network_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
    network_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(full_flag - 2, )
    network_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(full_flag - 3, )
    network_script += "CONFIG.Empty_Threshold_Assert_Value {4} "
    network_script += "CONFIG.Empty_Threshold_Negate_Value {5}] [get_bd_cells fifo_0]\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 input_ready_negate\n"
    network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
    network_script += "CONFIG.C_OPERATION {not} "
    network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells input_ready_negate]\n\n"

    network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_0/clk]\n"
    network_script += "connect_bd_net [get_bd_ports input_data] [get_bd_pins fifo_0/din]\n"
    network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins fifo_0/wr_en]\n"
    network_script += "connect_bd_net [get_bd_pins fifo_0/full] [get_bd_pins input_ready_negate/Op1]\n"
    network_script += "connect_bd_net [get_bd_ports input_ready] [get_bd_pins input_ready_negate/Res]\n\n"


    for l in range(len(layers)):
        # Generate Program
        if   layers[l]["type"] == "conv":
            assert layers[l]["input_packing"] != None
            if layers[l]["output_packing"] == None:
                if layers[l + 1]["type"] == "conv":
                    packing = conv.compute_max_packing(layers[l]["kernals"])
                elif layers[l + 1]["type"] == "pool":
                    packing = pool.compute_max_packing(layers[l]["kernals"])
                else:
                    raise ValueError("Unknoen interface, %s => s"%(str(layers[l]["type"]), str(layers[l + 1]["type"]), ) )

                layers[l]["output_packing"] = packing
                layers[l + 1 ]["input_packing"] = packing

            # Generate layer's program files
            conv.generate_layer(
                network_folder,
                "layer_%i"%(l),
                layer_width,
                layer_height,
                layer_depth,
                layers[l]["kernals"],
                layers[l]["input_packing"],
                layers[l]["output_packing"],
                use_BRAMs
            )

            # Update interlayer variables
            layer_width  = layer_width
            layer_height = layer_height
            layer_depth  = layers[l]["kernals"]
            word_width = 1
            fifo_words = layers[l]["output_packing"]
        elif layers[l]["type"] == "pool":
            assert layers[l]["input_packing"] != None
            if layers[l]["output_packing"] == None:
                packing = layers[l]["input_packing"]
                layers[l]["output_packing"] = packing
                layers[l + 1 ]["input_packing"] = packing

            # Generate layer's program files
            pool.generate_layer(
                network_folder,
                "layer_%i"%(l),
                layer_width,
                layer_height,
                layer_depth,
                layers[l]["input_packing"],
                use_BRAMs
            )

            # Update interlayer variables
            layer_width  = int(layer_width/2)
            layer_height = int(layer_height/2)
            word_width = 1
            fifo_words = layers[l]["output_packing"]
        elif layers[l]["type"] == "dense":
            assert layers[l]["input_packing"] != None
            if layers[l]["output_packing"] == None:
                if layers[l + 1]["type"] == "dense":
                    packing = dense.compute_max_packing(layers[l]["neurons"])
                elif layers[l + 1]["type"] == "acc":
                    packing = acc.compute_max_packing(layers[l]["neurons"])
                else:
                    raise ValueError("Unknoen interface, %s => s"%(str(layers[l]["type"]), str(layers[l + 1]["type"]), ) )

                layers[l]["output_packing"] = packing
                layers[l + 1 ]["input_packing"] = packing

            # Generate layer's program files
            dense.generate_layer(
                network_folder,
                "layer_%i"%(l),
                layer_width * layer_height * layer_depth,
                layers[l]["neurons"],
                layers[l]["input_packing"],
                layers[l]["output_packing"],
                use_BRAMs
            )

            # Update interlayer variables
            layer_width  = 1
            layer_height = 1
            layer_depth  = layers[l]["neurons"]
            word_width = 1
            fifo_words = layers[l]["output_packing"]
        elif layers[l]["type"] == "acc":
            output_data_width = tc_utils.unsigned.width(layer_width * layer_height * layer_depth)
            layers[l]["output_packing"] = 1

            # Generate layer's program files
            acc.generate_layer(
                network_folder,
                "layer_%i"%(l),
                layer_width * layer_height * layer_depth,
                layers[l]["neurons"],
                layers[l]["input_packing"],
                use_BRAMs
            )

            # Update interlayer variables
            layer_width  = 1
            layer_height = 1
            layer_depth  = layers[l]["neurons"]
            word_width = output_data_width
            fifo_words = 1
        else:
            raise ValueError("Unknoen layer type, %s"%(str(layers[l]["type"]), ) )


        # Generate layer's toolchain files
        run_toolchain(
            program     = network_folder + "\\layer_%i_program.fpea"%(l, ),
            parameters  = network_folder + "\\layer_%i_parameters.json"%(l, ),
            generics    = network_folder + "\\layer_%i_generics.json"%(l, ),
            output_dir  = network_folder + "\\toolchain_files",
            processor_name      = "layer_%i"%(l, ),
            concat_naming       = True,
            force_generation    = True
        )

        fifo_area = layer_width * layer_height * layer_depth
        fifo_width = word_width * fifo_words
        assert fifo_area % fifo_words == 0
        fifo_depth = int(fifo_area/fifo_words)
        fifo_depth_pot = 2**math.ceil(math.log(fifo_depth, 2))
        fifo_depth_pot = max(16, fifo_depth_pot)
        if fifo_depth < FIFO_FULL_MIN:
            scaling_fact = math.ceil(FIFO_FULL_MIN/fifo_depth)

            full_flag = scaling_fact * fifo_depth
            empty_flag = fifo_depth_pot - fifo_depth

        else:
            full_flag = fifo_depth
            empty_flag = None

        fifo_depth_pot = 2**math.ceil(math.log(fifo_depth, 2))
        fifo_depth_pot = max(16, fifo_depth_pot)
        assert full_flag <= fifo_depth_pot


        network_script += "create_bd_cell -type module -reference layer_%i_inst layer_%i\n\n"%(l, l, )

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 layer_%i_kickoff_concat\n"%(l, )
        if l == 0:
            network_script += "set_property -dict [list CONFIG.NUM_PORTS {2}] [get_bd_cells layer_%i_kickoff_concat]\n"%(l, )
        else:
            network_script += "set_property -dict [list CONFIG.NUM_PORTS {3}] [get_bd_cells layer_%i_kickoff_concat]\n\n"%(l, )

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_reduced_logic:2.0 layer_%i_kickoff_reduce\n"%(l, )
        if l == 0:
            network_script += "set_property -dict [list CONFIG.C_SIZE {2}] [get_bd_cells layer_%i_kickoff_reduce]\n\n"%(l, )
        else:
            network_script += "set_property -dict [list CONFIG.C_SIZE {3}] [get_bd_cells layer_%i_kickoff_reduce]\n\n"%(l, )

        if l != 0:
            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 layer_%i_running_negate\n"%(l - 1, )
            network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
            network_script += "CONFIG.C_OPERATION {not} "
            network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells layer_%i_running_negate]\n\n"%(l - 1, )

        input_FIFO  = l
        output_FIFO = l + 1

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_%i\n"%(output_FIFO, )
        network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
        network_script += "CONFIG.Input_Data_Width {%i} "%(fifo_width, )
        network_script += "CONFIG.Input_Depth {%i} "%(fifo_depth_pot, )
        network_script += "CONFIG.Output_Data_Width {%i} "%(fifo_width, )
        network_script += "CONFIG.Output_Depth {%i} "%(fifo_depth_pot, )
        network_script += "CONFIG.Reset_Pin {false} "
        network_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
        network_script += "CONFIG.Use_Dout_Reset {false} "
        network_script += "CONFIG.Use_Extra_Logic {true} "
        network_script += "CONFIG.Data_Count_Width {10} "
        network_script += "CONFIG.Write_Data_Count_Width {10} "
        network_script += "CONFIG.Read_Data_Count_Width {10} "
        if l != LAST_LAYER:
            network_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
            network_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(full_flag - 1, )
            network_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(full_flag - 2, )
        else:
            network_script += "CONFIG.Programmable_Full_Type {No_Programmable_Full_Threshold} "
        if empty_flag != None:
            network_script += "CONFIG.Programmable_Empty_Type {Single_Programmable_Empty_Threshold_Constant} "
            network_script += "CONFIG.Empty_Threshold_Assert_Value {%i} "%(empty_flag - 1, )
            network_script += "CONFIG.Empty_Threshold_Negate_Value {%i} "%(empty_flag - 2, )
        network_script += "] [get_bd_cells fifo_%i]\n"%(output_FIFO, )

        network_script += "create_bd_port -dir O layer_%i_running\n"%(l, )
        network_script += "connect_bd_net [get_bd_pins /layer_%i/running] [get_bd_ports layer_%i_running]\n"%(l, l, )

        network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins layer_%i/clock]\n"%(l, )
        network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_%i/clk]\n"%(output_FIFO, )

        network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(input_FIFO, l, )
        network_script += "connect_bd_net [get_bd_pins layer_%i/GET_FIFO_0_adv] [get_bd_pins fifo_%i/rd_en]\n"%(l, input_FIFO, )

        network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins fifo_%i/din]\n"%(l, output_FIFO, )
        network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins fifo_%i/wr_en]\n"%(l, output_FIFO, )

        if l != 0:
            network_script += "connect_bd_net [get_bd_pins layer_%i/running] [get_bd_pins layer_%i_running_negate/Op1]\n"%(l - 1, l - 1, )

        network_script += "connect_bd_net [get_bd_pins fifo_%i/prog_full] [get_bd_pins layer_%i_kickoff_concat/In0]\n"%(input_FIFO, l, )
        if empty_flag == None:
            network_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins layer_%i_kickoff_concat/In1]\n"%(output_FIFO, l, )
        else:
            network_script += "connect_bd_net [get_bd_pins fifo_%i/prog_empty] [get_bd_pins layer_%i_kickoff_concat/In1]\n"%(output_FIFO, l, )
        if l != 0:
            network_script += "connect_bd_net [get_bd_pins layer_%i_running_negate/Res] [get_bd_pins layer_%i_kickoff_concat/In2]\n"%(l - 1, l, )
        network_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_concat/Dout] [get_bd_pins layer_%i_kickoff_reduce/Op1]\n"%(l, l, )
        network_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_reduce/Res] [get_bd_pins layer_%i/kickoff]\n\n"%(l, l, )


    # Finish network with output
    network_script += "create_bd_port -dir O -from %i -to 0 -type data output_data\n"%(fifo_width - 1, )
    network_script += "create_bd_port -dir I output_read\n"
    network_script += "create_bd_port -dir O output_valid\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 output_valid_negate\n"
    network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
    network_script += "CONFIG.C_OPERATION {not} "
    network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells output_valid_negate]\n\n"

    network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_ports output_data]\n"%(LAST_LAYER + 1, )
    network_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins fifo_%i/rd_en]\n"%(LAST_LAYER + 1, )
    network_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins output_valid_negate/Op1]\n"%(LAST_LAYER + 1, )
    network_script += "connect_bd_net [get_bd_pins output_valid_negate/Res] [get_bd_ports output_valid]\n\n"

    network_script += "save_bd_design\n"
    network_script += "close_bd_design [current_bd_design]\n\n"

    dir_pathway = os.path.dirname(__file__).replace("\\", "/")
    network_script += "make_wrapper -files [get_files %s/%s/measuring/measuring.srcs/sources_1/bd/network/network.bd] -top\n"%(dir_pathway, network_name, )
    network_script += "add_files -norecurse %s/%s/measuring/measuring.srcs/sources_1/bd/network/hdl/network_wrapper.vhd\n"%(dir_pathway, network_name, )
    network_script += "set_property top network_wrapper [current_fileset]\n\n"

    with open("%s\\gen_block_diagram.tcl"%(network_folder, ), "w") as f:
        f.write(network_script)

    # Create testbench
    tb = gen_utils.indented_string()

    tb += "library IEEE;\n"
    tb += "use IEEE.std_logic_1164.ALL;\n\n"

    tb += "entity testbench is\n"
    tb += "end testbench;\n\n"

    tb += "architecture arch of testbench is\n\>"
    tb += "signal clock : std_logic := '0';\n\n"

    tb += "signal input_data  : std_logic_vector ( %i downto 0 );\n"%(INPUT_WIDTH - 1, )
    tb += "signal input_ready : std_logic_vector ( 0 to 0 );\n"
    tb += "signal input_write : std_logic := '0';\n\n"

    for l in range(len(layers)):
        tb += "signal layer_%i_running : std_logic;\n"%(l, )
        tb += "signal layer_%i_frame : integer := -1;\n"%(l, )

    tb += "\n"

    tb += "signal output_data  : std_logic_vector (%i downto 0 );\n"%(fifo_width - 1, )
    tb += "signal output_read  : std_logic := '0';\n"
    tb += "signal output_valid : std_logic_vector ( 0 to 0 );\n"

    tb += "\<begin\n\>"

    tb += "UUT : entity work.network_wrapper(STRUCTURE)\n\>"
    tb += "port map(\n\>"
    tb += "clock => clock,\n\n"

    tb += "input_data  => input_data,\n"
    tb += "input_ready => input_ready,\n"
    tb += "input_write => input_write,\n\n"

    for l in range(len(layers)):
        tb += "layer_%i_running => layer_%i_running,\n"%(l, l, )
    tb += "\n"

    tb += "output_data  => output_data,\n"
    tb += "output_read  => output_read,\n"
    tb += "output_valid => output_valid\n"

    tb += "\<);\n\<\n"

    tb += "-- Generate clock\n"
    tb += "process\n\>"
    tb += "\<begin\n\>"
    tb += "wait for 1000 ns;\n"
    tb += "loop\n\>"
    tb += "clock <= '1';\n"
    tb += "wait for 5 ns;\n"
    tb += "clock <= '0';\n"
    tb += "wait for 5 ns;\n"
    tb += "\<end loop;\n"
    tb += "\<end process;\n\n"

    tb += "-- Generate input_data\n"
    print()
    tb += "input_data <= \"%s\";\n\n"%(("01"*math.ceil(INPUT_WIDTH))[:INPUT_WIDTH], )

    tb += "-- Generate input_write\n"
    tb += "process(clock)\n\>"
    tb += "\<begin\n\>"
    tb += "if rising_edge(clock) then\n\>"
    tb += "input_write <= input_ready(0);\n"
    tb += "\<end if;\n"
    tb += "\<end process;\n\n"

    for l in range(len(layers)):
        tb += "-- Track layer_%i_frame\n"%(l, )
        tb += "process(layer_%i_running)\n\>"%(l, )
        tb += "\<begin\n\>"
        tb += "if rising_edge(layer_%i_running) then\n\>"%(l, )
        tb += "report \"layer_%i starting frame \" & integer'Image(layer_%i_frame + 1) severity note;\n"%(l, l, )
        tb += "layer_%i_frame <= layer_%i_frame + 1;\n"%(l, l, )
        tb += "\<end if;\n"
        tb += "if falling_edge(layer_%i_running) then\n\>"%(l, )
        tb += "report \"layer_%i finished frame \" & integer'Image(layer_%i_frame) severity note;\n"%(l, l, )
        tb += "\<end if;\n"
        tb += "\<end process;\n\n"

    tb += "-- Generate output_read\n"
    tb += "process(clock)\n\>"
    tb += "\<begin\n\>"
    tb += "if rising_edge(clock) then\n\>"
    tb += "output_read <= output_valid(0);\n"
    tb += "\<end if;\n"
    tb += "\<end process;\n\n"

    tb += "\<end arch;\n"

    with open("%s\\testbench.vhd"%(network_folder, ), "w") as f:
        f.write(str(tb))

    return network_folder
