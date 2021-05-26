# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain import FPE_assembly as asm_utils

from FPE.toolchain.HDL_generation.processor import alu_dsp48e1

from FPE.toolchain.HDL_generation.memory import delay
from FPE.toolchain.HDL_generation.memory import register

import itertools as it
import copy

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Handle instr_set section of config
    assert(len(config_in["instr_set"]) > 0)
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])

    # Handle program_flow section of config
    config_out["program_flow"] = {}
    assert(type(config_in["program_flow"]["uncondional_jump"]) == type(True))
    config_out["program_flow"]["uncondional_jump"] = config_in["program_flow"]["uncondional_jump"]
    assert(type(config_in["program_flow"]["ZOLs"]) == type({}))
    config_out["program_flow"]["ZOLs"] = copy.deepcopy(config_in["program_flow"]["ZOLs"])


    assert(type(config_in["program_flow"]["stallable"]) == type(True))
    config_out["program_flow"]["stallable"] = config_in["program_flow"]["stallable"]

    assert(type(config_in["program_flow"]["statuses"]) == type({}))
    config_out["program_flow"]["statuses"] = {}
    for exe, statuses in config_in["program_flow"]["statuses"].items():
        assert(type(statuses) == type([]))
        config_out["program_flow"]["statuses"][exe] = copy.copy(statuses)

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

    # Handle address_sources section of config
    assert(type(config_in["address_sources"]) == type({}))
    config_out["address_sources"] = {}
    for addr in config_in["address_sources"]:
        config_out["address_sources"][addr] = {}

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
                "parts" : "all",
            },
            {
                "library" : "ieee",
                "package" : "numeric_std",
                "parts" : "all",
            },
        ]

        # Generation Module Code
        define_decode_table_type()
        compute_instr_sections()
        generate_input_ports()
        generate_fetch_signals()
        generate_exe_signals()
        generate_store_signals()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_std_logic_signal(sig_name, value_opcode_table):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    # Declare control port
    INTERFACE["ports"] += [
        {
            "name" : sig_name,
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

    ARCH_HEAD += "signal pre_%s : std_logic;\n"%(sig_name, )

    ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(sig_name, reg, )

    ARCH_BODY += "generic map (data_width => 1)\n"

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "enable => not stall,\n"

    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "data_in(0)  => pre_%s,\n"%(sig_name, )
    ARCH_BODY += "data_out(0) => %s\n"%(sig_name, )

    ARCH_BODY += "\<);\n\<"

    # Built decode table
    opcode_value_table = {}
    for opcode in range(2**INSTR_SECTIONS["opcode"]["width"]):
        values = [
            value
            for value, opcodes in value_opcode_table.items()
            if  opcode in opcodes
        ]

        if   len(values) == 0:
            opcode_value_table[opcode] = 'U'
        elif len(values) == 1:
            opcode_value_table[opcode] = values[0]
        else:
            raise ValueError("Multiple values, %s, for signal, %s, for opcode, %i]"%(
                    str(values),
                    sig_name,
                    opcode,
                )
            )

    # Add decode table
    ARCH_HEAD += "constant %s_decode_table : decode_table := (\>\n"%(sig_name, )
    # Working decode table, in as rows of 8 values
    for i in range(2**max([INSTR_SECTIONS["opcode"]["width"] - 3, 0])):
        for j in range(2**min([INSTR_SECTIONS["opcode"]["width"], 3])):
            ARCH_HEAD += "\'%s\',\t"%(opcode_value_table[8*i + j])
        ARCH_HEAD += "\n"
    ARCH_HEAD.drop_last_X(3)
    ARCH_HEAD += "\n\<);\n\n"

    ARCH_BODY += "pre_%s <= 'U' when %s /= '1' else %s_decode_table(%s);\n\n"%(sig_name, INPUT_SIGNALS["enable"], sig_name, INPUT_SIGNALS["OPCODE"])

def generate_std_logic_vector_signal(sig_name, vec_len, value_opcode_table):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    assert(vec_len >= 0)

    # Declare control port
    INTERFACE["ports"] += [
        {
            "name" : sig_name,
            "type" : "std_logic_vector(%i downto 0)"%(vec_len - 1, ),
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

    ARCH_HEAD += "signal pre_%s : std_logic_vector(%i downto 0);\n"%(sig_name, vec_len - 1)

    ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(sig_name, reg, )

    ARCH_BODY += "generic map (data_width => %i)\n"%(vec_len, )

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "enable => not stall,\n"

    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "data_in  => pre_%s,\n"%(sig_name, )
    ARCH_BODY += "data_out => %s\n"%(sig_name, )

    ARCH_BODY += "\<);\n\<"

    # Built decode table
    opcode_value_table = {}
    for opcode in range(2**INSTR_SECTIONS["opcode"]["width"]):
        values = [
            list(value)
            for value, opcodes in value_opcode_table.items()
            if  opcode in opcodes
        ]

        if   len(values) == 0:
            opcode_value_table[opcode] = ['U']*vec_len
        elif len(values) == 1:
            opcode_value_table[opcode] = list(values[0])
            # Reverse as bit are number right to the left not left to right
            opcode_value_table[opcode].reverse()

        else:
            raise ValueError("Multiple values, %s, for signal, %s, for opcode, %i]"%(
                    str(values),
                    sig_name,
                    opcode,
                )
            )

    # Add decode table
    for bit in range(vec_len):
        ARCH_HEAD += "constant %s_bit_%i_decode_table : decode_table := (\>\n"%(sig_name, bit, )
        # Working decode table, in as rows of 8 values
        for i in range(2**max([INSTR_SECTIONS["opcode"]["width"] - 3, 0])):
            for j in range(2**min([INSTR_SECTIONS["opcode"]["width"], 3])):
                ARCH_HEAD += "\'%s\',\t"%(opcode_value_table[8*i + j][bit])
            ARCH_HEAD += "\n"
        ARCH_HEAD.drop_last_X(3)
        ARCH_HEAD += "\n\<);\n"

        ARCH_BODY += "pre_%s(%i) <= 'U' when %s /= '1' else %s_bit_%i_decode_table(%s);\n"%(
            sig_name,
            bit,
            INPUT_SIGNALS["enable"],
            sig_name,
            bit,
            INPUT_SIGNALS["OPCODE"]
        )

    ARCH_HEAD += "\n"
    ARCH_BODY += "\n"

def generate_input_signals_delay(stage):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ARCH_HEAD += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(stage, CONFIG["instr_decoder"]["instr_width"]  - 1, )

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

    ARCH_BODY += "%s_instr_delay : entity work.%s(arch)\>\n"%(stage, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => %s,\n"%(INPUT_SIGNALS["instr"], )
    ARCH_BODY += "data_out => %s_instr_delay_out\n"%(stage, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["instr"] = "%s_instr_delay_out"%(stage, )

    ARCH_HEAD += "signal %s_enable_delay_out : std_logic;\n"%(stage, )

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

    ARCH_BODY += "%s_enable_delay : entity work.%s(arch)\>\n"%(stage, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["program_flow"]["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0) => %s,\n"%(INPUT_SIGNALS["enable"], )
    ARCH_BODY += "data_out(0) => %s_enable_delay_out\n"%(stage, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["enable"] = "%s_enable_delay_out"%(stage, )

    ARCH_HEAD += "signal %s_opcode : integer;\n\n"%(stage, )
    ARCH_BODY += "%s_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        stage,
        INPUT_SIGNALS["instr"],
        INSTR_SECTIONS["opcode"]["range"],
    )
    INPUT_SIGNALS["OPCODE"] = "%s_opcode"%(stage, )

#####################################################################

def define_decode_table_type():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "type decode_table is array(0 to %i) of std_logic;\n\n"%(
        2**CONFIG["instr_decoder"]["opcode_width"] - 1,
    )

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

    ARCH_HEAD += "signal input_opcode : integer;\n\n"
    ARCH_BODY += "input_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        INPUT_SIGNALS["instr"],
        INSTR_SECTIONS["opcode"]["range"],
    )
    INPUT_SIGNALS["OPCODE"] = "input_opcode"

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

    # Handle COMM GET's adv signal
    if "GET" in CONFIG["data_memories"]:
        mem = "GET"
        config = CONFIG["data_memories"][mem]
        for read in range(len(config["reads"])):
            sig_name = "GET_read_%i_adv"%(read,)

            value_opcode_table = { "1" : [], "0" : []}
            for instr_id, instr_val in CONFIG["instr_set"].items():
                fetches = asm_utils.instr_fetches(instr_id)
                fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                fetch_mods = [asm_utils.access_mods(fetch) for fetch in fetches]
                indexes = [i for i, fetch_mem in enumerate(fetch_mems) if fetch_mem == mem]

                if len(indexes) > read and "ADV" in fetch_mods[indexes[read]]:
                    value_opcode_table["1"].append(instr_val)
                else:
                    value_opcode_table["0"].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle COMM GET's enable signal, only needed when stalling is possible
    if CONFIG["program_flow"]["stallable"]:
        if "GET" in CONFIG["data_memories"]:
            mem = "GET"
            config = CONFIG["data_memories"][mem]
            for read in range(len(config["reads"])):
                sig_name = "GET_read_%i_adv"%(read,)

                value_opcode_table = { "1" : [], "0" : []}
                for instr_id, instr_val in CONFIG["instr_set"].items():
                    fetches = asm_utils.instr_fetches(instr_id)
                    fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                    fetch_mods = [asm_utils.access_mods(fetch) for fetch in fetches]
                    indexes = [i for i, fetch_mem in enumerate(fetch_mems) if fetch_mem == mem]

                    if len(indexes) > read:
                        value_opcode_table["1"].append(instr_val)
                    else:
                        value_opcode_table["0"].append(instr_val)

                # Check the signal varies
                value_opcode_table = {
                    k : v
                    for k, v in value_opcode_table.items()
                    if len(v) > 0
                }
                if len(value_opcode_table) > 1:
                    generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle fetch addr muxes
    for mem, config in CONFIG["data_memories"].items():
        for read, read_details in enumerate(config["reads"]):
            sel_sig = "%s_read_%i_addr_sel"%(mem, read)
            sel_width = tc_utils.unsigned.width(len(read_details["addr"]) - 1)

            value_opcode_table = {}
            for mux_index, signal_details in enumerate(sorted(read_details["addr"], key=lambda x : x["signal"])):
                sel_val = tc_utils.unsigned.encode(mux_index, sel_width)
                for instr_id, instr_val in CONFIG["instr_set"].items():
                    fetches = asm_utils.instr_fetches(instr_id)
                    fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                    fetch_addr_coms = [asm_utils.addr_com(asm_utils.access_addr(fetch)) for fetch in fetches]
                    fetch_addr_ports = [asm_utils.addr_port(asm_utils.access_addr(fetch)) for fetch in fetches]

                    read_indexes = [
                        index
                        for index, fetch_mem in enumerate(fetch_mems)
                        if fetch_mem == mem
                    ]

                    if (
                        len(read_indexes) > read
                        and fetch_addr_coms[read_indexes[read]] == signal_details["com"]
                        and str(fetch_addr_ports[read_indexes[read]]) == str(signal_details["port"])
                    ):
                        try:
                            value_opcode_table[sel_val].append(instr_val)
                        except KeyError:
                            value_opcode_table[sel_val] = [instr_val, ]

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_vector_signal(sel_sig, sel_width, value_opcode_table)

    # Handle bam step generic forward signal
    for bam, config in CONFIG["address_sources"].items():
        sig_name = "%s_step_generic_forward"%(bam, )

        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            # Collect all accesses of instr
            accesses = asm_utils.instr_fetches(instr_id) + asm_utils.instr_stores(instr_id)

            # Collect addr info for accesses
            addrs = [ asm_utils.access_addr(access) for access in accesses ]
            addr_coms = [ asm_utils.addr_com(addr) for addr in addrs ]
            addr_mods = [ asm_utils.addr_mods(addr) for addr in addrs ]

            # Filter access to only one that used the bam under consideration
            indexes = [ i for i, addr_com in enumerate(addr_coms) if addr_com == bam ]

            # Check in forward mod in any of the access that us this bam
            if any(
                [
                    "FORWARD" in addr_mods[index].keys()
                    for index in indexes
                ]
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle bam step generic forward signal
    for bam, config in CONFIG["address_sources"].items():
        sig_name = "%s_step_generic_backward"%(bam, )

        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            # Collect all accesses of instr
            accesses = asm_utils.instr_fetches(instr_id) + asm_utils.instr_stores(instr_id)

            # Collect addr info for accesses
            addrs = [ asm_utils.access_addr(access) for access in accesses ]
            addr_coms = [ asm_utils.addr_com(addr) for addr in addrs ]
            addr_mods = [ asm_utils.addr_mods(addr) for addr in addrs ]

            # Filter access to only one that used the bam under consideration
            indexes = [ i for i, addr_com in enumerate(addr_coms) if addr_com == bam ]

            # Check in backward mod in any of the access that us this bam
            if any(
                [
                    "BACKWARD" in addr_mods[index].keys()
                    for index in indexes
                ]
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)


    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("fetch")

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
    ARCH_BODY += "\n"

jump_mnemonic_jump_statuses_map = {
    "JEQ" : {
        "exe" : "ALU",
        "statuses" : ["equal"],
    },
    "JNE" : {
        "exe" : "ALU",
        "statuses" : ["lesser", "greater"],
    },
    "JLT" : {
        "exe" : "ALU",
        "statuses" : ["lesser"],
    },
    "JLE" : {
        "exe" : "ALU",
        "statuses" : ["equal", "lesser"],
    },
    "JGT" : {
        "exe" : "ALU",
        "statuses" : ["greater"],
    },
    "JGE" : {
        "exe" : "ALU",
        "statuses" : ["equal", "greater"],
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

    # Handle exe enables
    for exe in CONFIG["execute_units"]:
        sig_name = "%s_enable"%(exe, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if asm_utils.instr_exe_unit(instr_id) == exe:
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle exe controls
    for exe in CONFIG["execute_units"]:
        for control, config in CONFIG["execute_units"][exe]["controls"].items():
            sig_name = "_".join([exe, control])
            value_opcode_table = {
                v : []
                for v in config["values"].values()
            }

            for instr_id, instr_val in CONFIG["instr_set"].items():
                if asm_utils.instr_exe_unit(instr_id) == exe:
                    oper = exe_lib_lookup[exe].instr_to_oper(instr_id)
                    if oper in config["values"]:
                        value_opcode_table[config["values"][oper]].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_vector_signal(sig_name, config["width"], value_opcode_table)

    # Handle exe input muxes
    for exe, config in CONFIG["execute_units"].items():
        for input, channals in enumerate(config["inputs"]):
            for word, srcs in enumerate(channals["data"]):
                sel_sig = "%s_in_%i_word_%i_sel"%(exe, input, word,)
                sel_width = tc_utils.unsigned.width(len(srcs) - 1)

                value_opcode_table = {}
                for mux_index, src in enumerate(sorted(srcs, key=lambda d : d["signal"] )):
                    sel_val = tc_utils.unsigned.encode(mux_index, sel_width)
                    for instr_id, instr_val in CONFIG["instr_set"].items():
                        exe_unit =  asm_utils.instr_exe_unit(instr_id)
                        fetches = asm_utils.instr_fetches(instr_id)
                        fetch_mems = [ asm_utils.access_mem(fetch) for fetch in fetches ]

                        if (
                            exe_unit == exe
                            and len(fetch_mems) > input
                            and fetch_mems[input] == src["com"]
                            and fetch_mems[:input].count(src["com"]) == src["port"]
                        ):
                            try:
                                value_opcode_table[sel_val].append(instr_val)
                            except KeyError:
                                value_opcode_table[sel_val] = [instr_val, ]
                # Check the signal varies
                value_opcode_table = {
                    k : v
                    for k, v in value_opcode_table.items()
                    if len(v) > 0
                }
                if len(value_opcode_table) > 1:
                    generate_std_logic_vector_signal(sel_sig, sel_width, value_opcode_table)

    # Handle uncondional jumping signal
    if CONFIG["program_flow"]["uncondional_jump"]:
        sig_name = "jump_uncondional"
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if asm_utils.instr_mnemonic(instr_id) == "JMP":
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle condional jumping signals
    for exe, statuses in CONFIG["program_flow"]["statuses"].items():
        for status in statuses:
            sig_name = "jump_%s_%s"%(exe, status)
            value_opcode_table = { "1" : [], "0" : []}
            for instr_id, instr_val in CONFIG["instr_set"].items():
                mnemonic = asm_utils.instr_mnemonic(instr_id)

                if (
                    mnemonic in jump_mnemonic_jump_statuses_map # instr in a jump
                    and jump_mnemonic_jump_statuses_map[mnemonic]["exe"] == exe # jump uses status(es) from curr exe unit
                    and status in jump_mnemonic_jump_statuses_map[mnemonic]["statuses"] # jump uses current status
                ):
                    value_opcode_table["1"].append(instr_val)
                else:
                    value_opcode_table["0"].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle bam reset signals
    for bam, config in CONFIG["address_sources"].items():
        sig_name = "%s_reset"%(bam, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if (
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_RESET"
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle bam seek forward signals
    for bam, config in CONFIG["address_sources"].items():
        sig_name = "%s_step_fetched_forward"%(bam, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if(
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_SEEK"
                and "FORWARD" in asm_utils.instr_mods(instr_id)
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle bam seek backward signald
    for bam, config in CONFIG["address_sources"].items():
        sig_name = "%s_step_fetched_backward"%(bam, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if(
                asm_utils.instr_exe_unit(instr_id) == bam
                and asm_utils.instr_mnemonic(instr_id) == "BAM_SEEK"
                and "BACKWARD" in asm_utils.instr_mods(instr_id)
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle ZOL seek signals
    for ZOL, config in CONFIG["program_flow"]["ZOLs"].items():
        sig_name = "%s_seek"%(ZOL, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if(
                asm_utils.instr_exe_unit(instr_id) == ZOL
                and asm_utils.instr_mnemonic(instr_id) == "ZOL_SEEK"
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle ZOL set signals
    for ZOL, config in CONFIG["program_flow"]["ZOLs"].items():
        sig_name = "%s_set"%(ZOL, )
        value_opcode_table = { "1" : [], "0" : []}
        for instr_id, instr_val in CONFIG["instr_set"].items():
            if(
                asm_utils.instr_exe_unit(instr_id) == ZOL
                and asm_utils.instr_mnemonic(instr_id) == "ZOL_SET"
            ):
                value_opcode_table["1"].append(instr_val)
            else:
                value_opcode_table["0"].append(instr_val)

        # Check the signal varies
        value_opcode_table = {
            k : v
            for k, v in value_opcode_table.items()
            if len(v) > 0
        }
        if len(value_opcode_table) > 1:
            generate_std_logic_signal(sig_name, value_opcode_table)

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("exe")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

exe_update_mnemonics_map = {
    "ALU" :  ["UCMP", "SCMP", ],
}

def generate_store_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    import json
    # Handle store enables
    for mem, config in CONFIG["data_memories"].items():
        for write in range(len(config["writes"])):
            sig_name = "%s_write_%i_enable"%(mem, write)

            value_opcode_table = { "1" : [], "0" : []}
            for instr_id, instr_val in CONFIG["instr_set"].items():
                stores = asm_utils.instr_stores(instr_id)
                store_mems = [asm_utils.access_mem(store) for store in stores]

                if store_mems.count(mem) >= write + 1:
                    value_opcode_table["1"].append(instr_val)
                else:
                    value_opcode_table["0"].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_signal(sig_name, value_opcode_table)

    # Handle store addr muxes
    for mem, config in CONFIG["data_memories"].items():
        for write, write_details in enumerate(config["writes"]):
            sel_sig = "%s_write_%i_addr_sel"%(mem, write)
            sel_width = tc_utils.unsigned.width(len(write_details["addr"]) - 1)

            value_opcode_table = {}
            for mux_index, signal_details in enumerate(sorted(write_details["addr"], key=lambda d : d["signal"])):
                sel_val = tc_utils.unsigned.encode(mux_index, sel_width)
                for instr_id, instr_val in CONFIG["instr_set"].items():
                    stores = asm_utils.instr_stores(instr_id)
                    store_mems = [asm_utils.access_mem(store) for store in stores]
                    store_addr_coms = [asm_utils.addr_com(asm_utils.access_addr(store)) for store in stores]
                    store_addr_ports = [asm_utils.addr_port(asm_utils.access_addr(store)) for store in stores]

                    write_indexes = [
                        index
                        for index, store_mem in enumerate(store_mems)
                        if store_mem == mem
                    ]

                    if (
                        len(write_indexes) > write
                        and store_addr_coms[write_indexes[write]] == signal_details["com"]
                        and str(store_addr_ports[write_indexes[write]]) == str(signal_details["port"])
                    ):
                        try:
                            value_opcode_table[sel_val].append(instr_val)
                        except KeyError:
                            value_opcode_table[sel_val] = [instr_val, ]

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }

            if len(value_opcode_table) > 1:
                generate_std_logic_vector_signal(sel_sig, sel_width, value_opcode_table)

    # Handle store data muxes
    for mem, config in CONFIG["data_memories"].items():
        for write, write_details in enumerate(config["writes"]):
            for word, srcs in enumerate(write_details["data"]):
                if len(srcs) > 1:
                    raise NotImplementedError()

    # Handle statuses update signals
    for exe in CONFIG["program_flow"]["statuses"].keys():
        if len(CONFIG["program_flow"]["statuses"][exe]) > 0:
            sig_name = "update_%s_statuses"%(exe, )

            value_opcode_table = { "1" : [], "0" : []}
            for instr_id, instr_val in CONFIG["instr_set"].items():
                fetches = asm_utils.instr_fetches(instr_id)
                fetch_mems = [asm_utils.access_mem(fetch) for fetch in fetches]
                fetch_mods = [asm_utils.access_mods(fetch) for fetch in fetches]
                indexes = [i for i, fetch_mem in enumerate(fetch_mems) if fetch_mem == mem]

                if (
                    asm_utils.instr_exe_unit(instr_id) == exe
                    and asm_utils.instr_mnemonic(instr_id) in exe_update_mnemonics_map[exe]
                ):
                    value_opcode_table["1"].append(instr_val)
                else:
                    value_opcode_table["0"].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                generate_std_logic_signal(sig_name, value_opcode_table)

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("store")

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
    ARCH_BODY += "\n"
