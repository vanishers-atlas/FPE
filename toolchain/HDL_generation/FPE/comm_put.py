# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Stalling parameters
    assert(type(config_in["can_stall"]) == type(True))
    assert(type(config_in["stallable"]) == type(True))
    if config_in["can_stall"] == True:
        config_out["stalling"] = "ACTIVE"
    elif config_in["stallable"] == True:
        config_out["stalling"] = "PASSIVE"
    else:
        config_out["stalling"] = "NONE"

    # Data pori parameters
    assert(config_in["writes"] >= 1)
    config_out["writes"] = config_in["writes"]
    assert(config_in["FIFOs"] >= 1)
    config_out["FIFOs"] = config_in["FIFOs"]

    # Datapath parametes
    assert(config_in["data_width"] >= 0)
    config_out["data_width"] = config_in["data_width"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_out["FIFOs"] - 1)

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "PUT"

        # Denote Data width, writes, and FIFOs parameters
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%if"%(config["FIFOs"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%ss"%(config["stalling"][0], )

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
        gen_general_ports()
        gen_FIFO_ports ()
        gen_write_ports()
        gen_assignment_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_general_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # handle clock port
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]

    if CONFIG["stalling"] == "ACTIVE":
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "inout"
            }
        ]
    elif CONFIG["stalling"] == "PASSIVE":
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

def gen_FIFO_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "-- FIFO ports buffers\n"
    ARCH_BODY += "-- FIFO ports buffers\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 0,
            "sync_forces"   : 0,
            "has_enable"    : False
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    for FIFO in range(CONFIG["FIFOs"]):
        # Declare ports standard comm put ports
        INTERFACE["ports"] += [
            {
                "name" : "FIFO_%i_data"%(FIFO, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "out"
            },
            {
                "name" : "FIFO_%i_write"%(FIFO, ),
                "type" : "std_logic",
                "direction" : "out"
            }
        ]

        if CONFIG["stalling"] == "ACTIVE":
            INTERFACE["ports"] += [
                {
                    "name" : "FIFO_%i_ready"%(FIFO, ),
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]

        # Generate output buffers
        ARCH_HEAD += "signal FIFO_%i_write_internal : std_logic;\n"%(FIFO, )
        ARCH_HEAD += "signal FIFO_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(FIFO, CONFIG["data_width"] - 1)

        ARCH_BODY += "FIFO_%i_data_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => FIFO_%i_data_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out => FIFO_%i_data\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<"

        ARCH_BODY += "FIFO_%i_write_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)
        ARCH_BODY += "generic map (data_width => 1)\n"
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in (0) => FIFO_%i_write_internal,\n"%(FIFO, )
        ARCH_BODY += "data_out(0) => FIFO_%i_write\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<"

def gen_write_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for port in range(CONFIG["writes"]):
        # Declare port
        INTERFACE["ports"] += [
            {
                "name" : "write_%i_addr"%(port, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_data_word_0"%(port, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_enable"%(port, ),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

def gen_assignment_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle stalling
    if CONFIG["stalling"] == "ACTIVE":
        if CONFIG["writes"] == 1:
            ARCH_BODY += "stall <=\> %s\nelse 'Z';\<\n"%(
                "\nelse ".join(
                    [
                        "'1' when write_0_enable = '1' and write_0_addr = \"%s\" and FIFO_%i_ready /= '1'"%(
                            tc_utils.unsigned.encode(FIFO, CONFIG["addr_width"]),
                            FIFO
                        )
                        for FIFO in range(CONFIG["FIFOs"])
                    ]
                )
            )
        else:
            raise NotImplementedError()

    # Data paths
    ARCH_BODY += "\n-- Data Path\n"
    if CONFIG["writes"] == 1:
        for FIFO in range(CONFIG["FIFOs"]):
            ARCH_BODY += "FIFO_%i_data_buffer_in <= write_0_data_word_0;\n"%(FIFO, )

            if CONFIG["stalling"] == "NONE":
                ARCH_BODY += "FIFO_%i_write_internal <= '1' when write_0_enable = '1' and write_0_addr = \"%s\" else '0';\n"%(FIFO, tc_utils.unsigned.encode(0, CONFIG["addr_width"]))
            else:
                ARCH_BODY += "FIFO_%i_write_internal <= '1' when write_0_enable = '1' and write_0_addr = \"%s\" and stall /= '1' else '0';\n"%(FIFO, tc_utils.unsigned.encode(0, CONFIG["addr_width"]))
    else:
        raise NotImplementedError()
