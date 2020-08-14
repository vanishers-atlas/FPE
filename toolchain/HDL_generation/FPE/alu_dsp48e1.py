# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

def generate_HDL(config, output_path, module_name, generate_name=True,force_generation=True):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION

    # Moves parameters into global scope
    CONFIG = config
    OUTPUT_PATH = output_path
    MODULE_NAME = gen_utils.handle_module_name(module_name, config, generate_name)
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
        process_operations()
        generate_ports()
        instanate_Slice()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

operation_sel_map = {
    "ADD#fetch~acc#acc" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "000",  # Z => 0
            "11",   # Y => C
            "10",   # X => P

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "ADD#fetch~fetch#acc" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "000",  # Z => 0
            "11",   # Y => C
            "11",   # X => A:B

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "ADD#fetch~fetch#store" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "000",  # Z => 0
            "11",   # Y => C
            "11",   # X => A:B

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "ADD#fetch~acc#store" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "000",  # Z => 0
            "11",   # Y => C
            "10",   # X => P

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "SUB#fetch~fetch#store" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "11",   # X => A:B

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "SUB#fetch~acc#acc" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "10",   # X => P

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "SUB#fetch~fetch#acc" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "11",   # X => A:B

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "SUB#fetch~acc#store" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "10",   # X => P

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "MUL#fetch~fetch#acc" : {
        "fetch_mapping" : ["A", "B"],
        "controls" : "".join([
            "000",  # Z => 0
            "01",   # Y => M
            "01",   # X => M

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "MUL#fetch~fetch#store" : {
        "fetch_mapping" : ["A", "B"],
        "controls" : "".join([
            "000",  # Z => 0
            "01",   # Y => M
            "01",   # X => M

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "AND#fetch~fetch#store" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "11",   # X => A:B

            "1100", # P => X and/or Z
        ]),
    },

    "OR#fetch~fetch#store" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "10",   # Y => -1
            "11",   # X => A:B

            "1100", # P => X and/or Z
        ]),
    },

    "XOR#fetch~fetch#store" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "11",   # X => A:B

            "0111", # P => X XOR Z
        ]),
    },

    "CMP#acc~fetch#" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "010",  # Z => P
            "11",   # Y => C
            "00",   # X => 0

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "CMP#fetch~fetch#" : {
        "fetch_mapping" : ["C", "A:B"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "11",   # X => A:B

            "0011", # P => Z - (Y + X + CarryIn)
        ]),
    },

    "MOV#fetch#acc" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "00",   # X => 0

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "MOV#fetch#store" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "011",  # Z => C
            "00",   # Y => 0
            "00",   # X => 0

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "MOV#acc#store" : {
        "fetch_mapping" : [],
        "controls" : "".join([
            "010",  # Z => P
            "00",   # Y => 0
            "00",   # X => 0

            "0000", # P => Z + Y + X + CarryIn
        ]),
    },

    "NOT#fetch#store" : {
        "fetch_mapping" : ["C"],
        "controls" : "".join([
            "011",  # Z => C
            "10",   # Y => all 1s
            "00",   # X => 0

            "0000", # P => x NOR Z
        ]),
    },

    "NOT#acc#store" : {
        "fetch_mapping" : [],
        "controls" : "".join([
            "010",  # Z => P
            "10",   # Y => all 1s
            "00",   # X => 0

            "0000", # P => x NOR Z
        ]),
    },
}

def process_operations():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Collect required data ports for ops
    for op in CONFIG["operations"]:
        num_fetchs = gen_utils.decode_num_fetchs(op)
        if num_fetchs > CONFIG["inputs"]:
            raise ValueError("Operation, %s, requires inputs >= %i"%(op, num_fetchs))

        num_stores = gen_utils.decode_num_stores(op)
        if num_stores > CONFIG["outputs"]:
            raise ValueError("Operation, %s, requires outputs >= %i"%(op, num_stores))

    # Generate required control signals for each op
    INTERFACE["operation_sel"] = {}
    for op in CONFIG["operations"]:
        INTERFACE["operation_sel"][op] = operation_sel_map[op]["controls"]

    # Flag number of clock cycles needed
    INTERFACE["cycles required"] = 1

def generate_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Generate common control
    INTERFACE["ports"] += [
        { "name" : "clock" , "type" : "std_logic", "direction" : "in" },
        { "name" : "enable", "type" : "std_logic", "direction" : "in" },
        {
            "name" : "operation_sel",

            # 10 downto 0 as 7 for op(erand) mode and 4 for 4 ALU mode = 11 bits
            "type" : "std_logic_vector(10 downto 0)",

            "direction" : "in"
        },
    ]

    # Generate data inputs
    for read in range(CONFIG["inputs"]):
        INTERFACE["ports"] += [ { "name" : "in_%i"%(read), "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ), "direction" : "in" } ]

    # Generate data outputs
    for write in range(CONFIG["outputs"]):
        INTERFACE["ports"] += [ { "name" : "out_%i"%(write), "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ), "direction" : "out" } ]

    # Generate status outputs
    for port in sorted(CONFIG["statuses"]):
        INTERFACE["ports"] += [ { "name" : "status_" + port, "type" : "std_logic", "direction" : "out" } ]

def instanate_Slice():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    IMPORTS += [ {"library" : "UNISIM", "package" : "vcomponents", "parts" : "all"} ]

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
    use_mult = "\"NONE\""
    has_mul = False
    has_AB = False
    for op in CONFIG["operations"]:
        if op.split("#")[0] == "MUL":
            use_mult = "\"MULTIPLY\""
            has_mul = True
        if "A:B" in operation_sel_map[op]["fetch_mapping"]:
            has_AB = True
        if has_mul and has_AB:
            use_mult = "\"DYNAMIC\""
            break
    ARCH_BODY += "USE_MULT => %s,\n"%(use_mult)

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

    ARCH_HEAD += "signal slice_operandSel   : std_logic_vector (6 downto 0);\n"
    ARCH_HEAD += "signal slice_ALUmode      : std_logic_vector (3  downto 0);\n"

    ARCH_BODY += "OPMODE  => slice_operandSel,\n"
    ARCH_BODY += "ALUMODE => slice_ALUmode,\n"
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

    # Connect controls from ID
    ARCH_BODY += "slice_operandSel <= operation_sel(10 downto 4);\n"
    ARCH_BODY += "slice_ALUmode    <= operation_sel( 3 downto 0);\n"

    # Compute how slice input and AlU inputs connect
    data_mapping = {
        "A" : set(),
        "B" : set(),
        "C" : set(),
        "D" : set(),
        "A:B" : set(),
    }
    for op in CONFIG["operations"]:
        for fetch, port in enumerate(operation_sel_map[op]["fetch_mapping"]):
            data_mapping[port].add(fetch)

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

            ARCH_BODY += "slice_A(%i downto 0) <= in_%i;\n"%(CONFIG["data_width"] - 1, list(data_mapping["A"])[0])
            if CONFIG["data_width"] < 30:
                ARCH_BODY += "slice_A(29 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
        # Acting as A:B input
        else:
            if CONFIG["data_width"] > 48:
                raise ValueError("A:B can't handle data_widths larger than 48 bits")

            ARCH_BODY += "slice_A(%i downto 0) <= in_%i(in_%i'left downto 18);\n"%(CONFIG["data_width"] - 18 - 1, list(data_mapping["A"])[0], list(data_mapping["A"])[0])
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

        ARCH_BODY += "slice_B(%i downto 0) <= in_%i;\n"%(CONFIG["data_width"] - 1, list(data_mapping["B"] | data_mapping["A:B"])[0])
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

        ARCH_BODY += "slice_C(%i downto 0) <= in_%i;\n"%(CONFIG["data_width"] - 1, list(data_mapping["C"])[0])
        if CONFIG["data_width"] < 48:
            ARCH_BODY += "slice_C(47 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
    # Multiple sources
    else:
        raise NotImplementedError()

    # Handle slice D
    # Not used
    if len(data_mapping["D"]) == 0:
        ARCH_BODY += "slice_D <= (others => '1');\n"
    # Single source
    elif len(data_mapping["D"]) == 1:
        if CONFIG["data_width"] < 25:
            raise ValueError("slice_D can't handle data_widths larger than 25 bits")

        ARCH_BODY += "slice_D(%i downto 0) <= in_%i;\n"%(CONFIG["data_width"] - 1, list(data_mapping["D"])[0])
        if CONFIG["data_width"] < 25:
            ARCH_BODY += "slice_D(25 downto %i) <= (others => '0');\n"%(CONFIG["data_width"], )
    # Multiple sources
    else:
        raise NotImplementedError()


    # Connect data outputs
    ARCH_BODY += "out_0 <= slice_p(out_0'left downto 0);\n"
    if "lesser" in CONFIG["statuses"]:
        ARCH_BODY += "status_lesser <= slice_p(out_0'left);\n"
