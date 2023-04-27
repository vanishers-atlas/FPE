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
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SET":
                raise ValueError("Ripple tracker doesn't support ZOL_SET instructions")
            elif mnemonic in ["ZOL_SEEK", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)

    return config


def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

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

        com_det.add_generic("overwrites", "std_logic_vector", SRL_WIDTH*gen_det.config["tallies"])

        com_det.add_port("clock", "std_logic", "in")
        com_det.add_port("match_found", "std_logic", "in")
        com_det.add_port("overwrites_reached", "std_logic", "out")

        com_det.add_interface_item("overwrites_encoding",
            {
                "type"      : "biased_tally",
                "bias"      : SRL_BAIS,
                "range"     : SRL_RANGE,
                "tallies"   : gen_det.config["tallies"]
            }
        )

        # Include required libs
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_import("UNISIM", "vcomponents", "all")

        # Generation Module Code
        generate_state_machine(gen_det, com_det)
        generate_SRLs(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_state_machine(gen_det, com_det):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_FSM"
    else:
        module_name = None

    sub_interface, sub_name = ZOL_inverted_SR_FSM.generate_HDL(
        {},
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "state_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    assert len(sub_interface["generics"]) == 0
    # com_det.arch_body += "generic map ()\n"

    assert len(sub_interface["ports"]) == 4
    assert "clock" in sub_interface["ports"].keys()
    assert "match_found" in sub_interface["ports"].keys()
    assert "not_tracking" in sub_interface["ports"].keys()
    assert "overwrites_reached" in sub_interface["ports"].keys()

    com_det.arch_body += "port map (\n\>"

    com_det.arch_head += "signal not_tracking : std_logic;\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "match_found  => match_found,\n"
    com_det.arch_body += "overwrites_reached => overwrites_reached_int,\n"
    com_det.arch_body += "not_tracking  => not_tracking\n"

    com_det.arch_body += "\<);\n\<\n"

def generate_SRLs(gen_det, com_det):
    com_det.arch_body += "-- Ripple iteration tracker\n"
    com_det.arch_head += "signal overwrites_reached_int : std_logic;\n"

    # Generate ripple chain of SRLC32Es
    for ripple in range(gen_det.config["tallies"]):
        com_det.arch_head += "signal ripple_%i_out : std_logic;\n"%(ripple, )

        com_det.arch_body += "ripple_%i : SRLC32E\n\>"%(ripple)
        com_det.arch_body += "generic map (INIT => X\"00000000\")\n"
        com_det.arch_body += "port map (\>\n"

        com_det.arch_body += "A => overwrites(%i downto %i),\n"%(5*ripple + 4, 5*ripple)

        # Handle the specail case of the first SRL
        if ripple == 0:
            com_det.arch_body += "D => not_tracking,\n"
        else:
            com_det.arch_body += "D => ripple_%i_out,\n"%(ripple - 1)

        com_det.arch_body += "Q => ripple_%i_out,\n"%(ripple)
        com_det.arch_body += "CLK => clock,\n"
        com_det.arch_body += "CE => match_found,\n"
        com_det.arch_body += "Q31 => open\n"
        com_det.arch_body += "\<);\n\<\n"

    # Connect output of final SRLC32E to overwrites_reached
    com_det.arch_body += "overwrites_reached_int <=  ripple_%i_out;\n"%(gen_det.config["tallies"] - 1)
    com_det.arch_body += "overwrites_reached <=  overwrites_reached_int;\n"
