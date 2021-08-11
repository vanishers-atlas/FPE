# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register

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
    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]
    assert(config_in["FIFOs"] >= 1)
    config_out["FIFOs"] = config_in["FIFOs"]

    # Datapath parametes
    assert(config_in["data_width"] >= 0)
    config_out["data_width"] = config_in["data_width"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_out["FIFOs"] - 1)

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "GET"

        # Denote Data width, writes, and FIFOs parameters
        generated_name += "_%ird"%(config["reads"], )
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
        INTERFACE = { "ports" : [], "generics" : [] }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
            {
                "library" : "ieee",
                "package" : "Numeric_Std",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        gen_general_ports()
        gen_FIFO_ports ()
        gen_read_ports()
        gen_read_logic()

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
        "has_async_force"  : False,
        "has_sync_force"   : False,
        "has_enable"    : False
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    for FIFO in range(CONFIG["FIFOs"]):
        # Declare ports
        INTERFACE["ports"] += [
            {
                "name" : "FIFO_%i_data"%(FIFO, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "FIFO_%i_red"%(FIFO, ),
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

        # Generate FIFO red buffer
        ARCH_HEAD += "signal FIFO_%i_red_buffer_in : std_logic;\n"%(FIFO,)

        ARCH_BODY += "FIFO_%i_red_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        ARCH_BODY += "generic map (data_width => 1)\n"

        ARCH_BODY += "port map (\n\>"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in(0) => FIFO_%i_red_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out(0) => FIFO_%i_red\n"%(FIFO, )

        ARCH_BODY += "\<);\n\<\n"

def gen_read_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : CONFIG["stalling"] != "NONE"
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    # Handle reads with advance
    ARCH_BODY += "\n-- Output Buffers\n"
    for read in range(CONFIG["reads"]):
        # Declare port
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
            },
            {
                "name" : "read_%i_adv"%(read, ),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

        ARCH_HEAD += "signal read_%i_addr_int : integer;\n"%(read)
        ARCH_BODY += "read_%i_addr_int <= to_integer(unsigned(read_%i_addr));\n\n"%(read, read)

        # Generate output buffers
        ARCH_HEAD += "signal read_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(read, CONFIG["data_width"] - 1)

        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"

        if CONFIG["stalling"] != "NONE":
            INTERFACE["ports"] += [
                {
                    "name" : "read_%i_enable"%(read, ),
                    "type" : "std_logic",
                    "direction" : "in"
                },
            ]
            ARCH_BODY += "enable => read_%i_enable and not stall,\n"%(read, )
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => read_%i_data_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )

        ARCH_BODY += "\<);\n\<\n"

def gen_read_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Datapath logic
    ARCH_BODY += "\n-- Data Path\n"
    if CONFIG["FIFOs"] == 1:
        for read in range(CONFIG["reads"]):
            ARCH_BODY += "read_%i_data_buffer_in <= FIFO_0_data;\n"%(read, )
    else:
        for read in range(CONFIG["reads"]):
            ARCH_BODY += "read_%i_data_buffer_in <= \>"%(read, )
            for addr in range(CONFIG["FIFOs"]):
                ARCH_BODY += "FIFO_%i_data when read_%i_addr_int = %i\nelse "%(
                    addr, read, addr
                )
            ARCH_BODY += "(others => 'U');\<\n"

    # Advance logic
    for FIFO in range(CONFIG["FIFOs"]):
        ARCH_BODY += "FIFO_%i_red_buffer_in <= \>"%(FIFO, )

        if CONFIG["stalling"] != "NONE":
            ARCH_BODY += "'0' when stall = '1'\nelse "

        for port in range(CONFIG["reads"]):
            ARCH_BODY += "'1' when read_%i_adv = '1' and read_%i_addr = \"%s\"\nelse "%(
                    port,
                    port,
                    tc_utils.unsigned.encode(FIFO, CONFIG["addr_width"])
                )
        ARCH_BODY += "\<'0';\n"

    # Stall logic
    if CONFIG["stalling"] == "ACTIVE":
        # Get teady for each read's FIFO
        for read in range(CONFIG["reads"]):
            ARCH_HEAD += "signal read_%i_ready : std_logic;\n"%(read, )

            if CONFIG["FIFOs"] == 1:
                ARCH_BODY += "read_%i_ready <= FIFO_0_ready;\n"%(read, )
            else:
                ARCH_BODY += "read_%i_ready <= \>"%(read, )
                for addr in range(CONFIG["FIFOs"]):
                    ARCH_BODY += "FIFO_%i_ready when read_%i_addr_int = %i\nelse "%(
                        addr, read, addr
                    )
                ARCH_BODY += "'1';\<\n"

        # Convert ready into stall
        for read in range(CONFIG["reads"]):
            ARCH_BODY += "stall <= '1' when read_%i_ready /= '1' and read_%i_enable = '1' else 'Z';\n"%(read, read,)
