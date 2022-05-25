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
        INTERFACE = { "ports" : {}, "generics" : {} }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        gen_ports()
        gen_stalling_logic()
        gen_FIFO_data_logic()
        gen_FIFO_write_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Decalre clock and runnning ports
    INTERFACE["ports"]["clock"] = {
        "type" : "std_logic",
        "direction" : "in",
    }
    INTERFACE["ports"]["running"] = {
        "type" : "std_logic",
        "direction" : "in",
    }

    # Handle FIFO ports
    for FIFO in range(CONFIG["FIFOs"]):
        INTERFACE["ports"]["FIFO_%i_data"%(FIFO, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["data_width"],
            "direction" : "out"
        }
        INTERFACE["ports"]["FIFO_%i_write"%(FIFO, )] = {
            "type" : "std_logic",
            "direction" : "out"
        }
        if CONFIG["FIFO_handshakes"]:
            INTERFACE["ports"]["FIFO_%i_ready"%(FIFO, )] = {
                "type" : "std_logic",
                "direction" : "in"
            }

    # Handle read ports
    for write in range(CONFIG["writes"]):
        INTERFACE["ports"]["write_%i_addr"%(write, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["addr_width"],
            "direction" : "in",
        }
        INTERFACE["ports"]["write_%i_data"%(write, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["data_width"],
            "direction" : "in"
        }
        INTERFACE["ports"]["write_%i_enable"%(write, )] = {
            "type" : "std_logic",
            "direction" : "in"
        }

    # Handle stalling ports
    if CONFIG["stall_type"] != "NONE":
        INTERFACE["ports"]["stall_in"] = {
            "type" : "std_logic",
            "direction" : "in"
        }
    if   CONFIG["stall_type"] == "ACTIVE":
        INTERFACE["ports"]["stall_out"] = {
            "type" : "std_logic",
            "direction" : "inout"
        }

def gen_stalling_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONFIG["stall_type"] != "NONE":
        ARCH_HEAD += "signal stall : std_logic;\n"

        if CONFIG["stall_type"] == "PASSIVE":
            ARCH_BODY += "stall <= stall_in;\n"
        elif CONFIG["stall_type"] == "ACTIVE":
            ARCH_HEAD += "signal FIFOs_ready_buffered : std_logic_vector(%i downto 0);\n"%(CONFIG["FIFOs"] - 1, )

            reg_interface, reg_name = register.generate_HDL(
                {
                    "has_async_force" : False,
                    "has_sync_force" : False,
                    "has_enable"    : False,
                    "force_on_init" : False
                },
                OUTPUT_PATH,
                module_name=None,
                concat_naming=False,
                force_generation=FORCE_GENERATION
            )

            ARCH_BODY += "FIFOs_ready_buffer : entity work.%s(arch)\>\n"%(reg_name, )

            ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["FIFOs"], )

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in  => (%s),\n"%(
                ", ".join(
                    [
                        "%i => FIFO_%i_ready"%(FIFO, FIFO, )
                        for FIFO in range(CONFIG["FIFOs"])
                    ]
                )
            )
            ARCH_BODY += "data_out => FIFOs_ready_buffered\n"
            ARCH_BODY += "\<);\n\<\n"



            ARCH_HEAD += "signal generated_stall : std_logic;\n"

            ARCH_BODY += "stall <= stall_in or generated_stall;\n"
            ARCH_BODY += "stall_out <= generated_stall;\n"

            # This code may need reworking, depending on how vivado handles many termed logic expressions
            ARCH_BODY += "generated_stall <= %s;\n"%(
                " or ".join([
                    "(FIFO_%i_write_buffer_out and not FIFOs_ready_buffered(%i))"%(FIFO, FIFO, )
                    for FIFO in range(CONFIG["FIFOs"])
                ]),
            )

def gen_FIFO_write_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate FIFO_adv buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : CONFIG["stall_type"] != "NONE",
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    # instance FIFO_adv buffers
    ARCH_HEAD += "\n-- FIFO write signals\n"
    ARCH_BODY += "\n-- FIFO write buffers\n"
    for FIFO in range(CONFIG["FIFOs"]):
        ARCH_HEAD += "signal FIFO_%i_write_buffer_in : std_logic;\n"%(FIFO,)
        ARCH_HEAD += "signal FIFO_%i_write_buffer_out : std_logic;\n"%(FIFO,)

        ARCH_BODY += "FIFO_%i_write_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        ARCH_BODY += "generic map (data_width => 1)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["stall_type"] != "NONE":
            ARCH_BODY += "enable => not stall,\n"
        ARCH_BODY += "data_in(0) => FIFO_%i_write_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out(0) => FIFO_%i_write_buffer_out\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<\n"

        if CONFIG["stall_type"] == "NONE":
            ARCH_BODY += "FIFO_%i_write <= FIFO_%i_write_buffer_out;\n"%(FIFO, FIFO, )
        else:
            ARCH_BODY += "FIFO_%i_write <= FIFO_%i_write_buffer_out and not stall;\n"%(FIFO, FIFO, )

    # FIFO_adv logic
    ARCH_BODY += "\n-- FIFO advance logic\n"
    if CONFIG["writes"] == 1:
        if CONFIG["FIFOs"] == 1:
            ARCH_BODY += "FIFO_0_write_buffer_in <= running and write_0_enable;\n"
        else:#CONFIG["FIFOs"] >= 2:
            for FIFO in range(CONFIG["FIFOs"]):
                # This code may need reworking, depending on how vivado handles many termed logic expressions
                ARCH_BODY += "FIFO_%i_write_buffer_in <= running and FIFO_%i_ready and write_0_enable and %s;\n"%(
                    FIFO, FIFO,
                    " and ".join([
                        "write_0_addr(%i)"%(bit, ) if FIFO&2**bit
                        else "(not write_0_addr(%i))"%(bit, )
                        for bit in range(CONFIG["addr_width"])
                    ])
                )
    else:#CONFIG["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")

def gen_FIFO_data_logic ():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate read_data buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"    : CONFIG["stall_type"] != "NONE",
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    # Generate FIFO_data buffers
    ARCH_HEAD += "\n-- FIFO data signals\n"
    ARCH_BODY += "\n-- FIFO data buffers\n"
    for FIFO in range(CONFIG["FIFOs"]):
        ARCH_HEAD += "signal FIFO_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(FIFO, CONFIG["data_width"] - 1)

        ARCH_BODY += "FIFO_%i_data_buffer : entity work.%s(arch)\>\n"%(FIFO, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"
        if CONFIG["stall_type"] != "NONE":
            ARCH_BODY += "enable => not stall,\n"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => FIFO_%i_data_buffer_in,\n"%(FIFO, )
        ARCH_BODY += "data_out => FIFO_%i_data\n"%(FIFO, )
        ARCH_BODY += "\<);\n\<\n"

    # FIFO_data assignment logic
    ARCH_BODY += "\n-- FIFO_data assignment logic\n"
    if CONFIG["writes"] == 1:
        for FIFO in range(CONFIG["FIFOs"]):
            ARCH_BODY += "FIFO_%i_data_buffer_in <= write_0_data;\n"%(FIFO, )
    else:#CONFIG["writes"] >  1:
        raise NotImplementedError("Support for 2+ writes needs adding")
