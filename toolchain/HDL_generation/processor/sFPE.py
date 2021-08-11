# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain import FPE_assembly as asm_utils

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

from FPE.toolchain.HDL_generation.basic import delay, mux, dist_ROM

import itertools as it
import copy

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

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = ""

        raise NotImplementedError()

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name, generate_name=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = preprocess_config(config)
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, CONFIG, generate_name)
    GENERATE_NAME = generate_name
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
        INTERFACE = { "ports" : [], "generics" : [] }

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
        gen_program_fetch()
        gen_instr_decoder()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_non_pipelined_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Create global clock
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]

    # Create and pull down stall signal
    if CONFIG["program_flow"]["stallable"]:
        ARCH_HEAD += "signal stall : std_logic;\n"
        ARCH_BODY += "stall <= 'L';\n"

#####################################################################

def mux_signals(lane, dst_sig, dst_width, srcs, signal_padding):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle case of only 1 source, ie an unmuxed connection
    if len(srcs) == 1:
        ARCH_BODY += "%s <= %s;\n"%(
            dst_sig,
            gen_utils.connect_signals(
                srcs[0]["signal"],
                srcs[0]["width"],
                dst_width,
                signal_padding
            )
        )
    # Handle case of multiple sources, ie a muxed connection
    else:
        # Determine mux sel port width
        # - 1 to go from number of inputs to largest sel value
        sel_width = tc_utils.unsigned.width(len(srcs) - 1)
        sel_sig = dst_sig + "_sel"
        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(sel_sig, sel_width - 1)

        # Imply mux via VHDL condissional assignment of input signal
        ARCH_BODY += "%s <=\>"%(dst_sig, )
        for sel_val, src in enumerate( sorted( srcs, key=lambda d : d["signal"] ) ):
            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                gen_utils.connect_signals(lane + src["signal"], src["width"], dst_width, signal_padding),
                sel_sig,
                tc_utils.unsigned.encode(sel_val, sel_width),
            )
        ARCH_BODY += "(others => 'U');\<\n"

#####################################################################

exe_predeclared_ports = [
    "clock",
    "stall"
]

exe_lib_lookup = {
    "ALU" : ALU,
}

def gen_execute_units():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Exe components\n"

    CONFIG["exe_stages"] = 0

    # Loinstr over all exe components
    for exe, config in CONFIG["execute_units"].items():

        # Generate exe code
        interface, name = exe_lib_lookup[exe].generate_HDL(
            {
                **config,
                "inputs" : len(config["inputs"]),
                "outputs" : len(config["outputs"]),
                "oper_set" : config["oper_set"],
                "stallable" : CONFIG["program_flow"]["stallable"],
            },
            OUTPUT_PATH,
            exe,
            True,
            FORCE_GENERATION
        )

        # Store exe details
        config["controls"] = copy.deepcopy(interface["controls"])

        # instantiate exe for each lane
        for lane in CONFIG["SIMD"]["lanes_names"]:
            inst = lane + exe

            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, name)

            ARCH_BODY += "port map (\>\n"

            # Handle predeclared ports
            for port in sorted(
                [
                    port
                    for port in interface["ports"]
                    if port["name"] in exe_predeclared_ports
                ],
                key=lambda d : d["name"]
            ):
                ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

            # Handle prefixed ports
            for port in sorted(
                [
                    port
                    for port in interface["ports"]
                    if port["name"] not in exe_predeclared_ports
                ],
                key=lambda d : d["name"]
            ):
                ARCH_HEAD += "signal %s_%s : %s;\n"%(inst, port["name"], port["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port["name"], inst, port["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"
            ARCH_BODY += "\<\n"

        # Create input port muxes
        for input, channels in enumerate(config["inputs"]):
            for word, srcs  in enumerate(channels["data"]):
                assert(word == 0)
                dst_sig = "%s%s_in_%i"%(lane, exe, input, )
                mux_signals(lane, dst_sig, config["data_width"], srcs, CONFIG["signal_padding"])


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

mem_predeclared_ports = [
    "clock",
    "stall"
]

def inst_data_memory(lane, mem, config, comp, interface):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    inst = lane + mem

    # instantiate memory
    ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, comp)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"]):
            INTERFACE["generics"] += [
                {
                    "name" : inst + "_" + generic["name"],
                    "type" : generic["type"]
                }
            ]
            ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], inst, generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    # Handle non prefixed ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] in mem_predeclared_ports
        ],
        key=lambda d : d["name"]
    ):
        ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

    # Handle prefixed ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] not in mem_predeclared_ports
        ],
        key=lambda d : d["name"]
    ):
        if port["name"].startswith("FIFO_"):
            # Handle rippliing FIFO ports to tinstr level:
            INTERFACE["ports"] += [
                {
                    "name" : inst + "_" + port["name"],
                    "type" : port["type"],
                    "direction" : port["direction"]
                }
            ]
        else:
            # handle ports useding internal to FPE
            ARCH_HEAD += "signal %s_%s : %s;\n"%(inst, port["name"], port["type"])
        # Connect prt
        ARCH_BODY += "%s => %s_%s,\n"%(port["name"], inst, port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"
    # Create read addr port muxes
    for read, signals in enumerate(config["reads"]):
        # Handle Addr signals
        dst_sig = inst + "_read_%i_addr"%(read,)
        mux_signals(lane, dst_sig, config["addr_width"], signals["addr"], "unsigned")

    # Create write port muxes
    for write, signals in enumerate(config["writes"]):
        # Handle Addr signals
        dst_sig = inst + "_write_%i_addr"%(write,)
        mux_signals(lane, dst_sig, config["addr_width"], signals["addr"], "unsigned")

        # Data port
        for word, details in enumerate(signals["data"]):
            assert(word == 0)
            dst_sig = inst + "_write_%i_data"%(write, )
            mux_signals(lane, dst_sig, config["data_width"], details, CONFIG["signal_padding"])

def gen_data_memories():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Memories components\n"
    # loinstr over all data memories
    for mem, config in CONFIG["data_memories"].items():

        # Generate memory code
        interface, name = mem_lib_lookup[mem].generate_HDL(
            {
                **config,
                "reads" : len(config["reads"]),
                "writes" : len(config["writes"]),
                "stallable" : CONFIG["program_flow"]["stallable"],
            },
            OUTPUT_PATH,
            mem,
            True,
            FORCE_GENERATION
        )

        # Handle shared (across lanes) memories
        if mem in ["IMM"]:
            inst_data_memory("", mem, config, name, interface)

            # Fan read data signals to each lane
            if len(CONFIG["SIMD"]["lanes_names"]) < 1:
                raise NotImplementedError()
        # Handle private (to each lane) memories
        else:
            # Repeat instantiation for each lane
            for lane in CONFIG["SIMD"]["lanes_names"]:
                inst_data_memory(lane, mem, config, name, interface)

#####################################################################

addr_sources_predeclared_ports = [
    "clock",
    "stall"
]

def gen_addr_sources():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Address components\n"
    for bam, config in CONFIG["address_sources"].items():
        interface, name = BAM.generate_HDL(
            {
                **config,
                "inputs" : [len(words) for words in config["inputs"]],
                "stallable" : CONFIG["program_flow"]["stallable"],
            },
            OUTPUT_PATH,
            "BAM",
            True,
            FORCE_GENERATION
        )

        ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(bam, name)

        if len(interface["generics"]) != 0:
            ARCH_BODY += "generic map (\>\n"

            for generic in sorted(interface["generics"], key=lambda p : p["name"]):
                INTERFACE["generics"] += [
                    {
                        "name" : bam + "_" + generic["name"],
                        "type" : generic["type"]
                    }
                ]
                ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], bam, generic["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\>\n"

        # Handle predeclared ports
        for port in sorted(
            [
                port for port in interface["ports"]
                if port["name"] in addr_sources_predeclared_ports
            ],
            key=lambda p : p["name"]
        ):
            ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

        # Handle non predeclared ports
        for port in sorted(
            [
                port for port in interface["ports"]
                if port["name"] not in addr_sources_predeclared_ports
            ],
            key=lambda p : p["name"]
        ):
            ARCH_HEAD += "signal %s_%s : %s;\n"%(bam, port["name"], port["type"])
            ARCH_BODY += "%s => %s_%s,\n"%(port["name"], bam, port["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"

        ARCH_BODY += "\<\n"


        # Create input port muxes
        for input, channels in enumerate(config["inputs"]):
            for word, srcs  in enumerate(channels["data"]):
                assert(word == 0)
                dst_sig = "%s_in_%i"%(bam, input, )
                # Only use lane 0 as BAM as shared across lanes
                mux_signals(CONFIG["SIMD"]["lanes_names"][0], dst_sig, config["step_width"], srcs, "unsigned")

#####################################################################

def gen_program_fetch():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Program fetch components\n"

    gen_program_counter()
    if len( CONFIG["program_flow"]["ZOLs"]) != 0:
        gen_zero_overhead_loop()
    gen_program_memory()

PC_predeclared_ports = [
    "clock",
    "kickoff",
    "stall",
    "ZOL_value",
    "ZOL_overwrite",
]

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = PC.generate_HDL(
        {
            **CONFIG["program_flow"],
            "statuses"  : {
                exe : config["statuses"]
                for exe, config in CONFIG["execute_units"].items()
                if "statuses" in config and len(config["statuses"]) != 0
            },
            "inputs" : [len(words) for words in CONFIG["program_flow"]["inputs"]],
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        MODULE_NAME + "_PC",
        True,
        FORCE_GENERATION
    )

    CONFIG["program_flow"]["PC_width"] = interface["PC_width"]

    ARCH_BODY += "\nPC : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda p : p["name"]):
            INTERFACE["generics"] += [ { "name" : "PC_" + generic["name"], "type" : generic["type"] } ]
            ARCH_BODY += "%s => PC_%s,\n"%(generic["name"], generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    # Handle predefined ports
    for port in [
        port
        for port in interface["ports"]
        if port["name"] in PC_predeclared_ports
    ]:
        ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

    # Handle non predefined ports
    for port in [
        port
        for port in interface["ports"]
        if port["name"] not in PC_predeclared_ports
    ]:
        ARCH_HEAD += "signal PC_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => PC_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n\n"

    # Handle kickoff input
    INTERFACE["ports"] += [
        {
            "name" : "kickoff",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]

    # Handle running output
    INTERFACE["ports"] += [
        {
            "name" : "running",
            "type" : "std_logic",
            "direction" : "out"
        }
    ]
    ARCH_BODY += "running <= PC_running;\n\n"

    # Create input port muxes
    for input, channels in enumerate(CONFIG["program_flow"]["inputs"]):
        for word, srcs  in enumerate(channels["data"]):
            assert(word == 0)
            dst_sig = "%s_in_%i"%("PC", input, )
            mux_signals(CONFIG["SIMD"]["lanes_names"][0], dst_sig, CONFIG["program_flow"]["PC_width"], srcs, "unsigned")

    # Handle jump status ports
    for port in [port for port in interface["ports"] if "_status_" in port["name"] ]:
        ARCH_BODY += "PC_%s <= %s;\n"%(port["name"], port["name"])

    # delay PC'c running signal to act as ID enable
    DELAY_INTERFACE, DELAY_NAME = delay.generate_HDL(
        {
            "width" : 1,
            # delay of 1 for PC's setup cycle
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_HEAD += "signal PC_running_1, PC_running_2 : std_logic;\n"

    ARCH_BODY += "PC_running_delay_0 : entity work.%s(arch)\>\n"%(DELAY_NAME)

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"
    ARCH_BODY += "data_in (0) => PC_running,\n"
    ARCH_BODY += "data_out(0) => PC_running_1\n"
    ARCH_BODY += "\<);\<\n\n"

    ARCH_BODY += "PC_running_delay_1 : entity work.%s(arch)\>\n"%(DELAY_NAME)

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"
    ARCH_BODY += "data_in (0) => PC_running_1,\n"
    ARCH_BODY += "data_out(0) => PC_running_2\n"
    ARCH_BODY += "\<);\<\n\n"

ZOL_predeclared_ports = [
    "clock",
    "PC_running",
    "PC_value",
    "overwrite",
    "overwrite_value",
    "stall",
]

def gen_zero_overhead_loop():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if len(CONFIG["program_flow"]["ZOLs"]) != 0:
        INTERFACE["ZOL_iterations_encoding"] = {}

        # Pull ZOL bused to defauly values
        ARCH_HEAD += "signal ZOL_value : std_logic_vector(%i downto 0) := (others => 'L');\n"%(CONFIG["program_flow"]["PC_width"] - 1, )
        ARCH_HEAD += "signal ZOL_overwrite : std_logic := 'L';\n"

        # Generate ZOL hardward
        for ZOL_name, ZOL_details in CONFIG["program_flow"]["ZOLs"].items():
            interface, name = ZOL.generate_HDL(
                {
                    **ZOL_details,
                    "PC_width"  : CONFIG["program_flow"]["PC_width"],
                    "stallable" : CONFIG["program_flow"]["stallable"],
                },
                OUTPUT_PATH,
                MODULE_NAME + ZOL_name,
                True,
                FORCE_GENERATION
            )

            INTERFACE["ZOL_iterations_encoding"][ZOL_name] = interface["iterations_encoding"]

            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(ZOL_name, name)

            if len(interface["generics"]) != 0:
                ARCH_BODY += "generic map (\>\n"

                for generic in sorted(interface["generics"], key=lambda p : p["name"]):
                    INTERFACE["generics"] += [ { "name" : "%s_%s"%(ZOL_name, generic["name"]), "type" : generic["type"] } ]
                    ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], ZOL_name, generic["name"])

                ARCH_BODY.drop_last_X(2)
                ARCH_BODY += "\<\n)\n"

            ARCH_BODY += "port map (\>\n"


            # Handle predeclared ports
            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "stall => stall,\n"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "PC_running => PC_running_1,\n"
            ARCH_BODY += "PC_value   => PC_value,\n"
            ARCH_BODY += "overwrite  => ZOL_overwrite,\n"
            ARCH_BODY += "overwrite_value  => ZOL_value,\n"

            # Handle declared ports
            declared_ports = [
                port
                for port in interface["ports"]
                if port["name"] not in ZOL_predeclared_ports
            ]
            for port in declared_ports:
                ARCH_HEAD += "signal %s_%s : %s;\n"%(ZOL_name, port["name"], port["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port["name"], ZOL_name, port["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"

            ARCH_BODY += "\<\n\n"

            # Create input port muxes
            for input, channels in enumerate(ZOL_details["inputs"]):
                for word, srcs  in enumerate(channels["data"]):
                    assert(word == 0)
                    # Put port width from interface
                    port_name = "in_%i"%(input, )
                    port = [port for port in interface["ports"] if port["name"] == port_name]
                    assert(len(port) == 1)
                    port_width = int(port[0]["type"].split("(")[1].split("downto")[0]) + 1

                    dst_sig = "%s_%s"%(ZOL_name, port_name)
                    mux_signals("", dst_sig, port_width, srcs, CONFIG["signal_padding"])

def gen_program_memory():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ROM.generate_HDL(
        {
            "depth" : CONFIG["program_flow"]["program_length"],
            "addr_width" : CONFIG["program_flow"]["PC_width"],
            "data_width" : CONFIG["instr_decoder"]["instr_width"],
            "read_blocks" : [1],
            "reads" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        MODULE_NAME + "_PM",
        True,
        True
    )

    ARCH_BODY += "\nPM : entity work.%s(arch)\>\n"%(name)

    INTERFACE["generics"] += [
        {
            "name" : "PM_init_mif",
            "type" : "string"
        }
    ]
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

ID_predeclared_ports = [
    "clock",
    "stall"
]

ID_non_fanout_ports = [
    "instr",
    "enable",
]

def gen_instr_decoder():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ID.generate_HDL(
        {
            **CONFIG,
        },
        OUTPUT_PATH,
        MODULE_NAME + "_ID",
        GENERATE_NAME,
        FORCE_GENERATION
    )

    ARCH_BODY += "\nID : entity work.%s(arch)\>\n"%(name, )

    ARCH_BODY += "port map (\>\n"

    # Handle predeclared ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] in ID_predeclared_ports
        ],
        key=lambda d : d["name"]
    ):
        ARCH_BODY += "%s => %s,\n"%(port["name"], port["name"])

    # Handle prefixed ports
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if port["name"] not in ID_predeclared_ports
        ],
        key=lambda d : d["name"]
    ):
        ARCH_HEAD += "signal ID_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => ID_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "ID_instr <= PM_data;\n"
    ARCH_BODY += "ID_enable <= PC_running_2;\n"

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
                port["name"] not in ID_predeclared_ports
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
