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

def compute_kickoff_data(input_rows, input_cols, data_depth, batch_size):
    return batch_size

def compute_kickoff_space(input_rows, input_cols, data_depth, batch_size):
    return 1

def generate_layer(path, layer_name, input_rows, input_cols, data_depth, batch_size, use_BRAMs=False, pregened_memfiles=None):

    assert type(batch_size) == int and 0 < batch_size and batch_size <= data_depth and data_depth % batch_size == 0, "batch_size must be a postive int that is a factor of data_depth"

    # Generate toolchain input files
    generate_layer_fpea(path,layer_name, input_rows, input_cols, data_depth, batch_size)
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


def generate_layer_fpea(path, layer_name, input_rows, input_cols, data_depth, batch_size):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "DEF input_rows %i ;\n"%(input_rows, )
    fpea += "DEF input_cols %i ;\n"%(input_cols, )
    fpea += "DEF data_depth %i ;\n"%(data_depth, )
    if batch_size != 1 and batch_size != data_depth:
        fpea += "DEF batch_size %i ;\n"%(batch_size, )
    fpea += "\n"

    fpea += "DEF curr_row  0 ;\n"
    fpea += "DEF row_upper 0 ;\n"
    fpea += "DEF row_lower 1 ;\n"
    fpea += "\n"

    fpea += "DEF curr_col   1 ;\n"
    fpea += "DEF col_first  0 ;\n"
    fpea += "DEF col_second 1 ;\n"
    fpea += "\n"

    fpea += "DEF mid_row   2 ;\n"
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
    fpea += "JEQ (LOWER_COL_SWITCH);\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "\n"


    fpea += "// determine which col is being processed\n"
    fpea += "UPPER_COL_SWITCH :\n"
    fpea += "UCMP (REG[curr_col], col_second);\n"
    fpea += "NOP;\n"
    fpea += "JEQ (UPPER_SECOND_READ);\n"
    fpea += "JNE (UPPER_FIRST_READ);\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "\n"

    fpea += "// Handle upper row\n"
    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (col_first, REG[curr_col]); // Move program to first col for furture kickoffs \n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    if batch_size == 1:
        fpea += "// Store upper first elements\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "UPPER_FIRST_READ :\n"
        fpea += "MOV (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    elif batch_size == data_depth:
        fpea += "UPPER_FIRST_READ :\n"
        fpea += "// Store upper first elements\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    else:
        fpea += "// Store upper first elements\n"
        fpea += "ZOL (data_depth/batch_size)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "UPPER_FIRST_READ :\n"
        fpea += "ZOL (batch_size)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"

        fpea += "NOP;\n"
        fpea += "\<}\n"
        fpea += "\n"

    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (col_second, REG[curr_col]); // Move program to second col for furture kickoffs \n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    if batch_size == 1:
        fpea += "// OR upper second elements and store\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "UPPER_SECOND_READ :\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    elif batch_size == data_depth:
        fpea += "UPPER_SECOND_READ :\n"
        fpea += "// OR upper second elements and store\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    else:
        fpea += "// OR upper second elements and store\n"
        fpea += "ZOL (data_depth/batch_size)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "UPPER_SECOND_READ :\n"
        fpea += "ZOL (batch_size)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"

        fpea += "NOP;\n"
        fpea += "\<}\n"
        fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Jump to the end of the program to await next kickout\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (0, REG[mid_row]); // Mark row as fiunished \n"
    fpea += "MOV (row_lower, REG[curr_row]); // Move program to lower row for furture kickoffs \n"
    fpea += "MOV (col_first, REG[curr_col]); // Move program to first col for furture kickoffs \n"
    fpea += "\n"


    fpea += "// determine which col is being processed\n"
    fpea += "LOWER_COL_SWITCH :\n"
    fpea += "UCMP (REG[curr_col], col_second);\n"
    fpea += "NOP;\n"
    fpea += "JEQ (LOWER_SECOND_READ);\n"
    fpea += "JNE (LOWER_FIRST_READ);\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "NOP ;\n"
    fpea += "\n"

    fpea += "// Handle lower row\n"
    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (col_first, REG[curr_col]); // Move program to first col for furture kickoffs \n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    if batch_size == 1:
        fpea += "// OR lower first elements and store\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "LOWER_FIRST_READ :\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    elif batch_size == data_depth:
        fpea += "LOWER_FIRST_READ :\n"
        fpea += "// OR lower first elements and store\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    else:
        fpea += "// OR lower first elements and store\n"
        fpea += "ZOL (data_depth/batch_size)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "LOWER_FIRST_READ :\n"
        fpea += "ZOL (batch_size)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "\n"

        fpea += "NOP;\n"
        fpea += "\<}\n"
        fpea += "\n"


    fpea += "// Jump to the end of the program to await next kickoff\n"
    fpea += "JMP (END);\n"
    fpea += "MOV (col_second, REG[curr_col]); // Move program to second col for furture kickoffs \n"
    fpea += "NOP;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    if batch_size == 1:
        fpea += "JMP (END);\n"
        fpea += "// OR lower second elements and output\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "LOWER_SECOND_READ :\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], PUT[0]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    elif batch_size == data_depth:

        fpea += "LOWER_SECOND_READ :\n"
        fpea += "// OR lower second elements and output\n"
        fpea += "ZOL (data_depth)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], PUT[0]);\n"
        fpea += "\<}\n"
        fpea += "\n"
    else:
        fpea += "// OR lower second elements and output\n"
        fpea += "ZOL (data_depth/batch_size)\n"
        fpea += "{\>\n"

        fpea += "JMP (END);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "\n"

        fpea += "LOWER_SECOND_READ :\n"
        fpea += "ZOL (batch_size)\n"
        fpea += "{\>\n"
        fpea += "OR (GET[0]<ADV>, RAM[BAM[second_element]<FORWARD>], PUT[0]);\n"
        fpea += "\<}\n"
        fpea += "\n"

        fpea += "NOP;\n"
        fpea += "\<}\n"
        fpea += "\n"

    fpea += "NOP;\n"
    fpea += "\<}\n"
    fpea += "\n"

    fpea += "MOV (0, REG[mid_row]); // Mark row as finished \n"
    fpea += "MOV (row_upper, REG[curr_row]); // Move program to upper row for furture kickoffs \n"
    fpea += "MOV (col_first, REG[curr_col]); // Move program to first col for furture kickoffs \n"


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
                "depth": 3,
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
