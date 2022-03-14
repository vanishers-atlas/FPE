# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    config["operand_widths"] = [1, ]

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    raise NotImplementedError()

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    values = { "0" : [], "1" : [], }

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            fetches = asm_utils.instr_fetches(instr)
            # Check for MOV(ACC, X)
            if mnemonic_parts[0] in ["PMOV", "MOV", ] and len(fetches) == 0:
                values["0"].append(instr)
            else:
                values["1"].append(instr)
        else:
            values["0"].append(instr)

    gen_utils.add_control(controls, "exe", instr_prefix + "core_acc_enable", values, "std_logic")

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["stallable"]) == bool, "stallable must be a bool"
    config_out["stallable"] = config_in["stallable"]

    assert type(config_in["operand_widths"]) == list, "operand_widths must be a list"
    assert len(config_in["operand_widths"]) == 1, "operand_widths can only contrain 1 element"
    assert type(config_in["operand_widths"][0]) == int, "operand_widths' values must be ints"
    assert config_in["operand_widths"][0] >= 1, "operand_widths' values must be greater than 0"
    config_out["operand_widths"] = config_in["operand_widths"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = ""

        raise NotImplementedError()

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
        gen_passthrough_core(gen_det, com_det)


        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_passthrough_core(gen_det, com_det):

    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("acc_enable", "std_logic", "in")
    if gen_det.config["stallable"]:
        com_det.add_port("stall", "std_logic", "in")

    com_det.add_port("operand_0", "std_logic_vector", "in", gen_det.config["operand_widths"][0])
    com_det.add_port("result_0", "std_logic_vector", "out", gen_det.config["operand_widths"][0])


    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "delay_reg : entity work.%s(arch)\>\n"%(reg_name, )

    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["operand_widths"][0], )

    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "clock => clock,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => acc_enable and not stall,\n"
    else:
        com_det.arch_body += "enable => acc_enable,\n"
    com_det.arch_body += "data_in => operand_0,\n"
    com_det.arch_body += "data_out  => result_0 \n"

    com_det.arch_body += "\<);\n\<\n"
