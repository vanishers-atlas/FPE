# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

def generate_HDL(config, output_path, module_name, generate_name=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, generate_name, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = gen_utils.handle_module_name(module_name, config, generate_name)
    generate_name = generate_name
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
            "ports" : [],
            "generics" : []
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        example()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def example():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, generate_name, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Example generic
    INTERFACE["generics"] += [
        {
            "name" : "data_width",
            "type" : "integer",
        }
    ]

    # Example port
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]
