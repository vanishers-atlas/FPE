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

def generate_layer(path, layer_name, input_neurons, output_neurons, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, input_neurons, output_neurons)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, use_BRAMs)

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


def generate_layer_fpea(path, layer_name, input_neurons, output_neurons):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF input_neurons  %i ;\n"%(input_neurons, )
    fpea += "DEF output_neurons %i ;\n"%(output_neurons, )
    fpea += "\n"

    fpea += "// Define meaningfully names for Block access managers\n"
    fpea += "DEF acts       0 ;\n"
    fpea += "DEF weights    1 ;\n"
    fpea += "\n"

    fpea += "// Define meaningfully names for reg addresses\n"
    fpea += "DEF popcount 0 ;\n"
    fpea += "\n"

    fpea += "RESET BAM[acts] ;\n"
    fpea += "RESET BAM[weights] ;\n"
    fpea += "NOP ;\n"
    fpea += "\n"

    fpea += "// Read input data to RAM\n"
    fpea += "REP (input_neurons)\n"
    fpea += "{\>\n"
    fpea += "MOV( GET[0]<ADV>, RAM[BAM[acts]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Process each output neuron in turn\n"
    fpea += "REP (output_neurons)\n"
    fpea += "{\>\n"
    fpea += "// assuming input_neurons in a power of 2\n"
    fpea += "// BAM[acts] will have wrapped around to 0 at this point\n"
    fpea += "// therefore no need to reset\n"
    fpea += "\n"

    fpea += "// Clear popcount\n"
    fpea += "MOV (0, REG[popcount]);\n"

    fpea += "// Compute popcount\n"
    fpea += "REP (input_neurons )\n"
    fpea += "{\>\n"
    fpea += "XNOR ( RAM[BAM[acts]<FORWARD>], ROMA[BAM[weights]<FORWARD>], ACC ) ;\n"
    fpea += "AND ( ACC, 1, ACC ) ;\n"
    fpea += "ADD ( REG[popcount], ACC, REG[popcount]) ;\n"
    fpea += "\<}\n"

    fpea += "MOV ( ACC, PUT[0] ) ;\n"

    fpea += "\<}\n"
    fpea += "NOP ;\n"

    fpea += "\<}\n"

    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, use_BRAMs):

    ROM_depth = output_neurons * input_neurons

    RAM_depth = input_neurons

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
                "addr_max": input_neurons - 1,
                "offset_max": input_neurons - 1,
                "step_max": 1
            },
            "BAM_1": {
                "addr_max": ROM_depth - 1 ,
                "offset_max": ROM_depth - 1,
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
                "data_width": popcount_width
            },
            "RAM": {
                "data_width": 1,
                "depth": RAM_depth,
                "type" : "DIST"
            },
            "REG": {
                "data_width": popcount_width,
                "depth": 1
            },
            "ROM_A": {
                "data_width": 1,
                "depth": ROM_depth,
                "type" : "DIST" if use_BRAMs else "DIST"
            }
        },
        "execute_units": {
            "ALU": {
                "data_width": popcount_width
            }
        },
        "program_flow": {
            "rep_bank": {
                "stall_on_id_change": "ALWAYS",
                "subtype": "preloaded"
            }
        },
    }


    with open(path + "\\" + layer_name + "_parameters.json", "w") as f:
        f.write(json.dumps(parameters, sort_keys=True, indent=2))

    generics = {
        "BAM_0_base": 0,
        "BAM_0_internal_step_value": 1,
        "BAM_1_base": 0,
        "BAM_1_internal_step_value": 1,
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
