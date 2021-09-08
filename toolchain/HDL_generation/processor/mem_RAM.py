# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import dist_RAM

import math

from FPE.toolchain.HDL_generation.basic import register, mux


#####################################################################

possible_BRAMs = [
    {
        "width" : 1,
        "depth" : 16 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 2,
        "depth" : 8 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 4,
        "depth" : 4 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 9,
        "depth" : 2 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 18,
        "depth" : 1 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    }
]

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(config_in["writes"] >= 1)
    config_out["writes"] = config_in["writes"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    if "init_type" in config_in.keys():
        assert(type(config_in["init_type"]) == type(""))
        assert(config_in["init_type"] in ["NONE", "MIF"])
        config_out["init_type"] = config_in["init_type"]
    else:
        config_out["init_type"] = "NONE"

    # Check data type
    assert(type(config_in["type"]) == type(""))
    assert(config_in["type"] in ["DIST", "BLOCK"])
    if   config_in["type"] == "DIST":
        assert(config_in["depth"] >= 1)
        config_out["depth"] = config_in["depth"]
        config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

        assert(config_in["data_width"] >= 1)
        config_out["data_width"] = config_in["data_width"]
    elif config_in["type"] == "BLOCK":
        assert(config_in["depth"] >= 1)
        assert(config_in["data_width"] >= 1)
        mem_rquired = config_in["depth"] * config_in["data_width"]

        # Check all possible block_sizes and select the most mem effisanct one
        tilings = []
        for BRAM in possible_BRAMs:
            subwords = math.ceil(config_in["data_width"] / BRAM["width"])
            addr_banks = math.ceil(config_in["depth"] / BRAM["depth"])

            total_mem = subwords * addr_banks * BRAM["total_mem"]
            wasted_mem = total_mem - mem_rquired

            tilings.append(
                {
                    "subwords" : subwords,
                    "addr_banks" : addr_banks,
                    "wasted_mem" : wasted_mem,
                    "BRAM_width" : BRAM["width"],
                    "BRAM_depth" : BRAM["depth"],
                    "BRAM_primitive"  : BRAM["primitive"],
                }
            )

        # Filter for lowest wasted_mem, to use less hards
        best_wasted_mem = min([
            tiling["wasted_mem"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["wasted_mem"] == best_wasted_mem
        ]

        # Filter for lowest addr_banks, to save of muxing
        lowest_rows = min([
            tiling["addr_banks"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["addr_banks"] == lowest_rows
        ]

        # Filter for lowest subwords, to reduce signal count
        lowest_rows = min([
            tiling["subwords"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["subwords"] == lowest_rows
        ]

        # If multiple options left usage the first one
        tiling = tilings[0]

        config_out["subwords"] = tiling["subwords"]
        config_out["addr_banks"] = tiling["addr_banks"]
        config_out["BRAM_width"] = tiling["BRAM_width"]
        config_out["BRAM_depth"] = tiling["BRAM_depth"]
        config_out["BRAM_primitive"]  = tiling["BRAM_primitive"]
        config_out["BRAM_addr_width"] = tc_utils.unsigned.width(config_out["BRAM_depth"] - 1)

        config_out["data_width"] = tiling["subwords"] * tiling["BRAM_width"]

        config_out["depth"] = tiling["addr_banks"] * tiling["BRAM_depth"]
        config_out["addr_width"] = tc_utils.unsigned.width(config_out["depth"] - 1)

    else:
        raise ValueError("Unknown RAM type, %s"%(config_in["type"], ) )

    config_out["type"] = config_in["type"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "RAM"

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

        if config["type"] == "DIST":
            generated_name += "_D"
        elif config["type"] == "BLOCK":
            generated_name += "_B"
        else:
            raise ValueError("Unknown RAM type, %s"%(config_in["type"], ) )

        if config["stallable"]:
            generated_name += "_S"
        else:
            generated_name += "_N"

        if config["init_type"] != "NONE":
            generated_name += "_" + config["init_type"]

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
        INTERFACE = { "ports" : [], "generics" : [], "overwrites" : {} }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        gen_ports()

        if   CONFIG["type"] == "DIST":
            gen_wordwise_distributed_RAM()
        elif CONFIG["type"] == "BLOCK":
            gen_wordwise_block_RAM()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Handle common ports
    INTERFACE["ports"] += [
        {
            "name" : "clock",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]
    if CONFIG["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

    # Declare read ports
    for read in range(CONFIG["reads"]):
        INTERFACE["ports"] += [
            {
                "name" : "read_%i_addr"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "read_%i_data"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "out"
            }
        ]

    # Declare write ports
    for write in range(CONFIG["writes"]):
        INTERFACE["ports"] += [
            {
                "name" : "write_%i_addr"%(write, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_data"%(write, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "write_%i_enable"%(write, ),
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

def gen_wordwise_distributed_RAM():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONFIG["init_type"] == "MIF":
        INTERFACE["generics"] += [
            {
                "name" : "init_mif",
                "type" : "string"
            }
        ]


    if   CONFIG["writes"] == 1 and CONFIG["reads"] == 1:
        # Generate a basic ROM to handle be having
        ram_interface, ram_name = dist_RAM.generate_HDL(
            {
                "depth" : CONFIG["depth"],
                "ports_config" : "SIMPLE_DUAL",
                "synchronous_reads" : True,
                "enabled_reads" : CONFIG["stallable"],
                "init_type" : "MIF" if CONFIG["init_type"] == "MIF" else "NONE"
            },
            OUTPUT_PATH,
            "RAM",
            True,
            False
        )

        # Instancate RAM
        ARCH_BODY += "dist_RAM : entity work.%s(arch)\>\n"%(ram_name,)

        ARCH_BODY += "generic map (\>\n"
        if CONFIG["init_type"] == "MIF":
            ARCH_BODY += "init_mif => init_mif\n"
        ARCH_BODY += "data_width => %i\n"%(CONFIG["data_width"], )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "read_enable => not stall,\n"
        ARCH_BODY += "read_addr => read_0_addr,\n"
        ARCH_BODY += "read_data => read_0_data,\n"
        ARCH_BODY += "write_addr => write_0_addr,\n"
        ARCH_BODY += "write_data => write_0_data,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "write_enable => write_0_enable and not stall\n"
        else:
            ARCH_BODY += "write_enable => write_0_enable\n"
        ARCH_BODY += "\<);\n\<\n"

    elif CONFIG["writes"] == 1 and CONFIG["reads"] <= 3:
        # Generate a basic ROM to handle be having
        ram_interface, ram_name = dist_RAM.generate_HDL(
            {
                "depth" : CONFIG["depth"],
                "ports_config" : "QUAD",
                "synchronous_reads" : True,
                "enabled_reads" : CONFIG["stallable"],
                "init_type" : "MIF"
            },
            OUTPUT_PATH,
            "RAM",
            True,
            False
        )

        # Instancate RAM
        ARCH_BODY += "dist_RAM : entity work.%s(arch)\>\n"%(ram_name,)

        ARCH_BODY += "generic map (\>\n"
        if CONFIG["init_type"] == "MIF":
            ARCH_BODY += "init_mif => init_mif\n"
        ARCH_BODY += "data_width => %i\n"%(CONFIG["data_width"], )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "read_enable => not stall,\n"
        for read in range(0, reads):
            ARCH_BODY += "read_%i_addr => read_%i_addr,\n"%(read, read, )
            ARCH_BODY += "read_%i_data => read_%i_data,\n"%(read, read, )
        for read in range(reads, 3):
            ARCH_BODY += "write_addr => write_0_addr,\n"
            ARCH_BODY += "write_data => write_0_data,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "write_enable => write_0_enable and not stall\n"
        else:
            ARCH_BODY += "write_enable => write_0_enable\n"
        ARCH_BODY += "\<);\n\<\n"
    elif CONFIG["writes"] < 1:
        raise NotIMplementedError("Support for 2+ writes needs adding")
    else:# CONFIG["reads"] < 3
        raise NotIMplementedError("Support for 4+ reads needs adding")

def gen_wordwise_block_RAM():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    if CONFIG["init_type"] == "MIF":
        raise NotImplanentedError("BLOCK type RAMs currently lack a means to init they value")

    IMPORTS += [
        {
            "library" : "UNISIM",
            "package" : "vcomponents",
            "parts" : "all"
        }
    ]

    # Push back changes to config
    INTERFACE["overwrites"]["addr_width"] = CONFIG["addr_width"]
    INTERFACE["overwrites"]["data_width"] = CONFIG["data_width"]

    # Generate BRAM
    if CONFIG["reads"] == 1 and CONFIG["writes"] == 1:
        if CONFIG["BRAM_primitive"] == "RAMB18E1":
            BRAM_HEAD, BRAM_BODY = gen_RAMB18E1()
        else:
            raise ValueError("Unknown BRAM_primitive, %s"%(str(CONFIG["BRAM_primitive"]), ) )

        # Generate template code for all subwords in an addr_1ank
        BANK_HEAD = gen_utils.indented_string()
        BANK_BODY = gen_utils.indented_string()
        print("Greating template addr_Bank")

        # Declare bank wide addr and data signals
        BANK_HEAD += "signal BRAM_bank_BANKNAME_read_addr : std_logic_vector(%i downto 0);\n"%(CONFIG["addr_width"] - 1, )
        BANK_HEAD += "signal BRAM_bank_BANKNAME_write_addr : std_logic_vector(%i downto 0);\n"%(CONFIG["addr_width"] - 1, )
        BANK_HEAD += "signal BRAM_bank_BANKNAME_read_data : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )
        BANK_HEAD += "signal BRAM_bank_BANKNAME_write_data : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1, )
        BANK_HEAD += "signal BRAM_bank_BANKNAME_write_enable : std_logic;\n"

        # Include BRAMs each all subwords
        for subword in range(CONFIG["subwords"]):
            print("Handling subword %i of %i"%(subword, CONFIG["subwords"] - 1, ))
            BANK_HEAD += str(BRAM_HEAD).replace("SUBWORDNAME", str(subword))
            BANK_BODY += str(BRAM_BODY).replace("SUBWORDNAME", str(subword))

            # Connect up addr singals
            if CONFIG["BRAM_addr_width"] >= 14:
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_addr <= BRAM_bank_BANKNAME_read_addr(13 downto 0);\n".replace( "SUBWORDNAME", str(subword) )
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_write_addr <= BRAM_bank_BANKNAME_write_addr(13 downto 0);\n".replace( "SUBWORDNAME", str(subword) )
            else:
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_addr(13 downto %i) <= BRAM_bank_BANKNAME_read_addr(%i downto 0);\n".replace(
                    "SUBWORDNAME", str(subword)
                )%(
                    14 - CONFIG["BRAM_addr_width"],
                    CONFIG["BRAM_addr_width"]  - 1,
                )
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_addr(%i downto 0) <= (others => '0');\n\n".replace(
                    "SUBWORDNAME", str(subword)
                )%(
                    14 - CONFIG["BRAM_addr_width"] - 1,
                )
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_write_addr(13 downto %i) <= BRAM_bank_BANKNAME_write_addr(%i downto 0);\n".replace(
                    "SUBWORDNAME", str(subword)
                )%(
                    14 - CONFIG["BRAM_addr_width"],
                    CONFIG["BRAM_addr_width"]  - 1,
                )
                BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_write_addr(%i downto 0) <= (others => '0');\n\n".replace(
                    "SUBWORDNAME", str(subword)
                )%(
                    14 - CONFIG["BRAM_addr_width"] - 1,
                )

            # Connect up data singals
            BANK_BODY += "BRAM_bank_BANKNAME_read_data(%i downto %i) <= BRAM_BANKNAME_SUBWORDNAME_read_data;\n".replace(
                "SUBWORDNAME", str(subword)
            )%(
                ((subword + 1) * CONFIG["BRAM_width"]) - 1,
                (subword * CONFIG["BRAM_width"]),
            )
            BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_write_data <= BRAM_bank_BANKNAME_write_data(%i downto %i);\n\n".replace(
                "SUBWORDNAME", str(subword)
            )%(
                ((subword + 1) * CONFIG["BRAM_width"]) - 1,
                (subword * CONFIG["BRAM_width"]),
            )

            # Connect up enable singals
            BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_write_enable <= BRAM_bank_BANKNAME_write_enable;\n\n".replace( "SUBWORDNAME", str(subword) )

        # Generate addr_banks as needed
        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs" : 2
            },
            OUTPUT_PATH,
            "mux",
            True,
            False
        )

        mux_outputs = [[]]
        for bank in range(CONFIG["addr_banks"]):
            print("Handling bank %i of %i"%(bank, CONFIG["addr_banks"] - 1, ))
            ARCH_HEAD += str(BANK_HEAD).replace("BANKNAME", str(bank))
            ARCH_BODY += str(BANK_BODY).replace("BANKNAME", str(bank))

            # Connect up bank's addr ports
            ARCH_BODY += "BRAM_bank_BANKNAME_read_addr <= read_0_addr;\n".replace("BANKNAME", str(bank) )
            ARCH_BODY += "BRAM_bank_BANKNAME_write_addr <= write_0_addr;\n".replace("BANKNAME", str(bank) )

            # Connect up bank's enable ports
            if CONFIG["addr_width"] == CONFIG["BRAM_addr_width"]:
                ARCH_BODY += "BRAM_bank_BANKNAME_write_enable <= write_0_enable;\n".replace("BANKNAME", str(bank) )
            else:
                ARCH_BODY += "BRAM_bank_BANKNAME_write_enable <= write_0_enable and %s;\n".replace(
                    "BANKNAME", str(bank)
                )%(
                    " and ".join([
                        "write_0_addr(%i)"%(bit + CONFIG["BRAM_addr_width"], ) if bank & 2**bit
                        else "(not write_0_addr(%i))"%(bit + CONFIG["BRAM_addr_width"], )
                        for bit in range(CONFIG["addr_width"] - CONFIG["BRAM_addr_width"])
                    ]),
                )



            # Connect up bank's data ports
            ARCH_BODY += "BRAM_bank_BANKNAME_write_data <= write_0_data;\n".replace("BANKNAME", str(bank) )

            ARCH_HEAD += "signal banks_BANKNAME_to_BANKNAME_read_data : std_logic_vector(%i downto 0);\n".replace(
                "BANKNAME", str(bank) )%(CONFIG["data_width"] - 1, )
            ARCH_BODY += "banks_BANKNAME_to_BANKNAME_read_data <= BRAM_bank_BANKNAME_read_data;\n".replace( "BANKNAME", str(bank) )

            # Add muxs as needed
            mux_outputs[0].append((bank, bank))
            for level in range(len(mux_outputs)):
                if len(mux_outputs[level]) == 2:
                    start_bank_A, end_bank_A = mux_outputs[level][0]
                    start_bank_B, end_bank_B = mux_outputs[level][1]

                    ARCH_HEAD += "signal banks_%i_to_%i_read_data : std_logic_vector(%i downto 0);\n"%(
                        start_bank_A,
                        end_bank_B,
                        CONFIG["data_width"]  - 1,
                    )

                    ARCH_BODY += "banks_%i_to_%i_read_data_muz : entity work.%s(arch)\>\n"%(
                        start_bank_A, end_bank_B, mux_name,
                    )

                    ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

                    ARCH_BODY += "port map (\n\>"
                    ARCH_BODY += "sel(0) => read_0_addr(%i),\n"%(CONFIG["BRAM_addr_width"] + level, )
                    ARCH_BODY += "data_in_0 => banks_%i_to_%i_read_data,\n"%(start_bank_A, end_bank_A, )
                    ARCH_BODY += "data_in_1 => banks_%i_to_%i_read_data,\n"%(start_bank_B, end_bank_B, )
                    ARCH_BODY += "data_out => banks_%i_to_%i_read_data\n"%(start_bank_A, end_bank_B, )

                    ARCH_BODY += "\<);\n\<\n"

                    # Update mux mux_outputs
                    mux_outputs[level] = []
                    try:
                        mux_outputs[level + 1].append((start_bank_A, end_bank_B))
                    except IndexError:
                        mux_outputs.append([(start_bank_A, end_bank_B)])

        # Handle imbalances mux trees
        if any([ len(mux_outputs[level]) != 0 for level in range(len(mux_outputs) - 1) ]):
            for level in range(len(mux_outputs)):
                if len(mux_outputs[level]) != 0:
                    start_bank_A, end_bank_A = mux_outputs[level][0]
                    if len(mux_outputs[level]) == 1:
                        start_bank_B = end_bank_A + 1
                        end_bank_B = start_bank_B + end_bank_A - start_bank_A
                    else:
                        assert(len(mux_outputs[level]) == 2)
                        start_bank_B, end_bank_B = mux_outputs[level][1]

                    ARCH_HEAD += "signal banks_%i_to_%i_read_data : std_logic_vector(%i downto 0);\n"%(
                        start_bank_A,
                        end_bank_B,
                        CONFIG["data_width"]  - 1,
                    )

                    ARCH_BODY += "banks_%i_to_%i_read_data_muz : entity work.%s(arch)\>\n"%(
                        start_bank_A, end_bank_B, mux_name,
                    )

                    ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

                    ARCH_BODY += "port map (\n\>"
                    ARCH_BODY += "sel(0) => read_0_addr(%i),\n"%(CONFIG["BRAM_addr_width"] + level, )

                    ARCH_BODY += "data_in_0 => banks_%i_to_%i_read_data,\n"%(start_bank_A, end_bank_A, )
                    if len(mux_outputs[level]) == 1:
                        ARCH_BODY += "data_in_1 => (others => 'U'),\n"
                    else:
                        ARCH_BODY += "data_in_1 => banks_%i_to_%i_read_data,\n"%(start_bank_B, end_bank_B, )
                    ARCH_BODY += "data_out => banks_%i_to_%i_read_data\n"%(start_bank_A, end_bank_B, )

                    ARCH_BODY += "\<);\n\<\n"

                    # Update mux mux_outputs
                    mux_outputs[level] = []
                    try:
                        mux_outputs[level + 1].append((start_bank_A, end_bank_B))
                    except IndexError:
                        mux_outputs.append([(start_bank_A, end_bank_B)])

        mux_output = mux_outputs[-1][0]
        # connect data output to a registor
        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force" : False,
                "has_sync_force" : False,
                "has_enable"   : CONFIG["stallable"]
            },
            OUTPUT_PATH,
            "register",
            True,
            False
        )

        ARCH_BODY += "read_0_buffer : entity work.%s(arch)\>\n"%(reg_name, )

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        if CONFIG["stallable"]:
            ARCH_BODY += "enable => not stall,\n"
        ARCH_BODY += "data_in  => banks_0_to_%i_read_data,\n"%(mux_output[1], )
        ARCH_BODY += "data_out => read_0_data\n"
        ARCH_BODY += "\<);\n\<\n"

    else:#CONFIG["reads"] >= 3
        raise NOtImplementedError("Only 1 read and 1 write to a BRAM are supported")

def gen_RAMB18E1():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    BRAM_HEAD = gen_utils.indented_string()
    BRAM_BODY = gen_utils.indented_string()

    BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME : RAMB18E1\n\>"

    BRAM_BODY += "generic map (\>\n"

    # BRAM_BODY += "\n-- Initialization File: RAM initialization file\n"
    # BRAM_BODY += "INIT_FILE => \"NONE\",\n"

    # BRAM_BODY += "\n-- INITP_00 to INITP_07: Initial contents of parity memory array\n"
    # BRAM_BODY += "INITP_00 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_01 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_02 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_03 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_04 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_05 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_06 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_07 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"

    # BRAM_BODY += "\n-- INIT_00 to INIT_3F: Initial contents of data memory array\n"
    # BRAM_BODY += "INIT_00 => X\"000000000000000000000000000000000000000000000000FEDCBA9876543210\",\n"
    # BRAM_BODY += "INIT_01 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_02 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_03 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_04 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_05 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_06 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_07 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_08 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_09 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_10 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_11 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_12 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_13 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_14 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_15 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_16 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_17 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_18 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_19 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_20 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_21 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_22 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_23 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_24 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_25 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_26 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_27 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_28 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_29 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_31 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_30 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_32 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_33 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_34 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_35 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_36 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_37 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_38 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_39 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"

    BRAM_BODY += "\n-- INIT_A, INIT_B: Initial values on output ports\n"
    BRAM_BODY += "INIT_A => X\"00000\",\n"
    BRAM_BODY += "INIT_B => X\"00000\",\n"

    BRAM_BODY += "\n-- DOA_REG, DOB_REG: Optional output register (0 or 1)\n"
    BRAM_BODY += "DOA_REG => 0,\n"
    BRAM_BODY += "DOB_REG => 0,\n"

    BRAM_BODY += "-- RSTREG_PRIORITY_A, RSTREG_PRIORITY_B: Reset or enable priority (\"RSTREG\" or \"REGCE\")\n"
    BRAM_BODY += "RSTREG_PRIORITY_A => \"RSTREG\",\n"
    BRAM_BODY += "RSTREG_PRIORITY_B => \"RSTREG\",\n"

    BRAM_BODY += "-- SRVAL_A, SRVAL_B: Set/reset value for output\n"
    BRAM_BODY += "SRVAL_A => X\"00000\",\n"
    BRAM_BODY += "SRVAL_B => X\"00000\",\n"

    BRAM_BODY += "\n-- Address Collision Mode: \"PERFORMANCE\" or \"DELAYED_WRITE\"\n"
    BRAM_BODY += "RDADDR_COLLISION_HWCONFIG => \"PERFORMANCE\",\n"

    BRAM_BODY += "\n-- Collision check: Values (\"ALL\", \"WARNING_ONLY\", \"GENERATE_X_ONLY\" or \"NONE\")\n"
    BRAM_BODY += "SIM_COLLISION_CHECK => \"NONE\",\n"

    BRAM_BODY += "-- WriteMode: Value on output upon a write (\"WRITE_FIRST\", \"READ_FIRST\", or \"NO_CHANGE\")\n"
    BRAM_BODY += "WRITE_MODE_A => \"WRITE_FIRST\",\n"
    BRAM_BODY += "WRITE_MODE_B => \"WRITE_FIRST\",\n"

    BRAM_BODY += "\n-- RAM Mode: \"SDP\" or \"TDP\"\n"
    BRAM_BODY += "RAM_MODE => \"TDP\",\n"

    BRAM_BODY += "\n-- READ_WIDTH_A/B, WRITE_WIDTH_A/B: Read/write width per port\n"
    BRAM_BODY += "READ_WIDTH_A  => %i,\n"%(CONFIG["BRAM_width"], )
    BRAM_BODY += "READ_WIDTH_B  => 0,\n"
    BRAM_BODY += "WRITE_WIDTH_A => 0,\n"
    BRAM_BODY += "WRITE_WIDTH_B => %i,\n"%(CONFIG["BRAM_width"], )

    BRAM_BODY += "-- Simulation Device: Must be set to \"7SERIES\" for simulation behavior\n"
    BRAM_BODY += "SIM_DEVICE => \"7SERIES\"\n"

    BRAM_BODY += "\<)\n"


    BRAM_BODY += "port map (\>\n"

    BRAM_BODY += "-- Port A, Read only\n"
    BRAM_BODY += "CLKARDCLK     => clock,\n"

    BRAM_BODY += "WEA           => \"00\",\n"
    if CONFIG["stallable"]:
        BRAM_BODY += "ENARDEN 		=> not stall,\n"
    else:
        BRAM_BODY += "ENARDEN 		=> '1',\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_read_addr : std_logic_vector(13 downto 0);\n"
    BRAM_BODY += "ADDRARDADDR(13 downto 0)   => BRAM_BANKNAME_SUBWORDNAME_read_addr,\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_DO_A : std_logic_vector(15 downto 0);\n"
    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_PO_A : std_logic_vector( 1 downto 0);\n"
    BRAM_BODY += "DOADO         => BRAM_BANKNAME_SUBWORDNAME_DO_A,\n"
    BRAM_BODY += "DOPADOP	 	=> BRAM_BANKNAME_SUBWORDNAME_PO_A,\n"

    BRAM_BODY += "DIADI         => (others => '1'),\n"
    BRAM_BODY += "DIPADIP		=> (others => '1'),\n"

    BRAM_BODY += "REGCEAREGCE 	=> '0',\n"
    BRAM_BODY += "RSTRAMARSTRAM => '0',\n"
    BRAM_BODY += "RSTREGARSTREG => '0',\n"

    BRAM_BODY += "-- Port B, Write only\n"
    BRAM_BODY += "CLKBWRCLK 	=> clock,\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_write_enable : std_logic;\n"
    BRAM_BODY += "WEBWE           => (0 => BRAM_BANKNAME_SUBWORDNAME_write_enable, 1 => BRAM_BANKNAME_SUBWORDNAME_write_enable, others => '0'),\n"
    if CONFIG["stallable"]:
        BRAM_BODY += "ENBWREN 		=> not stall,\n"
    else:
        BRAM_BODY += "ENBWREN 		=> '1',\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_write_addr : std_logic_vector(13 downto 0);\n"
    BRAM_BODY += "ADDRBWRADDR(13 downto 0)   => BRAM_BANKNAME_SUBWORDNAME_write_addr,\n"

    BRAM_BODY += "DOBDO			=> open,\n"
    BRAM_BODY += "DOPBDOP       => open,\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_DI_B : std_logic_vector(15 downto 0);\n"
    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_PI_B : std_logic_vector( 1 downto 0);\n"
    BRAM_BODY += "DIBDI			=> BRAM_BANKNAME_SUBWORDNAME_DI_B,\n"
    BRAM_BODY += "DIPBDIP	    => BRAM_BANKNAME_SUBWORDNAME_PI_B,\n"

    BRAM_BODY += "REGCEB 		=> '0',\n"
    BRAM_BODY += "RSTRAMB 		=> '0',\n"
    BRAM_BODY += "RSTREGB 		=> '0'\n"


    BRAM_BODY += "\<);\n\<\n"

    # Build read data
    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_read_data : std_logic_vector(%i downto 0);\n"%( CONFIG["BRAM_width"] - 1, )
    if   CONFIG["BRAM_width"] ==  1:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_data <= BRAM_BANKNAME_SUBWORDNAME_DO_A(0 downto 0);\n\n"
    elif CONFIG["BRAM_width"] ==  2:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_data <= BRAM_BANKNAME_SUBWORDNAME_DO_A(1 downto 0);\n\n"
    elif CONFIG["BRAM_width"] ==  4:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_data <= BRAM_BANKNAME_SUBWORDNAME_DO_A(3 downto 0);\n\n"
    elif CONFIG["BRAM_width"] ==  9:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_data <= BRAM_BANKNAME_SUBWORDNAME_PO_A(0 downto 0) & BRAM_BANKNAME_SUBWORDNAME_DO_A(7 downto 0);\n\n"
    elif CONFIG["BRAM_width"] == 18:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_read_data <= BRAM_BANKNAME_SUBWORDNAME_PO_A & BRAM_BANKNAME_SUBWORDNAME_DO_A;\n\n"
    else:
        raise ValueError("Unknown BRAM_width, %i"%(BRAM_width, ) )

    # Build write data
    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_write_data : std_logic_vector(%i downto 0);\n"%( CONFIG["BRAM_width"] - 1, )
    if   CONFIG["BRAM_width"] ==  1:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(0 downto 0) <= BRAM_BANKNAME_SUBWORDNAME_write_data;\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(15 downto 1) <= (others => '-');\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B <= (others => '-');\n"
    elif CONFIG["BRAM_width"] ==  2:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(1 downto 0) <= BRAM_BANKNAME_SUBWORDNAME_write_data;\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(15 downto 2) <= (others => '-');\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B <= (others => '-');\n\n"
    elif CONFIG["BRAM_width"] ==  4:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(3 downto 0) <= BRAM_BANKNAME_SUBWORDNAME_write_data;\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(15 downto 4) <= (others => '-');\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B <= (others => '-');\n\n"
    elif CONFIG["BRAM_width"] ==  9:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(7 downto 0) <= BRAM_BANKNAME_SUBWORDNAME_write_data(7 downto 0);\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B(15 downto8 ) <= (others => '-');\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B(0 downto 0) <= BRAM_BANKNAME_SUBWORDNAME_write_data(8 downto 8);\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B(1 downto 1) <= (others => '-');\n\n"
    elif CONFIG["BRAM_width"] == 18:
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_DI_B <= BRAM_BANKNAME_SUBWORDNAME_write_data(15 downto 0);\n"
        BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_PI_B <= BRAM_BANKNAME_SUBWORDNAME_write_data(17 downto 16);\n\n"
    else:
        raise ValueError("Unknown BRAM_width, %i"%(BRAM_width, ) )

    return BRAM_HEAD, BRAM_BODY

if __name__ == "__main__":
    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 1,
            "depth"         : 16 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 2,
            "depth"         : 32 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 2,
            "depth"         : 41 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 2,
            "depth"         : 16 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 2,
            "depth"         : 8 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 4,
            "depth"         : 4 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )


    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 9,
            "depth"         : 2 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )

    generate_HDL(
        {
            "type"          : "BLOCK",
            "data_width"    : 18,
            "depth"         : 1 * 1024,
            "reads"         : 1,
            "writes"        : 1,
            "stallable"     : False,
        },
        ".",
        "test_ROM",
        generate_name=True,
        force_generation=True
    )
