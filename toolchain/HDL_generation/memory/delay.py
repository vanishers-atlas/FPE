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
        IMPORTS += [ {"library" : "ieee", "package" : "Numeric_Std", "parts" : "all"} ]

        # Generation Module Code
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        INTERFACE["generics"] += [ { "name" : "delay_width", "type" : "integer", } ]
        INTERFACE["generics"] += [ { "name" : "delay_depth", "type" : "integer", } ]

        INTERFACE["ports"] += [ { "name" : "data_in" , "type" : "std_logic_vector(delay_width - 1 downto 0)", "direction" : "in"  } ]
        INTERFACE["ports"] += [ { "name" : "data_out", "type" : "std_logic_vector(delay_width - 1 downto 0)", "direction" : "out" } ]

        ARCH_HEAD += "type data_array is array (delay_depth - 1 downto 0) of std_logic_vector(delay_width - 1 downto 0);\n"
        ARCH_HEAD += "signal data : data_array;\n"

        ARCH_BODY += "process (clock)\>\n"
        ARCH_BODY += "\<begin\>\n"

        ARCH_BODY += "if rising_edge(clock) then\>\n"

        ARCH_BODY += "if data'left > 0 then\>\n"
        ARCH_BODY += "data(data'left - 1 downto 0) <= data(data'left downto 1);\n"
        ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "data(data'left) <= data_in;\n"

        ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end process;\n"

        ARCH_BODY += "data_out <= data(0);\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_value_array():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Declare internal data array
    ARCH_HEAD += "type data_array is array (%i downto 0) of std_logic_vector(%i downto 0);\n"%(CONFIG["depth"] - 1, CONFIG["data_width"] - 1)
    ARCH_HEAD += "signal data : data_array;\n"

def gen_reads():
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
            }
        ]

        # Generate output buffers
        ARCH_HEAD += "signal read_%i_buffer_in : std_logic_vector(%i downto 0);\n"%(read, CONFIG["data_width"] - 1)

        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => read_%i_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )
        ARCH_BODY += "\<);\n\<"

        ARCH_BODY += "read_%i_buffer_in <= data(to_integer(unsigned(read_%i_addr)));\n"%(read, read)

def gen_writes():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for write in range(CONFIG["writes"]):
        # Declare port
        INTERFACE["ports"] += [
            {
                "name" : "write_%i_addr"%(write, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_data"%(write, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_enable"%(write, ),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

    if CONFIG["writes"] == 1:
        ARCH_BODY += "\n-- Write proccess\n"
        ARCH_BODY += "process (clock)\>\n"
        ARCH_BODY += "\<begin\>\n"
        ARCH_BODY += "if rising_edge(clock) then\>\n"
        ARCH_BODY += "if write_0_enable = '1' then\>\n"
        ARCH_BODY += "data(to_integer(unsigned(write_0_addr))) <= write_0_data;\n"
        ARCH_BODY += "\<end if;\n"
        ARCH_BODY += "\<end if;\n"
        ARCH_BODY += "\<end process;\n"

    else:
        raise NotImplementedError()
