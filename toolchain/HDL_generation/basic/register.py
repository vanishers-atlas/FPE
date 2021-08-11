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

    assert(type(config_in["has_enable"]) == type(True))
    config_out["has_enable"] = config_in["has_enable"]

    assert(type(config_in["has_async_force"]) == type(True))
    assert(type(config_in["has_sync_force"]) == type(True))

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

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "register"

        # Handle enable
        if config["has_enable"] == True:
            generated_name += "_e"

        # Handle force
        if   config["force_type"] == "NONE":
            generated_name += "_n"
        elif config["force_type"] == "SYNC":
            generated_name += "_s"
        elif config["force_type"] == "ASYNC":
            generated_name += "_a"

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name, generate_name=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = preprocess_config(config)
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, CONFIG, generate_name)
    GENERATE_NAME = generate_name
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

        # Declare common ports and generics
        INTERFACE["generics"] += [
            {
                "name" : "data_width",
                "type" : "integer",
            }
        ]
        if CONFIG["force_type"] != "NONE":
            IMPORTS += [
                {
                    "library" : "ieee",
                    "package" : "numeric_std",
                    "parts" : "all"
                }
            ]

            INTERFACE["generics"] += [
                {
                    "name" : "force_value",
                    "type" : "integer",
                }
            ]

        INTERFACE["ports"] += [
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

        # Generate process start
        if CONFIG["force_type"] == "ASYNC":
            ARCH_BODY += "process (clock, force)\>\n"
        else:
            ARCH_BODY += "process (clock)\>\n"
        ARCH_BODY += "\<begin\n\>"

        # Handle ASYNC force
        if CONFIG["force_type"] == "ASYNC":
            ARCH_BODY += "if force = '1' then\n\>"
            ARCH_BODY += "data_out <= std_logic_vector(to_unsigned(force_value, data_out'length));\n"
            ARCH_BODY += "\<els"

        ARCH_BODY += "if rising_edge(clock) then\n\>"

        # Handle SYNC force
        if CONFIG["force_type"] == "SYNC":
            ARCH_BODY += "if force = '1' then\n\>"
            ARCH_BODY += "data_out <= std_logic_vector(to_unsigned(force_value, data_out'length));\n"

            if CONFIG["has_enable"]:
                ARCH_BODY += "\<els"
            else:
                ARCH_BODY += "\<else\>\n"

        # Handle enable
        if CONFIG["has_enable"]:
            ARCH_BODY += "if enable = '1' then\n\>"

        # Handle registoring the input value
        ARCH_BODY += "data_out <= data_in;\n"

        # Close extra if
        if CONFIG["force_type"] == "ASYNC" or CONFIG["has_enable"]:
            ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end if;\n"
        ARCH_BODY += "\<end process;\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
