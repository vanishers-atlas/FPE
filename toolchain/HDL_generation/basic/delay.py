# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["width"] >= 1)
    config_out["width"] = config_in["width"]

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]


    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "delay"

        generated_name += "_%iw"%(config["width"])

        generated_name += "_%id"%(config["depth"])

        if config["stallable"]:
            generated_name += "_stall"
        else:
            generated_name += "_nostall"

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name, concat_naming=False, force_generation=False):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = preprocess_config(config)
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, CONFIG)
    CONCAT_NAMING = concat_naming
    FORCE_GENERATION = force_generation

    # Load return variables from pre-existing file if allowed and can
    try:
        return gen_utils.load_files(FORCE_GENERATION, OUTPUT_PATH, MODULE_NAME)
    except gen_utils.FilesInvalid:
        # Generate new file
        global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

        # Init generation and return varables
        IMPORTS   = []
        ARCH_HEAD = gen_utils.indented_string()
        ARCH_BODY = gen_utils.indented_string()
        INTERFACE = { "ports" : [], "generics" : [] }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            },
            {
                "name" : "data_in",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1,),
                "direction" : "in"
            },
            {
                "name" : "data_out",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1,),
                "direction" : "out"
            }
        ]
        if CONFIG["stallable"]:
            INTERFACE["ports"] += [
                {
                    "name" : "stall",
                    "type" : "std_logic",
                    "direction" : "in"
                },
            ]

        # Delay of depth 0, is a wire
        if CONFIG["depth"] == 0:
            ARCH_BODY += "data_out <= data_in;\n"
        # Delay of depth 1, is a registor
        elif CONFIG["depth"] == 1:
            reg_interface, reg_name = register.generate_HDL(
                {
                    "has_async_force"  : False,
                    "has_sync_force"   : False,
                    "has_enable"    : CONFIG["stallable"],
                    "force_on_init" : False
                },
                OUTPUT_PATH,
                module_name=None,
                concat_naming=False,
                force_generation=FORCE_GENERATION
            )

            ARCH_BODY += "delay_reg : entity work.%s(arch)\>\n"%(reg_name)
            ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["width"])
            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            if CONFIG["stallable"]:
                ARCH_BODY += "enable => not stall,\n"
            ARCH_BODY += "data_in  => data_in,\n"
            ARCH_BODY += "data_out => data_out\n"
            ARCH_BODY += "\<);\n\<"
        # Delay of depth 2+. is a shift reg
        else:
            ARCH_HEAD += "type data_array is array(%i downto 0) of std_logic_vector(%i downto 0);\n"%(CONFIG["depth"] - 1, CONFIG["width"] - 1)
            ARCH_HEAD += "signal data : data_array;\n"

            ARCH_BODY += "process (clock)\>\n"
            ARCH_BODY += "\<begin\>\n"

            ARCH_BODY += "if rising_edge(clock) then\>\n"

            if CONFIG["stallable"]:
                ARCH_BODY += "if stall /= '1' then\>\n"

            ARCH_BODY += "data(data'left - 1 downto 0) <= data(data'left downto 1);\n"
            ARCH_BODY += "data(data'left) <= data_in;\n"

            if CONFIG["stallable"]:
                ARCH_BODY += "\<end if;\n"

            ARCH_BODY += "\<end if;\n"

            ARCH_BODY += "\<end process;\n"

            ARCH_BODY += "data_out <= data(0);\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
