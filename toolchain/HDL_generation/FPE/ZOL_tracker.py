# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["width"] > 0)
    config_out["width"] = config_in["width"]

    assert(config_in["count"] > 0)
    config_out["count"] = config_in["count"]

    # Handle delay regs and delay encoding
    config_out["delay_encoding"] = {
        "bais"  : 1,
        "range" : 31
    }
    config_out["registers"] = tc_utils.biased_tally.width(
        config_out["count"],
        config_out["delay_encoding"]["bais" ],
        config_out["delay_encoding"]["range"]
    )

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = "ZOL"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%iw"%(config["width"])
        generated_name += "_%ireg"%(config["registers"])
        generated_name += "_%ib"%(config["delay_encoding"]["bais"])
        generated_name += "_%ir"%(config["delay_encoding"]["range"])

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
            "generics" : [],
            "delay_encoding" : {
                "width" : CONFIG["registers"],
                "bais" : CONFIG["delay_encoding"]["bais"],
                "range" : CONFIG["delay_encoding"]["range"]
            }
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Setop common ports
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

        generate_PC_checking()
        generate_delay()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

def generate_PC_checking():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [
        {
            "library" : "ieee",
            "package" : "numeric_std",
            "parts" : "all"
        }
    ]

    INTERFACE["generics"] += [
        {
            "name" : "start_value",
            "type" : "integer",
        },
        {
            "name" : "end_value",
            "type" : "integer",
        },
    ]

    INTERFACE["ports"] += [
        {
            "name" : "value_in",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1),
            "direction" : "in"
        },
        {
            "name" : "value_out",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1),
            "direction" : "out"
        },
        {
            "name" : "overwrite",
            "type" : "std_logic",
            "direction" : "out"
        },
        {
            "name" : "PC_running",
            "type" : "std_logic",
            "direction" : "in"
        },
    ]
    if CONFIG["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            },
        ]

    ARCH_HEAD += "type tracker_state is (INACTIVE, SETUP, ACTIVE, CLEAR);\n"
    ARCH_HEAD += "signal last_state : tracker_state := INACTIVE;\n"
    ARCH_HEAD += "signal curr_state : tracker_state;\n"

    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "last_state <= curr_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"

    ARCH_BODY += "curr_state <=\>SETUP when last_state = INACTIVE and start_found = '1'\n"
    ARCH_BODY += "else CLEAR    when last_state = SETUP  and delay_out   = '1'\n"
    ARCH_BODY += "else ACTIVE   when last_state = SETUP  and end_found_delayed = '1'\n"
    ARCH_BODY += "else CLEAR    when last_state = ACTIVE and delay_out   = '1'\n"
    ARCH_BODY += "else INACTIVE when last_state = CLEAR  and delay_out   = '0'\n"
    ARCH_BODY += "else last_state;\n\<\n"


    ARCH_HEAD += "signal start_found : std_logic;\n"
    ARCH_HEAD += "signal end_found : std_logic;\n"
    ARCH_HEAD += "signal end_found_delayed : std_logic;\n"

    ARCH_BODY += "start_found <= '1' when PC_running = '1' and start_value = to_integer(unsigned(value_in)) else '0';\n"

    if CONFIG["stallable"]:
        ARCH_BODY += "end_found   <= '1' when stall /= '1' and PC_running = '1' and end_value = to_integer(unsigned(value_in)) else '0';\n\n"
    else:
        ARCH_BODY += "end_found   <= '1' when PC_running = '1' and end_value = to_integer(unsigned(value_in)) else '0';\n\n"

    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "end_found_delayed <= end_found;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"

    ARCH_BODY += "delay_clock_enable <= end_found;\n"
    ARCH_BODY += "delay_in <= '1' when curr_state = SETUP else '0';\n\n"

    ARCH_BODY += "value_out <= std_logic_vector(to_unsigned(start_value, value_out'length));\n"
    ARCH_BODY += "overwrite <= '1' when end_found = '1' and (curr_state = SETUP or curr_state = ACTIVE) else '0';\n\n"

def generate_delay():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [
        {
            "library" : "UNISIM",
            "package" : "vcomponents",
            "parts" : "all"
        },
    ]

    INTERFACE["generics"] += [
        {
            "name" : "delay_tally",
            "type" : "std_logic_vector(%i downto 0)"%(5*CONFIG["registers"] - 1),
        },
    ]

    ARCH_HEAD += "signal delay_in, delay_out, delay_clock_enable : std_logic;\n"

    # Handle a;; other  SRLs
    for reg in range(CONFIG["registers"]):
        ARCH_HEAD += "signal delay_reg_%i_out : std_logic;\n"%(reg)

        ARCH_BODY += "reg_%i : SRLC32E\n\>"%(reg)
        ARCH_BODY += "generic map (INIT => X\"00000000\")\n"
        ARCH_BODY += "port map (\>\n"
        ARCH_BODY += "A => delay_tally(%i downto %i),\n"%(5*reg + 4, 5*reg)

        # Handle the specail case of the first SRL
        if reg == 0:
            ARCH_BODY += "D => delay_in,\n"
        else:
            ARCH_BODY += "D => delay_reg_%i_out,\n"%(reg - 1)

        ARCH_BODY += "Q => delay_reg_%i_out,\n"%(reg)
        ARCH_BODY += "CLK => clock,\n"
        ARCH_BODY += "CE => delay_clock_enable,\n"
        ARCH_BODY += "Q31 => open\n"
        ARCH_BODY += "\<);\n\<\n"

    # Connect final reg to delay out
    ARCH_BODY += "delay_out <=  delay_reg_%i_out;\n"%(reg)
