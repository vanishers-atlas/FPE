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
import random

def generate_layer(path, layer_name, data_cols, data_rows, data_depth, num_kernals, num_lanes, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, num_lanes, use_BRAMs, pregened_memfiles)


def generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF data_rows   %i ;\n"%(data_rows, )
    fpea += "DEF data_cols   %i ;\n"%(data_cols, )
    fpea += "DEF data_depth  %i ;\n"%(data_depth, )
    fpea += "DEF num_kernals %i ;\n"%(num_kernals, )
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
    fpea += "DEF packing  0 ;\n"
    fpea += "DEF popcount  1 ;\n"
    fpea += "\n"


    fpea += "// Reset BAMs\n"
    fpea += "RESET BAM[act_write];\n"
    fpea += "RESET BAM[act_row_0];\n"
    fpea += "RESET BAM[act_row_1];\n"
    fpea += "RESET BAM[act_row_2];\n"
    fpea += "RESET BAM[thresholds];\n"
    #fpea += "RESET BAM[gammas];\n"
    fpea += "\n"


    fpea += "// Set Regfile,\n"
    fpea += "MOV(0, REG[packing]) ;\n"
    fpea += "\n"


    fpea += "// Pad first row,\n"
    fpea += "MOV(0, ACC) ;\n"
    fpea += "ZOL (data_cols + 2)\n"
    fpea += "{\>\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(ACC, ACC) ;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Handle second row,\n"

    fpea += "// pad first col\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "MOV(ACC, REG[packing]) ;\n"

    fpea += "// read of middle cols\n"
    fpea += "ZOL (data_depth * data_cols)\n"
    fpea += "{\>\n"
    fpea += "MOV( GET[0]<ADV>, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"

    fpea += "// pad last col\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "\n"


    fpea += "// Process all but last row\n"
    fpea += "ZOL (data_rows - 1)\n"
    fpea += "{\>\n"

    fpea += "// Read in next row,\n"

    fpea += "// pad first col\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "MOV(ACC, REG[packing]) ;\n"

    fpea += "// read of middle cols\n"
    fpea += "ZOL (data_depth * data_cols)\n"
    fpea += "{\>\n"
    fpea += "MOV( GET[0]<ADV>, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"

    fpea += "// pad last col\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
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
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    fpea += "// * 3 for each col of the kernel\n"
    fpea += "ZOL (3 * data_depth )\n"
    fpea += "{\>\n"
    fpea += "XNOR ( RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "XNOR ( RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "XNOR ( RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
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

    fpea += "// Pad first row,\n"
    fpea += "MOV(1, ACC) ;\n"
    fpea += "ZOL (data_cols + 2)\n"
    fpea += "{\>\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(ACC, ACC) ;\n"
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
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    fpea += "// * 3 for each col of the kernel\n"
    fpea += "ZOL (3 * data_depth )\n"
    fpea += "{\>\n"
    fpea += "XNOR ( RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "XNOR ( RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "XNOR ( RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
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


def generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, num_lanes, use_BRAMs, pregened_memfiles):

    kernal_ROM_depth = num_kernals * 3 * 3 * data_depth
    threshold_ROM_depth = num_kernals * data_cols * data_rows
    gamma_ROM_depth = num_kernals * data_cols * data_rows
    ROM_depth = kernal_ROM_depth + threshold_ROM_depth + gamma_ROM_depth

    # 2 ** ceil(log( , 2) is the BAM roll over relates on the addr space being a power of 2
    # 3 for 3 rows
    # (2 + data_cols) for padded rows
    # data_depth for data depth
    RAM_depth = 2 ** math.ceil(math.log((3 * (2 + data_cols) * data_depth), 2))

    popcount_width = tc_utils.unsigned.width(3 * 3 * data_depth)

    parameters = {
        "signal_padding" : "unsigned",
        "external_stall" : False,
	  	"report_stall" : False,

    	"SIMD": {
    		"lanes": num_lanes
    	},
    	"address_sources": {
            # act_write BAM
    		"BAM_0": {
    			"addr_max": RAM_depth - 1,
    			"offset_max": RAM_depth - 1,
    			"step_max": 1
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
    			"step_max": 1
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
    			"depth": 2
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

    # Generate mem files
    required_mems = []
    for lane in range(num_lanes):
        required_mems.append("LANE_%i_ROM_A"%(lane, ))
        required_mems.append("LANE_%i_RAM"%(lane, ))

    assert pregened_memfiles == None or type(pregened_memfiles) == dict, "invalid ROMs parameter"
    mifs = {}
    for mem in required_mems:
        if pregened_memfiles != None and mem in pregened_memfiles.keys():
            mifs[mem] = pregened_memfiles[mem]
        else:
            if mem.startswith("LANE_"):
                para_name = "_".join(mem.split("_")[2:])
            else:
                para_name = mem

            rand_mem = "%s_%s.mem"%(layer_name, mem, )
            generate_rand_mem(
                path,
                rand_mem,
                parameters["data_memories"][para_name]["data_width"],
                parameters["data_memories"][para_name]["depth"]
            )
            mifs[mem] = rand_mem

    generics = {
    	"BAM_0_base": 0,
    	"BAM_0_internal_step_value": 1,
    	"BAM_1_base": 0*(data_cols + 2)*data_depth,
    	"BAM_1_internal_step_value": 1,
        "BAM_2_base": 1*(data_cols + 2)*data_depth,
    	"BAM_2_internal_step_value": 1,
        "BAM_3_base": 2*(data_cols + 2)*data_depth,
    	"BAM_3_internal_step_value": 1,
    	"BAM_4_base": 0,
    	"BAM_4_internal_step_value": 1,
    	"BAM_5_base": kernal_ROM_depth,
    	"BAM_5_internal_step_value": 1,
    }
    for k, v in mifs.items():
        generics[k + "_init_mif"] = "..\\%s"%(v, )

    with open(path + "\\" + layer_name + "_generics.json", "w") as f:
        f.write(json.dumps(generics, sort_keys=True, indent=2))

    return parameters, generics


def generate_rand_mem(path, name, width, depth):
    with open(path + "\\" + name, "w") as f:
        max_value = 2**width
        for line in range(depth):
            f.write(tc_utils.unsigned.encode(random.randrange(max_value), width))
            f.write("\n")
