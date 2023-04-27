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
from FPE.toolchain.HDL_generation import HDL_generator as HDL_generator

# import import assembler files (extactors)
from FPE.toolchain.assembler import IMM_handling
from FPE.toolchain.assembler import PM_handling
from FPE.toolchain.assembler import hidden_ZOL_handling
from FPE.toolchain.assembler import preloaded_rep_bank_handling

def determine_require_generics(interface):
    generics = {}
    for generic in interface["generics"].keys():
        # Skipped handled generics
        if generic in [ "IMM_init_mif", "PM_init_mif", "PC_end_value", ]:
            pass
        # Skipped handled ZOL generics
        elif generic.startswith("hidden_ZOL_"):
            pass
        # Skipped handled ZOL generics
        elif generic == "rep_bank_starting_loop_id" or generic.startswith("rep_bank_loop_"):
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

    # Handle hidden ZOL values
    if "hidden_ZOLs_overwrites_encoding" in interface.keys():
        handler = hidden_ZOL_handling.handler(program_context, interface["hidden_ZOLs_overwrites_encoding"])
        walker.walk(handler, program_context["program_tree"])

        for loop_name, values in handler.get_output().items():
            generics["%s_overwrites" %(loop_name)] = values["overwrites"]
            generics["%s_check_value"%(loop_name)] = values["check_value"]
            generics["%s_overwrite_value"  %(loop_name)] = values["overwrite_value"]


    if "rep_bank_preloaded_overwrites_encoding" in interface.keys():
        assert "rep_bank_preloaded_pc_values_encoding" in interface.keys() and "rep_bank_preloaded_loop_id_encoding" in interface.keys()

        handler = preloaded_rep_bank_handling.handler(program_context, interface["rep_bank_preloaded_overwrites_encoding"], interface["rep_bank_preloaded_pc_values_encoding"], interface["rep_bank_preloaded_loop_id_encoding"])
        walker.walk(handler, program_context["program_tree"])

        for loop_name, values in handler.get_loop_details().items():
            generics["%s_overwrites"%(loop_name)] = values["overwrites"]
            generics["%s_start_value"%(loop_name)] = values["start_value"]
            generics["%s_end_value"%(loop_name)] = values["end_value"]

        starting_loop_id, FSM_edges = handler.get_FSM_details()
        generics["rep_bank_starting_loop_id"] = starting_loop_id
        for loop_id, edges in FSM_edges.items():
            generics["rep_bank_loop_%i_on_overwrite"%(loop_id)] = edges[0]
            generics["rep_bank_loop_%i_on_fallthrough"%(loop_id)] = edges[2]
            if config["program_flow"]["rep_bank"]["stall_on_id_change"] == "CONDITIONALLY":
                generics["rep_bank_loop_%i_on_overwrite_stall"%(loop_id)] = edges[1]
                generics["rep_bank_loop_%i_on_fallthrough_stall"%(loop_id)] = edges[3]

    HDL_generator.wrap_module(processor_name, interface, generics, wrapped_name = processor_name + "_inst", HDL_output_path=output_path, full_wrap = True )
