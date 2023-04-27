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
        generated_name = "ZOL_inverted_SR_FSM"

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name=None, concat_naming=False, force_generation=False):

    # Check and preprocess parameters
    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"

    config = preprocess_config(config)
    module_name = handle_module_name(module_name, config)

    # Combine parameters into generation_details class for easy passing to functons
    gen_det = gen_utils.generation_details(config, output_path, module_name, concat_naming, force_generation)

    # Load return variables from pre-existing file if allowed and can
    try:
        return gen_utils.load_files(gen_det)
    except gen_utils.FilesInvalid:
        # Init component_details
        com_det = gen_utils.component_details()

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Generation Module Code
        generate_FSM(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_FSM(gen_det, com_det):
    # Declare required ports
    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("match_found", "std_logic", "in")
    com_det.add_port("overwrites_reached", "std_logic", "in")
    com_det.add_port("not_tracking", "std_logic", "out")

    # Describe FSM
    com_det.arch_head += "-- State signal values\n"
    com_det.arch_head += "-- '1' : Not Work/Setup\n"
    com_det.arch_head += "-- '0' : RUNNING\n"
    com_det.arch_head += "signal curr_state, next_state : std_logic := '1';\n\n"

    com_det.arch_body += "-- State Buffering\n"
    com_det.arch_body += "process (clock)\>\n"
    com_det.arch_body += "\<begin\>\n"
    com_det.arch_body += "if rising_edge(clock) and match_found = '1' then\>\n"
    com_det.arch_body += "curr_state <= next_state;\n"
    com_det.arch_body += "\<end if;\n"
    com_det.arch_body += "\<end process;\n\n"

    com_det.arch_body += "-- next_state computing\n"
    com_det.arch_body += "next_state <=\> '0' when curr_state = '1' and match_found = '1'\n"
    com_det.arch_body += "else '1' when curr_state = '0' and overwrites_reached = '1'\n"
    com_det.arch_body += "else curr_state;\<\n\n"

    com_det.arch_body += "not_tracking <= curr_state;\n"
