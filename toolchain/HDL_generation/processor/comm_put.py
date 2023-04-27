# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    writes = 0
    for instr in instr_set:
        store_mems = [ asm_utils.access_mem(access) for access in asm_utils.instr_stores(instr) ]
        writes = max(writes, store_mems.count(instr_id))
    config["writes"] = writes

    return config

write_addr_patern = re.compile("write_(\d+)_addr")
write_data_patern = re.compile("write_(\d+)_data")

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    # Gather pathway ports
    write_addr_ports = []
    write_data_ports = []
    for port in interface["ports"]:
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
        writes = [store for store, access in enumerate(asm_utils.instr_stores(instr)) if asm_utils.access_mem(access) == instr_id ]

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

    # Stalling parameters
    assert type(config_in["FIFO_handshakes"]) == bool, "FIFO_handshakes must be a boolean"
    config_out["FIFO_handshakes"] = config_in["FIFO_handshakes"]

    assert type(config_in["stallable"]) == bool, "stallable must be a boolean"
    config_out["stallable"] = config_in["stallable"]

    if   config_in["FIFO_handshakes"]:
        config_out["stall_type"] = "ACTIVE"
    elif config_in["stallable"]:
        config_out["stall_type"] = "PASSIVE"
    else:
        config_out["stall_type"] = "NONE"


    # Data pori parameters
    assert type(config_in["writes"]) == int, "writes must be an int"
    assert config_in["writes"] > 0., "writes must be greater than 0"
    config_out["writes"] = config_in["writes"]

    assert type(config_in["FIFOs"]) == int, "FIFOs must be an int"
    assert config_in["FIFOs"] > 0., "FIFOs must be greater than 0"
    config_out["FIFOs"] = config_in["FIFOs"]

    # Datapath parametes
    assert type(config_in["data_width"]) == int, "data_width must be an int"
    assert config_in["data_width"] > 0., "data_width must be greater than 0"
    config_out["data_width"] = config_in["data_width"]

    config_out["addr_width"] = tc_utils.unsigned.width(config_out["FIFOs"] - 1)

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "PUT"

        # Denote Data width, writes, and FIFOs parameters
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%if"%(config["FIFOs"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%s"%(config["stall_type"][0], )

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

        # Generation Module Code
        gen_ports(gen_det, com_det)
        gen_stalling_logic(gen_det, com_det)
        gen_FIFO_data_logic(gen_det, com_det)
        gen_FIFO_write_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_ports(gen_det, com_det):
    # Decalre clock and runnning ports
    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("running", "std_logic", "in")

    # Handle FIFO ports
    for FIFO in range(gen_det.config["FIFOs"]):
        com_det.add_port("FIFO_%i_data"%(FIFO, ), "std_logic_vector", "out", gen_det.config["data_width"])
        com_det.add_port("FIFO_%i_write"%(FIFO, ), "std_logic", "out")

        if gen_det.config["FIFO_handshakes"]:
            com_det.add_port("FIFO_%i_ready"%(FIFO, ), "std_logic", "in")

    # Handle read ports
    for write in range(gen_det.config["writes"]):
        com_det.add_port("write_%i_addr"%(write, ), "std_logic_vector", "in", gen_det.config["addr_width"])
        com_det.add_port("write_%i_data"%(write, ), "std_logic_vector", "in", gen_det.config["data_width"])
        com_det.add_port("write_%i_enable"%(write, ), "std_logic", "in")

    # Handle stalling ports
    if gen_det.config["stall_type"] != "NONE":
        com_det.add_port("stall_in", "std_logic", "in")

    if   gen_det.config["stall_type"] == "ACTIVE":
        com_det.add_port("stall_out", "std_logic", "out")


def gen_stalling_logic(gen_det, com_det):
    if gen_det.config["stall_type"] != "NONE":
        com_det.arch_head += "signal stall : std_logic;\n"

        if gen_det.config["stall_type"] == "PASSIVE":
            com_det.arch_body += "stall <= stall_in;\n"
        elif gen_det.config["stall_type"] == "ACTIVE":
            com_det.arch_head += "signal FIFOs_ready_buffered : std_logic_vector(%i downto 0);\n"%(gen_det.config["FIFOs"] - 1, )

            reg_interface, reg_name = register.generate_HDL(
                {
                    "has_async_force" : False,
                    "has_sync_force" : False,
                    "has_enable"    : False,
                    "force_on_init" : False
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            com_det.arch_body += "FIFOs_ready_buffer : entity work.%s(arch)\>\n"%(reg_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["FIFOs"], )

            com_det.arch_body += "port map (\n\>"
            com_det.arch_body += "clock => clock,\n"
            com_det.arch_body += "data_in  => (%s),\n"%(
                ", ".join(
                    [
                        "%i => FIFO_%i_ready"%(FIFO, FIFO, )
                        for FIFO in range(gen_det.config["FIFOs"])
                    ]
                )
            )
            com_det.arch_body += "data_out => FIFOs_ready_buffered\n"
            com_det.arch_body += "\<);\n\<\n"



            com_det.arch_head += "signal generated_stall : std_logic;\n"

            com_det.arch_body += "stall <= stall_in or generated_stall;\n"
            com_det.arch_body += "stall_out <= generated_stall;\n"

            # This code may need reworking, depending on how vivado handles many termed logic expressions
            com_det.arch_body += "generated_stall <= %s;\n"%(
                " or ".join([
                    "(FIFO_%i_write_buffer_out and not FIFO_%i_ready)"%(FIFO, FIFO, )
                    for FIFO in range(gen_det.config["FIFOs"])
                ]),
            )

def gen_FIFO_write_logic(gen_det, com_det):
    # Generate FIFO_adv buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : gen_det.config["stall_type"] != "NONE",
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # instance FIFO_adv buffers
    com_det.arch_head += "\n-- FIFO write signals\n"
    com_det.arch_body += "\n-- FIFO write buffers\n"
    for FIFO in range(gen_det.config["FIFOs"]):
        com_det.arch_head += "signal FIFO_%i_write_buffer_in : std_logic;\n"%(FIFO,)
        com_det.arch_head += "signal FIFO_%i_write_buffer_out : std_logic;\n"%(FIFO,)

        com_det.arch_body += "FIFO_%i_write_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        com_det.arch_body += "generic map (data_width => 1)\n"

        com_det.arch_body += "port map (\n\>"
        com_det.arch_body += "clock => clock,\n"
        if gen_det.config["stall_type"] != "NONE":
            com_det.arch_body += "enable => not stall,\n"
        com_det.arch_body += "data_in(0) => FIFO_%i_write_buffer_in,\n"%(FIFO, )
        com_det.arch_body += "data_out(0) => FIFO_%i_write_buffer_out\n"%(FIFO, )
        com_det.arch_body += "\<);\n\<\n"

        if gen_det.config["stall_type"] == "NONE":
            com_det.arch_body += "FIFO_%i_write <= FIFO_%i_write_buffer_out;\n"%(FIFO, FIFO, )
        else:
            com_det.arch_body += "FIFO_%i_write <= FIFO_%i_write_buffer_out and not stall;\n"%(FIFO, FIFO, )

    # FIFO_adv logic
    com_det.arch_body += "\n-- FIFO advance logic\n"
    if gen_det.config["writes"] == 1:
        if gen_det.config["FIFOs"] == 1:
            com_det.arch_body += "FIFO_0_write_buffer_in <= running and write_0_enable;\n"
        else:#gen_det.config["FIFOs"] >= 2:
            for FIFO in range(gen_det.config["FIFOs"]):
                # This code may need reworking, depending on how vivado handles many termed logic expressions
                com_det.arch_body += "FIFO_%i_write_buffer_in <= running and FIFO_%i_ready and write_0_enable and %s;\n"%(
                    FIFO, FIFO,
                    " and ".join([
                        "write_0_addr(%i)"%(bit, ) if FIFO&2**bit
                        else "(not write_0_addr(%i))"%(bit, )
                        for bit in range(gen_det.config["addr_width"])
                    ])
                )
    else:#gen_det.config["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")

def gen_FIFO_data_logic (gen_det, com_det):
    # Generate read_data buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : gen_det.config["stall_type"] != "NONE",
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # Generate FIFO_data buffers
    com_det.arch_head += "\n-- FIFO data signals\n"
    com_det.arch_body += "\n-- FIFO data buffers\n"
    for FIFO in range(gen_det.config["FIFOs"]):
        com_det.arch_head += "signal FIFO_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(FIFO, gen_det.config["data_width"] - 1)

        com_det.arch_body += "FIFO_%i_data_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

        com_det.arch_body += "port map (\n\>"
        if gen_det.config["stall_type"] != "NONE":
            com_det.arch_body += "enable => not stall,\n"
        com_det.arch_body += "clock => clock,\n"
        com_det.arch_body += "data_in  => FIFO_%i_data_buffer_in,\n"%(FIFO, )
        com_det.arch_body += "data_out => FIFO_%i_data\n"%(FIFO, )
        com_det.arch_body += "\<);\n\<\n"

    # FIFO_data assignment logic
    com_det.arch_body += "\n-- FIFO_data assignment logic\n"
    if gen_det.config["writes"] == 1:
        for FIFO in range(gen_det.config["FIFOs"]):
            com_det.arch_body += "FIFO_%i_data_buffer_in <= write_0_data;\n"%(FIFO, )
    else:#gen_det.config["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")
