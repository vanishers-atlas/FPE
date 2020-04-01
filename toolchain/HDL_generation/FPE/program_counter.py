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
        IMPORTS += [
            {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"},
            {"library" : "ieee", "package" : "numeric_std", "parts" : "all"},
        ]

        # Setop common ports
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generation Module Code
        generate_state_management()
        generate_generate_running()
        generate_value_register()
        generate_end_value_checking()
        generate_jumping()
        generate_next_value()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_state_management():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        { "name" : "kickoff", "type" : "std_logic", "direction" : "in"  }
    ]

    ARCH_HEAD += "type PC_states is (INACTIVE, STARTING, ACTIVE);\n"
    ARCH_HEAD += "signal last_state : PC_states := INACTIVE;\n"
    ARCH_HEAD += "signal curr_state : PC_states;\n"

    ARCH_BODY += "-- State updating process\n"
    ARCH_BODY += "process(clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "last_state <= curr_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n"

    ARCH_BODY += "curr_state <=\> STARTING when last_state = INACTIVE and kickoff = '1'\n"
    ARCH_BODY += "else ACTIVE   when last_state = STARTING\n"
    ARCH_BODY += "else INACTIVE when last_state = ACTIVE and end_reached = '1'\n"
    ARCH_BODY += "else last_state;\n"

def generate_generate_running():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        { "name" : "running", "type" : "std_logic", "direction" : "out" }
    ]

    ARCH_HEAD += "signal internal_running : std_logic;\n"

    ARCH_BODY += "\n-- Running handling\n"
    ARCH_BODY += "running <= internal_running;\n"

    ARCH_BODY += "internal_running <=\> '0' when last_state = INACTIVE\n"
    ARCH_BODY += "else '1' when (last_state = STARTING or last_state = ACTIVE)\n"
    ARCH_BODY += "else 'U';\<\n"

def generate_value_register():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        { "name" : "value", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "out"  },
    ]

    ARCH_BODY += "\n-- Value register\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 0,
            "sync_forces"   : 1,
            "has_enable"    : True
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    ARCH_BODY += "value_reg : entity work.%s(arch)\>\n"%(reg_name)

    ARCH_BODY += "generic map (\n\>"
    ARCH_BODY += "data_width => %i,\n"%(CONFIG["width"], )
    ARCH_BODY += "syn_0_value => 0"
    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "enable  => internal_running,\n"
    ARCH_BODY += "syn_reset_sel(0) => value_reg_reset,\n"
    ARCH_BODY += "data_in  => next_value,\n"
    ARCH_BODY += "data_out => internal_value\n"
    ARCH_BODY += "\<);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "\n-- Value register controls\n"

    ARCH_HEAD += "signal value_reg_reset : std_logic;\n"

    ARCH_BODY += "value_reg_reset <=\> '1' when last_state = STARTING\n"
    ARCH_BODY += "else '0' when last_state = INACTIVE or last_state = ACTIVE\n"
    ARCH_BODY += "else 'U';\<\n"

    ARCH_HEAD += "signal internal_value, next_value : std_logic_vector(%i downto 0);\n"%(CONFIG["width"] - 1)

    ARCH_BODY += "value <= internal_value;\n"

def generate_end_value_checking():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- End Value Checking\n"

    INTERFACE["generics"] += [ { "name" : "end_value", "type" : "integer", } ]

    ARCH_HEAD += "signal end_reached : std_logic;\n"

    ARCH_BODY += "end_reached <= '1' when to_integer(unsigned(next_value)) = end_value else '0';\n"

def generate_jumping():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Exit if no jumping
    if not CONFIG["uncondional_jump"] and len(CONFIG["statuses"]) == 0:
        CONFIG["jumping_enabled"] = False
        return

    CONFIG["jumping_enabled"] = True
    INTERFACE["ports"] += [
        { "name" : "jump_value", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "in"  }
    ]

    ARCH_HEAD += "signal jump_occured : std_logic;\n"
    jump_occured = "jump_occured <=\>"

    if CONFIG["uncondional_jump"]:
        INTERFACE["ports"] += [ { "name" : "jump_uncondional", "type" : "std_logic", "direction" : "in"  } ]
        jump_occured += "'1' when jump_uncondional = '1'\nelse "

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 0,
            "sync_forces"   : 0,
            "has_enable"    : True
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    for exe, signals in CONFIG["statuses"].items():
        INTERFACE["ports"] += [ { "name" : "update_%s_statuses"%(exe), "type" : "std_logic", "direction" : "in"  } ]

        ARCH_HEAD += "signal %s_statuses_in, %s_statuses_out : std_logic_vector(%i downto 0);\n"%(exe, exe, len(signals) - 1)

        ARCH_BODY += "%s_reg : entity work.%s(arch)\>\n"%(exe, reg_name)
        ARCH_BODY += "generic map ( data_width => %i )\n"%(len(signals))
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "enable => update_%s_statuses,\n"%(exe)
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => %s_statuses_in,\n"%(exe)
        ARCH_BODY += "data_out => %s_statuses_out\n"%(exe)
        ARCH_BODY += "\<);\n"
        ARCH_BODY += "\<\n"

        for i, signal in enumerate(signals):
            INTERFACE["ports"] += [
                { "name" : "%s_status_%s"%(exe, signal), "type" : "std_logic", "direction" : "in"  },
                { "name" : "jump_%s_%s"%(exe, signal), "type" : "std_logic", "direction" : "in"  },
            ]

            ARCH_HEAD += "signal %s_status_%s_buffered : std_logic;\n"%(exe, signal)

            ARCH_BODY += "%s_statuses_in(%i) <= %s_status_%s;\n"%(exe, i, exe, signal)
            ARCH_BODY += "%s_status_%s_buffered <= %s_statuses_out(%i);\n"%(exe, signal, exe, i)

            jump_occured += "'1' when %s_status_%s_buffered = '1' and jump_%s_%s = '1'\nelse "%(exe, signal, exe, signal)

    jump_occured += "\<'0';\n"
    ARCH_BODY += jump_occured

def generate_next_value():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "next_value <=\> "
    if CONFIG["supports_ZOL"]:
        INTERFACE["ports"] += [
            { "name" : "ZOL_value", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1), "direction" : "in"  },
            { "name" : "ZOL_overwrite", "type" : "std_logic", "direction" : "in"  }
        ]

        ARCH_BODY += "ZOL_value when ZOL_overwrite = '1'\nelse "

    if CONFIG["jumping_enabled"]:
        ARCH_BODY += "jump_value when jump_occured = '1'\nelse "

    ARCH_BODY += "std_logic_vector(to_unsigned(to_integer(unsigned(internal_value)) + 1, next_value'length));\n\<"
