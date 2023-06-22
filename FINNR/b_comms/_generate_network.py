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
from _layer_types.conv import generate_layer as conv
from _layer_types.pool import generate_layer as pool
from _layer_types.dense import generate_layer as dense
from _layer_types.acc import generate_layer as acc

layer_types_LUT = {
    "conv" : conv,
    "pool" : pool,
    "dense" : dense,
    "acc" : acc,
}

def generation_network(network_name, input_dims, data_path, use_BRAMs=True):

    # Store each network in its own folder
    network_folder = ".\\" + network_name
    try:
        os.makedirs(network_folder + "\\toolchain_files")
    except FileExistsError:
        pass

    # Start tcl script
    network_script = ""
    network_script += "create_bd_design \"network\"\n\n"
    network_script += "create_bd_port -dir I -type clk -freq_hz 100000000 clock\n\n"

    network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconstant:1.1 kickoff_const\n\n"

    # Generate datapath thought block digram
    layer_width  = input_dims["width"]
    layer_height = input_dims["height"]
    layer_depth  = input_dims["depth"]
    data_width   = 1
    fifo = 0
    reg = 0
    layer = 0
    for part in data_path:
        # Handle store parts
        if part["type"] == "FIFO":
            last_store_type = "FIFO"

            fifo_depth = part["depth"](layer_width, layer_height, layer_depth)

            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 fifo_%i\n"%(fifo, )
            network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
            network_script += "CONFIG.Input_Data_Width {%i} "%(data_width, )
            network_script += "CONFIG.Input_Depth {%i} "%(fifo_depth, )
            network_script += "CONFIG.Output_Data_Width {%i} "%(data_width, )
            network_script += "CONFIG.Output_Depth {%i} "%(fifo_depth, )
            network_script += "CONFIG.Reset_Pin {false} "
            network_script += "CONFIG.Reset_Type {Asynchronous_Reset} "
            network_script += "CONFIG.Use_Dout_Reset {false} "
            network_script += "CONFIG.Use_Extra_Logic {true} "
            network_script += "CONFIG.Data_Count_Width {10} "
            network_script += "] [get_bd_cells fifo_%i]\n"%(fifo, )
            network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins fifo_%i/clk]\n\n"%(fifo, )


            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 FIFO_%i_empty_negate\n"%(fifo, )
            network_script += "set_property -dict [list CONFIG.C_SIZE {1} CONFIG.C_OPERATION {not} ] [get_bd_cells FIFO_%i_empty_negate]\n\n"%(fifo, )
            network_script += "connect_bd_net [get_bd_pins fifo_%i/empty] [get_bd_pins FIFO_%i_empty_negate/Op1]\n\n"%(fifo, fifo, )


            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 FIFO_%i_full_negate\n"%(fifo, )
            network_script += "set_property -dict [list CONFIG.C_SIZE {1} CONFIG.C_OPERATION {not} ] [get_bd_cells FIFO_%i_full_negate]\n\n"%(fifo, )
            network_script += "connect_bd_net [get_bd_pins fifo_%i/full] [get_bd_pins FIFO_%i_full_negate/Op1]\n\n"%(fifo, fifo, )

            if layer != 0:
                network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins fifo_%i/din]\n"%(layer - 1, fifo, )
                network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins fifo_%i/wr_en]\n"%(layer  - 1, fifo, )
                network_script += "connect_bd_net [get_bd_pins FIFO_%i_full_negate/Res] [get_bd_pins layer_%i/PUT_FIFO_0_ready]\n\n"%(fifo, layer  - 1, )

            fifo += 1
        elif part["type"] == "reg":
            last_store_type = "reg"

            # Generate required modules
            if reg == 0:
                HDL_generator.generate(
                    "basic.register",
                    "passthrought_along_reg",
                    {
                        "has_enable" : True,
                        "force_on_init" : False,
                        "has_sync_force" : False,
                        "has_async_force" : False,
                    },
                    HDL_output_path=network_folder,
                    concat_naming = False,
                    force_generation = True
                )

                HDL_generator.generate(
                    "basic.RS_FF_latch",
                    "passthrought_along_RSFF",
                    {
                        "hardcoded_init" : "0",
                        "has_enable" : False,
                        "clocked" : True,
                    },
                    HDL_output_path=network_folder,
                    concat_naming = False,
                    force_generation = True
                )

            network_script += "create_bd_cell -type module -reference passthrought_along_reg reg_%i\n"%(reg, )
            network_script += "set_property -dict [list CONFIG.data_width {%i}] [get_bd_cells reg_%i]\n\n"%(data_width, reg, )

            network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins reg_%i/clock]\n"%(reg, )

            if layer != 0:
                network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins reg_%i/data_in]\n"%(layer -1, reg, )
                network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins reg_%i/enable]\n"%(layer -1, reg, )
            network_script += "\n"


            network_script += "create_bd_cell -type module -reference passthrought_along_RSFF RSFF_%i\n"%(reg, )
            network_script += "set_property -dict [list CONFIG.Pre_reset {true} CONFIG.Pre_set {false}] [get_bd_cells RSFF_%i]\n"%(reg, )

            network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins RSFF_%i/clock]\n"%(reg, )
            if layer != 0:
                network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins RSFF_%i/S]\n"%(layer -1, reg, )
            network_script += "\n"

            network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 RSFF_%i_negate\n"%(reg, )
            network_script += "set_property -dict [list CONFIG.C_SIZE {1} CONFIG.C_OPERATION {not} CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells RSFF_%i_negate]\n\n"%(reg, )

            network_script += "connect_bd_net [get_bd_pins RSFF_%i/Q] [get_bd_pins RSFF_%i_negate/Op1]\n"%(reg, reg, )
            if layer != 0:
                network_script += "connect_bd_net [get_bd_pins RSFF_%i_negate/Res] [get_bd_pins layer_%i/PUT_FIFO_0_ready]\n"%(reg, layer -1, )
            network_script += "\n"

            reg += 1
        # Generate FPE parts
        else:
            if   part["type"] == "conv":
                # Generate layer's program files
                conv.generate_layer(
                    network_folder,
                    "layer_%i"%(layer),
                    layer_width,
                    layer_height,
                    layer_depth,
                    part["kernals"],
                    use_BRAMs
                )

                # Update layer variables
                layer_width  = layer_width
                layer_height = layer_height
                layer_depth  = part["kernals"]
                data_width   = 1
            elif part["type"] == "pool":
                # Generate layer's program files
                pool.generate_layer(
                    network_folder,
                    "layer_%i"%(layer),
                    layer_width,
                    layer_height,
                    layer_depth,
                    use_BRAMs
                )

                # Update layer variables
                layer_width  = int(layer_width/2)
                layer_height = int(layer_height/2)
                layer_depth  = int(layer_depth)
                data_width   = 1
            elif part["type"] == "dense":
                # Generate layer's program files
                dense.generate_layer(
                    network_folder,
                    "layer_%i"%(layer),
                    layer_width * layer_height * layer_depth,
                    part["neurons"],
                    use_BRAMs
                )

                # Update layer variables
                layer_width  = 1
                layer_height = 1
                layer_depth  = part["neurons"]
                data_width   = 1
            elif part["type"] == "acc":
                next_data_width   = tc_utils.unsigned.width(layer_width * layer_height * layer_depth)

                # Generate layer's program files
                acc.generate_layer(
                    network_folder,
                    "layer_%i"%(layer),
                    layer_width * layer_height * layer_depth,
                    part["neurons"],
                    use_BRAMs
                )

                # Update layer variables
                layer_width  = 1
                layer_height = 1
                layer_depth  = part["neurons"]
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

            network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins layer_%i/clock]\n"%(layer, )
            network_script += "connect_bd_net [get_bd_pins kickoff_const/dout] [get_bd_pins layer_%i/kickoff]\n"%(layer, )
            network_script += "create_bd_port -dir O layer_%i_running\n"%(layer, )
            network_script += "connect_bd_net [get_bd_pins /layer_%i/running] [get_bd_ports layer_%i_running]\n\n"%(layer, layer, )


            if last_store_type == "FIFO":
                network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(fifo - 1, layer, )
                network_script += "connect_bd_net [get_bd_pins fifo_%i/rd_en] [get_bd_pins layer_%i/GET_FIFO_0_adv]\n"%(fifo - 1, layer, )
                network_script += "connect_bd_net [get_bd_pins FIFO_%i_empty_negate/Res] [get_bd_pins layer_%i/GET_FIFO_0_valid]\n\n"%(fifo - 1, layer, )
            elif last_store_type == "reg":
                pass
                network_script += "connect_bd_net [get_bd_pins reg_%i/data_out] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(reg - 1, layer, )
                network_script += "connect_bd_net [get_bd_pins RSFF_%i/Q] [get_bd_pins layer_%i/GET_FIFO_0_valid]\n"%(reg - 1, layer, )
                network_script += "connect_bd_net [get_bd_pins layer_%i/GET_FIFO_0_adv] [get_bd_pins RSFF_%i/R]\n"%(layer, reg - 1, )
            else:
                raise ValueError("Unknow last_store_type, " + str(last_store_type))
            layer += 1

    # Connect data input
    network_script += "create_bd_port -dir I -from 0 -to 0 -type data input_data\n"
    network_script += "create_bd_port -dir I input_write\n"
    network_script += "create_bd_port -dir O input_ready\n\n"

    if data_path[0]["type"] == "FIFO":
        network_script += "connect_bd_net [get_bd_ports input_data] [get_bd_pins fifo_0/din]\n"
        network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins fifo_0/wr_en]\n"
        network_script += "connect_bd_net [get_bd_pins FIFO_0_full_negate/Res] [get_bd_ports input_ready]\n\n"
    elif data_path[0]["type"] == "reg":
        pass
        network_script += "connect_bd_net [get_bd_ports input_data] [get_bd_pins reg_0/data_in]\n"
        network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins reg_0/enable]\n"
        network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins RSFF_0/S]\n"
        network_script += "connect_bd_net [get_bd_pins RSFF_0_negate/Res] [get_bd_ports input_ready]\n"
    else:
        raise ValueError("Unknow data_path[0][\"type\"], " + str(data_path[0]["type"]))

    # Connect data output

    network_script += "create_bd_port -dir O -from %i -to 0 -type data output_data\n"%(data_width - 1, )
    network_script += "create_bd_port -dir I output_read\n"
    network_script += "create_bd_port -dir O output_valid\n\n"

    if data_path[-1]["type"] == "FIFO":
        last_fifo = fifo - 1
        network_script += "connect_bd_net [get_bd_pins fifo_%i/dout] [get_bd_ports output_data]\n"%(last_fifo, )
        network_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins fifo_%i/rd_en]\n"%(last_fifo, )
        network_script += "connect_bd_net [get_bd_pins FIFO_%i_empty_negate/Res] [get_bd_ports output_valid]\n\n"%(last_fifo, )
    elif data_path[-1]["type"] == "reg":
        last_reg = reg - 1
        network_script += "connect_bd_net [get_bd_pins reg_%i/data_out] [get_bd_ports output_data]\n"%(last_reg, )
        network_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins RSFF_%i/R]\n"%(last_reg, )
        network_script += "connect_bd_net [get_bd_pins RSFF_%i/Q] [get_bd_ports output_valid]\n\n"%(last_reg, )
    else:
        raise ValueError("Unknow data_path[-1][\"type\"], " + str(data_path[-1]["type"]))

    # Finish tcl script
    network_script += "save_bd_design\n"
    network_script += "close_bd_design [current_bd_design]\n\n"

    dir_pathway = os.path.dirname(__file__).replace("\\", "/")
    network_script += "make_wrapper -files [get_files %s/%s/measuring/measuring.srcs/sources_1/bd/network/network.bd] -top\n"%(dir_pathway, network_name, )
    network_script += "add_files -norecurse %s/%s/measuring/measuring.srcs/sources_1/bd/network/hdl/network_wrapper.vhd\n"%(dir_pathway, network_name, )
    network_script += "set_property top network_wrapper [current_fileset]\n\n"

    with open("%s\\gen_block_diagram.tcl"%(network_folder, ), "w") as f:
        f.write(network_script)

    # Create testbench
    if True:
        NUM_LAYERS =  layer
        tb = gen_utils.indented_string()

        tb += "library IEEE;\n"
        tb += "use IEEE.std_logic_1164.ALL;\n\n"

        tb += "entity testbench is\n"
        tb += "end testbench;\n\n"

        tb += "architecture arch of testbench is\n\>"
        tb += "signal clock : std_logic := '0';\n\n"

        tb += "signal input_data  : std_logic_vector ( 0 to 0 );\n"
        tb += "signal input_write : std_logic := '0';\n\n"
        if data_path[0]["type"] == "FIFO":
            tb += "signal input_ready : std_logic_vector ( 0 to 0 );\n"
        elif data_path[0]["type"] == "reg":
            tb += "signal input_ready : std_logic;\n"
        else:
            raise ValueError("Unknow data_path[0][\"type\"], " + str(data_path[0]["type"]))

        for layer in range(NUM_LAYERS):
            tb += "signal layer_%i_running : std_logic;\n"%(layer, )
            tb += "signal layer_%i_frame : integer := -1;\n"%(layer, )

        tb += "\n"

        tb += "signal output_data  : std_logic_vector (%i downto 0 );\n"%(next_data_width - 1, )
        tb += "signal output_read  : std_logic := '0';\n"
        if data_path[-1]["type"] == "FIFO":
            tb += "signal output_valid : std_logic_vector ( 0 to 0 );\n"
        elif data_path[-1]["type"] == "reg":
            tb += "signal output_valid : std_logic;\n"
        else:
            raise ValueError("Unknow data_path[-1][\"type\"], " + str(data_path[-1]["type"]))

        tb += "\<begin\n\>"

        tb += "UUT : entity work.network_wrapper(STRUCTURE)\n\>"
        tb += "port map(\n\>"
        tb += "clock => clock,\n\n"

        tb += "input_data  => input_data,\n"
        tb += "input_ready => input_ready,\n"
        tb += "input_write => input_write,\n\n"

        for layer in range(NUM_LAYERS):
            tb += "layer_%i_running => layer_%i_running,\n"%(layer, layer, )
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
        tb += "input_data <= \"1\";\n\n"

        tb += "-- Generate input_write\n"
        tb += "process(clock)\n\>"
        tb += "\<begin\n\>"
        tb += "if rising_edge(clock) then\n\>"
        if data_path[0]["type"] == "FIFO":
            tb += "input_write <= input_ready(0);\n"
        elif data_path[0]["type"] == "reg":
            tb += "input_write <= input_ready\n"
        else:
            raise ValueError("Unknow data_path[0][\"type\"], " + str(data_path[0]["type"]))
        tb += "\<end if;\n"
        tb += "\<end process;\n\n"

        for layer in range(NUM_LAYERS):
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
        if data_path[-1]["type"] == "FIFO":
            tb += "output_read <= output_valid(0);\n"
        elif data_path[-1]["type"] == "reg":
            tb += "output_read <= output_valid;\n"
        else:
            raise ValueError("Unknow data_path[-1][\"type\"], " + str(data_path[-1]["type"]))
        tb += "\<end if;\n"
        tb += "\<end process;\n\n"

        tb += "\<end arch;\n"

        with open("%s\\testbench.vhd"%(network_folder, ), "w") as f:
            f.write(str(tb))

    return network_folder
