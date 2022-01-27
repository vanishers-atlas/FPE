# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import itertools as it
import copy

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import alu_dsp48e1 as ALU
from FPE.toolchain.HDL_generation.processor import comm_get as GET
from FPE.toolchain.HDL_generation.processor import comm_put as PUT
from FPE.toolchain.HDL_generation.processor import mem_regfile as REG
from FPE.toolchain.HDL_generation.processor import mem_RAM as RAM
from FPE.toolchain.HDL_generation.processor import mem_ROM as ROM
from FPE.toolchain.HDL_generation.processor import block_access_manager as BAM
from FPE.toolchain.HDL_generation.processor import instruction_decoder as ID
from FPE.toolchain.HDL_generation.processor import program_counter as PC
from FPE.toolchain.HDL_generation.processor import zero_overhead_loop as ZOL

from FPE.toolchain.HDL_generation.basic import delay
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

jump_exe_status_map = {
    "ALU" : {
        "JEQ" : ["equal"],
        "JNE" : ["lesser", "greater"],
        "JLT" : ["lesser"],
        "JLE" : ["equal", "lesser"],
        "JGT" : ["greater"],
        "JGE" : ["equal", "greater"],
    },
}

def precheck_config(config_in):
    config_out = {}

    #####################################################################
    # Precheck and copy input
    #####################################################################

    # Handle SIMD section of config
    config_out["SIMD"] = {}
    config_out["SIMD"] = copy.deepcopy(config_in["SIMD"])
    assert(config_in["SIMD"]["lanes"] >= 0)

    # Handle instr_set section of config
    assert(len(config_in["instr_set"]) > 0)
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])

    # Handle program_flow section of config
    config_out["program_flow"] = {}
    config_out["program_flow"] = copy.deepcopy(config_in["program_flow"])
    assert(config_in["program_flow"]["program_length"] >= 0)
    assert(len(config_in["program_flow"]["ZOLs"]) >= 0)

    # Handle instr_decoder section of config
    config_out["instr_decoder"] = {}
    config_out["instr_decoder"] = copy.deepcopy(config_in["instr_decoder"])
    assert(config_in["instr_decoder"]["opcode_width"] > 0)
    assert(type(config_in["instr_decoder"]["addr_widths"]) == type([]))
    for width in config_in["instr_decoder"]["addr_widths"]:
        assert(width > 0)

    # Handle address_sources section of config
    config_out["address_sources"] = {}
    config_out["address_sources"] = copy.deepcopy(config_in["address_sources"])
    for bam in config_in["address_sources"]:
        assert(config_in["address_sources"][bam]["addr_width"] > 0)
        assert(config_in["address_sources"][bam]["step_width"] > 0)


    # Handle data_memory section of config
    config_out["data_memories"] = {}
    config_out["data_memories"] = copy.deepcopy(config_in["data_memories"])
    assert(len(config_in["data_memories"]) > 0)
    for mem in config_in["data_memories"].keys():
        assert(config_in["data_memories"][mem]["addr_width"] > 0)
        assert(config_in["data_memories"][mem]["data_width"] > 0)

        # Check FIFO_handshakes of comm memories
        if mem in ["GET", "PUT"]:
            assert(type(config_in["data_memories"][mem]["FIFO_handshakes"]) == type(True))

        # Check type of ROM and RAM memories
        if mem in ["ROM_A", "ROM_B", "RAM"]:
            assert(type(config_in["data_memories"][mem]["type"]) == type(""))

    # Handle execute_units section of config
    config_out["execute_units"] = {}
    config_out["execute_units"] = copy.deepcopy(config_in["execute_units"])

    assert(len(config_in["execute_units"]) > 0)
    for exe in config_in["execute_units"].keys():
        assert(config_in["execute_units"][exe]["data_width"] > 0)

    return config_out

#####################################################################

def preprocess_mem_addr_datapath(config, stage, dst_mem):
    addr_datapath = []

    for instr in config["instr_set"].keys():
        if stage == "fetch":
            accesses = asm_utils.instr_fetches(instr)
        elif stage == "store":
            accesses = asm_utils.instr_stores(instr)
        else:
            raise ValueError(stage)

        access_mems = [ asm_utils.access_mem(access) for access in accesses ]
        access_addrs = [ asm_utils.access_addr(access) for access in accesses ]

        # Find all indexes (accesses) that use this mem
        indexes = [i for i, mem in enumerate(access_mems) if mem == dst_mem]

        # Add more accesses if needed
        for _ in range(len(addr_datapath), len(indexes)):
            addr_datapath.append([])

        # Map the found indexes to accesses
        for access, index in  enumerate(indexes):
            # Compute the addr source signal
            src_com = asm_utils.addr_com(access_addrs[index])
            src_port = int(asm_utils.addr_port(access_addrs[index]))
            src_signal = "%s_addr_%i_%s"%(src_com, src_port, stage)


            if not any([
                src_signal == addr["signal"]
                for addr in addr_datapath[access]
            ]):
                if src_com == "ID":
                    src_width = config["instr_decoder"]["addr_widths"][src_port]
                else:
                    src_width = config["address_sources"][src_com]["addr_width"]

                addr_datapath[access].append(
                    {
                        "signal" : src_signal,
                        "com" : src_com,
                        "port" : src_port,
                        "width" : src_width
                    }
                )
    return addr_datapath

def preprocess_mem_data_datapath(config, mem):
    input_datapath = []

    for instr in config["instr_set"].keys():
        exe_unit = asm_utils.instr_exe_unit(instr)

        stores = asm_utils.instr_stores(instr)
        store_mems = [ asm_utils.access_mem(store) for store in stores ]
        store_mods = [ asm_utils.access_mods(store) for store in stores ]

        indexes = [ index for index, store_mem in enumerate(store_mems) if store_mem == mem]

        # Add more inputs if needed
        for _ in range(len(input_datapath), len(indexes)):
            input_datapath.append( [] )

        for write, index in enumerate(indexes):

            # Work out number of words in access, defaulting in 1
            try:
                words = int(store_mods[index]["block_size"])
            except KeyError:
                words = 1


            # Add more words if needed
            for _ in range(len(input_datapath[write]), words):
                input_datapath[write].append( [] )

            for word in range(words):
                assert(word == 0)
                data_signal = "%s_out_%i"%(exe_unit, index, )

                if not any([
                    data_signal == scr["signal"]
                    for scr in input_datapath[write][word]
                ]):
                    input_datapath[write][word].append(
                        {
                            "signal" : data_signal,
                            "com" : exe_unit,
                            "port" : index,
                            "width" : config["execute_units"][exe_unit]["data_width"]
                        }
                    )

    return input_datapath

def preprocess_mem_access_blocks(config, stage, dst_mem):
    access_blocks = set()

    for instr in config["instr_set"].keys():
        if stage == "fetch":
            accesses = asm_utils.instr_fetches(instr)
        elif stage == "store":
            accesses = asm_utils.instr_stores(instr)
        else:
            raise ValueError(stage)

        access_mems  = [ asm_utils.access_mem(access) for access in accesses ]
        access_addrs = [ asm_utils.access_addr(access) for access in accesses ]
        access_mods  = [ asm_utils.access_mods(access) for access in accesses ]


        # Find all indexes (accesses) that use this mem
        indexes = [i for i, mem in enumerate(access_mems) if mem == dst_mem]

        # Add block size of each found accesses
        for access in indexes:
            if "block_size" in access_mods[access]:
                access_blocks.add(int(access_mods[access]["block_size"]))
            else:
                access_blocks.add(1)

    return list(sorted(access_blocks))

#####################################################################
# Functions for preprocessing the data paths of any exe component
# ie. any component that reads fetched/writes stored data
#####################################################################

def preprocess_exe_input_datapath(config, exe):
    input_datapath = []

    for instr in config["instr_set"].keys():
        exe_unit = asm_utils.instr_exe_unit(instr)

        fetches = asm_utils.instr_fetches(instr)
        fetch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]
        fetch_mods = [ asm_utils.access_mods(fetch) for fetch in fetches ]

        if exe == exe_unit:
            # Add more inputs if needed
            for _ in range(len(input_datapath), len(fetch_mems)):
                input_datapath.append( [] )

            # Process each input
            for input, fetch_mem in enumerate(fetch_mems):
                fetch_read = fetch_mems[:input + 1].count(fetch_mem) - 1

                # Work out number of words in access, defaulting in 1
                try:
                    words = int(fetch_mods[input]["block_size"])
                except KeyError:
                    words = 1

                # Add more words if needed
                for _ in range(len(input_datapath[input]), words):
                    input_datapath[input].append( [] )

                for word in range(words):
                    assert(word == 0)
                    data_signal = "%s_read_%i_data"%(fetch_mem, fetch_read, )

                    if not any([
                        data_signal == scr["signal"]
                        for scr in input_datapath[input][word]
                    ]):
                        input_datapath[input][word].append(
                            {
                                "signal" : data_signal,
                                "com" : fetch_mem,
                                "port" : fetch_read,
                                "width" : config["data_memories"][fetch_mem]["data_width"],
                            }
                        )

    return input_datapath

def preprocess_exe_output_datapath(config, exe):
    output_datapaths = []

    for instr in config["instr_set"].keys():
        exe_unit = asm_utils.instr_exe_unit(instr)

        stores = asm_utils.instr_stores(instr)
        store_mems = [ asm_utils.access_mem(store) for store in stores ]
        store_mods = [ asm_utils.access_mods(store) for store in stores ]

        if exe == exe_unit:
            # Add more outputs if needed
            for _ in range(len(output_datapaths), len(store_mems)):
                output_datapaths.append( [] )

            # Process each input
            for output, fetch_mem in enumerate(store_mods):
                store_write = store_mems[:output + 1].count(store_mems) - 1

                # Work out number of words in access, defaulting in 1
                try:
                    words = int(store_mods[output]["block_size"])
                except KeyError:
                    words = 1

                # Add more words if needed
                for _ in range(len(output_datapaths[output]), words):
                    output_datapaths[output].append( [] )

    return output_datapaths


#####################################################################

def preprocess_config(config_in):
    config_out = precheck_config(config_in)

    #####################################################################
    # Process copied Config
    #####################################################################

    # Include standard pipeline stages
    config_out["pipeline_stage"] = ["PC", "PM", "ID", "FETCH", "EXE", "STORE"]

    # Handle SIMD section of config
    if config_out["SIMD"]["lanes"] == 1:
        config_out["SIMD"]["lanes_names"] = [""]
    else:
        config_out["SIMD"]["lanes_names"] = [
            "LANE_%i_"%(l)
             for l in range(CONFIG["SIMD"]["lanes"])
        ]

    # Handle program_flow section of config
    for ZOL in config_out["program_flow"]["ZOLs"].keys():
        ZOL_input = preprocess_exe_input_datapath(config_out, ZOL)
        config_out["program_flow"]["ZOLs"][ZOL]["inputs"] = []
        for data in ZOL_input:
            config_out["program_flow"]["ZOLs"][ZOL]["inputs"].append(
                {
                    "data" : data,
                }
            )

    config_out["program_flow"]["uncondional_jump"] = any([
        asm_utils.instr_mnemonic(instr) == "JMP"
        for instr in config_out["instr_set"].keys()
    ])
    config_out["program_flow"]["statuses"] = {}
    config_out["program_flow"]["inputs"] = []
    pc_input = preprocess_exe_input_datapath(config_out, "PC")
    for data in pc_input:
        config_out["program_flow"]["inputs"].append(
            {
                "data" : data,
            }
        )

    config_out["program_flow"]["stallable"] = False


    # Handle instr_decoder section of config
    config_out["instr_decoder"]["instr_width"] = config_out["instr_decoder"]["opcode_width"] + sum(config_out["instr_decoder"]["addr_widths"])

    # Handle address_sources section of config
    for bam in config_out["address_sources"]:
        config_out["address_sources"][bam]["inputs"] = []
        bam_data = preprocess_exe_input_datapath(config_out, bam)
        for data in bam_data:
            config_out["address_sources"][bam]["inputs"].append(
                {
                    "data" : data,
                }
            )

    # Handle data_memory section of config
    for mem in config_out["data_memories"].keys():
        # Check for stall sources
        if mem in ["GET", "PUT"]:
            if config_out["data_memories"][mem]["FIFO_handshakes"] == True:
                config_out["program_flow"]["stallable"] = True

        # Work out read blocks
        config_out["data_memories"][mem]["read_blocks"] = preprocess_mem_access_blocks(config_out, "fetch", mem)

        # Work out datapaths for fetchs
        # Only need to handle addrs as only inputs are muxed
        config_out["data_memories"][mem]["reads"] = []
        reads_addrs = preprocess_mem_addr_datapath(config_out, "fetch", mem)
        for addr in reads_addrs:
            config_out["data_memories"][mem]["reads"].append(
                {
                    "addr" : addr,
                }
            )

        # Work out read blocks
        config_out["data_memories"][mem]["write_blocks"] = preprocess_mem_access_blocks(config_out, "store", mem)

        # Work out datapaths for stores
        # Need to handle addrs and data as inputs are muxed
        config_out["data_memories"][mem]["writes"] = []
        write_addrs = preprocess_mem_addr_datapath(config_out, "store", mem)
        write_data =  preprocess_mem_data_datapath(config_out, mem)
        for addr, data in zip(
            preprocess_mem_addr_datapath(config_out, "store", mem),
            preprocess_mem_data_datapath(config_out, mem)
        ):
            config_out["data_memories"][mem]["writes"].append(
                {
                    "addr" : addr,
                    "data" : data,
                }
            )

    # Handle execute_units section of config
    for exe in config_out["execute_units"].keys():
        # Work out input datapaths
        config_out["execute_units"][exe]["inputs"] = []
        input_data = preprocess_exe_input_datapath(config_out, exe)
        for data in input_data:
            config_out["execute_units"][exe]["inputs"].append(
                {
                    "data" : data,
                }
            )

        # Work out outputs datapaths
        # Only number of outputs and words needed
        config_out["execute_units"][exe]["outputs"] = []
        output_data = preprocess_exe_output_datapath(config_out, exe)
        for data in output_data:
            config_out["execute_units"][exe]["outputs"].append(
                {
                    "data" : data,
                }
            )

        # Extract execute_unit oper_set,
        # Tell exe unit what oper to implanent
        config_out["execute_units"][exe]["oper_set"] = list( sorted( set(
            [
                exe_lib_lookup[exe].instr_to_oper(instr)
                for instr in config_out["instr_set"].keys()
                if exe == asm_utils.instr_exe_unit(instr)
            ]
        ) ) )

        # Extract statuses execute_unit has to generate
        config_out["execute_units"][exe]["statuses"] = []
        if exe in jump_exe_status_map:
            for instr in config_out["instr_set"].keys():
                if asm_utils.instr_mnemonic(instr) in jump_exe_status_map[exe]:
                    for status in jump_exe_status_map[exe][asm_utils.instr_mnemonic(instr)]:
                        if status not in config_out["execute_units"][exe]["statuses"]:
                            config_out["execute_units"][exe]["statuses"].append(status)

        config_out["program_flow"]["statuses"][exe] = config_out["execute_units"][exe]["statuses"]

        # Set the signal padding option for the execute_unit
        config_out["execute_units"][exe]["signal_padding"] = config_in["signal_padding"]

    # Set the signal padding option
    config_out["signal_padding"] = config_in["signal_padding"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = ""

        raise NotImplementedError()

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
        global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

        # Init generation and return varables
        IMPORTS   = []
        DATAPATHS = gen_utils.init_datapaths()
        CONTROLS = gen_utils.init_controls()
        ARCH_HEAD = gen_utils.indented_string()
        ARCH_BODY = gen_utils.indented_string()
        INTERFACE = {
            "ports" : { },
            "generics" : { },
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generate VHDL
        gen_non_pipelined_signals()
        gen_execute_units()
        gen_data_memories()
        gen_addr_sources()
        gen_predecode_pipeline()
        gen_datapath_muxes()
        gen_instr_decoder()
        gen_running_delays()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_non_pipelined_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    # Create global clock
    INTERFACE["ports"]["clock"] = {
        "direction" : "in",
        "type" : "std_logic",
    }

    # Create and pull down stall signal
    if CONFIG["program_flow"]["stallable"]:
        ARCH_HEAD += "signal stall : std_logic;\n"

#####################################################################

exe_lib_lookup = {
    "ALU" : ALU,
}

exe_predeclared_ports = {
    "clock" : "clock",
    "stall" : "stall",
}

def gen_execute_units():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Exe components\n"

    # Loinstr over all exe components
    for exe, config in CONFIG["execute_units"].items():

        # instantiate exe for each lane
        for lane in CONFIG["SIMD"]["lanes_names"]:
            inst = lane + exe

            # Generate exe code
            if CONCAT_NAMING:
                module_name = MODULE_NAME + "_" + lane + exe
            else:
                module_name = None

            config = exe_lib_lookup[exe].add_inst_config(
                inst,
                CONFIG["instr_set"],
                {
                    **config,
                    "signal_padding" : CONFIG["signal_padding"],
                    "stallable" : CONFIG["program_flow"]["stallable"],
                }
            )
            interface, name = exe_lib_lookup[exe].generate_HDL(
                config,
                OUTPUT_PATH,
                module_name=module_name,
                concat_naming=CONCAT_NAMING,
                force_generation=FORCE_GENERATION
            )

            # OLd way of handling controls, remove once ALU updated to new way
            CONFIG["execute_units"][exe]["controls"] = copy.deepcopy(interface["controls"])

            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, name)

            ARCH_BODY += "port map (\>\n"

            # Handle predeclared ports
            for port, signal in exe_predeclared_ports.items():
                if port in interface["ports"]:
                    ARCH_BODY += "%s => %s,\n"%(port, signal, )

            # Handle non-predeclared ports
            for port in sorted(interface["ports"].keys()):
                if port not in exe_predeclared_ports.keys():
                    detail = interface["ports"][port]
                    try:
                        ARCH_HEAD += "signal %s_%s : %s(%i downto 0);\n"%(inst, port, detail["type"], detail["width"] -1, )
                    except KeyError:
                        ARCH_HEAD += "signal %s_%s : %s;\n"%(inst, port, detail["type"])
                    ARCH_BODY += "%s => %s_%s,\n"%(port, inst, port)

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"
            ARCH_BODY += "\<\n"

            # Handle pathways and controls
            DATAPATHS = gen_utils.merge_datapaths(DATAPATHS, exe_lib_lookup[exe].get_inst_pathways(exe, inst + "_", CONFIG["instr_set"], interface, config, lane) )
            CONTROLS = gen_utils.merge_controls( CONTROLS, exe_lib_lookup[exe].get_inst_controls(exe, inst + "_", CONFIG["instr_set"], interface, config) )


#####################################################################

mem_lib_lookup = {
    "GET" : GET,
    "PUT" : PUT,
    "REG" : REG,
    "RAM" : RAM,
    "IMM" : ROM,
    "ROM_A" : ROM,
    "ROM_B" : ROM,
}

mem_predeclared_ports_all_mems = {
    "clock" : "clock",
    "stall" : "stall",
}

mem_predeclared_ports_per_mem = {
    "GET" : {
        "running" : "running_FETCH",
    },
    "PUT" : {
        "running" : "running_STORE",
    },
    "REG" : { },
    "RAM" : { },
    "IMM" : { },
    "ROM_A" : { },
    "ROM_B" : { },
}


def gen_data_memories():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Memories components\n"
    # loinstr over all data memories
    for mem, config in CONFIG["data_memories"].items():
        for lane in CONFIG["SIMD"]["lanes_names"]:
            # Generate memory code
            if CONCAT_NAMING:
                module_name = MODULE_NAME + "_" + lane + mem
            else:
                module_name = None

            inst = lane + mem

            config = mem_lib_lookup[mem].add_inst_config(
                mem,
                CONFIG["instr_set"],
                {
                    **config,
                    "signal_padding" : CONFIG["signal_padding"],
                    "stallable" : CONFIG["program_flow"]["stallable"],
                }
            )
            sub_interface, sub_name = mem_lib_lookup[mem].generate_HDL(
                config,
                OUTPUT_PATH,
                module_name=module_name,
                concat_naming=CONCAT_NAMING,
                force_generation=FORCE_GENERATION
            )

            # instantiate memory
            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, sub_name)

            if len(sub_interface["generics"]) != 0:
                ARCH_BODY += "generic map (\>\n"

                for generic in sorted(sub_interface["generics"]):
                    details = sub_interface["generics"][generic]
                    INTERFACE["generics"][inst + "_" + generic] = {
                        "type" : details["type"]
                    }
                    ARCH_BODY += "%s => %s_%s,\n"%(generic, inst, generic)

                ARCH_BODY.drop_last_X(2)
                ARCH_BODY += "\<\n)\n"

            ARCH_BODY += "port map (\>\n"

            # Handle predeclared common to all mems ports
            for port, signal in mem_predeclared_ports_all_mems.items():
                if port in sub_interface["ports"]:
                    ARCH_BODY += "%s => %s,\n"%(port, signal, )

            # Handle predeclared for spific mem ports
            for port, signal in mem_predeclared_ports_per_mem[mem].items():
                if port in sub_interface["ports"]:
                    ARCH_BODY += "%s => %s,\n"%(port, signal, )

            # Handle non-predeclared ports
            for port in sorted(sub_interface["ports"].keys()):
                if port not in mem_predeclared_ports_all_mems.keys() and port not in mem_predeclared_ports_per_mem[mem].keys():
                    detail = sub_interface["ports"][port]
                    if port.startswith("FIFO_"):
                        # Handle rippliing FIFO ports:
                        INTERFACE["ports"][inst + "_" + port] = detail
                    else:
                        # handle ports useding internal to FPE
                        try:
                            ARCH_HEAD += "signal %s_%s : %s(%i downto 0);\n"%(inst, port, detail["type"], detail["width"] - 1, )
                        except KeyError:
                            ARCH_HEAD += "signal %s_%s : %s;\n"%(inst, port, detail["type"])
                    # Connect prt
                    ARCH_BODY += "%s => %s_%s,\n"%(port, inst, port)

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"

            ARCH_BODY += "\<\n"

            # Handle pathways and controls
            DATAPATHS = gen_utils.merge_datapaths(DATAPATHS, mem_lib_lookup[mem].get_inst_pathways(mem, inst + "_", CONFIG["instr_set"], sub_interface, config, lane))
            CONTROLS = gen_utils.merge_controls( CONTROLS, mem_lib_lookup[mem].get_inst_controls(mem, inst + "_", CONFIG["instr_set"], sub_interface, config) )

#####################################################################

addr_sources_predeclared_ports = {
    "clock" : "clock" ,
    "stall" : "stall"
}

def gen_addr_sources():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    # Declare data paths for ID addrs
    # needs to happen before ID is generated so ID can be passed the mux controls
    for instr in CONFIG["instr_set"]:
        ID_addr = 0
        for read, access in enumerate(asm_utils.instr_srcs(instr)):
            if asm_utils.addr_com(asm_utils.access_addr(access)) == "ID":
                for lane in CONFIG["SIMD"]["lanes_names"]:
                    gen_utils.add_datapath(DATAPATHS, "%sfetch_addr_%i"%(lane, read), "fetch", True, instr, "ID_addr_%i_fetch"%(ID_addr, ), "unsigned",  CONFIG["instr_decoder"]["addr_widths"][ID_addr])
                ID_addr += 1

        for write, access in enumerate(asm_utils.instr_dests(instr)):
            if asm_utils.addr_com(asm_utils.access_addr(access)) == "ID":
                for lane in CONFIG["SIMD"]["lanes_names"]:
                    gen_utils.add_datapath(DATAPATHS, "%sstore_addr_%i"%(lane, write), "store", True, instr, "ID_addr_%i_store"%(ID_addr, ), "unsigned",  CONFIG["instr_decoder"]["addr_widths"][ID_addr])
                ID_addr += 1

    ARCH_BODY += "\n-- Address components\n"
    for bam, config in CONFIG["address_sources"].items():
        for lane in CONFIG["SIMD"]["lanes_names"]:
            inst = lane + bam

            if CONCAT_NAMING:
                module_name = MODULE_NAME + "_" + lane + bam
            else:
                module_name = None
            config = BAM.add_inst_config(
                bam,
                CONFIG["instr_set"],
                {
                    **config,
                    "signal_padding" : CONFIG["signal_padding"],
                    "stallable" : CONFIG["program_flow"]["stallable"],
                }
            )
            interface, name = BAM.generate_HDL(
                config,
                OUTPUT_PATH,
                module_name=module_name,
                concat_naming=CONCAT_NAMING,
                force_generation=FORCE_GENERATION
            )


            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, name)

            if len(interface["generics"]) != 0:
                ARCH_BODY += "generic map (\>\n"

                for generic in sorted(interface["generics"]):
                    details = interface["generics"][generic]
                    INTERFACE["generics"][bam + "_" + generic] = details
                    ARCH_BODY += "%s => %s_%s,\n"%(generic, bam, generic)

                ARCH_BODY.drop_last_X(2)
                ARCH_BODY += "\<\n)\n"

            ARCH_BODY += "port map (\>\n"

            # Handle predeclared ports
            for port, signal in addr_sources_predeclared_ports.items():
                if port in interface["ports"].keys():
                    ARCH_BODY += "%s => %s,\n"%(port, signal)

            # Handle non predeclared ports
            for port in sorted(interface["ports"].keys()):
                if port not in addr_sources_predeclared_ports.keys():
                    details = interface["ports"][port]
                    try:
                        ARCH_HEAD += "signal %s_%s : %s(%i downto 0);\n"%(bam, port, details["type"], details["width"] - 1, )
                    except KeyError:
                        ARCH_HEAD += "signal %s_%s : %s;\n"%(bam, port, details["type"], )

                    ARCH_BODY += "%s => %s_%s,\n"%(port, bam, port, )

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"

            ARCH_BODY += "\<\n"

            # Handle pathways and controls
            DATAPATHS = gen_utils.merge_datapaths(DATAPATHS, BAM.get_inst_pathways(bam, inst + "_", CONFIG["instr_set"], interface, config, lane) )
            CONTROLS = gen_utils.merge_controls( CONTROLS, BAM.get_inst_controls(bam, inst + "_", CONFIG["instr_set"], interface, config) )



#####################################################################

def gen_predecode_pipeline():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Program fetch components\n"

    gen_program_counter()
    gen_zero_overhead_loops()
    gen_program_memory()

PC_predeclared_ports = {
    "clock" : "clock",
    "kickoff" : "kickoff",
    "ZOL_value" : "overwrite_PC_value_bus",
    "ZOL_overwrite" : "overwrite_PC_enable_bus",
    "stall" : "stall",
    "running" : "running_PC",
}

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_PC"
    else:
        module_name = None

    interface, name = PC.generate_HDL(
        {
            **CONFIG["program_flow"],
            "statuses"  : {
                exe : config["statuses"]
                for exe, config in CONFIG["execute_units"].items()
                if "statuses" in config and len(config["statuses"]) != 0
            },
            "inputs" : [len(words) for words in CONFIG["program_flow"]["inputs"]],
            "signal_padding" : CONFIG["signal_padding"],
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    # Work around for old list versions of interface
    if type(interface["ports"]) == list:
        interface["ports"] = {
            port["name"] : port
            for port in interface["ports"]
        }
    if type(interface["generics"]) == list:
        interface["generics"] = {
            generic["name"] : generic
            for generic in interface["generics"]
        }


    CONFIG["program_flow"]["PC_width"] = interface["PC_width"]

    ARCH_BODY += "\nPC : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"].keys()):
            details = interface["generics"][generic]
            INTERFACE["generics"]["PC_" + generic] = details
            ARCH_BODY += "%s => PC_%s,\n"%(generic, generic)

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    # Handle predeclared ports
    for port, signal in PC_predeclared_ports.items():
        if port in interface["ports"]:
            ARCH_BODY += "%s => %s,\n"%(port, signal)

    # Handle non predeclared ports
    for port in interface["ports"]:
        if port not in PC_predeclared_ports.keys():
            details = interface["ports"][port]
            ARCH_HEAD += "signal PC_%s : %s;\n"%(port, details["type"])
            ARCH_BODY += "%s => PC_%s,\n"%(port, port)

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n\n"

    # Handle kickoff input
    INTERFACE["ports"]["kickoff"] = {
        "type" : "std_logic",
        "direction" : "in"
    }

    # Handle jump status ports
    for port in interface["ports"]:
        if "_status_" in port:
            ARCH_BODY += "PC_%s <= %s;\n"%(port, port)

# Key is port name, value signal name
ZOL_predeclared_ports = {
    "clock" : "clock",
    "stall" : "stall",
    "PC_value" : "PC_value",
    "PC_running" : "running_PC",
    "overwrite_PC_enable" : "overwrite_PC_enable_bus",
    "overwrite_PC_value" : "overwrite_PC_value_bus",
}

ZOL_declared_ports = [
    "seek_check_value", "seek_overwrite_value", "seek_enable",
    "set_overwrites", "set_enable",
]

def gen_zero_overhead_loops():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    if len(CONFIG["program_flow"]["ZOLs"]) != 0:
        INTERFACE["ZOL_overwrites_encoding"] = {}

        # Pull ZOL bused to defauly values
        ARCH_HEAD += "signal overwrite_PC_value_bus  : std_logic_vector(%i downto 0) := (others => 'L');\n"%(CONFIG["program_flow"]["PC_width"] - 1, )
        ARCH_HEAD += "signal overwrite_PC_enable_bus : std_logic := 'L';\n"

    # Generate ZOL hardward
    for ZOL_name, ZOL_details in CONFIG["program_flow"]["ZOLs"].items():
        if CONCAT_NAMING:
            module_name = MODULE_NAME + "_" + ZOL_name
        else:
            module_name = None

        ZOL_details = ZOL.add_inst_config(ZOL_name, CONFIG["instr_set"], ZOL_details)
        interface, name = ZOL.generate_HDL(
            {
                **ZOL_details,
                "PC_width"  : CONFIG["program_flow"]["PC_width"],
                "signal_padding" : CONFIG["signal_padding"],
                "stallable" : CONFIG["program_flow"]["stallable"],
            },
            OUTPUT_PATH,
            module_name=module_name,
            concat_naming=CONCAT_NAMING,
            force_generation=FORCE_GENERATION
        )
        INTERFACE["ZOL_overwrites_encoding"][ZOL_name] = interface["overwrites_encoding"]


        ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(ZOL_name, name)

        if len(interface["generics"]) != 0:
            ARCH_BODY += "generic map (\>\n"

            for generic in sorted(interface["generics"].keys()):
                details = interface["generics"][generic]
                INTERFACE["generics"][ZOL_name + "_" + generic] = details
                ARCH_BODY += "%s => %s_%s,\n"%(generic, ZOL_name, generic)

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\>\n"

        if __debug__:
            for port in interface["ports"]:
                assert (    port in ZOL_predeclared_ports.keys()
                        or  port in ZOL_declared_ports
                    ), "Unknown Port, " + port

        # Handle predeclared ports
        for port, signal in ZOL_predeclared_ports.items():
            if port in interface["ports"]:
                ARCH_BODY += "%s => %s,\n"%(port, signal)

        # Handle declared ports
        for port in ZOL_declared_ports:
            if port in interface["ports"]:
                details = interface["ports"][port]
                try:
                    ARCH_HEAD += "signal %s_%s : %s(%i downto 0);\n"%(ZOL_name, port, details["type"], details["width"] - 1, )
                except KeyError:
                    ARCH_HEAD += "signal %s_%s : %s;\n"%(ZOL_name, port, details["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port, ZOL_name, port)

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"

        ARCH_BODY += "\<\n\n"

        # Handle pathways and controls
        DATAPATHS = gen_utils.merge_datapaths(DATAPATHS,ZOL.get_inst_pathways(ZOL_name, ZOL_name + "_", CONFIG["instr_set"], interface, ZOL_details, CONFIG["SIMD"]["lanes_names"][0]))
        CONTROLS = gen_utils.merge_controls( CONTROLS, ZOL.get_inst_controls(ZOL_name, ZOL_name + "_", CONFIG["instr_set"], interface, ZOL_details) )

def gen_program_memory():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_PM"
    else:
        module_name = None

    interface, name = ROM.generate_HDL(
        {
            "depth" : CONFIG["program_flow"]["program_length"],
            "addr_width" : CONFIG["program_flow"]["PC_width"],
            "data_width" : CONFIG["instr_decoder"]["instr_width"],
            "read_blocks" : [1],
            "type" : "DIST",
            "reads" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "\nPM : entity work.%s(arch)\>\n"%(name)

    INTERFACE["generics"]["PM_init_mif"] = {
        "type" : "string"
    }

    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "init_mif => PM_init_mif\n"
    ARCH_BODY += "\<)\n"

    ARCH_HEAD += "signal PM_addr : std_logic_vector(%i downto 0);\n"%( CONFIG["program_flow"]["PC_width"] - 1)
    ARCH_HEAD += "signal PM_data : std_logic_vector(%i downto 0);\n"%( CONFIG["instr_decoder"]["instr_width"] - 1)

    ARCH_BODY += "port map (\>\n"
    ARCH_BODY += "clock => clock,\n"
    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"
    ARCH_BODY += "read_0_addr => PM_addr,\n"
    ARCH_BODY += "read_0_data => PM_data\n"
    ARCH_BODY += "\<);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "PM_addr <= PC_value;\n"

#####################################################################

def gen_datapath_muxes():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    mux_controls, ARCH_HEAD, ARCH_BODY = gen_utils.gen_datapath_muxes(DATAPATHS, OUTPUT_PATH, FORCE_GENERATION, ARCH_HEAD, ARCH_BODY)
    CONTROLS = gen_utils.merge_controls(CONTROLS, mux_controls)

#####################################################################

ID_predeclared_ports = {
    "clock" : "clock",
    "stall" : "stall"
}

ID_non_fanout_ports = [
    "instr",
    "enable",
]

def gen_instr_decoder():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY
    global CONTROLS

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_ID"
    else:
        module_name = None

    interface, name = ID.generate_HDL(
        {
            **CONFIG,
            "controls" : CONTROLS
        },
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "\nID : entity work.%s(arch)\>\n"%(name, )

    ARCH_BODY += "port map (\>\n"

    # Handle predeclared ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] in ID_predeclared_ports.keys()
        ],
        key=lambda d : d["name"]
    ):
        ARCH_BODY += "%s => %s,\n"%(port["name"], ID_predeclared_ports[port["name"]])

    # Handle prefixed ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] not in ID_predeclared_ports.keys()
        ],
        key=lambda d : d["name"]
    ):
        ARCH_HEAD += "signal ID_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => ID_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "ID_instr <= PM_data;\n"
    ARCH_BODY += "ID_enable <= running_ID;\n"

    # Handle PC control signals
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if (
                port["name"].startswith("jump_")
                or (port["name"].startswith("update_") and port["name"].endswith("_statuses"))
            )
        ],
        key=lambda d : d["name"]
    ):
        ARCH_BODY += "PC_%s <= ID_%s;\n"%(port["name"], port["name"])

    # Handle fanning out control signals
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if (
                port["name"] not in ID_predeclared_ports.keys()
                and port["name"] not in ID_non_fanout_ports
                and not port["name"].startswith("addr_")
                and not port["name"].startswith("jump_")
                and not (port["name"].startswith("update_") and port["name"].endswith("_statuses"))
            )
        ],
        key=lambda d : d["name"]
    ):
        for lane in CONFIG["SIMD"]["lanes_names"]:
            ARCH_BODY += "%s%s <= ID_%s;\n"%(lane, port["name"], port["name"])

#####################################################################

def gen_running_delays():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    # Declare each stage's running signal
    for stage in CONFIG["pipeline_stage"]:
        ARCH_HEAD += "signal running_%s : std_logic;\n"%(stage, )

    DELAY_INTERFACE, DELAY_NAME = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    for i, (stage_in, stage_out) in enumerate(zip(CONFIG["pipeline_stage"][:-1], CONFIG["pipeline_stage"][1:])):
        ARCH_BODY += "running_delay_%i : entity work.%s(arch)\>\n"%(i, DELAY_NAME, )

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["program_flow"]["stallable"]:
            ARCH_BODY += "stall => stall,\n"
        ARCH_BODY += "data_in (0) => running_%s,\n"%(stage_in, )
        ARCH_BODY += "data_out(0) => running_%s\n"%(stage_out, )
        ARCH_BODY += "\<);\<\n\n"

    # Handle running output
    INTERFACE["ports"]["running"] = {
        "type" : "std_logic",
        "direction" : "out"
    }
    ARCH_BODY += "running <= running_PC;\n\n"
