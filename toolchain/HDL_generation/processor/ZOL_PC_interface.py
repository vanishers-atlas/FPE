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

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    if config["seekable"]:
        for instr in instr_set:
            if instr_id in asm_utils.instr_exe_units(instr):
                mnemonic = asm_utils.instr_mnemonic(instr)
                if   mnemonic == "ZOL_SEEK":
                    gen_utils.add_datapath_dest(pathways, "%sfetch_data_0_word_0"%(lane, ), "exe", instr, instr_prefix + "seek_overwrite_value", "unsigned", interface["ports"]["seek_overwrite_value"]["width"])
                    gen_utils.add_datapath_dest(pathways, "%sfetch_data_1_word_0"%(lane, ), "exe", instr, instr_prefix + "seek_check_value", "unsigned", interface["ports"]["seek_check_value"]["width"])

    return pathways

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
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, config)
    CONCAT_NAMING = concat_naming
    FORCE_GENERATION = force_generation

    # Load return variables from pre-exiting file if allowed and can
    try:
        return gen_utils.load_files(FORCE_GENERATION, OUTPUT_PATH, MODULE_NAME)
    except gen_utils.FilesInvalid:
        # Generate new file
        global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

        # Init generation and return varables
        IMPORTS   = []
        ARCH_HEAD = gen_utils.indented_string()
        ARCH_BODY = gen_utils.indented_string()
        INTERFACE = {
            "ports" : { },
            "generics" : { },
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Include stall port if needed
        if CONFIG["stallable"]:
            INTERFACE["ports"]["stall"] = {
                "type" : "std_logic",
                "direction" : "in"
            }


        # Generation Module Code
        generate_check_and_overwrite_values()
        generate_PC_check_handling()
        generate_overwrite_handling()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_check_and_overwrite_values():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Declare internal check and overwrite values
    ARCH_HEAD += "signal check_value_int : std_logic_vector(%i downto 0);\n"%(CONFIG["PC_width"] - 1, )
    ARCH_HEAD += "signal overwrite_value_int : std_logic_vector(%i downto 0);\n"%(CONFIG["PC_width"] - 1, )

    if not CONFIG["seekable"]:
        # ZOL is not seekable ie check/overwrite values are fixed, therefore use generics
        INTERFACE["generics"]["check_value"] = {
            "type" : "integer",
        }
        INTERFACE["generics"]["overwrite_value"] = {
            "type" : "integer",
        }


        # Import to_unsigned funtions
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts" : "all"
            }
        ]

        ARCH_BODY += "-- Convert generics to std_logic_vectors\n"
        ARCH_BODY += "check_value_int <=  std_logic_vector(to_unsigned(check_value, %i));\n"%(CONFIG["PC_width"], )
        ARCH_BODY += "overwrite_value_int <=  std_logic_vector(to_unsigned(overwrite_value, %i));\n\n"%(CONFIG["PC_width"], )
    else:
        # ZOL is seekable ie check/overwrite values are variable, therefore use registors and ports

        INTERFACE["ports"]["clock"] = {
            "type" : "std_logic",
            "direction" : "in",
        }
        INTERFACE["ports"]["seek_check_value"] = {
            "type" : "std_logic_vector",
            "width": CONFIG["PC_width"],
            "direction" : "in",
        }
        INTERFACE["ports"]["seek_overwrite_value"] = {
            "type" : "std_logic_vector",
            "width": CONFIG["PC_width"],
            "direction" : "in",
        }
        INTERFACE["ports"]["seek_enable"] = {
            "type" : "std_logic",
            "direction" : "in",
        }

        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force"  : False,
                "has_sync_force"   : False,
                "has_enable"    : True,
                "force_on_init" : True
            },
            OUTPUT_PATH,
            module_name=None,
            concat_naming=False,
            force_generation=FORCE_GENERATION
        )

        ARCH_BODY += "-- Register check_value\n"

        ARCH_BODY += "check_value_reg : entity work.%s(arch)\>\n"%(reg_name, )

        ARCH_BODY += "generic map (\>\n"
        ARCH_BODY += "data_width => %i,\n"%(CONFIG["PC_width"], )
        ARCH_BODY += "force_value => %i\n"%(2**CONFIG["PC_width"] - 1, )
        ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => seek_enable,\n"
        else:
            ARCH_BODY += "enable => seek_enable and not stall,\n"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => seek_check_value,\n"
        ARCH_BODY += "data_out => check_value_int\n"

        ARCH_BODY += "\<);\n\<\n"


        ARCH_BODY += "-- Register overwrite_value\n"

        ARCH_BODY += "overwrite_value_reg : entity work.%s(arch)\>\n"%(reg_name, )

        ARCH_BODY += "generic map (\>\n"
        ARCH_BODY += "data_width => %i,\n"%(CONFIG["PC_width"], )
        ARCH_BODY += "force_value => %i\n"%(2**CONFIG["PC_width"] - 1, )
        ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => seek_enable,\n"
        else:
            ARCH_BODY += "enable => seek_enable and not stall,\n"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => seek_overwrite_value,\n"
        ARCH_BODY += "data_out => overwrite_value_int\n"

        ARCH_BODY += "\<);\n\<\n"


def generate_PC_check_handling():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Declare ports for PC checking
    INTERFACE["ports"]["PC_value"] = {
        "type" : "std_logic_vector",
        "width": CONFIG["PC_width"],
        "direction" : "in",
    }
    INTERFACE["ports"]["PC_running"] = {
        "type" : "std_logic",
        "direction" : "in",
    }
    INTERFACE["ports"]["match_found"] = {
        "type" : "std_logic",
        "direction" : "out",
    }

    ARCH_BODY += "-- Check if PC matches end Value\n"
    ARCH_HEAD += "signal PC_equality_result : std_logic;\n"
    ARCH_HEAD += "signal match_found_int : std_logic;\n"

    ARCH_BODY += "PC_equality_result <= '1' when PC_value = check_value_int else '0';\n"

    if not CONFIG["stallable"]:
        ARCH_BODY += "match_found_int <= PC_running and PC_equality_result;\n"
    else:
        ARCH_BODY += "match_found_int <= '1' when PC_running and PC_equality_result and not stall;\n"
    ARCH_BODY += "match_found <= match_found_int;\n"


def generate_overwrite_handling():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle PC_overwrite
    INTERFACE["ports"]["overwrite_PC_value"] = {
        "type" : "std_logic_vector",
        "width": CONFIG["PC_width"],
        "direction" : "out",
    }
    INTERFACE["ports"]["overwrite_PC_enable"] = {
        "type" : "std_logic",
        "direction" : "out",
    }
    INTERFACE["ports"]["overwrites_reached"] = {
        "type" : "std_logic",
        "direction" : "in",
    }

    # Handle PC overwriting
    ARCH_HEAD += "signal overwrite_int : std_logic;\n\n"

    ARCH_BODY += "-- Compute  overwriting of PC\n"
    ARCH_BODY += "overwrite_int <= match_found_int and not overwrites_reached;\n"
    ARCH_BODY += "overwrite_PC_enable <= '1' when overwrite_int = '1' else 'L';\n\n"

    ARCH_BODY += "overwrite_PC_value <= overwrite_value_int when overwrite_int = '1' else (others => 'L');\n\n"
