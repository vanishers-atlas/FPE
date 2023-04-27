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
    return 1

def compute_parallelism_factor(input_rows, input_cols, data_depth):
    return min(32, data_depth)

mif_gen_test = re.compile("([A-Za-z0-9_]+)(_subblock_([0-9]+)).init_mif")
def generate_layer(path, layer_name, input_rows, input_cols, data_depth, parallelism_factor, use_BRAMs=False, pregened_memfiles=None):

    # Generate toolchain input files
    generate_layer_fpea(path,layer_name, input_rows, input_cols, data_depth, parallelism_factor)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, input_rows, input_cols, data_depth, parallelism_factor, use_BRAMs)

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



def generate_layer_fpea(path, layer_name, input_rows, input_cols, data_depth, parallelism_factor):
    assert data_depth >= parallelism_factor and data_depth % parallelism_factor == 0
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "DEF input_rows %i ;\n"%(input_rows, )
    fpea += "DEF input_cols %i ;\n"%(input_cols, )
    fpea += "DEF data_depth %i ;\n"%(data_depth, )
    fpea += "DEF par_factor %i ;\n"%(parallelism_factor, )
    fpea += "\n"

    fpea += "// Define meaningfully names for Block access managers\n"
    fpea += "DEF first_element  0 ;\n"
    fpea += "DEF second_element 1 ;\n"
    fpea += "DEF reg_file_addr  2 ;\n"
    fpea += "\n"

    fpea += "RESET BAM[first_element];\n"
    fpea += "RESET BAM[second_element];\n"
    fpea += "RESET BAM[reg_file_addr];\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "// Handle each pair of rows\n"
    fpea += "ZOL (input_rows / 2)\n"
    fpea += "{\>\n"

    fpea += "// Handle upper row of pair\n"
    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Handle Store first upper elements\n"
    if data_depth == parallelism_factor:
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "PMOV(par_factor, REG[0], RAM[BAM[first_element]<FORWARD>]);\n"
    else:
        fpea += "ZOL (data_depth/par_factor)\n"
        fpea += "{\>\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "PMOV(par_factor, REG[0], RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
    fpea += "\n"


    fpea += "// Handle second upper elements\n"
    if data_depth == parallelism_factor:
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
    else:
        fpea += "ZOL (data_depth/par_factor)\n"
        fpea += "{\>\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[second_element]<FORWARD>], RAM[BAM[second_element]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
    fpea += "\n"

    fpea += "\<}\n"
    fpea += "\n"


    fpea += "// Handle lower row of pair\n"
    fpea += "ZOL (input_cols / 2)\n"
    fpea += "{\>\n"

    fpea += "// Handle first lower elements\n"
    if data_depth == parallelism_factor:
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
    else:
        fpea += "ZOL (data_depth/par_factor)\n"
        fpea += "{\>\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[first_element]<FORWARD>], RAM[BAM[first_element]<FORWARD>]);\n"
        fpea += "\<}\n"
    fpea += "\n"

    fpea += "// Handle second lower elements\n"
    if data_depth == parallelism_factor:
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[second_element]<FORWARD>], REG[0]);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (REG[BAM[reg_file_addr]<FORWARD>], PUT[0]);\n"
        fpea += "\<}\n"
    else:
        fpea += "ZOL (data_depth/par_factor)\n"
        fpea += "{\>\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (GET[0]<ADV>, REG[BAM[reg_file_addr]<FORWARD>]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "POR(par_factor, REG[0], RAM[BAM[second_element]<FORWARD>], REG[0]);\n"
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        fpea += "ZOL (par_factor)\n"
        fpea += "{\>\n"
        fpea += "MOV (REG[BAM[reg_file_addr]<FORWARD>], PUT[0]);\n"
        fpea += "\<}\n"
        fpea += "NOP;\n"
        fpea += "\<}\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "\<}\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "\<}\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "\<}\n"


    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, input_rows, input_cols, data_depth, parallelism_factor, use_BRAMs):
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
                "step_max": parallelism_factor
            },
            "BAM_1": {
                "addr_max": RAM_depth - 1,
                "offset_max": RAM_depth - 1,
                "step_max": parallelism_factor
            },
            "BAM_2": {
                "addr_max": parallelism_factor - 1,
                "offset_max": parallelism_factor - 1,
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
                "data_width": 1,
                "depth": parallelism_factor
            }
        },
        "execute_units": {
            "ALU": {
                "data_width": 1
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
      "BAM_0_increment": parallelism_factor,
      "BAM_1_base": 0,
      "BAM_1_increment": parallelism_factor,
      "BAM_2_base": 0,
      "BAM_2_increment": 1,
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
