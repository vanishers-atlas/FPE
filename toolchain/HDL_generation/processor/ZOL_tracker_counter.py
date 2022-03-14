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

from FPE.toolchain.HDL_generation.processor import ZOL_setup_pulse_FSM

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SET":
                config["settable"] = True
            elif mnemonic in ["ZOL_SEEK", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)

    return config


def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic = asm_utils.instr_mnemonic(instr)
            if   mnemonic == "ZOL_SET":
                gen_utils.add_datapath_dest(pathways, "%sfetch_data_0_word_0"%(lane, ), "exe", instr, instr_prefix + "set_overwrites", "unsigned", interface["ports"]["set_overwrites"]["width"])
            elif mnemonic in ["ZOL_SEEK", ]:
                pass
            else:
                raise ValueError("Unknow instr mnemonic, " + mnemonic)

    return pathways


def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    if "set_enable" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if asm_utils.instr_mnemonic(instr) == "ZOL_SET" and instr_id in asm_utils.instr_exe_units(instr):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "set_enable", values, "std_logic")

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}


    assert "overwrites" in config_in.keys(), "Passed config lacks overwrites key"
    assert type(config_in["overwrites"]) is  int, "overwrites must in an integer"
    assert config_in["overwrites"] > 0, "overwrites mst be greater than 0"

    config_out["overwrites"] = config_in["overwrites"]

    config_out["bits"] = max(1, math.ceil(math.log(config_in["overwrites"], 2)))

    assert(type(config_in["settable"]) == type(True))
    config_out["settable"] = config_in["settable"]


    assert "settable" in config_in.keys(), "Passed config lacks settable key"
    assert type(config_in["settable"]) is bool, "settable must be a boolean"

    config_out["settable"] = config_in["settable"]

    if config_out["settable"]:
        assert "stallable" in config_in.keys(), "Passed config lacks stallable key"
        assert type(config_in["stallable"]) is bool, "stallable must be a boolean"

        config_out["stallable"] = config_in["stallable"]


    return config_out


def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL_tracker_counter"

        # Add max overwrites
        generated_name += "_%i"%(2**(config["bits"]) - 1, )

        # Mark if fixed or _settable
        if config["settable"]:
            generated_name += "_settable"

            # Mark if stallable
            if config["stallable"]:
                generated_name += "_stallable"
        else:
            generated_name += "_fixed"


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
            "generics" : {},
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
                "PC_running" : {
                    "type" : "std_logic",
                    "direction" : "in",
                }
            },
            "overwrites_encoding" : {
                "type"  : "unsigned",
                "width" : CONFIG["bits"]
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
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts"   : "all"
            }
        ]


        # Generation Module Code
        generate_state_machine()
        generate_overwrites_value()
        generate_counter_reg()
        generate_decrementer()
        generate_overwrites_reached()

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

    sub_interface, sub_name = ZOL_setup_pulse_FSM.generate_HDL(
        {},
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "state_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    assert len(sub_interface["generics"]) == 0
    # ARCH_BODY += "generic map ()\n"

    assert len(sub_interface["ports"]) == 5
    assert "clock" in sub_interface["ports"]
    assert "match_found" in sub_interface["ports"]
    assert "overwrites_reached" in sub_interface["ports"]
    assert "setup" in sub_interface["ports"]
    assert "setup" in sub_interface["ports"]
    assert "PC_running" in sub_interface["ports"]

    ARCH_BODY += "port map (\n\>"

    ARCH_HEAD += "signal setup : std_logic;\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "match_found  => match_found,\n"
    ARCH_BODY += "overwrites_reached => overwrites_reached_int,\n"
    ARCH_BODY += "PC_running  => PC_running,\n"
    ARCH_BODY += "setup  => setup\n"

    ARCH_BODY += "\<);\n\<\n"


def generate_overwrites_value():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if not CONFIG["settable"]:
        # overwrites is fixeds therefore use generic
        INTERFACE["generics"]["overwrites"] = {
            "type" : "std_logic_vector",
            "width": CONFIG["bits"],
        }
    else:
        # overwrites is settable therefore use registor and port
        INTERFACE["ports"]["set_overwrites"] = {
            "type" : "std_logic_vector",
            "width": CONFIG["bits"],
            "direction" : "in",
        }
        INTERFACE["ports"]["set_enable"] = {
            "type" : "std_logic",
            "direction" : "in",
        }

        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force"  : False,
                "has_sync_force"   : False,
                "has_enable"    : True,
                "force_on_init" : False
            },
            OUTPUT_PATH,
            module_name=None,
            concat_naming=False,
            force_generation=FORCE_GENERATION
        )

        ARCH_BODY += "-- overwrites register\n"

        ARCH_BODY += "overwrites_reg : entity work.%s(arch)\>\n"%(reg_name, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["bits"], )

        ARCH_BODY += "port map (\n\>"

        if not CONFIG["stallable"]:
            ARCH_BODY += "enable => set_enable,\n"
        else:
            ARCH_BODY += "enable => set_enable and not stall,\n"
            INTERFACE["ports"]["stall"] = {
                "type" : "std_logic",
                "direction" : "in",
            }

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => set_overwrites,\n"

        ARCH_HEAD += "signal overwrites : std_logic_vector(%i downto 0);\n"%(CONFIG["bits"] - 1)
        ARCH_BODY += "data_out => overwrites\n"

        ARCH_BODY += "\<);\n\<\n"


def generate_counter_reg():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "-- counter register\n"

    ARCH_BODY += "counter_reg : entity work.%s(arch)\>\n"%(reg_name, )

    ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["bits"], )

    ARCH_BODY += "port map (\n\>"

    ARCH_HEAD += "signal curr_count, next_count : std_logic_vector(%i downto 0);\n"%(CONFIG["bits"] - 1)

    ARCH_BODY += "clock => clock,\n"
    if not CONFIG["settable"]:
        ARCH_BODY += "enable => match_found or setup,\n"
    else:
        ARCH_BODY += "enable => match_found or setup or set_enable,\n"
    ARCH_BODY += "data_in  => next_count,\n"
    ARCH_BODY += "data_out => curr_count\n"

    ARCH_BODY += "\<);\n\<\n"

    mux_interface, mux_name = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "-- Mux next_count\n"

    ARCH_BODY += "next_count_mux : entity work.%s(arch)\>\n"%(mux_name, )

    ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["bits"], )

    ARCH_BODY += "port map (\n\>"

    ARCH_BODY += "sel(0)    => setup,\n"
    ARCH_BODY += "data_in_0 => decremented_count,\n"
    ARCH_BODY += "data_in_1 => overwrites,\n"
    if not CONFIG["settable"]:
        ARCH_BODY += "data_out  => next_count\n"
    else:
        ARCH_HEAD += "signal next_count_int : std_logic_vector(%i downto 0);\n"%(CONFIG["bits"] - 1)

        ARCH_BODY += "data_out  => next_count_int\n"

    ARCH_BODY += "\<);\n\<\n"

    if CONFIG["settable"]:
        ARCH_BODY += "next_count_int_mux : entity work.%s(arch)\>\n"%(mux_name, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["bits"], )

        ARCH_BODY += "port map (\n\>"

        ARCH_BODY += "sel(0)    => set_enable,\n"
        ARCH_BODY += "data_in_0 => next_count_int,\n"
        ARCH_BODY += "data_in_1 => set_overwrites,\n"
        ARCH_BODY += "data_out  => next_count\n"

        ARCH_BODY += "\<);\n\<\n"




def generate_decrementer():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- decrementer\n"
    ARCH_HEAD += "signal decremented_count  : std_logic_vector(%i downto 0);\n"%(CONFIG["bits"] - 1, )
    ARCH_BODY += "decremented_count <= std_logic_vector(to_unsigned(to_integer(unsigned(curr_count)) - 1, %i));\n\n"%(CONFIG["bits"], )


def generate_overwrites_reached():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- Generate overwrites_reached\n"
    ARCH_HEAD += "signal overwrites_reached_int : std_logic;\n"

    ARCH_BODY += "overwrites_reached_int <= '1' when to_integer(unsigned(curr_count)) = 0 else '0';\n\n"
    ARCH_BODY += "overwrites_reached <=  overwrites_reached_int;\n"
