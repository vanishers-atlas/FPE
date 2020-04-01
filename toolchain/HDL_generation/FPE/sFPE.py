
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
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

        # Setop common ports
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generate VHDL
        pre_process_instr_set()
        gen_execute_units()
        gen_data_memories()
        gen_addr_sources()
        gen_instr_fetch()

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

    # Exstract number of reads and writes for each memory
    for mem, config in CONFIG["data_memories"].items():
        config["reads" ] = max([ asm_utils.decode_fetch_components(op).count(mem) for op in CONFIG["instr_set"].keys() ] )
        config["writes"] = max([ asm_utils.decode_store_components(op).count(mem) for op in CONFIG["instr_set"].keys() ] )

    # Exstract number of reads and writes, and statuses for each exe element
    for exe, config in CONFIG["execute_units"].items():
        config["inputs" ] = max([ len(asm_utils.decode_fetchs(op)) for op in CONFIG["instr_set"].keys() if exe == asm_utils.decode_exe_component(op) ] )
        config["outputs"] = max([ len(asm_utils.decode_stores(op)) for op in CONFIG["instr_set"].keys() if exe == asm_utils.decode_exe_component(op) ] )

        config["operations"] = list(set([
            gen_utils.get_exe_operation_code(op)
            for op in CONFIG["instr_set"].keys()
            if exe == asm_utils.decode_exe_component(op)
        ]))
        config["statuses"] = []
        if exe in jump_exe_status_map:
            for op in CONFIG["instr_set"].keys():
                mnemonic = asm_utils.decode_mnemonic(op)
                if mnemonic in jump_exe_status_map[exe]:
                    config["statuses"] += jump_exe_status_map[exe][mnemonic]
            config["statuses"] = list(set(config["statuses"]))

    # Exstract instruction fetch related para
    CONFIG["fetch_decode"]["instr_width"] = CONFIG["opcode_width"] + CONFIG["fetch_decode"]["encoded_addrs"] * CONFIG["addr_width"]
    CONFIG["fetch_decode"]["uncondional_jump"] = any([op.startswith(("JMP")) for op in CONFIG["instr_set"].keys()])

    # Built read addr map
    CONFIG["fetch_addr_connects"] = {}
    # Declare addr inputs for mem used in fetch
    for mem, config in CONFIG["data_memories"].items():
        for read in range(config["reads"]):
            dst = "%s_read_%i_addr"%(mem, read)
            CONFIG["fetch_addr_connects"][dst] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        dsts = []
        for mem, src in zip(asm_utils.decode_fetch_components(op), asm_utils.decode_fetch_addresses(op)):
            dst = "%s_read_%i_addr"%(mem, dsts.count(mem))
            dsts.append(mem)
            if src.startswith(("ID_addr_")):
                src += "_fetch"
            if src not in CONFIG["fetch_addr_connects"][dst]:
                CONFIG["fetch_addr_connects"][dst][src] = None

    # Built read data addr map
    CONFIG["fetch_data_connects"] = {}
    # Declare data inputs for execute unit
    for exe, para in CONFIG["execute_units"].items():
        for read in range(para["inputs"]):
            dst = "%s_in_%i"%(exe, read)
            CONFIG["fetch_data_connects"][dst] = {}
    # Declare data inputs for address sources
    for addr, para in CONFIG["address_sources"].items():
        if addr.startswith("BAM_"):
            if para["data_inc"] == True:
                dst = "%s_data_in"%(addr)
                CONFIG["fetch_data_connects"][dst] = {}
    # Declare data inputs for PC if jumping is present
    if any([op.startswith(("JMP", "JLT")) for op in CONFIG["instr_set"].keys()]):
        dst = "PC_jump_value"
        CONFIG["fetch_data_connects"][dst] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        exe = asm_utils.decode_exe_component(op)
        if exe != "":
            srcs = []
            for port, mem in enumerate(asm_utils.decode_fetch_components(op)):
                if exe.startswith(("ALU")):
                    dst = "%s_in_%i"%(exe, port)
                elif exe.startswith(("BAM_")):
                    dst = "%s_data_in"%(exe)
                elif exe.startswith(("PC")):
                    dst = "PC_jump_value"
                src = "%s_read_%i_data"%(mem, srcs.count(mem))
                srcs.append(mem)
                if src not in CONFIG["fetch_data_connects"][dst]:
                    CONFIG["fetch_data_connects"][dst][src] = None

    # Built write addr map
    CONFIG["store_addr_connects"] = {}
    # Declare addr inputs for mem used in store
    for mem, config in CONFIG["data_memories"].items():
        for write in range(config["writes"]):
            dst = "%s_write_%i_addr"%(mem, write)
            CONFIG["store_addr_connects"][dst] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        dsts = []
        for mem, src in zip(asm_utils.decode_store_components(op), asm_utils.decode_store_addresses(op)):
            dst = "%s_write_%i_addr"%(mem, dsts.count(mem))
            dsts.append(mem)
            if src.startswith(("ID_addr_")):
                src += "_store"
            if src not in CONFIG["store_addr_connects"][dst]:
                CONFIG["store_addr_connects"][dst][src] = None

    # Built write data map
    CONFIG["store_data_connects"] = {}
    # Declare data inputs for mem used in store
    for mem, config in CONFIG["data_memories"].items():
        for write in range(config["writes"]):
            dst = "%s_write_%i_data"%(mem, write)
            CONFIG["store_data_connects"][dst] = {}
    # process instr set for collections
    for op in CONFIG["instr_set"].keys():
        exe = asm_utils.decode_exe_component(op)
        if exe != "":
            dsts = []
            for port, mem in enumerate(asm_utils.decode_store_components(op)):
                src = "%s_out_%i"%(exe, port)
                dst = "%s_write_%i_data"%(mem, dsts.count(mem))
                dsts.append(mem)
                if src not in CONFIG["store_data_connects"][dst]:
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
                "data_width" : CONFIG["data_width"],
            },
            OUTPUT_PATH,
            exe,
            APPEND_HASH,
            FORCE_GENERATION
        )

        # Store exe details
        config["interface"] = interface
        CONFIG["exe_stages"] = max([CONFIG["exe_stages"], interface["cycles required"]])

        # instantiate ALU
        ARCH_BODY += "%s : entity work.%s(arch)\>\n"%(exe, name)

        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "clock => clock,\n"

        for port in sorted([port for port in interface["ports"] if port["name"] != "clock" ], key=lambda d : d["name"]):
            ARCH_HEAD += "signal %s_%s : %s;\n"%(exe, port["name"], port["type"])
            ARCH_BODY += "%s => %s_%s,\n"%(port["name"], exe, port["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"
        ARCH_BODY += "\<\n"

        # Create input port muxes
        for read in range(config["inputs"]):
            port = "%s_in_%i"%(exe, read)

            # Handle speacel edge of only 1 source for input
            if len(CONFIG["fetch_data_connects"][port]) == 1:
                ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["fetch_data_connects"][port].keys())[0])
                del CONFIG["fetch_data_connects"][port]
            # Handle general, muxed case
            else:
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][port]) - 1)
                select_signal = "%s_sel"%(port)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(port)
                for i, src in enumerate(CONFIG["fetch_data_connects"][port].keys()):
                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["fetch_data_connects"][port][src] = select_value
                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
                ARCH_BODY += "\<(others => 'U');\n"

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
                "addr_width" : CONFIG["addr_width"],
                "data_width" : CONFIG["data_width"],
            },
            OUTPUT_PATH,
            mem,
            APPEND_HASH,
            FORCE_GENERATION
        )

        # Store memory details
        config["interface"] = interface

        # instantiate each each memory
        ARCH_BODY += "%s : entity work.%s(arch)\>\n"%(mem, name)

        if len(interface["generics"]) != 0:
            ARCH_BODY += "generic map (\>\n"

            for generic in sorted(interface["generics"]):
                INTERFACE["generics"] += [ { "name" : mem + "_" + generic["name"], "type" : generic["type"] } ]
                ARCH_BODY += "%s => %s_%s,\n"%(generic["name"], mem, generic["name"])

            ARCH_BODY.drop_last_X(2)
            ARCH_BODY += "\<\n)\n"

        ARCH_BODY += "port map (\>\n"

        ARCH_BODY += "clock => clock,\n"

        for port in sorted([port for port in interface["ports"] if port["name"].startswith("FIFO_")], key=lambda d : d["name"]):
            INTERFACE["ports"] += [ { "name" : mem + "_" + port["name"], "type" : port["type"], "direction" : port["direction"] } ]
            ARCH_BODY += "%s => %s_%s,\n"%(port["name"], mem, port["name"])

        for port in sorted([port for port in interface["ports"] if not port["name"].startswith("FIFO_") and port["name"] != "clock"  ], key=lambda d : d["name"]):
            ARCH_HEAD += "signal %s_%s : %s;\n"%(mem, port["name"], port["type"])
            ARCH_BODY += "%s => %s_%s,\n"%(port["name"], mem, port["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"

        ARCH_BODY += "\<\n"

        # Create read addr muxes
        for read in range(config["reads"]):
            port = "%s_read_%i_addr"%(mem, read)

            # Handle speacel edge of only 1 source for input
            if len(CONFIG["fetch_addr_connects"][port]) == 1:
                ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["fetch_addr_connects"][port].keys())[0])
                del CONFIG["fetch_addr_connects"][port]
            # Handle general, muxed case
            else:
                print()
                print(CONFIG["fetch_addr_connects"][port])
                print()
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_addr_connects"][port]) - 1)
                select_signal = "%s_sel"%(port)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(port)
                for i, src in enumerate(CONFIG["fetch_addr_connects"][port].keys()):
                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["fetch_addr_connects"][port][src] = select_value
                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
                ARCH_BODY += "\<(others => 'U');\n"


        # Create write muxes
        for write in range(config["writes"]):
            # Handle write data muxes
            port = "%s_write_%i_data"%(mem, write)
            # Handle speacel edge of only 1 source for input
            if len(CONFIG["store_data_connects"][port]) == 1:
                ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["store_data_connects"][port].keys())[0])
                del CONFIG["store_data_connects"][port]
            # Handle general, muxed case
            else:
                print()
                print(CONFIG["store_data_connects"][port])
                print()
                raise notImplenentedError()
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["store_data_connects"][port]) - 1)
                select_signal = "%s_sel"%(port)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(port)
                for i, src in enumerate(CONFIG["store_data_connects"][port].keys()):
                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["store_data_connects"][port][src] = select_value
                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
                ARCH_BODY += "\<(others => 'U');\n"

                raise notImplenentedError()

            # Handle write addr muxes
            port = "%s_write_%i_addr"%(mem, write)
            # Handle speacel edge of only 1 source for input
            if len(CONFIG["store_addr_connects"][port]) == 1:
                ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["store_addr_connects"][port].keys())[0])
                del CONFIG["store_addr_connects"][port]
            # Handle general, muxed case
            else:
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["store_addr_connects"][port]) - 1)
                select_signal = "%s_sel"%(port)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(port)
                for i, src in enumerate(CONFIG["store_addr_connects"][port].keys()):
                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["store_addr_connects"][port][src] = select_value
                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
                ARCH_BODY += "\<(others => 'U');\n"

#####################################################################

def gen_addr_sources():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Address components\n"
    for addr, para in CONFIG["address_sources"].items():
        interface, name = BAM.generate_HDL(
            {
                **para,
                "addr_width" : CONFIG["addr_width"],
                "data_width" : CONFIG["data_width"],
            },
            OUTPUT_PATH,
            "BAM",
            True,
            FORCE_GENERATION
        )

        para["interface"] = interface

        ARCH_BODY += "%s : entity work.%s(arch)\>\n"%(addr, name)

        if len(interface["generics"]) != 0:
            ARCH_BODY += "generic map (\>\n"

            for generic in sorted(interface["generics"], key=lambda p : p["name"]):
                INTERFACE["generics"] += [ { "name" : addr + "_" + generic["name"], "type" : generic["type"] } ]
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
        if para["data_inc"] == True:
            port = "%s_data_in"%(addr)

            # Handle speacel edge of only 1 source for input
            if len(CONFIG["fetch_data_connects"][port]) == 1:
                ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["fetch_data_connects"][port].keys())[0])
                del CONFIG["fetch_data_connects"][port]
            # Handle general, muxed case
            else:
                # Define mux select
                select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][port]) - 1)
                select_signal = "%s_sel"%(port)
                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(select_signal, select_width - 1)

                # Geneter mux code
                ARCH_BODY += "%s <=\>"%(port)
                for i, src in enumerate(CONFIG["fetch_data_connects"][port].keys()):
                    select_value = tc_utils.unsigned.encode(i, select_width)
                    CONFIG["fetch_data_connects"][port][src] = select_value
                    ARCH_BODY += "%s when %s = \"%s\"\nelse "%(src, select_signal, select_value)
                ARCH_BODY += "\<(others => 'U');\n"

#####################################################################

def gen_instr_fetch():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- instruction fetch dnd decode components\n"

    gen_program_counter()
    if len( CONFIG["fetch_decode"]["ZOLs"]) != 0:
        gen_zero_overhead_loop()
    gen_program_memory()
    gen_instruction_decoder()

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = program_counter.generate_HDL(
        {
            "length" : CONFIG["fetch_decode"]["program_length"],
            "width"  : CONFIG["fetch_decode"]["PC_width"],
            "statuses"  : {exe : para["statuses"] for exe, para in CONFIG["execute_units"].items() if "statuses" in para and len(para["statuses"]) != 0},
            "uncondional_jump" : CONFIG["fetch_decode"]["uncondional_jump"],
            "supports_ZOL" : len( CONFIG["fetch_decode"]["ZOLs"]) != 0,
        },
        OUTPUT_PATH,
        "PC",
        APPEND_HASH,
        FORCE_GENERATION
    )

    CONFIG["fetch_decode"]["interface"] = interface

    ARCH_BODY += "PC : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda p : p["name"]):
            INTERFACE["generics"] += [ { "name" : "PC_" + generic["name"], "type" : generic["type"] } ]
            ARCH_BODY += "%s => PC_%s,\n"%(generic["name"], generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "clock => clock,\n"

    INTERFACE["ports"] += [ { "name" : "kickoff", "type" : "std_logic", "direction" : "in" } ]
    INTERFACE["ports"] += [ { "name" : "running", "type" : "std_logic", "direction" : "out" } ]

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
        port = "PC_jump_value"

        # Handle speacel edge of only 1 source for input
        if len(CONFIG["fetch_data_connects"][port]) == 1:
            ARCH_BODY += "%s <= %s;\n"%(port, list(CONFIG["fetch_data_connects"][port].keys())[0])
            del CONFIG["fetch_data_connects"][port]
        # Handle general, muxed case
        else:
            # Define mux select
            select_width  = tc_utils.unsigned.width(len(CONFIG["fetch_data_connects"][port]) - 1)
            select_signal = "%s_sel"%(port)
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
            "PC_width"  : CONFIG["fetch_decode"]["PC_width"],
            "ZOLs"      : CONFIG["fetch_decode"]["ZOLs"]
        },
        OUTPUT_PATH,
        "ZOL_manager",
        APPEND_HASH,
        FORCE_GENERATION
    )

    ARCH_BODY += "ZOL : entity work.%s(arch)\>\n"%(name)

    if len(interface["generics"]) != 0:
        ARCH_BODY += "generic map (\>\n"

        for generic in sorted(interface["generics"], key=lambda p : p["name"]):
            INTERFACE["generics"] += [ { "name" : "ZOL_" + generic["name"], "type" : generic["type"] } ]
            ARCH_BODY += "%s => ZOL_%s,\n"%(generic["name"], generic["name"])

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"

    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "PC_running => PC_running,\n"
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
            "depth" : CONFIG["fetch_decode"]["program_length"],
            "addr_width" : CONFIG["fetch_decode"]["PC_width"],
            "data_width" : CONFIG["fetch_decode"]["instr_width"],
            "reads" : 1,
        },
        OUTPUT_PATH,
        "PM",
        APPEND_HASH,
        FORCE_GENERATION
    )

    ARCH_BODY += "PM : entity work.%s(arch)\>\n"%(name)

    INTERFACE["generics"] += [ { "name" : "PM_mem_file", "type" : "string" } ]
    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "mem_file => PM_mem_file\n"
    ARCH_BODY += "\<)\n"

    ARCH_HEAD += "signal PM_addr : std_logic_vector(%i downto 0);\n"%( CONFIG["fetch_decode"]["PC_width"] - 1)
    ARCH_HEAD += "signal instr : std_logic_vector(%i downto 0);\n"%( CONFIG["fetch_decode"]["instr_width"] - 1)

    ARCH_BODY += "port map (\>\n"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "read_0_addr => PM_addr,\n"
    ARCH_BODY += "read_0_data => instr\n"
    ARCH_BODY += "\<);\n"

    ARCH_BODY += "\<\n"

def gen_instruction_decoder():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    interface, name = instruction_decoder.generate_HDL(
        {
            **CONFIG,
        },
        OUTPUT_PATH,
        "ID",
        APPEND_HASH,
        FORCE_GENERATION
    )

    ARCH_BODY += "ID : entity work.%s(arch)\>\n"%(name, )

    ARCH_BODY += "port map (\>\n"

    ARCH_BODY += "clock  => clock,\n"
    ARCH_BODY += "enable => ID_running,\n"

    for port in sorted([port for port in interface["ports"] if port["name"] not in ["clock", "enable"]], key=lambda d : d["name"]):
        ARCH_HEAD += "signal ID_%s : %s;\n"%(port["name"], port["type"])
        ARCH_BODY += "%s => ID_%s,\n"%(port["name"], port["name"])

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    for port in sorted([port for port in interface["ports"] if port["name"] not in ["clock", "enable"] and not port["name"].startswith("addr_") ], key=lambda d : d["name"]):
        if port["direction"] == "in":
            ARCH_BODY += "ID_%s <= %s;\n"%(port["name"], port["name"])
        elif port["direction"] == "out":
            ARCH_BODY += "%s <= ID_%s;\n"%(port["name"], port["name"])
        else:
            raise ValueError("Unknown port direction, " + str(port))
