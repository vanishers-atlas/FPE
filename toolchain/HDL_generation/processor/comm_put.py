# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register, mux

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Stalling parameters
    assert(type(config_in["FIFO_handshakes"]) == type(True))
    config_out["FIFO_handshakes"] = config_in["FIFO_handshakes"]
    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]
    if   config_in["FIFO_handshakes"]:
        config_out["stall_type"] = "ACTIVE"
    elif config_in["stallable"]:
        config_out["stall_type"] = "PASSIVE"
    else:
        config_out["stall_type"] = "NONE"

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
        generated_name += "_%s"%(config["stall_type"][0], )

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

        # Generation Module Code
        gen_ports()
        gen_stalling_logic()
        gen_FIFO_data_logic()
        gen_FIFO_write_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Decalre clock and runnning ports
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        },
        {
            "name" : "running",
            "type" : "std_logic",
            "direction" : "in"
        },
    ]

    # Handle FIFO ports
    for FIFO in range(CONFIG["FIFOs"]):
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
        if CONFIG["FIFO_handshakes"]:
            INTERFACE["ports"] += [
                {
                    "name" : "FIFO_%i_ready"%(FIFO, ),
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]

    # Handle read ports
    for read in range(CONFIG["writes"]):
        INTERFACE["ports"] += [
            {
                "name" : "write_%i_addr"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_data"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_enable"%(read, ),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

    # Handle stalling ports
    if   CONFIG["stall_type"] == "ACTIVE":
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "inout"
            }
        ]
    elif CONFIG["stall_type"] == "PASSIVE":
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

def gen_stalling_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle FIFO_handshakes stall checking
    if CONFIG["FIFO_handshakes"] :
        ARCH_BODY += "\n-- FIFO_handshakes stall logic\n"

        ARCH_HEAD += "signal FIFO_handshake_stall : std_logic;\n"
        ARCH_BODY += "stall <= '1' when FIFO_handshake_stall = '1' else 'L';\n"

        if CONFIG["FIFOs"] == 1:
            # This code may need reworking, depending on how vivado handles many termed logic expressions
            ARCH_BODY += "FIFO_handshake_stall <= %s;\n"%(
                " or ".join([
                    "(write_%i_enable and not FIFO_0_ready)"%(i, )
                    for i in range(CONFIG["writes"])
                ]),
            )
        else:#CONFIG["FIFOs"] >  1:
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs" : CONFIG["FIFOs"]
                },
                OUTPUT_PATH,
                "mux",
                True,
                False
            )

            for write in range(CONFIG["writes"]):
                ARCH_HEAD += "signal write_%i_FIFO_ready : std_logic;\n"%(write, )

                ARCH_BODY += "write_%i_FIFO_ready_mux : entity work.%s(arch)\>\n"%(write, mux_name, )

                ARCH_BODY += "generic map (data_width => 1)\n"

                ARCH_BODY += "port map (\n\>"
                ARCH_BODY += "sel => write_%i_addr,\n"%(write, )
                for i in range(0, CONFIG["FIFOs"]):
                    ARCH_BODY += "data_in_%i(0) => FIFO_%i_ready,\n"%(i, i, )
                for i in range(CONFIG["FIFOs"], mux_interface["number_inputs"]):
                    ARCH_BODY += "data_in_%i(0) => '0',\n"%(i, )
                ARCH_BODY += "data_out(0) => write_%i_FIFO_ready\n"%(write, )

                ARCH_BODY += "\<);\n\<\n"

            # This code may need reworking, depending on how vivado handles many termed logic expressions
            ARCH_BODY += "FIFO_handshake_stall <= %s;\n"%(
                " or ".join([
                    "(write_%i_enable and not write_%i_FIFO_ready)"%(i, i, )
                    for i in range(CONFIG["writes"])
                ]),
            )

def gen_FIFO_write_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate FIFO_adv buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : False
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    # instance FIFO_adv buffers
    ARCH_HEAD += "\n-- FIFO write signals\n"
    ARCH_BODY += "\n-- FIFO write buffers\n"
    for FIFO in range(CONFIG["FIFOs"]):
        ARCH_HEAD += "signal FIFO_%i_write_buffer_in : std_logic;\n"%(FIFO,)

        ARCH_BODY += "FIFO_%i_write_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        ARCH_BODY += "generic map (data_width => 1)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in(0) => FIFO_%i_write_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out(0) => FIFO_%i_write\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<\n"

    # FIFO_adv logic
    ARCH_BODY += "\n-- FIFO advance logic\n"
    if CONFIG["writes"] == 1:
        if CONFIG["FIFOs"] == 1:
            if CONFIG["stall_type"] != "NONE":
                ARCH_BODY += "FIFO_0_write_buffer_in <= (not stall) and running and write_0_enable;\n"
            else:
                ARCH_BODY += "FIFO_0_write_buffer_in <= running and write_0_enable;\n"
        else:#CONFIG["FIFOs"] >= 2:
            if CONFIG["stall_type"] != "NONE":
                for FIFO in range(CONFIG["FIFOs"]):
                    # This code may need reworking, depending on how vivado handles many termed logic expressions
                    ARCH_BODY += "FIFO_%i_write_buffer_in <= (not stall) and running and FIFO_%i_ready and write_0_enable and %s;\n"%(
                        FIFO, FIFO,
                        " and ".join([
                            "write_0_addr(%i)"%(bit, ) if FIFO&2**bit
                            else "(not write_0_addr(%i))"%(bit, )
                            for bit in range(CONFIG["addr_width"])
                        ])
                    )
            else:
                for FIFO in range(CONFIG["FIFOs"]):
                    # This code may need reworking, depending on how vivado handles many termed logic expressions
                    ARCH_BODY += "FIFO_%i_write_buffer_in <= running and FIFO_%i_ready and write_0_enable and %s;\n"%(
                        FIFO, FIFO,
                        " and ".join([
                            "write_0_addr(%i)"%(bit, ) if FIFO&2**bit
                            else "(not write_0_addr(%i))"%(bit, )
                            for bit in range(CONFIG["addr_width"])
                        ])
                    )
    else:#CONFIG["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")

def gen_FIFO_data_logic ():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate read_data buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : CONFIG["stall_type"] != "NONE"
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    # Generate FIFO_data buffers
    ARCH_HEAD += "\n-- FIFO data signals\n"
    ARCH_BODY += "\n-- FIFO data buffers\n"
    for FIFO in range(CONFIG["FIFOs"]):
        ARCH_HEAD += "signal FIFO_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(FIFO, CONFIG["data_width"] - 1)

        ARCH_BODY += "FIFO_%i_data_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"
        if CONFIG["stall_type"] != "NONE":
            ARCH_BODY += "enable => not stall,\n"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => FIFO_%i_data_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out => FIFO_%i_data\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<\n"

    # FIFO_data assignment logic
    ARCH_BODY += "\n-- FIFO_data assignment logic\n"
    if CONFIG["writes"] == 1:
        for FIFO in range(CONFIG["FIFOs"]):
            ARCH_BODY += "FIFO_%i_data_buffer_in <= write_0_data;\n"%(FIFO, )
    else:#CONFIG["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")
