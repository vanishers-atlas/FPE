# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    raise NotImplementedError()

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    raise NotImplementedError()

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    raise NotImplementedError()

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "has_enable" in config_in.keys(), "Passed config lacks has_enable key"
    assert type(config_in["has_enable"]) is bool, "has_enable must be a bool"
    config_out["has_enable"] = config_in["has_enable"]

    assert "clocked" in config_in.keys(), "Passed config lacks clocked key"
    assert type(config_in["clocked"]) is bool, "clocked must be a bool"
    config_out["clocked"] = config_in["clocked"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        if config["clocked"]:
            generated_name = "RS_flipflop"
        else:
            generated_name = "RS_latch"

        # Handle enable
        if config["has_enable"] == True:
            generated_name += "_enable"

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
        generate_logic(gen_det, com_det)


        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_logic(gen_det, com_det):

    # Declare ports
    com_det.add_port("R", "std_logic", "in")
    com_det.add_port("S", "std_logic", "in")
    com_det.add_port("Q", "std_logic", "out")
    if gen_det.config["clocked"]:
        com_det.add_port("clock", "std_logic", "in")
    if gen_det.config["has_enable"]:
        com_det.add_port("enable", "std_logic", "in")

    # Generate process start
    if gen_det.config["clocked"]:
        com_det.arch_body  += "process (clock)\n"
        com_det.arch_body  += "begin\n\>"
        com_det.arch_body += "if rising_edge(clock) then\n\>"
    else:
        com_det.arch_body  += "process (R, S"

        if gen_det.config["has_enable"]:
            com_det.arch_body  += ", enable"
        com_det.arch_body  += ")\n"
        com_det.arch_body  += "begin\n\>"

    if gen_det.config["has_enable"]:
        com_det.arch_body += "if enable = '1' then\n\>"

    com_det.arch_body += "if R = '1' and S = '0' then\n\>"
    com_det.arch_body += "Q <= '0';\n"
    com_det.arch_body += "\<elsif R = '0' and S = '1' then\n\>"
    com_det.arch_body += "Q <= '1';\n"
    com_det.arch_body += "\<elsif R = '1' and S = '1' then\n\>"
    com_det.arch_body += "Q <= 'X';\n"
    com_det.arch_body += "\<end if;\n"


    if gen_det.config["has_enable"]:
        com_det.arch_body += "\<end if;\n"

    if gen_det.config["clocked"]:
        com_det.arch_body += "\<end if;\n"

    com_det.arch_body += "\<end process;\n"
