# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re

from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import delay

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    inputs  = 0

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            inputs = max(inputs, len(asm_utils.instr_fetches(instr)))

    config["inputs"] = inputs

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    for instr in instr_set:
        for fetch, addr_comp in enumerate([ asm_utils.addr_com(asm_utils.access_addr(fetch)) for fetch in asm_utils.instr_fetches(instr) ]):
            if addr_comp == instr_id:
                gen_utils.add_datapath_source(pathways, "%sfetch_addr_%i"%(lane, fetch), "fetch", instr, "%saddr_0_fetch"%(instr_prefix, ), "unsigned", config["addr_width"])

        for write, addr_comp in enumerate([ asm_utils.addr_com(asm_utils.access_addr(store)) for store in asm_utils.instr_stores(instr) ]):
            if addr_comp == instr_id:
                gen_utils.add_datapath_source(pathways, "%sstore_addr_%i"%(lane, write), "store", instr, "%saddr_0_store"%(instr_prefix, ), "unsigned", config["addr_width"])

        if instr_id in asm_utils.instr_exe_units(instr):
            if asm_utils.instr_mnemonic(instr) == "BAM_SEEK":
                gen_utils.add_datapath_dest(pathways, "%sfetch_data_0_word_0"%(lane, ), "exe", instr, "%sin_0"%(instr_prefix, ), "unsigned", config["step_width"])


    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle step generic forward control
    if "step_generic_forward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            accesses = asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)
            addrs = [ asm_utils.access_addr(access) for access in asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)]
            this_bam_addrs = [addr for addr in addrs if asm_utils.addr_com(addr) == instr_id]
            if len(this_bam_addrs) != 0 and any([ "FORWARD" in asm_utils.addr_mods(addr).keys() for addr in this_bam_addrs ]):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "step_generic_forward", values, "std_logic")

    # Handle step generic backwards control
    if "step_generic_backward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            accesses = asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)
            addrs = [ asm_utils.access_addr(access) for access in asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)]
            this_bam_addrs = [addr for addr in addrs if asm_utils.addr_com(addr) == instr_id]
            if len(this_bam_addrs) != 0 and any([ "BACKWARD" in asm_utils.addr_mods(addr).keys() for addr in this_bam_addrs ]):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "step_generic_backward", values, "std_logic")

    # Handle reset control
    if "reset" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if asm_utils.instr_mnemonic(instr) == "BAM_RESET" and instr_id in asm_utils.instr_exe_units(instr):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "reset", values, "std_logic")

    # Handle seek forward control
    if "step_fetched_forward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if (    asm_utils.instr_mnemonic(instr) == "BAM_SEEK"
                and instr_id in asm_utils.instr_exe_units(instr)
                and "FORWARD" in asm_utils.instr_mods(instr)
            ):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "step_fetched_forward", values, "std_logic")

    # Handle seek forward control
    if "step_fetched_backward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if (    asm_utils.instr_mnemonic(instr) == "BAM_SEEK"
                and instr_id in asm_utils.instr_exe_units(instr)
                and "BACKWARD" in asm_utils.instr_mods(instr)
            ):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "step_fetched_backward", values, "std_logic")


    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["addr_width"]) == int, "addr_width must be an int"
    assert config_in["addr_width"] > 0, "addr_width must greater than 0"
    config_out["addr_width"] = config_in["addr_width"]

    assert type(config_in["offset_width"]) == int, "offset_width must be an int"
    assert config_in["offset_width"] > 0, "offset_width must greater than 0"
    config_out["offset_width"] = config_in["offset_width"]

    assert type(config_in["step_width"]) == int, "step_width must be an int"
    assert config_in["step_width"] > 0, "step_width must greater than 0"
    config_out["step_width"] = config_in["step_width"]

    assert type(config_in["inputs"]) == int, "inputs must be an int"
    assert config_in["inputs"] >= 0, "inputs must greater than or equal to 0"
    config_out["inputs"] = config_in["inputs"]

    assert type(config_in["steps"]) == list, "steps must be a list"
    config_out["steps"] = []
    for step in config_in["steps"]:
        assert step in [
                "fetched_backward",
                "fetched_forward",
                "generic_backward",
                "generic_forward",
            ], "unknown step value, " + step
        assert step not in config_out["steps"], "step listed more than once " + step
        config_out["steps"].append(step)

    assert type(config_in["stallable"]) == bool, "stallable must be a boolean"
    config_out["stallable"] = config_in["stallable"]

    return config_out

import zlib

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "BAM"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%ia"%(config["addr_width"])
        generated_name += "_%io"%(config["offset_width"])
        generated_name += "_%is"%(config["step_width"])

        generated_name += "_%s"%str( hex( zlib.adler32("\n".join(config["steps"]).encode('utf-8')) )).lstrip("0x").zfill(8)

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name, concat_naming=False, force_generation=False):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = preprocess_config(config)
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, CONFIG)
    CONCAT_NAMING = concat_naming
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
        INTERFACE = { "ports" : { }, "generics" : { } }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            },
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts" : "all"
            }
        ]

        INTERFACE["ports"]["clock"] = {
            "type" : "std_logic",
            "direction" : "in",
        }

        if CONFIG["stallable"]:
            INTERFACE["ports"]["stall_in"] = {
                "type" : "std_logic",
                "direction" : "in",
            }
            ARCH_HEAD += "signal stall : std_logic;\n"
            ARCH_BODY += "stall <= stall_in;\n"


        # Generation Module Code
        generate_data_ports()
        generate_step_controls()
        generate_outset_adder_acc()
        generate_base_adders()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_data_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for input in range(CONFIG["inputs"]):
        INTERFACE["ports"]["in_%i"%(input, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["step_width"],
            "direction" : "in",
        }

def generate_step_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "signal selected_step : std_logic_vector(%i downto 0);\n"%(CONFIG["step_width"] - 1, )
    ARCH_BODY += "selected_step <= \>"

    # Handle fixed/generic step
    if set(CONFIG["steps"])&set(["generic_forward", "generic_backward"]):
        INTERFACE["generics"]["increment"] = {
            "type" : "integer"
        }
        if "generic_forward" in CONFIG["steps"]:
            INTERFACE["ports"]["step_generic_forward"] = {
                "type" : "std_logic",
                "direction" : "in",
            }
            ARCH_BODY +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_forward = '1'\nelse "
        if "generic_backward" in CONFIG["steps"]:
            INTERFACE["ports"]["step_generic_backward"] = {
                "type" : "std_logic",
                "direction" : "in"
            }
            ARCH_BODY +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_backward = '1'\nelse "

    # Handle fetched/data step
    if set(CONFIG["steps"])&set(["fetched_forward", "fetched_backward"]):
        # Check inputs
        assert(CONFIG["inputs"] >= 1)

        if "fetched_forward" in CONFIG["steps"]:
            INTERFACE["ports"]["step_fetched_forward"] = {
                "type" : "std_logic",
                "direction" : "in"
            }
            ARCH_BODY += "in_0 when step_fetched_forward = '1'\nelse "
        if "fetched_backward" in CONFIG["steps"]:
            INTERFACE["ports"]["step_fetched_backward"] = {
                "type" : "std_logic",
                "direction" : "in"
            }
            ARCH_BODY += "in_0 when step_fetched_backward = '1'\nelse "

    ARCH_BODY += "(others => '0');\<\n"


    ARCH_HEAD += "signal step_forward, step_backward : std_logic;\n"
    ARCH_BODY += "step_forward <= \>"
    if "generic_forward" in CONFIG["steps"]:
        ARCH_BODY +="'1' when step_generic_forward = '1'\nelse "
    if "fetched_forward" in CONFIG["steps"]:
        ARCH_BODY += "'1' when step_fetched_forward = '1'\nelse "
    ARCH_BODY += "'0';\n"


    ARCH_BODY += "step_backward <= \>"
    if "generic_backward" in CONFIG["steps"]:
        ARCH_BODY +="'1' when step_generic_backward = '1'\nelse "
    if "fetched_backward" in CONFIG["steps"]:
        ARCH_BODY += "'1' when step_fetched_backward = '1'\nelse "
    ARCH_BODY += "'0';\n"

def generate_outset_adder_acc():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"]["reset"] = {
        "type" : "std_logic",
        "direction" : "in"
    }

    ARCH_HEAD += "signal curr_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["offset_width"] - 1, )
    ARCH_HEAD += "signal next_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["offset_width"] - 1, )

    ARCH_BODY += "next_offset <=\>std_logic_vector( to_unsigned( to_integer( unsigned( curr_offset ) ) + to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_forward = '1'\nelse "
    ARCH_BODY += "std_logic_vector( to_unsigned( to_integer( unsigned( curr_offset ) ) - to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_backward = '1'\nelse "
    ARCH_BODY += "curr_offset;\<\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : True,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "offset_acc : entity work.%s(arch)\>\n"%(reg_name)

    ARCH_BODY += "generic map (\>\n"

    ARCH_BODY += "force_value => 0,\n"
    ARCH_BODY += "data_width => %i\n"%(CONFIG["offset_width"])

    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "enable => ( step_forward or step_backward ) and not stall,\n"
    else:
        ARCH_BODY += "enable => step_forward or step_backward,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in => next_offset,\n"
    ARCH_BODY += "data_out => curr_offset,\n"
    ARCH_BODY += "force => reset\n"

    ARCH_BODY += "\<);\n\<"

def generate_base_adders():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["generics"]["base"] = {
        "type" : "integer"
    }
    INTERFACE["ports"]["addr_0_fetch"] = {
        "type" : "std_logic_vector",
        "width": CONFIG["addr_width"],
        "direction" : "out"
    }
    INTERFACE["ports"]["addr_0_store"] = {
        "type" : "std_logic_vector",
        "width": CONFIG["addr_width"],
        "direction" : "out"
    }

    # Declare addr signals
    ARCH_HEAD += "signal addr_0_fetch_internal : std_logic_vector(%i downto 0);"%(CONFIG["addr_width"] - 1, )

    # Generate addr value
    ARCH_BODY += "addr_0_fetch_internal <= std_logic_vector(to_unsigned(base + to_integer(unsigned(curr_offset)), addr_0_fetch_internal'length));\n\n"
    ARCH_BODY += "addr_0_fetch <= addr_0_fetch_internal;\n"

    # Generate addr delay
    delay_interface, delay_name = delay.generate_HDL(
        {
            "width" : CONFIG["addr_width"],
            "depth" : 2,
            "has_enable" : CONFIG["stallable"],
            "inited" : False,
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "pre_addr_0_store_delay : entity work.%s(arch)\>\n"%(delay_name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "enable => not stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => addr_0_fetch_internal,\n"
    ARCH_BODY += "data_out => addr_0_store\n"

    ARCH_BODY += "\<);\n\<\n"
