from ..  import utils as gen_utils
from ... import utils as tc_utils

def generate_HDL(config, output_path, module_name, append_hash=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION

    config["registers"] = tc_utils.biased_tally.width(config["count"], 1, 31)
    del config["count"]

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

        # Setop common ports
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        generate_PC_checking()
        #generate_state_control()
        generate_delay()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

def generate_PC_checking():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [ {"library" : "ieee"  , "package" : "numeric_std"   , "parts" : "all"} ]

    INTERFACE["generics"] += [
        { "name" : "start_value", "type" : "integer", },
        { "name" : "end_value"  , "type" : "integer", },
    ]

    INTERFACE["ports"] += [
        { "name" : "value_in" , "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "in" },
        { "name" : "value_out", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "out" },
        { "name" : "overwrite", "type" : "std_logic", "direction" : "out" },
        { "name" : "PC_running"  , "type" : "std_logic", "direction" : "in" },
    ]
    ARCH_HEAD += "type tracker_state is (INACTIVE, ACTIVE);\n"
    ARCH_HEAD += "signal curr_state : tracker_state := INACTIVE;\n"
    ARCH_HEAD += "signal next_state : tracker_state;\n"

    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "curr_state <= next_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"

    ARCH_BODY += "next_state <=\>ACTIVE when curr_state = INACTIVE and start_found = '1'\n"
    ARCH_BODY += "else INACTIVE when curr_state = ACTIVE and delay_out = '1'\n"
    ARCH_BODY += "else curr_state;\n\>\n"

    ARCH_BODY += "value_out <= std_logic_vector(to_unsigned(start_value, value_out'length));\n"

    ARCH_HEAD += "signal start_found : std_logic;\n"
    ARCH_HEAD += "signal end_found : std_logic;\n"

    ARCH_BODY += "start_found <= '1' when PC_running = '1' and start_value = to_integer(unsigned(value_in)) else '0';\n"
    ARCH_BODY += "end_found   <= '1' when end_value = to_integer(unsigned(value_in)) else '0';\n"

    ARCH_BODY += "delay_in <= '1' when curr_state = INACTIVE and start_found = '1' else '0';\n"
    ARCH_BODY += "delay_clock_enable <= delay_in or end_found;\n"
    ARCH_BODY += "overwrite <= '1' when end_found = '1' and delay_out = '0' else '0';\n"


def generate_state_control():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [ {"library" : "ieee"  , "package" : "numeric_std"   , "parts" : "all"} ]

    INTERFACE["generics"] += [
        { "name" : "start_value", "type" : "integer", },
        { "name" : "end_value"  , "type" : "integer", },
    ]

    INTERFACE["ports"] += [
        { "name" : "value_in" , "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "in" },
        { "name" : "value_out", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "out" },
        { "name" : "overwrite", "type" : "std_logic", "direction" : "out" },
        { "name" : "PC_running"  , "type" : "std_logic", "direction" : "in" },
    ]

    ARCH_HEAD += "type tracker_state is (INACTIVE, ACTIVE);\n"
    ARCH_HEAD += "signal state : tracker_state := INACTIVE;\n"

    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"

    ARCH_BODY += "if rising_edge(clock) then\>\n"

    ARCH_BODY += "case state is\>\n"

    ARCH_BODY += "\<when INACTIVE =>\>\n"
    ARCH_BODY += "overwrite <= '0';\n"
    ARCH_BODY += "delay_in <= '0';\n"
    ARCH_BODY += "delay_clock_enable  <= '0';\n"

    ARCH_BODY += "if PC_running = '1' and start_value = to_integer(unsigned(value_in)) then\>\n"
    ARCH_BODY += "state <= ACTIVE;\n"
    ARCH_BODY += "delay_in <= '1';\n"
    ARCH_BODY += "delay_clock_enable  <= '1';\n"
    ARCH_BODY += "\<end if;\n"

    ARCH_BODY += "\<when ACTIVE =>\>\n"
    ARCH_BODY += "overwrite <= '0';\n"
    ARCH_BODY += "delay_in <= '0';\n"
    ARCH_BODY += "delay_clock_enable  <= '0';\n"

    ARCH_BODY += "if end_value = to_integer(unsigned(value_in)) then\>\n"
    ARCH_BODY += "delay_clock_enable  <= '1';\n"
    ARCH_BODY += "if delay_out = '1' then\>\n"
    ARCH_BODY += "state <= INACTIVE;\n"
    ARCH_BODY += "\<else\>\n"
    ARCH_BODY += "overwrite <= '1';\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end if;\n"

    ARCH_BODY += "\<end case;\n"

    ARCH_BODY += "\<end if;\n"

    ARCH_BODY += "\<end process;\n\n"

def generate_delay():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [ {"library" : "UNISIM", "package" : "vcomponents"   , "parts" : "all"}, ]

    INTERFACE["generics"] += [
        { "name" : "delay_tally", "type" : "integer", },
    ]

    ARCH_HEAD += "signal delay_in, delay_out, delay_clock_enable : std_logic;\n"

    if CONFIG["registers"] == 1:
        ARCH_BODY += "reg : SRLC32E\n\>"
        ARCH_BODY += "generic map (INIT => X\"80000000\")\n"
        ARCH_BODY += "port map (\>\n"
        ARCH_BODY += "A => std_logic_vector(to_unsigned(delay_tally, 5)),\n"
        ARCH_BODY += "D => delay_in,\n"
        ARCH_BODY += "Q => delay_out,\n"
        ARCH_BODY += "CLK => clock,\n"
        ARCH_BODY += "CE => delay_clock_enable,\n"
        ARCH_BODY += "Q31 => open\n"
        ARCH_BODY += "\<);\n\<"
    else:
        raise NotImplementedError()
