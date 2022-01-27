# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

# Import ParseTreeWalker from antlr so extactors can walk loading tree
from antlr4 import ParseTreeWalker

# Import json for reading/writing json files
import json

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

# import import assembler files (extactors)
from FPE.toolchain.assembler import IMM_handling
from FPE.toolchain.assembler import PM_handling
from FPE.toolchain.assembler import ZOL_handling

def determine_require_generics(interface):
    generics = {}
    for generic in interface["generics"].keys():
        # Skipped handled generics
        if generic in [ "IMM_init_mif", "PM_init_mif", "PC_end_value", ]:
            pass
        # Skipped handled ZOL generics
        elif generic.startswith("bound_ZOL_"):
            pass
        else:
            generics[generic] = None
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
    program_context = asm_utils.load_file(assembly_filename)
    walker = ParseTreeWalker()

    # Handle IMM memory
    if "IMM" in config["data_memories"]:
        imm_file = processor_name + "_IMM.mem"

        handler = IMM_handling.handler(program_context)
        walker.walk(handler, program_context["program_tree"])
        imm_data = handler.get_output()

        program_context["IMM_addr_map"] = {
            v : a
            for (a, v) in imm_data.items()
        }
        # pad imm_data to correct depth, should only trigger when a jump label and an imm operand share the same value
        for i in range(len(imm_data), config["data_memories"]["IMM"]["depth"]):
            imm_data[i] = 0

        write_mif_file(output_path + "\\" + imm_file, config["data_memories"]["IMM"]["depth"], config["data_memories"]["IMM"]["data_width"], imm_data)

        generics["IMM_init_mif"] = imm_file
    else:
        program_context["IMM_addr_map"] = {}

    # Handle program memory
    handler = PM_handling.handler(config, program_context)
    pm_file = processor_name + "_PM.mem"
    walker.walk(handler, program_context["program_tree"])
    program_end, program = handler.get_output()

    write_mif_file(
        output_path + "\\" + pm_file,
        config["program_flow"]["program_length"],
        config["instr_decoder"]["opcode_width"] + sum(config["instr_decoder"]["addr_widths"]),
        program
    )

    generics["PM_init_mif"]  = pm_file
    generics["PC_end_value"] = program_end

    # Handle ZOL values
    if "ZOL_overwrites_encoding" in interface.keys():
        handler = ZOL_handling.handler(program_context, interface["ZOL_overwrites_encoding"])
        walker.walk(handler, program_context["program_tree"])

        for ZOL_name, values in handler.get_output().items():
            generics["%s_overwrites" %(ZOL_name)] = values["overwrites"]
            generics["%s_check_value"%(ZOL_name)] = values["check_value"]
            generics["%s_overwrite_value"  %(ZOL_name)] = values["overwrite_value"]

    # Generate testbench style file, with example instancation
    IMPORTS   = []
    ARCH_HEAD = gen_utils.indented_string()
    ARCH_BODY = gen_utils.indented_string()
    INTERFACE = { "ports" : {}, "generics" : {} }

    # Include extremely commom libs
    IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

    ARCH_BODY +=  "%s_instance : entity work.%s(arch)\n\>"%(processor_name, processor_name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in interface["generics"].keys():
            details = interface["generics"][generic]
            if details["type"] == "string" or details["type"].startswith("std_logic_vector"):
                ARCH_BODY += "%s => \"%s\",\n"%(generic, generics[generic])
            else:
                ARCH_BODY += "%s => %s,\n"%(generic, generics[generic])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    for port in interface["ports"].keys():
        details = interface["ports"][port]
        INTERFACE["ports"][port] = details
        ARCH_BODY += "%s => %s,\n"%(port, port)

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    # Save code to file
    gen_utils.generate_files(output_path, processor_name + "_inst", IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)
