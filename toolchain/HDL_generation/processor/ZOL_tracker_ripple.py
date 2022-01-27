# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))


import math

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.processor import ZOL_inverted_SR_FSM

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    for instr in instr_set:
        if asm_utils.instr_exe_unit(instr) == instr_id:
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SET":
                raise ValueError("Ripple tracker doesn't support ZOL_SET instructions")
            elif mnemonic in ["ZOL_SEEK", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)

    return config


def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = {}

    return pathways


def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls


#####################################################################

SRL_BAIS  = 1
SRL_RANGE = 31
SRL_WIDTH = math.ceil(math.log(SRL_RANGE, 2))

def preprocess_config(config_in):
    config_out = {}


    assert "overwrites" in config_in.keys(), "Passed config lacks overwrites key"
    assert type(config_in["overwrites"]) is  int, "overwrites must in an integer"
    assert config_in["overwrites"] > 0, "overwrites mst be greater than 0"

    config_out["overwrites"] = config_in["overwrites"]

    config_out["tallies"] = tc_utils.biased_tally.width(
        config_in["overwrites"],
        SRL_BAIS,
        SRL_RANGE
    )

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL_tracker_ripple"

        # Add min and max overwrites
        generated_name += "_%i_%i"%(
                SRL_BAIS * config["tallies"],
                (SRL_BAIS + SRL_RANGE) * config["tallies"],
            )

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name=None, concat_naming=False, force_generation=False):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, config)
    CONCAT_NAMING = concat_naming
    FORCE_GENERATION = force_generation

    # Load return variables from pre-exiting file if allowed and can
    try:
        return gen_utils.load_files(FORCE_GENERATION, OUTPUT_PATH, MODULE_NAME)
    except gen_utils.FilesInvalid:
        # Generate new file
        global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

        # Init generation and return varables
        IMPORTS   = []
        ARCH_HEAD = gen_utils.indented_string()
        ARCH_BODY = gen_utils.indented_string()
        INTERFACE = {
            "generics" : {
                "overwrites" : {
                    "type" : "std_logic_vector",
                    "width" : SRL_WIDTH*CONFIG["tallies"],
                }
            },
            "ports" : {
                "clock" : {
                    "type" : "std_logic",
                    "direction" : "in",
                },
                "match_found" : {
                    "type" : "std_logic",
                    "direction" : "in",
                },
                "overwrites_reached" : {
                    "type" : "std_logic",
                    "direction" : "out",
                },
            },
            "overwrites_encoding" : {
                "type"      : "biased_tally",
                "bias"      : SRL_BAIS,
                "range"     : SRL_RANGE,
                "tallies"   : CONFIG["tallies"]
            },
        }

        # Include required libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
            {
                "library" : "UNISIM",
                "package" : "vcomponents",
                "parts" : "all"
            },
        ]



        # Generation Module Code
        generate_state_machine()
        generate_SRLs()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_state_machine():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_FSM"
    else:
        module_name = None

    sub_interface, sub_name = ZOL_inverted_SR_FSM.generate_HDL(
        {},
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "state_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    assert len(sub_interface["generics"]) == 0
    # ARCH_BODY += "generic map ()\n"

    assert len(sub_interface["ports"]) == 4
    assert "clock" in sub_interface["ports"].keys()
    assert "match_found" in sub_interface["ports"].keys()
    assert "not_tracking" in sub_interface["ports"].keys()
    assert "overwrites_reached" in sub_interface["ports"].keys()

    ARCH_BODY += "port map (\n\>"

    ARCH_HEAD += "signal not_tracking : std_logic;\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "match_found  => match_found,\n"
    ARCH_BODY += "overwrites_reached => overwrites_reached_int,\n"
    ARCH_BODY += "not_tracking  => not_tracking\n"

    ARCH_BODY += "\<);\n\<\n"

def generate_SRLs():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- Ripple iteration tracker\n"
    ARCH_HEAD += "signal overwrites_reached_int : std_logic;\n"

    # Generate ripple chain of SRLC32Es
    for ripple in range(CONFIG["tallies"]):
        ARCH_HEAD += "signal ripple_%i_out : std_logic;\n"%(ripple, )

        ARCH_BODY += "ripple_%i : SRLC32E\n\>"%(ripple)
        ARCH_BODY += "generic map (INIT => X\"00000000\")\n"
        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "A => overwrites(%i downto %i),\n"%(5*ripple + 4, 5*ripple)

        # Handle the specail case of the first SRL
        if ripple == 0:
            ARCH_BODY += "D => not_tracking,\n"
        else:
            ARCH_BODY += "D => ripple_%i_out,\n"%(ripple - 1)

        ARCH_BODY += "Q => ripple_%i_out,\n"%(ripple)
        ARCH_BODY += "CLK => clock,\n"
        ARCH_BODY += "CE => match_found,\n"
        ARCH_BODY += "Q31 => open\n"
        ARCH_BODY += "\<);\n\<\n"

    # Connect output of final SRLC32E to overwrites_reached
    ARCH_BODY += "overwrites_reached_int <=  ripple_%i_out;\n"%(CONFIG["tallies"] - 1)
    ARCH_BODY += "overwrites_reached <=  overwrites_reached_int;\n"
