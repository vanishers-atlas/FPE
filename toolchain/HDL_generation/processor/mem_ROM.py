# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import dist_ROM

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "ROM"

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

        if config["stallable"]:
            generated_name += "_S"
        else:
            generated_name += "_N"


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
            },
        ]

        # Generation Module Code
        INTERFACE["generics"] += [
            {
                "name" : "init_mif",
                "type" : "string"
            }
        ]

        gen_ports()

        gen_wordwise_distributed_ROM()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle common ports
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]
    if CONFIG["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

    # Declare read ports
    for read in range(CONFIG["reads"]):
        INTERFACE["ports"] += [
            {
                "name" : "read_%i_addr"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "read_%i_data"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "out"
            }
        ]

def gen_wordwise_distributed_ROM():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONFIG["reads"] <= 3:
        # Generate a basic ROM to handle be having
        rom_interface, rom_name = dist_ROM.generate_HDL(
            {
                "depth" : CONFIG["depth"],
                "reads" : CONFIG["reads"],
                "synchronous" : True,
                "has_enable" : CONFIG["stallable"],
                "init_type" : "MIF"
            },
            OUTPUT_PATH,
            "ROM",
            True,
            False
        )

        # Instancate ROM
        ARCH_BODY += "dist_ROM : entity work.%s(arch)\>\n"%(rom_name,)

        ARCH_BODY += "generic map (\>\n"
        ARCH_BODY += "data_width => %i,\n"%(CONFIG["data_width"], )
        ARCH_BODY += "init_mif => init_mif\n"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "read_enable => not stall,\n"
        ARCH_BODY += ",\n".join([
            "read_%i_addr => read_%i_addr,\nread_%i_data => read_%i_data"%(
                read, read, read, read,
            )
            for read in range(CONFIG["reads"])
        ])
        ARCH_BODY += "\<);\n\<\n"
    else:
        raise NotIMplementedError("Support for 4+ reads does adding")
