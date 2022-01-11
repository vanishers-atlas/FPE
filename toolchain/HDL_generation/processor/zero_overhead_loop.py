# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import math

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.basic import register

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["PC_width"] > 0)
    config_out["PC_width"] = config_in["PC_width"]

    assert(type(config_in["seekable"]) == type(True))
    config_out["seekable"] = config_in["seekable"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    assert(config_in["iterations"] > 0)
    config_out["tracker_type"] = config_in["tracker_type"]
    if   config_in["tracker_type"] == "ripple":
        config_out["tracker_ripples"] = tc_utils.biased_tally.width(
            config_in["iterations"],
            SRL_BAIS,
            SRL_RANGE
        )
        config_out["iterations_encoding"] = {
            "type"      : "biased_tally",
            "bias"      : SRL_BAIS,
            "range"     : SRL_RANGE,
            "tallies"   : config_out["tracker_ripples"]
        }
        config_out["iterations"] = 32*config_out["tracker_ripples"]
    elif config_in["tracker_type"] == "cascade":
        config_out["tracker_cascades"] = max(1, math.ceil(math.log(config_in["iterations"], 32)))

        config_out["iterations_encoding"] = {
            "type"  : "unsigned",
            "width" : 5*config_out["tracker_cascades"]
        }
        config_out["iterations"] = 32**(config_out["tracker_cascades"]) - 1
    elif config_in["tracker_type"] == "counter":
        config_out["tracker_bits"] = max(1, math.ceil(math.log(config_in["iterations"], 2)))
        config_out["iterations_encoding"] = {
            "type"  : "unsigned",
            "width" : config_out["tracker_bits"]
        }
        config_out["iterations"] = 2**(config_out["tracker_bits"]) - 1

        assert(type(config_in["settable"]) == type(True))
        config_out["settable"] = config_in["settable"]
    else:
        raise ValueError("Unknown tracker_type, " + str(config_in["tracker_type"]))

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = "ZOL"

        # Include behavour flags
        generated_name += "_"

        if config["seekable"]:  generated_name += "S"
        else:                   generated_name += "F"

        if config["stallable"]: generated_name += "S"
        else:                   generated_name += "N"


        # Include delay type and max inter
        generated_name += "_" + str(config["PC_width"])
        generated_name += "_" + config["tracker_type"]
        generated_name += "_" + str(config["iterations"])

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
        INTERFACE = {
            "ports" : [ ],
            "generics" : [ ],
            "iterations_encoding" : CONFIG["iterations_encoding"]
        }

        # Include global libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Setup global ports
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]
        if CONFIG["stallable"]:
            INTERFACE["ports"] += [
                {
                    "name" : "stall",
                    "type" : "std_logic",
                    "direction" : "in"
                },
            ]

        # Generation Module Code
        generate_PC_interface()
        generate_state_management()
        generate_tracker()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_PC_interface():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle Start/end values
    ARCH_HEAD += "signal start_value_int : std_logic_vector(%i downto 0);\n"%(CONFIG["PC_width"] - 1, )
    ARCH_HEAD += "signal end_value_int   : std_logic_vector(%i downto 0);\n\n"%(CONFIG["PC_width"] - 1, )

    if not CONFIG["seekable"]:
        # ZOL is not seekable therefore start/end values are fixed, therefore use generics
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

        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts" : "all"
            }
        ]

        ARCH_BODY += "-- Handle start value\n"
        ARCH_BODY += "start_value_int <=  std_logic_vector(to_unsigned(start_value, %i));\n\n"%(CONFIG["PC_width"], )

        ARCH_BODY += "-- Handle end value\n"
        ARCH_BODY += "end_value_int <=  std_logic_vector(to_unsigned(end_value, %i));\n\n"%(CONFIG["PC_width"], )
    else:
        # ZOL is seekable, ie start/end values are variable, therefore use registors and ports
        INTERFACE["ports"] += [
            {
                "name" : "in_0",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
                "direction" : "in"
            },
            {
                "name" : "in_1",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
                "direction" : "in"
            },
            {
                "name" : "seek",
                "type" : "std_logic",
                "direction" : "in"
            },
        ]

        interface, reg = register.generate_HDL(
            {
                "has_async_forces"  : False,
                "has_sync_forces"   : False,
                "has_enable"    : True
            },
            OUTPUT_PATH,
            "register",
            True,
            False
        )

        ARCH_BODY += "-- Handle start value\n"

        ARCH_BODY += "start_value_reg : entity work.%s(arch)\>\n"%(reg, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["PC_width"], )

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => seek,\n"
        else:
            ARCH_BODY += "enable => seek and not stall,\n"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => in_0(%i downto 0),\n"%(CONFIG["PC_width"] - 1, )
        ARCH_BODY += "data_out => start_value_int\n"

        ARCH_BODY += "\<);\n\<\n"


        ARCH_BODY += "-- Handle end value\n"

        ARCH_BODY += "end_value_reg : entity work.%s(arch)\>\n"%(reg, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["PC_width"], )

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => seek,\n"
        else:
            ARCH_BODY += "enable => seek and not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => in_1(%i downto 0),\n"%(CONFIG["PC_width"] - 1, )
        ARCH_BODY += "data_out => end_value_int\n"

        ARCH_BODY += "\<);\n\<\n"

    # Handle PC_checking
    INTERFACE["ports"] += [
        {
            "name" : "PC_value",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
            "direction" : "in"
        },
        {
            "name" : "PC_running",
            "type" : "std_logic",
            "direction" : "in"
        },
    ]

    ARCH_BODY += "-- Check if PC matches end Value\n"
    ARCH_HEAD += "signal end_found : std_logic;\n"

    if not CONFIG["stallable"]:
        ARCH_BODY += "end_found <= '1' when PC_running = '1' and PC_value = end_value_int else '0';\n\n"
    else:
        ARCH_BODY += "end_found <= '1' when stall /= '1' and PC_running = '1' and PC_value = end_value_int else '0';\n\n"


    # Handle PC_overwrite
    INTERFACE["ports"] += [
        # Declare PC interface ports
        {
            "name" : "overwrite_value",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1, ),
            "direction" : "out"
        },
        {
            "name" : "overwrite",
            "type" : "std_logic",
            "direction" : "out",
        },
    ]

    # Handle PC overwriting
    ARCH_HEAD += "signal overwrite_int : std_logic;\n\n"

    ARCH_BODY += "-- Handle overwriting of PC\n"
    ARCH_BODY += "overwrite_int <= end_found and not iterations_reached;\n\n"

    ARCH_BODY += "overwrite <= '1' when overwrite_int = '1' else 'Z';\n"
    ARCH_BODY += "overwrite_value <= start_value_int when overwrite_int = '1' else (others => 'Z');\n\n"

def generate_state_management():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "-- State signal values\n"
    ARCH_HEAD += "-- '1' : Not Work/Setup\n"
    ARCH_HEAD += "-- '0' : RUNNING\n"
    ARCH_HEAD += "signal curr_state, next_state : std_logic := '1';\n\n"

    ARCH_BODY += "-- State Buffering\n"
    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) and end_found = '1' then\>\n"
    ARCH_BODY += "curr_state <= next_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"

    ARCH_BODY += "-- next_state computing\n"
    ARCH_BODY += "next_state <=\> '0' when curr_state = '1' and end_found = '1'\n"
    ARCH_BODY += "else '1' when curr_state = '0' and iterations_reached = '1'\n"
    ARCH_BODY += "else curr_state;\<\n\n"


#####################################################################

def generate_tracker():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "signal iterations_reached : std_logic;\n\n"

    ARCH_BODY += "-- Handle iteration tracking\n"

    if   CONFIG["tracker_type"] == "ripple":
        generate_tracker_ripple()
    elif CONFIG["tracker_type"] == "cascade":
        generate_tracker_cascade()
    elif CONFIG["tracker_type"] == "counter":
        generate_tracker_counter()
    else:
        raise ValueError("Unknown tracker_type, " + str(config_in["tracker_type"]))

SRL_BAIS  = 1
SRL_RANGE = 31

def generate_tracker_ripple():
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
            "name" : "iterations",
            "type" : "std_logic_vector(%i downto 0)"%(5*CONFIG["tracker_ripples"] - 1),
        },
    ]

    ARCH_BODY += "-- Ripple iteration tracker\n"

    # Generate ripple chain of SRLC32Es
    for ripple in range(CONFIG["tracker_ripples"]):
        ARCH_HEAD += "signal ripple_%i_out : std_logic;\n"%(ripple, )

        ARCH_BODY += "ripple_%i : SRLC32E\n\>"%(ripple)
        ARCH_BODY += "generic map (INIT => X\"00000000\")\n"
        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "A => iterations(%i downto %i),\n"%(5*ripple + 4, 5*ripple)

        # Handle the specail case of the first SRL
        if ripple == 0:
            ARCH_BODY += "D => curr_state,\n"
        else:
            ARCH_BODY += "D => ripple_%i_out,\n"%(ripple - 1)

        ARCH_BODY += "Q => ripple_%i_out,\n"%(ripple)
        ARCH_BODY += "CLK => clock,\n"
        ARCH_BODY += "CE => end_found,\n"
        ARCH_BODY += "Q31 => open\n"
        ARCH_BODY += "\<);\n\<\n"

    # Connect output of final SRLC32E to iterations_reached
    ARCH_BODY += "iterations_reached <=  ripple_%i_out;\n"%(CONFIG["tracker_ripples"] - 1)

def generate_tracker_cascade():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [
        {
            "library" : "UNISIM",
            "package" : "vcomponents",
            "parts" : "all"
        },
    ]

    ARCH_BODY += "-- Cascade Iteration Tracker Stepdown Ladder\n"

    # Handle Cascade stepdown ladder
    ARCH_HEAD += "signal stepdown_0 : std_logic;\n"
    ARCH_BODY += "stepdown_0 <= end_found;\n\n"

    for rang in range(CONFIG["tracker_cascades"] - 1):
        # Instantiate SRL for stepping down one stepdown to next
        ARCH_BODY += "stepdown_SRL_%i : SRLC32E\>\n"%(rang, )

        ARCH_BODY += "generic map ( init => X\"00000001\")\n"

        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "A => \"11111\",\n"

        ARCH_HEAD += "signal stepdown_SRL_%i_out : std_logic;\n"%(rang, )
        ARCH_BODY += "D => stepdown_SRL_%i_out,\n"%(rang, )

        ARCH_BODY += "Q => open,\n"
        ARCH_BODY += "Q31 => stepdown_SRL_%i_out,\n"%(rang, )

        ARCH_BODY += "clk =>clock,\n"

        ARCH_HEAD += "signal stepdown_SRL_%i_enable : std_logic := '0';\n"%(rang, )
        ARCH_BODY += "ce => stepdown_SRL_%i_enable,\n"%(rang, )

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\n\<);\<\n\n"

        # Generate SRL enable signal
        ARCH_BODY += "stepdown_SRL_%i_enable <= stepdown_%i and not (%s);\n\n"%(
            rang, rang,
            " and ".join([
                "counter_SRL_%i_out"%(c, )
                for c in range(rang + 1, CONFIG["tracker_cascades"])
            ])
        )

        # Process SRL output into stepdown
        ARCH_HEAD += "signal stepdown_%i : std_logic;\n"%(rang + 1, )
        ARCH_BODY += "stepdown_%i <= stepdown_SRL_%i_out and stepdown_%i;\n\n"%(rang + 1, rang, rang)

    # Handle Cascade counters
    ARCH_BODY += "-- Cascade Iteration Tracker Counters\n"

    INTERFACE["generics"] += [
        {
            "name" : "iterations",
            "type" : "std_logic_vector(%i downto 0)"%(5*CONFIG["tracker_cascades"] - 1),
        },
    ]

    for counter in range(CONFIG["tracker_cascades"]):
          # Instantiate SRL for stepping down one stepdown to next
          ARCH_BODY += "counter_SRL_%i : SRLC32E\>\n"%(counter, )

          ARCH_BODY += "generic map ( init => X\"00000001\")\n"

          ARCH_BODY += "port map (\>\n"

          ARCH_BODY += "A => iterations(%i downto %i),\n"%(5*counter + 4, 5*counter)

          ARCH_HEAD += "signal counter_SRL_%i_out : std_logic;\n"%(counter, )
          ARCH_BODY += "Q => counter_SRL_%i_out,\n"%(counter, )
          ARCH_BODY += "D => counter_SRL_%i_out,\n"%(counter, )

          ARCH_BODY += "Q31 => open,\n"

          ARCH_BODY += "clk =>clock,\n"

          ARCH_HEAD += "signal counter_SRL_%i_enable : std_logic := '0';\n"%(counter, )
          ARCH_BODY += "ce => counter_SRL_%i_enable,\n"%(counter, )

          ARCH_BODY.drop_last_X(2)
          ARCH_BODY += "\n\<);\<\n\n"

          # Generate SRL enable signal
          ARCH_BODY += "counter_SRL_%i_enable <= (\n\>(counter_SRL_%i_out and curr_state)\n"%(counter, counter, )
          ARCH_BODY += "or (stepdown_%i and not counter_SRL_%i_out"%(counter, counter,)
          # Add all higher order counters to enable,
          if counter + 1 < CONFIG["tracker_cascades"]:
               ARCH_BODY += " and %s"%(
                " and ".join([
                    "counter_SRL_%i_out"%(c, )
                    for c in range(counter + 1, CONFIG["tracker_cascades"])
                ])
              )
          ARCH_BODY += ")\<\n);\n\n"

    # Generate iterations_reached
    ARCH_BODY += "-- Cascade Iteration Tracker iterations_reached computation\n"

    ARCH_BODY += "iterations_reached <= (%s);\n\n"%(
        " and ".join([
            "counter_SRL_%i_out"%(c, )
            for c in range(CONFIG["tracker_cascades"])
        ])
    )

def generate_tracker_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, reg = register.generate_HDL(
        {
            "has_async_forces"  : False,
            "has_sync_forces"   : False,
            "has_enable"    : True
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    # Instancate count register
    ARCH_BODY += "-- Counter Iteration Tracker Counter Reg\n"
    ARCH_HEAD += "signal count_reg_in  : std_logic_vector(%i downto 0);\n"%(CONFIG["tracker_bits"] - 1, )
    ARCH_HEAD += "signal count_reg_out : std_logic_vector(%i downto 0);\n"%(CONFIG["tracker_bits"] - 1, )

    ARCH_BODY += "count_reg : entity work.%s(arch)\>\n"%(reg, )

    ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["tracker_bits"], )

    ARCH_BODY += "port map (\n\>"

    if not CONFIG["stallable"]:
        ARCH_BODY += "enable => end_found,\n"
    else:
        ARCH_BODY += "enable => end_found and not stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => count_reg_in,\n"
    ARCH_BODY += "data_out => count_reg_out\n"

    ARCH_BODY += "\<);\n\<\n"

    # Generation count reset value
    if not CONFIG["settable"]:
        INTERFACE["generics"] += [
            {
                "name" : "iterations",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["tracker_bits"] - 1, ),
            }
        ]
    else:
        INTERFACE["ports"] += [
            {
                "name" : "set",
                "type" : "std_logic",
                "direction" : "in",
            },
        ]
        # Check in in_0 has already been been declared
        in_0 = [port for port in INTERFACE["ports"] if port["name"] == "in_0"]
        assert(len(in_0) < 2)
        # In_o not declared so declare as normal
        if len(in_0) == 0:
            INTERFACE["ports"] += [
                {
                    "name" : "in_0",
                    "type" : "std_logic_vector(%i downto 0)"%(CONFIG["tracker_bits"] - 1, ),
                    "direction" : "in",
                }
            ]
        # In_o already declared therefore check if it needs e expanding
        else:
            in_0_width = int(in_0[0]["type"].split("(")[1].split("downto")[0]) + 1
            if CONFIG["tracker_bits"] > in_0_width:
                in_0[0]["type"] = "std_logic_vector(%i downto 0)"%(CONFIG["tracker_bits"] - 1, ),

        ARCH_BODY += "-- Counter Iteration Tracker Reset Value Reg\n"
        ARCH_HEAD += "signal iterations : std_logic_vector(%i downto 0);\n"%(CONFIG["tracker_bits"] - 1, )

        ARCH_BODY += "iterations_reg : entity work.%s(arch)\>\n"%(reg, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["tracker_bits"], )

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => set,\n"
        else:
            ARCH_BODY += "enable => set and not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => in_0(%i downto 0),\n"%(CONFIG["tracker_bits"] - 1, )
        ARCH_BODY += "data_out => iterations\n"

        ARCH_BODY += "\<);\n\<\n"

    # Generation count decrement
    ARCH_BODY += "-- Counter Iteration Tracker Decrement\n"
    ARCH_HEAD += "signal decrement_in  : std_logic_vector(%i downto 0);\n"%(CONFIG["tracker_bits"] - 1, )
    ARCH_HEAD += "signal decrement_out : std_logic_vector(%i downto 0);\n"%(CONFIG["tracker_bits"] - 1, )

    IMPORTS += [
        {
            "library" : "ieee",
            "package" : "numeric_std",
            "parts"   : "all"
        }
    ]

    ARCH_BODY += "decrement_out <= std_logic_vector(to_unsigned(to_integer(unsigned(decrement_in)) - 1, %i));\n\n"%(CONFIG["tracker_bits"], )

    # Connect up parts and generate iterations_reached
    if not CONFIG["settable"]:
        ARCH_BODY += "-- Connect reg, decrement and reset value\n"
        ARCH_BODY += "-- As iterations is predecremented (when the generic is set)\n"
        ARCH_BODY += "-- While state is idle/setip count_reg_in is set to it\n"
        ARCH_BODY += "count_reg_in <= iterations when curr_state = '1' else decrement_out;\n"
        ARCH_BODY += "decrement_in <= count_reg_out;\n\n"
    else:
        ARCH_BODY += "-- Connect reg, decrement and reset value\n"
        ARCH_BODY += "-- While state is idle/setip decrement_in is set to iterations\n"
        ARCH_BODY += "-- Saving the programmer from having to predecremented iterations_in\n"
        ARCH_BODY += "-- While mantions that writing X to iterations_in yields X iterations\n"
        ARCH_BODY += "count_reg_in <= decrement_out;\n"
        ARCH_BODY += "decrement_in <= iterations when curr_state = '1' else count_reg_out;\n\n"

    ARCH_BODY += "-- Generate iterations_reached\n"
    ARCH_BODY += "iterations_reached <= '1' when to_integer(unsigned(count_reg_in)) = 0 else '0';\n\n"


#####################################################################

if __name__ == "__main__":
    generate_HDL(
        {
            "PC_width" : 5,
            "tracker_type" : "counter",
            "iterations" : 21,
            "stallable" : False,
            "seekable"  : False,
            "settable" : False,
        },
        ".",
        "test_ZOL",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "PC_width" : 5,
            "tracker_type" : "counter",
            "iterations" : 61,
            "stallable" : False,
            "seekable"  : False,
            "settable" : False,
        },
        ".",
        "test_ZOL",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "PC_width" : 5,
            "tracker_type" : "counter",
            "iterations" : 1301,
            "stallable" : False,
            "seekable"  : False,
            "settable" : False,
        },
        ".",
        "test_ZOL",
        generate_name=True,
        force_generation=True
    )
