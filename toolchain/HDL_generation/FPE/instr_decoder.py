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

from FPE.toolchain.HDL_generation.memory import delay
from FPE.toolchain.HDL_generation.memory import register

import itertools as it
import copy

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    # Handle instr_set section of config
    assert(len(config_in["instr_set"]) > 0)
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    # Handle program_flow section of config
    config_out["program_flow"] = {}
    assert(type(config_in["program_flow"]["uncondional_jump"]) == type(True))
    config_out["program_flow"]["uncondional_jump"] = config_in["program_flow"]["uncondional_jump"]

    assert(type(config_in["program_flow"]["stallable"]) == type(True))
    config_out["program_flow"]["stallable"] = config_in["program_flow"]["stallable"]

    assert(type(config_in["program_flow"]["statuses"]) == type({}))
    config_out["program_flow"]["statuses"] = {}
    for exe, statuses in config_in["program_flow"]["statuses"].items():
        assert(type(statuses) == type([]))
        config_out["program_flow"]["statuses"][exe] = copy.copy(statuses)

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()


    # Handle instruction decoder section of config
    config_out["instr_decoder"] = {}

    assert(config_in["instr_decoder"]["instr_width"] > 0)
    config_out["instr_decoder"]["instr_width"] = config_in["instr_decoder"]["instr_width"]

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
    assert(type(config_in["address_sources"]) == type({}))
    config_out["address_sources"] = {}
    for addr in config_in["address_sources"]:
        config_out["address_sources"][addr] = {}


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

        # Check depth for container memories
        if mem in ["IMM", "RAM", "REG"]:
            assert(config_in["data_memories"][mem]["depth"] > 0)
            config_out["data_memories"][mem]["depth"] = config_in["data_memories"][mem]["depth"]

        # Check reads
        assert(type(config_in["data_memories"][mem]["reads"]) == type([]))
        config_out["data_memories"][mem]["reads"] = []
        for read in config_in["data_memories"][mem]["reads"]:
            assert("addr" in read)
            assert(len(read["addr"]) > 0)
            config_out["data_memories"][mem]["reads"].append(read)

        # Check writes
        assert(type(config_in["data_memories"][mem]["writes"]) == type([]))
        config_out["data_memories"][mem]["writes"] = []
        for write in config_in["data_memories"][mem]["writes"]:
            assert("addr" in write)
            assert(len(write["addr"]) > 0)
            assert("data" in write)
            assert(len(write["data"]) > 0)
            config_out["data_memories"][mem]["writes"].append(write)

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

        # Check inputs
        assert(type(config_in["execute_units"][exe]["inputs"]) == type([]))
        config_out["execute_units"][exe]["inputs"] = []
        for input in config_in["execute_units"][exe]["inputs"]:
            assert("data" in input)
            assert(len(input["data"]) > 0)
            config_out["execute_units"][exe]["inputs"].append(input)

        # Check controls
        assert(type(config_in["execute_units"][exe]["controls"]) == type({}))
        config_out["execute_units"][exe]["controls"] = {}
        for control_name, control_details in config_in["execute_units"][exe]["controls"].items():
            assert(type(control_details) == type({}))
            config_out["execute_units"][exe]["controls"][control_name] = {}

            assert(control_details["width"] > 0)
            config_out["execute_units"][exe]["controls"][control_name]["width"] = control_details["width"]

            assert(type(control_details["values"]) == type({}))
            config_out["execute_units"][exe]["controls"][control_name]["values"] = {}
            for op, value in control_details["values"].items():
                assert(type(value) == type(""))
                config_out["execute_units"][exe]["controls"][control_name]["values"][op] = value

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

        #print(generated_name)
        #exit()

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
                "parts" : "all",
            },
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts" : "all",
            },
        ]

        # Generation Module Code
        compute_instr_sections()
        generate_input_ports()
        generate_fetch_signals()
        generate_exe_signals()
        generate_store_signals()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def compute_instr_sections():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME
    global INPUT_SIGNALS, INSTR_SECTIONS

    INSTR_SECTIONS = {}

    # Handle opcode
    INSTR_SECTIONS["opcode"] = {
        "width" : CONFIG["instr_decoder"]["opcode_width"],
        "range" : "%i downto %i"%(CONFIG["instr_decoder"]["instr_width"] - 1,  CONFIG["instr_decoder"]["instr_width"] - CONFIG["instr_decoder"]["opcode_width"])
    }

    # Section off addrs
    INSTR_SECTIONS["addrs"] = []
    addr_start = CONFIG["instr_decoder"]["instr_width"] - CONFIG["instr_decoder"]["opcode_width"]
    for width in CONFIG["instr_decoder"]["addr_widths"]:
        INSTR_SECTIONS["addrs"].append( {
            "width" : width,
            "range" : "%i downto %i"%(addr_start - 1,  addr_start - width)
        } )
        addr_start -= width

def generate_input_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    INTERFACE["ports"] += [
        {
            "name" : "clock" ,
            "type" : "std_logic",
            "direction" : "in"
        },
        {
            "name" : "enable",
            "type" : "std_logic",
            "direction" : "in"
        },
        {
            "name" : "instr",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["instr_decoder"]["instr_width"] - 1),
            "direction" : "in"
        }
    ]

    INPUT_SIGNALS = {}
    INPUT_SIGNALS["instr"] = "instr"
    INPUT_SIGNALS["enable"] = "enable"

    if CONFIG["program_flow"]["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall" ,
                "type" : "std_logic",
                "direction" : "in"
            },
        ]

def generate_fetch_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Split off opcode
    opcode = "%s(%s)"%(INPUT_SIGNALS["instr"], INSTR_SECTIONS["opcode"]["range"])

    # Handle COMM GET's adv signal
    if "GET" in CONFIG["data_memories"]:
        mem = "GET"
        config = CONFIG["data_memories"][mem]

        for read in range(len(config["reads"])):
            port_name = "GET_read_%i_adv"%(read,)

            # Declare control port
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            advancing_instr_vals = []
            for instr_id, instr_val in CONFIG["instr_set"].items():
                fetches = asm_utils.instr_fetches(instr_id)
                fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                fetch_mods = [asm_utils.access_mods(fetch) for fetch in fetches]
                indexes = [i for i, fetch_mem in enumerate(fetch_mems) if fetch_mem == mem]

                if len(indexes) > read and "ADV" in fetch_mods[indexes[read]]:
                    advancing_instr_vals.append(instr_val)

            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in advancing_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    # Handle COMM GET's enable signal, only needed when stalling is possible
    if CONFIG["program_flow"]["stallable"]:
        if "GET" in CONFIG["data_memories"]:
            mem = "GET"
            config = CONFIG["data_memories"][mem]

            for read in range(len(config["reads"])):
                port_name = "%s_read_%i_enable"%(mem, read,)

                # Declare control port
                INTERFACE["ports"] += [
                    {
                        "name" : port_name,
                        "type" : "std_logic",
                        "direction" : "out"
                    }
                ]

                # Buffer port
                interface, reg = register.generate_HDL(
                    {
                        "async_forces"  : 0,
                        "sync_forces"   : 0,
                        "has_enable"    : CONFIG["program_flow"]["stallable"]
                    },
                    OUTPUT_PATH,
                    "register",
                    True,
                    False
                )

                ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

                ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

                ARCH_BODY += "generic map (data_width => 1)\n"

                ARCH_BODY += "port map (\n\>"

                if CONFIG["program_flow"]["stallable"]:
                    ARCH_BODY += "enable => not stall,\n"

                ARCH_BODY += "trigger => clock,\n"
                ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
                ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

                ARCH_BODY += "\<);\n\<\n"

                # Buffer assementment logic
                advancing_instr_vals = []
                for instr_id, instr_val in CONFIG["instr_set"].items():
                    fetches = asm_utils.instr_fetches(instr_id)
                    fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                    fetch_mods = [asm_utils.access_mods(fetch) for fetch in fetches]
                    indexes = [i for i, fetch_mem in enumerate(fetch_mems) if fetch_mem == mem]

                    if len(indexes) > read:
                        advancing_instr_vals.append(instr_val)

                ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
                ARCH_BODY += "\nor ".join(
                    [
                        "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                        for instr_val in advancing_instr_vals
                    ]
                )
                ARCH_BODY += "\<\nelse '0';\<\n\n"

    # Handle fetch addr muxes
    for mem, config in CONFIG["data_memories"].items():
        for read in config["reads"]:
            # Handle muxed addr
            if len(read["addr"]) > 1:
                raise NotImplementedError()

    # Handle bam signals
    for bam, config in CONFIG["address_sources"].items():
        # Handle bam step forward signal
        step_forward_instr_vals = []
        for instr_id, instr_val in CONFIG["instr_set"].items():
            # Collect all accesses of instr
            accesses = asm_utils.instr_fetches(instr_id) + asm_utils.instr_stores(instr_id)

            # Collect addr info for accesses
            addrs = [ asm_utils.access_addr(access) for access in accesses ]
            addr_coms = [ asm_utils.addr_com(addr) for addr in addrs ]
            addr_mods = [ asm_utils.addr_mods(addr) for addr in addrs ]

            # Filter access to only one that used the bam under consideration
            indexes = [ i for i, addr_com in enumerate(addr_coms) if addr_com == bam ]

            # Check mods of filtered accesses
            for mods in [ addr_mods[i] for i in indexes ]:
                if "FORWARD" in mods:
                    step_forward_instr_vals.append(instr_val)
        if len(step_forward_instr_vals) != 0:
            # Declare port
            port_name = "%s_step_generic_forward"%(bam, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in step_forward_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

        # Handle bam step BACKWARD signal
        step_backward_instr_vals = []
        for instr_id, instr_val in CONFIG["instr_set"].items():
            # Collect all accesses of instr
            accesses = asm_utils.instr_fetches(instr_id) + asm_utils.instr_stores(instr_id)

            # Collect addr info for accesses
            addrs = [ asm_utils.access_addr(access) for access in accesses ]
            addr_coms = [ asm_utils.addr_com(addr) for addr in addrs ]
            addr_mods = [ asm_utils.addr_mods(addr) for addr in addrs ]

            # Filter access to only one that used the bam under consideration
            indexes = [ i for i, addr_com in enumerate(addr_coms) if addr_com == bam ]

            # Check mods of filtered accesses
            for mods in [ addr_mods[i] for i in indexes ]:
                if "BACKWARD" in mods:
                    step_backward_instr_vals.append(instr_val)
        if len(step_backward_instr_vals) != 0:
            # Declare port
            port_name = "%s_step_generic_backward"%(bam, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in step_backward_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    delay_name = "fetch"

    ARCH_HEAD += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(delay_name, CONFIG["instr_decoder"]["instr_width"]  - 1, )

    interface, name = delay.generate_HDL(
        {
            "width" : CONFIG["instr_decoder"]["instr_width"],
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_instr_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => %s,\n"%(INPUT_SIGNALS["instr"], )
    ARCH_BODY += "data_out => %s_instr_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["instr"] = "%s_instr_delay_out"%(delay_name, )

    ARCH_HEAD += "signal %s_enable_delay_out : std_logic;\n"%(delay_name, )

    interface, name = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_enable_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0) => %s,\n"%(INPUT_SIGNALS["enable"], )
    ARCH_BODY += "data_out(0) => %s_enable_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["enable"] = "%s_enable_delay_out"%(delay_name, )

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle fetch addrs
    for addr, dic in enumerate(INSTR_SECTIONS["addrs"]):
        width = dic["width"]
        section = dic["range"]

        INTERFACE["ports"] += [
            {
                "name" : "addr_%i_fetch"%(addr),
                "type" : "std_logic_vector(%i downto 0)"%(width - 1),
                "direction" : "out"
            }
        ]

        ARCH_BODY += "addr_%i_fetch <= %s(%s);\n"%(addr, INPUT_SIGNALS["instr"], section)

jump_mnemonic_jump_statuses_map = {
    "JLT" : {
        "exe" : "ALU",
        "statuses" : ["lesser",]
    }
}

exe_lib_lookup = {
    "ALU" : alu_dsp48e1,
}

def generate_exe_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Split off opcode
    opcode = "%s(%s)"%(INPUT_SIGNALS["instr"], INSTR_SECTIONS["opcode"]["range"])

    # Handle exe enables
    for exe in CONFIG["execute_units"]:
        # Declare control port
        port_name = "%s_enable"%(exe, )
        INTERFACE["ports"] += [
            {
                "name" : port_name,
                "type" : "std_logic",
                "direction" : "out"
            }
        ]

        # Buffer port
        interface, reg = register.generate_HDL(
            {
                "async_forces"  : 0,
                "sync_forces"   : 0,
                "has_enable"    : CONFIG["program_flow"]["stallable"]
            },
            OUTPUT_PATH,
            "register",
            True,
            False
        )

        ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

        ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

        ARCH_BODY += "generic map (data_width => 1)\n"

        ARCH_BODY += "port map (\n\>"

        if CONFIG["program_flow"]["stallable"]:
            ARCH_BODY += "enable => not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
        ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

        ARCH_BODY += "\<);\n\<\n"

        # Buffer assementment logic
        ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
        ARCH_BODY += "\nor ".join(
            [
                "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if asm_utils.instr_exe_unit(instr_id) == exe
            ]
        )
        ARCH_BODY += "\<\nelse '0';\<\n\n"

    # Handle exe controls
    for exe in CONFIG["execute_units"]:
        for control, config in CONFIG["execute_units"][exe]["controls"].items():
            # Declare control port
            port_name = "%s_%s"%(exe, control)
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic_vector(%i downto 0)"%(config["width"] - 1),
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s  : std_logic_vector(%i downto 0);\n"%(port_name, config["width"] - 1, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => %i)\n"%(config["width"])

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> (others => 'U') when %s /= '1'\n"%(port_name, INPUT_SIGNALS["enable"])
            for oper, value in config["values"].items():
                ARCH_BODY +=  "else \"%s\" when\> "%(value)
                ARCH_BODY += "\nor ".join(
                    [
                        "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                        for instr_id, instr_val in CONFIG["instr_set"].items()
                        if (
                            asm_utils.instr_exe_unit(instr_id) == exe
                            and exe_lib_lookup[exe].instr_to_oper(instr_id) == oper
                        )
                    ]
                )
                ARCH_BODY += "\<\n"

            ARCH_BODY += "else (others => 'U');\<\n\n"

    # Handle exe input muxes
    for exe, config in CONFIG["execute_units"].items():
        for input, signals in enumerate(config["inputs"]):
            # Handle muxed addr
            if len(signals["data"]) > 1:
                # Determine mux sel port width
                # - 1 to go from number of inputs to largest sel value
                sel_val_width = tc_utils.unsigned.width(len(signals["data"]) - 1)

                # Declare control port
                port_name = "%s_in_%i_sel"%(exe, input)
                INTERFACE["ports"] += [
                    {
                        "name" : port_name,
                        "type" : "std_logic_vector(%i downto 0)"%(sel_val_width - 1),
                        "direction" : "out"
                    }
                ]

                # Buffer port
                interface, reg = register.generate_HDL(
                    {
                        "async_forces"  : 0,
                        "sync_forces"   : 0,
                        "has_enable"    : CONFIG["program_flow"]["stallable"]
                    },
                    OUTPUT_PATH,
                    "register",
                    True,
                    False
                )

                ARCH_HEAD += "signal pre_%s  : std_logic_vector(%i downto 0);\n"%(port_name, sel_val_width - 1, )

                ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

                ARCH_BODY += "generic map (data_width => %i)\n"%(sel_val_width, )

                ARCH_BODY += "port map (\n\>"

                if CONFIG["program_flow"]["stallable"]:
                    ARCH_BODY += "enable => not stall,\n"

                ARCH_BODY += "trigger => clock,\n"
                ARCH_BODY += "data_in  => pre_%s,\n"%(port_name, )
                ARCH_BODY += "data_out => %s\n"%(port_name, )

                ARCH_BODY += "\<);\n\<\n"

                # Buffer assementment logic
                ARCH_BODY += "pre_%s <=\> (others => 'U') when %s /= '1'\n"%(port_name, INPUT_SIGNALS["enable"])
                for sel_val, src in enumerate( sorted( signals["data"], key=lambda x : x["signal"] ) ):
                    instr_values = []
                    for instr_id, instr_val in CONFIG["instr_set"].items():
                        exe_unit = asm_utils.instr_exe_unit(instr_id)

                        fetches = asm_utils.instr_fetches(instr_id)
                        fetch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]

                        if (
                            # exe is in used
                            exe_unit == exe

                            # recieving input from src["com"]
                            and len(fetch_mems) > input
                            and fetch_mems[input] == src["com"]

                            # recieving input from src["port"]
                            and fetch_mems[:input + 1].count(src["com"]) > src["port"]
                        ):
                            instr_values.append(instr_val)

                    ARCH_BODY +=  "else \"%s\" when\> "%(sel_val)
                    ARCH_BODY += "\nor ".join(
                        [
                            "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                            for instr_val in instr_values
                        ]
                    )
                    ARCH_BODY += "\<\n"
                ARCH_BODY += "else (others => 'U');\<\n\n"

    # Handle jumping signals
    if CONFIG["program_flow"]["uncondional_jump"]:
        # Declare port
        port_name = "jump_uncondional"
        INTERFACE["ports"] += [
            {
                "name" : port_name,
                "type" : "std_logic",
                "direction" : "out"
            }
        ]

        # Buffer port
        interface, reg = register.generate_HDL(
            {
                "async_forces"  : 0,
                "sync_forces"   : 0,
                "has_enable"    : CONFIG["program_flow"]["stallable"]
            },
            OUTPUT_PATH,
            "register",
            True,
            False
        )

        ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

        ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

        ARCH_BODY += "generic map (data_width => 1)\n"

        ARCH_BODY += "port map (\n\>"

        if CONFIG["program_flow"]["stallable"]:
            ARCH_BODY += "enable => not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
        ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

        ARCH_BODY += "\<);\n\<\n"

        # Buffer assementment logic
        ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
        ARCH_BODY += "\nor ".join(
            [
                "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if asm_utils.instr_mnemonic(instr_id) == "JMP"
            ]
        )
        ARCH_BODY += "\<\nelse '0';\<\n\n"
    for exe, statuses in CONFIG["program_flow"]["statuses"].items():
        for status in statuses:
            # Declare port
            port_name = "jump_%s_%s"%(exe, status)
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Find opcodes
            instr_vals = []
            for instr_id, instr_val in CONFIG["instr_set"].items():
                jump = asm_utils.instr_mnemonic(instr_id)
                if (
                    jump in jump_mnemonic_jump_statuses_map
                    and jump_mnemonic_jump_statuses_map[jump]["exe"] == exe
                    and status in jump_mnemonic_jump_statuses_map[jump]["statuses"]
                ):
                    instr_vals.append(instr_val)

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])

            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    # Handle bam signals
    for bam, config in CONFIG["address_sources"].items():
        # Handle bam reset signal
        reset_instr_vals = [
            instr_val
            for instr_id, instr_val in CONFIG["instr_set"].items()
            if(
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_RESET"
            )
        ]
        if len(reset_instr_vals) != 0:
            # Declare port
            port_name = "%s_reset"%(bam, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in reset_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

        # Handle bam seek forward signal
        seek_forward_instr_vals = [
            instr_val
            for instr_id, instr_val in CONFIG["instr_set"].items()
            if(
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_SEEK"
                and "FORWARD" in asm_utils.instr_mods(instr_id)
            )
        ]
        if len(seek_forward_instr_vals) != 0:
            # Declare port
            port_name = "%s_step_fetched_forward"%(bam, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in seek_forward_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

        # Handle bam seek forward signal
        seek_backward_instr_vals = [
            instr_val
            for instr_id, instr_val in CONFIG["instr_set"].items()
            if(
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_SEEK"
                and "BACKWARD" in asm_utils.instr_mods(instr_id)
            )
        ]
        if len(seek_backward_instr_vals) != 0:
            # Declare port
            port_name = "%s_step_fetched_backward"%(bam, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in seek_backward_instr_vals
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    delay_name = "exe"

    ARCH_HEAD += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(delay_name, CONFIG["instr_decoder"]["instr_width"]  - 1, )

    interface, name = delay.generate_HDL(
        {
            "width" : CONFIG["instr_decoder"]["instr_width"],
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_instr_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => %s,\n"%(INPUT_SIGNALS["instr"], )
    ARCH_BODY += "data_out => %s_instr_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["instr"] = "%s_instr_delay_out"%(delay_name, )

    ARCH_HEAD += "signal %s_enable_delay_out : std_logic;\n"%(delay_name, )

    interface, name = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_enable_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0) => %s,\n"%(INPUT_SIGNALS["enable"], )
    ARCH_BODY += "data_out(0) => %s_enable_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["enable"] = "%s_enable_delay_out"%(delay_name, )

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

exe_update_mnemonics_map = {
    "ALU" :  ["CMP", ],
}

def generate_store_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Split off opcode
    opcode = "%s(%s)"%(INPUT_SIGNALS["instr"], INSTR_SECTIONS["opcode"]["range"])

    # Handle store enables
    for mem, config in CONFIG["data_memories"].items():
        for write in range(len(config["writes"])):
            # Create port
            port_name = "%s_write_%i_enable"%(mem, write)
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_HEAD += "signal pre_%s  : std_logic;\n"%(port_name, )

            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            enable_instr_values = []
            for instr_id, instr_val in CONFIG["instr_set"].items():
                stores = asm_utils.instr_stores(instr_id)
                store_mems = [ asm_utils.access_mem(store) for store in stores ]

                if store_mems.count(mem) >= write + 1:
                    enable_instr_values.append(instr_val)


            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"], )
            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_val in enable_instr_values
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    # Handle store addr muxes
    for mem, config in CONFIG["data_memories"].items():
        for write, signals in enumerate(config["writes"]):
            # Handle muxed addr
            if len(signals["addr"]) > 1:
                # Determine mux sel port width
                # - 1 to go from number of inputs to largest sel value
                sel_val_width = tc_utils.unsigned.width(len(signals["addr"]) - 1)

                # Declare control port
                port_name = "%s_write_%i_addr_sel"%(mem, write)
                INTERFACE["ports"] += [
                    {
                        "name" : port_name,
                        "type" : "std_logic_vector(%i downto 0)"%(sel_val_width - 1),
                        "direction" : "out"
                    }
                ]

                # Buffer port
                interface, reg = register.generate_HDL(
                    {
                        "async_forces"  : 0,
                        "sync_forces"   : 0,
                        "has_enable"    : CONFIG["program_flow"]["stallable"]
                    },
                    OUTPUT_PATH,
                    "register",
                    True,
                    False
                )

                ARCH_HEAD += "signal pre_%s  : std_logic_vector(%i downto 0);\n"%(port_name, sel_val_width - 1, )

                ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

                ARCH_BODY += "generic map (data_width => %i)\n"%(sel_val_width, )

                ARCH_BODY += "port map (\n\>"

                if CONFIG["program_flow"]["stallable"]:
                    ARCH_BODY += "enable => not stall,\n"

                ARCH_BODY += "trigger => clock,\n"
                ARCH_BODY += "data_in  => pre_%s,\n"%(port_name, )
                ARCH_BODY += "data_out => %s\n"%(port_name, )

                ARCH_BODY += "\<);\n\<\n"

                # Buffer assementment logic
                ARCH_BODY += "pre_%s <=\> (others => 'U') when %s /= '1'\n"%(port_name, INPUT_SIGNALS["enable"])
                for sel_val, src in enumerate( sorted( signals["addr"], key=lambda x : x["signal"] ) ):
                    instr_values = []
                    for instr_id, instr_val in CONFIG["instr_set"].items():
                        stores = asm_utils.instr_stores(instr_id)
                        store_mems = [ asm_utils.access_mem(store) for store in stores ]
                        store_addrs = [ asm_utils.access_addr(store) for store in stores ]
                        store_addr_coms = [ asm_utils.addr_com(addr) for addr in store_addrs ]
                        store_addr_ports = [ asm_utils.addr_port(addr) for addr in store_addrs ]

                        write_indexes = [
                            store
                            for store, store_mem in enumerate(store_mems)
                            if mem == store_mem
                        ]

                        if (
                            # mem write is in use
                            len(write_indexes) > write

                            # recieving input from src["com"]
                            and store_addr_coms[write_indexes[write]] == src["com"]

                            # recieving input from src["com"]
                            and store_addr_ports[write_indexes[write]] == str(src["port"])
                        ):
                            instr_values.append(instr_val)

                    ARCH_BODY +=  "else \"%s\" when\> "%(sel_val)
                    ARCH_BODY += "\nor ".join(
                        [
                            "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                            for instr_val in instr_values
                        ]
                    )
                    ARCH_BODY += "\<\n"
                ARCH_BODY += "else (others => 'U');\<\n\n"

    # Handle store data muxes
    for mem, config in CONFIG["data_memories"].items():
        for write in config["writes"]:
                # Handle muxed data
                if len(write["data"]) > 1:
                    raise NotImplementedError()

    # Handle statuser update signals
    for exe in CONFIG["program_flow"]["statuses"].keys():
        if len(CONFIG["program_flow"]["statuses"][exe]) > 0:
            # Declare port
            port_name = "update_%s_statuses"%(exe, )
            INTERFACE["ports"] += [
                {
                    "name" : port_name,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]

            # Buffer port
            interface, reg = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : CONFIG["program_flow"]["stallable"]
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port_name, )


            ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(port_name, reg, )

            ARCH_BODY += "generic map (data_width => 1)\n"

            ARCH_BODY += "port map (\n\>"

            if CONFIG["program_flow"]["stallable"]:
                ARCH_BODY += "enable => not stall,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in(0)  => pre_%s,\n"%(port_name, )
            ARCH_BODY += "data_out(0) => %s\n"%(port_name, )

            ARCH_BODY += "\<);\n\<\n"

            # Buffer assementment logic
            ARCH_BODY += "pre_%s <=\> 'U' when %s /= '1'\nelse '1' when\> "%(port_name, INPUT_SIGNALS["enable"])

            ARCH_BODY += "\nor ".join(
                [
                    "%s = \"%s\""%(opcode, tc_utils.unsigned.encode(instr_val, CONFIG["instr_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                        asm_utils.instr_exe_unit(instr_id) == exe
                        and asm_utils.instr_mnemonic(instr_id) in exe_update_mnemonics_map[exe]
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    delay_name = "store"

    ARCH_HEAD += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(delay_name, CONFIG["instr_decoder"]["instr_width"]  - 1, )

    interface, name = delay.generate_HDL(
        {
            "width" : CONFIG["instr_decoder"]["instr_width"],
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_instr_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => %s,\n"%(INPUT_SIGNALS["instr"], )
    ARCH_BODY += "data_out => %s_instr_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["instr"] = "%s_instr_delay_out"%(delay_name, )

    ARCH_HEAD += "signal %s_enable_delay_out : std_logic;\n"%(delay_name, )

    interface, name = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["program_flow"]["stallable"],
        },
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_BODY += "%s_enable_delay : entity work.%s(arch)\>\n"%(delay_name, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0) => %s,\n"%(INPUT_SIGNALS["enable"], )
    ARCH_BODY += "data_out(0) => %s_enable_delay_out\n"%(delay_name, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["enable"] = "%s_enable_delay_out"%(delay_name, )

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle store addrs
    for addr, dic in enumerate(INSTR_SECTIONS["addrs"]):
        width = dic["width"]
        section = dic["range"]

        INTERFACE["ports"] += [
            {
                "name" : "addr_%i_store"%(addr),
                "type" : "std_logic_vector(%i downto 0)"%(width - 1),
                "direction" : "out"
            }
        ]

        ARCH_BODY += "addr_%i_store <= %s(%s);\n"%(addr, INPUT_SIGNALS["instr"], section)
