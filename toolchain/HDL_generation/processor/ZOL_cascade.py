# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import math

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["PC_width"] > 0)
    config_out["PC_width"] = config_in["PC_width"]

    # Handle delay regs and delay encoding
    assert(config_in["count"] > 0)
    config_out["counters"] = math.ceil(math.log(config_in["count"], 32))

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = "ZOL_cascade"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%iw"%(config["PC_width"])
        generated_name += "_%ib"%(5 * CONFIG["counters"])

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
            "ports" : [
                { "name" : "clock"  , "type" : "std_logic", "direction" : "in" },
            ],
            "generics" : [

            ],
            "delay_encoding" : {
                "type" : "unsigned",
                "bits" : 5 * CONFIG["counters"],
            }
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
            {
                "library" : "unisim",
                "package" : "vcomponents",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        generate_PC_interface()
        generate_state_logic()
        generate_stepdown_ladder()
        generate_count_trackers()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_PC_interface():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [
        {"library" : "ieee"  , "package" : "numeric_std"   , "parts" : "all"}
    ]

    INTERFACE["generics"] += [
        { "name" : "start_value", "type" : "integer := 0", },
        { "name" : "end_value", "type" : "integer := 0", },
    ]

    port_width = CONFIG["PC_width"]
    INTERFACE["ports"] += [
        { "name" : "PC_running", "type" : "std_logic", "direction" : "in" },
        { "name" : "value_in" , "type" : f"std_logic_vector({port_width - 1} downto 0)", "direction" : "in" },
        { "name" : "value_out", "type" : f"std_logic_vector({port_width - 1} downto 0)", "direction" : "out" },
        { "name" : "overwrite", "type" : "std_logic", "direction" : "out" },
    ]

    ARCH_BODY += "-- Check PC value against key values\n"
    ARCH_HEAD += "signal start_found : std_logic;\n"
    ARCH_BODY += "start_found <= '1' when PC_running = '1' and start_value = to_integer(unsigned(value_in)) else '0';\n"
    ARCH_HEAD += "signal end_found : std_logic;\n"
    ARCH_BODY += "end_found   <= '1' when PC_running = '1' and end_value = to_integer(unsigned(value_in)) else '0';\n\n"

    ARCH_BODY += "-- Output overwrite signals\n"
    ARCH_BODY += "value_out <= std_logic_vector(to_unsigned(start_value, value_out'length)) when end_found = '1' else (others => 'Z');\n"
    ARCH_BODY += "overwrite <= '1' when curr_state = ACTIVE and end_found = '1' else 'Z';\n\n"


def generate_state_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    possible_states = ", ".join([ "INACTIVE", "ACTIVE", "RELOAD", "LAST_PASS" ])
    ARCH_HEAD += f"type tracker_state is ({possible_states});\n"

    ARCH_HEAD += "signal last_state : tracker_state := INACTIVE;\n"
    ARCH_HEAD += "signal curr_state : tracker_state;\n"

    ARCH_BODY += "-- Store state for next clock cycle\n"
    ARCH_BODY += "process (clock)\>\n"
    ARCH_BODY += "\<begin\>\n"
    ARCH_BODY += "if rising_edge(clock) then\>\n"
    ARCH_BODY += "last_state <= curr_state;\n"
    ARCH_BODY += "\<end if;\n"
    ARCH_BODY += "\<end process;\n\n"


    ARCH_BODY += "-- Generate curr state this clock cycle, different tables for single amd multi instruction bodies\n"

    ARCH_BODY += "SINGLE_INST_BODY : if start_value = end_value generate \>\n"

    ARCH_BODY += "curr_state <=\>ACTIVE when last_state = INACTIVE and start_found = '1'\n"
    ARCH_BODY += "else RELOAD when last_state = ACTIVE and count_reached_0 = '1'\n"
    ARCH_BODY += "else INACTIVE  when last_state = RELOAD\n"
    ARCH_BODY += "else last_state;\n\<\n"

    ARCH_BODY += "\<end generate SINGLE_INST_BODY;\n"

    ARCH_BODY += "MULTI_INST_BODY : if start_value /= end_value generate \>\n"

    ARCH_BODY += "curr_state <=\>ACTIVE when last_state = INACTIVE and start_found = '1'\n"
    ARCH_BODY += "else RELOAD when last_state = ACTIVE and count_reached_0 = '1'\n"
    ARCH_BODY += "else LAST_PASS when last_state = RELOAD\n"
    ARCH_BODY += "else INACTIVE  when last_state = LAST_PASS and end_found = '1'\n"
    ARCH_BODY += "else last_state;\n\<\n"

    ARCH_BODY += "\<end generate MULTI_INST_BODY;\n\n"


#####################################################################

def generate_stepdown_ladder():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    stepdown_rangs = CONFIG["counters"] - 1

    ARCH_BODY += "-- Peroid_0 is the input tcik, therefoe just assign to signal\n"
    ARCH_HEAD += f"signal peroid_0: std_logic;\n"
    ARCH_BODY += f"peroid_0 <= end_found;\n\n"

    for rang in range(stepdown_rangs):
        comp = f"stepdown_{rang}"

        ARCH_BODY += f"-- Peroid_{rang + 1} is stepdowned down form peroid_{rang}, therefore use an stepdown rang\n"

        # Generate controls for stepdown SRL
        ARCH_HEAD += f"signal peroid_{rang + 1}_needed : std_logic;\n"
        ARCH_BODY += f"{comp}_enable <= peroid_{rang} and peroid_{rang + 1}_needed when curr_state = ACTIVE else '0';\n"

        # Instantiate SRL for converting else period to next
        ARCH_BODY += f"{comp} : SRLC32E\>\n"

        ARCH_BODY += "generic map ( init => X\"00000001\")\n"

        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "A => \"11111\",\n"

        ARCH_HEAD += f"signal {comp}_out : std_logic;\n"
        ARCH_BODY += f"D => {comp}_out,\n"

        ARCH_BODY += "Q => open,\n"
        ARCH_BODY += f"Q31 => {comp}_out,\n"

        ARCH_BODY += "clk =>clock,\n"

        ARCH_HEAD += f"signal {comp}_enable : std_logic := '0';\n"
        ARCH_BODY += f"ce => {comp}_enable,\n"

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\n\<);\<\n"

        # Process output from stepdown SRL into peroid signal
        ARCH_HEAD += f"signal peroid_{rang + 1}: std_logic;\n"
        ARCH_BODY += f"peroid_{rang + 1} <= {comp}_out and peroid_{rang};\n\n"

    # Generate trackers controlled signals
    if stepdown_rangs >= 1:
        ARCH_BODY += f"-- Connecting up ladder controls to tracker outputs\n"

        last_rang = stepdown_rangs - 1
        last_tracker = last_rang + 1
        ARCH_BODY += f"peroid_{last_rang + 1}_needed <= not tracker_{last_tracker}_out;\n"

        # stepdown_rangs - 2, - 1 for zero indexing, -1 as last rang handled above
        for rang in range(stepdown_rangs - 2, -1, -1):
            tracker = rang + 1
            ARCH_BODY += f"peroid_{rang + 1}_needed <= peroid_{rang + 1}_needed or not tracker_{tracker}_out;\n"
        ARCH_BODY += "\n"

def generate_count_trackers():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- Setup shared counter data signal\n"
    ARCH_HEAD += f"signal trackers_data_in : std_logic;\n"
    ARCH_BODY += f"trackers_data_in <= '1' when curr_state = RELOAD else '0';\n\n"

    INTERFACE["generics"] += [
        {
            "name" : "count_value",
            "type" : "std_logic_vector(%i downto 0)"%(5*CONFIG["counters"] - 1),
        },
    ]

    # Handle MS count tracker
    tracker = CONFIG["counters"] -1
    period = tracker
    comp = f"tracker_{tracker}"

    ARCH_BODY += f"-- Tracker {tracker}, handles blocks of 32^{tracker}\n"

    ARCH_HEAD += f"signal {comp}_enable : std_logic;\n"
    ARCH_BODY += f"{comp}_enable <=\>peroid_{period} and not {comp}_out when curr_state = ACTIVE\n"
    ARCH_BODY += f"else '1' when curr_state = RELOAD\nelse '0';\<\n"


    ARCH_BODY += f"{comp} : SRLC32E\>\n"

    ARCH_BODY += "generic map ( init => X\"00000001\")\n"

    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "A => count_value(%i downto %i),\n"%(5*CONFIG["counters"] - 1, 5*CONFIG["counters"] - 5)

    ARCH_BODY += f"D => trackers_data_in,\n"

    ARCH_HEAD += f"signal {comp}_out : std_logic;\n"
    ARCH_BODY += f"Q => {comp}_out,\n"

    ARCH_BODY += "Q31 => open,\n"

    ARCH_BODY += "clk => clock,\n"

    ARCH_BODY += f"ce => {comp}_enable,\n"

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\n\<);\<\n"

    ARCH_HEAD += f"signal count_reached_{tracker} : std_logic;\n"
    ARCH_BODY += f"count_reached_{tracker} <= {comp}_out;\n\n"

    # Generate counter LUTs
    # CONFIG["counters"] - 2. -1 for zero indexing. -1 as MS tracker was handled above
    for tracker in range(CONFIG["counters"] - 2, -1, -1):
        period = tracker
        comp = f"tracker_{tracker}"

        ARCH_BODY += f"-- Tracker {tracker}, handles blocks of 32^{tracker}\n"

        ARCH_HEAD += f"signal {comp}_enable : std_logic;\n"
        ARCH_BODY += f"{comp}_enable <=\>peroid_{period} and count_reached_{tracker + 1} and not {comp}_out when curr_state = ACTIVE\n"
        ARCH_BODY += f"else '1' when curr_state = RELOAD\nelse '0';\<\n"


        ARCH_BODY += f"{comp} : SRLC32E\>\n"

        ARCH_BODY += "generic map ( init => X\"00000001\")\n"

        ARCH_BODY += "port map (\>\n"


        ARCH_BODY += "A => count_value(%i downto %i),\n"%(5*tracker + 4, 5*tracker)


        ARCH_BODY += f"D => trackers_data_in,\n"

        ARCH_HEAD += f"signal {comp}_out : std_logic;\n"
        ARCH_BODY += f"Q => {comp}_out,\n"

        ARCH_BODY += "Q31 => open,\n"

        ARCH_BODY += "clk => clock,\n"

        ARCH_BODY += f"ce => {comp}_enable,\n"

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\n\<);\<\n"

        ARCH_HEAD += f"signal count_reached_{tracker} : std_logic;\n"
        ARCH_BODY += f"count_reached_{tracker} <= {comp}_out and count_reached_{tracker + 1};\n\n"


if __name__ == "__main__":
    generate_HDL(
        {
            "width" : 3,
            "counters" : 4,
        },
        ".",
        "test_ZOL",
        generate_name=False,
        force_generation=True
    )
