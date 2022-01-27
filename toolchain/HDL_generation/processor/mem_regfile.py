# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    reads = 0
    for instr in instr_set:
        fetch_mems = [ asm_utils.access_mem(access) for access in asm_utils.instr_fetches(instr) ]
        reads = max(reads, fetch_mems.count(instr_id))
    config["reads"] = reads

    writes = 0
    for instr in instr_set:
        store_mems = [ asm_utils.access_mem(access) for access in asm_utils.instr_stores(instr) ]
        writes = max(writes, store_mems.count(instr_id))
    config["writes"] = writes

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = { }

    for instr in instr_set:
        read = 0
        for access in asm_utils.instr_fetches(instr):
            if asm_utils.access_mem(access) == instr_id:
                # Handle fetch addr
                gen_utils.add_datapath(pathways, "%sfetch_addr_%i"%(lane, read), "fetch", False, instr, "%sread_%i_addr"%(instr_prefix, read, ), "unsigned", config["addr_width"])

                # Handle fetch data
                gen_utils.add_datapath(pathways, "%sfetch_data_%i"%(lane, read), "exe", True, instr, "%sread_%i_data"%(instr_prefix, read, ), config["signal_padding"], config["data_width"])

                read += 1

        write = 0
        for access in asm_utils.instr_stores(instr):
            if asm_utils.access_mem(access) == instr_id:
                # Handle store addr
                gen_utils.add_datapath(pathways, "%sstore_addr_%i"%(lane, write), "store", False, instr, "%swrite_%i_addr"%(instr_prefix, write, ), "unsigned", config["addr_width"])

                # Handle store data
                gen_utils.add_datapath(pathways, "%sstore_data_%i"%(lane, write), "store", False, instr, "%swrite_%i_data"%(instr_prefix, write, ), config["signal_padding"], config["data_width"])

                write += 1

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(type(config_in["read_blocks"]) == type([]))
    config_out["read_blocks"] = []
    for block_write in config_in["read_blocks"]:
        assert(block_write >= 1)
        config_out["read_blocks"].append(block_write)

    assert(config_in["writes"] >= 1)
    config_out["writes"] = config_in["writes"]

    assert(type(config_in["write_blocks"]) == type([]))
    config_out["write_blocks"] = []
    for block_write in config_in["write_blocks"]:
        assert(block_write >= 1)
        config_out["write_blocks"].append(block_write)

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "REG"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

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
        INTERFACE = { "ports" : { }, "generics" : { }, }

        # Include extremely commom libs
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

        # Generation Module Code
        INTERFACE["ports"]["clock"] = {
            "type" : "std_logic",
            "direction" : "in"
        }
        if CONFIG["stallable"]:
            INTERFACE["ports"]["stall"] = {
                "type" : "std_logic",
                "direction" : "in"
            }

        gen_registers()
        gen_reads()
        gen_writes()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_registers():
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

    ARCH_HEAD += "-- Register signals\n"
    ARCH_BODY += "-- Registers\n"

    for reg in range(CONFIG["depth"]):
        ARCH_HEAD += "signal reg_%i_in  : std_logic_vector(%i downto 0);\n"%(reg, CONFIG["data_width"] - 1)
        ARCH_HEAD += "signal reg_%i_out : std_logic_vector(%i downto 0);\n"%(reg, CONFIG["data_width"] - 1)
        ARCH_HEAD += "signal reg_%i_enable : std_logic;\n"%(reg, )

        ARCH_BODY += "reg_%i : entity work.%s(arch)\>\n"%(reg, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"], )
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "enable  => reg_%i_enable,\n"%(reg, )
        ARCH_BODY += "data_in  => reg_%i_in,\n"%(reg, )
        ARCH_BODY += "data_out => reg_%i_out\n"%(reg, )
        ARCH_BODY += "\<);\n\<\n"

def gen_reads():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : CONFIG["stallable"],
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "-- Read buffers\n"

    for read in range(CONFIG["reads"]):
        # Declare port
        INTERFACE["ports"]["read_%i_addr"%(read, )] = {
                "type" : "std_logic_vector",
                "width": CONFIG["addr_width"],
                "direction" : "in",
        }
        INTERFACE["ports"]["read_%i_data"%(read, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["data_width"],
            "direction" : "out",
        }


        # Generate output buffers
        ARCH_HEAD += "signal read_%i_buffer_in : std_logic_vector(%i downto 0);\n"%(read, CONFIG["data_width"] - 1)

        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"

        if CONFIG["stallable"]:
            ARCH_BODY += "enable  => not stall,\n"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => read_%i_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )

        ARCH_BODY += "\<);\n\<"

        ARCH_BODY += "read_%i_buffer_in <=\>"%(read, )
        for reg in range(CONFIG["depth"]):
            ARCH_BODY += "reg_%i_out when read_%i_addr = \"%s\"\nelse "%(reg, read, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
        ARCH_BODY += "(others => 'X');\n\<"

        ARCH_BODY += "\n"

def gen_writes():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for write in range(CONFIG["writes"]):
        # Declare port
        INTERFACE["ports"]["write_%i_addr"%(write, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["addr_width"],
            "direction" : "in",
        }
        INTERFACE["ports"]["write_%i_data"%(write, )] = {
            "type" : "std_logic_vector",
            "width": CONFIG["data_width"],
            "direction" : "in",
        }
        INTERFACE["ports"]["write_%i_enable"%(write, )] = {
            "type" : "std_logic",
            "direction" : "in",
        }

    if CONFIG["writes"] == 1:
        for reg in range(CONFIG["depth"]):
            ARCH_BODY += "reg_%i_in <= write_0_data;\n"%(reg, )
            if CONFIG["stallable"]:
                ARCH_BODY += "reg_%i_enable <= write_0_enable and not stall when write_0_addr = \"%s\" else '0';\n"%(reg, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
            else:
                ARCH_BODY += "reg_%i_enable <= write_0_enable when write_0_addr = \"%s\" else '0';\n"%(reg, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
    else:
        raise NotImplementedError()
