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
        IMPORTS += [ {"library" : "ieee", "package" : "numeric_std", "parts" : "all"} ]

        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generation Module Code
        generate_increment_controls()
        generate_outset_adder_acc()
        generate_base_adders()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_increment_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "signal selected_increment : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )
    ARCH_BODY += "selected_increment <= \>"

    # Declare fetch fixed increment generic
    INTERFACE["generics"] += [ { "name" : "increment", "type" : "integer" } ]
    INTERFACE["ports"] += [
        { "name" : "fetch_fixed_inc", "type" : "std_logic", "direction" : "in" }
    ]
    ARCH_BODY +="std_logic_vector(to_unsigned(increment, %i)) when fetch_fixed_inc = '1'\nelse "%(CONFIG["data_width"])

    # Declare port for data increment
    if  CONFIG["data_inc"] == True:
        INTERFACE["ports"] += [
            { "name" : "data_in" , "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ), "direction" : "in" },
            { "name" : "data_inc", "type" : "std_logic", "direction" : "in" }
        ]
        ARCH_BODY += "data_in when data_inc = '1'\nelse "

    ARCH_BODY += "(others => '0');\<\n"


    ARCH_HEAD += "signal advance : std_logic;\n"
    ARCH_BODY += "advance <= fetch_fixed_inc"
    if  CONFIG["data_inc"] == True:
        ARCH_BODY += " or data_inc"
    ARCH_BODY += ";\n"

def generate_outset_adder_acc():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [ { "name" : "reset", "type" : "std_logic", "direction" : "in" } ]

    ARCH_HEAD += "signal curr_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )
    ARCH_HEAD += "signal last_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )

    ARCH_BODY += "curr_offset <= std_logic_vector(to_unsigned(to_integer(unsigned(selected_increment)) + to_integer(unsigned(last_offset)), curr_offset'length));\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 1,
            "sync_forces"   : 0,
            "has_enable"    : True
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    ARCH_BODY += "offset_acc : entity work.%s(arch)\>\n"%(reg_name)
    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "asyn_0_value => 0,\n"
    ARCH_BODY += "data_width => %i\n"%(CONFIG["data_width"])
    ARCH_BODY += "\<)\n"
    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "enable => advance,\n"
    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "data_in => curr_offset,\n"
    ARCH_BODY += "data_out => last_offset,\n"
    ARCH_BODY += "asyn_reset_sel(0) => reset\n"
    ARCH_BODY += "\<);\n\<"

def generate_base_adders():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["generics"] += [ { "name" : "base", "type" : "integer" } ]
    INTERFACE["ports"] += [ { "name" : "address", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ), "direction" : "out" } ]

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

    ARCH_HEAD += "signal pre_address : std_logic_vector(%i downto 0);"%(CONFIG["addr_width"] - 1, )

    ARCH_BODY += "address_buffer: entity work.%s(arch)\>\n"%(reg_name)
    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "data_width => %i\n"%(CONFIG["addr_width"])
    ARCH_BODY += "\<)\n"
    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "data_in => pre_address,\n"
    ARCH_BODY += "data_out => address\n"
    ARCH_BODY += "\<);\n\<"

    ARCH_BODY += "pre_address <= std_logic_vector(to_unsigned(base + to_integer(unsigned(curr_offset)), pre_address'length));\n"
