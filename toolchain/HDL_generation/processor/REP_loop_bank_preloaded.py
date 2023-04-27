# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import dist_ROM

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
    if "PREPROCESSED" in config_in.keys() and config_in["PREPROCESSED"] == True:
        if __debug__:
            assert "PC_width" in config_in
            assert type(config_in["PC_width"]) == int
            assert config_in["PC_width"] > 0

            assert "stallable" in config_in
            assert type(config_in["stallable"]) == bool

            assert "depth" in config_in
            assert type(config_in["depth"]) == int
            assert config_in["depth"] > 0
        return config_in
    else:
        config_out = {}

        assert "PC_width" in config_in
        assert type(config_in["PC_width"]) == int
        assert config_in["PC_width"] > 0
        config_out["PC_width"] = config_in["PC_width"]

        assert "stallable" in config_in
        assert type(config_in["stallable"]) == bool
        config_out["stallable"] = config_in["stallable"]

        assert "loops" in config_in
        assert type(config_in["loops"]) == list
        config_out["depth"] = len(config_in["loops"])

        config_out["PREPROCESSED"] = True

        return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "REP_loop_bank_preloaded"

        # Handle PC_wdith
        generated_name += "_%iw"%(config["PC_width"], )

        # Handle bank depth
        generated_name += "_%id"%(config["depth"], )

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
        gen_preloaded_ROM(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_common_ports(gen_det, com_det):
    com_det.add_port("clock", "std_logic", "in")

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")


def gen_preloaded_ROM(gen_det, com_det):

    rom_interface, rom_name = dist_ROM.generate_HDL(
        {
            "depth" : gen_det.config["depth"],
            "width" : 2*gen_det.config["PC_width"],
            "reads" : 1,
            "synchronous" : True,
            "has_enable" : gen_det.config["stallable"],
            "init_type" : "GENERIC_STD"
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("preloaded_pc_values_encoding",
        {
            "type"  : "unsigned",
            "width" : gen_det.config["PC_width"]
        }
    )

    # Instancate ROM
    com_det.arch_body += "loop_ROM : entity work.%s(arch)\>\n"%(rom_name, )

    com_det.arch_body += "generic map (\n\>"
    for loop_id in range(gen_det.config["depth"]):
        com_det.add_generic("loop_%i_start_value"%(loop_id, ), "std_logic_vector", gen_det.config["PC_width"])
        com_det.add_generic("loop_%i_end_value"%(loop_id, ), "std_logic_vector", gen_det.config["PC_width"])
        com_det.arch_body += "init_%i => loop_%i_start_value & loop_%i_end_value,\n"%(loop_id, loop_id, loop_id, )
    for loop_id in range(gen_det.config["depth"], 2**rom_interface["addr_width"]):
        com_det.arch_body += "init_%i => (others => '0'),\n"%(loop_id, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<)\n"

    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "clock => clock,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "read_enable => not stall_in,\n"

    com_det.add_interface_item("addr_width", rom_interface["addr_width"])
    com_det.add_port("loop_id", "std_logic_vector", "in", rom_interface["addr_width"])
    com_det.arch_body += "read_0_addr => loop_id,\n"
    com_det.arch_head += "signal loop_data : std_logic_vector(%i downto 0);\n"%(2*gen_det.config["PC_width"]  - 1, )
    com_det.arch_body += "read_0_data => loop_data\n"

    com_det.arch_body += "\<);\n\<\n"

    com_det.add_port("loop_start", "std_logic_vector", "out", gen_det.config["PC_width"])
    com_det.add_port("loop_end", "std_logic_vector", "out", gen_det.config["PC_width"])
    com_det.arch_body += "loop_start <= loop_data(%i downto %i);\n"%(2*gen_det.config["PC_width"]-1, 1*gen_det.config["PC_width"], )
    com_det.arch_body += "loop_end   <= loop_data(%i downto %i);\n"%(1*gen_det.config["PC_width"]-1, 0*gen_det.config["PC_width"], )
