# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import copy

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.basic import RS_FF_latch
from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

import json

def add_inst_config(instr_id, instr_set, config):

    PC_only_jump = False
    ALU_jump = False

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if mnemonic == "JMP":
                PC_only_jump = True

            if mnemonic in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
                ALU_jump = True


    config["PC_only_jump"] = PC_only_jump
    config["ALU_jump"] = ALU_jump

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    # Handle fetched_operand ports
    if "jump_value" in interface["ports"]:
        for instr in instr_set:
            if instr_id in asm_utils.instr_exe_units(instr):
                mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
                if mnemonic in ["JMP", "JEQ", "JNE", "JGT", "JGE", "JLT", "JTE", ]:
                    gen_utils.add_datapath_dest(pathways, "%sfetch_data_0_word_0"%(lane, ),
                        "exe", instr, instr_prefix + "PC_jump_value", "unsigned", interface["ports"]["jump_value"]["width"]
                    )

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle acc_enable control
    if "PC_only_jump" in interface["ports"].keys():
        PC_only_jump = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JMP", ]:
                PC_only_jump["1"].append(instr)
            else:
                PC_only_jump["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "PC_PC_only_jump", PC_only_jump, "std_logic")


    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Handle stalling
    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    # Handle counter value
    assert(config_in["program_length"] > 0)
    config_out["program_length"] = config_in["program_length"]
    config_out["PC_width"] = tc_utils.unsigned.width(config_out["program_length"] - 1)

    # Hanlde ZOLs
    config_out["ZOLs_present"] = len(config_in["ZOLs"]) > 0

    # Handle jumping
    assert(type(config_in["PC_only_jump"]) == bool)
    config_out["PC_only_jump"] = config_in["PC_only_jump"]

    assert(type(config_in["ALU_jump"]) == bool)
    config_out["ALU_jump"] = config_in["ALU_jump"]

    return config_out

import zlib

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "PC"

        generated_name += "_%ir"%2**config["PC_width"]

        if config["stallable"]:
            generated_name += "_stall"

        if config["PC_only_jump"]:
            generated_name += "_JMP"

        if config["ALU_jump"]:
            generated_name += "_ALU"

        if config["ZOLs_present"]:
            generated_name += "_ZOL"


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
        com_det.add_import("ieee", "numeric_std", "all")

        # Setop common ports
        com_det.add_port("clock", "std_logic", "in")

        # Generation Module Code
        gen_running_FF(gen_det, com_det)
        gen_value_reg(gen_det, com_det)
        gen_end_checking(gen_det, com_det)
        gen_next_value_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_running_FF(gen_det, com_det):

    # Declare ports
    com_det.add_port("kickoff", "std_logic", "in")
    com_det.add_port("running", "std_logic", "out")

    com_det.arch_head += "signal running_internal : std_logic;\n"

    RSFF_interface, RSFF_name = RS_FF_latch.generate_HDL(
        {
            "has_enable": False,
            "clocked"   : True,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "running_FF : entity work.%s(arch)\>\n"%(RSFF_name, )
    com_det.arch_body += "generic map ( stating_state => '0')\n"
    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "S => kickoff and not program_end_reached,\n"
    com_det.arch_body += "R =>program_end_reached,\n"
    com_det.arch_body += "Q => running_internal\n"
    com_det.arch_body += "\<);\n\<\n"

    com_det.arch_body += "running <= running_internal;\n\n"

def gen_value_reg(gen_det, com_det):

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : True,
            "has_enable"    : True,
            "force_on_init" : True
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "value_reg : entity work.%s(arch)\>\n"%(reg_name, )
    com_det.arch_body += "generic map (\>\n"
    com_det.arch_body += "data_width => %i,\n"%(gen_det.config["PC_width"], )
    com_det.arch_body += "force_value => 0\n"
    com_det.arch_body += "\<)\n"

    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "force => program_end_reached,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "enable  => running_internal and not stall_in,\n"
    else:
        com_det.arch_body += "enable  => running_internal,\n"

    com_det.arch_head += "signal curr_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

    com_det.arch_body += "data_in  => next_value,\n"
    com_det.arch_body += "data_out => curr_value\n"
    com_det.arch_body += "\<);\n\<\n"

    com_det.add_port("value", "std_logic_vector", "out", gen_det.config["PC_width"])
    com_det.arch_body += "value <= curr_value;\n\n"

def gen_end_checking(gen_det, com_det):
    com_det.add_generic("end_value", "integer")

    com_det.arch_head += "signal program_end_reached : std_logic;\n"
    com_det.arch_body += "program_end_reached <= '1' when to_integer(unsigned(curr_value)) = end_value else '0';\n\n"

def gen_next_value_logic(gen_det, com_det):
    com_det.arch_head += "signal next_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )
    value_tail = "next_value"

    _, mux_2 = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    if gen_det.config["PC_only_jump"] or gen_det.config["ALU_jump"]:
        com_det.add_port("jump_value", "std_logic_vector", "in", gen_det.config["PC_width"])

        if gen_det.config["PC_only_jump"]:
            com_det.add_port("PC_only_jump", "std_logic", "in")
        if gen_det.config["ALU_jump"]:
            com_det.add_port("ALU_jump", "std_logic", "in")

        com_det.arch_body += "jumping_mux : entity work.%s(arch)\>\n"%(mux_2, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["PC_width"], )

        com_det.arch_body += "port map (\n\>"

        if   gen_det.config["PC_only_jump"] and gen_det.config["ALU_jump"]:
            com_det.arch_body += "sel(0) => PC_only_jump or ALU_jump,\n"
        elif gen_det.config["PC_only_jump"] and not gen_det.config["ALU_jump"]:
            com_det.arch_body += "sel(0) => PC_only_jump,\n"
        elif not gen_det.config["PC_only_jump"] and gen_det.config["ALU_jump"]:
            com_det.arch_body += "sel(0) => ALU_jump,\n"
        else:
            raise ValueError("Unknown jump case")

        com_det.arch_head += "signal jump_fail_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

        com_det.arch_body += "data_in_0 => jump_fail_value,\n"
        com_det.arch_body += "data_in_1 => jump_value,\n"

        com_det.arch_body += "data_out  => %s\n"%(value_tail, )
        value_tail = "jump_fail_value"

        com_det.arch_body += "\<);\n\<\n"

    if gen_det.config["ZOLs_present"]:
        com_det.add_port("zero_overhead_value", "std_logic_vector", "in", gen_det.config["PC_width"])
        com_det.add_port("zero_overhead_overwrite", "std_logic", "in")

        com_det.arch_body += "zero_overhead_mux : entity work.%s(arch)\>\n"%(mux_2, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["PC_width"], )

        com_det.arch_body += "port map (\n\>"

        com_det.arch_body += "sel(0) => zero_overhead_overwrite,\n"

        com_det.arch_head += "signal zero_overhead_fail_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

        com_det.arch_body += "data_in_0 => zero_overhead_fail_value,\n"
        com_det.arch_body += "data_in_1 => zero_overhead_value,\n"

        com_det.arch_body += "data_out  => %s\n"%(value_tail, )
        value_tail = "zero_overhead_fail_value"

        com_det.arch_body += "\<);\n\<\n"


    com_det.arch_head += "signal inc_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

    com_det.arch_body += "inc_value <= std_logic_vector(to_unsigned(to_integer(unsigned(curr_value)) + 1, %i));\n"%(gen_det.config["PC_width"], )
    com_det.arch_body += " %s <= inc_value;\n\n"%(value_tail, )
