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
from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import RS_FF_latch as RS


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(type(config_in["inputs"]) == int)
    assert(config_in["inputs"] >= 1)
    config_out["inputs"] = config_in["inputs"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "piso_sequencer_shift_based"

        generated_name += "_%i"%(config["inputs"], )

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
        com_det.add_port("clock", "std_logic", "in")
        com_det.add_generic("data_width", "integer")
        generate_input_regs(gen_det, com_det)
        generate_control_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_input_regs(gen_det, com_det):

    com_det.add_port("inputs_write", "std_logic", "in")
    com_det.add_port("data_out", "std_logic_vector(data_width - 1 downto 0)", "out")

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"   : True,
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    mux_interface, mux_name = mux.generate_HDL(
        {
            "inputs" : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_head += "signal reg_muxes_sel : std_logic_vector(0 downto 0);\n"
    com_det.arch_head += "signal reg_enable : std_logic;\n"
    for input in range(gen_det.config["inputs"]):
        com_det.arch_head += "signal reg_%i_in, reg_%i_out : std_logic_vector(data_width - 1 downto 0);\n"%(input, input, )
        com_det.add_port("data_in_%i"%(input, ), "std_logic_vector(data_width - 1 downto 0)", "in")

        com_det.arch_body += "reg_%i : entity work.%s(arch)@>\n"%(input, reg_name)

        com_det.arch_body += "generic map (data_width => data_width)\n"

        com_det.arch_body += "port map (\n@>"
        com_det.arch_body += "clock => clock,\n"
        com_det.arch_body += "enable => reg_enable,\n"
        com_det.arch_body += "data_in  => reg_%i_in,\n"%(input, )
        com_det.arch_body += "data_out => reg_%i_out\n"%(input, )
        com_det.arch_body += "@<);\n@<\n"

        if input != gen_det.config["inputs"] - 1:
            com_det.arch_body += "reg_%i_mux : entity work.%s(arch)@>\n"%(input, mux_name, )

            com_det.arch_body += "generic map (data_width => data_width)\n"

            com_det.arch_body += "port map (\n@>"
            com_det.arch_body += "sel => reg_muxes_sel,\n"
            com_det.arch_body += "data_in_0  => data_in_%i,\n"%(input, )
            com_det.arch_body += "data_in_1  => reg_%i_out,\n"%(input + 1, )
            com_det.arch_body += "data_out => reg_%i_in\n"%(input, )
            com_det.arch_body += "@<);\n@<\n"
        else:
            com_det.arch_body += "reg_%i_in <= data_in_%i;\n"%(input, input, )


    com_det.arch_body += "data_out <= reg_0_out;\n"


def generate_control_logic(gen_det, com_det):

    RS_interface, RS_name = RS.generate_HDL(
        {
            "hardcoded_init" : None,
            "has_enable" : False,
            "clocked"   : True
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_head += "signal state_R : std_logic;\n"
    com_det.arch_head += "signal state_Q : std_logic;\n"

    com_det.arch_body += "state_RS : entity work.%s(arch)@>\n"%(RS_name, )

    com_det.arch_body += "generic map (stating_state => '0')\n"

    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "S => inputs_write,\n"
    com_det.arch_body += "R => state_R,\n"
    com_det.arch_body += "Q => state_Q\n"
    com_det.arch_body += "@<);\n@<\n"

    com_det.add_port("output_write", "std_logic", "out")
    com_det.arch_body += "output_write <= state_Q;\n"

    com_det.arch_body += "reg_muxes_sel(0) <= state_Q;\n"
    com_det.arch_body += "reg_enable <= state_Q or inputs_write;\n"


    com_det.add_import("UNISIM", "vcomponents", "all")
    assert gen_det.config["inputs"] <= 32
    com_det.arch_body += "reset_delay : SRLC32E\n@>"
    com_det.arch_body += "generic map (INIT => X\"00000001\")\n"
    com_det.arch_body += "port map (@>\n"

    com_det.arch_body += "A => \"%s\",\n"%(tc_utils.unsigned.encode(gen_det.config["inputs"] - 1, 5), )
    com_det.arch_body += "D => state_R,\n"
    com_det.arch_body += "Q => state_R,\n"
    com_det.arch_body += "CLK => clock,\n"
    com_det.arch_body += "CE => state_Q,\n"
    com_det.arch_body += "Q31 => open\n"
    com_det.arch_body += "@<);\n@<\n"
