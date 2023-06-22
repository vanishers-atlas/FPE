# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain.HDL_generation.utils.indented_string import IndentedString

import json
import math
import re

def compute_popcount(data_cols, data_rows, data_depth):
	return tc_utils.unsigned.width(3 * 3 * data_depth)

def compute_parallelism_factor(data_cols, data_rows, data_depth):
	width = compute_popcount(data_cols, data_rows, data_depth)
	for p_fact in [32, 16, 8, 4, 2]:
		if width * p_fact + p_fact - 1 <= 48:
			return p_fact

mif_gen_test = re.compile("([A-Za-z0-9_]+)(_subblock_([0-9]+)).init_mif")
def generate_layer(path, layer_name, data_cols, data_rows, data_depth, num_kernals, parallelism_factor, use_BRAMs=False, pregened_memfiles=None):
	# Generate toolchain input files
	generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals, parallelism_factor)
	parameters, generics = generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, parallelism_factor, use_BRAMs)

	# Generate mem files
	assert pregened_memfiles == None or type(pregened_memfiles) == list, "invalid ROMs parameter"
	subblocks = {}
	for generic in generics.keys():
		match = mif_gen_test.search(generic)
		if match:
			mem = match.group(1)
			pregen_name = match.group(2)
			subblock = int(match.group(3))
			if pregened_memfiles != None and pregen_name in pregened_memfiles:
				pass
			elif not subblock:
				generate_blank_mem(
					path,
					"%s_%s.mem"%(layer_name, mem, ),
					parameters["data_memories"][mem]["data_width"],
					parameters["data_memories"][mem]["depth"]
				)
			else:
				try:
					subblocks[mem] = max(subblocks[mem], subblock + 1)
				except KeyError as e:
					subblocks[mem] =  subblock + 1

	for mem, num_mifs in subblocks.items():
		print(mem, num_mifs)
		for mif in range(num_mifs):
			generate_blank_mem(
				path,
				"%s_%s_subblock_%s.mem"%(layer_name, mem, mif),
				parameters["data_memories"][mem]["data_width"],
				math.ceil(parameters["data_memories"][mem]["depth"]/num_mifs)
			)



def generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals, parallelism_factor):
	fpea = IndentedString()

	fpea += "{\>\n"

	fpea += "// Define layer constants\n"
	fpea += "DEF data_rows   %i ;\n"%(data_rows, )
	fpea += "DEF data_cols   %i ;\n"%(data_cols, )
	fpea += "DEF data_depth  %i ;\n"%(data_depth, )
	fpea += "DEF num_kernals %i ;\n"%(num_kernals, )
	fpea += "DEF par_factor  %i ;\n"%(parallelism_factor, )
	fpea += "\n"

	fpea += "// Define meaningfully names for Block access managers\n"
	fpea += "DEF act_write  0 ;\n"
	fpea += "DEF act_row_0  1 ;\n"
	fpea += "DEF act_row_1  2 ;\n"
	fpea += "DEF act_row_2  3 ;\n"
	fpea += "DEF kernels    4 ;\n"
	fpea += "DEF thresholds 5 ;\n"
	fpea += "DEF gammas     5 ;\n"
	fpea += "\n"

	fpea += "// Define meaningfully names for reg addresses\n"
	fpea += "DEF collect_a  0 * par_factor ;\n"
	fpea += "DEF collect_b  1 * par_factor ;\n"
	fpea += "DEF row_0_working  0 * par_factor ;\n"
	fpea += "DEF row_1_working  1 * par_factor ;\n"
	fpea += "DEF row_2_working  2 * par_factor ;\n"
	fpea += "DEF packing 3 * par_factor ;\n"
	fpea += "DEF pop_acc 4 * par_factor ;\n"
	fpea += "\n"

	fpea += "DEF masks_addr  num_kernals * (9*data_depth + 2*data_rows*data_cols) ;\n"

	fpea += "// Setup packing area of regfile,\n"
	for i in range(parallelism_factor):
		fpea += "MOV(%i, REG[packing + %i]);\n"%((i + 1)%2, i)
	fpea += "\n"

	fpea += "// Reset BAMs\n"
	fpea += "RESET BAM[act_write];\n"
	fpea += "RESET BAM[act_row_0];\n"
	fpea += "RESET BAM[act_row_1];\n"
	fpea += "RESET BAM[act_row_2];\n"
	fpea += "RESET BAM[thresholds];\n"
	#fpea += "RESET BAM[gammas];\n"
	fpea += "\n"


	fpea += "// Pad first row,\n"
	fpea += "PMOV(par_factor, REG[packing], ACC);\n"
	fpea += "ZOL (data_cols + 2)\n"
	fpea += "{\>\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, ACC, RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "PNOT(par_factor, ACC, REG[packing]) ;\n"
	fpea += "\<}\n"
	fpea += "PNOT(par_factor, ACC, REG[packing]) ;\n"
	fpea += "NOP;\n"
	fpea += "NOP;\n"
	fpea += "\n"


	fpea += "// Handle second row,\n"

	fpea += "// pad first col\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, REG[packing], RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "PNOT(par_factor, ACC, REG[packing]) ;\n"
	fpea += "\n"

	fpea += "// read of middle cols\n"
	fpea += "ZOL (data_depth * data_cols/(2*par_factor))\n"
	fpea += "{\>\n"
	for i in range(parallelism_factor):
		fpea += "MOV( GET[0]<ADV>, REG[collect_a + %i]) ;\n"%(i, )
	for i in range(parallelism_factor):
		fpea += "MOV( GET[0]<ADV>, REG[collect_b + %i]) ;\n"%(i, )
	fpea += "NOP;\n"
	fpea += "PMOV(par_factor, REG[collect_a], RAM[BAM[act_write]<FORWARD>] ) ;\n"
	fpea += "PMOV(par_factor, REG[collect_b], RAM[BAM[act_write]<FORWARD>] ) ;\n"
	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// pad last col\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, REG[packing], RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "\n"


	fpea += "// Process all but last row\n"
	fpea += "ZOL (data_rows - 1)\n"
	fpea += "{\>\n"

	fpea += "// Read in next row,\n"

	fpea += "// pad first col\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, REG[packing], RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "PNOT(par_factor, ACC, REG[packing]) ;\n"
	fpea += "\n"

	fpea += "// read of middle cols\n"
	fpea += "ZOL (data_depth * data_cols/(2*par_factor))\n"
	fpea += "{\>\n"
	for i in range(parallelism_factor):
		fpea += "MOV( GET[0]<ADV>, REG[collect_a + %i]) ;\n"%(i, )
	for i in range(parallelism_factor):
		fpea += "MOV( GET[0]<ADV>, REG[collect_b + %i]) ;\n"%(i, )
	fpea += "NOP;\n"
	fpea += "PMOV(par_factor, REG[collect_a], RAM[BAM[act_write]<FORWARD>] ) ;\n"
	fpea += "PMOV(par_factor, REG[collect_b], RAM[BAM[act_write]<FORWARD>] ) ;\n"
	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// pad last col\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, REG[packing], RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "\n"


	fpea += "// Slide window across rows\n"
	fpea += "ZOL (data_cols)\n"
	fpea += "{\>\n"

	fpea += "// Reset kenral BAM to start at first kernel\n"
	fpea += "RESET BAM[kernels];\n"
	fpea += "\n"

	fpea += "// Process each kernel\n"
	fpea += "ZOL (num_kernals)\n"
	fpea += "{\>\n"

	fpea += "// Clear popcount\n"
	fpea += "MOV (0, REG[pop_acc]);\n"

	fpea += "// Compute popcount\n"
	fpea += "// * 3 for each col of the kernel\n"
	fpea += "ZOL (3 * (data_depth / par_factor) )\n"
	fpea += "{\>\n"

	fpea += "PXNOR (par_factor, RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_0_working] ) ;\n"
	fpea += "PXNOR (par_factor, RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_1_working] ) ;\n"
	fpea += "PXNOR (par_factor, RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_2_working] ) ;\n"

	for p_factor in [16,8,4,2]:
		if (2*p_factor) <= parallelism_factor:
			fpea += "PADD (%i, REG[row_0_working], REG[row_0_working + %i], REG[row_0_working]) ;\n"%(p_factor, p_factor, )
			fpea += "PADD (%i, REG[row_1_working], REG[row_1_working + %i], REG[row_1_working]) ;\n"%(p_factor, p_factor, )
			fpea += "PADD (%i, REG[row_2_working], REG[row_2_working + %i], REG[row_2_working]) ;\n"%(p_factor, p_factor, )
	fpea += "ADD (REG[row_0_working], REG[row_0_working + 1], REG[row_0_working]) ;\n"
	fpea += "ADD (REG[row_1_working], REG[row_1_working + 1], REG[row_1_working]) ;\n"
	fpea += "ADD (REG[row_2_working], REG[row_2_working + 1], REG[row_2_working]) ;\n"
	fpea += "ADD (REG[row_0_working], REG[pop_acc], ACC);\n"
	fpea += "ADD (REG[row_1_working], ACC, ACC);\n"
	fpea += "ADD (REG[row_2_working], ACC, REG[pop_acc]);\n"
	fpea += "\n"
	fpea += "\<}\n"

	fpea += "// Perform thresholding\n"
	fpea += "SUB(ROMA[BAM[thresholds]<FORWARD>], ACC, ACC);\n"
	fpea += "// Move difference sign to bit 0, not masking require as the store to put will remove all but bit 0\n"
	fpea += "LRL(ACC, 1, ACC);\n"
	fpea += "// Difference and gammas use 2 comp. signing, but XNOR converts that tos mathmatic sign function\n"
	fpea += "XNOR ( ACC, ROMA[BAM[gammas]<FORWARD>], PUT[0] ) ;\n"

	fpea += "// Knock acc_row BAMs back for next kernal\n"
	fpea += "SEEK BAM[act_row_0] (3 * data_depth)<BACKWARD>;\n"
	fpea += "SEEK BAM[act_row_1] (3 * data_depth)<BACKWARD>;\n"
	fpea += "SEEK BAM[act_row_2] (3 * data_depth)<BACKWARD>;\n"

	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// Seek acc_row BAMs forward for next col\n"
	fpea += "SEEK BAM[act_row_0] (data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_1] (data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_2] (data_depth)<FORWARD>;\n"

	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// Seek acc_row BAMs forward for next row\n"
	fpea += "SEEK BAM[act_row_0] (2 * data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_1] (2 * data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_2] (2 * data_depth)<FORWARD>;\n"


	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// Handle last row,\n"
	fpea += "PMOV(par_factor, REG[packing], ACC);\n"
	fpea += "ZOL (data_cols + 2)\n"
	fpea += "{\>\n"
	fpea += "ZOL (data_depth/par_factor)\n"
	fpea += "{\>\n"
	fpea += "PMOV(par_factor, ACC, RAM[BAM[act_write]<FORWARD>]);\n"
	fpea += "\<}\n"
	fpea += "PNOT(par_factor, ACC, REG[packing]) ;\n"
	fpea += "\<}\n"
	fpea += "\n"


	fpea += "// Slide window across rows\n"
	fpea += "ZOL (data_cols)\n"
	fpea += "{\>\n"

	fpea += "// Reset kenral BAM to start at first kernel\n"
	fpea += "RESET BAM[kernels];\n"
	fpea += "\n"

	fpea += "// Process each kernel\n"
	fpea += "ZOL (num_kernals)\n"
	fpea += "{\>\n"

	fpea += "// Clear popcount\n"
	fpea += "MOV (0, REG[pop_acc]);\n"

	fpea += "// Compute popcount\n"
	fpea += "// * 3 for each col of the kernel\n"
	fpea += "ZOL (3 * (data_depth / par_factor) )\n"
	fpea += "{\>\n"

	fpea += "PXNOR (par_factor, RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_0_working] ) ;\n"
	fpea += "PXNOR (par_factor, RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_1_working] ) ;\n"
	fpea += "PXNOR (par_factor, RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
	fpea += "PAND  (par_factor, ACC, ROMA[masks_addr], REG[row_2_working] ) ;\n"

	for p_factor in [16,8,4,2]:
		if (2*p_factor) <= parallelism_factor:
			fpea += "PADD (%i, REG[row_0_working], REG[row_0_working + %i], REG[row_0_working]) ;\n"%(p_factor, p_factor, )
			fpea += "PADD (%i, REG[row_1_working], REG[row_1_working + %i], REG[row_1_working]) ;\n"%(p_factor, p_factor, )
			fpea += "PADD (%i, REG[row_2_working], REG[row_2_working + %i], REG[row_2_working]) ;\n"%(p_factor, p_factor, )
	fpea += "ADD (REG[row_0_working], REG[row_0_working + 1], REG[row_0_working]) ;\n"
	fpea += "ADD (REG[row_1_working], REG[row_1_working + 1], REG[row_1_working]) ;\n"
	fpea += "ADD (REG[row_2_working], REG[row_2_working + 1], REG[row_2_working]) ;\n"
	fpea += "ADD (REG[row_0_working], REG[pop_acc], ACC);\n"
	fpea += "ADD (REG[row_1_working], ACC, ACC);\n"
	fpea += "ADD (REG[row_2_working], ACC, REG[pop_acc]);\n"
	fpea += "\n"
	fpea += "\<}\n"

	fpea += "// Perform thresholding\n"
	fpea += "SUB(ROMA[BAM[thresholds]<FORWARD>], ACC, ACC);\n"
	fpea += "// Move difference sign to bit 0, not masking require as the store to put will remove all but bit 0\n"
	fpea += "LRL(ACC, 1, ACC);\n"
	fpea += "// Difference and gammas use 2 comp. signing, but XNOR converts that tos mathmatic sign function\n"
	fpea += "XNOR ( ACC, ROMA[BAM[gammas]<FORWARD>], PUT[0] ) ;\n"

	fpea += "// Knock acc_row BAMs back for next kernal\n"
	fpea += "SEEK BAM[act_row_0] (3 * data_depth)<BACKWARD>;\n"
	fpea += "SEEK BAM[act_row_1] (3 * data_depth)<BACKWARD>;\n"
	fpea += "SEEK BAM[act_row_2] (3 * data_depth)<BACKWARD>;\n"

	fpea += "\<}\n"
	fpea += "\n"

	fpea += "// Seek acc_row BAMs forward for next col\n"
	fpea += "SEEK BAM[act_row_0] (data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_1] (data_depth)<FORWARD>;\n"
	fpea += "SEEK BAM[act_row_2] (data_depth)<FORWARD>;\n"

	fpea += "\<}\n"

	fpea += "NOP;\n"
	fpea += "\<}\n"

	with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
		f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, parallelism_factor, use_BRAMs):

	kernal_ROM_depth = num_kernals * 3 * 3 * data_depth
	threshold_ROM_depth = num_kernals * data_cols * data_rows
	gamma_ROM_depth = num_kernals * data_cols * data_rows
	ROM_depth = kernal_ROM_depth + threshold_ROM_depth + gamma_ROM_depth + parallelism_factor

	# 2 ** ceil(log( , 2) is the BAM roll over relates on the addr space being a power of 2
	# 3 for 3 rows
	# (2 + data_cols) for padded rows
	# data_depth for data depth
	RAM_depth = 2 ** math.ceil(math.log((3 * (2 + data_cols) * data_depth), 2))

	popcount_width = compute_popcount(data_cols, data_rows, data_depth)

	parameters = {
		"signal_padding" : "unsigned",
		"external_stall" : False,
		"report_stall" : False,

		"SIMD": {
			"lanes": 1
		},
		"address_sources": {
			# act_write BAM
			"BAM_0": {
				"addr_max": RAM_depth - 1,
				"offset_max": RAM_depth - 1,
				"step_max": parallelism_factor
			},
			# act_row_0 BAM
			"BAM_1": {
				"addr_max": RAM_depth - 1,
				"offset_max": RAM_depth - 1,
				"step_max": 3 * data_depth * (data_cols + 2)
			},
			# act_row_1 BAM
			"BAM_2": {
				"addr_max": RAM_depth - 1,
				"offset_max": RAM_depth - 1,
				"step_max": 3 * data_depth * (data_cols + 2)
			},
			# act_row_2 BAM
			"BAM_3": {
				"addr_max": RAM_depth - 1,
				"offset_max": RAM_depth - 1,
				"step_max": 3 * data_depth * (data_cols + 2)
			},
			# kernels BAM
			"BAM_4": {
				"addr_max": kernal_ROM_depth - 1,
				"offset_max": kernal_ROM_depth - 1,
				"step_max": parallelism_factor
			},
			# thresholds and gammas BAM
			"BAM_5": {
				"addr_max": ROM_depth - 1,
				"offset_max": threshold_ROM_depth + gamma_ROM_depth - 1,
				"step_max": 1
			}
		},
		"data_memories": {
			"GET": {
				"FIFOs": 1,
				"FIFO_handshakes": False,
				"data_width": 1
			},
			"PUT": {
				"FIFOs": 1,
				"FIFO_handshakes": False,
				"data_width": 1
			},
			"RAM": {
				"data_width": 1,
				"depth": RAM_depth,
				"type" : "DIST"
			},
			"REG": {
				"data_width": popcount_width,
				"depth": 5*parallelism_factor + 1
			},
			"ROM_A": {
				"data_width": popcount_width,
				"depth": ROM_depth,
				"type" : "DIST"
			}
		},
		"execute_units": {
			"ALU": {
				"data_width": popcount_width + 1,
			}
		},
		"program_flow": {
            "hidden_ZOLs": {
                "tracker_type"  : "ripple",
                "pune_single_iteration" : False,
            },
        }
	}

	with open(path + "\\" + layer_name + "_parameters.json", "w") as f:
		f.write(json.dumps(parameters, sort_keys=True, indent=2))

	generics = {
		"BAM_0_base": 0,
		"BAM_0_internal_step_value": parallelism_factor,
		"BAM_1_base": 0*(data_cols + 2)*data_depth,
		"BAM_1_internal_step_value": parallelism_factor,
		"BAM_2_base": 1*(data_cols + 2)*data_depth,
		"BAM_2_internal_step_value": parallelism_factor,
		"BAM_3_base": 2*(data_cols + 2)*data_depth,
		"BAM_3_internal_step_value": parallelism_factor,
		"BAM_4_base": 0,
		"BAM_4_internal_step_value": parallelism_factor,
		"BAM_5_base": kernal_ROM_depth,
		"BAM_5_internal_step_value": 1,
		"RAM_init_mif": "..\\%s_RAM.mem"%(layer_name, ),
	}

	for subblock in range(parallelism_factor):
		generics["ROM_A_subblock_%i_init_mif"%(subblock, )] = "..\\%s_ROM_A_subblock_%i.mem"%(layer_name, subblock, )

	with open(path + "\\" + layer_name + "_generics.json", "w") as f:
		f.write(json.dumps(generics, sort_keys=True, indent=2))

	return parameters, generics


def generate_blank_mem(path, name, width, depth):
	with open(path + "\\" + name, "w") as f:
		data = math.floor( ((2**width) - 1)/3)
		step = 1
		for line in range(depth):
			if data < 0:
				data = 0
				step = 1
			elif data > (2**width) - 1:
				data = (2**width) - 1
				step = -1

			f.write(tc_utils.unsigned.encode(data, width))
			data += step
			f.write("\n")
