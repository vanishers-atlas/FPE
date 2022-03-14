# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))


import math

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.processor import ZOL_inverted_SR_FSM

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SET":
                raise ValueError("Cascade tracker doesn't support ZOL_SET instructions")
            elif mnemonic in ["ZOL_SEEK", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)

    return config


def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    return pathways


def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}


    assert "overwrites" in config_in.keys(), "Passed config lacks overwrites key"
    assert type(config_in["overwrites"]) is  int, "overwrites must in an integer"
    assert config_in["overwrites"] > 0, "overwrites mst be greater than 0"

    config_out["overwrites"] = config_in["overwrites"]

    config_out["cascades"] = max(1, math.ceil(math.log(config_in["overwrites"], 32)))

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL_tracker_cascade"

        # Add max overwrites
        generated_name += "_%i"%(32**(config["cascades"]) - 1, )

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name=None, concat_naming=False, force_generation=False):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, config)
    CONCAT_NAMING = concat_naming
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
            "generics" : {
                "overwrites" : {
                    "type" : "std_logic_vector",
                    "width": 5*CONFIG["cascades"],
                },
            },
            "ports" : {
                "clock" : {
                    "type" : "std_logic",
                    "direction" : "in",
                },
                "match_found" : {
                    "type" : "std_logic",
                    "direction" : "in",
                },
                "overwrites_reached" : {
                    "type" : "std_logic",
                    "direction" : "out",
                },
            },
            "overwrites_encoding" : {
                "type"  : "unsigned",
                "width" : 5*CONFIG["cascades"]
            }
        }

        # Include required libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
            {
                "library" : "UNISIM",
                "package" : "vcomponents",
                "parts" : "all"
            },
        ]


        # Generation Module Code
        generate_state_machine()
        generate_stepdown_SRLs()
        generate_counter_SRLs()
        generate_overwrites_reached_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_state_machine():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_FSM"
    else:
        module_name = None

    sub_interface, sub_name = ZOL_inverted_SR_FSM.generate_HDL(
        {},
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "state_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    assert len(sub_interface["generics"]) == 0
    # ARCH_BODY += "generic map ()\n"

    assert len(sub_interface["ports"]) == 4
    assert "clock" in sub_interface["ports"].keys()
    assert "match_found" in sub_interface["ports"].keys()
    assert "not_tracking" in sub_interface["ports"].keys()
    assert "overwrites_reached" in sub_interface["ports"].keys()

    ARCH_BODY += "port map (\n\>"

    ARCH_HEAD += "signal not_tracking : std_logic;\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "match_found  => match_found,\n"
    ARCH_BODY += "overwrites_reached => overwrites_reached_int,\n"
    ARCH_BODY += "not_tracking  => not_tracking\n"

    ARCH_BODY += "\<);\n\<\n"


def generate_stepdown_SRLs():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- Cascade Iteration Tracker Stepdown Ladder\n"

    # Handle Cascade stepdown ladder
    ARCH_HEAD += "signal stepdown_0 : std_logic;\n"
    ARCH_BODY += "stepdown_0 <= match_found;\n\n"

    for rang in range(CONFIG["cascades"] - 1):
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
                for c in range(rang + 1, CONFIG["cascades"])
            ])
        )

        # Process SRL output into stepdown
        ARCH_HEAD += "signal stepdown_%i : std_logic;\n"%(rang + 1, )
        ARCH_BODY += "stepdown_%i <= stepdown_SRL_%i_out and stepdown_%i;\n\n"%(rang + 1, rang, rang)


def generate_counter_SRLs():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle Cascade counters
    ARCH_BODY += "-- Cascade Iteration Tracker Counters\n"

    for counter in range(CONFIG["cascades"]):
          # Instantiate SRL for stepping down one stepdown to next
          ARCH_BODY += "counter_SRL_%i : SRLC32E\>\n"%(counter, )

          ARCH_BODY += "generic map ( init => X\"00000001\")\n"

          ARCH_BODY += "port map (\>\n"

          ARCH_BODY += "A => overwrites(%i downto %i),\n"%(5*counter + 4, 5*counter)

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
          ARCH_BODY += "counter_SRL_%i_enable <= (\n\>(counter_SRL_%i_out and not_tracking)\n"%(counter, counter, )
          ARCH_BODY += "or (stepdown_%i and not counter_SRL_%i_out"%(counter, counter,)
          # Add all higher order counters to enable,
          if counter + 1 < CONFIG["cascades"]:
               ARCH_BODY += " and %s"%(
                " and ".join([
                    "counter_SRL_%i_out"%(c, )
                    for c in range(counter + 1, CONFIG["cascades"])
                ])
              )
          ARCH_BODY += ")\<\n);\n\n"


def generate_overwrites_reached_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate overwrites_reached
    # Connect output of final SRLC32E to overwrites_reached
    ARCH_BODY += "-- Cascade Iteration Tracker overwrites_reached computation\n"
    ARCH_HEAD += "signal overwrites_reached_int : std_logic;\n"

    ARCH_BODY += "overwrites_reached_int <= (%s);\n\n"%(
        " and ".join([
            "counter_SRL_%i_out"%(c, )
            for c in range(CONFIG["cascades"])
        ])
    )
    ARCH_BODY += "overwrites_reached <=  overwrites_reached_int;\n"
