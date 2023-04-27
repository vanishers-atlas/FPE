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
from _layer_types.conv_frame    import generate_layer as conv_frame
from _layer_types.conv_row      import generate_layer as conv_row
from _layer_types.conv_batch    import generate_layer as conv_batch
conv_types = {
	"conv_frame" : conv_frame,
	"conv_row"   : conv_row,
	"conv_batch" : conv_batch,
}

from _layer_types.pool_frame    import generate_layer as pool_frame
from _layer_types.pool_pair     import generate_layer as pool_pair
from _layer_types.pool_row      import generate_layer as pool_row
from _layer_types.pool_batch    import generate_layer as pool_batch
pool_types = {
	"pool_frame" : pool_frame,
	"pool_pair"  : pool_pair,
	"pool_row"   : pool_row,
	"pool_batch" : pool_batch,
}

from _layer_types.dense_frame   import generate_layer as dense_frame
from _layer_types.dense_batch   import generate_layer as dense_batch
dense_types = {
	"dense_frame" : dense_frame,
	"dense_batch" : dense_batch,
}

from _layer_types.acc_frame     import generate_layer as acc_frame
from _layer_types.acc_batch     import generate_layer as acc_batch
acc_types = {
	"acc_frame" : acc_frame,
	"acc_batch" : acc_batch,
}

def generation_network(network_name, input_dims, FPEs, buffers, use_BRAMs=True):

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

	# Generate datapath thought block digram
	layer_width  = input_dims["width"]
	layer_height = input_dims["height"]
	layer_depth  = input_dims["depth"]
	data_width   = 1
	for layer, FPE in enumerate(FPEs):
		if   FPE["type"] in conv_types.keys():
			if FPE["type"].endswith("_batch"):
				# Generate layer's program files
				FPE["batch_size"] = FPE["batch_size"](layer_width, layer_height, layer_depth)
				conv_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					layer_width,
					layer_height,
					layer_depth,
					FPE["kernals"],
					FPE["batch_size"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = conv_types[FPE["type"]].compute_kickoff_data(layer_width, layer_height, layer_depth, FPE["kernals"], FPE["batch_size"])
				buffers[layer + 1]["empty_level"] = conv_types[FPE["type"]].compute_kickoff_space(layer_width, layer_height, layer_depth, FPE["kernals"], FPE["batch_size"])
			else:
				# Generate layer's program files
				conv_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					layer_width,
					layer_height,
					layer_depth,
					FPE["kernals"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = conv_types[FPE["type"]].compute_kickoff_data(layer_width, layer_height, layer_depth, FPE["kernals"])
				buffers[layer + 1]["empty_level"] = conv_types[FPE["type"]].compute_kickoff_space(layer_width, layer_height, layer_depth, FPE["kernals"])

			# Update layer variables
			layer_width  = layer_width
			layer_height = layer_height
			layer_depth  = FPE["kernals"]
			data_width   = 1
		elif FPE["type"] in pool_types.keys():
			# Generate layer's program files
			if FPE["type"].endswith("_batch"):
				FPE["batch_size"] = FPE["batch_size"](layer_width, layer_height, layer_depth)
				pool_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					layer_width,
					layer_height,
					layer_depth,
					FPE["batch_size"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = pool_types[FPE["type"]].compute_kickoff_data(layer_height, layer_width, layer_depth, FPE["batch_size"])
				buffers[layer + 1]["empty_level"] = pool_types[FPE["type"]].compute_kickoff_space(layer_height, layer_width, layer_depth, FPE["batch_size"])
			else:
				pool_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					layer_width,
					layer_height,
					layer_depth,
					use_BRAMs
				)

				buffers[layer]["full_level"] = pool_types[FPE["type"]].compute_kickoff_data(layer_height, layer_width, layer_depth)
				buffers[layer + 1]["empty_level"] = pool_types[FPE["type"]].compute_kickoff_space(layer_height, layer_width, layer_depth)

			# Update layer variables
			layer_width  = int(layer_width/2)
			layer_height = int(layer_height/2)
			layer_depth  = int(layer_depth)
			data_width   = 1
		elif FPE["type"] in dense_types.keys():
			# Generate layer's program files
			input_neurons = layer_width * layer_height * layer_depth
			if FPE["type"].endswith("_batch"):
				FPE["batch_size"] = FPE["batch_size"](layer_width, layer_height, layer_depth)
				dense_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					input_neurons,
					FPE["neurons"],
					FPE["batch_size"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = dense_types[FPE["type"]].compute_kickoff_data(input_neurons, FPE["neurons"], FPE["batch_size"])
				buffers[layer + 1]["empty_level"] = dense_types[FPE["type"]].compute_kickoff_space(input_neurons, FPE["neurons"], FPE["batch_size"])
			else:
				dense_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					input_neurons,
					FPE["neurons"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = dense_types[FPE["type"]].compute_kickoff_data(input_neurons, FPE["neurons"])
				buffers[layer + 1]["empty_level"] = dense_types[FPE["type"]].compute_kickoff_space(input_neurons, FPE["neurons"])

			# Update layer variables
			layer_width  = 1
			layer_height = 1
			layer_depth  = FPE["neurons"]
			data_width   = 1
		elif FPE["type"] in acc_types.keys():
			next_data_width   = tc_utils.unsigned.width(layer_width * layer_height * layer_depth)

			# Generate layer's program files+
			input_neurons = layer_width * layer_height * layer_depth
			if FPE["type"].endswith("_batch"):
				FPE["batch_size"] = FPE["batch_size"](layer_width, layer_height, layer_depth)
				acc_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					input_neurons,
					FPE["neurons"],
					FPE["batch_size"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = acc_types[FPE["type"]].compute_kickoff_data(input_neurons, FPE["neurons"], FPE["batch_size"])
				buffers[layer + 1]["empty_level"] = acc_types[FPE["type"]].compute_kickoff_space(input_neurons, FPE["neurons"], FPE["batch_size"])
			else:
				acc_types[FPE["type"]].generate_layer(
					network_folder,
					"layer_%i"%(layer),
					input_neurons,
					FPE["neurons"],
					use_BRAMs
				)

				buffers[layer]["full_level"] = acc_types[FPE["type"]].compute_kickoff_data(input_neurons, FPE["neurons"])
				buffers[layer + 1]["empty_level"] = acc_types[FPE["type"]].compute_kickoff_space(input_neurons, FPE["neurons"])

			# Update layer variables
			layer_width  = 1
			layer_height = 1
			layer_depth  = FPE["neurons"]
			data_width   = next_data_width
		else:
			raise ValueError("Unknoen layer type, %s"%(str(layer_details["type"]), ) )

		buffers[layer + 1]["data_width"] = data_width

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

		network_script += "create_bd_cell -type module -reference layer_%i_inst layer_%i\n"%(layer, layer, )
		network_script += "\n"

		network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins layer_%i/clock]\n"%(layer, )
		network_script += "create_bd_port -dir O layer_%i_running\n"%(layer, )
		network_script += "connect_bd_net [get_bd_pins /layer_%i/running] [get_bd_ports layer_%i_running]\n\n"%(layer, layer, )
		network_script += "\n"

		network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 layer_%i_kickoff_and\n"%(layer, )
		network_script += "set_property -dict [list CONFIG.C_SIZE {1} CONFIG.C_OPERATION {and} ] [get_bd_cells layer_%i_kickoff_and]\n"%(layer, )
		network_script += "\n"

		network_script += "connect_bd_net [get_bd_pins layer_%i_kickoff_and/Res] [get_bd_pins layer_%i/kickoff]\n"%(layer, layer,)
		network_script += "\n"

	reg_gened = False
	for buffer, details in enumerate(buffers):
		# Handle store parts
		if details["type"] == "FIFO":
			last_store_type = "FIFO"

			try:
				full_level = details["full_level"]
			except Exception as e:
				full_level = None
			try:
				empty_level = details["empty_level"]
			except Exception as e:
				empty_level = None
			try:
				fifo_depth =  details["fifo_depth"]
				assert "full_level"  not in buffer.keys() or details["fifo_depth"] >= buffer["full_level"]
				assert "empty_level" not in buffer.keys() or details["fifo_depth"] >= buffer["empty_level"]

			except Exception as e:
				if full_level and empty_level:
					fifo_depth = 2**math.ceil(math.log(max(full_level, empty_level), 2))
				elif full_level:
					fifo_depth = 2**math.ceil(math.log(full_level, 2))
				elif empty_level:
					fifo_depth = 2**math.ceil(math.log(empty_level, 2))
				else:
					raise ValueError()
			data_width = details["data_width"]

			network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:fifo_generator:13.2 buffer_%i_fifo\n"%(buffer, )
			network_script += "set_property -dict [list CONFIG.Performance_Options {First_Word_Fall_Through} "
			network_script += "CONFIG.Input_Data_Width {%i} "%(data_width, )
			network_script += "CONFIG.Input_Depth {%i} "%(fifo_depth, )
			network_script += "CONFIG.Output_Data_Width {%i} "%(data_width, )
			network_script += "CONFIG.Output_Depth {%i} "%(fifo_depth, )
			network_script += "CONFIG.Reset_Pin {false} "
			if full_level:
				network_script += "CONFIG.Programmable_Full_Type {Single_Programmable_Full_Threshold_Constant} "
				network_script += "CONFIG.Full_Threshold_Assert_Value {%i} "%(full_level - 2, )
				network_script += "CONFIG.Full_Threshold_Negate_Value {%i} "%(full_level - 3, )
			if empty_level:
				network_script += "CONFIG.Programmable_Empty_Type {Single_Programmable_Empty_Threshold_Constant} "
				network_script += "CONFIG.Empty_Threshold_Assert_Value {%i} "%(empty_level - 2, )
				network_script += "CONFIG.Empty_Threshold_Negate_Value {%i} "%(empty_level - 2, )
			network_script += "] [get_bd_cells buffer_%i_fifo]\n"%(buffer, )

			network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins buffer_%i_fifo/clk]\n\n"%(buffer, )

			# Connect buffer to last layer
			if buffer != 0:
				fpe = buffer - 1
				network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_data] [get_bd_pins buffer_%i_fifo/din]\n"%(fpe, buffer, )
				network_script += "connect_bd_net [get_bd_pins layer_%i/PUT_FIFO_0_write] [get_bd_pins buffer_%i_fifo/wr_en]\n"%(fpe, buffer, )
				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/prog_empty] [get_bd_pins layer_%i_kickoff_and/Op1]\n\n"%(buffer, fpe, )
			else:
				network_script += "create_bd_port -dir I -from 0 -to 0 -type data input_data\n"
				network_script += "create_bd_port -dir I input_write\n"
				network_script += "create_bd_port -dir O input_ready\n\n"

				network_script += "connect_bd_net [get_bd_ports input_data] [get_bd_pins buffer_%i_fifo/din]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_ports input_write] [get_bd_pins buffer_%i_fifo/wr_en]\n\n"%(buffer, )

				network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 input_ready_negate\n"
				network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
				network_script += "CONFIG.C_OPERATION {not} "
				network_script += "] [get_bd_cells input_ready_negate]\n\n"

				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/full] [get_bd_pins input_ready_negate/Op1]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_pins input_ready_negate/Res] [get_bd_ports input_ready]\n\n"

			# Connect Buffer to next layer
			if buffer != len(buffers) - 1:
				fpe = buffer
				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/dout] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(buffer, fpe, )
				network_script += "connect_bd_net [get_bd_pins layer_%i/GET_FIFO_0_adv] [get_bd_pins buffer_%i_fifo/rd_en]\n"%(fpe, buffer, )
				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/prog_full] [get_bd_pins layer_%i_kickoff_and/Op2]\n\n"%(buffer, fpe, )
			else:
				network_script += "create_bd_port -dir O -from %i -to 0 -type data output_data\n"%(data_width - 1, )
				network_script += "create_bd_port -dir I output_read\n"
				network_script += "create_bd_port -dir O output_valid\n\n"

				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/dout] [get_bd_ports output_data]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins buffer_%i_fifo/rd_en]\n"%(buffer, )

				network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 output_valid_negate\n"
				network_script += "set_property -dict [list CONFIG.C_SIZE {1} "
				network_script += "CONFIG.C_OPERATION {not} "
				network_script += "] [get_bd_cells output_valid_negate]\n\n"

				network_script += "connect_bd_net [get_bd_pins buffer_%i_fifo/empty] [get_bd_pins output_valid_negate/Op1]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_pins output_valid_negate/Res] [get_bd_ports output_valid]\n\n"

		elif details["type"] == "reg":
			# Generate required modules
			if not reg_gened:
				reg_gened = True
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

			print(buffer)
			assert "fifo_depth"  not in details.keys() or details["fifo_depth"]  == 1
			assert "full_level"  not in details.keys() or details["full_level"]  == 1
			assert "empty_level" not in details.keys() or details["empty_level"] == 1

			data_width = details["data_width"]

			network_script += "create_bd_cell -type module -reference passthrought_along_reg buffer_%i_reg\n"%(buffer, )
			network_script += "set_property -dict [list CONFIG.data_width {%i}] [get_bd_cells buffer_%i_reg]\n\n"%(data_width, buffer, )

			network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins buffer_%i_reg/clock]\n"%(buffer, )

			network_script += "create_bd_cell -type module -reference passthrought_along_RSFF buffer_%i_RSFF\n"%(buffer, )
			network_script += "set_property -dict [list CONFIG.Pre_reset {true} CONFIG.Pre_set {false}] [get_bd_cells buffer_%i_RSFF]\n"%(buffer, )

			network_script += "connect_bd_net [get_bd_ports clock] [get_bd_pins buffer_%i_RSFF/clock]\n"%(buffer, )

			network_script += "create_bd_cell -type ip -vlnv xilinx.com:ip:util_vector_logic:2.0 buffer_%i_RSFF_negate\n"%(buffer, )
			network_script += "set_property -dict [list CONFIG.C_SIZE {1} CONFIG.C_OPERATION {not} CONFIG.LOGO_FILE {data/sym_notgate.png}] [get_bd_cells buffer_%i_RSFF_negate]\n\n"%(buffer, )

			# Connect Buffer to next layer
			if buffer != len(buffers) - 1:
				network_script += "connect_bd_net [get_bd_pins buffer_%i_reg/data_out] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(buffer, buffer, )
				network_script += "connect_bd_net [get_bd_pins layer_%i/GET_FIFO_0_adv] [get_bd_pins buffer_%i_RSFF/R]\n\n"%(buffer, buffer, )
			else:
				network_script += "create_bd_port -dir O -from %i -to 0 -type data output_data\n"%(data_width - 1, )
				network_script += "create_bd_port -dir I output_read\n"
				network_script += "create_bd_port -dir O output_valid\n\n"

				network_script += "connect_bd_net [get_bd_pins buffer_%i_reg/data_out] [get_bd_pins layer_%i/GET_FIFO_0_data]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_ports output_read] [get_bd_pins buffer_%i_RSFF/R]\n"%(buffer, )
				network_script += "connect_bd_net [get_bd_pins buffer_%i_RSFF/Q] [get_bd_ports output_valid]\n\n"%(buffer, )


		else:
			raise ValueError("unknown buffer type " + str(details["type"]) )

	# Add look to connect everything together here

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
		NUM_LAYERS =  len(FPEs)
		tb = gen_utils.indented_string()

		tb += "library IEEE;\n"
		tb += "use IEEE.std_logic_1164.ALL;\n\n"

		tb += "entity testbench is\n"
		tb += "end testbench;\n\n"

		tb += "architecture arch of testbench is\n\>"
		tb += "signal clock : std_logic := '0';\n\n"

		tb += "signal input_data  : std_logic_vector ( 0 to 0 );\n"
		tb += "signal input_ready : std_logic_vector ( 0 to 0 );\n"
		tb += "signal input_write : std_logic := '0';\n\n"

		for layer in range(NUM_LAYERS):
			tb += "signal layer_%i_running : std_logic;\n"%(layer, )
			tb += "signal layer_%i_frame : integer := -1;\n"%(layer, )

		tb += "\n"

		tb += "signal output_data  : std_logic_vector (%i downto 0 );\n"%(next_data_width - 1, )
		tb += "signal output_read  : std_logic := '0';\n"
		tb += "signal output_valid : std_logic_vector ( 0 to 0 );\n"

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
		tb += "input_write <= input_ready(0);\n"
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
		tb += "output_read <= output_valid(0);\n"
		tb += "\<end if;\n"
		tb += "\<end process;\n\n"

		tb += "\<end arch;\n"

		with open("%s\\testbench.vhd"%(network_folder, ), "w") as f:
			f.write(str(tb))

	return network_folder
