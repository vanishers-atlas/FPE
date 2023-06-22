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


def compute_max_packing(layer_depth):
    if layer_depth > 48 :
        if layer_depth % 48 == 0:
            return 48
        else:
            assert layer_depth % 32 == 0
            return 32
    else:
        return layer_depth


def generate_layer(path, layer_name, data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing, use_BRAMs)

    # Generate mem files
    assert pregened_memfiles == None or type(pregened_memfiles) == list, "invalid ROMs parameter"
    for mem in ["ROM_A", "RAM"]:
        if pregened_memfiles == None or mem not in pregened_memfiles:
            generate_blank_mem(
                path,
                "%s_%s.mem"%(layer_name, mem, ),
                parameters["data_memories"][mem]["data_width"],
                parameters["data_memories"][mem]["depth"]
            )


def generate_widths(data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing):
    popcount_width = tc_utils.unsigned.width(3 * 3 * data_depth)

    return {
        "popcount" : popcount_width,
        "ALU" : max([popcount_width + 1, input_packing, output_packing]),
        "GET" : input_packing,
        "PUT" : output_packing,
        "REG" : max([popcount_width, input_packing, output_packing]),
        "RAM" : input_packing,
        "ROM" : max([popcount_width, input_packing]),
    }


def generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing):
    widths = generate_widths(data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing)

    fpea = IndentedString()
    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF data_rows   %i ;\n"%(data_rows, )
    fpea += "DEF data_cols   %i ;\n"%(data_cols, )
    fpea += "DEF data_depth  %i ;\n"%(data_depth, )
    fpea += "DEF num_kernals %i ;\n"%(num_kernals, )
    fpea += "DEF input_packing  %i ;\n"%(input_packing, )
    fpea += "DEF output_packing %i ;\n"%(output_packing, )
    assert data_depth % input_packing == 0
    fpea += "DEF packed_words data_depth/input_packing ;\n"
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
    fpea += "DEF popcount 1 ;\n"
    fpea += "DEF pop_temp 2 ;\n"
    fpea += "DEF outpad   3 ;\n"
    fpea += "\n"


    fpea += "// Reset BAMs\n"
    fpea += "RESET BAM[act_write];\n"
    fpea += "RESET BAM[act_row_0];\n"
    fpea += "RESET BAM[act_row_1];\n"
    fpea += "RESET BAM[act_row_2];\n"
    fpea += "RESET BAM[thresholds];\n"
    #fpea += "RESET BAM[gammas];\n"
    fpea += "\n"


    fpea += "// Set packing,\n"
    assert input_packing % 2 == 0
    fpea += "MOV(0b10, ACC);\n"
    fpea += "ZOL (input_packing/2)\n"
    fpea += "{\>\n"
    fpea += "LSH(ACC, 2, ACC);\n"
    fpea += "ADD(ACC, 0b10, ACC);\n"
    fpea += "\<}\n"
    fpea += "MOV(ACC, REG[packing]) ;\n"
    fpea += "\n"


    fpea += "// Pad first row,\n"
    fpea += "ZOL (data_cols + 2)\n"
    fpea += "{\>\n"
    fpea += "ZOL (packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(ACC, ACC) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(REG[packing], REG[packing]) ;\n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"


    fpea += "// Handle second row,\n"

    fpea += "// pad first col\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(REG[packing], REG[packing] ) ;\n"

    fpea += "// read of middle cols\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (data_cols * packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV (GET[0]<ADV>, RAM[BAM[act_write]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "NOP;\n"

    fpea += "// pad last col\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL ( packed_words )\n"
    fpea += "{\>\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "\<}\n"
    fpea += "NOP;\n"
    fpea += "\n"


    fpea += "// Process all but last row\n"
    fpea += "ZOL (data_rows - 1)\n"
    fpea += "{\>\n"

    fpea += "// Read in next row,\n"

    fpea += "// pad first col\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(REG[packing], REG[packing] ) ;\n"

    fpea += "// read of middle cols\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (data_cols * packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV (GET[0]<ADV>, RAM[BAM[act_write]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "NOP;\n"


    fpea += "// pad last col\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV(REG[packing], RAM[BAM[act_write]<FORWARD>]) ;\n"
    fpea += "\<}\n"
    fpea += "NOP;\n"
    fpea += "\n"


    fpea += "// Slide window across rows\n"
    fpea += "ZOL (data_cols)\n"
    fpea += "{\>\n"

    fpea += "// Reset kenral BAM to start at first kernel\n"
    fpea += "RESET BAM[kernels];\n"
    fpea += "\n"

    fpea += "// Process each kernel\n"
    assert  num_kernals %     output_packing == 0
    fpea += "ZOL (num_kernals / output_packing)\n"
    fpea += "{\>\n"

    fpea += "// Clear output padding acculator\n"
    fpea += "MOV (0, ACC);\n"

    fpea += "ZOL (output_packing)\n"
    fpea += "{\>\n"

    fpea += "// Ready output pad for next iteration\n"
    fpea += "LSH (ACC, 1, REG[outpad]);\n"

    fpea += "// Clear popcount\n"
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    fpea += "// * 3 for each col of the kernel\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (3 * packed_words)\n"
    fpea += "{\>\n"

    fpea += "XNOR ( RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "XNOR ( RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "XNOR ( RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Knock acc_row BAMs back for next kernal\n"
    fpea += "SEEK BAM[act_row_0] (3 * packed_words)<BACKWARD>;\n"
    fpea += "SEEK BAM[act_row_1] (3 * packed_words)<BACKWARD>;\n"
    fpea += "SEEK BAM[act_row_2] (3 * packed_words)<BACKWARD>;\n"

    fpea += "// Perform thresholding\n"
    fpea += "SUB(ROMA[BAM[thresholds]<FORWARD>], REG[popcount], ACC);\n"
    fpea += "// Move difference sign to bit 0, not masking require as the store to put will remove all but bit 0\n"
    fpea += "RSH(ACC, %i, ACC);\n"%(widths["popcount"], )
    fpea += "// Difference and gammas use 2 comp. signing, but XNOR converts that tos mathmatic sign function\n"
    fpea += "XNOR ( ACC, ROMA[BAM[gammas]<FORWARD>], ACC ) ;\n"
    fpea += "AND  ( ACC, 0b1, ACC ) ;\n"
    fpea += "ADD  ( REG[outpad], ACC, ACC ) ;\n"

    fpea += "\<}\n"
    fpea += "MOV  ( ACC, PUT[0] ) ;\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Seek acc_row BAMs forward for next col\n"
    fpea += "SEEK BAM[act_row_0] (packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_1] (packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_2] (packed_words)<FORWARD>;\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Seek acc_row BAMs forward for next row\n"
    fpea += "SEEK BAM[act_row_0] (2 * packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_1] (2 * packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_2] (2 * packed_words)<FORWARD>;\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Handle last row,\n"
    fpea += "MOV(REG[packing], ACC ) ;\n"
    fpea += "ZOL (data_cols + 2)\n"
    fpea += "{\>\n"
    fpea += "ZOL (packed_words)\n"
    fpea += "{\>\n"
    fpea += "MOV(ACC, RAM[BAM[act_write]<FORWARD>] ) ;\n"
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
    assert  num_kernals %     output_packing == 0
    fpea += "ZOL (num_kernals / output_packing)\n"
    fpea += "{\>\n"

    fpea += "// Clear output padding acculator\n"
    fpea += "MOV (0, ACC);\n"

    fpea += "ZOL (output_packing)\n"
    fpea += "{\>\n"

    fpea += "// Ready output pad for next iteration\n"
    fpea += "LSH (ACC, 1, REG[outpad]);\n"

    fpea += "// Clear popcount\n"
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    fpea += "// Compute popcount\n"
    fpea += "// * 3 for each col of the kernel\n"
    assert data_depth % input_packing == 0
    fpea += "ZOL (3 * packed_words)\n"
    fpea += "{\>\n"

    fpea += "XNOR ( RAM[BAM[act_row_0]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "XNOR ( RAM[BAM[act_row_1]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "XNOR ( RAM[BAM[act_row_2]<FORWARD>], ROMA[BAM[kernels]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = (("1"*word_len + "0"*word_len)*math.ceil(input_packing/(2*word_len)))[-input_packing:]
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    if widths["ALU"] > widths["popcount"]:
        fpea += "AND ( ACC, 0b%s, ACC) ;\n"%("1"*input_packing, )
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Knock acc_row BAMs back for next kernal\n"
    fpea += "SEEK BAM[act_row_0] (3 * packed_words)<BACKWARD>;\n"
    fpea += "SEEK BAM[act_row_1] (3 * packed_words)<BACKWARD>;\n"
    fpea += "SEEK BAM[act_row_2] (3 * packed_words)<BACKWARD>;\n"

    fpea += "// Perform thresholding\n"
    fpea += "SUB(ROMA[BAM[thresholds]<FORWARD>], REG[popcount], ACC);\n"
    fpea += "// Move difference sign to bit 0, not masking require as the store to put will remove all but bit 0\n"
    fpea += "RSH(ACC, %i, ACC);\n"%(widths["popcount"], )
    fpea += "// Difference and gammas use 2 comp. signing, but XNOR converts that tos mathmatic sign function\n"
    fpea += "XNOR ( ACC, ROMA[BAM[gammas]<FORWARD>], ACC ) ;\n"
    fpea += "AND  ( ACC, 0b1, ACC ) ;\n"
    fpea += "ADD  ( REG[outpad], ACC, ACC ) ;\n"

    fpea += "\<}\n"
    fpea += "MOV  ( ACC, PUT[0] ) ;\n"

    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Seek acc_row BAMs forward for next col\n"
    fpea += "SEEK BAM[act_row_0] (packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_1] (packed_words)<FORWARD>;\n"
    fpea += "SEEK BAM[act_row_2] (packed_words)<FORWARD>;\n"

    fpea += "\<}\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"

    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing, use_BRAMs):
    widths = generate_widths(data_cols, data_rows, data_depth, num_kernals, input_packing, output_packing)

    assert data_depth % input_packing == 0
    packed_words = int(data_depth/input_packing)

    kernal_ROM_depth = num_kernals * 3 * 3 * packed_words
    threshold_ROM_depth = num_kernals * data_cols * data_rows
    gamma_ROM_depth = num_kernals * data_cols * data_rows
    ROM_depth = kernal_ROM_depth + threshold_ROM_depth + gamma_ROM_depth

    # 2 ** ceil(log( , 2) is the BAM roll over relates on the addr space being a power of 2
    # 3 for 3 rows
    # (2 + data_cols) for padded rows
    # data_depth for data depth
    RAM_depth = 2 ** math.ceil(math.log((3 * (2 + data_cols) * packed_words), 2))

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
    			"step_max": 1
    		},
            # act_row_0 BAM
    		"BAM_1": {
    			"addr_max": RAM_depth - 1,
    			"offset_max": RAM_depth - 1,
    			"step_max": 3 * packed_words * (data_cols + 2)
    		},
            # act_row_1 BAM
    		"BAM_2": {
    			"addr_max": RAM_depth - 1,
    			"offset_max": RAM_depth - 1,
    			"step_max": 3 * packed_words * (data_cols + 2)
    		},
            # act_row_2 BAM
    		"BAM_3": {
    			"addr_max": RAM_depth - 1,
    			"offset_max": RAM_depth - 1,
    			"step_max": 3 * packed_words * (data_cols + 2)
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
    			"data_width": widths["GET"],
    		},
    		"PUT": {
    			"FIFOs": 1,
    			"FIFO_handshakes": False,
    			"data_width": widths["PUT"],
    		},
    		"RAM": {
    			"data_width": widths["RAM"],
    			"depth": RAM_depth,
                "type" : "DIST"
    		},
    		"REG": {
    			"data_width":  widths["REG"],
    			"depth": 4
    		},
    		"ROM_A": {
    			"data_width":  widths["ROM"],
    			"depth": ROM_depth,
                "type" : "DIST"
    		}
    	},
    	"execute_units": {
    		"ALU": {
    			"data_width": widths["ALU"],
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
    	"BAM_0_internal_step_value": 1,
    	"BAM_1_base": 0*(data_cols + 2)*packed_words,
    	"BAM_1_internal_step_value": 1,
        "BAM_2_base": 1*(data_cols + 2)*packed_words,
    	"BAM_2_internal_step_value": 1,
        "BAM_3_base": 2*(data_cols + 2)*packed_words,
    	"BAM_3_internal_step_value": 1,
    	"BAM_4_base": 0,
    	"BAM_4_internal_step_value": 1,
    	"BAM_5_base": kernal_ROM_depth,
    	"BAM_5_internal_step_value": 1,
        "RAM_init_mif": "..\\%s_RAM.mem"%(layer_name, ),
    	"ROM_A_init_mif": "..\\%s_ROM_A.mem"%(layer_name, ),
    }

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
