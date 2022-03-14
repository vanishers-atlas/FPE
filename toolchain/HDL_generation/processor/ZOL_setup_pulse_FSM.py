# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL_setup_pulse_FSM"

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
            "ports" : { },
            "generics" : { },
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]


        # Generation Module Code
        generate_FSM()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_FSM():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Declare required ports
    INTERFACE["ports"]["clock"] = {
        "name"      : "clock",
        "direction" : "in",
        "type"      : "std_logic",
    }
    INTERFACE["ports"]["match_found"] = {
        "direction" : "in",
        "type"      : "std_logic",
    }
    INTERFACE["ports"]["overwrites_reached"] = {
        "direction" : "in",
        "type"      : "std_logic",
    }
    INTERFACE["ports"]["PC_running"] = {
        "direction" : "in",
        "type"      : "std_logic",
    }
    INTERFACE["ports"]["setup"] = {
        "direction" : "out",
        "type"      : "std_logic",
    }


    # Describe FSM
    ARCH_HEAD += "-- State signal values\n"
    ARCH_HEAD += "-- '1' : Setup\n"
    ARCH_HEAD += "-- '0' : RUNNING\n"
    ARCH_HEAD += "signal curr_state : std_logic := '1';\n"
    ARCH_HEAD += "signal next_state : std_logic;\n"

    ARCH_BODY += "-- State Buffering\n"
    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "curr_state <= next_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"

    ARCH_BODY += "-- next_state computing\n"
    ARCH_BODY += "next_state <=\> '1' when curr_state = '0' and overwrites_reached = '1' and match_found = '1'\n"
    #ARCH_BODY += "else '1' when PC_running /= '1'\n"
    ARCH_BODY += "else '0';\<\n\n"

    ARCH_BODY += "setup <=  '1' when curr_state = '1' or PC_running /= '1' else '0';\n"
