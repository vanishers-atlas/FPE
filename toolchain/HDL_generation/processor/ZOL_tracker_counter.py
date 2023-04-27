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

    # Check and preprocess parameters
    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"

    config = preprocess_config(config)
    module_name = handle_module_name(module_name, config)

    # Combine parameters into generation_details class for easy passing to functons
    gen_det = gen_utils.generation_details(config, output_path, module_name, concat_naming, force_generation)

    # Load return variables from pre-existing file if allowed and can
    try:
        return gen_utils.load_files(gen_det)
    except gen_utils.FilesInvalid:
        # Init component_details
        com_det = gen_utils.component_details()

        com_det.add_port("clock", "std_logic", "in")
        com_det.add_port("PC_running", "std_logic", "in")
        com_det.add_port("match_found", "std_logic", "in")
        com_det.add_port("overwrites_reached", "std_logic", "out")

        com_det.add_interface_item("overwrites_encoding",
            {
                "type"  : "unsigned",
                "width" : gen_det.config["bits"]
            }
        )

        # Include required libs
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_import("ieee", "numeric_std", "all")
        com_det.add_import("UNISIM", "vcomponents", "all")

        # Generation Module Code
        generate_state_machine(gen_det, com_det)
        generate_overwrites_value(gen_det, com_det)
        generate_counter_reg(gen_det, com_det)
        generate_decrementer(gen_det, com_det)
        generate_overwrites_reached(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_state_machine(gen_det, com_det):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_FSM"
    else:
        module_name = None

    sub_interface, sub_name = ZOL_setup_pulse_FSM.generate_HDL(
        {},
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "state_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    assert len(sub_interface["generics"]) == 0
    # com_det.arch_body += "generic map ()\n"

    assert len(sub_interface["ports"]) == 5
    assert "clock" in sub_interface["ports"]
    assert "match_found" in sub_interface["ports"]
    assert "overwrites_reached" in sub_interface["ports"]
    assert "setup" in sub_interface["ports"]
    assert "setup" in sub_interface["ports"]
    assert "PC_running" in sub_interface["ports"]

    com_det.arch_body += "port map (\n\>"

    com_det.arch_head += "signal setup : std_logic;\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "match_found  => match_found,\n"
    com_det.arch_body += "overwrites_reached => overwrites_reached_int,\n"
    com_det.arch_body += "PC_running  => PC_running,\n"
    com_det.arch_body += "setup  => setup\n"

    com_det.arch_body += "\<);\n\<\n"


def generate_overwrites_value(gen_det, com_det):
    if not gen_det.config["settable"]:
        # overwrites is fixeds therefore use generic
        com_det.add_generic("overwrites", "std_logic_vector", gen_det.config["bits"])
    else:
        # overwrites is settable therefore use registor and port
        com_det.add_port("set_overwrites", "std_logic_vector", "in", gen_det.config["bits"])
        com_det.add_port("set_enable", "std_logic", "in")

        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force"  : False,
                "has_sync_force"   : False,
                "has_enable"    : True,
                "force_on_init" : False
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        com_det.arch_body += "-- overwrites register\n"

        com_det.arch_body += "overwrites_reg : entity work.%s(arch)\>\n"%(reg_name, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["bits"], )

        com_det.arch_body += "port map (\n\>"

        if not gen_det.config["stallable"]:
            com_det.arch_body += "enable => set_enable,\n"
        else:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_body += "enable => set_enable and not stall_in,\n"

        com_det.arch_body += "clock => clock,\n"
        com_det.arch_body += "data_in  => set_overwrites,\n"

        com_det.arch_head += "signal overwrites : std_logic_vector(%i downto 0);\n"%(gen_det.config["bits"] - 1)
        com_det.arch_body += "data_out => overwrites\n"

        com_det.arch_body += "\<);\n\<\n"


def generate_counter_reg(gen_det, com_det):
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "-- counter register\n"

    com_det.arch_body += "counter_reg : entity work.%s(arch)\>\n"%(reg_name, )

    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["bits"], )

    com_det.arch_body += "port map (\n\>"

    com_det.arch_head += "signal curr_count, next_count : std_logic_vector(%i downto 0);\n"%(gen_det.config["bits"] - 1)

    com_det.arch_body += "clock => clock,\n"
    if not gen_det.config["settable"]:
        com_det.arch_body += "enable => match_found or setup,\n"
    else:
        com_det.arch_body += "enable => match_found or setup or set_enable,\n"
    com_det.arch_body += "data_in  => next_count,\n"
    com_det.arch_body += "data_out => curr_count\n"

    com_det.arch_body += "\<);\n\<\n"

    mux_interface, mux_name = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "-- Mux next_count\n"

    com_det.arch_body += "next_count_mux : entity work.%s(arch)\>\n"%(mux_name, )

    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["bits"], )

    com_det.arch_body += "port map (\n\>"

    com_det.arch_body += "sel(0)    => setup,\n"
    com_det.arch_body += "data_in_0 => decremented_count,\n"
    com_det.arch_body += "data_in_1 => overwrites,\n"
    if not gen_det.config["settable"]:
        com_det.arch_body += "data_out  => next_count\n"
    else:
        com_det.arch_head += "signal next_count_int : std_logic_vector(%i downto 0);\n"%(gen_det.config["bits"] - 1)

        com_det.arch_body += "data_out  => next_count_int\n"

    com_det.arch_body += "\<);\n\<\n"

    if gen_det.config["settable"]:
        com_det.arch_body += "next_count_int_mux : entity work.%s(arch)\>\n"%(mux_name, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["bits"], )

        com_det.arch_body += "port map (\n\>"

        com_det.arch_body += "sel(0)    => set_enable,\n"
        com_det.arch_body += "data_in_0 => next_count_int,\n"
        com_det.arch_body += "data_in_1 => set_overwrites,\n"
        com_det.arch_body += "data_out  => next_count\n"

        com_det.arch_body += "\<);\n\<\n"




def generate_decrementer(gen_det, com_det):
    com_det.arch_body += "-- decrementer\n"
    com_det.arch_head += "signal decremented_count  : std_logic_vector(%i downto 0);\n"%(gen_det.config["bits"] - 1, )
    com_det.arch_body += "decremented_count <= std_logic_vector(to_unsigned(to_integer(unsigned(curr_count)) - 1, %i));\n\n"%(gen_det.config["bits"], )


def generate_overwrites_reached(gen_det, com_det):
    com_det.arch_body += "-- Generate overwrites_reached\n"
    com_det.arch_head += "signal overwrites_reached_int : std_logic;\n"

    com_det.arch_body += "overwrites_reached_int <= '1' when to_integer(unsigned(curr_count)) = 0 else '0';\n\n"
    com_det.arch_body += "overwrites_reached <=  overwrites_reached_int;\n"
