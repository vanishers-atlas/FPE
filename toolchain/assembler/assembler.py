# Import ParseTreeWalker from antlr so extactors can walk loading tree
from antlr4 import ParseTreeWalker

# Import json for reading/writing json files
import json

# import FPE assembly handling module
from .. import FPE_assembly as asm_utils
from ..HDL_generation import utils  as gen_utils
from .. import utils  as tc_utils

from . import label_handling
from . import IMM_handling
from . import program_handling

def determine_require_generics(interface):
    generics = {}
    for generic in interface["generics"]:
        if generic["name"] in [
            "IMM_mem_file",
            "PM_mem_file",
            "PC_end_value",
        ]:
            pass
        else:
            generics[generic["name"]] = None
    return generics

def merge_generics(required, given, config = None):
    # Copy required generics into config
    if config == None:
        config = required.copy()

    # Loop over given generics
    for k, v in given.items():
        if k not in config or not isinstance(v, dict):
            config[k] = v
        else:
            merge_generics(None, v, config[k])
    return config

def check_for_none(data):
    for v in data.values():
        if isinstance(v, dict):
            if check_for_none(v):
                return True
        elif v == None:
            return True
    return False


def write_mif_file(filename, depth, width, data):
    with open(filename, "w") as f:
        addr_width = tc_utils.unsigned.width(depth - 1)
        for address in range(depth):
            value = data[address]
            if value > 0:
                f.write("%s\n"%(tc_utils.unsigned .encode(data[address], width), ) )
            else:
                f.write("%s\n"%(tc_utils.twos_comp.encode(data[address], width), ) )


def run(assembly_filename, config_filename, interface_filename, generic_file, processor_name, output_path):
    with open(config_filename, "r") as f:
        config = json.load(f)

    with open(interface_filename, "r") as f:
        interface = json.load(f)

    required_generics = determine_require_generics(interface)

    # Handle generic file
    try:
        # Load input generics
        with open(generic_file, "r") as f:
            given_generics = json.loads(f.read())

        # Check that all required generics are given
        generics = merge_generics(required_generics, given_generics)
        if check_for_none(generics):
            # Create blank generic file
            with open("required_generics.json", "w") as f:
                f.write(json.dumps(generics, sort_keys=True, indent=4))
            raise ValueError("Not all generics given, a partual filled in generic file was created, please replace the nulls")
    except FileNotFoundError:
        # Create blank generic file
        with open("required_generics.json", "w") as f:
            f.write(json.dumps({}, sort_keys=True, indent=4))
        raise ValueError("No generics file given, a blank one was created, please replace the nulls")

    # Prepare for processing assembly
    assembly = asm_utils.load_file(assembly_filename)
    walker = ParseTreeWalker()

    handler = label_handling.handler()
    walker.walk(handler, assembly)
    label_pc_map = handler.get_output()

    if "IMM" in config["data_memories"]:
        handler = IMM_handling.handler(label_pc_map)
        walker.walk(handler, assembly)
        imm_data, IMM_addr_map = handler.get_output()
        write_mif_file(output_path + "\\IMM.mem", config["data_memories"]["IMM"]["depth"], config["data_width"], imm_data)
        generics["IMM_mem_file"] = "IMM.mem"
    else:
        IMM_addr_map = {}

    handler = program_handling.handler(config, label_pc_map, IMM_addr_map)
    walker.walk(handler, assembly)
    program_end, program = handler.get_output()
    write_mif_file(output_path + "\\PM.mem", config["fetch_decode"]["program_length"], config["opcode_width"] + (config["fetch_decode"]["encoded_addrs"]*config["addr_width"]), program)
    generics["PM_mem_file"]  = "PM.mem"
    generics["PC_end_value"] = program_end

    # Generate testbench style file, with example instancation
    IMPORTS   = []
    ARCH_HEAD = gen_utils.indented_string()
    ARCH_BODY = gen_utils.indented_string()
    INTERFACE = { "ports" : [], "generics" : [] }

    # Include extremely commom libs
    IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

    ARCH_BODY +=  "%s_instance : entity work.%s(arch)\n\>"%(processor_name, processor_name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda g : g["name"]):
            if generic["type"] == "string":
                ARCH_BODY += "%s => \"%s\",\n"%(generic["name"], generics[generic["name"]])
            else:
                ARCH_BODY += "%s => %s,\n"%(generic["name"], generics[generic["name"]])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    for port in sorted(interface["ports"], key=lambda p : p["name"] ):
        INTERFACE["ports"].append(port)
        ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"


    # Save code to file
    gen_utils.generate_files(output_path, processor_name + "_inst", IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)
