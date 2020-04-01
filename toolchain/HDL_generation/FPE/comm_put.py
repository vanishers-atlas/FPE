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

        # Generation Module Code
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]
        gen_FIFO_ports ()
        gen_write_ports()
        gen_assignment_logic()

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

    for FIFO in range(CONFIG["depth"]):
        # Declare ports
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
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
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
                "name" : "write_%i_data"%(port, ),
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
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Data Path\n"
    if CONFIG["writes"] == 1:
        for FIFO in range(CONFIG["depth"]):
            ARCH_BODY += "FIFO_%i_data_buffer_in <= write_0_data;\n"%(FIFO, )
            ARCH_BODY += "FIFO_%i_write_internal <= write_0_enable when write_0_addr = \"%s\" else '0';\n"%(FIFO, tc_utils.unsigned.encode(0, CONFIG["addr_width"]))
    else:
        raise NotImplementedError()
