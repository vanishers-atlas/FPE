# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register

#####################################################################

import copy

def preprocess_config(config_in):
    config_out = {}

    # Handle stalling
    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    # Handle counter value
    assert(config_in["program_length"] > 0)
    config_out["program_length"] = config_in["program_length"]
    config_out["PC_width"] = tc_utils.unsigned.width(config_out["program_length"] - 1)

    # Hanlde ZOLs
    config_out["ZOLs_present"] = len(config_in["ZOLs"]) > 0

    # Handle jumping
    assert(type(config_in["uncondional_jump"]) == type(True))
    config_out["uncondional_jump"] = config_in["uncondional_jump"]
    config_out["statuses"] = copy.deepcopy(config_in["statuses"])
    config_out["jumping_enabled"] = config_out["uncondional_jump"] or len(config_out["statuses"]) > 0

    # Handle inputs
    assert(type(config_in["inputs"]) == type([]))
    config_out["inputs"] = []
    for words in config_in["inputs"]:
        assert(words == 1)
        config_out["inputs"].append(words)

    return config_out

import zlib

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "PC"

        generated_name += "_%ir"%2**config["PC_width"]

        if config["stallable"]:
            generated_name += "_stall"
        else:
            generated_name += "_nostall"

        if config["jumping_enabled"]:
            jumps = str(config["uncondional_jump"])
            jumps += "\n".join(sorted(config["statuses"]))
            generated_name += "_%sjmp"%str( hex(
                zlib.adler32(jumps.encode('utf-8'))
            ) ).lstrip("0x").zfill(8)
        else:
            generated_name += "_nojmp"

        if config["ZOLs_present"]:
            generated_name += "_ZOL"
        else:
            generated_name += "_noZOL"

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
            {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"},
            {"library" : "ieee", "package" : "numeric_std", "parts" : "all"},
        ]

        # Setop common ports
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generation Module Code
        populate_interface()
        generate_data_ports()
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

def populate_interface():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["PC_width"] = CONFIG["PC_width"]

def generate_data_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for input, words in enumerate(CONFIG["inputs"]):
        for word in range(words):
            INTERFACE["ports"] += [
                {
                    "name" : "in_%i_word_%i"%(input, word,),
                    "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
                    "direction" : "in"
                }
            ]




def generate_state_management():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        {
            "name" : "kickoff",
            "type" : "std_logic",
            "direction" : "in"
        }
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
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        {
            "name" : "running",
            "type" : "std_logic",
            "direction" : "out"
        }
    ]

    ARCH_HEAD += "signal internal_running : std_logic;\n"

    ARCH_BODY += "\n-- Running handling\n"
    ARCH_BODY += "running <= internal_running;\n"

    ARCH_BODY += "internal_running <=\> '0' when last_state = INACTIVE\n"
    ARCH_BODY += "else '1' when (last_state = STARTING or last_state = ACTIVE)\n"
    ARCH_BODY += "else 'U';\<\n"

def generate_value_register():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        {
            "name" : "value",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
            "direction" : "out"
        },
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
    ARCH_BODY += "data_width => %i,\n"%(CONFIG["PC_width"], )
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

    ARCH_HEAD += "signal internal_value, next_value : std_logic_vector(%i downto 0);\n"%(CONFIG["PC_width"] - 1)

    ARCH_BODY += "value <= internal_value;\n"

def generate_end_value_checking():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- End Value Checking\n"

    INTERFACE["generics"] += [
        {
            "name" : "end_value",
            "type" : "integer",
        }
    ]

    ARCH_HEAD += "signal end_reached : std_logic;\n"

    ARCH_BODY += "end_reached <= '1' when to_integer(unsigned(next_value)) = end_value else '0';\n"

def generate_jumping():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Exit if no jumping
    if not CONFIG["uncondional_jump"] and len(CONFIG["statuses"]) == 0:
        CONFIG["jumping_enabled"] = False
        return

    # Check there is enough input ports for jumping
    assert(len(CONFIG["inputs"]) >= 1)
    assert(CONFIG["inputs"][0] >= 1)

    CONFIG["jumping_enabled"] = True
    ARCH_HEAD += "signal jump_occured : std_logic;\n"
    jump_occured = "jump_occured <=\>"

    # Handle uncondional_jump
    if CONFIG["uncondional_jump"]:
        INTERFACE["ports"] += [
            {
                "name" : "jump_uncondional",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]
        jump_occured += "'1' when jump_uncondional = '1'\nelse "

    # Handle condional_jumps
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
        # Buffer all statuses from the same exe compoundent together
        INTERFACE["ports"] += [
            {
                "name" : "update_%s_statuses"%(exe),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

        ARCH_HEAD += "signal %s_statuses_in, %s_statuses_out : std_logic_vector(%i downto 0);\n"%(exe, exe, len(signals) - 1)

        ARCH_BODY += "%s_statuses_reg : entity work.%s(arch)\>\n"%(exe, reg_name)
        ARCH_BODY += "generic map ( data_width => %i )\n"%(len(signals))
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "enable => update_%s_statuses,\n"%(exe)
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => %s_statuses_in,\n"%(exe)
        ARCH_BODY += "data_out => %s_statuses_out\n"%(exe)
        ARCH_BODY += "\<);\n"
        ARCH_BODY += "\<\n"

        for i, signal in enumerate(signals):
            # Create status and jump port for each status
            INTERFACE["ports"] += [
                {
                    "name" : "%s_status_%s"%(exe, signal),
                    "type" : "std_logic",
                    "direction" : "in"
                },
                {
                    "name" : "jump_%s_%s"%(exe, signal),
                    "type" : "std_logic",
                    "direction" : "in"
                },
            ]

            # Pack and unpack statuses into buffer
            ARCH_HEAD += "signal %s_status_%s_buffered : std_logic;\n"%(exe, signal)

            ARCH_BODY += "%s_statuses_in(%i) <= %s_status_%s;\n"%(exe, i, exe, signal)
            ARCH_BODY += "%s_status_%s_buffered <= %s_statuses_out(%i);\n"%(exe, signal, exe, i)

            # Generate Jump logic
            jump_occured += "'1' when %s_status_%s_buffered = '1' and jump_%s_%s = '1'\nelse "%(exe, signal, exe, signal)

    # Finish jump occured logic and add to arch-body
    jump_occured += "\<'0';\n"
    ARCH_BODY += jump_occured

def generate_next_value():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "next_value <=\> "

    if CONFIG["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            },
        ]
        ARCH_BODY += "internal_value when stall = '1'\nelse "

    if CONFIG["ZOLs_present"]:
        INTERFACE["ports"] += [
            {
                "name" : "ZOL_value",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
                "direction" : "in"
            },
            {
                "name" : "ZOL_overwrite",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

        ARCH_BODY += "ZOL_value when ZOL_overwrite = '1'\nelse "

    if CONFIG["jumping_enabled"]:
        ARCH_BODY += "in_0_word_0 when jump_occured = '1'\nelse "

    ARCH_BODY += "std_logic_vector(to_unsigned(to_integer(unsigned(internal_value)) + 1, next_value'length));\n\<"
