# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["inputs"] >= 1)
    config_out["sel_width"] = tc_utils.unsigned.width(config_in["inputs"] - 1)
    config_out["inputs"] = 2**config_out["sel_width"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "mux"

        generated_name += "_%i"%(config["inputs"])

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

        # Add number of inputs into interface so other files can access it
        INTERFACE["number_inputs"] = CONFIG["inputs"]

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

        INTERFACE["ports"] += [
            {
                "name" : "sel",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["sel_width"] - 1. ),
                "direction" : "in"
            },
            *[
                {
                    "name" : "data_in_%i"%(i,),
                    "type" : "std_logic_vector(data_width - 1 downto 0)",
                    "direction" : "in"
                }
                for i in range(CONFIG["inputs"])
            ],
            {
                "name" : "data_out",
                "type" : "std_logic_vector(data_width - 1 downto 0)",
                "direction" : "out"
            }

        ]

        ARCH_BODY += "process (sel, %s)\>\n"%(
            ", ".join([ "data_in_%i"%(i,) for i in range(CONFIG["inputs"]) ])
        )
        ARCH_BODY += "\<begin\>\n"

        ARCH_BODY += "case sel is\>\n"
        for i in range(CONFIG["inputs"]):
            ARCH_BODY += "when \"%s\" =>\n\> data_out <= data_in_%i;\<\n"%(
                tc_utils.unsigned.encode(i, CONFIG["sel_width"]),
                i,
            )
        ARCH_BODY += "\<end case;\n"

        ARCH_BODY += "\<end process;\n"


        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
