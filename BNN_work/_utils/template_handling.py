# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import json
import math
import os
from FPE.toolchain import utils as tc_utils

from antlr4 import *
from . import templated_json

def realise_template(output_path, output_name, tempate_select, templated_values):

    # Ensure that path exist for the rest of the file
    os.makedirs(output_path, exist_ok=True)

    realise_program(output_path, output_name, tempate_select, templated_values)
    parameters = realise_parameters(output_path, output_name, tempate_select, templated_values)
    generics = realise_generics(output_path, output_name, tempate_select, templated_values)
    handle_memfiles(output_path, parameters, generics)


def realise_program(output_path, output_name, tempate_select, templated_values):
    with open(tempate_select + ".program.fpea", "r") as f:
        template = f.read()

    # Subitute templated_values in template
    for k,v in templated_values.items():
        template = template.replace("$"+k, str(v))

    # Check that all missing sections of the template have been filled if __name__ == '__main__':
    if template.count("$") != 0:
        with open("template.dump", "w") as f:
            f.write(template)
        raise ValueError("Not all templated values within the template supplied, please check template.dump to find missed values and supplies them")


    with open(output_path + "\\" + output_name + ".fpea", "w") as f:
        f.write(template)


def realise_parameters(output_path, output_name, tempate_select, templated_values):
    # Load template file into antlr
    inputFile = tempate_select + ".parameters.json"
    input  = FileStream(inputFile)
    lexer  = templated_json.Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = templated_json.Parser(stream)
    tree   = parser.obj()

    # Walk the anltr tree genetate the ouptu json
    walker = ParseTreeWalker()
    transformer = templated_json.Transformer(templated_values)
    walker.walk(transformer, tree)
    parameters = transformer.return_json()


    with open(output_path + "\\" + output_name + "_parameters.json", "w") as f:
        f.write(json.dumps(parameters, indent=2))

    return parameters


def realise_generics(output_path, output_name, tempate_select, templated_values):
    # Load template file into antlr
    inputFile = tempate_select + ".generics.json"
    input  = FileStream(inputFile)
    lexer  = templated_json.Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = templated_json.Parser(stream)
    tree   = parser.obj()

    # Walk the anltr tree genetate the ouptu json
    walker = ParseTreeWalker()
    transformer = templated_json.Transformer(templated_values)
    walker.walk(transformer, tree)
    generics = transformer.return_json()

    with open(output_path + "\\" + output_name + "_generics.json", "w") as f:
        f.write(json.dumps(generics, indent=2))

    return generics


def handle_memfiles(output_path, parameters, generics):
    # Gather all required memfites for generics
    memfiles = set()
    for k, v in generics.items():
        if k.endswith("_mem_file") and v.split("\\")[-1].startswith("blankmem_"):
            memfiles.add(v)
    memfiles = list(memfiles)

    for memfile in memfiles:
        mem_width, mem_depth = memfile.split("_")[-1].split(".")[0].split("x")
        mem_width = int(mem_width)
        mem_depth = int(mem_depth)
        pathend = memfile.lstrip(".").lstrip("\\")

        # Generate file is junk data to stop vivado later strip it out
        with open(output_path + "\\" + pathend, "w") as f:
            data = math.floor( ((2**mem_width) - 1)/3)
            step = 1
            for line in range(mem_depth):
                if data < 0:
                    data = 0
                    step = 1
                elif data > (2**mem_width) - 1:
                    data = (2**mem_width) - 1
                    step = -1

                f.write(tc_utils.unsigned.encode(data, mem_width))
                data += step
                f.write("\n")
