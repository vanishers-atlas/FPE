from ..  import utils as gen_utils
from ... import utils as tc_utils

def generate_HDL(config, output_path, module_name, append_hash=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = gen_utils.handle_module_name(module_name, config, append_hash)
    APPEND_HASH = append_hash
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
