# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain import FPE_assembly as asm_utils

from FPE.toolchain.HDL_generation.memory import delay

import itertools as it

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
            }
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
        generate_address_source_contols()
        generate_data_memory_controls()
        generate_program_counter_controls()
        generate_exe_compounds_controls()
        generate_path_select_controls()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_section_split():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    ARCH_BODY += "-- Instr sectioning\n"

    # Declare instr input port
    INTERFACE["ports"] += [
        {
            "name" : "instr",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["instruction_decoder"]["instr_width"] - 1),
            "direction" : "in"
        }
    ]

    # Section off opcode for decoding
    ARCH_HEAD += "signal opcode : std_logic_vector(%i downto 0);\n"%(CONFIG["instruction_decoder"]["opcode_width"] - 1)
    ARCH_BODY += "opcode <= instr(%i downto %i) when enable = '1' else (others => 'U');\n\n"%(
        CONFIG["instruction_decoder"]["instr_width"] - 1,
        CONFIG["instruction_decoder"]["instr_width"] - CONFIG["instruction_decoder"]["opcode_width"],
    )

    # Section off addrs
    addr_start = CONFIG["instruction_decoder"]["instr_width"] - CONFIG["instruction_decoder"]["opcode_width"]
    for addr, width in sorted(CONFIG["instruction_decoder"]["addr_widths"].items(), key=lambda kv: kv[0]):
        INTERFACE["ports"] += [
            {
                "name" : "%s_fetch"%(addr),
                "type" : "std_logic_vector(%i downto 0)"%(width - 1),
                "direction" : "out"
            },
            {
                "name" : "%s_store"%(addr),
                "type" : "std_logic_vector(%i downto 0)"%(width - 1),
                "direction" : "out"
            }
        ]

        ARCH_HEAD += "signal pre_%s_fetch : std_logic_vector(%i downto 0);\n"%(addr, width - 1)
        ARCH_HEAD += "signal pre_%s_store : std_logic_vector(%i downto 0);\n"%(addr, width - 1)


        ARCH_BODY += "pre_%s_fetch <= instr(%i downto %i) when enable = '1' else (others => 'U');\n\n"%(
            addr,
            addr_start - 1,
            addr_start - width
        )
        addr_start -= width


        # Generate fetch buffer
        ARCH_BODY += "%s_fetch_delay : entity work.%s(arch)\>\n"%(addr, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %i,"%(width)
        # Delay until first fetch stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s)
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_fetch,\n"%(addr)
        ARCH_BODY += "data_out => pre_%s_store\n" %(addr)
        ARCH_BODY += "\<);\n\<\n"

        ARCH_BODY += "%s_fetch <= pre_%s_store;\n\n"%(addr, addr)

        # Generate store buffer
        ARCH_BODY += "%s_store_delay : entity work.%s(arch)\>\n"%(addr, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %i,"%(width)
        # Delay for first fetch stage until first store stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get past the fetch stages
                    CONFIG["exe_stages"],   # to get past the exe   stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_store,\n"%(addr)
        ARCH_BODY += "data_out => %s_store\n"%(addr, )
        ARCH_BODY += "\<);\n\<\n"

def generate_address_source_contols():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
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
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    asm_utils.instr_exe_com(instr_id) == addr
                    and asm_utils.instr_mnemonic(instr_id) == "RESET"
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # Delay until first ese stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
        ARCH_BODY += "data_out(0) => %s\n"%(port)
        ARCH_BODY += "\<);\<\n\n"

        # Handle increment signals
        if any(
            [
                port["name"] == "step_generic_forward"
                for port in para["interface"]["ports"]
            ]
        ):
            port = "%s_step_generic_forward"%(addr)

            INTERFACE["ports"] += [
                {
                    "name" : port,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
            ARCH_BODY += "else '1' when\> "

            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                        (
                            addr in asm_utils.instr_fetch_addr_coms(instr_id)
                            and "FORWARD" in asm_utils.instr_fetch_addr_mods(instr_id)[asm_utils.instr_fetch_addr_coms(instr_id).index(addr)]
                        )
                        or
                        (
                            addr in asm_utils.instr_store_addr_coms(instr_id)
                            and "FORWARD" in asm_utils.instr_store_addr_mods(instr_id)[asm_utils.instr_store_addr_coms(instr_id).index(addr)]
                        )
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\n\<"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width =>  1,"
            # Delay until first fetch stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                    ]
                )
            )
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

        if any(
            [
                port["name"] == "step_generic_backward"
                for port in para["interface"]["ports"]
            ]
        ):
            port = "%s_step_generic_backward"%(addr)

            INTERFACE["ports"] += [
                {
                    "name" : port,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
            ARCH_BODY += "else '1' when\> "
            raise NotImplementedError()
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                        (
                            addr in asm_utils.instr_fetch_addr_coms(instr_id)
                            and "FORWARD" in asm_utils.instr_fetch_addr_mods(instr_id)[asm_utils.instr_fetch_addr_coms(instr_id).index(addr)]
                        )
                        or
                        (
                            addr in asm_utils.instr_store_addr_coms(instr_id)
                            and "FORWARD" in asm_utils.instr_store_addr_mods(instr_id)[asm_utils.instr_store_addr_coms(instr_id).index(addr)]
                        )
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\n\<"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width =>  1,"
            # Delay until first fetch stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                    ]
                )
            )
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

        if any(
            [
                port["name"] == "step_fetched_forward"
                for port in para["interface"]["ports"]
            ]
        ):
            port = "%s_step_fetched_forward"%(addr)

            INTERFACE["ports"] += [
                {
                    "name" : port,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
            ARCH_BODY += "else '1' when\> "

            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                        (
                            asm_utils.instr_mnemonic(instr_id) == "SEEK"
                            and asm_utils.instr_exe_com(instr_id) == addr
                            and "FORWARD" in asm_utils.instr_mods(instr_id)
                        )
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\n\<"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width =>  1,"
            # Delay until first ese stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                        1,                      # to get past the fetch stages
                    ]
                )
            )
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

        # Handle increment singals
        if any(
            [
                port["name"] == "step_fetched_backward"
                for port in para["interface"]["ports"]
            ]
        ):
            port = "%s_step_fetched_backward"%(addr)

            INTERFACE["ports"] += [
                {
                    "name" : port,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\n"%(port)
            ARCH_BODY += "else '1' when\> "
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                        (
                            asm_utils.instr_mnemonic(instr_id) == "SEEK"
                            and asm_utils.instr_exe_com(instr_id) == addr
                            and "BACKWARD" in asm_utils.instr_mods(instr_id)
                        )
                    )
                ]
            )
            ARCH_BODY += "\<\nelse '0';\n\<"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width =>  1,"
            # Delay until first ese stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                        1,                      # to get past the fetch stages
                    ]
                )
            )
            ARCH_BODY += "\<)\n"

            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "clock => clock,\n"
            ARCH_BODY += "data_in (0) => pre_%s,\n"%(port)
            ARCH_BODY += "data_out(0) => %s\n"%(port)
            ARCH_BODY += "\<);\<\n\n"

def generate_data_memory_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    # Handle get updates
    if "GET" in CONFIG["data_memories"].keys():
        ARCH_BODY += "-- Get advance generation\n\n"
        config = CONFIG["data_memories"]["GET"]

        for port_index in range(config["reads"]):

            port = "GET_read_%i_adv"%(port_index)

            INTERFACE["ports"] += [
                {
                    "name" : port,
                    "type" : "std_logic",
                    "direction" : "out"
                }
            ]
            ARCH_HEAD += "signal pre_%s : std_logic;\n"%(port)

            ARCH_BODY += "pre_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(port)

            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if (
                            "GET" in asm_utils.instr_fetch_access_coms(instr_id)
                        and "ADV" in asm_utils.instr_fetch_access_mods(instr_id)[asm_utils.instr_fetch_access_coms(instr_id).index("GET")]
                    )
                ]
            )
            ARCH_BODY += "\n\<else '0';\<\n\n"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME)

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width => 1,"
            # Delay until first fetch stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                    ]
                )
            )
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
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                    if asm_utils.instr_store_access_coms(instr_id).count(mem) >= write + 1
                ]
            )
            ARCH_BODY += "\<\nelse '0';\<\n\n"

            ARCH_BODY += "%s_delay : entity work.%s(arch)\>\n"%(port, DELAY_NAME    )

            ARCH_BODY += "generic map (\>"
            ARCH_BODY += "delay_width => 1,"
            # Delay until first store stage
            ARCH_BODY += "delay_depth => %i"%(
                sum(
                    [
                        1,                      # to get to the start of the fetch/read stage(s).
                        1,                      # to get past the fetch stages
                        CONFIG["exe_stages"],   # to get past the exe   stages
                    ]
                )
            )
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
    "update_ALU_statuses" : ["CMP", "SIGN"],
}

def generate_program_counter_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    for jump_signal in [
            p["name"]
            for p in CONFIG["program_fetch"]["program_counter_interface"]["ports"]
            if p["name"].startswith("jump_") and p["name"] != "jump_value"
        ]:
        # Catch unhandled jump signals
        assert jump_signal in jump_signal_mnemonic_map.keys()

        ARCH_BODY += "-- %s generation\n\n"%(jump_signal)

        INTERFACE["ports"] += [
            {
                "name" : "PC_%s"%(jump_signal),
                "type" : "std_logic",
                "direction" : "out"
            }
        ]
        ARCH_HEAD += "signal pre_PC_%s : std_logic;\n"%(jump_signal)

        ARCH_BODY += "pre_PC_%s <=\> 'U' when enable /= '1'\nelse '1' when\> "%(jump_signal)
        ARCH_BODY += "\nor ".join(
            [
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    asm_utils.instr_mnemonic(instr_id) in jump_signal_mnemonic_map[jump_signal]
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "pre_PC_%s_delay : entity work.%s(arch)\>\n"%(jump_signal, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # Delay until first ese stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_PC_%s,\n"%(jump_signal)
        ARCH_BODY += "data_out(0) => PC_%s\n"%(jump_signal)
        ARCH_BODY += "\<);\<\n\n"

    for update_signal in [
        p["name"]
        for p in CONFIG["program_fetch"]["program_counter_interface"]["ports"]
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
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                for instr_id, instr_val in CONFIG["instr_set"].items()
                if (
                    asm_utils.instr_mnemonic(instr_id) in update_signal_mnemonic_map[update_signal]
                )
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "pre_PC_%s_delay : entity work.%s(arch)\>\n"%(update_signal, DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # Delay until first store stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                    CONFIG["exe_stages"],   # to get past the exe   stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_PC_%s,\n"%(update_signal)
        ARCH_BODY += "data_out(0) => PC_%s\n"%(update_signal)
        ARCH_BODY += "\<);\<\n\n"

def generate_exe_compounds_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
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
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                    if asm_utils.instr_exe_com(instr_id) == "ALU" and gen_utils.get_exe_operation_code(instr_id) == exe_code
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "ALU_%s_delay : entity work.%s(arch)\>\n"%(port["name"], DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => pre_ALU_%s'length,"%(port["name"])
        # Delay until first ese stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                ]
            )
        )
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
                "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"])) for instr_id, instr_val in CONFIG["instr_set"].items()
                if asm_utils.instr_exe_com(instr_id) == "ALU"
            ]
        )
        ARCH_BODY += "\n\<else '0';\<\n\n"

        ARCH_BODY += "ALU_enable_delay : entity work.%s(arch)\>\n"%(DELAY_NAME)

        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => 1,"
        # Delay until first ese stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in (0) => pre_ALU_enable,\n"
        ARCH_BODY += "data_out(0) => ALU_enable\n"
        ARCH_BODY += "\<);\<\n\n"

def generate_path_select_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME

    # Handle fetch_addr_connects.
    for dst_id, src_mux in CONFIG["fetch_addr_connects"].items():
        dst_sig = "_".join(dst_id.split("#"))

        ARCH_BODY += "-- %s_mux_sel generation\n\n"%(dst_sig)

        # Handle operation select
        select_width = len(list(src_mux.values())[0])
        select_port_type = "std_logic_vector(%i downto 0)"%(select_width - 1)

        INTERFACE["ports"] += [
            {
                "name" : "%s_mux_sel"%(dst_sig),
                "type" : select_port_type,
                "direction" : "out"
            }
        ]
        ARCH_HEAD += "signal pre_%s_mux_sel : %s;\n"%(dst_sig, select_port_type)

        ARCH_BODY += "pre_%s_mux_sel <=\> "%(dst_sig)
        for src_id, select_code in src_mux.items():
            src_sig = "_".join(src_id.split("#"))

            ARCH_BODY += "\"%s\" when\>"%(select_code)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                            # Check if src is red during fetch of this opcode
                            src_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_fetch_addr_coms(instr_id),
                                    asm_utils.instr_fetch_addr_srcs(instr_id)
                                )
                            ]

                            # Check if dst is written during fetch of this opcode
                            and dst_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_fetch_access_coms(instr_id),
                                    asm_utils.instr_fetch_addr_dsts(instr_id)
                                )
                            ]

                            # Check if dst is written by src during fetch of this opcode
                            and (
                                [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_fetch_addr_coms(instr_id),
                                        asm_utils.instr_fetch_addr_srcs(instr_id)
                                    )
                                ].index(src_sig)
                                == [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_fetch_access_coms(instr_id),
                                        asm_utils.instr_fetch_addr_dsts(instr_id)
                                    )
                                ].index(dst_sig)
                            )
                        )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_mux_sel_delay : entity work.%s(arch)\>\n"%(dst_sig, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_mux_sel'length,"%(dst_sig)
        # Delay until first fetch stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_mux_sel,\n"%(dst_sig)
        ARCH_BODY += "data_out => %s_mux_sel\n"%(dst_sig)
        ARCH_BODY += "\<);\<\n\n"


    # Handle fetch_data_connects
    for dst_id, src_mux in CONFIG["fetch_data_connects"].items():
        dst_sig = "_".join(dst_id.split("#"))

        ARCH_BODY += "-- %s_mux_sel generation\n\n"%(dst_sig)

        # Handle operation select
        select_width = len(list(src_mux.values())[0])
        select_port_type = "std_logic_vector(%i downto 0)"%(select_width - 1)

        INTERFACE["ports"] += [
            {
                "name" : "%s_mux_sel"%(dst_sig),
                "type" : select_port_type,
                "direction" : "out"
            }
        ]
        ARCH_HEAD += "signal pre_%s_mux_sel : %s;\n"%(dst_sig, select_port_type)

        ARCH_BODY += "pre_%s_mux_sel <=\> "%(dst_sig)
        for src_id, select_code in src_mux.items():
            src_sig = "_".join(src_id.split("#"))

            ARCH_BODY += "\"%s\" when\>"%(select_code)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                            # Check if src is red during fetch of this opcode
                            src_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_fetch_access_coms(instr_id),
                                    asm_utils.instr_fetch_access_srcs(instr_id)
                                )
                            ]

                            # Check if dst is written during fetch of this opcode
                            and dst_sig in [
                                "_".join(p)
                                for p in zip(
                                    it.repeat(asm_utils.instr_exe_com(instr_id)),
                                    asm_utils.instr_fetch_access_dsts(instr_id)
                                )
                            ]

                            # Check if dst is written by src during fetch of this opcode
                            and (
                                [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_fetch_access_coms(instr_id),
                                        asm_utils.instr_fetch_access_srcs(instr_id)
                                    )
                                ].index(src_sig)
                                ==  [
                                    "_".join(p)
                                    for p in zip(
                                        it.repeat(asm_utils.instr_exe_com(instr_id)),
                                        asm_utils.instr_fetch_access_dsts(instr_id)
                                    )
                                ].index(dst_sig)
                            )
                        )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_mux_sel_delay : entity work.%s(arch)\>\n"%(dst_sig, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_mux_sel'length,"%(dst_sig)
        # Delay until first ese stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                      # to get to the start of the fetch/read stage(s).
                    1,                      # to get past the fetch stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_mux_sel,\n"%(dst_sig)
        ARCH_BODY += "data_out => %s_mux_sel\n"%(dst_sig)
        ARCH_BODY += "\<);\<\n\n"


    # Handle store_addr_connects
    for dst_id, src_mux in CONFIG["store_addr_connects"].items():
        dst_sig = "_".join(dst_id.split("#"))

        ARCH_BODY += "-- %s_mux_sel generation\n\n"%(dst_sig)

        # Handle operation select
        select_width = len(list(src_mux.values())[0])
        select_port_type = "std_logic_vector(%i downto 0)"%(select_width - 1)

        INTERFACE["ports"] += [
            {
                "name" : "%s_mux_sel"%(dst_sig),
                "type" : select_port_type,
                "direction" : "out"
            }
        ]
        ARCH_HEAD += "signal pre_%s_mux_sel : %s;\n"%(dst_sig, select_port_type)

        ARCH_BODY += "pre_%s_mux_sel <=\> "%(dst_sig)
        for src_id, select_code in src_mux.items():
            src_sig = "_".join(src_id.split("#"))

            ARCH_BODY += "\"%s\" when\>"%(select_code)
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                            # Check if src is red during store of this opcode
                            src_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_store_addr_coms(instr_id),
                                    asm_utils.instr_store_addr_srcs(instr_id)
                                )
                            ]

                            # Check if dst is written during store of this opcode
                            and dst_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_store_access_coms(instr_id),
                                    asm_utils.instr_store_addr_dsts(instr_id)
                                )
                            ]

                            # Check if dst is written by src during store of this opcode
                            and (
                                [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_store_addr_coms(instr_id),
                                        asm_utils.instr_store_addr_srcs(instr_id)
                                    )
                                ].index(src_sig)
                                ==  [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_store_access_coms(instr_id),
                                        asm_utils.instr_store_addr_dsts(instr_id)
                                    )
                                ].index(dst_sig)
                            )
                        )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_mux_sel_delay : entity work.%s(arch)\>\n"%(dst_sig, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_mux_sel'length,"%(dst_sig)
        # Delay until store stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                          # to get to the start of the fetch/read stage(s).
                    1,                          # to get past the fetch stages
                    CONFIG["exe_stages"],       # to get past the all but last exe stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_mux_sel,\n"%(dst_sig)
        ARCH_BODY += "data_out => %s_mux_sel\n"%(dst_sig)
        ARCH_BODY += "\<);\<\n\n"


    # Handle store_data_connects
    for dst, src_codes in CONFIG["store_data_connects"].items():
        dst_sig = "_".join(dst_id.split("#"))

        ARCH_BODY += "-- %s_mux_sel generation\n\n"%(dst_sig)

        # Handle operation select
        select_width = len(list(src_mux.values())[0])
        select_port_type = "std_logic_vector(%i downto 0)"%(select_width - 1)

        INTERFACE["ports"] += [
            {
                "name" : "%s_mux_sel"%(dst_sig),
                "type" : select_port_type,
                "direction" : "out"
            }
        ]
        ARCH_HEAD += "signal pre_%s_mux_sel : %s;\n"%(dst_sig, select_port_type)

        ARCH_BODY += "pre_%s_mux_sel <=\> "%(dst_sig)
        for src_id, select_code in src_mux.items():
            src_sig = "_".join(src_id.split("#"))

            ARCH_BODY += "\"%s\" when\>"%(select_code)
            raise NotImplementedError()
            ARCH_BODY += "\nor ".join(
                [
                    "opcode = \"%s\""%(tc_utils.unsigned.encode(instr_val, CONFIG["instruction_decoder"]["opcode_width"]))
                    for instr_id, instr_val in CONFIG["instr_set"].items()
                    if  (
                            # Check if src is red during store of this opcode
                            src_sig in [
                                "_".join(p)
                                for p in zip(
                                    asm_utils.instr_fetch_access_coms(instr_id),
                                    asm_utils.instr_fetch_access_srcs(instr_id)
                                )
                            ]

                            # Check if dst is written during store of this opcode
                            and dst_sig in [
                                "_".join(p)
                                for p in zip(
                                    it.repeat(asm_utils.instr_exe_com(instr_id)),
                                    asm_utils.instr_fetch_access_dsts(instr_id)
                                )
                            ]

                            # Check if dst is written by src during store of this opcode
                            and (
                                [
                                    "_".join(p)
                                    for p in zip(
                                        asm_utils.instr_fetch_access_coms(instr_id),
                                        asm_utils.instr_fetch_access_srcs(instr_id)
                                    )
                                ].index(src_sig)
                                ==  [
                                    "_".join(p)
                                    for p in zip(
                                        it.repeat(asm_utils.instr_exe_com(instr_id)),
                                        asm_utils.instr_fetch_access_dsts(instr_id)
                                    )
                                ].index(dst_sig)
                            )
                        )
                ]
            )
            ARCH_BODY += "\n\<else "
        ARCH_BODY += "(others => 'U');\<\n\n"

        ARCH_BODY += "%s_mux_sel_delay : entity work.%s(arch)\>\n"%(dst_sig, DELAY_NAME)
        ARCH_BODY += "generic map (\>"
        ARCH_BODY += "delay_width => %s_mux_sel'length,"%(dst_sig)
        # Delay until last exe stage
        ARCH_BODY += "delay_depth => %i"%(
            sum(
                [
                    1,                          # to get to the start of the fetch/read stage(s).
                    1,                          # to get past the fetch stages
                    CONFIG["exe_stages"] - 1,   # to get past the all but last exe stages
                ]
            )
        )
        ARCH_BODY += "\<)\n"

        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "data_in  => pre_%s_mux_sel,\n"%(dst_sig)
        ARCH_BODY += "data_out => %s_mux_sel\n"%(dst_sig)
        ARCH_BODY += "\<);\<\n\n"
