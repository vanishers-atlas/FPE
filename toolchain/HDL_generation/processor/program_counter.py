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
from FPE.toolchain.HDL_generation.basic import add_const
from FPE.toolchain.HDL_generation.basic import cmp_const

#####################################################################

import json

def add_inst_config(instr_id, instr_set, config):

    # Handle overwrites
    config["overwrite_sources"]  = []
    if "hidden_ZOLs" in config.keys() and len(config["hidden_ZOLs"]):
        config["overwrite_sources"].append("hidden_ZOLs")
    if "declared_ZOLs" in config.keys() and len(config["declared_ZOLs"]):
        config["overwrite_sources"].append("declared_ZOLs")
    if "rep_bank" in config.keys() and len(config["rep_bank"]["loops"]):
        config["overwrite_sources"].append("rep_bank_overwrite")

    # Handle PC only jumping, eg jmp
    for instr in instr_set:
        print(instr, asm_utils.instr_exe_units(instr))
        if asm_utils.instr_mnemonic(instr) == "JMP":
            config["jump_drivers"].append("PC_only_jump")

    return config

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    # Handle fetched_operand ports
    if "PC_only_jump" in config["jump_drivers"]:
        for instr in instr_set:
            if asm_utils.instr_mnemonic(instr) == "JMP":
                dataMesh.connect_sink(sink="PC_jump_value",
                    channel="%sfetch_data_0_word_0"%(lane, ),
                    condition=instr,
                    stage="exe", inplace_channel=True,
                    padding_type="unsigned", width=config["PC_width"]
                )

    return dataMesh

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle acc_enable control
    if "PC_only_jump" in config["jump_drivers"]:
        PC_only_jump = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JMP", ]:
                PC_only_jump["1"].append(instr)
            else:
                PC_only_jump["0"].append(instr)
        gen_utils.add_control(controls, "exe", "PC_only_jump", PC_only_jump, "std_logic")


    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Handle stalling
    assert type(config_in["stallable"]) == bool
    config_out["stallable"] = config_in["stallable"]

    # Handle counter value
    assert type(config_in["PC_width"]) == int
    assert config_in["PC_width"] > 0
    config_out["PC_width"] = config_in["PC_width"]

    # Hanlde overwrite sources
    assert type(config_in["overwrite_sources"]) == list
    config_out["overwrite_sources"] = config_in["overwrite_sources"]

    # Handle jump sources
    assert type(config_in["jump_drivers"]) == list
    config_out["jump_drivers"] = config_in["jump_drivers"]

    return config_out

import zlib

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "PC"

        generated_name += "_%ir"%2**config["PC_width"]

        if config["stallable"]:
            generated_name += "_stall"

        generated_name += "_%iO"%(config["overwrite_sources"], )

        generated_name += "_%iJ"%(config["jump_sources"], )

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
            "hardcoded_init": None,
            "has_enable": False,
            "clocked"   : True,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "running_FF : entity work.%s(arch)@>\n"%(RSFF_name, )
    com_det.arch_body += "generic map ( stating_state => '0')\n"
    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "S => kickoff and not program_end_reached,\n"
    com_det.arch_body += "R =>program_end_reached,\n"
    com_det.arch_body += "Q => running_internal\n"
    com_det.arch_body += "@<);\n@<\n"

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
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "value_reg : entity work.%s(arch)@>\n"%(reg_name, )
    com_det.arch_body += "generic map (@>\n"
    com_det.arch_body += "data_width => %i,\n"%(gen_det.config["PC_width"], )
    com_det.arch_body += "force_value => 0\n"
    com_det.arch_body += "@<)\n"

    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "force => program_end_reached,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "enable  => running_internal and not stall_in,\n"
    else:
        com_det.arch_body += "enable  => running_internal,\n"

    com_det.arch_head += "signal curr_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

    com_det.arch_body += "data_in  => next_value,\n"
    com_det.arch_body += "data_out => curr_value\n"
    com_det.arch_body += "@<);\n@<\n"

    com_det.add_port("value", "std_logic_vector", "out", gen_det.config["PC_width"])
    com_det.arch_body += "value <= curr_value;\n\n"

def gen_end_checking(gen_det, com_det):
    com_det.add_generic("end_value", "integer")

    _, cmp = cmp_const.generate_HDL(
        {
            "width" : gen_det.config["PC_width"]
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_head += "signal end_value_found : std_logic;\n"

    com_det.arch_body += "end_value_check : entity work.%s(arch)@>\n"%(cmp, )
    com_det.arch_body += "generic map (const => end_value)\n"

    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "value_in => curr_value,\n"
    com_det.arch_body += "match => end_value_found\n"
    com_det.arch_body += "@<);\n@<\n"


    com_det.arch_head += "signal program_end_reached : std_logic;\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "program_end_reached <= end_value_found and not stall_in;\n"
    else:
        com_det.arch_body += "program_end_reached <= end_value_found;\n"

def gen_next_value_logic(gen_det, com_det):
    com_det.arch_head += "signal next_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )
    value_tail = "next_value"

    _, mux_2 = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    for overwrite in range(len(gen_det.config["overwrite_sources"])):
        com_det.add_port("overwrite_source_%i_enable"%(overwrite, ), "std_logic", "in")
        com_det.add_port("overwrite_source_%i_value"%(overwrite, ), "std_logic_vector", "in", gen_det.config["PC_width"])

        com_det.arch_body += "overwrite_mux_%i : entity work.%s(arch)@>\n"%(overwrite, mux_2, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["PC_width"], )

        com_det.arch_body += "port map (\n@>"
        com_det.arch_body += "sel(0) => overwrite_source_%i_enable,\n"%(overwrite, )


        com_det.arch_head += "signal overwrite_tail_value_%i : std_logic_vector(%i downto 0);\n"%(overwrite, gen_det.config["PC_width"] - 1, )

        com_det.arch_body += "data_in_0 => overwrite_tail_value_%i,\n"%(overwrite, )
        com_det.arch_body += "data_in_1 => overwrite_source_%i_value,\n"%(overwrite, )

        com_det.arch_body += "data_out  => %s\n"%(value_tail, )
        value_tail = "overwrite_tail_value_%i"%(overwrite, )

        com_det.arch_body += "@<);\n@<\n"

    if gen_det.config["jump_drivers"]:
        com_det.add_port("jump_value", "std_logic_vector", "in", gen_det.config["PC_width"])

        com_det.arch_head += "signal jump_taken : std_logic;\n"

        com_det.arch_body += "jump_taken <= "
        for driver in range(len(gen_det.config["jump_drivers"])):
            com_det.add_port("jump_driver_%i"%(driver, ), "std_logic", "in")
            com_det.arch_body += "jump_driver_%i or "%(driver, )
        com_det.arch_body.drop_last(3)
        com_det.arch_body += ";\n"

        com_det.arch_body += "jump_mux : entity work.%s(arch)@>\n"%(mux_2, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["PC_width"], )

        com_det.arch_body += "port map (\n@>"
        com_det.arch_body += "sel(0) => jump_taken,\n"

        com_det.arch_head += "signal non_jump_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

        com_det.arch_body += "data_in_0 => non_jump_value,\n"
        com_det.arch_body += "data_in_1 => jump_value,\n"

        com_det.arch_body += "data_out  => %s\n"%(value_tail, )
        value_tail = "non_jump_value"

        com_det.arch_body += "@<);\n@<\n"


    com_det.arch_head += "signal inc_value : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

    _, inc = add_const.generate_HDL(
        {
            "width" : gen_det.config["PC_width"]
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "value_inc : entity work.%s(arch)@>\n"%(inc, )
    com_det.arch_body += "generic map (const => 1)\n"

    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "value_in => curr_value,\n"
    com_det.arch_body += "value_out => inc_value\n"
    com_det.arch_body += "@<);\n@<\n"

    com_det.arch_body += " %s <= inc_value;\n\n"%(value_tail, )
