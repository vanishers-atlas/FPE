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

    assert(config_in["async_forces"] >= 0 )
    config_out["async_forces"] = config_in["async_forces"]

    assert(config_in["sync_forces"] >= 0 )
    config_out["sync_forces"] = config_in["sync_forces"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "register"

        # Handle enable
        if config["has_enable"] == True:
            generated_name += "_e"

        # Handle forces
        generated_name += "_%ia_%is"%(config["async_forces"], config["sync_forces"])

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
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

        # Declare common ports and generics
        INTERFACE["generics"] += [
            {
                "name" : "data_width",
                "type" : "integer",
            }
        ]

        INTERFACE["ports"] += [
            {
                "name" : "trigger",
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

        # Generate process start
        ARCH_BODY += "process (trigger"
        if CONFIG["async_forces"] != 0:
            asyn_sel = tc_utils.unsigned.width(CONFIG["async_forces"])

            INTERFACE["ports"] += [
                {
                    "name" : "asyn_reset_sel",
                    "type" : "std_logic_vector(%i downto 0)"%(asyn_sel - 1),
                    "direction" : "in"
                }
            ]

            ARCH_BODY += ", asyn_reset_sel"

        ARCH_BODY += ")\nbegin\n\>"

        # Handle asynchronous forces
        if CONFIG["async_forces"] != 0:
            if not any([
                imp["library"] == "ieee" and imp["package"] == "numeric_std" and imp["parts"] == "all"
                for imp in IMPORTS
            ]):
                IMPORTS += [ {"library" : "ieee", "package" : "numeric_std", "parts" : "all"} ]

            for i in range(CONFIG["async_forces"]):
                INTERFACE["generics"] += [
                    {
                        "name" : "asyn_%i_value"%(i),
                        "type" : "integer",
                    }
                ]

                ARCH_BODY += "if asyn_reset_sel = \"%s\" then\n\>"%(tc_utils.unsigned.encode(i + 1, asyn_sel))
                ARCH_BODY += "data_out <= std_logic_vector(to_unsigned(asyn_%i_value, data_out'length));\n"%(i)
                ARCH_BODY += "\<els"

        # Handle synchronous check
        ARCH_BODY += "if rising_edge(trigger) then\n\>"

        # Handle synchronous forces
        if CONFIG["sync_forces"] != 0:
            syn_sel = tc_utils.unsigned.width(CONFIG["sync_forces"])

            INTERFACE["ports"] += [
                {
                    "name" : "syn_reset_sel",
                    "type" : "std_logic_vector(%i downto 0)"%(syn_sel - 1),
                    "direction" : "in"
                }
            ]

            if not any([
                imp["library"] == "ieee" and imp["package"] == "numeric_std" and imp["parts"] == "all"
                for imp in IMPORTS
            ]):
                IMPORTS += [ {"library" : "ieee", "package" : "numeric_std", "parts" : "all"} ]

            for i in range(CONFIG["sync_forces"]):
                INTERFACE["generics"] += [
                    {
                        "name" : "syn_%i_value"%(i),
                        "type" : "integer",
                    }
                ]

                ARCH_BODY += "if syn_reset_sel = \"%s\" then\n\>"%(tc_utils.unsigned.encode(i + 1, syn_sel))
                ARCH_BODY += "data_out <= std_logic_vector(to_unsigned(syn_%i_value, data_out'length));\n"%(i)
                ARCH_BODY += "\<els"

        # Handle enable
        if CONFIG["has_enable"]:
            INTERFACE["ports"] += [
                {
                    "name" : "enable",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]
            ARCH_BODY += "if enable = '1' then\n\>"

        # Preform read and store
        ARCH_BODY += "data_out <= data_in;\n"

        # Close enable if
        if CONFIG["has_enable"]:
            ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end if;\n"
        ARCH_BODY += "\<end process;\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
