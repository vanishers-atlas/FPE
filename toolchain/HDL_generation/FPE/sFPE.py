# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain import FPE_assembly as asm_utils

from FPE.toolchain.HDL_generation.FPE import alu_dsp48e1
from FPE.toolchain.HDL_generation.FPE import comm_get
from FPE.toolchain.HDL_generation.FPE import comm_put
from FPE.toolchain.HDL_generation.FPE import reg_file
from FPE.toolchain.HDL_generation.FPE import BAM
from FPE.toolchain.HDL_generation.FPE import instr_decoder
from FPE.toolchain.HDL_generation.FPE import program_counter
from FPE.toolchain.HDL_generation.FPE import ZOL_manager

from FPE.toolchain.HDL_generation.memory import RAM
from FPE.toolchain.HDL_generation.memory import ROM
from FPE.toolchain.HDL_generation.memory import delay

import itertools as it
import copy

#####################################################################

jump_exe_status_map = {
    "ALU" : {
        "JLT" : ["lesser"]
    },
}

def preprocess_config(config_in):
    config_out = {}

    #####################################################################
    # Precheck and copy input
    #####################################################################

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    # Handle SIMD section of config
    config_out["SIMD"] = {}
    assert(config_in["SIMD"]["lanes"] >= 0)
    config_out["SIMD"]["lanes"] = config_in["SIMD"]["lanes"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle instr_set section of config
    assert(len(config_in["instr_set"]) > 0)
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle program_flow section of config
    config_out["program_flow"] = {}

    assert(config_in["program_flow"]["program_length"] >= 0)
    config_out["program_flow"]["program_length"] = config_in["program_flow"]["program_length"]

    assert(len(config_in["program_flow"]["ZOLs"]) >= 0)
    config_out["program_flow"]["ZOLs"] = copy.deepcopy(config_in["program_flow"]["ZOLs"])

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle instr_decoder section of config
    config_out["instr_decoder"] = {}

    assert(config_in["instr_decoder"]["opcode_width"] > 0)
    config_out["instr_decoder"]["opcode_width"] = config_in["instr_decoder"]["opcode_width"]

    assert(type(config_in["instr_decoder"]["addr_widths"]) == type([]))
    config_out["instr_decoder"]["addr_widths"] = []
    for width in config_in["instr_decoder"]["addr_widths"]:
        assert(width > 0)
        config_out["instr_decoder"]["addr_widths"].append(width)


    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle address_sources section of config
    config_out["address_sources"] = {}

    for bam in config_in["address_sources"]:
        config_out["address_sources"][bam] = {}

        assert(config_in["address_sources"][bam]["addr_width"] > 0)
        config_out["address_sources"][bam]["addr_width"] = config_in["address_sources"][bam]["addr_width"]

        assert(config_in["address_sources"][bam]["offset_width"] > 0)
        config_out["address_sources"][bam]["offset_width"] = config_in["address_sources"][bam]["offset_width"]

        assert(config_in["address_sources"][bam]["step_width"] > 0)
        config_out["address_sources"][bam]["step_width"] = config_in["address_sources"][bam]["step_width"]

        assert(type(config_in["address_sources"][bam]["steps"]) == type([]))
        config_out["address_sources"][bam]["steps"] = []
        for step in config_in["address_sources"][bam]["steps"]:
            assert(step in [
                    "fetched_backward",
                    "fetched_forward",
                    "generic_backward",
                    "generic_forward",
                ]
            )
            assert(step not in config_out["address_sources"][bam]["steps"])
            config_out["address_sources"][bam]["steps"].append(step)

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle data_memory section of config
    config_out["data_memories"] = {}

    assert(len(config_in["data_memories"]) > 0)
    for mem in config_in["data_memories"].keys():
        config_out["data_memories"][mem] = {}

        # Check data_width for all memories
        assert(config_in["data_memories"][mem]["data_width"] > 0)
        config_out["data_memories"][mem]["data_width"] = config_in["data_memories"][mem]["data_width"]

        # Check data_width for all memories
        assert(config_in["data_memories"][mem]["addr_width"] > 0)
        config_out["data_memories"][mem]["addr_width"] = config_in["data_memories"][mem]["addr_width"]

        # Check FIFOs of comm memories
        if mem in ["GET", "PUT"]:
            assert(config_in["data_memories"][mem]["FIFOs"] > 0)
            config_out["data_memories"][mem]["FIFOs"] = config_in["data_memories"][mem]["FIFOs"]

        # Check can_stall of comm memories
        if mem in ["GET", "PUT"]:
            assert(type(config_in["data_memories"][mem]["can_stall"]) == type(True))
            config_out["data_memories"][mem]["can_stall"] = config_in["data_memories"][mem]["can_stall"]

        # Check depth for container memories
        if mem in ["IMM", "RAM", "ROM", "REG"]:
            assert(config_in["data_memories"][mem]["depth"] > 0)
            config_out["data_memories"][mem]["depth"] = config_in["data_memories"][mem]["depth"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle execute_units section of config
    config_out["execute_units"] = {}

    assert(len(config_in["execute_units"]) > 0)
    for exe in config_in["execute_units"].keys():
        config_out["execute_units"][exe] = {}

        # Check data_width for all execute_units
        assert(config_in["execute_units"][exe]["data_width"] > 0)
        config_out["execute_units"][exe]["data_width"] = config_in["execute_units"][exe]["data_width"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    #####################################################################
    # Process copied Config
    #####################################################################

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    # Handle SIMD section of config
    if config_out["SIMD"]["lanes"] == 1:
        config_out["SIMD"]["lanes_names"] = [""]
    else:
        config_out["SIMD"]["lanes_names"] = [
            "LANE_%i_"%(l)
             for l in range(CONFIG["SIMD"]["lanes"])
        ]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle program_flow section of config
    config_out["program_flow"]["uncondional_jump"] = any([
        asm_utils.instr_mnemonic(instr) == "JMP"
        for instr in config_out["instr_set"].keys()
    ])
    config_out["program_flow"]["statuses"] = {}

    config_out["program_flow"]["stallable"] = False

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle instr_decoder section of config
    config_out["instr_decoder"]["instr_width"] = config_out["instr_decoder"]["opcode_width"] + sum(config_out["instr_decoder"]["addr_widths"])

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle address_sources section of config
    for bam in config_in["address_sources"]:
        config_out["address_sources"][bam]["data"] = []
        # Check if any steps require data to be fetched
        if any([step.startswith("fetched_") for step in config_out["address_sources"][bam]["steps"] ]):
            for instr in config_out["instr_set"].keys():
                exe_unit = asm_utils.instr_exe_unit(instr)

                fetches = asm_utils.instr_fetches(instr)
                fatch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]

                if bam == exe_unit:
                    assert(len(fetches) <= 1)
                    for fatch_mem in fatch_mems:
                        fetch_port = 0
                        data_signal = "%s_read_%i_data"%(fatch_mem, fetch_port,)

                        if not any([
                            data_signal == data["signal"]
                            for data in config_out["address_sources"][bam]["data"]
                        ]):
                            config_out["address_sources"][bam]["data"].append(
                                {
                                    "signal" : data_signal,
                                    "com" : fatch_mem,
                                    "port" : fetch_port,
                                    "width" : config_out["data_memories"][fatch_mem]["data_width"]
                                }
                            )

    #import json
    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle data_memory section of config
    for mem in config_out["data_memories"].keys():
        # Check for stall sources
        if mem in ["GET", "PUT"]:
            if config_out["data_memories"][mem]["can_stall"] == True:
                config_out["program_flow"]["stallable"] = True

        # Work out datapaths for fetchs
        # Only need to handle addrs as only inputs are muxed
        config_out["data_memories"][mem]["reads"] = []
        for instr in config_out["instr_set"].keys():
            fetches = asm_utils.instr_fetches(instr)
            fatch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]
            fatch_addrs = [ asm_utils.access_addr(fetch) for fetch in fetches ]

            # Find all indexes (fetches) that use this mem
            indexes = [i for i, fatch_mem in enumerate(fatch_mems) if mem == fatch_mem]

            # Add more reads if needed
            for _ in range(len(config_out["data_memories"][mem]["reads"]), len(indexes)):
                config_out["data_memories"][mem]["reads"].append( { "addr" : [] } )

            # Map the found indexes to reads
            for read, index in  enumerate(indexes):
                # Compute the addr source signal
                addr_com = asm_utils.addr_com(fatch_addrs[index])
                addr_port = int(asm_utils.addr_port(fatch_addrs[index]))
                addr_signal = "%s_addr_%i_fetch"%(addr_com, addr_port)

                if not any([
                    addr_signal == addr["signal"]
                    for addr in config_out["data_memories"][mem]["reads"][read]["addr"]
                ]):
                    if addr_com == "ID":
                        width = config_out["instr_decoder"]["addr_widths"][addr_port]
                    else:
                        width = config_out["address_sources"][addr_com]["addr_width"]

                    config_out["data_memories"][mem]["reads"][read]["addr"].append(
                        {
                            "signal" : addr_signal,
                            "com" : addr_com,
                            "port" : addr_port,
                            "width" : width
                        }
                    )

        # Work out datapaths for stores
        # Need to handle addrs and data as inputs are muxed
        config_out["data_memories"][mem]["writes"] = []
        for instr in config_out["instr_set"].keys():
            exe_unit = asm_utils.instr_exe_unit(instr)
            stores = asm_utils.instr_stores(instr)
            store_mems = [ asm_utils.access_mem(store) for store in stores ]
            store_addrs = [ asm_utils.access_addr(store) for store in stores ]

            # Find all indexes (stores) that use this mem
            indexes = [i for i, store_mem in enumerate(store_mems) if mem == store_mem]

            # Add more writes if needed
            for _ in range(len(config_out["data_memories"][mem]["writes"]), len(indexes)):
                config_out["data_memories"][mem]["writes"].append( { "addr" : [], "data" : [] } )

            # Map the found indexes to stores
            for write, index in  enumerate(indexes):
                # Handle addr mapping
                # Compute the addr source signal
                addr_com = asm_utils.addr_com(store_addrs[index])
                addr_port = int(asm_utils.addr_port(store_addrs[index]))
                addr_signal = "%s_addr_%i_store"%(addr_com, addr_port)

                if not any([
                    addr_signal == addr["signal"]
                    for addr in config_out["data_memories"][mem]["writes"][write]["addr"]
                ]):
                    if addr_com == "ID":
                        width = config_out["instr_decoder"]["addr_widths"][addr_port]
                    else:
                        width = config_out["address_sources"][addr_com]["addr_width"]

                    config_out["data_memories"][mem]["writes"][write]["addr"].append(
                        {
                            "signal" : addr_signal,
                            "com" : addr_com,
                            "port" : addr_port,
                            "width" : width
                        }
                    )

                # Handle data mapping
                # Compute the data source signal
                data_signal = "%s_out_%i"%(exe_unit, index)

                if not any([
                    data_signal == data["signal"]
                    for data in config_out["data_memories"][mem]["writes"][write]["data"]
                ]):
                    config_out["data_memories"][mem]["writes"][write]["data"].append(
                        {
                            "signal" : data_signal,
                            "com" : exe_unit,
                            "port" : index,
                            "width" : config_out["execute_units"][exe]["data_width"]
                        }
                    )

    #import json
    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle execute_units section of config
    for exe in config_in["execute_units"].keys():
        # Work out datapaths for inputs
        # Only need to handle addrs as only inputs are muxed
        config_out["execute_units"][exe]["inputs"] = []
        for instr in config_out["instr_set"].keys():
            exe_unit = asm_utils.instr_exe_unit(instr)

            fetches = asm_utils.instr_fetches(instr)
            fatch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]

            if exe == exe_unit:
                # Add more inputs if needed
                for _ in range(len(config_out["execute_units"][exe]["inputs"]), len(fatch_mems)):
                    config_out["execute_units"][exe]["inputs"].append( { "data" : [] } )

                # Map the fetches to inputs
                for input, fatch_mem in  enumerate(fatch_mems):
                    fetch_port = fatch_mems[input - 1:].count(fatch_mem) - 1
                    data_signal = "%s_read_%i_data"%(fatch_mem,fetch_port, )

                    if not any([
                        data_signal == data["signal"]
                        for data in config_out["execute_units"][exe]["inputs"][input]["data"]
                    ]):
                        config_out["execute_units"][exe]["inputs"][input]["data"].append(
                            {
                                "signal" : data_signal,
                                "com" : fatch_mem,
                                "port" : fetch_port,
                                "width" : config_out["data_memories"][fatch_mem]["data_width"]
                            }
                        )

        # Work out datapaths for outputs
        # Only number of outputs needed, therefore create blank dicts for furture expandion
        config_out["execute_units"][exe]["outputs"] = []
        for instr in config_out["instr_set"].keys():
            exe_unit = asm_utils.instr_exe_unit(instr)

            stores = asm_utils.instr_stores(instr)
            store_mems = [ asm_utils.access_mem(store) for store in stores ]

            if exe == exe_unit:
                # Add more outputs if needed
                for _ in range(len(config_out["execute_units"][exe]["outputs"]), len(store_mems)):
                    config_out["execute_units"][exe]["outputs"].append( { } )

        # Extract execute_unit oper_set, used to tell the ID what control signals the exe unit requires
        config_out["execute_units"][exe]["oper_set"] = {
            oper : None
            for oper in sorted(
                set(
                    [
                        exe_lib_lookup[exe].instr_to_oper(instr)
                        for instr in config_out["instr_set"].keys()
                        if exe == asm_utils.instr_exe_unit(instr)
                    ]
                )
            )
        }

        # Extract statuses execute_unit has to generate
        config_out["execute_units"][exe]["statuses"] = []
        if exe in jump_exe_status_map:
            for instr in config_out["instr_set"].keys():
                if asm_utils.instr_mnemonic(instr) in jump_exe_status_map[exe]:
                    for status in jump_exe_status_map[exe][asm_utils.instr_mnemonic(instr)]:
                        if status not in config_out["execute_units"][exe]["statuses"]:
                            config_out["execute_units"][exe]["statuses"].append(status)

        config_out["program_flow"]["statuses"][exe] = config_out["execute_units"][exe]["statuses"]

    #import json
    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

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

    # Load return variables from pre-exiting file if allowed and can
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

        import json
        with open("dump.json", "w") as f:
            f.write(json.dumps(config, sort_keys=True, indent=4))

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

exe_predeclared_ports = [
    "clock",
    "stall"
]

exe_lib_lookup = {
    "ALU" : alu_dsp48e1,
}

def gen_execute_units():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Exe components\n"

    CONFIG["exe_stages"] = 0

    # Loinstr over all exe components
    for exe, config in CONFIG["execute_units"].items():

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        # Generate exe code
        interface, name = exe_lib_lookup[exe].generate_HDL(
            {
                **config,
                "inputs" : len(config["inputs"]),
                "outputs" : len(config["outputs"]),
                "oper_set" : list(config["oper_set"].keys()),
                "stallable" : CONFIG["program_flow"]["stallable"],
            },
            OUTPUT_PATH,
            exe,
            True,
            FORCE_GENERATION
        )

        # Store exe details
        config["controls"] = copy.deepcopy(interface["controls"])

        #print(json.dumps(config, indent=2, sort_keys=True))
        #exit()

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
            for input, signals in enumerate(config["inputs"]):
                dst_sig = lane + exe + "_in_%i"%(input,)

                # Handle case of only 1 source, ie an unmuxed connection
                if len(signals["data"]) == 1:
                    src_sig = lane + signals["data"][0]["signal"]
                    ARCH_BODY += "%s <= %s;\n"%(dst_sig, gen_utils.connect_signals(src_sig, signals["data"][0]["width"], config["data_width"]) )
                # Handle case of multiple sources, ie a muxed connection
                else:
                    # Determine mux sel port width
                    # - 1 to go from number of inputs to largest sel value
                    sel_val_width = tc_utils.unsigned.width(len(signals["data"]) - 1)
                    mux_name = dst_sig + "_sel"
                    ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(mux_name, sel_val_width - 1)

                    # Imply mnx via VHDL condissional assignment of input signal
                    ARCH_BODY += "%s <=\>"%(dst_sig, )
                    for sel_val, src in enumerate( sorted( signals["data"], key=lambda x : x["signal"] ) ):
                        src_sig = lane + src["signal"]
                        ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                            gen_utils.connect_signals(src_sig, src["width"], config["data_width"]),
                            mux_name,
                            tc_utils.unsigned.encode(sel_val, sel_val_width),
                        )
                    ARCH_BODY += "(others => 'U');\<\n"


#####################################################################

mem_lib_lookup = {
    "GET" : comm_get,
    "PUT" : comm_put,
    "REG" : reg_file,
    "RAM" : RAM,
    "ROM" : ROM,
    "IMM" : ROM,
}

mem_predeclared_ports = [
    "clock",
    "stall"
]

def gen_data_memories():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Memories components\n"
    # loinstr over all data memories
    for mem, config in CONFIG["data_memories"].items():

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

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

        # Store memory details

        #print(json.dumps(config, indent=2, sort_keys=True))
        #exit()

        # Handle shared (across lanes) memories
        if mem in ["IMM"]:
            com_name = mem
            # instantiate single mem
            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(mem, name)

            if len(interface["generics"]) != 0:
                ARCH_BODY += "generic map (\>\n"

                for generic in sorted(interface["generics"]):
                    INTERFACE["generics"] += [
                        {
                            "name" : mem + "_" + generic["name"],
                            "type" : generic["type"]
                        }
                    ]
                    ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], mem, generic["name"])

                ARCH_BODY.drop_last_X(2)
                ARCH_BODY += "\<\n)\n"

            ARCH_BODY += "port map (\>\n"

            # Handle predeclared ports
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
                ARCH_HEAD += "signal %s_%s : %s;\n"%(com_name, port["name"], port["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port["name"], com_name, port["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"

            ARCH_BODY += "\<\n"

            # Create read addr port muxes
            for read, signals in enumerate(config["reads"]):
                #print(read, signals)
                dst_sig = mem + "_read_%i_addr"%(read,)
                #print(dst_sig)

                # Handle case of only 1 source, ie an unmuxed connection
                if len(signals["addr"]) == 1:
                    src_sig = signals["addr"][0]["signal"]
                    ARCH_BODY += "%s <= %s;\n"%(dst_sig, gen_utils.connect_signals(src_sig, signals["addr"][0]["width"], config["addr_width"]) )
                # Handle case of multiple sources, ie a muxed connection
                else:
                    raise NotTestedError()
                    # Determine mux sel port width
                    # - 1 to go from number of inputs to largest sel value
                    sel_val_width = tc_utils.unsigned.width(len(signals["addr"]) - 1)
                    mux_name = dst_sig + "_sel"
                    ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(mux_name, sel_val_width - 1)

                    # Imply mnx via VHDL condissional assignment of input signal
                    ARCH_BODY += "%s <=\>"%(dst_sig, )
                    for sel_val, src in enumerate( sorted( signals["addr"], key=lambda x : x["signal"] ) ):
                        src_sig = lane + src["signal"]
                        ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                            gen_utils.connect_signals(src_sig, src["width"], config["data_width"]),
                            mux_name,
                            tc_utils.unsigned.encode(sel_val, sel_val_width),
                        )
                    ARCH_BODY += "(others => 'U');\<\n"

            # Create read data signals for each lane
            for read in range(len(config["reads"])):
                src_sig = mem + "_read_%i_data"%(read,)
                signal_type = "std_logic_vector(%i downto 0)"%(config["data_width"] - 1)
                for lane in CONFIG["SIMD"]["lanes_names"]:
                    if lane != "":
                        dst_sig = lane + src_sig
                        ARCH_Head += "signal %s : %s;\n"%(dst_sig, signal_type)
                        ARCH_BODY += "%s <= %s;\n"%(dst_sig, src_sig)


            # Create write port muxes
            for write, signals in enumerate(config["writes"]):
                raise NotImplementedError()


        # Handle private (to each lane) memories
        else:
            # Repeat instantiation for each lane
            for lane in CONFIG["SIMD"]["lanes_names"]:
                inst = lane + mem

                # instantiate each memory
                ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(inst, name)

                if len(interface["generics"]) != 0:
                    ARCH_BODY += "generic map (\>\n"

                    for generic in sorted(interface["generics"]):
                        INTERFACE["generics"] += [
                            {
                                "name" : lane + mem + "_" + generic["name"],
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
                    dst_sig = inst + "_read_%i_addr"%(read,)

                    # Handle case of only 1 source, ie an unmuxed connection
                    if len(signals["addr"]) == 1:
                        src_sig = signals["addr"][0]["signal"]
                        ARCH_BODY += "%s <= %s;\n"%(dst_sig, gen_utils.connect_signals(src_sig, signals["addr"][0]["width"], config["addr_width"]) )
                    # Handle case of multiple sources, ie a muxed connection
                    else:
                        raise NotTestedError()
                        # Determine mux sel port width
                        # - 1 to go from number of inputs to largest sel value
                        sel_val_width = tc_utils.unsigned.width(len(signals["addr"]) - 1)
                        mux_name = dst_sig + "_sel"
                        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(mux_name, sel_val_width - 1)

                        # Imply mnx via VHDL condissional assignment of input signal
                        ARCH_BODY += "%s <=\>"%(dst_sig, )
                        for sel_val, src in enumerate( sorted( signals["addr"], key=lambda x : x["signal"] ) ):
                            src_sig = lane + src["signal"]
                            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                                gen_utils.connect_signals(src_sig, src["width"], config["data_width"]),
                                mux_name,
                                tc_utils.unsigned.encode(sel_val, sel_val_width),
                            )
                        ARCH_BODY += "(others => 'U');\<\n"

                # Create write port muxes
                for write, signals in enumerate(config["writes"]):
                    # Addr port
                    dst_sig = inst + "_write_%i_addr"%(write,)

                    # Handle case of only 1 source, ie an unmuxed connection
                    if len(signals["addr"]) == 1:
                        src_sig = signals["addr"][0]["signal"]
                        ARCH_BODY += "%s <= %s;\n"%(dst_sig, gen_utils.connect_signals(src_sig, signals["addr"][0]["width"], config["addr_width"]) )

                    # Handle case of multiple sources, ie a muxed connection
                    else:
                        # Determine mux sel port width
                        # - 1 to go from number of inputs to largest sel value
                        sel_val_width = tc_utils.unsigned.width(len(signals["addr"]) - 1)
                        mux_name = dst_sig + "_sel"
                        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(mux_name, sel_val_width - 1)

                        # Imply mnx via VHDL condissional assignment of input signal
                        ARCH_BODY += "%s <=\>"%(dst_sig, )
                        for sel_val, src in enumerate( sorted( signals["addr"], key=lambda x : x["signal"] ) ):
                            src_sig = lane + src["signal"]
                            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                                gen_utils.connect_signals(src_sig, src["width"], config["addr_width"]),
                                mux_name,
                                tc_utils.unsigned.encode(sel_val, sel_val_width),
                            )
                        ARCH_BODY += "(others => 'U');\<\n"

                    # Data port
                    dst_sig = inst + "_write_%i_data"%(write,)
                    #print(dst_sig)

                    # Handle case of only 1 source, ie an unmuxed connection
                    if len(signals["data"]) == 1:
                        src_sig = signals["data"][0]["signal"]
                        ARCH_BODY += "%s <= %s;\n"%(dst_sig, gen_utils.connect_signals(src_sig, signals["data"][0]["width"], config["data_width"]) )
                    # Handle case of multiple sources, ie a muxed connection
                    else:
                        raise NotTestedError()
                        # Determine mux sel port width
                        # - 1 to go from number of inputs to largest sel value
                        sel_val_width = tc_utils.unsigned.width(len(signals["data"]) - 1)
                        mux_name = dst_sig + "_sel"
                        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(mux_name, sel_val_width - 1)

                        # Imply mnx via VHDL condissional assignment of input signal
                        ARCH_BODY += "%s <=\>"%(dst_sig, )
                        for sel_val, src in enumerate( sorted( signals["data"], key=lambda x : x["signal"] ) ):
                            src_sig = lane + src["signal"]
                            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                                gen_utils.connect_signals(src_sig, src["width"], config["data_width"]),
                                mux_name,
                                tc_utils.unsigned.encode(sel_val, sel_val_width),
                            )
                        ARCH_BODY += "(others => 'U');\<\n"

    #print(json.dumps(CONFIG["execute_units"][exe], indent=2, sort_keys=True))
    #exit()

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
        if any( port["name"] == "data_in" for port in interface["ports"] ):
            dst_sig = bam + "_data_in"

            # Handle case of only 1 source, ie an unmuxed connection
            if len(CONFIG["address_sources"][bam]["data"]) == 1:
                src_sig = CONFIG["address_sources"][bam]["data"][0]["signal"]
                ARCH_BODY += "%s <= %s;\n"%(
                    dst_sig,
                    gen_utils.connect_signals(
                        src_sig,
                        CONFIG["address_sources"][bam]["data"][0]["width"],
                        config["step_width"]
                    )
                )
            # Handle case of multiple sources, ie a muxed connection
            else:
                raise NotImplementedError()

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
    "stall"
]

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = program_counter.generate_HDL(
        {
            **CONFIG["program_flow"],
            "statuses"  : {
                exe : config["statuses"]
                for exe, config in CONFIG["execute_units"].items()
                if "statuses" in config and len(config["statuses"]) != 0
            },
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

    # Handle jump valur port
    if any([port["name"] == "jump_value" for port in interface["ports"]]):
        ARCH_BODY += "PC_jump_value <= IMM_read_0_data;\n"

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

def gen_zero_overhead_loop():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ZOL_manager.generate_HDL(
        {
            "PC_width"  : CONFIG["program_flow"]["PC_width"],
            "ZOLs"      : CONFIG["program_flow"]["ZOLs"],
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        MODULE_NAME + "_ZOL_manager",
        True,
        FORCE_GENERATION
    )
    INTERFACE["ZOL_delay_encoding"] = interface["delay_encoding"]

    ARCH_BODY += "\nZOL : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda p : p["name"]):
            INTERFACE["generics"] += [ { "name" : "ZOL_" + generic["name"], "type" : generic["type"] } ]
            ARCH_BODY += "%s => ZOL_%s,\n"%(generic["name"], generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "PC_running => PC_running_1,\n"
    ARCH_BODY += "value_in   => PC_value,\n"
    ARCH_BODY += "value_out  => PC_ZOL_value,\n"
    ARCH_BODY += "overwrite  => PC_ZOL_overwrite,\n"

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n\n"

    ARCH_BODY += "PM_addr <= PC_value;\n"

def gen_program_memory():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ROM.generate_HDL(
        {
            "depth" : CONFIG["program_flow"]["program_length"],
            "addr_width" : CONFIG["program_flow"]["PC_width"],
            "data_width" : CONFIG["instr_decoder"]["instr_width"],
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
            "name" : "PM_mem_file",
            "type" : "string"
        }
    ]
    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "mem_file => PM_mem_file\n"
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

    interface, name = instr_decoder.generate_HDL(
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
