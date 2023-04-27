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

def compute_kickoff_data(input_rows, input_cols, data_depth):
    return 2 * input_cols * data_depth

def compute_kickoff_space(input_rows, input_cols, data_depth):
     return int(input_cols * data_depth / 2)

def generate_layer(path, layer_name, input_rows, input_cols, data_depth, use_BRAMs=False, pregened_memfiles=None):

    # Generate toolchain input files
    generate_layer_fpea(path,layer_name, input_rows, input_cols, data_depth)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, input_rows, input_cols, data_depth, use_BRAMs)

    # Generate mem files
    assert pregened_memfiles == None or type(pregened_memfiles) == list, "invalid ROMs parameter"
    for mem in ["RAM", ]:
        if pregened_memfiles == None or mem not in pregened_memfiles:
            generate_blank_mem(
                path,
                "%s_%s.mem"%(layer_name, mem, ),
                parameters["data_memories"][mem]["data_width"],
                parameters["data_memories"][mem]["depth"]
            )


def generate_layer_fpea(path, layer_name, input_rows, input_cols, data_depth):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "DEF input_rows %i ;\n"%(input_rows, )
    fpea += "DEF input_cols %i ;\n"%(input_cols, )
    fpea += "DEF data_depth %i ;\n"%(data_depth, )
    fpea += "\n"

    fpea += "DEF curr_row   0 ;\n"
    fpea += "DEF row_upper 0 ;\n"
    fpea += "DEF row_lower 1 ;\n"
    fpea += "\n"

    fpea += "DEF mid_row   1 ;\n"
    fpea += "\n"

    fpea += "DEF first_element  0 ;\n"
    fpea += "DEF second_element 1 ;\n"
    fpea += "\n"

    fpea += "// determine if at the start of a row\n"
    fpea += "UCMP (REG[mid_row], 1);\n"
    fpea += "NOP ;\n"
    fpea += "JEQ (ROW_SWITCH) ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"


    fpea += "// Start of row bookkeeping :\n"
    fpea += "RESET BAM[first_element];\n"
    fpea += "RESET BAM[second_element];\n"
    fpea += "MOV (1, REG[mid_row]);  // Mark row as started for furcture kickoffs\n"


    fpea += "// determine which row is being processed\n"
    fpea += "ROW_SWITCH :\n"
    fpea += "UCMP (REG[curr_row], row_lower);\n"
    fpea += "NOP;\n"
    fpea += "JEQ (LOWER_PAIR);\n"
    fpea += "JNE (UPPER_PAIR);\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "\n"


    fpea += "// Handle upper row of pairs\n"
    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "UPPER_PAIR :\n"
    fpea += "// Store upper first elements\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "MOV (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// OR upper second elements and store\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Jump to the end of the program to await next kickout\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (0, REG[mid_row]); // Mark row as fiunished \n"
    fpea += "MOV (row_lower, REG[curr_row]); // Move program to lower pairs for furture kickoffs \n"
    fpea += "NOP;\n"
    fpea += "\n"


    fpea += "// Handle lower row of pairs\n"

    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "LOWER_PAIR :\n"

    fpea += "// OR lower first elements and store\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "OR (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// OR lower second elements and output\n"
    fpea += "ZOL (data_depth)\n"
    fpea += "{\>\n"
    fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], PUT[0]);\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "MOV (0, REG[mid_row]); // Mark row as finished \n"
    fpea += "MOV (row_upper, REG[curr_row]); // Move program to upper pairs for furture kickoffs \n"


    fpea += "END :\n"
    fpea += "NOP;\n"

    fpea += "\<}\n"
    fpea += "\n"


    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, input_rows, input_cols, data_depth, use_BRAMs):
    RAM_depth = int(input_cols/2 * data_depth)
    parameters = {
        "signal_padding" : "unsigned",

        "external_stall" : False,
	  	"report_stall" : False,

        "SIMD": {
            "lanes": 1
        },
        "address_sources": {
            "BAM_0": {
                "addr_max": RAM_depth - 1,
                "offset_max": RAM_depth - 1,
                "step_max": 1,
            },
            "BAM_1": {
                "addr_max": RAM_depth - 1,
                "offset_max": RAM_depth - 1,
                "step_max": 1,
            }
        },
        "data_memories": {
            "GET": {
                "FIFOs": 1,
                "FIFO_handshakes": False,
                "data_width": 1,
            },
            "PUT": {
                "FIFOs": 1,
                "FIFO_handshakes": False,
                "data_width": 1,
            },
            "RAM": {
                "data_width": 1,
                "depth": RAM_depth,
                "type" : "DIST",
            },
            "REG": {
                "data_width": 1,
                "depth": 2,
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
      "BAM_0_base": 0,
      "BAM_0_increment": 1,
      "BAM_1_base": 0,
      "BAM_1_increment": 1,
      "RAM_mem_file":"..\\%s_RAM.mem"%(layer_name, ),
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
