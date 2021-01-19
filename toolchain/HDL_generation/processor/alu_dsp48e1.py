# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register

import warnings

#####################################################################

from FPE.toolchain import FPE_assembly as asm_utils

internal_loctations = [ "acc" ]

def instr_to_oper(instr):
    return "#".join(
        [
            asm_utils.instr_mnemonic(instr),
            "~".join(
                [
                    src.lower() if src.lower() in internal_loctations
                    else "fetch"
                    for src in asm_utils.instr_srcs(instr)
                ]
            ),
            "~".join(
                [
                    dst.lower() if dst.lower() in internal_loctations
                    else "store"
                    for dst in asm_utils.instr_dests(instr)
                ]
            ),
        ]
    )

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    assert(config_in["data_width"] > 0)
    config_out["data_width"] = config_in["data_width"]

    assert(config_in["inputs"] > 0)
    config_out["inputs"] = config_in["inputs"]

    assert(config_in["outputs"] > 0)
    config_out["outputs"] = config_in["outputs"]

    assert(type(config_in["oper_set"]) == type([]))
    assert(len(config_in["oper_set"]) > 0)
    config_out["oper_set"] = config_in["oper_set"]

    # Check inputs/outputs required by op_set
    for oper in config_out["oper_set"]:
        num_fetchs = gen_utils.oper_num_fetchs(oper)
        if num_fetchs > config_out["inputs"]:
            raise ValueError("Operation, %s, requires inputs >= %i"%(oper, num_fetchs))

        num_stores = gen_utils.oper_num_stores(oper)
        if num_stores > config_out["outputs"]:
            raise ValueError("Operation, %s, requires outputs >= %i"%(oper, num_stores))

    config_out["statuses"] = set()
    config_out["delayed_statuses"] = set()
    config_out["internal_statuses"] = set()
    for status in config_in["statuses"]:
        if   status == "equal":
            config_out["statuses"].add("equal")

            config_out["internal_statuses"].add("equal")
        elif status == "lesser":
            config_out["statuses"].add("lesser")

            config_out["internal_statuses"].add("lesser")
        elif status == "greater":
            config_out["statuses"].add("greater")

            config_out["internal_statuses"].add("greater")
            config_out["internal_statuses"].add("lesser")
            config_out["internal_statuses"].add("equal")
        else:
            raise ValueError("Unknown Status, %s, eqsuired from ALU"%(status, ))

    if ( any([gen_utils.oper_mnemonic(oper) == "SCMP" for oper in config_out["oper_set"]])
        and "lesser" in config_out["internal_statuses"]
    ):
        config_out["delayed_statuses"].add("operand_0_sign")
        config_out["delayed_statuses"].add("operand_1_sign")

    # Set the signal padding option
    config_out["signal_padding"] = config_in["signal_padding"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

import zlib

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        generated_name = "ALU_48E1"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        # Hash oper_set
        generated_name += "_%sop"%str( hex( zlib.adler32("\n".join(config["oper_set"]).encode('utf-8')) )).lstrip("0x").zfill(8)

        # Append data width
        generated_name += "_%sw"%config["data_width"]

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
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

        # Generation Module Code
        populate_interface()
        handle_DSP()
        handle_shifter()
        generate_ports()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def populate_interface():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["controls"] = {}

    # Flag number of clock cycles needed
    INTERFACE["cycles required"] = 1

def generate_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate common control
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        },
        {
            "name" : "enable",
            "type" : "std_logic",
            "direction" : "in"
        },
    ]

    INTERFACE["ports"] += [
        {
            "name" : control,
            "type" : "std_logic_vector(%i downto 0)"%(interface["width"] - 1,),
            "direction" : "in"
        }
        for control, interface in INTERFACE["controls"].items()
    ]

    if CONFIG["stallable"]:
        # Generate common control
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            },
        ]

    # Generate data inputs
    for read in range(CONFIG["inputs"]):
        INTERFACE["ports"] += [
            {
                "name" : "in_%i_word_0"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            }
        ]

        ARCH_HEAD += "signal in_%i : std_logic_vector(%i downto 0);\n"%(read, CONFIG["data_width"] - 1, )
        ARCH_BODY += "in_%i <= in_%i_word_0;\n"%(read, read, )

    # Generate data outputs
    for write in range(CONFIG["outputs"]):
        INTERFACE["ports"] += [
            {
                "name" : "out_%i_word_0"%(write, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "out"
            }
        ]

        ARCH_HEAD += "signal out_%i : std_logic_vector(%i downto 0);\n"%(write, CONFIG["data_width"] - 1, )
        ARCH_BODY += "out_%i_word_0 <= out_%i;\n"%(write, write, )

    # Generate status outputs
    INTERFACE["ports"] += [
        {
            "name" : "status_%s"%(port, ),
            "type" : "std_logic",
            "direction" : "out"
        }
        for port in sorted(CONFIG["statuses"])
    ]

#####################################################################

def get_oper_details_DSP_slice(oper):
    # Pass through slice opers
    if   gen_utils.oper_mnemonic(oper) == "MOV":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "00",   # Y => 0
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).split("@")[0] in ["LSH", "RSH", "LRL", "RRL", ]:
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] in ["fetch", "acc"]:
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "shifter_out",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        else:
            raise NotImplementedError(oper)

    # Arithmetic Operations
    elif gen_utils.oper_mnemonic(oper) == "MUL":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : "in_0",
                    "B" : "in_1",
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "01",   # Y => M
                        "01",   # X => M
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : "in_0",
                    "B" : "acc",
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "01",   # Y => M
                        "01",   # X => M
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] == "acc" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : "acc",
                    "B" : "in_0",
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "01",   # Y => M
                        "01",   # X => M
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : "acc",
                    "B" : "acc",
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "01",   # Y => M
                        "01",   # X => M
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "ADD":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : "in_1",
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "11",   # Y => C
                        "11",   # X => A:B
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] in ["fetch", "acc",] and inputs[1] in ["fetch", "acc",] and inputs[0] != inputs[1]:
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "000",  # Z => 0
                        "11",   # Y => C
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "00",   # Y => 0
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0000" # P => Z + Y + X + CarryIn
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) in ["SUB", "UCMP", "SCMP", ]:
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : "in_1",
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "11",   # X => A:B
                    ]
                ),
                "ALU_MODE" : "0011" # P => Z - (Y + X + CarryIn)
            }
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0011" # P => Z - (Y + X + CarryIn)
            }
        elif inputs[0] == "acc" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "11",   # Y => C
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "0011" # P => Z - (Y + X + CarryIn)
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "00",   # Y => 0
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0011" # P => Z - (Y + X + CarryIn)
            }
        else:
            raise NotImplementedError(oper)

    # Logical Operations
    elif gen_utils.oper_mnemonic(oper) == "NOT":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "10",   # Y => all 1s
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "1101" # P => X OR (NOT Z)
            }
        elif inputs[0] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "10",   # Y => all 1s
                        "00",   # X => 0
                    ]
                ),
                "ALU_MODE" : "1101" # P => X OR (NOT Z)
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "OR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : "in_1",
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "10",   # Y => used with ALU to select or
                        "11",   # X => A:B
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        elif inputs[0] in ["fetch", "acc",] and inputs[1] in ["fetch", "acc",] and inputs[0] != inputs[1]:
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "10",   # Y => used with ALU to select or
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "10",   # Y => used with ALU to select or
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "AND":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : "in_1",
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => used with ALU to select and
                        "11",   # X => A:B
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        elif inputs[0] in ["fetch", "acc",] and inputs[1] in ["fetch", "acc",] and inputs[0] != inputs[1]:
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => used with ALU to select and
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "00",   # Y => used with ALU to select and
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "1100" # P => X and/or Z depening on Y op mod
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "XOR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : "in_1",
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "11",   # X => A:B
                    ]
                ),
                "ALU_MODE" : "0100" # P => X XOR Z
            }
        elif inputs[0] in ["fetch", "acc",] and inputs[1] in ["fetch", "acc",] and inputs[0] != inputs[1]:
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : "in_0",
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "011",  # Z => C
                        "00",   # Y => 0
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0100" # P => X XOR Z
            }
        elif inputs[0] == "acc" and inputs[1] == "acc":
            return {
                "mappings" : {
                    "A" : None,
                    "B" : None,
                    "C" : None,
                    "D" : None,
                    "AB" : None,
                },
                "OP_MODE" : "".join(
                    [
                        "010",  # Z => P
                        "00",   # Y => 0
                        "10",   # X => P
                    ]
                ),
                "ALU_MODE" : "0100" # P => X XOR Z
            }
        else:
            raise NotImplementedError(oper)

    else:
        raise NotImplementedError(oper)

def handle_DSP():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Instancate DSP slice
    IMPORTS += [
        {
            "library" : "UNISIM",
            "package" : "vcomponents",
            "parts" : "all"
        }
    ]

    ARCH_BODY += "DSP48E1_inst : DSP48E1\>\n"

    ARCH_BODY += "generic map (\>\n"

    # Disable cascading
    ARCH_BODY += "-- Disable cascading \n"
    ARCH_BODY += "A_INPUT => \"DIRECT\",\n"
    ARCH_BODY += "B_INPUT => \"DIRECT\",\n"

    # Disable pre_adder
    ARCH_BODY += "-- Disable pre_adder \n"
    ARCH_BODY += "USE_DPORT => FALSE,\n"

    # Enable / Disable multiplier as needed
    ARCH_BODY += "-- Multiplier setting \n"
    multiplier_used = any(
        [
            gen_utils.oper_mnemonic(oper) == "MUL"
            for oper in CONFIG["oper_set"]
        ]
    )
    AB_used = any(
        [
            get_oper_details_DSP_slice(oper)["mappings"]["AB"] != None
            for oper in CONFIG["oper_set"]
        ]
    )

    if not multiplier_used:
        ARCH_BODY += "USE_MULT => \"NONE\",\n"
    elif multiplier_used and not AB_used:
        ARCH_BODY += "USE_MULT => \"MULTIPLY\",\n"
    elif multiplier_used and AB_used:
        ARCH_BODY += "USE_MULT => \"DYNAMIC\",\n"
    else:
        raise ValueError("Unknown case for multiplier_used (%s) and AB_used (%s)"%(str(multiplier_used), str(AB_used)))

    # Enable / Disable pattern Detector based on presentance of equal statuses
    if "equal" in CONFIG["internal_statuses"]:
        ARCH_BODY += "-- Disable Pattern Detector \n"
        ARCH_BODY += "USE_PATTERN_DETECT => \"PATDET\",\n"
        ARCH_BODY += "AUTORESET_PATDET   => \"NO_RESET\",\n"

        # Set to only look at bits data_width -1 downto 0
        bin_mask = "1" * (48 - CONFIG["data_width"]) + "0" * CONFIG["data_width"]
        hex_mask = hex(int(bin_mask, 2))[2:]
        ARCH_BODY += "MASK    => X\"%s\",\n"%(hex_mask, )
        ARCH_BODY += "PATTERN => X\"000000000000\",\n"
        ARCH_BODY += "SEL_MASK    => \"MASK\",\n"
        ARCH_BODY += "SEL_PATTERN => \"PATTERN\",\n"
    else:
        ARCH_BODY += "-- Disable Pattern Detector \n"
        ARCH_BODY += "USE_PATTERN_DETECT => \"NO_PATDET\",\n"
        ARCH_BODY += "AUTORESET_PATDET   => \"NO_RESET\",\n"
        ARCH_BODY += "MASK    => X\"3fffffffffff\",\n"
        ARCH_BODY += "PATTERN => X\"000000000000\",\n"
        ARCH_BODY += "SEL_MASK    => \"MASK\",\n"
        ARCH_BODY += "SEL_PATTERN => \"PATTERN\",\n"

    # Handle SIMD
    ARCH_BODY += "-- Disable SIMD \n"
    ARCH_BODY += "USE_SIMD => \"ONE48\",\n"

    # Handle Pipeline registors
    ARCH_BODY += "-- Handle Pipeline registors\n"
    ARCH_BODY += "ACASCREG   => 0,\n"
    ARCH_BODY += "ALUMODEREG => 0,\n"
    ARCH_BODY += "BCASCREG   => 0,\n"

    ARCH_BODY += "AREG  => 0,\n"
    ARCH_BODY += "BREG  => 0,\n"
    ARCH_BODY += "CREG  => 0,\n"
    ARCH_BODY += "DREG  => 1,\n"
    ARCH_BODY += "ADREG => 0,\n"
    ARCH_BODY += "MREG  => 0,\n"
    ARCH_BODY += "PREG  => 1,\n"

    ARCH_BODY += "OPMODEREG  => 0,\n"
    ARCH_BODY += "INMODEREG  => 1,\n"
    ARCH_BODY += "CARRYINREG => 1,\n"
    ARCH_BODY += "CARRYINSELREG => 1\n"

    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\>\n"

    # Disable casxading
    ARCH_BODY += "-- Disable casxading \n"
    ARCH_BODY += "ACIN => (others => '1'),\n"
    ARCH_BODY += "BCIN => (others => '1'),\n"
    ARCH_BODY += "PCIN => (others => '1'),\n"
    ARCH_BODY += "CARRYCASCIN => '1',\n"
    ARCH_BODY += "MULTSIGNIN  => '1',\n"
    ARCH_BODY += "ACOUT => open,\n"
    ARCH_BODY += "BCOUT => open,\n"
    ARCH_BODY += "PCOUT => open,\n"
    ARCH_BODY += "CARRYCASCOUT => open,\n"
    ARCH_BODY += "MULTSIGNOUT  => open,\n"

    # Enable / Disable pattern Detector based on presentance of equal statuses
    if "equal" in CONFIG["internal_statuses"]:
        ARCH_BODY += "-- Disable Pattern Detector\n"
        ARCH_BODY += "OVERFLOW  => open,\n"
        ARCH_BODY += "UNDERFLOW => open,\n"
        ARCH_HEAD += "signal pattern_found : std_logic;\n"
        ARCH_BODY += "PATTERNDETECT  => pattern_found,\n"
        ARCH_BODY += "PATTERNBDETECT => open,\n"
    else:
        ARCH_BODY += "-- Disable Pattern Detector\n"
        ARCH_BODY += "OVERFLOW  => open,\n"
        ARCH_BODY += "UNDERFLOW => open,\n"
        ARCH_BODY += "PATTERNDETECT  => open,\n"
        ARCH_BODY += "PATTERNBDETECT => open,\n"

    # Handle normal data output
    ARCH_BODY += "-- Handle normal data output\n"
    ARCH_BODY += "CARRYOUT => open,\n"

    ARCH_HEAD += "signal slice_p   : std_logic_vector (47 downto 0);\n"
    ARCH_BODY += "P => slice_p,\n"

    # Handle Control ports
    ARCH_BODY += "-- Handle Control ports\n"
    ARCH_BODY += "CLK => clock,\n"

    # Generate required DSP control signals for each oper
    ALU_MODE = {}
    OP_MODE = {}

    for oper in CONFIG["oper_set"]:
        oper_details = get_oper_details_DSP_slice(oper)
        OP_MODE[oper]  = oper_details["OP_MODE"]
        ALU_MODE[oper] = oper_details["ALU_MODE"]

    if len(set(ALU_MODE.values())) != 1:
        INTERFACE["controls"]["DSP_ALU_MODE"] = {}
        INTERFACE["controls"]["DSP_ALU_MODE"]["width"] = 4
        INTERFACE["controls"]["DSP_ALU_MODE"]["values"] = ALU_MODE
    else:
        ARCH_HEAD += "constant DSP_ALU_MODE : std_logic_vector(3 downto 0) := \"%s\";\n"%(list(ALU_MODE.values())[0], )

    if len(set(OP_MODE.values())) != 1:
        INTERFACE["controls"]["DSP_OP_MODE"] = {}
        INTERFACE["controls"]["DSP_OP_MODE"]["width"] = 7
        INTERFACE["controls"]["DSP_OP_MODE"]["values"] = OP_MODE
    else:
        ARCH_HEAD += "constant DSP_OP_MODE : std_logic_vector(6 downto 0) := \"%s\";\n"%(list(OP_MODE.values())[0], )

    ARCH_BODY += "ALUMODE => DSP_ALU_MODE,\n"
    ARCH_BODY += "OPMODE  => DSP_OP_MODE,\n"
    ARCH_BODY += "INMODE  => (others => '0'),\n"
    ARCH_BODY += "CARRYINSEL => (others => '0'),\n"

    # Handle data ports
    ARCH_BODY += "-- Handle data input ports\n"
    ARCH_HEAD += "signal slice_A   : std_logic_vector (29 downto 0);\n"
    ARCH_HEAD += "signal slice_B   : std_logic_vector (17 downto 0);\n"
    ARCH_HEAD += "signal slice_C   : std_logic_vector (47 downto 0);\n"
    ARCH_HEAD += "signal slice_D   : std_logic_vector (24 downto 0);\n"

    ARCH_BODY += "A => slice_A,\n"
    ARCH_BODY += "B => slice_B,\n"
    ARCH_BODY += "C => slice_C,\n"
    ARCH_BODY += "D => slice_D,\n"
    ARCH_BODY += "CARRYIN => '1',\n"

    ARCH_BODY += "-- Reset/Clock Enable: 1-bit (each) input: Reset/Clock Enable Inputs\n"
    ARCH_BODY += "CEA1 => '0',\n"
    ARCH_BODY += "CEA2 => '0',\n"
    ARCH_BODY += "CEB1 => '0',\n"
    ARCH_BODY += "CEB2 => '0',\n"
    ARCH_BODY += "CEC  => '0',\n"
    ARCH_BODY += "CEAD => '0',\n"
    ARCH_BODY += "CED  => '0',\n"
    ARCH_BODY += "CEM  => '0',\n"

    if CONFIG["stallable"]:
        ARCH_BODY += "CEP  => enable and not stall,\n"
    else:
        ARCH_BODY += "CEP  => enable,\n"

    ARCH_BODY += "CECTRL => '0',\n"
    ARCH_BODY += "CEINMODE  => '0',\n"
    ARCH_BODY += "CEALUMODE => '0',\n"
    ARCH_BODY += "CECARRYIN => '0',\n"

    ARCH_BODY += "RSTA => '0',\n"
    ARCH_BODY += "RSTB => '0',\n"
    ARCH_BODY += "RSTC => '0',\n"
    ARCH_BODY += "RSTD => '0',\n"
    ARCH_BODY += "RSTM => '0',\n"
    ARCH_BODY += "RSTP => '0',\n"
    ARCH_BODY += "RSTCTRL => '0',\n"
    ARCH_BODY += "RSTINMODE => '0',\n"
    ARCH_BODY += "RSTALLCARRYIN => '0',\n"
    ARCH_BODY += "RSTALUMODE => '0'\n"
    ARCH_BODY += "\<);\n"

    ARCH_BODY += "\<\n"

    ####################################################################
    #  Handle Data inputs
    ####################################################################

    # Compute how slice input and AlU inputs connect
    data_mapping = {
        "A" : set(),
        "B" : set(),
        "C" : set(),
        "D" : set(),
        "AB" : set(),
    }
    for oper in CONFIG["oper_set"]:
        for port, input in get_oper_details_DSP_slice(oper)["mappings"].items():
            if input != None:
                data_mapping[port].add(input)


    # Handle slice_AB
    if len(data_mapping["AB"]) != 0:
        # Check data width
        if CONFIG["data_width"] > 48:
            raise ValueError("slice_AB can't handle data_widths larger than 48 bits")

        # Declare signal and handle mapping signal to DSP ports
        ARCH_HEAD += "signal slice_AB  : std_logic_vector (47 downto 0);\n"
        data_mapping["B"].add("AB")
        if CONFIG["data_width"] > 18:
            data_mapping["A"].add("AB")

        # Single source
        if len(data_mapping["AB"]) == 1:
            ARCH_BODY += "slice_AB <= %s;\n\n"%(gen_utils.connect_signals(list(data_mapping["AB"])[0], CONFIG["data_width"], 48, CONFIG["signal_padding"]), )

        # Multiple sources
        else:
            raise NotImplementedError()


    # slice_A not used
    if len(data_mapping["A"]) == 0:
        ARCH_BODY += "slice_A <= (others => '1');\n\n"
    # slice_A only used by slice_AB
    elif len(data_mapping["A"]) == 1 and list(data_mapping["A"])[0] == "AB":
        ARCH_BODY += "slice_A <= slice_AB(47 downto 18);\n\n"
    # slice_A used
    else:
        # Check data width
        if CONFIG["data_width"] > 25:
            warnings.warn("slice_A can only handle data_widths to up 25 bits, any bits outside 24 downto 0 will be ignored")
        # Single src
        if len(data_mapping["A"]) == 1:
            ARCH_BODY += "slice_A <= %s;\n\n"%(gen_utils.connect_signals(list(data_mapping["A"])[0], CONFIG["data_width"], 30, CONFIG["signal_padding"]), )
        # Multiple sources,
        else:
            # Generate required control signals for each oper
            INTERFACE["controls"]["DSP_A_SEL"] = {}
            INTERFACE["controls"]["DSP_A_SEL"]["width"] = tc_utils.unsigned.width(len(data_mapping["A"]) - 1)
            INTERFACE["controls"]["DSP_A_SEL"]["values"] = {}

            sel_map = {
                v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["DSP_A_SEL"]["width"] )
                for i, v in enumerate(sorted(list(data_mapping["A"])))
            }

            # Concider AB concat as well as direct port A inputs
            if "AB" in sel_map.keys():
                for oper in CONFIG["oper_set"]:
                    mapping = get_oper_details_DSP_slice(oper)["mappings"]

                    if   mapping["AB"] == None and mapping["A"] == None:
                        pass
                    elif mapping["AB"] == None and mapping["A"] != None:
                        INTERFACE["controls"]["DSP_A_SEL"]["values"][oper] = sel_map[mapping["A"]]
                    elif mapping["AB"] != None and mapping["A"] == None:
                        INTERFACE["controls"]["DSP_A_SEL"]["values"][oper] = sel_map["AB"]
                    elif mapping["AB"] != None and mapping["A"] != None:
                        raise VAlueError("slice_B can't be used as both port A and part of AB concat in the same oper")

            # Concider Only direct port A inputs
            else:
                for oper in CONFIG["oper_set"]:
                    mapping = get_oper_details_DSP_slice(oper)["mappings"]
                    if mapping["A"] != None:
                        INTERFACE["controls"]["DSP_A_SEL"]["values"][oper] = sel_map[mapping["A"]]

            ARCH_BODY += "slice_A <=\>"
            for src, control_code in sel_map.items():
                # Handle A:B
                if src == "AB":
                    ARCH_BODY += "slice_AB(47 downto 18) when DSP_A_SEL = \"%s\"\nelse "%( control_code, )
                # Handle direct src
                else:
                    ARCH_BODY += "%s when DSP_A_SEL = \"%s\"\nelse "%(
                            gen_utils.connect_signals(src, CONFIG["data_width"], 30, CONFIG["signal_padding"]),
                            control_code,
                        )
            ARCH_BODY += "(others => 'U');\<\n\n"


    # slice_B not used
    if len(data_mapping["B"]) == 0:
        ARCH_BODY += "slice_B <= (others => '1');\n\n"
    # slice_B only used by slice_AB
    elif len(data_mapping["B"]) == 1 and list(data_mapping["B"])[0] == "AB":
        ARCH_BODY += "slice_B <= slice_AB(17 downto 0);\n\n"
    # slice_B used
    else:
        # Check data width
        if CONFIG["data_width"] > 18:
            warnings.warn("slice_B can only handle data_widths to up 18 bits, any bits outside 17 downto 0 will be ignored")

        # Single src
        if len(data_mapping["B"]) == 1:
            ARCH_BODY += "slice_B <= %s;\n\n"%(gen_utils.connect_signals(list(data_mapping["B"])[0], CONFIG["data_width"], 30, CONFIG["signal_padding"]), )

        # Multiple sources
        else:
            # Generate required control signals for each oper
            INTERFACE["controls"]["DSP_B_SEL"] = {}
            INTERFACE["controls"]["DSP_B_SEL"]["width"] = tc_utils.unsigned.width(len(data_mapping["B"]) - 1)
            INTERFACE["controls"]["DSP_B_SEL"]["values"] = {}

            sel_map = {
                v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["DSP_B_SEL"]["width"] )
                for i, v in enumerate(sorted(list(data_mapping["B"])))
            }

            # Concider AB concat as well as direct port B inputs
            if "AB" in sel_map.keys():
                for oper in CONFIG["oper_set"]:
                    mapping = get_oper_details_DSP_slice(oper)["mappings"]

                    if   mapping["AB"] == None and mapping["B"] == None:
                        pass
                    elif mapping["AB"] == None and mapping["B"] != None:
                        INTERFACE["controls"]["DSP_B_SEL"]["values"][oper] = sel_map[mapping["B"]]
                    elif mapping["AB"] != None and mapping["B"] == None:
                        INTERFACE["controls"]["DSP_B_SEL"]["values"][oper] = sel_map["AB"]
                    elif mapping["AB"] != None and mapping["B"] != None:
                        raise VAlueError("slice_B can't be used as both port B and part of AB concat in the same oper")

            # Concider Only direct port B inputs
            else:
                for oper in CONFIG["oper_set"]:
                    mapping = get_oper_details_DSP_slice(oper)["mappings"]
                    if mapping["B"] != None:
                        INTERFACE["controls"]["DSP_B_SEL"]["values"][oper] = sel_map[mapping["B"]]

            ARCH_BODY += "slice_B <=\>"
            for src, control_code in sel_map.items():
                # Handle A:B
                if src == "AB":
                    ARCH_BODY += "slice_AB(17 downto 0) when DSP_B_SEL = \"%s\"\nelse "%( control_code, )
                # Handle direct src
                else:
                    ARCH_BODY += "%s when DSP_B_SEL = \"%s\"\nelse "%(
                            gen_utils.connect_signals(src, CONFIG["data_width"], 18, CONFIG["signal_padding"]),
                            control_code,
                        )
            ARCH_BODY += "(others => 'U');\<\n\n"


    # slice_C not used
    if len(data_mapping["C"]) == 0:
        ARCH_BODY += "slice_C <= (others => '1');\n\n"
    # slice_C used
    else:
        # Check data width
        if CONFIG["data_width"] > 48:
            raise ValueError("slice_C can't handle data_widths larger than 48 bits")

        # Single source
        if len(data_mapping["C"]) == 1:
            ARCH_BODY += "slice_C <= %s;\n\n"%(gen_utils.connect_signals(list(data_mapping["C"])[0], CONFIG["data_width"], 48, CONFIG["signal_padding"]), )
        # Multiple sources
        else:
            # Generate required control signals for each oper
            INTERFACE["controls"]["DSP_C_SEL"] = {}
            INTERFACE["controls"]["DSP_C_SEL"]["width"] = tc_utils.unsigned.width(len(data_mapping["C"]) - 1)
            INTERFACE["controls"]["DSP_C_SEL"]["values"] = {}

            sel_map = {
                v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["DSP_C_SEL"]["width"] )
                for i, v in enumerate(sorted(list(data_mapping["C"])))
            }

            for oper in CONFIG["oper_set"]:
                mapping = get_oper_details_DSP_slice(oper)["mappings"]
                if mapping["C"] != None:
                    INTERFACE["controls"]["DSP_C_SEL"]["values"][oper] = sel_map[mapping["C"]]

            ARCH_BODY += "slice_C <=\>"
            for src, control_code in sel_map.items():
                ARCH_BODY += "%s when DSP_C_SEL = \"%s\"\nelse "%(
                        gen_utils.connect_signals(src, CONFIG["data_width"], 48, CONFIG["signal_padding"]),
                        control_code,
                    )
            ARCH_BODY += "(others => 'U');\<\n\n"


    # slice_D not used
    if len(data_mapping["D"]) == 0:
        ARCH_BODY += "slice_D <= (others => '1');\n\n"
    # slice_D used
    else:
        if CONFIG["data_width"] < 25:
            raise ValueError("slice_D can't handle data_widths larger than 25 bits")

        raise NotImplementedError()


    ####################################################################
    #  Handle Outputs
    ####################################################################

    # Connect data outputs
    ARCH_HEAD += "signal acc : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )
    ARCH_BODY += "acc <= slice_p(out_0'left downto 0);\n\n"
    ARCH_BODY += "out_0 <= acc;\n\n"

    # Handle internal statuses
    SCMP_used = any([gen_utils.oper_mnemonic(oper) == "SCMP" for oper in CONFIG["oper_set"]])
    UCMP_used = any([gen_utils.oper_mnemonic(oper) == "UCMP" for oper in CONFIG["oper_set"]])

    if "operand_0_sign" in CONFIG["delayed_statuses"]:
        ARCH_HEAD += "signal operand_0_sign_in, operand_0_sign_out : std_logic;\n"

        ARCH_BODY += "operand_0_sign_in <=\>in_0(in_0'left) when DSP_OP_MODE(4) = '1'\n"
        ARCH_BODY += "else acc(acc'left) when DSP_OP_MODE(4) = '0'\n"
        ARCH_BODY += "else 'U';\<\n\n"

    if "operand_1_sign" in CONFIG["delayed_statuses"]:
        ARCH_HEAD += "signal operand_1_sign_in, operand_1_sign_out : std_logic;\n"

        ARCH_BODY += "operand_1_sign_in <=\>in_0(in_0'left) when DSP_OP_MODE(1 downto 0) = \"00\"\n"
        ARCH_BODY += "else in_1(in_1'left) when DSP_OP_MODE(1 downto 0) = \"11\"\n"
        ARCH_BODY += "else acc(acc'left) when DSP_OP_MODE(1 downto 0) = \"10\"\n"
        ARCH_BODY += "else 'U';\<\n\n"

    if len(CONFIG["delayed_statuses"]) != 0:
        reg_interface, reg_name = register.generate_HDL(
            {
                "async_forces"  : 0,
                "sync_forces"   : 0,
                "has_enable"    : True
            },
            OUTPUT_PATH,
            "register",
            True,
            False
        )


        # Buffer all delayed_statuses together
        ARCH_HEAD += "signal delayed_statuses_in, delayed_statuses_out : std_logic_vector(%i downto 0);\n"%(len(CONFIG["delayed_statuses"]) - 1, )

        ARCH_BODY += "delayed_statuses_reg : entity work.%s(arch)\>\n"%(reg_name, )

        ARCH_BODY += "generic map ( data_width => %i )\n"%(len(CONFIG["delayed_statuses"]))

        ARCH_BODY += "port map (\n\>"

        if CONFIG["stallable"]:
            ARCH_BODY += "enable  => enable and not stall,\n"
        else:
            ARCH_BODY += "enable  => enable,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => delayed_statuses_in,\n"
        ARCH_BODY += "data_out => delayed_statuses_out\n"
        ARCH_BODY += "\<);\<\n\n"

        # Pack and unpack statuses into buffer
        for i, status in enumerate(CONFIG["delayed_statuses"]):
            ARCH_BODY += "delayed_statuses_in(%i) <= %s_in;\n"%(i, status, )
            ARCH_BODY += "%s_out <= delayed_statuses_out(%i);\n\n"%(status, i, )

    if "equal" in CONFIG["internal_statuses"]:
        ARCH_HEAD += "signal internal_equal : std_logic;\n"
        ARCH_BODY += "internal_equal <= pattern_found;\n\n"

    if "lesser" in CONFIG["internal_statuses"]:
        ARCH_HEAD += "signal internal_lesser : std_logic;\n"

        if   SCMP_used and UCMP_used:
            # Generate required control signals for each oper
            INTERFACE["controls"]["LESSER_DATATYPE"] = {}
            INTERFACE["controls"]["LESSER_DATATYPE"]["width"] = 1 # 2 options with 1 bit sel required
            INTERFACE["controls"]["LESSER_DATATYPE"]["values"] = {}

            sel_map = {
                "UCMP" : "0",
                "SCMP" : "1",
            }

            for oper in CONFIG["oper_set"]:
                mnemonic = gen_utils.oper_mnemonic(oper)
                if mnemonic in sel_map.keys():
                    INTERFACE["controls"]["LESSER_DATATYPE"]["values"][oper] = sel_map[mnemonic]

            # Delay LESSER_DATATYPE until after sub runs
            reg_interface, reg_name = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : True
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )


            # Buffer all delayed_statuses together
            ARCH_HEAD += "signal LESSER_DATATYPE_synced : std_logic_vector(%i downto 0);\n"%(INTERFACE["controls"]["LESSER_DATATYPE"]["width"]  - 1, )

            ARCH_BODY += "LESSER_DATATYPE_reg : entity work.%s(arch)\>\n"%(reg_name, )

            ARCH_BODY += "generic map ( data_width => %i )\n"%(INTERFACE["controls"]["LESSER_DATATYPE"]["width"], )

            ARCH_BODY += "port map (\n\>"

            if CONFIG["stallable"]:
                ARCH_BODY += "enable  => enable and not stall,\n"
            else:
                ARCH_BODY += "enable  => enable,\n"

            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in  => LESSER_DATATYPE,\n"
            ARCH_BODY += "data_out => LESSER_DATATYPE_synced\n"
            ARCH_BODY += "\<);\<\n\n"

            assert("operand_0_sign" in CONFIG["delayed_statuses"])
            assert("operand_1_sign" in CONFIG["delayed_statuses"])

            ARCH_BODY += "internal_lesser <=\>slice_p(acc'left + 1) when LESSER_DATATYPE_synced = \"0\"\n"
            ARCH_BODY += "else (\>\n"
            ARCH_BODY += "(operand_0_sign_out and not operand_1_sign_out) -- -ve - +ve; -ve < +ve\n"
            ARCH_BODY += "or (operand_0_sign_out and acc(acc'left)) -- +ve - X => -ve, X either -ve (-ve < +ve) or X larger +ve (therefore <)\n"
            ARCH_BODY += "or (not operand_1_sign_out and acc(acc'left))-- X - +ve => -ve, X either -ve (-ve < +ve) or X smaller +ve (therefore <)\n"
            ARCH_BODY += "\<) when LESSER_DATATYPE_synced = \"1\"\n"
            ARCH_BODY += "else 'U';\n\<\n"

        elif SCMP_used and not UCMP_used:
            assert("operand_0_sign" in CONFIG["delayed_statuses"])
            assert("operand_1_sign" in CONFIG["delayed_statuses"])
            ARCH_BODY += "internal_lesser <=\>(\>\n"
            ARCH_BODY += "(operand_0_sign_out and not operand_1_sign_out) -- -ve - +ve; -ve < +ve\n"
            ARCH_BODY += "or (operand_0_sign_out and acc(acc'left)) -- +ve - X => -ve, X either -ve (-ve < +ve) or X larger +ve (therefore <)\n"
            ARCH_BODY += "or (not operand_1_sign_out and acc(acc'left))-- X - +ve => -ve, X either -ve (-ve < +ve) or X smaller +ve (therefore <)\n"
            ARCH_BODY += "\<);\<\n"

        elif not SCMP_used and UCMP_used:
            ARCH_BODY += "internal_lesser <= slice_p(acc'left + 1);\n\n"
        else:
            raise ValueError("Lesser internal status requires SCMP and/ot UCMP to be used")

    if "greater" in CONFIG["internal_statuses"]:
        ARCH_HEAD += "signal internal_greater : std_logic;\n"

        assert("equal" in CONFIG["internal_statuses"])
        assert("lesser" in CONFIG["internal_statuses"])

        ARCH_BODY += "internal_greater <= internal_lesser nor internal_equal;\n\n"

    # Connect output statuses
    for status in sorted(CONFIG["statuses"]):
        ARCH_BODY += "status_%s <= internal_%s;\n\n"%(status, status)



#####################################################################

def get_oper_details_shifter(oper):
    # Non shift operations
    if   gen_utils.oper_mnemonic(oper) in [
        "MOV",
        "MUL", "ADD", "SUB", "UCMP", "SCMP",
        "NOT", "OR", "AND", "XOR",

    ]:
        return {
            "input" : None,
            "bits"  : None,
            "type"  : None,
        }
    elif gen_utils.oper_mnemonic(oper).split("@")[0] in ["LSH", "RSH", "LRL", "RRL", ]:
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "input" : "in_0",
                "bits"  : int(gen_utils.oper_mnemonic(oper).split("@")[1]),
                "type"  : gen_utils.oper_mnemonic(oper).split("@")[0],
            }
        elif inputs[0] == "acc":
            return {
                "input" : "acc",
                "bits"  : int(gen_utils.oper_mnemonic(oper).split("@")[1]),
                "type"  : gen_utils.oper_mnemonic(oper).split("@")[0],
            }
        else:
            raise NotImplementedError(oper)
    else:
        raise NotImplementedError(oper)

def connect_LSH(bits):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    return "(%s, others => '0')"%(
        ", ".join(
            [
                "(%i) => shifter_in(%i)"%(i, i - bits)
                for i in range(bits, CONFIG["data_width"], 1)
            ]
        )
    )

def connect_LRL(bits):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    return "(%s)"%(
        ", ".join(
            [
                "(%i) => shifter_in(%i)"%(i, (i - bits)%CONFIG["data_width"])
                for i in range(CONFIG["data_width"])
            ]
        )
    )

def connect_RSH(bits):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    return "(%s, others => '0')"%(
        ", ".join(
            [
                "(%i) => shifter_in(%i)"%(i - bits, i)
                for i in range(bits, CONFIG["data_width"], 1)
            ]
        )
    )

def connect_RRL(bits):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    return "(%s)"%(
        ", ".join(
            [
                "(%i) => shifter_in(%i)"%(i, (i + bits)%CONFIG["data_width"])
                for i in range(CONFIG["data_width"])
            ]
        )
    )

shift_type_connect_map= {
    "LSH" : connect_LSH,
    "RSH" : connect_RSH,
    "LRL" : connect_LRL,
    "RRL" : connect_RRL,
}

def handle_shifter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Collect all shifts from oper_set
    shifts = []
    for oper in CONFIG["oper_set"]:
        details = get_oper_details_shifter(oper)
        if   details["type"] == None and details["bits"] == None:
            pass
        elif details["type"] != None and details["bits"] != None:
            d = {
                "type" : details["type"],
                "bits" : details["bits"],
            }

            if d not in shifts:
                shifts.append(d)
        else:
            raise ValueError("A shift's type and bits must wither both be set or both None")
    shifts = sorted(shifts, key=lambda d : str(d))

    # Check shift is used
    if len(shifts) != 0:
        # Handle shifter_in
        input_map = set()
        for oper in CONFIG["oper_set"]:
            input = get_oper_details_shifter(oper)["input"]
            if input != None:
                input_map.add(input)

        if len(input_map) == 0:
            raise ValueError("shifter requires at least 1 input")
        else:
            # Declare signal
            ARCH_HEAD += "signal shifter_in : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )

            # Single source
            if len(input_map) == 1:
                ARCH_BODY += "shifter_in <= %s;\n\n"%(list(input_map)[0], )

            # Multiple sources
            else:
                # Generate required control signals for each oper
                INTERFACE["controls"]["SHIFT_IN_SEL"] = {}
                INTERFACE["controls"]["SHIFT_IN_SEL"]["width"] = tc_utils.unsigned.width(len(input_map) - 1)
                INTERFACE["controls"]["SHIFT_IN_SEL"]["values"] = {}

                sel_map = {
                    v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["SHIFT_IN_SEL"]["width"] )
                    for i, v in enumerate(sorted(list(input_map)))
                }

                for oper in CONFIG["oper_set"]:
                    input = get_oper_details_shifter(oper)["input"]
                    if input != None:
                        INTERFACE["controls"]["SHIFT_IN_SEL"]["values"][oper] = sel_map[input]
                        input_map.add(input)

                ARCH_BODY += "shifter_in <=\>"
                for src, control_code in sel_map.items():
                    ARCH_BODY += "%s when SHIFT_IN_SEL = \"%s\"\nelse "%(
                            src,
                            control_code,
                        )
                ARCH_BODY += "(others => 'U');\<\n\n"

        # Generate shifter logic
        ARCH_HEAD += "signal shifter_out : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1)
        if len(shifts) == 1:
                ARCH_BODY += "shifter_out <= %s;\n"%(
                    shift_type_connect_map[shifts[0]["type"]](shifts[0]["bits"])
                )
        else:
            # Generate required control signals for each oper
            INTERFACE["controls"]["SHIFT_SEL"] = {}
            INTERFACE["controls"]["SHIFT_SEL"]["width"] = tc_utils.unsigned.width(len(shifts) - 1)
            INTERFACE["controls"]["SHIFT_SEL"]["values"] = {}

            shift_map = {
                v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["SHIFT_SEL"]["width"] )
                for i, v in enumerate([
                    "%s@%i"%(shift["type"], shift["bits"], )
                    for shift in shifts
                ])
            }

            for oper in CONFIG["oper_set"]:
                try:
                    INTERFACE["controls"]["SHIFT_SEL"]["values"][oper] = shift_map[gen_utils.oper_mnemonic(oper)]
                except KeyError:
                    pass

            # Generate shifter VHDL
            ARCH_BODY += "shifter_out <=\>"
            for shift, control_code in shift_map.items():
                ARCH_BODY += "%s when SHIFT_SEL = \"%s\"\nelse "%(
                    shift_type_connect_map[shift.split("@")[0]](int(shift.split("@")[1]) ),
                    control_code,
                )
            ARCH_BODY += "(others => 'U');\<\n\n"
