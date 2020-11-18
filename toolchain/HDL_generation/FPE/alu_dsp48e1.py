# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

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

    config_out["statuses"] = config_in["statuses"]

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
                "name" : "in_%i"%(read),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            }
        ]

    # Generate data outputs
    for write in range(CONFIG["outputs"]):
        INTERFACE["ports"] += [
            {
                "name" : "out_%i"%(write),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "out"
            }
        ]

    # Generate status outputs
    for port in sorted(CONFIG["statuses"]):
        INTERFACE["ports"] += [
            {
                "name" : "status_%s"(port, ),
                "type" : "std_logic",
                "direction" : "out"
            }
        ]

#####################################################################

def get_DSP_mappings(oper):
    # Pass though slice
    if   gen_utils.oper_mnemonic(oper) == "MOV":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : None,
            }
        elif inputs[0] == "acc":
            return {
                "A" : None,
                "B" : None,
                "C" : None,
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("LSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "shifter_out",
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("RSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "shifter_out",
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)

    # Arithmetic Operations
    elif gen_utils.oper_mnemonic(oper) == "MUL":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : "in_0",
                "B" : "in_1",
                "C" : None,
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "ADD":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : "in_1",
            }
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "SUB":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : "in_1",
            }
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "CMP":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : "in_0",
                "B" : None,
                "C" : None,
                "D" : None,
                "A:B" : "in_1",
            }
        elif inputs[0] == "acc"   and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)

    # Logical Operations
    elif gen_utils.oper_mnemonic(oper) == "NOT":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : None,
            }
        elif inputs[0] == "acc":
            return {
                "A" : None,
                "B" : None,
                "C" : None,
                "D" : None,
                "A:B" : None,
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "OR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : "in_1",
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "AND":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : "in_1",
            }
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "XOR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return {
                "A" : None,
                "B" : None,
                "C" : "in_0",
                "D" : None,
                "A:B" : "in_1",
            }
        else:
            raise NotImplementedError(oper)

    else:
        raise NotImplementedError(oper)

def get_DSP_OP_MODE(oper):
    # Passthrough Operations
    if   gen_utils.oper_mnemonic(oper) == "MOV":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "00",   # X => 0
                ]
            )
        elif inputs[0] == "acc":
            return "".join(
                [
                    "010",  # Z => P
                    "00",   # Y => 0
                    "00",   # X => 0
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("LSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "00",   # X => 0
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("RSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "00",   # X => 0
                ]
            )
        else:
            raise NotImplementedError(oper)

    # Arithmetic Operations
    elif gen_utils.oper_mnemonic(oper) == "MUL":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "000",  # Z => 0
                    "01",   # Y => M
                    "01",   # X => M
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "ADD":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "000",  # Z => 0
                    "11",   # Y => C
                    "11",   # X => A:B
                ]
            )
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return "".join(
                [
                    "000",  # Z => 0
                    "11",   # Y => C
                    "10",   # X => P
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "SUB":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "11",   # X => A:B
                ]
            )
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "10",   # X => P
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "CMP":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "11",   # X => A:B
                ]
            )
        elif inputs[0] == "acc"   and inputs[1] == "fetch":
            return "".join(
                [
                    "010",  # Z => P
                    "11",   # Y => C
                    "00",   # X => 0
                ]
            )
        else:
            raise NotImplementedError(oper)

    # Logical Operations
    elif gen_utils.oper_mnemonic(oper) == "NOT":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "10",   # Y => all 1s
                    "00",   # X => 0
                ]
            )
        elif inputs[0] == "acc":
            return "".join(
                [
                    "010",  # Z => P
                    "10",   # Y => all 1s
                    "00",   # X => 0
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "OR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "10",   # Y => -1
                    "11",   # X => A:B
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "AND":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "11",   # X => A:B
                ]
            )
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "XOR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "".join(
                [
                    "011",  # Z => C
                    "00",   # Y => 0
                    "11",   # X => A:B
                ]
            )
        else:
            raise NotImplementedError(oper)

    else:
        raise NotImplementedError(oper)

def get_DSP_ALU_MODE(oper):
    # Passthrough Operations
    if   gen_utils.oper_mnemonic(oper) == "MOV":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "0000" # P => Z + Y + X + CarryIn
        elif inputs[0] == "acc":
            return "0000" # P => Z + Y + X + CarryIn
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("LSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "0000" # P => Z + Y + X + CarryIn
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper).startswith("RSH_"):
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "0000" # P => Z + Y + X + CarryIn
        else:
            raise NotImplementedError(oper)

    # Arithmetic Operations
    elif gen_utils.oper_mnemonic(oper) == "MUL":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "0000" # P => Z + Y + X + CarryIn
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "ADD":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "0000" # P => Z + Y + X + CarryIn
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return "0000" # P => Z + Y + X + CarryIn
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "SUB":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "0011" # P => Z - (Y + X + CarryIn)
        elif inputs[0] == "fetch" and inputs[1] == "acc":
            return "0011" # P => Z - (Y + X + CarryIn)
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "CMP":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "0011" # P => Z - (Y + X + CarryIn)
        elif inputs[0] == "acc"   and inputs[1] == "fetch":
            return "0011" # P => Z - (Y + X + CarryIn)
        else:
            raise NotImplementedError(oper)

    # Logical Operations
    elif gen_utils.oper_mnemonic(oper) == "NOT":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch":
            return "1101" # P => X OR (NOT Z)
        elif inputs[0] == "acc":
            return "1101", # P => X OR (NOT Z)
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "OR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "1100" # P => X and/or Z
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "AND":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "1100" # P => X and/or Z
        else:
            raise NotImplementedError(oper)
    elif gen_utils.oper_mnemonic(oper) == "XOR":
        inputs = gen_utils.oper_srcs(oper)
        if   inputs[0] == "fetch" and inputs[1] == "fetch":
            return "0111" # P => X XOR Z
        else:
            raise NotImplementedError(oper)

    else:
        raise NotImplementedError(oper)

def handle_DSP():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate required DSP control signals for each oper
    INTERFACE["controls"]["DSP_ALU_MODE"] = {}
    INTERFACE["controls"]["DSP_ALU_MODE"]["width"] = 4
    INTERFACE["controls"]["DSP_ALU_MODE"]["values"] = {}

    INTERFACE["controls"]["DSP_OP_MODE"] = {}
    INTERFACE["controls"]["DSP_OP_MODE"]["width"] = 7
    INTERFACE["controls"]["DSP_OP_MODE"]["values"] = {}

    for oper in CONFIG["oper_set"]:
        INTERFACE["controls"]["DSP_OP_MODE"]["values"][oper]  = get_DSP_OP_MODE(oper)
        INTERFACE["controls"]["DSP_ALU_MODE"]["values"][oper] = get_DSP_ALU_MODE(oper)

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

    # Enable/ disable multiplier as needed
    ARCH_BODY += "-- Multiplier setting \n"
    multiplier_used = any(
        [
            gen_utils.oper_mnemonic(oper) == "MUL"
            for oper in CONFIG["oper_set"]
        ]
    )
    AB_used = any(
        [
            "A:B" in get_DSP_mappings(oper)
            for oper in CONFIG["oper_set"]
        ]
    )

    if multiplier_used == False:
        ARCH_BODY += "USE_MULT => \"NONE\",\n"
    elif multiplier_used == True and AB_used == False:
        ARCH_BODY += "USE_MULT => \"MULTIPLY\",\n"
    elif multiplier_used == True and AB_used == True:
        ARCH_BODY += "USE_MULT => \"DYNAMIC\",\n"
    else:
        raise ValueError("Unknown case for multiplier_used (%s) and AB_used (%s)"%(str(multiplier_used), str(AB_used)))

    # Disable pattern Detector
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

    # Disable Pattern Detector
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
    ARCH_BODY += "OPMODE  => DSP_OP_MODE,\n"
    ARCH_BODY += "ALUMODE => DSP_ALU_MODE,\n"
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

    # Compute how slice input and AlU inputs connect
    data_mapping = {
        "A" : set(),
        "B" : set(),
        "C" : set(),
        "D" : set(),
        "A:B" : set(),
    }
    for oper in CONFIG["oper_set"]:
        for port, input in get_DSP_mappings(oper).items():
            if input != None:
                data_mapping[port].add(input)

    # Handle slice A
    # Not used
    if (    ( CONFIG["data_width"] <= 18 and len(data_mapping["A"]) == 0)
        or  ( CONFIG["data_width"] >  18 and len(data_mapping["A"]) + len(data_mapping["A:B"]) == 0 )
    ):
        ARCH_BODY += "slice_A <= (others => '1');\n"
    # Single source
    elif(   ( CONFIG["data_width"] <= 18 and len(data_mapping["A"]) == 1)
        or  ( CONFIG["data_width"] >  18 and len(data_mapping["A"]) + len(data_mapping["A:B"]) == 1 )
    ):
        # Acting as sole A input
        if len(data_mapping["A"]) == 1:
            if CONFIG["data_width"] > 30:
                raise ValueError("slice_A can't handle data_widths larger than 30 bits")

            ARCH_BODY += "slice_A(%i downto 0) <= %s;\n"%(CONFIG["data_width"] - 1, list(data_mapping["A"])[0])
            if CONFIG["data_width"] < 30:
                ARCH_BODY += "slice_A(29 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
        # Acting as A:B input
        else:
            if CONFIG["data_width"] > 48:
                raise ValueError("A:B can't handle data_widths larger than 48 bits")

            ARCH_BODY += "slice_A(%i downto 0) <= %s(%s'left downto 18);\n"%(CONFIG["data_width"] - 18 - 1, list(data_mapping["A"])[0], list(data_mapping["A"])[0])
            if CONFIG["data_width"] < 48:
                ARCH_BODY += "slice_A(29 downto %i) <= (others => '0');\n"%(CONFIG["data_width"]  - 18, )
    # Multiple sources
    else:
        raise NotImplementedError()

    # Handle slice B
    # Not used
    if ( len(data_mapping["B"] | data_mapping["A:B"]) == 0 ):
        ARCH_BODY += "slice_B <= (others => '1');\n"
    # Single source
    elif( len(data_mapping["B"] | data_mapping["A:B"]) == 1 ):
        # Acting as sole B width check
        if len(data_mapping["A"]) == 1 and CONFIG["data_width"] > 18:
            raise ValueError("slice_B can't handle data_widths larger than 18 bits")

        ARCH_BODY += "slice_B(%i downto 0) <= %s;\n"%(CONFIG["data_width"] - 1, list(data_mapping["B"] | data_mapping["A:B"])[0])
        if CONFIG["data_width"] < 18:
            ARCH_BODY += "slice_B(17 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
    # Multiple sources
    else:
        raise NotImplementedError()

    # Handle slice C
    # Not used
    if len(data_mapping["C"]) == 0:
        ARCH_BODY += "slice_C <= (others => '1');\n"
    # Single source
    elif len(data_mapping["C"]) == 1:
        if CONFIG["data_width"] > 48:
            raise ValueError("slice_C can't handle data_widths larger than 48 bits")

        ARCH_BODY += "slice_C <= %s;\n"%(gen_utils.connect_signals(list(data_mapping["C"])[0], CONFIG["data_width"], 48), )
    # Multiple sources
    else:
        # Generate required control signals for each oper
        INTERFACE["controls"]["DSP_C_SEL"] = {}
        INTERFACE["controls"]["DSP_C_SEL"]["width"] = tc_utils.unsigned.width(len(data_mapping["C"]) - 1)
        INTERFACE["controls"]["DSP_C_SEL"]["values"] = {}

        sel_map = {
            v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["DSP_C_SEL"]["width"] )
            for i, v in enumerate(data_mapping["C"])
        }

        for oper in CONFIG["oper_set"]:
            try:
                INTERFACE["controls"]["DSP_C_SEL"]["values"][oper] = sel_map[get_DSP_mappings(oper)["C"]]
            except KeyError:
                pass

        ARCH_BODY += "slice_C <=\>"
        for src, control_code in sel_map.items():
            ARCH_BODY += "%s when DSP_C_SEL = \"%s\"\nelse "%(
                    gen_utils.connect_signals(src, CONFIG["data_width"], 48),
                    control_code,
                )
        ARCH_BODY += "(others => 'U')\<\n;"

    # Handle slice D
    # Not used
    if len(data_mapping["D"]) == 0:
        ARCH_BODY += "slice_D <= (others => '1');\n"
    # Single source
    elif len(data_mapping["D"]) == 1:
        if CONFIG["data_width"] < 25:
            raise ValueError("slice_D can't handle data_widths larger than 25 bits")

        ARCH_BODY += "slice_D(%i downto 0) <= %s;\n"%(CONFIG["data_width"] - 1, list(data_mapping["D"])[0])
        if CONFIG["data_width"] < 25:
            ARCH_BODY += "slice_D(25 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
    # Multiple sources
    else:
        raise NotImplementedError()


    # Connect data outputs
    ARCH_BODY += "out_0 <= slice_p(out_0'left downto 0);\n"
    if "lesser" in CONFIG["statuses"]:
        ARCH_BODY += "status_lesser <= slice_p(out_0'left);\n"

#####################################################################

def handle_shifter():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    shifts = set (
        [
            gen_utils.oper_mnemonic(oper)
            for oper in CONFIG["oper_set"]
            if (
                gen_utils.oper_mnemonic(oper).startswith("LSH_")
                or gen_utils.oper_mnemonic(oper).startswith("RSH_")
            )
        ]
    )

    if len(shifts) != 0:
        # Generate required control signals for each oper
        INTERFACE["controls"]["SHIFT_SEL"] = {}
        INTERFACE["controls"]["SHIFT_SEL"]["width"] = tc_utils.unsigned.width(len(shifts) - 1)
        INTERFACE["controls"]["SHIFT_SEL"]["values"] = {}

        shift_map = {
            v : tc_utils.unsigned.encode(i, INTERFACE["controls"]["SHIFT_SEL"]["width"] )
            for i, v in enumerate(shifts)
        }

        for oper in CONFIG["oper_set"]:
            try:
                INTERFACE["controls"]["SHIFT_SEL"]["values"][oper] = shift_map[gen_utils.oper_mnemonic(oper)]
            except KeyError:
                pass

        # Generate shifter VHDL
        ARCH_HEAD += "signal shifter_out : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1)
        ARCH_BODY += "shifter_out <=\>"
        for shift, control_code in shift_map.items():
            dir, bits = shift.split("_")
            bits = int(bits)

            print(dir, bits)
            # Handle left shift
            if dir == "LSH":
                ARCH_BODY += "(%s, others => '0') when SHIFT_SEL = \"%s\"\nelse "%(
                    ", ".join(
                        [
                            "(%i) => in_0(%i)"%(i, i - bits)
                            for i in range(bits, CONFIG["data_width"], 1)
                        ]
                    ),
                    control_code,
                )
            # Handle right shift
            elif dir == "RSH":
                ARCH_BODY += "(%s, others => '0') when SHIFT_SEL = \"%s\"\nelse "%(
                    ", ".join(
                        [
                            "(%i) => in_0(%i)"%(i - bits, i)
                            for i in range(bits, CONFIG["data_width"], 1)
                        ]
                    ),
                    control_code,
                )
            else:
                raise NotImplementedError(shift)
        ARCH_BODY += "(others => 'U')\<\n;"
