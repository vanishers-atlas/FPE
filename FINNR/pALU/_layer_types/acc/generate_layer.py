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

def compute_popcount(input_neurons):
    return tc_utils.unsigned.width(input_neurons)

def compute_parallelism_factor(input_neurons):
    width = compute_popcount(input_neurons)

    for p_fact in [2, 4, 8, 16, 32]:
        if width * p_fact + p_fact - 1 <= 48:
            return p_fact

mif_gen_test = re.compile("([A-Za-z0-9_]+)(_subblock_([0-9]+)).init_mif")
def generate_layer(path, layer_name, input_neurons, output_neurons, parallelism_factor, use_BRAMs=False, pregened_memfiles=None):
    # Generate toolchain input files
    generate_layer_fpea(path, layer_name, input_neurons, output_neurons, parallelism_factor)
    parameters, generics = generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, parallelism_factor, use_BRAMs)

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



def generate_layer_fpea(path, layer_name, input_neurons, output_neurons, parallelism_factor):
    fpea = IndentedString()

    fpea += "{\>\n"

    fpea += "// Define layer constants\n"
    fpea += "DEF input_neurons  %i ;\n"%(input_neurons, )
    fpea += "DEF output_neurons %i ;\n"%(output_neurons, )
    fpea += "DEF par_factor %i ;\n"%(parallelism_factor, )
    fpea += "\n"

    fpea += "// Define meaningfully names for Block access managers\n"
    fpea += "DEF acts_write 0 ;\n"
    fpea += "DEF acts_read  1 ;\n"
    fpea += "DEF weights    2 ;\n"
    fpea += "\n"

    fpea += "// Define meaningfully names for reg locations\n"
    if parallelism_factor == input_neurons:
        fpea += "DEF pop_acc par_factor;\n"
    else:
        fpea += "DEF pop_acc 2 * par_factor;\n"
    fpea += "\n"

    fpea += "RESET BAM[acts_write] ;\n"
    fpea += "RESET BAM[acts_read] ;\n"
    fpea += "RESET BAM[weights] ;\n"
    fpea += "NOP;\n"
    fpea += "\n"

    fpea += "// Read input data to RAM\n"
    fpea += "ZOL (input_neurons)\n"
    fpea += "{\>\n"
    fpea += "MOV( GET[0]<ADV>, RAM[BAM[acts_write]<FORWARD>] ) ;\n"
    fpea += "\<}\n"
    if parallelism_factor == input_neurons:
        fpea += "NOP;\n"
        fpea += "NOP;\n"
    fpea += "\n"

    fpea += "// Process each output neuron in turn\n"
    fpea += "ZOL (output_neurons)\n"
    fpea += "{\>\n"
    if parallelism_factor == input_neurons:
        fpea += "MOV (0, REG[pop_acc]);\n"

        fpea += "// Compute popcount\n"
        fpea += "PXNOR (par_factor, RAM[BAM[acts_read]<FORWARD>], ROMA[BAM[weights]<FORWARD>], ACC ) ;\n"
        fpea += "PAND  (par_factor, ACC, ROMA[input_neurons * output_neurons], REG[0] ) ;\n"%()
        fpea += "NOP;\n"
        fpea += "NOP;\n"
        for p_factor in [16,8,4,2]:
            if (2*p_factor) <= parallelism_factor:
                fpea += "PADD (%i, REG[0], REG[%i], REG[0]) ;\n"%(p_factor, p_factor, )
                fpea += "NOP;\n"
                fpea += "NOP;\n"
        fpea += "ADD (REG[0], REG[1], ACC) ;\n"
        fpea += "ADD (REG[pop_acc], ACC, REG[pop_acc]);\n"
    else:
        fpea += "MOV (0, REG[pop_acc]);\n"

        fpea += "// Compute popcount\n"
        fpea += "ZOL (input_neurons/(2*par_factor) )\n"
        fpea += "{\>\n"
        fpea += "PXNOR (par_factor, RAM[BAM[acts_read]<FORWARD>], ROMA[BAM[weights]<FORWARD>], ACC ) ;\n"
        fpea += "PAND  (par_factor, ACC, ROMA[input_neurons * output_neurons], REG[0] ) ;\n"%()
        fpea += "PXNOR (par_factor, RAM[BAM[acts_read]<FORWARD>], ROMA[BAM[weights]<FORWARD>], ACC ) ;\n"
        fpea += "PAND  (par_factor, ACC, ROMA[input_neurons * output_neurons], REG[par_factor] ) ;\n"%()
        for p_factor in [16,8,4,2]:
            if (2*p_factor) <= parallelism_factor:
                fpea += "PADD (%i, REG[0], REG[%i], REG[0]) ;\n"%(p_factor, p_factor, )
                fpea += "NOP;\n"
                fpea += "PADD (%i, REG[par_factor], REG[par_factor + %i], REG[par_factor]) ;\n"%(p_factor, p_factor, )
        fpea += "ADD (REG[0], REG[1], ACC) ;\n"
        fpea += "ADD (REG[pop_acc], ACC, REG[pop_acc]);\n"
        fpea += "ADD (REG[par_factor], ACC, ACC);\n"
        fpea += "ADD (REG[par_factor + 1], ACC, REG[pop_acc]);\n"
        fpea += "\<}\n"

    fpea += "// Ou-put popcount\n"
    fpea += "MOV( ACC, PUT[0]);\n"

    fpea += "\<}\n"
    fpea += "NOP ;\n"

    fpea += "\<}\n"

    with open(path + "\\" + layer_name + "_program.fpea", "w") as f:
        f.write(str(fpea))


def generate_layer_parameters_and_generics(path, layer_name, input_neurons, output_neurons, parallelism_factor, use_BRAMs):

    number_wieghts = output_neurons * input_neurons
    number_theashords = output_neurons
    number_betas = output_neurons
    ROM_depth = number_wieghts + number_theashords + number_betas + parallelism_factor

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
            "BAM_0": { # acts_write
                "addr_max": RAM_depth - 1,
                "offset_max": RAM_depth - 1,
                "step_max": 1,
            },
            "BAM_1": { # acts_read
                "addr_max": RAM_depth - 1 ,
                "offset_max": RAM_depth - 1,
                "step_max": parallelism_factor,
            },
            "BAM_2": { # weights
                "addr_max": number_wieghts - 1 ,
                "offset_max": number_wieghts - 1,
                "step_max": parallelism_factor,
            },
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
            "hidden_ZOLs": {
                "tracker_type"  : "ripple",
                "pune_single_iteration" : False,
            },
        }
    }

    if parallelism_factor == input_neurons:
        parameters["data_memories"]["REG"]["depth"] = parallelism_factor + 1
    else:
        parameters["data_memories"]["REG"]["depth"] = 2*parallelism_factor + 1

    with open(path + "\\" + layer_name + "_parameters.json", "w") as f:
        f.write(json.dumps(parameters, sort_keys=True, indent=2))

    generics = {
        # acts_write
        "BAM_0_base": 0,
        "BAM_0_internal_step_value": 1,
        # acts_read
        "BAM_1_base": 0,
        "BAM_1_internal_step_value": parallelism_factor,
        # weights
        "BAM_2_base": 0,
        "BAM_2_internal_step_value": parallelism_factor,

        "RAM_init_mif": "..\\%s_RAM_A.mem"%(layer_name, ),
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
