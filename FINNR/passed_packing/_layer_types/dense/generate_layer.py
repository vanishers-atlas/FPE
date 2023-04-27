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

def compute_max_packing(data_depth):
    if data_depth > 32:
        return 32
    else:
        return data_depth

def generate_layer(path, layer_name, input_neurons, output_neurons, input_packing, output_packing, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, input_neurons, output_neurons, input_packing, output_packing)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, input_packing, output_packing, use_BRAMs)

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


def generate_layer_fpea(path, layer_name, input_neurons, output_neurons, input_packing, output_packing):
    popcount_width = tc_utils.unsigned.width(input_neurons)

    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF input_neurons  %i ;\n"%(input_neurons, )
    fpea += "DEF output_neurons %i ;\n"%(output_neurons, )
    fpea += "DEF input_packing  %i ;\n"%(input_packing, )
    fpea += "DEF output_packing %i ;\n"%(output_packing, )
    fpea += "\n"

    fpea += "// Define meaningfully names for Block access managers\n"
    fpea += "DEF weights    0 ;\n"
    fpea += "DEF thresholds 0 ;\n"
    fpea += "DEF gammas     0 ;\n"
    if input_packing != input_neurons:
        fpea += "DEF acts       1 ;\n"
    fpea += "\n"


    fpea += "// Define meaningfully names for reg addresses\n"
    fpea += "DEF popcount 0 ;\n"
    fpea += "DEF pop_temp 1 ;\n"
    fpea += "DEF outpad   2 ;\n"
    fpea += "\n"

    if input_packing != input_neurons:
        fpea += "RESET BAM[acts] ;\n"
        fpea += "NOP ;\n"
    fpea += "RESET BAM[weights] ;\n"
    #fpea += "RESET BAM[thresholds] ;\n"
    #fpea += "RESET BAM[gammas] ;\n"

    fpea += "\n"

    fpea += "// Read input data to RAM\n"
    assert input_neurons % input_packing == 0
    fpea += "ZOL (input_neurons / input_packing)\n"
    fpea += "{\>\n"
    if input_packing == input_neurons:
        fpea += "MOV (GET[0]<ADV>, RAM[0]);\n"
    else:
        fpea += "MOV (GET[0]<ADV>, RAM[BAM[acts]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "\n"

    if input_packing == input_neurons:
        fpea += "NOP ;\n"
        fpea += "NOP ;\n"
        fpea += "\n"

    fpea += "// Process each output neuron in turn\n"
    assert output_neurons % output_packing == 0
    fpea += "ZOL (output_neurons/output_packing)\n"
    fpea += "{\>\n"

    fpea += "// Clear output padding acc\n"
    fpea += "MOV (0, ACC);\n"

    fpea += "ZOL (output_packing)\n"
    fpea += "{\>\n"

    fpea += "// assuming input_neurons in a power of 2\n"
    fpea += "// BAM[acts] will have wrapped around to 0 at this point\n"
    fpea += "// therefore no need to reset\n"
    fpea += "\n"

    fpea += "// Ready output pad for next iteration\n"
    fpea += "LSH (ACC, 1, REG[outpad]);\n"

    fpea += "// Clear popcount\n"
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    assert input_neurons % input_packing == 0
    fpea += "ZOL (input_neurons / input_packing)\n"
    fpea += "{\>\n"
    if input_packing == input_neurons:
        fpea += "XNOR ( RAM[0], ROMA[BAM[weights]<FORWARD>], REG[pop_temp] ) ;\n"
    else:
        fpea += "XNOR ( RAM[BAM[acts]<FORWARD>], ROMA[BAM[weights]<FORWARD>], REG[pop_temp] ) ;\n"
    for e in range(math.ceil(math.log(input_packing,2))):
        word_len = 2 ** e
        mask = ("1"*word_len + "0"*word_len)*int(input_packing/(2*word_len))
        fpea += "AND ( ACC, 0b%s, ACC ) ;\n"%(mask, )
        fpea += "RSH(ACC, %i, REG[pop_temp]);\n"%(word_len, )
        fpea += "NOT(0b%s, ACC);\n"%(mask, )
        fpea += "AND (REG[pop_temp], ACC, ACC ) ;\n"
        fpea += "ADD (REG[pop_temp], ACC, REG[pop_temp]) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\<}\n"

    fpea += "// Perform thresholding\n"
    fpea += "SUB(ROMA[BAM[thresholds]<FORWARD>], ACC, ACC);\n"
    fpea += "// Move difference sign to bit 0, not masking require as the store to put will remove all but bit 0\n"
    fpea += "RSH(ACC, %i, ACC);\n"%(popcount_width - 1, )
    fpea += "// Difference and gammas use 2 comp. signing, but XNOR converts that tos mathmatic sign function\n"
    fpea += "XNOR ( ACC, ROMA[BAM[gammas]<FORWARD>], ACC ) ;\n"
    fpea += "AND  ( ACC, 0b1, ACC ) ;\n"
    fpea += "ADD  ( REG[outpad], ACC, ACC ) ;\n"

    fpea += "\<}\n"
    fpea += "MOV  ( ACC, PUT[0] ) ;\n"

    fpea += "\<}\n"
    fpea += "NOP ;\n"

    fpea += "\<}\n"

    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, input_packing, output_packing, use_BRAMs):
    assert input_neurons % input_packing == 0
    packed_weights = int(input_neurons/input_packing)

    ROM_depth = output_neurons * (packed_weights + 2)

    RAM_depth = packed_weights

    popcount_width = tc_utils.unsigned.width(input_neurons)

    parameters = {
        "signal_padding" : "unsigned",

        "external_stall" : False,
	  	"report_stall" : False,

        "SIMD": {
            "lanes": 1
        },
        "address_sources": {
            "BAM_0": {
                "addr_max": ROM_depth - 1 ,
                "offset_max": ROM_depth - 1,
                "step_max": 1
            },
            "BAM_1": {
                "addr_max": RAM_depth - 1,
                "offset_max": RAM_depth - 1,
                "step_max": 1
            },
        },
        "data_memories": {
            "GET": {
                "FIFOs": 1,
                "FIFO_handshakes": False,
                "data_width": input_packing,
            },
            "PUT": {
                "FIFOs": 1,
                "FIFO_handshakes": False,
                "data_width": output_packing,
            },
            "RAM": {
                "data_width": input_packing,
                "depth": RAM_depth,
                "type" : "DIST"
            },
            "REG": {
                "data_width": max([input_packing, output_packing, popcount_width]),
                "depth": 3
            },
            "ROM_A": {
                "data_width": max([input_packing, popcount_width]),
                "depth": ROM_depth,
                "type" : "DIST" if use_BRAMs else "DIST"
            }
        },
        "execute_units": {
            "ALU": {
                "data_width": max([input_packing, output_packing, popcount_width]),
            }
        },
        "program_flow": {
            "bound_ZOL_tracker_type"  : "ripple",
            "pune_single_iteration_bound_ZOLs" : "false",
        }
    }


    with open(path + "\\" + layer_name + "_parameters.json", "w") as f:
        f.write(json.dumps(parameters, sort_keys=True, indent=2))

    generics = {
        "BAM_0_base": 0,
        "BAM_0_increment": 1,
        "BAM_1_base": 0,
        "BAM_1_increment": 1,
        "RAM_init_mif": "..\\%s_RAM_A.mem"%(layer_name, ),
    	"ROM_A_init_mif": "..\\%s_ROM_A.mem"%(layer_name, )
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
