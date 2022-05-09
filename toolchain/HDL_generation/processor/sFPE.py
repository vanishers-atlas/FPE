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

from FPE.toolchain.HDL_generation.processor import ALU
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

def preprocess_config(config_in):
    config_out = {}

    # Handle stallable
    config_out["stallable"] = False

      # Include standard pipeline stages
    config_out["pipeline_stage"] = ["PM", "ID", "FETCH", "EXE", "STORE"]

    # Handle SIMD section of config
    config_out["SIMD"] = {}

    assert type(config_in["SIMD"]["lanes"]) == int, "SIMD.lanes must be an int"
    assert config_in["SIMD"]["lanes"] > 0, "SIMD.lanes must be greater than 0"
    config_out["SIMD"]["lanes"] = config_in["SIMD"]["lanes"]

    if config_out["SIMD"]["lanes"] == 1:
        config_out["SIMD"]["lanes_names"] = [""]
    else:
        config_out["SIMD"]["lanes_names"] = [
            "LANE_%i_"%(l)
            for l in range(CONFIG["SIMD"]["lanes"])
        ]


    # Handle instr_set section of config
    assert type(config_in["instr_set"]) == dict, "instr_set must be a dict"
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])


    # Handle program_flow section of config
    assert type(config_in["program_flow"]) == dict, "program_flow must be a dict"
    config_out["program_flow"] = copy.deepcopy(config_in["program_flow"])
    assert type(config_in["program_flow"]["ZOLs"]) == dict, "program_flow.lanes must be an dict"


    # Handle instr_decoder section of config
    assert type(config_in["instr_decoder"]) == dict, "instr_decoder must be a dict"
    config_out["instr_decoder"] = copy.deepcopy(config_in["instr_decoder"])

    assert type(config_in["instr_decoder"]["addr_widths"]) == list, "instr_decoder.addr_widths must be a list"
    assert all([type(width) == int for width in config_in["instr_decoder"]["addr_widths"]]), "instr_decoder.addr_widths must integers"
    assert all([width > 0 for width in config_in["instr_decoder"]["addr_widths"]]), "instr_decoder.addr_widths must be greater than 0"

    assert type(config_in["instr_decoder"]["opcode_width"]) == int , "instr_decoder.opcode_width must integers"
    assert config_in["instr_decoder"]["opcode_width"] > 0, "instr_decoder.opcode_width must be greater than 0"

    config_out["instr_decoder"]["instr_width"] = sum(config_in["instr_decoder"]["addr_widths"]) + config_in["instr_decoder"]["opcode_width"]


    # Handle address_sources section of config
    assert type(config_in["address_sources"]) == dict, "address_sources must be a dict"
    config_out["address_sources"] = copy.deepcopy(config_in["address_sources"])


    # Handle data_memory section of config
    assert type(config_in["data_memories"]) == dict, "data_memories must be a dict"
    config_out["data_memories"] = copy.deepcopy(config_in["data_memories"])

    if "GET" in config_in["data_memories"].keys():
        assert type(config_out["data_memories"]["GET"]["FIFO_handshakes"]) == bool, "data_memories.GET.FIFO_handshakes must be bool"
        if config_out["data_memories"]["GET"]["FIFO_handshakes"] == True:
            config_out["stallable"] = True

    if "PUT" in config_in["data_memories"].keys():
        assert type(config_out["data_memories"]["PUT"]["FIFO_handshakes"]) == bool, "data_memories.PUT.FIFO_handshakes must be bool"
        if config_out["data_memories"]["PUT"]["FIFO_handshakes"] == True:
            config_out["stallable"] = True


    # Handle execute_units section of config
    assert type(config_in["execute_units"]) == dict, "execute_units must be a dict"
    config_out["execute_units"] = copy.deepcopy(config_in["execute_units"])


    # Set the signal padding option
    assert type(config_in["signal_padding"]) == str, "signal_padding must be a str"
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
        INTERFACE = { "ports" : { }, "generics" : { }, }

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
    if CONFIG["stallable"]:
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
                    "stallable" : CONFIG["stallable"],
                }
            )
            interface, name = exe_lib_lookup[exe].generate_HDL(
                config,
                OUTPUT_PATH,
                module_name=module_name,
                concat_naming=CONCAT_NAMING,
                force_generation=FORCE_GENERATION
            )

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
                    "stallable" : CONFIG["stallable"],
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
        for read, access in enumerate(asm_utils.instr_fetches(instr)):
            if asm_utils.addr_com(asm_utils.access_addr(access)) == "ID":
                for lane in CONFIG["SIMD"]["lanes_names"]:
                    gen_utils.add_datapath_source(DATAPATHS, "%sfetch_addr_%i"%(lane, read), "fetch", instr, "ID_addr_%i_fetch"%(ID_addr, ), "unsigned",  CONFIG["instr_decoder"]["addr_widths"][ID_addr])
                ID_addr += 1

        for write, access in enumerate(asm_utils.instr_stores(instr)):
            if asm_utils.addr_com(asm_utils.access_addr(access)) == "ID":
                for lane in CONFIG["SIMD"]["lanes_names"]:
                    gen_utils.add_datapath_source(DATAPATHS, "%sstore_addr_%i"%(lane, write), "store", instr, "ID_addr_%i_store"%(ID_addr, ), "unsigned",  CONFIG["instr_decoder"]["addr_widths"][ID_addr])
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
                    "stallable" : CONFIG["stallable"],
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
    "stall" : "stall",
    "ALU_jump" : "ALU_core_jump_taken",
}

def gen_program_counter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    if CONCAT_NAMING:
        module_name = MODULE_NAME + "_PC"
    else:
        module_name = None

    config = PC.add_inst_config(
        "PC",
        CONFIG["instr_set"],
        {
            **CONFIG["program_flow"],
            "stallable" : CONFIG["stallable"],
        }
    )
    interface, name = PC.generate_HDL(
        config,
        OUTPUT_PATH,
        module_name=module_name,
        concat_naming=CONCAT_NAMING,
        force_generation=FORCE_GENERATION
    )
    # controls
    DATAPATHS = gen_utils.merge_datapaths(DATAPATHS, PC.get_inst_pathways("PC", "", CONFIG["instr_set"], interface, config, CONFIG["SIMD"]["lanes_names"][0]) )
    CONTROLS  = gen_utils.merge_controls( CONTROLS , PC.get_inst_controls("PC", "", CONFIG["instr_set"], interface, config) )

    CONFIG["program_flow"]["PC_width"] = interface["ports"]["value"]["width"]

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
    for port, details  in interface["ports"].items():
        if port not in PC_predeclared_ports.keys():
            try:
                ARCH_HEAD += "signal PC_%s : %s(%i downto 0);\n"%(port, details["type"], details["width"] - 1, )
            except KeyError:
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
    "PC_running" : "PC_running",
}

ZOL_declared_ports = [
    "overwrite_PC_enable", "overwrite_PC_value",
    "seek_check_value", "seek_overwrite_value", "seek_enable",
    "set_overwrites", "set_enable",
]

def gen_zero_overhead_loops():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ZOL_overwrites_encoding"] = {}

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
                "stallable" : CONFIG["stallable"],
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

    # Build mux tree for ZOL overwrite and values
    if len(CONFIG["program_flow"]["ZOLs"].keys()) > 1:
        _, mux_2 = mux.generate_HDL(
            {
                "inputs" : 2
            },
            OUTPUT_PATH,
            module_name=None,
            concat_naming=False,
            force_generation=FORCE_GENERATION
        )


        lavel = 0
        value_width = CONFIG["program_flow"]["PC_width"]
        mux_ends = [(zol + "_overwrite_PC_enable", zol + "_overwrite_PC_value", ) for zol in CONFIG["program_flow"]["ZOLs"].keys() ]
        while len(mux_ends) > 1:
            mux_ends_new = []
            for pair, ((a_enable, a_value), (b_enable, b_value)) in enumerate(zip(mux_ends[0::2], mux_ends[1::2])):
                ARCH_HEAD += "signal ZOL_overwrite_%i_%i : std_logic;\n"%(lavel, pair, )
                ARCH_BODY += "ZOL_overwrite_%i_%i <=  %s or %s;\n"%(lavel, pair, a_enable, b_enable, )

                ARCH_BODY += "ZOL_value_mux_%i_%i : entity work.%s(arch)\>\n"%(lavel, pair, mux_2, )
                ARCH_BODY += "generic map (data_width => %i)\n"%(value_width, )
                ARCH_BODY += "port map (\n\>"
                ARCH_BODY += "sel(0) => %s,\n"%(b_enable, )
                ARCH_BODY += "data_in_0 => %s,\n"%(a_value, )
                ARCH_BODY += "data_in_1 => %s,\n"%(b_value, )

                ARCH_HEAD += "signal ZOL_value_mux_%i_%i_out : std_logic_vector(%i downto 0);\n"%(lavel, pair, value_width - 1, )
                ARCH_BODY += "data_out => ZOL_value_mux_%i_%i_out\n"%(lavel, pair, )

                ARCH_BODY += "\<);\n\<\n"

                mux_ends_new.append(("ZOL_overwrite_%i_%i"%(lavel, pair, ), "ZOL_value_mux_%i_%i_out"%(lavel, pair, ), ) )

            if len(mux_ends) % 2 == 1:
                mux_ends_new.append(mux_ends[-1])

            mux_ends = mux_ends_new
            lavel += 1

        # Connect end of mux and or tree to PC
        ARCH_BODY += "PC_zero_overhead_overwrite <= %s;\n"%(mux_ends[0][0], )
        ARCH_BODY += "PC_zero_overhead_value <= %s;\n\n"%(mux_ends[0][1], )

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
            "buffer_reads" : True,
            "type" : "DIST",
            "reads" : 1,
            "stallable" : CONFIG["stallable"],
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
    if CONFIG["stallable"]:
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
    for port, signal in ID_predeclared_ports.items():
        if port in interface["ports"]:
            ARCH_BODY += "%s => %s,\n"%(port, signal, )

    # Handle prefixed ports
    for port in sorted(interface["ports"].keys()):
        if port not in ID_predeclared_ports.keys():
            details = interface["ports"][port]
            try:
                ARCH_HEAD += "signal ID_%s : %s(%i downto 0);\n"%(port, details["type"], details["width"] - 1, )
            except Exception as e:
                ARCH_HEAD += "signal ID_%s : %s;\n"%(port, details["type"], )
            ARCH_BODY += "%s => ID_%s,\n"%(port, port, )

    ARCH_BODY.drop_last_X(2)
    ARCH_BODY += "\<\n);\n"

    ARCH_BODY += "\<\n"

    ARCH_BODY += "ID_instr <= PM_data;\n"
    ARCH_BODY += "ID_enable <= running_ID;\n"

    # Handle PC control signals
    for port in sorted(interface["ports"]):
        if port.startswith("jump_") or (port.startswith("update_") and port.endswith("_statuses")):
            ARCH_BODY += "PC_%s <= ID_%s;\n"%(port, port, )

    # Handle fanning out control signals
    for port in sorted(interface["ports"]):
        if (
            port not in ID_predeclared_ports.keys()
            and port not in ID_non_fanout_ports
            and not port.startswith("addr_")
            and not port.startswith("jump_")
            and not (port.startswith("update_") and port.endswith("_statuses"))
        ):
            for lane in CONFIG["SIMD"]["lanes_names"]:
                ARCH_BODY += "%s%s <= ID_%s;\n"%(lane, port, port, )

#####################################################################

def gen_running_delays():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, DATAPATHS, CONTROLS, ARCH_HEAD, ARCH_BODY

    # Handle running output
    INTERFACE["ports"]["running"] = {
        "type" : "std_logic",
        "direction" : "out"
    }
    ARCH_BODY += "running <= PC_running;\n\n"

    # Declare each stage's running signal
    for stage in CONFIG["pipeline_stage"]:
        ARCH_HEAD += "signal running_%s : std_logic;\n"%(stage, )

    ARCH_BODY += "running_%s <= PC_running;\n"%(CONFIG["pipeline_stage"][0], )

    DELAY_INTERFACE, DELAY_NAME = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["stallable"],
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
        if CONFIG["stallable"]:
            ARCH_BODY += "stall => stall,\n"
        ARCH_BODY += "data_in (0) => running_%s,\n"%(stage_in, )
        ARCH_BODY += "data_out(0) => running_%s\n"%(stage_out, )
        ARCH_BODY += "\<);\<\n\n"
