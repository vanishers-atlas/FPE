# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re
import math
import json
import copy

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import dist_RAM
from FPE.toolchain.HDL_generation.basic import register

from FPE.toolchain.HDL_generation.processor import BAPA_common as BAPA_harness

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    config["buffer_reads"] = True

    config["reads"] = 0
    config["writes"] = 0
    for instr in instr_set:
        count = 0
        for access in asm_utils.instr_fetches(instr):
            if asm_utils.access_mem(access) == instr_id:
                count += 1
        config["reads"] = max(config["reads"], count)

        count = 0
        for access in asm_utils.instr_stores(instr):
            if asm_utils.access_mem(access) == instr_id:
                count += 1
        config["writes"] = max(config["writes"], count)

    BAPA_config = BAPA_harness.add_inst_config(instr_id, instr_set, config)
    if BAPA_config != None:
        config["buffer_reads"] = False
        config["BAPA"] = BAPA_config

    return config

read_addr_patern = re.compile("read_(\d+)_addr")
read_data_patern = re.compile("read_(\d+)_data")
write_addr_patern = re.compile("write_(\d+)_addr")
write_data_patern = re.compile("write_(\d+)_data")

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    if "BAPA" in config.keys():
        pathways = BAPA_harness.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    else:
        # Gather pathway ports
        read_addr_ports = []
        read_data_ports = []
        write_addr_ports = []
        write_data_ports = []
        for port in interface["ports"]:
            match = read_addr_patern.fullmatch(port)
            if match:
                read_addr_ports.append(int(match.group(1)))
                continue

            match = read_data_patern.fullmatch(port)
            if match:
                read_data_ports.append(int(match.group(1)))
                continue

            match = write_addr_patern.fullmatch(port)
            if match:
                write_addr_ports.append(int(match.group(1)))
                continue

            match = write_data_patern.fullmatch(port)
            if match:
                write_data_ports.append(int(match.group(1)))
                continue

        # Loop over all instructions and generate paths for all found pathway ports
        for instr in instr_set:
            reads  = [fetch for fetch, access in enumerate(asm_utils.instr_fetches(instr)) if asm_utils.access_mem(access) == instr_id ]
            writes = [store for store, access in enumerate(asm_utils.instr_stores(instr)) if asm_utils.access_mem(access) == instr_id ]

            # Handle read_addr_ports
            for read in read_addr_ports:
                if read < len(reads):
                    fetch = reads[read]
                    gen_utils.add_datapath_dest(pathways, "%sfetch_addr_%i"%(lane, fetch, ), "fetch", instr, "%sread_%i_addr"%(instr_prefix, read, ), "unsigned", config["addr_width"])

            # Handle read_data_ports
            for read in read_data_ports:
                if read < len(reads):
                    fetch = reads[read]
                    gen_utils.add_datapath_source(pathways, "%sfetch_data_%i_word_0"%(lane, fetch, ), "exe", instr, "%sread_%i_data"%(instr_prefix, read, ), config["signal_padding"], config["data_width"])

            # Handle write_data_ports
            for write in write_addr_ports:
                if write < len(writes):
                    store = writes[write]
                    gen_utils.add_datapath_dest(pathways, "%sstore_addr_%i"%(lane, store, ), "store", instr, "%swrite_%i_addr"%(instr_prefix, write, ), "unsigned", config["addr_width"])

            # Handle write_data_ports
            for write in write_data_ports:
                if write < len(writes):
                    store = writes[write]
                    gen_utils.add_datapath_dest(pathways, "%sstore_data_%i_word_0"%(lane, store, ), "store", instr, "%swrite_%i_data"%(instr_prefix, write, ), config["signal_padding"], config["data_width"])

    return pathways

write_enables_pattern = re.compile("write_(\d+)_enable")

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    if "BAPA" in config.keys():
        controls = BAPA_harness.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    else:
        # Gather controt ports
        write_enable_controls = []
        for port in interface["ports"]:
            match = write_enables_pattern.fullmatch(port)
            if match:
                write_enable_controls.append(int(match.group(1)) )
                continue

        # Handle write_enable_controls
        for write in write_enable_controls:
            values = { "0" : [], "1" : [], }

            for instr in instr_set:
                if [asm_utils.access_mem(store) for store in asm_utils.instr_stores(instr)].count(instr_id) > write:
                    values["1"].append(instr)
                else:
                    values["0"].append(instr)

            gen_utils.add_control(controls, "store", instr_prefix + "write_%i_enable"%(write, ), values, "std_logic")

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["reads"]) == int, "reads must be an int"
    assert config_in["reads"] > 0, "reads must be greater than 0"
    config_out["reads"] = config_in["reads"]

    assert type(config_in["buffer_reads"]) == bool, "buffer_reads must be a bool"
    config_out["buffer_reads"] = config_in["buffer_reads"]

    assert type(config_in["writes"]) == int, "writes must be an int"
    assert config_in["writes"] > 0, "writes must be greater than 0"
    config_out["writes"] = config_in["writes"]

    assert type(config_in["depth"]) == int, "depth must be an int"
    assert config_in["depth"] > 0, "depth must be greater than 0"
    config_out["depth"] = config_in["depth"]

    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    if "BAPA" in config_in.keys():
        config_out["BAPA"] = BAPA_harness.preprocess_config(config_in["BAPA"])

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "REG"

        if "BAPA" in config.keys():
            sub_name = BAPA_harness.handle_module_name(None, config["BAPA"])
            raise N0tImplementedError()

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

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

        # Generation component code
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_port("clock", "std_logic", "in")
        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_head += "signal stall : std_logic;\n"
            com_det.arch_body += "stall <= stall_in;\n"

        if "BAPA" in gen_det.config.keys():
            gen_BAPA_regfile(gen_det, com_det)
        else:
            gen_ram(gen_det, com_det)
            gen_reads(gen_det, com_det)
            gen_writes(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name

#####################################################################

def gen_BAPA_regfile(gen_det, com_det):
    gen_det, com_det = handle_harness_blocks(gen_det, com_det)
    gen_det, com_det = handle_BAPA_harness(gen_det, com_det)

    return gen_det, com_det

wrapped_fanin_signals = ["clock", "stall_in"]
wrapped_internal_signals = [
    re.compile("read_(\d+)_addr"),
    re.compile("read_(\d+)_data"),
    re.compile("write_(\d+)_addr"),
    re.compile("write_(\d+)_data"),
    re.compile("write_(\d+)_enable"),
]

def handle_harness_blocks(gen_det, com_det):
    # Compute wrapped memory details
    wrapped_config = copy.deepcopy(gen_det.config)
    # Remove BAPA from wrapped_config as BAPA is being handled in this super component
    del wrapped_config["BAPA"]
    wrapped_config = { ** wrapped_config, **gen_det.config["BAPA"]["wrapped_mems"] }

    if gen_det.concat_naming :
        module_name = gen_det.module_name + "_subblock"
    else:
        module_name = None

    wrapped_interface, wrapped_name = generate_HDL(
        config=wrapped_config,
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    gen_det.config["BAPA"]["wrapped_mems"]["addr_width"] = wrapped_interface["addr_width"]

    # Instancate sub blocks
    for subblock in range(gen_det.config["BAPA"]["wrapped_mems"]["num_blocks"]):
        com_det.arch_body += "wrapped_%i : entity work.%s(arch)\>\n"%(subblock, wrapped_name, )

        if wrapped_interface["generics"]:
            com_det.arch_body += "generic map (\>\n"
            raise NotImplementedError()
            com_det.arch_body += "\<)\n"

        com_det.arch_body += "port map (\n\>"

        # Handle fanin signals
        for signal in wrapped_fanin_signals:
            if signal in wrapped_interface["ports"]:
                com_det.arch_body += "%s => %s,\n"%(signal, signal)

        # Handle internal signals
        for rule in wrapped_internal_signals:
            for port in [port for port in wrapped_interface["ports"].keys() if rule.fullmatch(port) ]:
                details = wrapped_interface["ports"][port]

                com_det.arch_body += "%s => block_%i_%s,\n"%(port, subblock, port, )


        com_det.arch_body.drop_last_X(2)
        com_det.arch_body += "\n\<);\n\<\n"

    return gen_det, com_det

hardness_fanin_signals = ["clock", "stall_in"]

hardness_ripple_up_addrs = [
    re.compile("read_(\d+)_addr"),
    re.compile("write_(\d+)_addr"),
]
hardness_ripple_up_data = [
    re.compile("read_(\d+)_word_(\d+)"),
    re.compile("write_(\d+)_word_(\d+)"),
]
hardness_ripple_up_signals = [
    re.compile("write_(\d+)_enable_(\d+)"),
]

hardness_wrapped_addrs = [
    re.compile("block_(\d+)_read_(\d+)_addr"),
    re.compile("block_(\d+)_write_(\d+)_addr"),
]
hardness_wrapped_data = [
    re.compile("block_(\d+)_read_(\d+)_data"),
    re.compile("block_(\d+)_write_(\d+)_data"),
]
hardness_internal_signals = [
    re.compile("block_(\d+)_write_(\d+)_enable"),
]

def handle_BAPA_harness(gen_det, com_det):
    # Generate BAPA harness
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_BAPA_harness"
    else:
        module_name = None

    harness_interface, harness_name = BAPA_harness.generate_HDL(
        config=gen_det.config["BAPA"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    gen_det.config["addr_width"] = gen_det.config["BAPA"]["wrapped_mems"]["addr_width"] + harness_interface["BAPA_addr_bits"]

    # Instancate BAPA harness
    com_det.arch_body += "BAPA_harness : entity work.%s(arch)\>\n"%(harness_name, )

    com_det.arch_body += "generic map (\>\n"
    com_det.arch_body += "data_width => %i,\n"%(gen_det.config["data_width"], )
    com_det.arch_body += "block_addr_width => %i\n"%(gen_det.config["BAPA"]["wrapped_mems"]["addr_width"], )
    com_det.arch_body += "\<)\n"

    com_det.arch_body += "port map (\n\>"

    # Handle fanin signals
    for signal in hardness_fanin_signals:
        if signal in harness_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(signal, signal)


    # Ripple up harness addrs
    for rule in hardness_ripple_up_addrs:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            width = gen_det.config["addr_width"]
            com_det.add_port(port, "std_logic_vector", details["direction"], width)

            # Connect harness port to rippled port
            com_det.arch_body += "%s => %s,\n"%(port, port)

    # Ripple up harness data
    for rule in hardness_ripple_up_data:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            width = gen_det.config["addr_width"]
            com_det.add_port(port, "std_logic_vector", details["direction"], width)

            # Connect harness port to rippled port
            com_det.arch_body += "%s => %s,\n"%(port, port)

    # Handle ripple up signals
    for rule in hardness_ripple_up_signals:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            # Declare rippled port
            try:
                com_det.add_port(port, details["type"], details["direction"], details["width"])
            except KeyError:
                com_det.add_port(port, details["type"], details["direction"])

            # Connect harness port to rippled port
            com_det.arch_body += "%s => %s,\n"%(port, port)


    # Connect wrapped addrs
    for rule in hardness_wrapped_addrs:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            width = gen_det.config["BAPA"]["wrapped_mems"]["addr_width"]

            com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(port, width - 1, )
            com_det.arch_body += "%s => %s,\n"%(port, port)

    # Connect wrapped data
    for rule in hardness_wrapped_data:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            width = gen_det.config["BAPA"]["wrapped_mems"]["data_width"]

            com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(port, width - 1, )
            com_det.arch_body += "%s => %s,\n"%(port, port)

    # Handle internal signals
    for rule in hardness_internal_signals:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            # Declare inturnal signal
            try:
                com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(port, details["width"] - 1, )
            except KeyError:
                com_det.arch_head += "signal %s : std_logic;\n"%(port, )

            # Connect harness port to internal signal
            com_det.arch_body += "%s => %s,\n"%(port, port)

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"

    return gen_det, com_det



#####################################################################

def gen_ram(gen_det, com_det):
    com_det.add_interface_item("addr_width", gen_det.config["addr_width"])

    if gen_det.config["writes"] != 1:
        raise ValueError("regfile only supports 1 write per cycle")

    # Determine ram config type
    if gen_det.config["reads"] == 1:
        com_det.ports_config = "SIMPLE_DUAL"
    elif gen_det.config["reads"] <= 3:
        com_det.ports_config = "QUAD"
    else:
        raise ValueError("regfile only supports up 3 reads per cycle")

    ram_interface, ram_name = dist_RAM.generate_HDL(
        {
            "depth" : gen_det.config["depth"],
            "init_type" : "NONE",
            "ports_config" : com_det.ports_config,
            "synchronicity" : "WRITE_ONLY",
            "enabled_reads" : False,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_head += "-- RAM signals\n"
    com_det.arch_body += "-- RAM block\n"

    com_det.arch_body += "RAM_core : entity work.%s(arch)\>\n"%(ram_name, )
    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )
    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "clock => clock,\n"


    # Handle wrute port
    com_det.arch_head += "signal RAM_write_enable : std_logic;\n"
    com_det.arch_body += "write_enable  => RAM_write_enable,\n"

    com_det.arch_head += "signal RAM_write_data  : std_logic_vector(%i downto 0);\n"%(gen_det.config["data_width"] - 1, )

    if any(portname == "read_write_addr" for portname in ram_interface["ports"].keys()):
        com_det.arch_body += "write_data => RAM_write_data,\n"
        com_det.arch_body += "read_write_data => open,\n"

        com_det.arch_head += "signal RAM_write_addr  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )
        com_det.arch_body += "read_write_addr  => RAM_write_addr,\n"
    elif any(portname == "write_addr" for portname in ram_interface["ports"].keys()):
        com_det.arch_body += "write_data  => RAM_write_data,\n"

        com_det.arch_head += "signal RAM_write_addr  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )
        com_det.arch_body += "write_addr  => RAM_write_addr,\n"
    else:
        raise NotImplementedError("Unknown write behavour")

    # Handle read port
    if any(portname == "read_addr" for portname in ram_interface["ports"].keys()):
        com_det.arch_head += "signal RAM_read_addr_0  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )
        com_det.arch_head += "signal RAM_read_data_0  : std_logic_vector(%i downto 0);\n"%(gen_det.config["data_width"] - 1, )

        com_det.arch_body += "read_addr  => RAM_read_addr_0,\n"
        com_det.arch_body += "read_data  => RAM_read_data_0,\n"
    elif any(portname == "read_2_addr" for portname in ram_interface["ports"].keys()):
        com_det.arch_head += "signal RAM_read_addr_0  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )
        com_det.arch_head += "signal RAM_read_addr_1  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )
        com_det.arch_head += "signal RAM_read_addr_2  : std_logic_vector(%i downto 0);\n"%(ram_interface["addr_width"] - 1, )

        com_det.arch_body += "read_0_addr  => RAM_read_addr_0,\n"
        com_det.arch_body += "read_1_addr  => RAM_read_addr_1,\n"
        com_det.arch_body += "read_2_addr  => RAM_read_addr_2,\n"

        com_det.arch_head += "signal RAM_read_data_0  : std_logic_vector(%i downto 0);\n"%(gen_det.config["data_width"] - 1, )
        com_det.arch_head += "signal RAM_read_data_1  : std_logic_vector(%i downto 0);\n"%(gen_det.config["data_width"] - 1, )
        com_det.arch_head += "signal RAM_read_data_2  : std_logic_vector(%i downto 0);\n"%(gen_det.config["data_width"] - 1, )

        com_det.arch_body += "read_0_data  => RAM_read_data_0,\n"
        com_det.arch_body += "read_1_data  => RAM_read_data_1,\n"
        com_det.arch_body += "read_2_data  => RAM_read_data_2,\n"
    else:
        raise NotImplementedError("Unknown read behavour")

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\<);\n\<\n"

def gen_reads(gen_det, com_det):

    if gen_det.config["buffer_reads"]:
        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force"  : False,
                "has_sync_force"   : False,
                "has_enable"    : gen_det.config["stallable"],
                "force_on_init" : False
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

    for read in range(gen_det.config["reads"]):
        # Declare port
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector", "in", gen_det.config["addr_width"])
        com_det.add_port("read_%i_data"%(read, ), "std_logic_vector", "out", gen_det.config["data_width"])

        com_det.arch_head += "signal read_%i_data_internal : std_logic_vector(%i downto 0);\n"%(read, gen_det.config["data_width"] - 1)
        if gen_det.config["buffer_reads"]:
            # Generate output buffers

            com_det.arch_body += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)

            com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

            com_det.arch_body += "port map (\n\>"

            if gen_det.config["stallable"]:
                com_det.arch_body += "enable  => not stall_in,\n"

            com_det.arch_body += "clock => clock,\n"
            com_det.arch_body += "data_in  => read_%i_data_internal,\n"%(read, )
            com_det.arch_body += "data_out => read_%i_data\n"%(read, )

            com_det.arch_body += "\<);\n\<"

            com_det.arch_body += "\n"
        else:
            com_det.arch_body += "read_%i_data <= read_%i_data_internal;\n"%(read, read, )

    if com_det.ports_config == "SIMPLE_DUAL":
        com_det.arch_body += "RAM_read_addr_0 <= read_0_addr;\n"
        com_det.arch_body += "read_0_data_internal <= RAM_read_data_0;\n"
    elif com_det.ports_config == "QUAD":
        for read in range(gen_det.config["reads"]):
            com_det.arch_body += "RAM_read_addr_%i <= read_%i_addr;\n"%(read, read, )
            com_det.arch_body += "read_%i_data_internal <= RAM_read_data_%i;\n"%(read, read, )

        for read in range(gen_det.config["reads"], 3):
            com_det.arch_body += "RAM_read_addr_%i <= (others => '1');\n"%(read, )
    else:
        raise ValueError("regfile only supports up 3 reads per cycle")

def gen_writes(gen_det, com_det):

    if gen_det.config["writes"] == 1:
        com_det.add_port("write_0_addr", "std_logic_vector", "in", gen_det.config["addr_width"])
        com_det.add_port("write_0_data", "std_logic_vector", "in", gen_det.config["data_width"])
        com_det.add_port("write_0_enable", "std_logic", "in")

        com_det.arch_body += "RAM_write_data <= write_0_data;\n"
        com_det.arch_body += "RAM_write_addr <= write_0_addr;\n"
        com_det.arch_body += "RAM_write_enable <= write_0_enable;\n"
    else:
        raise NotImplementedError("Regfile can only handle 1 wrtie per cycle")
