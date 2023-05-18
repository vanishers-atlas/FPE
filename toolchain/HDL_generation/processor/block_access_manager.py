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
from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import dist_ROM

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

    base_addr = "base_addr" in interface["ports"].keys()


    for instr in instr_set:
        accesses = asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)
        for access, addr_comp in enumerate([ asm_utils.addr_com(asm_utils.access_addr(access)) for access in accesses]):
            if base_addr and addr_comp == instr_id:
                gen_utils.add_datapath_dest(pathways, "%sprefetch_addr_%i"%(lane, access), "prefetch", instr, "%sbase_addr"%(instr_prefix, ), "unsigned", interface["ports"]["base_addr"]["width"])

        for fetch, addr_comp in enumerate([ asm_utils.addr_com(asm_utils.access_addr(fetch)) for fetch in asm_utils.instr_fetches(instr) ]):
            if addr_comp == instr_id:
                gen_utils.add_datapath_source(pathways, "%sfetch_addr_%i"%(lane, fetch), "fetch", instr, "%saddr_0_fetch"%(instr_prefix, ), "unsigned", config["addr_width"])
                prefetch_needed = base_addr

        for write, addr_comp in enumerate([ asm_utils.addr_com(asm_utils.access_addr(store)) for store in asm_utils.instr_stores(instr) ]):
            if addr_comp == instr_id:
                gen_utils.add_datapath_source(pathways, "%sstore_addr_%i"%(lane, write), "store", instr, "%saddr_0_store"%(instr_prefix, ), "unsigned", config["addr_width"])
                prefetch_needed = base_addr

        if instr_id in asm_utils.instr_exe_units(instr):
            if asm_utils.instr_mnemonic(instr) == "BAM_SEEK":
                gen_utils.add_datapath_dest(pathways, "%sfetch_data_0_word_0"%(lane, ), "exe", instr, "%sfetched_step"%(instr_prefix, ), "unsigned", config["step_width"])


    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle step generic forward control
    if "step_forward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            accesses = asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)
            addrs = [ asm_utils.access_addr(access) for access in asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)]
            this_bam_addrs = [addr for addr in addrs if asm_utils.addr_com(addr) == instr_id]

            if len(this_bam_addrs) != 0:
                per_access_values = []
                for addr in this_bam_addrs:
                    mods = asm_utils.addr_mods(addr)
                    if "dir" in mods.keys() and mods["dir"] == "FORWARD":
                        per_access_values.append("1")
                    else:
                        per_access_values.append("0")

                # Convert per_access_values to instr wise value
                if '1' in per_access_values:
                    values["1"].append(instr)
                else:
                    values["0"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "step_forward", values, "std_logic")

    # Handle step generic backwards control
    if "step_backward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            accesses = asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)
            addrs = [ asm_utils.access_addr(access) for access in asm_utils.instr_fetches(instr) + asm_utils.instr_stores(instr)]
            this_bam_addrs = [addr for addr in addrs if asm_utils.addr_com(addr) == instr_id]


            if len(this_bam_addrs) != 0:
                for addr in this_bam_addrs:
                    mods = asm_utils.addr_mods(addr)
                    if "dir" in mods.keys() and mods["dir"] == "BACKWARD":
                        values["1"].append(instr)
                    else:
                        values["0"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "step_backward", values, "std_logic")

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
    if "seek_forward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if (    asm_utils.instr_mnemonic(instr) == "BAM_SEEK"
                and instr_id in asm_utils.instr_exe_units(instr)
                and "FORWARD" in asm_utils.instr_mods(instr)
            ):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "seek_forward", values, "std_logic")

    # Handle seek forward control
    if "seek_backward" in interface["ports"]:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            if (    asm_utils.instr_mnemonic(instr) == "BAM_SEEK"
                and instr_id in asm_utils.instr_exe_units(instr)
                and "BACKWARD" in asm_utils.instr_mods(instr)
            ):
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "exe", instr_prefix + "seek_backward", values, "std_logic")


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

    assert type(config_in["internal_step_type"]) == str, "internal_step_type must be a str"
    assert config_in["internal_step_type"] in ["none", "generic", "ROM"], "internal_step_type base_type, " + config_in["base_type"]
    config_out["internal_step_type"] = config_in["internal_step_type"]
    if config_in["internal_step_type"] == "ROM":
        assert type(config_in["interal_steps"]) == int, "interal_steps must be an int"
        assert config_in["interal_steps"] > 0, "interal_steps must greater than 0"
        config_out["interal_steps"] = config_in["interal_steps"]


    assert type(config_in["base_type"]) == str, "base_type must be a str"
    assert config_in["base_type"] in ["generic", "ROM"], "unknown base_type, " + config_in["base_type"]
    config_out["base_type"] = config_in["base_type"]
    if config_in["base_type"] == "ROM":
        assert type(config_in["internal_bases"]) == int, "internal_bases must be an int"
        assert config_in["internal_bases"] > 0, "internal_bases must greater than 0"
        config_out["internal_bases"] = config_in["internal_bases"]

    assert type(config_in["movements"]) == list, "movements must be a list"
    config_out["movements"] = []
    for movement in config_in["movements"]:
        assert len(movement) == 2
        source, direction = movement

        assert type(source) == str, "movement source must be a str"
        assert source in ["internal", "fetched"], "unknown movement source, " + source

        assert type(direction) == str, "movement direction must be a str"
        assert direction in ["forward", "backward"], "unknown movement direction, " + direction

        config_out["movements"].append((source, direction,))

    assert type(config_in["stallable"]) == bool, "stallable must be a boolean"
    config_out["stallable"] = config_in["stallable"]

    return config_out

import zlib

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "BAM"

        generated_name += "_%ia"%(config["addr_width"])
        generated_name += "_%io"%(config["offset_width"])
        generated_name += "_%is"%(config["step_width"])

        if config["internal_step_type"] == "ROM":
            generated_name += "_ROM%i"%(config["interal_steps"])
        else:
            generated_name += "_%s"%(config["internal_step_type"])

        if config["base_type"] == "ROM":
            generated_name += "_ROM%i"%(config["internal_bases"])
        else:
            generated_name += "_%s"%(config["base_type"])

        generated_name += "_%s"%(config["base_type"])
        config_out["movements"]

        generated_name += "_m%s"%str( hex( zlib.adler32("\n".join(config["movements"]).encode('utf-8')) )).lstrip("0x").zfill(8)

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

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

        # Generation Module Code
        gen_det, com_det = gen_common_ports(gen_det, com_det)
        gen_det, com_det = gen_offset_registor(gen_det, com_det)
        gen_det, com_det = gen_movement_logic(gen_det, com_det)
        gen_det, com_det = gen_step_logic(gen_det, com_det)
        gen_det, com_det = gen_base_logic(gen_det, com_det)


        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_common_ports(gen_det, com_det):
    com_det.add_port("clock", "std_logic", "in")

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")
        com_det.arch_head += "signal stall : std_logic;\n"
        com_det.arch_body += "stall <= stall_in;\n"

    com_det.add_port("reset", "std_logic", "in")

    return gen_det, com_det

#####################################################################

def gen_offset_registor(gen_det, com_det):

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

    com_det.arch_head += "signal next_offset : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )
    com_det.arch_head += "signal curr_offset : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )

    com_det.arch_body += "offset_acc : entity work.%s(arch)\>\n"%(reg_name)

    com_det.arch_body += "generic map (\>\n"

    com_det.arch_body += "force_value => 0,\n"
    com_det.arch_body += "data_width => %i\n"%(gen_det.config["offset_width"])

    com_det.arch_body += "\<)\n"

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => movement_enable and not stall,\n"
    else:
        com_det.arch_body += "enable => movement_enable,\n"

    com_det.arch_body += "clock => clock,\n"

    com_det.arch_body += "data_in => next_offset,\n"
    com_det.arch_body += "data_out => curr_offset,\n"
    com_det.arch_body += "force => reset\n"

    com_det.arch_body += "\<);\n\<"

    return gen_det, com_det

#####################################################################

def gen_movement_logic(gen_det, com_det):
    # Handle control points
    forwards = []
    backwards = []

    if ("fetched", "forward") in gen_det.config["movements"]:
        com_det.add_port("seek_forward", "std_logic", "in")
        forwards.append("seek_forward")
    if ("fetched", "backward") in gen_det.config["movements"]:
        com_det.add_port("seek_backward", "std_logic", "in")
        backwards.append("seek_backward")
    if ("internal", "forward" ) in gen_det.config["movements"]:
        com_det.add_port("step_forward", "std_logic", "in")
        forwards.append("step_forward")
    if ("internal", "backward") in gen_det.config["movements"]:
        com_det.add_port("step_backward", "std_logic", "in")
        backwards.append("step_backward")

    if forwards:
        com_det.arch_head += "signal movement_forwards : std_logic;\n"
        com_det.arch_body += "movement_forwards <= %s;\n"%(" or ".join(forwards), )

        com_det.arch_head += "signal offset_forwarded : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )
        com_det.arch_body += "offset_forwarded <= std_logic_vector(to_unsigned( to_integer(unsigned(curr_offset)) + to_integer(unsigned(selected_step)), next_offset'length));\n"
    if backwards:
        com_det.arch_head += "signal movement_backwards : std_logic;\n"
        com_det.arch_body += "movement_backwards <= %s;\n"%(" or ".join(backwards), )

        com_det.arch_head += "signal offset_backwarded : std_logic_vector(%i downto 0);\n"%(gen_det.config["offset_width"] - 1, )
        com_det.arch_body += "offset_backwarded <= std_logic_vector(to_unsigned( to_integer(unsigned(curr_offset)) - to_integer(unsigned(selected_step)), next_offset'length));\n"

    com_det.arch_head += "signal movement_enable : std_logic;\n"
    if forwards and backwards:
        com_det.arch_body += "movement_enable <= movement_forwards or movement_backwards;\n"
        com_det.arch_body += "next_offset <= offset_forwarded when movement_forwards = '1' else offset_backwarded when movement_backwards = '1' else curr_offset;\n\n"
    elif forwards:
        com_det.arch_body += "movement_enable <= movement_forwards;\n"
        com_det.arch_body += "next_offset <= offset_forwarded when movement_forwards = '1' else curr_offset;\n\n"
    elif backwards:
        com_det.arch_body += "movement_enable <= movement_backwards;\n"
        com_det.arch_body += "next_offset <= offset_backwarded when movement_backwards = '1' else curr_offset;\n\n"
    else:
        raise ValueError()


    return gen_det, com_det

#####################################################################

def gen_step_logic(gen_det, com_det):
    com_det.arch_head += "signal selected_step : std_logic_vector(%i downto 0);\n"%(gen_det.config["step_width"] - 1, )

    fetched_step = any([movement[0] == "fetched" for movement in gen_det.config["movements"]])
    internal_step = any([movement[0] == "internal" for movement in gen_det.config["movements"]])
    if fetched_step and internal_step:
        gen_det, com_det = gen_step_fetched_logic(gen_det, com_det)
        gen_det, com_det = gen_step_internal_logic(gen_det, com_det)

        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs"  : 2,
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        com_det.arch_head += "signal step_select : std_logic;\n"
        fetched_forward  = ("fetched", "forward") in gen_det.config["movements"]
        fetched_backward = ("fetched", "backward") in gen_det.config["movements"]
        if   fetched_forward and fetched_backward:
            com_det.arch_body += "step_select <= seek_forward or seek_backward;\n"
        elif fetched_forward:
            com_det.arch_body += "step_select <= seek_forward;\n"
        elif fetched_backward:
            com_det.arch_body += "step_select <= seek_backward;\n"



        com_det.arch_body += "step_select_mux : entity work.%s(arch)\>\n"%(mux_name, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["step_width"], )

        com_det.arch_body += "port map (\n\>"

        com_det.arch_body += "sel(0)    => step_select,\n"
        com_det.arch_body += "data_in_0 => internal_step,\n"
        com_det.arch_body += "data_in_1 => fetched_step,\n"
        com_det.arch_body += "data_out  => selected_step\n"

        com_det.arch_body += "\<);\n\<\n"
    elif fetched_step:
        gen_det, com_det = gen_step_fetched_logic(gen_det, com_det)
        com_det.arch_body += "selected_step <= fetched_step;\n"
    elif internal_step:
        gen_det, com_det = gen_step_internal_logic(gen_det, com_det)
        com_det.arch_body += "selected_step <= internal_step;\n"
    else:
        raise ValueError()

    return gen_det, com_det


def gen_step_fetched_logic(gen_det, com_det):
    com_det.add_port("fetched_step", "std_logic_vector", "in", gen_det.config["step_width"])

    return gen_det, com_det

def gen_step_internal_logic(gen_det, com_det):
    com_det.arch_head += "signal internal_step : std_logic_vector(%i downto 0);\n"%(gen_det.config["step_width"] - 1, )

    if   gen_det.config["internal_step_type"] == "generic":
        com_det.add_generic("internal_step_value", "integer")
        com_det.arch_body += "internal_step <= std_logic_vector(to_unsigned(internal_step_value, internal_step'length));\n\n"
    elif gen_det.config["internal_step_type"] == "ROM":
        raise NotImplementedError()
    else:
        raise ValueError()

    return gen_det, com_det

#####################################################################

def gen_base_logic(gen_det, com_det):

    com_det.arch_head += "signal selected_base : std_logic_vector(%i downto 0);\n"%(gen_det.config["addr_width"] - 1, )

    if   gen_det.config["base_type"] == "generic":
        gen_det, com_det = gen_base_type_generic(gen_det, com_det)
    elif gen_det.config["base_type"] == "ROM":
        gen_det, com_det = gen_base_type_ROM(gen_det, com_det)
    else:
        raise ValueError("Unknonw base_type value, %s"%(gen_det.config["base_type"], ))

    # Generate addr value
    com_det.arch_head += "signal addr_0_fetch_internal : std_logic_vector(%i downto 0);"%(gen_det.config["addr_width"] - 1, )
    com_det.arch_body += "addr_0_fetch_internal <= std_logic_vector(to_unsigned( "
    com_det.arch_body += "to_integer(unsigned(selected_base)) + to_integer(unsigned(curr_offset))"
    com_det.arch_body += ", addr_0_fetch_internal'length));\n\n"

    # Connect fetch addr port
    com_det.add_port("addr_0_fetch", "std_logic_vector", "out", gen_det.config["addr_width"])
    com_det.arch_body += "addr_0_fetch <= addr_0_fetch_internal;\n"

    # Connect store addr port
    com_det.add_port("addr_0_store", "std_logic_vector", "out", gen_det.config["addr_width"])
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

    return gen_det, com_det

def gen_base_type_generic(gen_det, com_det):

    com_det.add_generic("base", "integer")
    com_det.arch_body += "selected_base <= std_logic_vector(to_unsigned(base, selected_base'length));\n\n"

    return gen_det, com_det

def gen_base_type_ROM(gen_det, com_det):

    com_det.add_interface_item("required_stages", ["prefetch", ])

    rom_interface, rom_name = dist_ROM.generate_HDL(
        {
            "depth" : gen_det.config["internal_bases"],
            "width" : gen_det.config["addr_width"],
            "reads" : 1,
            "synchronous" : True,
            "has_enable" : gen_det.config["stallable"],
            "init_type" : "GENERIC_STD"
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # Instancate ROM
    com_det.arch_body += "internal_base_ROM : entity work.%s(arch)\>\n"%(rom_name, )

    com_det.arch_body += "generic map (\n\>"
    for index in range(gen_det.config["internal_bases"]):
        com_det.add_generic("base_%i"%(index, ), "std_logic_vector", gen_det.config["addr_width"])
        com_det.arch_body += "init_%i => base_%i,\n"%(index, index, )
    for index in range(gen_det.config["internal_bases"], 2**rom_interface["addr_width"]):
        com_det.arch_body += "init_%i => (others => '0'),\n"%(index, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<)\n"

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall,\n"

    com_det.arch_body += "clock => clock,\n"

    com_det.add_port("base_addr", "std_logic_vector", "in", rom_interface["addr_width"])
    com_det.arch_body += "read_0_addr => base_addr,\n"
    com_det.arch_body += "read_0_data => selected_base\n"

    com_det.arch_body += "\<);\n\<\n"


    return gen_det, com_det
