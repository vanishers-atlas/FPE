from ..  import utils as gen_utils
from ... import utils as tc_utils
from ... import FPE_assembly as asm_utils

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
            {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"},
            {"library" : "ieee", "package" : "numeric_std"   , "parts" : "all"},
        ]

        INTERFACE["ports"] += [
            { "name" : "clock" , "type" : "std_logic", "direction" : "in" },
            { "name" : "enable", "type" : "std_logic", "direction" : "in" }
        ]

        global DELAY_INTERFACE, DELAY_NAME
        DELAY_INTERFACE, DELAY_NAME     = delay.generate_HDL(
            {},
            OUTPUT_PATH,
            "delay",
            True,
            False
        )

        # Generation Module Code
        generate_section_split()
        generate_address_sources_controls()
        generate_data_memory_controls()
        generate_program_counter_controls()
        generate_exe_compounds_controls()
        generate_path_select_controls()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_section_split():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    ARCH_BODY += "-- Instr sectioning\n"

    # Declare instr input port
    INTERFACE["ports"] += [ { "name" : "instr", "type" : "std_logic_vector(%i downto 0)"%(CONFIG["fetch_decode"]["instr_width"] - 1), "direction" : "in" } ]

    # Section off opcode for decoding
    ARCH_HEAD += "signal opcode : std_logic_vector(%i downto 0);\n"%(CONFIG["opcode_width"] - 1)
    ARCH_BODY += "opcode <= instr(%i downto %i) when enable = '1' else (others => 'U');\n\n"%(CONFIG["fetch_decode"]["instr_width"] - 1, CONFIG["fetch_decode"]["instr_width"] - CONFIG["opcode_width"] )

    # Section off addrs
    addr_start = CONFIG["fetch_decode"]["instr_width"] - CONFIG["opcode_width"]
    for addr in range(CONFIG["fetch_decode"]["encoded_addrs"]):
        INTERFACE["ports"] += [
            { "name" : "addr_%i_fetch"%(addr), "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1), "direction" : "out" },
            { "name" : "addr_%i_store"%(addr), "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1), "direction" : "out" }
        ]

        ARCH_HEAD += "signal pre_addr_%i_fetch : std_logic_vector(%i downto 0);\n"%(addr, CONFIG["addr_width"] - 1)
        ARCH_HEAD += "signal pre_addr_%i_store : std_logic_vector(%i downto 0);\n"%(addr, CONFIG["addr_width"] - 1)


        ARCH_BODY += "pre_addr_%i_fetch <= instr(%i downto %i) when enable = '1' else (others => 'U');\n\n"%(
            addr,
            addr_start - addr*CONFIG["addr_width"] - 1,
            addr_start - (addr+1)*CONFIG["addr_width"]
        )

        # Generate fetch buffer
        ARCH_BODY += "addr_%i_fetch_delay : entity work.%s(arch)\>\n"%(addr, DELAY_NAME    )

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %i,"%(CONFIG["addr_width"])
        # delay of 1, translates to delay until next raising edge
        ARCH_BODY += "delay_depth => 1"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_addr_%i_fetch,\n"%(addr)
        ARCH_BODY += "data_out => pre_addr_%i_store\n" %(addr, )
        ARCH_BODY += "\<);\n\<\n"

        ARCH_BODY += "addr_%i_fetch <= pre_addr_%i_store;\n\n"%(addr, addr)

        # Generate store buffer
        ARCH_BODY += "addr_%i_store_delay : entity work.%s(arch)\>\n"%(addr, DELAY_NAME    )

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %i,"%(CONFIG["addr_width"])
        # delay of 1 + exe_stages,
        #   1 to get past the fetch/read stage(s)
        #   exe_stages to get past the exe stage(s) of the pipeline
        ARCH_BODY += "delay_depth => %i" %(1 + CONFIG["exe_stages"])
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_addr_%i_store,\n"%(addr)
        ARCH_BODY += "data_out => addr_%i_store\n"%(addr, )
        ARCH_BODY += "\<);\n\<\n"

def generate_address_sources_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    for addr, para in CONFIG["address_sources"].items():

        ARCH_BODY += "-- %s control signals generation\n\n"%(addr)

        # Handle reset signal
        port = "%s_reset"%(addr)
        INTERFACE["ports"] += [ { "name" : port, "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

        ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(port)
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                if (    asm_utils.decode_exe_component(instr_id) == addr
                    and asm_utils.decode_mnemonic(instr_id) == "BAM_RST"
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # delay of 2,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        ARCH_BODY += "delay_depth => 2"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
        ARCH_BODY += "data_out(0) => %s\n"%(port)
        ARCH_BODY += "\<);\<\n\n"

        # Handle increment singals
        port = "%s_fetch_fixed_inc"%(addr)

        INTERFACE["ports"] += [ { "name" : port, "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

        ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
        ARCH_BODY += "else '1' when\> "
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    (
                        addr in asm_utils.decode_fetch_address_components(instr_id)
                        and "ADV" in asm_utils.decode_fetch_address_mods(instr_id)[asm_utils.decode_fetch_address_components(instr_id).index(addr)]
                    )
                    or
                    (
                        addr in asm_utils.decode_store_address_components(instr_id)
                        and "ADV" in asm_utils.decode_store_address_mods(instr_id)[asm_utils.decode_store_address_components(instr_id).index(addr)]
                    )
                )
            ]
        )
        ARCH_BODY += "\<\nelse '0';\n\<"

        ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width =>  1,"
        # delay of 1, translates to delay until next raising edge
        ARCH_BODY += "delay_depth => 1"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
        ARCH_BODY += "data_out(0) => %s\n"%(port)
        ARCH_BODY += "\<);\<\n\n"

        if any([port["name"] == "exe_data_inc"] for port in para["interface"]["ports"]):
            port = "%s_data_inc"%(addr)

            INTERFACE["ports"] += [ { "name" : port, "type" : "std_logic", "direction" : "out" } ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
            ARCH_BODY += "else '1' when\> "
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                            asm_utils.decode_exe_component(instr_id) == addr
                        and asm_utils.decode_mnemonic(instr_id) == "BAM_ADV"
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\n\<"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width =>  1,"
            # delay of 2,
            #   1 to get to the start of the fetch/read stage(s)
            #   1 the number of fetch/read stage(s)
            ARCH_BODY += "delay_depth => 2"
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

def generate_data_memory_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    # Handle get updates
    if "GET" in CONFIG["data_memories"].keys():
        ARCH_BODY += "-- Get advance generation\n\n"
        config = CONFIG["data_memories"]["GET"]

        if config["reads"] > 1:
            raise notImplenentedError()

        port = "GET_read_0_adv"

        INTERFACE["ports"] += [ { "name" : port, "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

        ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(port)

        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                        "GET" in asm_utils.decode_fetch_components(instr_id)
                    and "ADV" in asm_utils.decode_fetch_mods(instr_id)[asm_utils.decode_fetch_components(instr_id).index("GET")]
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "get_0_adv_delay : entity work.%s(arch)\>\n"%(DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # delay of 1, translates to delay until next raising edge
        ARCH_BODY += "delay_depth => 1"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
        ARCH_BODY += "data_out(0) => %s\n"%(port)
        ARCH_BODY += "\<);\n\<\n"

    for mem, para in [(mem, para) for mem, para in CONFIG["data_memories"].items() if "writes" in para and para["writes"] > 0]:
        ARCH_BODY += "-- %s write enable generation\n\n"%(mem)
        for write in range(para["writes"]):
            port = "%s_write_%i_enable"%(mem, write)

            INTERFACE["ports"] += [ { "name" : port, "type" : "std_logic", "direction" : "out" }, ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(port)

            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                    if asm_utils.decode_store_components(instr_id).count(mem) >= write + 1
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME    )

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width => 1,"
            # delay of 2 + exe_stages,
            #   1 to get to the start of the fetch/read stage(s)
            #   1 the number of fetch/read stage(s)
            #   exe_stages to get past the exe stage(s) of the pipeline
            ARCH_BODY += "delay_depth => %i" %(1 + 1 + CONFIG["exe_stages"])
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

jump_signal_mnemonic_map = {
    "jump_uncondional" : ["JMP"],
    "jump_ALU_lesser"  : ["JLT"],
}

update_signal_mnemonic_map = {
    "update_ALU_statuses" : ["CMP"],
}

def generate_program_counter_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    for jump_signal in [
            p["name"]
            for p in CONFIG["fetch_decode"]["interface"]["ports"]
            if p["name"].startswith("jump_") and p["name"] != "jump_value"
        ]:
        # Catch unhandled jump signals
        assert jump_signal in jump_signal_mnemonic_map.keys()

        ARCH_BODY += "-- %s generation\n\n"%(jump_signal)

        INTERFACE["ports"] += [ { "name" : "PC_%s"%(jump_signal), "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_PC_%s : std_logic;\n"%(jump_signal)

        ARCH_BODY += "pre_PC_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(jump_signal)
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    asm_utils.decode_mnemonic(instr_id) in jump_signal_mnemonic_map[jump_signal]
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "pre_PC_%s_delay : entity work.%s(arch)\>\n"%(jump_signal, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # delay of 2,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        ARCH_BODY += "delay_depth => 2"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_PC_%s,\n"%(jump_signal)
        ARCH_BODY += "data_out(0) => PC_%s\n"%(jump_signal)
        ARCH_BODY += "\<);\<\n\n"

    for update_signal in [
        p["name"]
        for p in CONFIG["fetch_decode"]["interface"]["ports"]
        if p["name"].startswith("update_")
    ]:
        # Catch unhandled jump signals
        assert update_signal in update_signal_mnemonic_map.keys()

        ARCH_BODY += "-- %s generation\n\n"%(update_signal)

        INTERFACE["ports"] += [ { "name" : "PC_%s"%(update_signal), "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_PC_%s : std_logic;\n"%(update_signal)

        ARCH_BODY += "pre_PC_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(update_signal)
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    asm_utils.decode_mnemonic(instr_id) in update_signal_mnemonic_map[update_signal]
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "pre_PC_%s_delay : entity work.%s(arch)\>\n"%(update_signal, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # delay of 2 + exe_stages,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        #   exe_stages to get past the exe stage(s) of the pipeline
        ARCH_BODY += "delay_depth => %i"%(1 + 1 + CONFIG["exe_stages"])
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_PC_%s,\n"%(update_signal)
        ARCH_BODY += "data_out(0) => PC_%s\n"%(update_signal)
        ARCH_BODY += "\<);\<\n\n"

def generate_exe_compounds_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    if "ALU" in CONFIG["execute_units"].keys():
        config = CONFIG["execute_units"]["ALU"]

        ARCH_BODY += "-- ALU control signals generation\n\n"

        # Handle operation select
        port = [p for p in config["interface"]["ports"] if p["name"] == "operation_sel" ][0]

        INTERFACE["ports"] += [ { "name" : "ALU_%s"%(port["name"]), "type" : port["type"], "direction" : "out" } ]
        ARCH_HEAD += "signal pre_ALU_%s : %s;\n"%(port["name"], port["type"])

        ARCH_BODY += "pre_ALU_%s <=\> "%(port["name"])
        for exe_code, value in config["interface"]["operation_sel"].items():
            ARCH_BODY += "\"%s\" when\>"%(value)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                    if asm_utils.decode_exe_component(instr_id) == "ALU" and gen_utils.get_exe_operation_code(instr_id) == exe_code
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "ALU_%s_delay : entity work.%s(arch)\>\n"%(port["name"], DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => pre_ALU_%s'length,"%(port["name"])
        # delay of 2,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        ARCH_BODY += "delay_depth => 2"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_ALU_%s,\n"%(port["name"])
        ARCH_BODY += "data_out => ALU_%s\n"%(port["name"])
        ARCH_BODY += "\<);\<\n\n"

        # Handle ALU enable select
        INTERFACE["ports"] += [ { "name" : "ALU_enable", "type" : "std_logic", "direction" : "out" } ]
        ARCH_HEAD += "signal pre_ALU_enable : std_logic;\n"

        ARCH_BODY += "pre_ALU_enable <=\> '1' when\> "
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                if asm_utils.decode_exe_component(instr_id) == "ALU"
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "ALU_enable_delay : entity work.%s(arch)\>\n"%(DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # delay of 2,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        ARCH_BODY += "delay_depth => 2"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_ALU_enable,\n"
        ARCH_BODY += "data_out(0) => ALU_enable\n"
        ARCH_BODY += "\<);\<\n\n"

def generate_path_select_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, APPEND_HASH, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    # Handle fetch_addr_connects.
    for dst, src_codes in CONFIG["fetch_addr_connects"].items():
        ARCH_BODY += "-- %s_sel generation\n\n"%(dst)

        # Handle operation select
        port_type = "std_logic_vector(%i downto 0)"%(len(list(src_codes.values())[0]) - 1)

        INTERFACE["ports"] += [ { "name" : "%s_sel"%(dst), "type" : port_type, "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s_sel : %s;\n"%(dst, port_type)

        ARCH_BODY += "pre_%s_sel <=\> "%(dst)
        for src, code in src_codes.items():
            ARCH_BODY += "\"%s\" when\>"%(code)
            raise NotImplementedErrer()
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                            None
                        )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_sel_delay : entity work.%s(arch)\>\n"%(dst, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_sel'length,"%(dst)
        # delay of 1, translates to delay until next raising edge
        ARCH_BODY += "delay_depth => 1"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_sel,\n"%(dst)
        ARCH_BODY += "data_out => %s_sel\n"%(dst)
        ARCH_BODY += "\<);\<\n\n"

    # Handle fetch_data_connects
    for dst, src_codes in CONFIG["fetch_data_connects"].items():
        print()

        ARCH_BODY += "-- %s_sel generation\n\n"%(dst)

        # Handle operation select
        port_type = "std_logic_vector(%i downto 0)"%(len(list(src_codes.values())[0]) - 1)

        INTERFACE["ports"] += [ { "name" : "%s_sel"%(dst), "type" : port_type, "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s_sel : %s;\n"%(dst, port_type)

        ARCH_BODY += "pre_%s_sel <=\> "%(dst)
        for src, code in src_codes.items():
            ARCH_BODY += "\"%s\" when\>"%(code)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                        # Check if dst is written during store of this opcode
                        dst in [p for p in asm_utils.decode_exe_inputs(instr_id)]
                        # Check if src is red during store of this opcode
                        and src in [p + "_data" for p in asm_utils.decode_fetch_paths(instr_id)]
                        # Check if dst is written by src during store of this opcode
                        and [p for p in asm_utils.decode_exe_inputs(instr_id)].index(dst) == [p + "_data" for p in asm_utils.decode_fetch_paths(instr_id)].index(src)
                    )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_sel_delay : entity work.%s(arch)\>\n"%(dst, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_sel'length,"%(dst)
        # delay of 2,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        ARCH_BODY += "delay_depth => 2"
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_sel,\n"%(dst)
        ARCH_BODY += "data_out => %s_sel\n"%(dst)
        ARCH_BODY += "\<);\<\n\n"

    # Handle store_addr_connects
    for dst, src_codes in CONFIG["store_addr_connects"].items():
        #raise NotImplementedErrer()
        ARCH_BODY += "-- %s_sel generation\n\n"%(dst)

        # Handle operation select
        port_type = "std_logic_vector(%i downto 0)"%(len(list(src_codes.values())[0]) - 1)

        INTERFACE["ports"] += [ { "name" : "%s_sel"%(dst), "type" : port_type, "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s_sel : %s;\n"%(dst, port_type)

        ARCH_BODY += "pre_%s_sel <=\> "%(dst)

        for src, code in src_codes.items():
            ARCH_BODY += "\"%s\" when\>"%(code)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                        # Check if dst is written during store of this opcode
                        dst in [p + "_addr" for p in asm_utils.decode_store_paths(instr_id)]
                        # Check if src is red during store of this opcode
                        and src in [p + "_store" for p in asm_utils.decode_store_addresses(instr_id)]
                        # Check if dst is written by src during store of this opcode
                        and [p + "_addr" for p in asm_utils.decode_store_paths(instr_id)].index(dst) == [p + "_store" for p in asm_utils.decode_store_addresses(instr_id)].index(src)
                    )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_sel_delay : entity work.%s(arch)\>\n"%(dst, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_sel'length,"%(dst)
        # delay of 2 + exe_stages,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        #   exe_stages to get past the exe stage(s) of the pipeline
        ARCH_BODY += "delay_depth => %i" %(1 + 1 + CONFIG["exe_stages"])
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_sel,\n"%(dst)
        ARCH_BODY += "data_out => %s_sel\n"%(dst)
        ARCH_BODY += "\<);\<\n\n"

    # Handle store_data_connects
    for dst, src_codes in CONFIG["store_data_connects"].items():
        ARCH_BODY += "-- %s_sel generation\n\n"%(dst)

        # Handle operation select
        port_type = "std_logic_vector(%i downto 0)"%(len(list(src_codes.values())[0]) - 1)

        INTERFACE["ports"] += [ { "name" : "%s_sel"%(dst), "type" : port_type, "direction" : "out" } ]
        ARCH_HEAD += "signal pre_%s_sel : %s;\n"%(dst, port_type)

        ARCH_BODY += "pre_%s_sel <=\> "%(dst)
        for src, code in src_codes.items():
            ARCH_BODY += "\"%s\" when\>"%(code)
            raise NotImplementedErrer()
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                        None
                    )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_sel_delay : entity work.%s(arch)\>\n"%(dst, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_sel'length,"%(dst)
        # delay of 2 + exe_stages,
        #   1 to get to the start of the fetch/read stage(s)
        #   1 the number of fetch/read stage(s)
        #   exe_stages to get past the exe stage(s) of the pipeline
        ARCH_BODY += "delay_depth => %i" %(1 + 1 + CONFIG["exe_stages"])
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_sel,\n"%(dst)
        ARCH_BODY += "data_out => %s_sel\n"%(dst)
        ARCH_BODY += "\<);\<\n\n"
