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

def generate_layer(path, layer_name, data_cols, data_rows, data_depth, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, use_BRAMs)


def generate_layer_fpea(path, layer_name, data_cols, data_rows, data_depth):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF data_rows   %i ;\n"%(data_rows, )
    fpea += "DEF data_cols   %i ;\n"%(data_cols, )
    fpea += "DEF data_depth  %i ;\n"%(data_depth, )
    fpea += "\n"

    fpea += "// Define meaningfully names for reg addresses\n"
    fpea += "DEF packing  0 ;\n"
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
    fpea += "NOT(ACC, PUT[0] ) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(ACC, ACC) ;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Handle middle rows,\n"
    fpea += "ZOL (data_rows)\n"
    fpea += "{\>\n"

    fpea += "// Pad first col\n"
    fpea += "MOV(REG[packing], PUT[0]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, PUT[0] ) ;\n"
    fpea += "\<}\n"
    fpea += "MOV(ACC, REG[packing]) ;\n"

    fpea += "// read of middle cols\n"
    assert data_cols % 2 == 0, "Program expects an even number of data cols"
    fpea += "ZOL (data_depth * data_cols)\n"
    fpea += "{\>\n"
    fpea += "MOV( GET[0]<ADV>, PUT[0] ) ;\n"
    fpea += "\<}\n"

    fpea += "// pad last col\n"
    fpea += "MOV(REG[packing], PUT[0]) ;\n"
    fpea += "ZOL (data_depth - 1)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, PUT[0] ) ;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"
    fpea += "\n"


    assert data_rows % 2 == 0, "Program expects an even number of data rows"
    fpea += "// Pad last row,\n"
    fpea += "MOV(1, ACC) ;\n"
    fpea += "ZOL (data_cols + 2)\n"
    fpea += "{\>\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "NOT(ACC, PUT[0] ) ;\n"
    fpea += "\<}\n"
    fpea += "NOT(ACC, ACC) ;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"

    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, data_cols, data_rows, data_depth, use_BRAMs):
    parameters = {
        "signal_padding" : "unsigned",
        "external_stall" : False,
	  	"report_stall" : False,

    	"SIMD": {
    		"lanes": 1
    	},
    	"address_sources": {
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
    		"REG": {
    			"data_width": 1,
    			"depth": 1
    		}
    	},
    	"execute_units": {
    		"ALU": {
    			"data_width": 1,
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
