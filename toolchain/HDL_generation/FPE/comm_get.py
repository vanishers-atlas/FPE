from ..  import utils as gen_utils
from ... import utils as tc_utils

from ..memory import register

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
        IMPORTS += [ {"library" : "ieee", "package" : "Numeric_Std", "parts" : "all"} ]

        # Generation Module Code
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]
        gen_FIFO_ports ()
        gen_read_ports()
        gen_assignment_logic()
        gen_advance_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_FIFO_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
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

    ARCH_BODY += "-- FIFO Latches\n"

    for FIFO in range(CONFIG["depth"]):
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

        # Generate FIFO latch
        ARCH_HEAD += "signal FIFO_%i_data_latched : std_logic_vector(%i downto 0);\n"%(FIFO, CONFIG["data_width"] - 1)

        ARCH_BODY += "FIFO_%i_data_latch : entity work.%s(arch)\>\n"%(FIFO, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => FIFO_%i_data,\n"%(FIFO, )
        ARCH_BODY += "data_out => FIFO_%i_data_latched\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<\n"

def gen_read_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

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
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => read_%i_data_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )
        ARCH_BODY += "\<);\n\<\n"

def gen_assignment_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Data Path\n"
    if CONFIG["depth"] == 1:
        for read in range(CONFIG["reads"]):
            ARCH_BODY += "read_%i_data_buffer_in <= FIFO_0_data_latched;\n"%(read, )
    else:
        for read in range(CONFIG["reads"]):
            ARCH_BODY += "read_%i_data_buffer_in <= \>"%(read, )
            for addr in range(CONFIG["depth"]):
                ARCH_BODY += "FIFO_%i_data_latched when read_%i_addr_int = %i\nelse "%(
                    addr, read, addr
                )
            ARCH_BODY += "(others => 'U');\<\n"

def gen_advance_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for FIFO in range(CONFIG["depth"]):
        ARCH_BODY += "FIFO_%i_red <= \>"%(FIFO, )
        for port in range(CONFIG["reads"]):
            ARCH_BODY += "read_%i_adv when read_%i_addr = \"%s\"\nelse "%(
                    port,
                    port,
                    tc_utils.unsigned.encode(FIFO, CONFIG["addr_width"])
                )
        ARCH_BODY += "\<'0';\n"
