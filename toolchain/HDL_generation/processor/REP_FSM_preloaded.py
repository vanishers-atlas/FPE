# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import math

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import delay
from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import dist_ROM

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    raise NotImplementedError()

    return config

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    raise NotImplementedError()

    return dataMesh

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    raise NotImplementedError()

    return controls

#####################################################################

def preprocess_config(config_in):
    if "PREPROCESSED" in config_in.keys() and config_in["PREPROCESSED"] == True:
        if __debug__:
            assert "stallable" in config_in
            assert type(config_in["stallable"]) == bool

            assert "stall_on_id_change" in config_in
            assert type(config_in["stall_on_id_change"]) == str
            assert config_in["stall_on_id_change"] in ["NEVER", "ALWAYS", "CONDITIONALLY", ]

            assert "num_states" in config_in
            assert type(config_in["num_states"]) == int
            assert config_in["num_states"] > 0

            assert "loop_id_width" in config_in
            assert type(config_in["loop_id_width"]) == int
            assert config_in["loop_id_width"] > 0

            assert config_in["loop_id_width"] == tc_utils.unsigned.width(config_in["num_states"] - 1)
        return config_in
    else:
        config_out = {}

        assert "stallable" in config_in
        assert type(config_in["stallable"]) == bool
        config_out["stallable"] = config_in["stallable"]

        assert "stall_on_id_change" in config_in
        assert type(config_in["stall_on_id_change"]) == str
        assert config_in["stall_on_id_change"] in ["NEVER", "ALWAYS", "CONDITIONALLY", ]
        config_out["stall_on_id_change"] = config_in["stall_on_id_change"]

        assert "loops" in config_in
        assert type(config_in["loops"]) == list
        config_out["num_states"] = len(config_in["loops"])

        config_out["loop_id_width"] = tc_utils.unsigned.width(config_out["num_states"] - 1)

        config_out["PREPROCESSED"] = True

        return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "REP_FSM_preloaded"

        # Handle PC_wdith
        generated_name += "_%is"%(config["num_states"], )

        # Mark if stallable
        if config["stallable"]:
            generated_name += "_stallable"

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
        gen_common_ports(gen_det, com_det)
        gen_loop_id_reg(gen_det, com_det)
        gen_update_ROM(gen_det, com_det)
        gen_loop_id_delay(gen_det, com_det)
        gen_stall_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_common_ports(gen_det, com_det):
    com_det.add_port("clock", "std_logic", "in")

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")

    com_det.add_port("end_found", "std_logic", "in")
    com_det.add_port("last_iteration", "std_logic", "in")

def gen_loop_id_reg(gen_det, com_det):

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : True
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "loop_id_reg : entity work.%s(arch)@>\n"%(reg_name, )

    com_det.arch_body += "generic map (@>\n"
    com_det.arch_body += "data_width => %i,\n"%(gen_det.config["loop_id_width"], )
    com_det.add_generic("starting_loop_id", "integer",)
    com_det.arch_body += "force_value => starting_loop_id\n"
    com_det.arch_body += "@<)\n"

    com_det.arch_body += "port map (\n@>"

    com_det.arch_body += "clock => clock,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "enable  => end_found and not stall_in,\n"
    else:
        com_det.arch_body += "enable  => end_found,\n"

    com_det.arch_body += "data_in  => next_loop_id,\n"
    com_det.arch_head += "signal curr_loop_id : std_logic_vector(%i downto 0);\n"%(gen_det.config["loop_id_width"]  - 1, )
    com_det.arch_body += "data_out => curr_loop_id\n"

    com_det.arch_body += "@<);\n@<"

    com_det.arch_body += "\n"

    com_det.add_port("loop_id", "std_logic_vector", "out", gen_det.config["loop_id_width"])
    com_det.arch_body += "loop_id  <= curr_loop_id;\n"

def gen_update_ROM(gen_det, com_det):
    if gen_det.config["stall_on_id_change"] == "CONDITIONALLY":
        rom_width = gen_det.config["loop_id_width"] + 1
    else:
        rom_width = gen_det.config["loop_id_width"]

    rom_interface, rom_name = dist_ROM.generate_HDL(
        {
            "depth" : 2*gen_det.config["num_states"],
            "width" : rom_width,
            "reads" : 1,
            "synchronous" : False,
            "has_enable" : False,
            "init_type" : "GENERIC_STD"
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("preloaded_loop_id_encoding",
        {
            "type"  : "unsigned",
            "width" : gen_det.config["loop_id_width"]
        }
    )

    # Instancate ROM
    com_det.arch_body += "next_loop_id_ROM : entity work.%s(arch)@>\n"%(rom_name, )

    com_det.arch_body += "generic map (\n@>"
    if gen_det.config["stall_on_id_change"] == "CONDITIONALLY":
        for index in range(0, 2*gen_det.config["num_states"], 2):
            loop_id = math.floor(index/2)
            com_det.add_generic("loop_%i_on_overwrite"%(loop_id, ), "std_logic_vector", gen_det.config["loop_id_width"])
            com_det.add_generic("loop_%i_on_overwrite_stall"%(loop_id, ), "std_logic")
            com_det.arch_body += "init_%i => loop_%i_on_overwrite & loop_%i_on_overwrite_stall,\n"%(index, loop_id, loop_id, )
            com_det.add_generic("loop_%i_on_fallthrough"%(loop_id, ), "std_logic_vector", gen_det.config["loop_id_width"])
            com_det.add_generic("loop_%i_on_fallthrough_stall"%(loop_id, ), "std_logic")
            com_det.arch_body += "init_%i => loop_%i_on_fallthrough & loop_%i_on_fallthrough_stall,\n"%(index + 1, loop_id, loop_id, )
    else:
        for index in range(0, 2*gen_det.config["num_states"], 2):
            loop_id = math.floor(index/2)
            com_det.add_generic("loop_%i_on_overwrite"%(loop_id, ), "std_logic_vector", gen_det.config["loop_id_width"])
            com_det.arch_body += "init_%i => loop_%i_on_overwrite,\n"%(index, loop_id, )
            com_det.add_generic("loop_%i_on_fallthrough"%(loop_id, ), "std_logic_vector", gen_det.config["loop_id_width"])
            com_det.arch_body += "init_%i => loop_%i_on_fallthrough,\n"%(index + 1, loop_id, )
    for index in range(2*gen_det.config["num_states"], 2**rom_interface["addr_width"]):
        com_det.arch_body += "init_%i => (others => '0'),\n"%(index, )
    com_det.arch_body.drop_last(2)
    com_det.arch_body += "\n@<)\n"

    com_det.arch_body += "port map (\n@>"
    com_det.arch_body += "read_0_addr => curr_loop_id & last_iteration,\n"
    com_det.arch_head += "signal rom_data : std_logic_vector(%i downto 0);\n"%(rom_width - 1, )
    com_det.arch_body += "read_0_data => rom_data\n"

    com_det.arch_body += "@<);\n@<\n"

    com_det.arch_head += "signal next_loop_id : std_logic_vector(%i downto 0);\n"%(gen_det.config["loop_id_width"]  - 1, )
    if gen_det.config["stall_on_id_change"] == "CONDITIONALLY":
        com_det.arch_body += "next_loop_id <= rom_data(%i downto 1);\n"%(rom_width - 1, )

        com_det.arch_head += "signal stall_required : std_logic;\n"
        com_det.arch_body += "stall_required <= rom_data(0);\n"
    else:
        com_det.arch_body += "next_loop_id <= rom_data;\n"

def gen_loop_id_delay(gen_det, com_det):
    interface, name = delay.generate_HDL(
        {
            "width" : gen_det.config["loop_id_width"],
            "depth" : 1,
            "has_enable" : gen_det.config["stallable"],
            "inited" : True,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )


    com_det.arch_body += "loop_id_delay : entity work.%s(arch)@>\n"%(name, )

    com_det.arch_body += "generic map (init_value => starting_loop_id)\n"

    com_det.arch_body += "port map (\n@>"

    com_det.arch_body += "clock => clock,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall_in,\n"

    com_det.arch_body += "data_in  => curr_loop_id,\n"
    com_det.arch_head += "signal loop_id_delay_out : std_logic_vector(%i downto 0);\n"%(gen_det.config["loop_id_width"]  - 1, )
    com_det.arch_body += "data_out => loop_id_delay_out\n"

    com_det.arch_body += "@<);@<\n\n"

    com_det.add_port("loop_id_delayed", "std_logic_vector", "out", gen_det.config["loop_id_width"])
    com_det.arch_body += "loop_id_delayed <= loop_id_delay_out;\n\n"


def gen_stall_logic(gen_det, com_det):
    if   gen_det.config["stall_on_id_change"] == "NEVER":
        pass
    elif gen_det.config["stall_on_id_change"] == "ALWAYS":
        com_det.add_port("stall_out", "std_logic", "out")
        com_det.arch_body += "stall_out <= '1' when curr_loop_id /= loop_id_delay_out else '0';\n"
    elif gen_det.config["stall_on_id_change"] == "CONDITIONALLY":
        com_det.add_port("stall_out", "std_logic", "out")
        com_det.arch_body += "stall_out <= stall_required when curr_loop_id /= loop_id_delay_out else '0';\n"
