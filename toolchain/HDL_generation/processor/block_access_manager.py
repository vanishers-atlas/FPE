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

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_import("ieee", "numeric_std", "all")

        com_det.add_port("clock", "std_logic", "in")
        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_head += "signal stall : std_logic;\n"
            com_det.arch_body += "stall <= stall_in;\n"


        # Generation Module Code
        generate_data_ports(gen_det, com_det)
        generate_step_controls(gen_det, com_det)
        generate_outset_adder_acc(gen_det, com_det)
        generate_base_adders(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_data_ports(gen_det, com_det):
    for input in range(gen_det.config["inputs"]):
        com_det.add_port("in_%i"%(input, ), "std_logic_vector", "in", gen_det.config["step_width"])

def generate_step_controls(gen_det, com_det):
    com_det.arch_head += "signal selected_step : std_logic_vector(%i downto 0);\n"%(gen_det.config["step_width"] - 1, )
    com_det.arch_body += "selected_step <= \>"

    # Handle fixed/generic step
    if set(gen_det.config["steps"])&set(["generic_forward", "generic_backward"]):
        com_det.add_generic("increment", "integer")

        if "generic_forward" in gen_det.config["steps"]:
            com_det.add_port("step_generic_forward", "std_logic", "in")
            com_det.arch_body +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_forward = '1'\nelse "
        if "generic_backward" in gen_det.config["steps"]:
            com_det.add_port("step_generic_backward", "std_logic", "in")
            com_det.arch_body +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_backward = '1'\nelse "

    # Handle fetched/data step
    if set(gen_det.config["steps"])&set(["fetched_forward", "fetched_backward"]):
        # Check inputs
        assert(gen_det.config["inputs"] >= 1)

        if "fetched_forward" in gen_det.config["steps"]:
            com_det.add_port("step_fetched_forward", "std_logic", "in")
            com_det.arch_body += "in_0 when step_fetched_forward = '1'\nelse "
        if "fetched_backward" in gen_det.config["steps"]:
            com_det.add_port("step_fetched_backward", "std_logic", "in")
            com_det.arch_body += "in_0 when step_fetched_backward = '1'\nelse "

    com_det.arch_body += "(others => '0');\<\n"


    com_det.arch_head += "signal step_forward, step_backward : std_logic;\n"
    com_det.arch_body += "step_forward <= \>"
    if "generic_forward" in gen_det.config["steps"]:
        com_det.arch_body +="'1' when step_generic_forward = '1'\nelse "
    if "fetched_forward" in gen_det.config["steps"]:
        com_det.arch_body += "'1' when step_fetched_forward = '1'\nelse "
    com_det.arch_body += "'0';\n"


    com_det.arch_body += "step_backward <= \>"
    if "generic_backward" in gen_det.config["steps"]:
        com_det.arch_body +="'1' when step_generic_backward = '1'\nelse "
    if "fetched_backward" in gen_det.config["steps"]:
        com_det.arch_body += "'1' when step_fetched_backward = '1'\nelse "
    com_det.arch_body += "'0';\n"

def generate_outset_adder_acc(gen_det, com_det):
    com_det.add_port("reset", "std_logic", "in")

    com_det.arch_head += "signal curr_offset : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )
    com_det.arch_head += "signal next_offset : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )

    com_det.arch_body += "next_offset <=\>std_logic_vector( to_unsigned( to_integer( unsigned( curr_offset ) ) + to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_forward = '1'\nelse "
    com_det.arch_body += "std_logic_vector( to_unsigned( to_integer( unsigned( curr_offset ) ) - to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_backward = '1'\nelse "
    com_det.arch_body += "curr_offset;\<\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : True,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "offset_acc : entity work.%s(arch)\>\n"%(reg_name)

    com_det.arch_body += "generic map (\>\n"

    com_det.arch_body += "force_value => 0,\n"
    com_det.arch_body += "data_width => %i\n"%(gen_det.config["offset_width"])

    com_det.arch_body += "\<)\n"

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => ( step_forward or step_backward ) and not stall,\n"
    else:
        com_det.arch_body += "enable => step_forward or step_backward,\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "data_in => next_offset,\n"
    com_det.arch_body += "data_out => curr_offset,\n"
    com_det.arch_body += "force => reset\n"

    com_det.arch_body += "\<);\n\<"

def generate_base_adders(gen_det, com_det):
    com_det.add_generic("base", "integer")

    com_det.add_port("addr_0_fetch", "std_logic_vector", "out", gen_det.config["addr_width"])
    com_det.add_port("addr_0_store", "std_logic_vector", "out", gen_det.config["addr_width"])

    # Declare addr signals
    com_det.arch_head += "signal addr_0_fetch_internal : std_logic_vector(%i downto 0);"%(gen_det.config["addr_width"] - 1, )

    # Generate addr value
    com_det.arch_body += "addr_0_fetch_internal <= std_logic_vector(to_unsigned(base + to_integer(unsigned(curr_offset)), addr_0_fetch_internal'length));\n\n"
    com_det.arch_body += "addr_0_fetch <= addr_0_fetch_internal;\n"

    # Generate addr delay
    delay_interface, delay_name = delay.generate_HDL(
        {
            "width" : gen_det.config["addr_width"],
            "depth" : 2,
            "has_enable" : gen_det.config["stallable"],
            "inited" : False,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "pre_addr_0_store_delay : entity work.%s(arch)\>\n"%(delay_name)

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall,\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "data_in  => addr_0_fetch_internal,\n"
    com_det.arch_body += "data_out => addr_0_store\n"

    com_det.arch_body += "\<);\n\<\n"
