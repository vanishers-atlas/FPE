
import itertools as it

from ..  import utils        as gen_utils
from ... import utils        as  tc_utils
from ... import FPE_assembly as asm_utils

from . import alu_dsp48e1
from . import comm_get
from . import comm_put
from . import reg_file
from . import BAM
from . import instruction_decoder
from . import program_counter
from . import ZOL_manager

from ..memory import RAM
from ..memory import ROM
from ..memory import delay

def generate_HDL(config, output_path, module_name, append_hash=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = gen_utils.handle_module_name(module_name, config, append_hash)
    APPEND_HASH = append_hash
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

        # Setop common ports
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

        # Generate VHDL
        pre_process_instr_set()
        gen_execute_units()
        gen_data_memories()
        gen_addr_sources()
        gen_program_fetch()
        gen_instruction_decoder()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        import json
        with open("dump.json", "w") as f:
            f.write(json.dumps(config, sort_keys=True, indent=4))

        return INTERFACE, MODULE_NAME

#####################################################################

jump_exe_status_map = {
    "ALU" : {
        "JLT" : ["lesser"],
    },
}

def pre_process_instr_set():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle compute lanes
    assert(CONFIG["SIMD"]["lanes"] >= 0)
    if CONFIG["SIMD"]["lanes"] == 1:
        CONFIG["SIMD"]["lanes_names"] = [""]
    else:
        CONFIG["SIMD"]["lanes_names"] = [
            "LANE_%i_"%(l)
             for l in range(CONFIG["SIMD"]["lanes"])
        ]

    # Exstract number of reads and writes for each memory
    for mem, config in CONFIG["data_memories"].items():
        config["reads" ] = max(
            [
                asm_utils.instr_fetch_access_coms(op).count(mem)
                for op in CONFIG["instr_set"].keys()
            ]
        )
        config["writes"] = max(
            [
                asm_utils.instr_store_access_coms(op).count(mem)
                for op in CONFIG["instr_set"].keys()
            ]
        )


    # Exstract number of reads and writes, and statuses for each exe element
    for exe, config in CONFIG["execute_units"].items():
        config["inputs" ] = max(
            [
                len(asm_utils.instr_fetchs(op))
                for op in CONFIG["instr_set"].keys()
                if exe == asm_utils.instr_exe_com(op)
            ]
        )

        config["outputs"] = max(
            [
                len(asm_utils.instr_stores(op))
                for op in CONFIG["instr_set"].keys()
                if exe == asm_utils.instr_exe_com(op)
            ]
        )

        config["operations"] = list(
            set(
                [
                    gen_utils.get_exe_operation_code(op)
                    for op in CONFIG["instr_set"].keys()
                    if exe == asm_utils.instr_exe_com(op)
                ]
            )
        )

        config["statuses"] = []
        if exe in jump_exe_status_map:
            for op in CONFIG["instr_set"].keys():
                mnemonic = asm_utils.instr_mnemonic(op)
                if mnemonic in jump_exe_status_map[exe]:
                    config["statuses"] += jump_exe_status_map[exe][mnemonic]
            config["statuses"] = list(set(config["statuses"]))


    # Exstract instruction fetch related para
    CONFIG["instruction_decoder"]["instr_width"] = CONFIG["instruction_decoder"]["opcode_width"] + sum(CONFIG["instruction_decoder"]["addr_widths"].values())
    CONFIG["program_fetch"]["uncondional_jump"] = any(
        [
            op.startswith(("JMP")) for op in CONFIG["instr_set"].keys()
        ]
    )

    # Built read addr map
    CONFIG["fetch_addr_connects"] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        for dst_com, dst_port, src_com, src_port in zip(
            asm_utils.instr_fetch_access_coms(op),
            asm_utils.instr_fetch_addr_dsts(op),
            asm_utils.instr_fetch_addr_coms(op),
            asm_utils.instr_fetch_addr_srcs(op),
        ):
            dst = "#".join([dst_com, dst_port])
            src = "#".join([src_com, src_port])
            try:
                CONFIG["fetch_addr_connects"][dst][src] = None
            except KeyError:
                CONFIG["fetch_addr_connects"][dst] = {}
                CONFIG["fetch_addr_connects"][dst][src] = None

    # Built read data addr map
    CONFIG["fetch_data_connects"] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        exe = asm_utils.instr_exe_com(op)
        if exe != "":
            for dst_com, dst_port, src_com, src_port in zip(
                it.repeat(exe),
                asm_utils.instr_fetch_access_dsts(op),
                asm_utils.instr_fetch_access_coms(op),
                asm_utils.instr_fetch_access_srcs(op),
            ):
                dst = "#".join([dst_com, dst_port])
                src = "#".join([src_com, src_port])
                try:
                    CONFIG["fetch_data_connects"][dst][src] = None
                except KeyError:
                    CONFIG["fetch_data_connects"][dst] = {}
                    CONFIG["fetch_data_connects"][dst][src] = None


    # Built write addr map
    CONFIG["store_addr_connects"] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        for dst_com, dst_port, src_com, src_port in zip(
            asm_utils.instr_store_access_coms(op),
            asm_utils.instr_store_addr_dsts(op),
            asm_utils.instr_store_addr_coms(op),
            asm_utils.instr_store_addr_srcs(op),
        ):
            dst = "#".join([dst_com, dst_port])
            src = "#".join([src_com, src_port])
            try:
                CONFIG["store_addr_connects"][dst][src] = None
            except KeyError:
                CONFIG["store_addr_connects"][dst] = {}
                CONFIG["store_addr_connects"][dst][src] = None


    # Built write data map
    CONFIG["store_data_connects"] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        exe = asm_utils.instr_exe_com(op)
        if exe != "":
            for dst_com, dst_port, src_com, src_port in zip(
                asm_utils.instr_store_access_coms(op),
                asm_utils.instr_store_access_dsts(op),
                it.repeat(exe),
                asm_utils.instr_store_access_srcs(op),
            ):
                dst = "#".join([dst_com, dst_port])
                src = "#".join([src_com, src_port])
                try:
                    CONFIG["store_data_connects"][dst][src] = None
                except KeyError:
                    CONFIG["store_data_connects"][dst] = {}
                    CONFIG["store_data_connects"][dst][src] = None


#####################################################################

exe_lib_lookup = {
    "ALU" : alu_dsp48e1,
}

def gen_execute_units():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "-- Exe components\n"

    CONFIG["exe_stages"] = 0

    # Loop over all exe components
    for exe, config in CONFIG["execute_units"].items():
        # Generate exe code
        interface, name = exe_lib_lookup[exe].generate_HDL(
            {
                **config,
            },
            OUTPUT_PATH,
            exe,
            True,
            FORCE_GENERATION
        )

        # Store exe details
        config["interface"] = interface
        CONFIG["exe_stages"] = max([CONFIG["exe_stages"], interface["cycles required"]])

        # Repeat instantation for each lane
        for lane in CONFIG["SIMD"]["lanes_names"]:

            # instantiate ALU
            ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(lane + exe, name)

            ARCH_BODY += "port map (\>\n"

            ARCH_BODY += "clock => clock,\n"

            for port in sorted(
                [
                    port
                    for port in interface["ports"]
                    if port["name"] != "clock"
                ],
                key=lambda d : d["name"]
            ):
                ARCH_HEAD += "signal %s_%s : %s;\n"%(lane + exe, port["name"], port["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port["name"], lane + exe, port["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"
            ARCH_BODY += "\<\n"

            # Create input port muxes
            for read in range(config["inputs"]):
                dst_sig = lane + "_".join([exe, "in_%i"%(read,)])
                dst_id  = "#".join([exe, "in_%i"%(read,)])

                # Handle speacel edge of only 1 source for input
                if len(CONFIG["fetch_data_connects"][dst_id]) == 1:
                    src_id = list(CONFIG["fetch_data_connects"][dst_id].keys())[0]
                    src_sig = lane + "_".join(src_id.split("#"))
                    src_mem = src_id.split("#")[0]

                    ARCH_BODY += "%s <= %s;\n"%(
                        dst_sig,
                        gen_utils.connect_signals(
                            src_sig,
                            CONFIG["data_memories"][src_mem]["data_width"],
                            config["data_width"]
                        ),
                    )
                # Handle general, muxed case
                else:
                    # Define mux select
                    select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][dst_id]) - 1)
                    select_signal = "%s_mux_sel"%(dst_sig)
                    ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                    # Geneter mux code
                    ARCH_BODY += "%s <=\>"%(dst_sig)
                    for i, src_id in enumerate(CONFIG["fetch_data_connects"][dst_id].keys()):
                        src_sig = lane + "_".join(src_id.split("#"))
                        src_mem = src_id.split("#")[0]

                        select_value = tc_utils.unsigned.encode(i, select_width)
                        CONFIG["fetch_data_connects"][dst_id][src_id] = select_value

                        ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                            gen_utils.connect_signals(
                                src_sig,
                                CONFIG["data_memories"][src_mem]["data_width"],
                                config["data_width"]
                            ),
                            select_signal,
                            select_value,
                        )
                    ARCH_BODY += "\<(others => 'U');\n"

        # Remove speacel spaces for input muxes
        # Must be done here so each lane can see sate before deletion
        for read in range(config["inputs"]):
            dst_id  = "#".join([exe, "in_%i"%(read,)])
            if len(CONFIG["fetch_data_connects"][dst_id]) == 1:
                del CONFIG["fetch_data_connects"][dst_id]


#####################################################################

mem_lib_lookup = {
    "GET" : comm_get,
    "PUT" : comm_put,
    "REG" : reg_file,
    "RAM" : RAM,
    "ROM" : ROM,
    "IMM" : ROM,
}

def gen_data_memories():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Memories components\n"
    # loop over all data memories
    for mem, config in CONFIG["data_memories"].items():
        # Generate memory code
        interface, name = mem_lib_lookup[mem].generate_HDL(
            {
                **config,
            },
            OUTPUT_PATH,
            mem,
            True,
            FORCE_GENERATION
        )

        # Store memory details
        config["interface"] = interface

        # IMM is shared across lanes so handled differently than other mems
        if mem == "IMM":
            # instantiate single IMM memory
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

            ARCH_BODY += "clock => clock,\n"

            for port in sorted(
                [
                    port
                    for port in interface["ports"]
                    if (
                        port["name"] != "clock"
                    )
                ],
                key=lambda d : d["name"]
            ):
                ARCH_HEAD += "signal %s_%s : %s;\n"%(mem, port["name"], port["type"])
                ARCH_BODY += "%s => %s_%s,\n"%(port["name"], mem, port["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n);\n"

            ARCH_BODY += "\<\n"

            # Create IMM read addr muxes
            for read in range(config["reads"]):
                dst_sig = "_".join([mem, "read_%i_addr"%(read,)])
                dst_id  = "#".join([mem, "read_%i_addr"%(read,)])

                # Handle speacel edge of only 1 source for input
                if len(CONFIG["fetch_addr_connects"][dst_id]) == 1:
                    src_id = list(CONFIG["fetch_addr_connects"][dst_id].keys())[0]
                    src_sig = "_".join(src_id.split("#"))
                    src_addr = src_id.split("#")[0]

                    if src_addr == "ID":
                        ARCH_BODY += "%s <= %s;\n"%(
                            dst_sig,
                            gen_utils.connect_signals(
                                src_sig,
                                # [:-6] to remove ending _fetch or _store
                                CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1][:-6]],
                                config["addr_width"]
                            )
                        )
                    else:
                        ARCH_BODY += "%s <= %s;\n"%(
                            dst_sig,
                            gen_utils.connect_signals(
                                src_sig,
                                CONFIG["address_sources"][src_addr]["addr_width"],
                                config["addr_width"]
                            )
                        )
                    del CONFIG["fetch_addr_connects"][dst_id]
                # Handle general, muxed case
                else:
                    # Define mux select
                    select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_addr_connects"][dst_id]) - 1)
                    select_signal = "%s_mux_sel"%(dst_sig)
                    ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                    # Geneter mux code
                    ARCH_BODY += "%s <=\>"%(dst_sig)
                    for i, src_id in enumerate(CONFIG["fetch_addr_connects"][dst_id].keys()):
                        src_sig = "_".join(src_id.split("#"))
                        src_addr = src_id.split("#")[0]

                        select_value = tc_utils.unsigned.encode(i, select_width)
                        CONFIG["fetch_addr_connects"][dst_id][src_id] = select_value

                        if src_addr == "ID":
                            signal = gen_utils.connect_signals(
                                src_sig,
                                CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1]],
                                config["addr_width"]
                            )
                        else:
                            signal = gen_utils.connect_signals(
                                src_sig,
                                CONFIG["address_sources"][src_addr]["addr_width"],
                                config["addr_width"]
                            )

                        ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                            signal,
                            select_signal,
                            select_value
                        )
                    ARCH_BODY += "\<(others => 'U');\n"

            # Map IMM test data to each of the lanes
            for read in range(config["reads"]):
                    port_name = "read_%i_data"%(read)
                    data_signal = "_".join([mem, port_name])

                    signal_type = [
                        port["type"]
                        for port in interface["ports"]
                        if port["name"] == port_name
                    ][0]

                    for lane in filter(lambda lane : lane != "", CONFIG["SIMD"]["lanes_names"]):
                        lane_signal_name = lane + data_signal
                        ARCH_HEAD += "signal %s : %s;\n"%(lane_signal_name, signal_type)
                        ARCH_BODY += "%s <= %s;\n"%(lane_signal_name, data_signal)
        else:
            # Repeat instantation for each lane
            for lane in CONFIG["SIMD"]["lanes_names"]:
                # instantiate each each memory
                ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(lane + mem, name)

                if len(interface["generics"]) != 0:
                    ARCH_BODY += "generic map (\>\n"

                    for generic in sorted(interface["generics"]):
                        INTERFACE["generics"] += [
                            {
                                "name" : lane + mem + "_" + generic["name"],
                                "type" : generic["type"]
                            }
                        ]
                        ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], lane + mem, generic["name"])

                    ARCH_BODY.drop_last_X(2)
                    ARCH_BODY += "\<\n)\n"

                ARCH_BODY += "port map (\>\n"

                ARCH_BODY += "clock => clock,\n"

                for port in sorted(
                    [
                        port
                        for port in interface["ports"]
                        if port["name"].startswith("FIFO_")
                    ],
                    key=lambda d : d["name"]
                ):
                    INTERFACE["ports"] += [
                        {
                            "name" : lane + mem + "_" + port["name"],
                            "type" : port["type"],
                            "direction" : port["direction"]
                        }
                    ]
                    ARCH_BODY += "%s => %s_%s,\n"%(port["name"], lane + mem, port["name"])

                for port in sorted(
                    [
                        port
                        for port in interface["ports"]
                        if (
                            not port["name"].startswith("FIFO_")
                            and port["name"] != "clock"
                        )
                    ],
                    key=lambda d : d["name"]
                ):
                    ARCH_HEAD += "signal %s_%s : %s;\n"%(lane + mem, port["name"], port["type"])
                    ARCH_BODY += "%s => %s_%s,\n"%(port["name"], lane + mem, port["name"])

                ARCH_BODY.drop_last_X(2)
                ARCH_BODY += "\<\n);\n"

                ARCH_BODY += "\<\n"

                # Create read addr muxes
                for read in range(config["reads"]):
                    dst_sig = "_".join([mem, "read_%i_addr"%(read,)])
                    dst_id  = "#".join([mem, "read_%i_addr"%(read,)])

                    # Handle speacel edge of only 1 source for input
                    if len(CONFIG["fetch_addr_connects"][dst_id]) == 1:
                        src_id = list(CONFIG["fetch_addr_connects"][dst_id].keys())[0]
                        src_sig = "_".join(src_id.split("#"))
                        src_addr = src_id.split("#")[0]

                        if src_addr == "ID":
                            ARCH_BODY += "%s <= %s;\n"%(
                                lane + dst_sig,
                                gen_utils.connect_signals(
                                    src_sig,
                                    # [:-6] to remove ending _fetch or _store
                                    CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1][:-6]],
                                    config["addr_width"]
                                )
                            )
                        else:
                            ARCH_BODY += "%s <= %s;\n"%(
                                lane + dst_sig,
                                gen_utils.connect_signals(
                                    src_sig,
                                    CONFIG["address_sources"][src_addr]["addr_width"],
                                    config["addr_width"]
                                )
                            )
                    # Handle general, muxed case
                    else:
                        # Define mux select
                        select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_addr_connects"][dst_id]) - 1)
                        select_signal = "%s_mux_sel"%(dst_sig)
                        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                        # Geneter mux code
                        ARCH_BODY += "%s <=\>"%(lane + dst_sig)
                        for i, src_id in enumerate(CONFIG["fetch_addr_connects"][dst_id].keys()):
                            src_sig = "_".join(src_id.split("#"))
                            src_addr = src_id.split("#")[0]

                            select_value = tc_utils.unsigned.encode(i, select_width)
                            CONFIG["fetch_addr_connects"][dst_id][src_id] = select_value

                            if src_addr == "ID":
                                signal = gen_utils.connect_signals(
                                    src_sig,
                                    CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1]],
                                    config["addr_width"]
                                )
                            else:
                                signal = gen_utils.connect_signals(
                                    src_sig,
                                    CONFIG["address_sources"][src_addr]["addr_width"],
                                    config["addr_width"]
                                )

                            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                                signal,
                                select_signal,
                                select_value
                            )
                        ARCH_BODY += "\<(others => 'U');\n"

                # Create write muxes
                for write in range(config["writes"]):
                    print(mem, "write", write)
                    # Handle write addr muxes
                    dst_sig = "_".join([mem, "write_%i_addr"%(write,)])
                    dst_id  = "#".join([mem, "write_%i_addr"%(write,)])

                    # Handle speacel edge of only 1 source for input
                    if len(CONFIG["store_addr_connects"][dst_id]) == 1:
                        src_id = list(CONFIG["store_addr_connects"][dst_id].keys())[0]
                        src_sig = "_".join(src_id.split("#"))
                        src_addr = src_id.split("#")[0]

                        if src_addr == "ID":
                            ARCH_BODY += "%s <= %s;\n"%(
                                lane + dst_sig,
                                gen_utils.connect_signals(
                                    src_sig,
                                    # [:-6] to remove ending _fetch or _store
                                    CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1][:-6]],
                                    config["addr_width"]
                                )
                            )
                        else:
                            ARCH_BODY += "%s <= %s;\n"%(
                                dst_sig,
                                gen_utils.connect_signals(
                                    src_sig,
                                    CONFIG["address_sources"][src_addr]["addr_width"],
                                    config["addr_width"]
                                )
                            )
                    # Handle general, muxed case
                    else:
                        # Define mux select
                        select_width  = tc_utils.unsigned.width(len(CONFIG["store_addr_connects"][dst_id]) - 1)
                        select_signal = lane + "%s_mux_sel"%(dst_sig)
                        ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                        # Geneter mux code
                        ARCH_BODY += "%s <=\>"%(lane + dst_sig)
                        for i, src_id in enumerate(CONFIG["store_addr_connects"][dst_id].keys()):
                            src_sig = "_".join(src_id.split("#"))
                            src_addr = src_id.split("#")[0]

                            select_value = tc_utils.unsigned.encode(i, select_width)
                            CONFIG["store_addr_connects"][dst_id][src_id] = select_value

                            if src_addr == "ID":
                                signal = gen_utils.connect_signals(
                                    src_sig,
                                    # [:-6] to remove ending _fetch or _store
                                    CONFIG["instruction_decoder"]["addr_widths"][src_id.split("#")[1][:-6]],
                                    config["addr_width"]
                                )
                            else:
                                signal = gen_utils.connect_signals(
                                    src_sig,
                                    CONFIG["address_sources"][src_addr]["addr_width"],
                                    config["addr_width"]
                                )

                            ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                                signal,
                                select_signal,
                                select_value
                            )
                        ARCH_BODY += "\<(others => 'U');\n"

                    # Handle write data muxes
                    dst_sig = "_".join([mem, "write_%i_data"%(write,)])
                    dst_id  = "#".join([mem, "write_%i_data"%(write,)])

                    # Handle speacel edge of only 1 source for input
                    if len(CONFIG["store_data_connects"][dst_id]) == 1:
                        print("Found")
                        src_id = list(CONFIG["store_data_connects"][dst_id].keys())[0]
                        src_sig = "_".join(src_id.split("#"))
                        src_exe = src_id.split("#")[0]

                        ARCH_BODY += "%s <= %s;\n"%(
                            lane + dst_sig,
                            gen_utils.connect_signals(
                                lane + src_sig,
                                CONFIG["execute_units"][src_exe]["data_width"],
                                config["data_width"]
                            )
                        )

                    # Handle general, muxed case
                    else:
                        raise NotImplementedError()


            # Remove speacel spaces for input muxes
            # Must be done here so each lane can see sate before deletion
            for read in range(config["reads"]):
                dst_id = "#".join([mem, "read_%i_addr"%(read,)])
                if  len(CONFIG["fetch_addr_connects"][dst_id]) == 1:
                    del CONFIG["fetch_addr_connects"][dst_id]
            for write in range(config["writes"]):
                # Handle write addr muxes
                dst_id = "#".join([mem, "write_%i_addr"%(write,)])
                if  len(CONFIG["store_addr_connects"][dst_id]) == 1:
                    del CONFIG["store_addr_connects"][dst_id]
                dst_id = "#".join([mem, "write_%i_data"%(write,)])
                if  len(CONFIG["store_data_connects"][dst_id]) == 1:
                    print("removed")
                    del CONFIG["store_data_connects"][dst_id]

#####################################################################

def gen_addr_sources():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Address components\n"
    for addr, config in CONFIG["address_sources"].items():
        interface, name = BAM.generate_HDL(
            {
                **config,
                "exe_stages" : CONFIG["exe_stages"],
            },
            OUTPUT_PATH,
            "BAM",
            True,
            FORCE_GENERATION
        )

        config["interface"] = interface

        ARCH_BODY += "\n%s : entity work.%s(arch)\>\n"%(addr, name)

        if len(interface["generics"]) != 0:
            ARCH_BODY += "generic map (\>\n"

            for generic in sorted(interface["generics"], key=lambda p : p["name"]):
                INTERFACE["generics"] += [
                    {
                        "name" : addr + "_" + generic["name"],
                        "type" : generic["type"]
                    }
                ]
                ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], addr, generic["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "clock => clock,\n"
        for port in sorted([port for port in interface["ports"] if port["name"] != "clock" ], key=lambda p : p["name"]):
            ARCH_HEAD += "signal %s_%s : %s;\n"%(addr, port["name"], port["type"])
            ARCH_BODY += "%s => %s_%s,\n"%(port["name"], addr, port["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"

        ARCH_BODY += "\<\n"

        # Create read addr muxes
        if any(
            [
                port["name"] == "data_in"
                for port in interface["ports"]
            ]
        ):
            dst_sig = "_".join([addr, "data_in"])
            dst_id  = "#".join([addr, "data_in"])

            # Handle speacel edge of only 1 source for input
            if len(CONFIG["fetch_data_connects"][dst_id]) == 1:
                src_id = list(CONFIG["fetch_data_connects"][dst_id].keys())[0]
                src_sig = "_".join(src_id.split("#"))
                src_mem = src_id.split("#")[0]

                ARCH_BODY += "%s <= %s;\n"%(
                    dst_sig,
                    gen_utils.connect_signals(
                        src_sig,
                        CONFIG["data_memories"][src_mem]["data_width"],
                        config["step_width"]
                    )
                )

                del CONFIG["fetch_data_connects"][dst_id]

            # Handle general, muxed case
            else:
                raise NotImplementedError()
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][dst_id]) - 1)
                select_signal = "%s_mux_sel"%(dst_sig)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(dst_sig)
                for i, src_id in enumerate(CONFIG["fetch_data_connects"][dst_id].keys()):
                    src_sig = "_".join(src_id.split("#"))
                    src_mem = src_id.split("#")[0]

                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["fetch_data_connects"][dst_id][src_id] = select_value

                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(
                        gen_utils.connect_signals(
                            src_sig,
                            CONFIG["data_memories"][src_mem]["data_width"],
                            config["data_width"]
                        ),
                        select_signal,
                        select_value,
                    )
                ARCH_BODY += "\<(others => 'U');\n"

#####################################################################

def gen_program_fetch():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Program fetch components\n"

    gen_program_counter()
    if len( CONFIG["program_fetch"]["ZOLs"]) != 0:
        gen_zero_overhead_loop()
    gen_program_memory()

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = program_counter.generate_HDL(
        {
            "length" : CONFIG["program_fetch"]["program_length"],
            "width"  : CONFIG["program_fetch"]["addr_width"],
            "statuses"  : {
                exe : config["statuses"]
                for exe, config in CONFIG["execute_units"].items()
                if "statuses" in config and len(config["statuses"]) != 0
            },
            "uncondional_jump" : CONFIG["program_fetch"]["uncondional_jump"],
            "supports_ZOL" : len( CONFIG["program_fetch"]["ZOLs"]) != 0,
        },
        OUTPUT_PATH,
        MODULE_NAME + "_PC",
        APPEND_HASH,
        FORCE_GENERATION
    )

    CONFIG["program_fetch"]["program_counter_interface"] = interface

    ARCH_BODY += "\nPC : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda p : p["name"]):
            INTERFACE["generics"] += [ { "name" : "PC_" + generic["name"], "type" : generic["type"] } ]
            ARCH_BODY += "%s => PC_%s,\n"%(generic["name"], generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "clock => clock,\n"

    INTERFACE["ports"] += [
        {
            "name" : "kickoff",
            "type" : "std_logic",
            "direction" : "in"
        },
        {
            "name" : "running",
            "type" : "std_logic",
            "direction" : "out"
        }
    ]

    ARCH_HEAD += "signal PC_running : std_logic;\n"

    ARCH_BODY += "kickoff => kickoff,\n"
    ARCH_BODY += "running => PC_running,\n"

    for port in [port for port in interface["ports"] if port["name"] not in ["clock", "kickoff", "running"] ]:
        ARCH_HEAD += "signal PC_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => PC_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n\n"

    ARCH_BODY += "PM_addr <= PC_value;\n"
    ARCH_BODY += "running <= PC_running;\n\n"

    # Handle jumping ports
    if any([port["name"] == "jump_value" for port in interface["ports"]]):
        dst_sig = "_".join(["PC", "jump_value"])
        dst_id  = "#".join(["PC", "jump_value"])

        # Handle speacel edge of only 1 source for input
        if len(CONFIG["fetch_data_connects"][dst_id]) == 1:
            src_id = list(CONFIG["fetch_data_connects"][dst_id].keys())[0]
            src_sig = "_".join(src_id.split("#"))
            src_mem = src_id.split("#")[0]

            ARCH_BODY += "%s <= %s;\n"%(
                dst_sig,
                gen_utils.connect_signals(
                    src_sig,
                    CONFIG["data_memories"][src_mem]["data_width"],
                    CONFIG["program_fetch"]["addr_width"]
                )
            )

            del CONFIG["fetch_data_connects"][dst_id]
        # Handle general, muxed case
        else:
            raise NotImplementedError()
            # Define mux select
            select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][port]) - 1)
            select_signal = "%s_mux_sel"%(port)
            ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

            # Geneter mux code
            ARCH_BODY += "%s <=\>"%(port)
            for i, src in enumerate(CONFIG["fetch_data_connects"][port].keys()):
                select_value = tc_utils.unsigned.encode(i, select_width)
                CONFIG["fetch_data_connects"][port][src] = select_value
                ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
            ARCH_BODY += "\<(others => 'U');\n"

    for port in [port for port in interface["ports"] if "_status_" in port["name"] ]:
        ARCH_BODY += "PC_%s <= %s;\n"%(port["name"], port["name"])

    # delay PC'c running signal to act as ID enable
    DELAY_INTERFACE, DELAY_NAME = delay.generate_HDL(
        {},
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_HEAD += "signal PM_running, ID_running : std_logic;\n"

    ARCH_BODY += "PM_running_delay : entity work.%s(arch)\>\n"%(DELAY_NAME)

    ARCH_BODY += "generic map (\>"
    ARCH_BODY += "delay_width => 1,"
    # delay of 1 for PC's setup cycle
    ARCH_BODY += "delay_depth => 1"
    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in (0) => PC_running,\n"
    ARCH_BODY += "data_out(0) => PM_running\n"
    ARCH_BODY += "\<);\<\n\n"

    ARCH_BODY += "ID_running_delay : entity work.%s(arch)\>\n"%(DELAY_NAME)

    ARCH_BODY += "generic map (\>"
    ARCH_BODY += "delay_width => 1,"
    # delay of 1 for PM's read access
    ARCH_BODY += "delay_depth => 1"
    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in (0) => PM_running,\n"
    ARCH_BODY += "data_out(0) => ID_running\n"
    ARCH_BODY += "\<);\<\n\n"

def gen_zero_overhead_loop():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ZOL_manager.generate_HDL(
        {
            "PC_width"  : CONFIG["program_fetch"]["addr_width"],
            "ZOLs"      : CONFIG["program_fetch"]["ZOLs"]
        },
        OUTPUT_PATH,
        MODULE_NAME + "_ZOL_manager",
        APPEND_HASH,
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

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "PC_running => PM_running,\n"
    ARCH_BODY += "value_in   => PC_value,\n"
    ARCH_BODY += "value_out  => PC_ZOL_value,\n"
    ARCH_BODY += "overwrite  => PC_ZOL_overwrite,\n"

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n\n"

    ARCH_BODY += "PM_addr <= PC_value;\n"

def gen_program_memory():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = ROM.generate_HDL(
        {
            "depth" : CONFIG["program_fetch"]["program_length"],
            "addr_width" : CONFIG["program_fetch"]["addr_width"],
            "data_width" : CONFIG["instruction_decoder"]["instr_width"],
            "reads" : 1,
        },
        OUTPUT_PATH,
        MODULE_NAME + "_PM",
        APPEND_HASH,
        FORCE_GENERATION
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

    ARCH_HEAD += "signal PM_addr : std_logic_vector(%i downto 0);\n"%( CONFIG["program_fetch"]["addr_width"] - 1)
    ARCH_HEAD += "signal PM_data : std_logic_vector(%i downto 0);\n"%( CONFIG["instruction_decoder"]["instr_width"] - 1)

    ARCH_BODY += "port map (\>\n"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "read_0_addr => PM_addr,\n"
    ARCH_BODY += "read_0_data => PM_data\n"
    ARCH_BODY += "\<);\n"

    ARCH_BODY += "\<\n"

#####################################################################

def gen_instruction_decoder():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = instruction_decoder.generate_HDL(
        {
            **CONFIG,
        },
        OUTPUT_PATH,
        MODULE_NAME + "_ID",
        APPEND_HASH,
        FORCE_GENERATION
    )

    ARCH_BODY += "\nID : entity work.%s(arch)\>\n"%(name, )

    ARCH_HEAD += "signal ID_instr : std_logic_vector(%i downto 0);\n"%( CONFIG["instruction_decoder"]["instr_width"] - 1)


    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "clock  => clock,\n"
    ARCH_BODY += "instr  => ID_instr,\n"
    ARCH_BODY += "enable => ID_running,\n"

    for port in sorted(
        [
            port
            for port in interface["ports"] if port["name"] not in ["clock", "enable", "instr"]
        ],
        key=lambda d : d["name"]
    ):
        ARCH_HEAD += "signal ID_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => ID_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "ID_instr <= PM_data;\n"
    # Connect ID signals to components
    for port in sorted(
        [
            port
            for port in interface["ports"]
            if (
                port["name"] not in ["clock", "enable", "instr"]
                and not port["name"].startswith("addr_")
            )
        ],
        key=lambda d : d["name"]
    ):
        if port["name"].startswith("BAM_"):
            ARCH_BODY += "%s <= ID_%s;\n"%(port["name"], port["name"])
        else:
            for lane in CONFIG["SIMD"]["lanes_names"]:
                ARCH_BODY += "%s <= ID_%s;\n"%(lane + port["name"], port["name"])
