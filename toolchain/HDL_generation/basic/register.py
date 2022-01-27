# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "has_enable" in config_in.keys(), "Passed config lacks has_enable key"
    assert type(config_in["has_enable"]) is bool, "has_enable must be a bool"
    config_out["has_enable"] = config_in["has_enable"]

    assert "force_on_init" in config_in.keys(), "Passed config lacks force_on_init key"
    assert type(config_in["force_on_init"]) is bool, "force_on_init must be a bool"
    config_out["force_on_init"] = config_in["force_on_init"]

    assert "has_async_force" in config_in.keys(), "Passed config lacks has_async_force key"
    assert type(config_in["has_async_force"]) is bool, "has_async_force must be a bool"
    config_out["has_async_force"] = config_in["has_async_force"]

    assert "has_sync_force" in config_in.keys(), "Passed config lacks has_sync_force key"
    assert type(config_in["has_sync_force"]) is bool, "has_sync_force must be a bool"
    config_out["has_sync_force"] = config_in["has_sync_force"]


    if   config_in["has_async_force"] == False and config_in["has_sync_force"] == False:
        config_out["force_type"] = "NONE"
    elif config_in["has_async_force"] == False and config_in["has_sync_force"] == True :
        config_out["force_type"] = "SYNC"
    elif config_in["has_async_force"] == True  and config_in["has_sync_force"] == False:
        config_out["force_type"] = "ASYNC"
    elif config_in["has_async_force"] == True  and config_in["has_sync_force"] == True :
        raise ValueError(" ".join([
            "Only a sync focce xor an async force is supposted, not both together.",
            "If both forces are to the same value async only will have the same affact as both together"
        ]) )

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "register"

        # Handle initing
        if config["force_on_init"] == True:
            generated_name += "_inited"

        # Handle enable
        if config["has_enable"] == True:
            generated_name += "_enable"

        # Handle "force_on_init"
        if config["force_on_init"] == True:
            generated_name += "_inited"
            
        # Handle force
        if   config["force_type"] == "NONE":
            generated_name += "_no_force"
        elif config["force_type"] == "SYNC":
            generated_name += "_sync_force"
        elif config["force_type"] == "ASYNC":
            generated_name += "_async_force"

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
        INTERFACE = {
            "generics" : [
                {
                    "name" : "data_width",
                    "type" : "integer",
                },

            ],
            "ports" : [
                {
                    "name" : "clock",
                    "type" : "std_logic",
                    "direction" : "in"
                },
                {
                    "name" : "data_in",
                    "type" : "std_logic_vector(data_width - 1 downto 0)",
                    "direction" : "in"
                },
                {
                    "name" : "data_out",
                    "type" : "std_logic_vector(data_width - 1 downto 0)",
                    "direction" : "out"
                }
            ],
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
        ]

        if CONFIG["force_type"] != "NONE" or CONFIG["force_on_init"]:
            IMPORTS += [
                {
                    "library" : "ieee",
                    "package" : "numeric_std",
                    "parts" : "all"
                },
            ]

            INTERFACE["generics"] += [
                {
                    "name" : "force_value",
                    "type" : "integer"
                },
            ]

        if CONFIG["has_enable"]:
            INTERFACE["ports"] += [
                {
                    "name" : "enable",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]

        if CONFIG["force_type"] != "NONE":
            INTERFACE["ports"] += [
                {
                    "name" : "force",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]

        # Handle initing behavour
        if CONFIG["force_on_init"]:
            ARCH_HEAD += "signal data_internal : std_logic_vector(data_width - 1 downto 0) := std_logic_vector(to_unsigned(force_value, data_width));\n"
        else:
            ARCH_HEAD += "signal data_internal : std_logic_vector(data_width - 1 downto 0) := (others => 'U');\n"


        # Generate process start
        if CONFIG["force_type"] == "ASYNC":
            ARCH_BODY += "process (clock, force)\>\n"
        else:
            ARCH_BODY += "process (clock)\>\n"
        ARCH_BODY += "\<begin\n\>"

        # Handle ASYNC force
        if CONFIG["force_type"] == "ASYNC":
            ARCH_BODY += "if force = '1' then\n\>"
            ARCH_BODY += "data_internal <= std_logic_vector(to_unsigned(force_value, data_out'length));\n"
            ARCH_BODY += "\<els"

        ARCH_BODY += "if rising_edge(clock) then\n\>"

        # Handle SYNC force
        if CONFIG["force_type"] == "SYNC":
            ARCH_BODY += "if force = '1' then\n\>"
            ARCH_BODY += "data_internal <= std_logic_vector(to_unsigned(force_value, data_out'length));\n"

            if CONFIG["has_enable"]:
                ARCH_BODY += "\<els"
            else:
                ARCH_BODY += "\<else\>\n"

        # Handle enable
        if CONFIG["has_enable"]:
            ARCH_BODY += "if enable = '1' then\n\>"

        # Handle registoring the input value
        ARCH_BODY += "data_internal <= data_in;\n"

        # Close extra if
        if CONFIG["force_type"] == "ASYNC" or CONFIG["has_enable"]:
            ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end if;\n"
        ARCH_BODY += "\<end process;\n"

        # Handle registoring the input value
        ARCH_BODY += "data_out <= data_internal;\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
