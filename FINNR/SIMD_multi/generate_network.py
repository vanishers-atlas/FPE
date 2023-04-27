# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.FINNR import _utils as meas_utils
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

    assert "lanes" in input_dims    # check number of lanes give
    assert type(input_dims["lanes"]) == int  # check int
    assert input_dims["lanes"] > 0  # check positive
    assert math.log(input_dims["lanes"], 2) % 1 == 0 # Check pow of 2
    NUM_LANES = input_dims["lanes"]

    # Store each network in its own folder
    network_folder = ".\\" + network_name
    try:
        os.makedirs(network_folder + "\\toolchain_files")
    except FileExistsError:
        pass

    network_script = ""

    # Add input FIFO into network
    network_script += "create_bd_design \"network\"\n\n"

    network_script += "create_bd_port -dir I -type clk -freq_hz 100000000 clock\n\n"

    for lane in range(NUM_LANES):
        network_script += "create_bd_port -dir I -from 0 -to 0 -type data input_data_lane_%i\n"%(lane, )
    network_script += "create_bd_port -dir I input_write\n"
    network_script += "create_bd_port -dir O input_ready\n\n"

    input_size = input_dims["width"] * input_dims["height"]* input_dims["depth"]
    input_size_pot = 2**math.ceil(math.log(input_size, 2))

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_0\n"
    network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
    network_script += "CONFIG.Input_Data_Width {%i} "%(NUM_LANES)
    network_script += "CONFIG.Input_Depth {%i} "%(input_size_pot, )
    network_script += "CONFIG.Output_Data_Width {%i} "%(NUM_LANES)
    network_script += "CONFIG.Output_Depth {%i} "%(input_size_pot, )
    network_script += "CONFIG.Reset_Pin {false} "
    network_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
    network_script += "CONFIG.Use_Dout_Reset {false} "
    network_script += "CONFIG.Use_Extra_Logic {true} "
    network_script += "CONFIG.Data_Count_Width {10} "
    network_script += "CONFIG.Write_Data_Count_Width {10} "
    network_script += "CONFIG.Read_Data_Count_Width {10} "
    network_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
    network_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(input_size - 2, )
    network_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(input_size - 3, )
    network_script += "CONFIG.Empty_Threshold_Assert_Value {4} "
    network_script += "CONFIG.Empty_Threshold_Negate_Value {5}] [get_bd_cells fifo_0]\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 input_ready_negate\n"
    network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
    network_script += "CONFIG.C_OPERATION {not} "
    network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells input_ready_negate]\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 fifo_0_concat\n"
    network_script += "set_property -dict [list CONFIG.NUM_PORTS {%i}] [get_bd_cells fifo_0_concat]\n"%(NUM_LANES, )

    for lane in range(NUM_LANES):
        network_script += "connect_bd_net [get_bd_ports input_data_lane_%i] [get_bd_pins fifo_0_concat/in%i]\n"%(lane, lane, )
    network_script += "connect_bd_net [get_bd_pins fifo_0_concat/Dout] [get_bd_pins fifo_0/din]\n"

    network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_0/clk]\n"
    network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins fifo_0/wr_en]\n"
    network_script += "connect_bd_net [get_bd_pins fifo_0/full] [get_bd_pins input_ready_negate/Op1]\n"
    network_script += "connect_bd_net [get_bd_ports input_ready] [get_bd_pins input_ready_negate/Res]\n\n"

    LAST_LAYER = len(layers) - 1
    layer_width  = input_dims["width"]
    layer_height = input_dims["height"]
    layer_depth  = input_dims["depth"]
    data_width   = 1

    for layer, layer_details in enumerate(layers):
        # Generate Program
        if   layer_details["type"] == "conv":
            # Generate layer's program files
            conv.generate_layer(
                network_folder,
                "layer_%i"%(layer),
                layer_width,
                layer_height,
                layer_depth,
                layer_details["kernals"],
                NUM_LANES,
                use_BRAMs
            )

            # Update layer variables
            layer_width  = layer_width
            layer_height = layer_height
            layer_depth  = layer_details["kernals"]
            data_width   = 1
        elif layer_details["type"] == "pool":
            # Generate layer's program files
            pool.generate_layer(
                network_folder,
                "layer_%i"%(layer),
                layer_width,
                layer_height,
                layer_depth,
                NUM_LANES,
                use_BRAMs
            )

            # Update layer variables
            layer_width  = int(layer_width/2)
            layer_height = int(layer_height/2)
            layer_depth  = int(layer_depth)
            data_width   = 1
        elif layer_details["type"] == "dense":
            # Generate layer's program files
            dense.generate_layer(
                network_folder,
                "layer_%i"%(layer),
                layer_width * layer_height * layer_depth,
                layer_details["neurons"],
                NUM_LANES,
                use_BRAMs
            )

            # Update layer variables
            layer_width  = 1
            layer_height = 1
            layer_depth  = layer_details["neurons"]
            data_width   = 1
        elif layer_details["type"] == "acc":
            next_data_width   = tc_utils.unsigned.width(layer_width * layer_height * layer_depth)

            # Generate layer's program files
            acc.generate_layer(
                network_folder,
                "layer_%i"%(layer),
                layer_width * layer_height * layer_depth,
                layer_details["neurons"],
                NUM_LANES,
                use_BRAMs
            )

            # Update layer variables
            layer_width  = 1
            layer_height = 1
            layer_depth  = layer_details["neurons"]
            data_width   = next_data_width
        else:
            raise ValueError("Unknoen layer type, %s"%(str(layer_details["type"]), ) )

        # Generate layer's toolchain files
        run_toolchain(
            program     = network_folder + "\\layer_%i_program.fpea"%(layer, ),
            parameters  = network_folder + "\\layer_%i_parameters.json"%(layer, ),
            generics    = network_folder + "\\layer_%i_generics.json"%(layer, ),
            output_dir  = network_folder + "\\toolchain_files",
            processor_name      = "layer_%i"%(layer, ),
            concat_naming       = True,
            force_generation    = True
        )

        network_script += "create_bd_cell -type module -reference layer_%i_inst layer_%i\n\n"%(layer, layer, )

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 layer_%i_kickoff_concat\n"%(layer, )
        if layer == 0:
            network_script += "set_property -dict [list CONFIG.NUM_PORTS {2}] [get_bd_cells layer_%i_kickoff_concat]\n"%(layer, )
        else:
            network_script += "set_property -dict [list CONFIG.NUM_PORTS {3}] [get_bd_cells layer_%i_kickoff_concat]\n\n"%(layer, )

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_reduced_logic:2.0 layer_%i_kickoff_reduce\n"%(layer, )
        if layer == 0:
            network_script += "set_property -dict [list CONFIG.C_SIZE {2}] [get_bd_cells layer_%i_kickoff_reduce]\n\n"%(layer, )
        else:
            network_script += "set_property -dict [list CONFIG.C_SIZE {3}] [get_bd_cells layer_%i_kickoff_reduce]\n\n"%(layer, )

        if layer != 0:
            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 layer_%i_running_negate\n"%(layer - 1, )
            network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
            network_script += "CONFIG.C_OPERATION {not} "
            network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells layer_%i_running_negate]\n\n"%(layer - 1, )

        output_size = layer_width * layer_height * layer_depth
        output_size_pot = 2**math.ceil(math.log(output_size, 2))

        input_FIFO  = layer
        output_FIFO = layer + 1

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_%i\n"%(output_FIFO, )
        network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
        network_script += "CONFIG.Input_Data_Width {%i} "%(NUM_LANES * data_width, )
        network_script += "CONFIG.Input_Depth {%i} "%(output_size_pot, )
        network_script += "CONFIG.Output_Data_Width {%i} "%(NUM_LANES * data_width, )
        network_script += "CONFIG.Output_Depth {%i} "%(output_size_pot, )
        network_script += "CONFIG.Reset_Pin {false} "
        network_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
        network_script += "CONFIG.Use_Dout_Reset {false} "
        network_script += "CONFIG.Use_Extra_Logic {true} "
        network_script += "CONFIG.Data_Count_Width {10} "
        network_script += "CONFIG.Write_Data_Count_Width {10} "
        network_script += "CONFIG.Read_Data_Count_Width {10} "
        if layer != LAST_LAYER:
            network_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
        else:
            network_script += "CONFIG.Programmable_Full_Type {No_Programmable_Full_Threshold} "
        network_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(output_size - 1, )
        network_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(output_size - 2, )
        network_script += "CONFIG.Empty_Threshold_Assert_Value {4} "
        network_script += "CONFIG.Empty_Threshold_Negate_Value {5}] [get_bd_cells fifo_%i]\n"%(output_FIFO, )

        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:2.1 fifo_%i_concat\n"%(output_FIFO, )
        network_script += "set_property -dict [list CONFIG.NUM_PORTS {%i}] [get_bd_cells fifo_%i_concat]\n"%(NUM_LANES, output_FIFO, )

        for lane in range(NUM_LANES):
            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlslice:1.0 layer_%i_input_slice_lane_%i\n"%(layer, lane, )
            network_script += "set_property -dict [list CONFIG.DIN_WIDTH {%i} "%(NUM_LANES, )
            network_script += "CONFIG.DIN_FROM {%i} "%(lane, )
            network_script += "CONFIG.DIN_TO {%i} "%(lane, )
            network_script += "CONFIG.DOUT_WIDTH {1}] [get_bd_cells layer_%i_input_slice_lane_%i]\n\n"%(layer, lane, )

        for lane in range(NUM_LANES):
            network_script += "connect_bd_net [get_bd_pins layer_%i/LANE_%i_PUT_FIFO_0_data] [get_bd_pins fifo_%i_concat/in%i]\n"%(layer, lane, output_FIFO, lane, )
        network_script += "connect_bd_net [get_bd_pins fifo_%i_concat/Dout] [get_bd_pins fifo_%i/din]\n"%(output_FIFO, output_FIFO, )

        for lane in range(NUM_LANES):
            network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_pins layer_%i_input_slice_lane_%i/Din]\n"%(input_FIFO, layer, lane, )
            network_script += "connect_bd_net [get_bd_pins layer_%i_input_slice_lane_%i/Dout] [get_bd_pins layer_%i/LANE_%i_GET_FIFO_0_data]\n"%(layer, lane, layer, lane, )

        network_script += "create_bd_port -dir O layer_%i_running\n"%(layer, )
        network_script += "connect_bd_net [get_bd_pins layer_%i/running] [get_bd_ports layer_%i_running]\n"%(layer, layer, )

        network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins layer_%i/clock]\n"%(layer, )
        network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_%i/clk]\n"%(output_FIFO, )

        network_script += "connect_bd_net [get_bd_pins layer_%i/LANE_0_GET_FIFO_0_adv] [get_bd_pins fifo_%i/rd_en]\n"%(layer, input_FIFO, )

        network_script += "connect_bd_net [get_bd_pins layer_%i/LANE_0_PUT_FIFO_0_write] [get_bd_pins fifo_%i/wr_en]\n"%(layer, output_FIFO, )

        if layer != 0:
            network_script += "connect_bd_net [get_bd_pins layer_%i/running] [get_bd_pins layer_%i_running_negate/Op1]\n"%(layer - 1, layer - 1, )

        network_script += "connect_bd_net [get_bd_pins fifo_%i/prog_full] [get_bd_pins layer_%i_kickoff_concat/In0]\n"%(input_FIFO, layer, )
        network_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins layer_%i_kickoff_concat/In1]\n"%(output_FIFO, layer, )
        if layer != 0:
            network_script += "connect_bd_net [get_bd_pins layer_%i_running_negate/Res] [get_bd_pins layer_%i_kickoff_concat/In2]\n"%(layer - 1, layer, )
        network_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_concat/Dout] [get_bd_pins layer_%i_kickoff_reduce/Op1]\n"%(layer, layer, )
        network_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_reduce/Res] [get_bd_pins layer_%i/kickoff]\n\n"%(layer, layer, )

    print(data_width)

    # Finish network with output
    for lane in range(NUM_LANES):
        network_script += "create_bd_port -dir O -from %i -to 0 -type data output_data_lane_%i\n"%(data_width - 1, lane, )
    network_script += "create_bd_port -dir I output_read\n"
    network_script += "create_bd_port -dir O output_valid\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 output_valid_negate\n"
    network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
    network_script += "CONFIG.C_OPERATION {not} "
    network_script += "CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells output_valid_negate]\n\n"

    for lane in range(NUM_LANES):
        network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlslice:1.0 output_slice_lane_%i\n"%(lane, )
        network_script += "set_property -dict [list CONFIG.DIN_WIDTH {%i} "%(NUM_LANES * data_width, )
        network_script += "CONFIG.DIN_FROM {%i} "%(data_width * lane + data_width - 1, )
        network_script += "CONFIG.DIN_TO {%i} "%(data_width * lane, )
        network_script += "CONFIG.DOUT_WIDTH {%i}] [get_bd_cells output_slice_lane_%i]\n\n"%(data_width, lane, )

        network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_pins output_slice_lane_%i/Din]\n"%(LAST_LAYER + 1, lane, )
        network_script += "connect_bd_net [get_bd_pins output_slice_lane_%i/Dout] [get_bd_ports output_data_lane_%i]\n"%(lane, lane, )

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

    for lane in range(NUM_LANES):
        tb += "signal input_data_lane_%i  : std_logic_vector ( 0 to 0 );\n"%(lane, )
    tb += "signal input_ready : std_logic_vector ( 0 to 0 );\n"
    tb += "signal input_write : std_logic := '0';\n\n"

    for layer in range(len(layers)):
        tb += "signal layer_%i_running : std_logic;\n"%(layer, )
        tb += "signal layer_%i_frame : integer := -1;\n"%(layer, )

    tb += "\n"

    for lane in range(NUM_LANES):
        tb += "signal output_data_lane_%i  : std_logic_vector (%i downto 0 );\n"%(lane, data_width - 1, )
    tb += "signal output_read  : std_logic := '0';\n"
    tb += "signal output_valid : std_logic_vector ( 0 to 0 );\n"

    tb += "\<begin\n\>"

    tb += "UUT : entity work.network_wrapper(STRUCTURE)\n\>"
    tb += "port map(\n\>"
    tb += "clock => clock,\n\n"

    for lane in range(NUM_LANES):
        tb += "input_data_lane_%i  => input_data_lane_%i,\n"%(lane, lane, )
    tb += "input_ready => input_ready,\n"
    tb += "input_write => input_write,\n\n"

    for layer in range(len(layers)):
        tb += "layer_%i_running => layer_%i_running,\n"%(layer, layer, )
    tb += "\n"

    for lane in range(NUM_LANES):
        tb += "output_data_lane_%i  => output_data_lane_%i,\n"%(lane, lane, )
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
    for lane in range(NUM_LANES):
        tb += "input_data_lane_%i <= \"1\";\n"%(lane, )
    tb += "\n"

    tb += "-- Generate input_write\n"
    tb += "process(clock)\n\>"
    tb += "\<begin\n\>"
    tb += "if rising_edge(clock) then\n\>"
    tb += "input_write <= input_ready(0);\n"
    tb += "\<end if;\n"
    tb += "\<end process;\n\n"

    for layer in range(len(layers)):
        tb += "-- Track layer_%i_frame\n"%(layer, )
        tb += "process(layer_%i_running)\n\>"%(layer, )
        tb += "\<begin\n\>"
        tb += "if rising_edge(layer_%i_running) then\n\>"%(layer, )
        tb += "report \"layer_%i starting frame \" & integer'Image(layer_%i_frame + 1) severity note;\n"%(layer, layer, )
        tb += "layer_%i_frame <= layer_%i_frame + 1;\n"%(layer, layer, )
        tb += "\<end if;\n"
        tb += "if falling_edge(layer_%i_running) then\n\>"%(layer, )
        tb += "report \"layer_%i finished frame \" & integer'Image(layer_%i_frame) severity note;\n"%(layer, layer, )
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
