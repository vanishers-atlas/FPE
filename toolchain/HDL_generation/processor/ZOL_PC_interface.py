# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SEEK":
                config["seekable"] = True
            elif mnemonic in ["ZOL_SET", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)
    return config

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    if config["seekable"]:
        for instr in instr_set:
            if instr_id in asm_utils.instr_exe_units(instr):
                mnemonic = asm_utils.instr_mnemonic(instr)
                if   mnemonic == "ZOL_SEEK":
                    dataMesh.connect_sink(sink=instr_prefix + "seek_overwrite_value",
                        channel="%sfetch_data_0_word_0"%(lane, ),
                        condition=instr,
                        stage="exe", inplace_channel=True,
                        padding_type="unsigned", width=interface["ports"]["seek_overwrite_value"]["width"]
                    )
                    dataMesh.connect_sink(sink=instr_prefix + "seek_check_value",
                        channel="%sfetch_data_1_word_0"%(lane, ),
                        condition=instr,
                        stage="exe", inplace_channel=True,
                        padding_type="unsigned", width=interface["ports"]["seek_check_value"]["width"]
                    )
    return dataMesh

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    if "seek_enable" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if asm_utils.instr_mnemonic(instr) == "ZOL_SEEK" and instr_id in asm_utils.instr_exe_units(instr):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "seek_enable", values, "std_logic")

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}


    assert "PC_width" in config_in.keys(), "Passed config lacks PC_width key"
    assert type(config_in["PC_width"]) is  int, "PC_width must in an integer"
    assert config_in["PC_width"] > 0, "PC_width mst be greater than 0"

    config_out["PC_width"] = config_in["PC_width"]


    assert "seekable" in config_in.keys(), "Passed config lacks seekable key"
    assert type(config_in["seekable"]) is bool, "seekable must be a boolean"

    config_out["seekable"] = config_in["seekable"]


    assert "stallable" in config_in.keys(), "Passed config lacks stallable key"
    assert type(config_in["stallable"]) is bool, "stallable must be a boolean"

    config_out["stallable"] = config_in["stallable"]


    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL_PC_interface"

        # Make if fixed or seekable
        if config["seekable"] :
            generated_name += "_seekable"
        else:
            generated_name += "_fixed"

        # Append PC width
        generated_name += "_%i"%(config["PC_width"], )

        # Handle stalling
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

        # Include stall port if needed
        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_head += "signal stall : std_logic;\n"
            com_det.arch_body += "stall <= stall_in;\n"


        # Generation Module Code
        generate_check_and_overwrite_values(gen_det, com_det)
        generate_PC_check_handling(gen_det, com_det)
        generate_overwrite_handling(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_check_and_overwrite_values(gen_det, com_det):
    # Declare internal check and overwrite values
    com_det.arch_head += "signal check_value_int : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )
    com_det.arch_head += "signal overwrite_value_int : std_logic_vector(%i downto 0);\n"%(gen_det.config["PC_width"] - 1, )

    if not gen_det.config["seekable"]:
        # ZOL is not seekable ie check/overwrite values are fixed, therefore use generics
        com_det.add_generic("check_value", "integer")
        com_det.add_generic("overwrite_value", "integer")

        # Import to_unsigned funtions
        com_det.add_import("ieee", "numeric_std", "all")

        com_det.arch_body += "-- Convert generics to std_logic_vectors\n"
        com_det.arch_body += "check_value_int <=  std_logic_vector(to_unsigned(check_value, %i));\n"%(gen_det.config["PC_width"], )
        com_det.arch_body += "overwrite_value_int <=  std_logic_vector(to_unsigned(overwrite_value, %i));\n\n"%(gen_det.config["PC_width"], )
    else:
        # ZOL is seekable ie check/overwrite values are variable, therefore use registors and ports

        com_det.add_port("clock", "std_logic", "in")
        com_det.add_port("seek_check_value", "std_logic_vector", "in", gen_det.config["PC_width"])
        com_det.add_port("seek_overwrite_value", "std_logic_vector", "in", gen_det.config["PC_width"])
        com_det.add_port("seek_enable", "std_logic", "in")

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

        com_det.arch_body += "-- Register check_value\n"

        com_det.arch_body += "check_value_reg : entity work.%s(arch)@>\n"%(reg_name, )

        com_det.arch_body += "generic map (@>\n"
        com_det.arch_body += "data_width => %i,\n"%(gen_det.config["PC_width"], )
        com_det.arch_body += "force_value => %i\n"%(2**gen_det.config["PC_width"] - 1, )
        com_det.arch_body += "@<\n)\n"

        com_det.arch_body += "port map (\n@>"

        if not gen_det.config["stallable"]:
            com_det.arch_body += "enable => seek_enable,\n"
        else:
            com_det.arch_body += "enable => seek_enable and not stall,\n"

        com_det.arch_body += "clock => clock,\n"
        com_det.arch_body += "data_in  => seek_check_value,\n"
        com_det.arch_body += "data_out => check_value_int\n"

        com_det.arch_body += "@<);\n@<\n"


        com_det.arch_body += "-- Register overwrite_value\n"

        com_det.arch_body += "overwrite_value_reg : entity work.%s(arch)@>\n"%(reg_name, )

        com_det.arch_body += "generic map (@>\n"
        com_det.arch_body += "data_width => %i,\n"%(gen_det.config["PC_width"], )
        com_det.arch_body += "force_value => %i\n"%(2**gen_det.config["PC_width"] - 1, )
        com_det.arch_body += "@<\n)\n"

        com_det.arch_body += "port map (\n@>"

        if not gen_det.config["stallable"]:
            com_det.arch_body += "enable => seek_enable,\n"
        else:
            com_det.arch_body += "enable => seek_enable and not stall,\n"

        com_det.arch_body += "clock => clock,\n"
        com_det.arch_body += "data_in  => seek_overwrite_value,\n"
        com_det.arch_body += "data_out => overwrite_value_int\n"

        com_det.arch_body += "@<);\n@<\n"


def generate_PC_check_handling(gen_det, com_det):
    # Declare ports for PC checking
    com_det.add_port("PC_value", "std_logic_vector", "in", gen_det.config["PC_width"])
    com_det.add_port("PC_running", "std_logic", "in")
    com_det.add_port("match_found", "std_logic", "out")

    com_det.arch_body += "-- Check if PC matches end Value\n"
    com_det.arch_head += "signal PC_equality_result : std_logic;\n"
    com_det.arch_head += "signal match_found_int : std_logic;\n"

    com_det.arch_body += "PC_equality_result <= '1' when PC_value = check_value_int else '0';\n"

    if not gen_det.config["stallable"]:
        com_det.arch_body += "match_found_int <= PC_running and PC_equality_result;\n"
    else:
        com_det.arch_body += "match_found_int <= PC_running and PC_equality_result and not stall;\n"
    com_det.arch_body += "match_found <= match_found_int;\n"


def generate_overwrite_handling(gen_det, com_det):
    # Handle PC_overwrite
    com_det.add_port("overwrite_PC_value", "std_logic_vector", "out", gen_det.config["PC_width"])
    com_det.add_port("overwrite_PC_enable", "std_logic", "out")
    com_det.add_port("overwrites_reached", "std_logic", "in")

    # Handle PC overwriting
    com_det.arch_head += "signal overwrite_int : std_logic;\n\n"

    com_det.arch_body += "-- Compute  overwriting of PC\n"
    com_det.arch_body += "overwrite_int <= match_found_int and not overwrites_reached;\n"
    com_det.arch_body += "overwrite_PC_enable <= overwrite_int;\n\n"

    com_det.arch_body += "overwrite_PC_value <= overwrite_value_int;\n\n"
