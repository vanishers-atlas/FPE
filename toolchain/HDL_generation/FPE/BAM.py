# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))


from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register
from FPE.toolchain.HDL_generation.memory import delay

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
        IMPORTS += [ {"library" : "ieee", "package" : "numeric_std", "parts" : "all"} ]

        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generation Module Code
        generate_step_controls()
        generate_outset_adder_acc()
        generate_base_adders()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_step_controls():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "signal selected_step : std_logic_vector(%i downto 0);\n"%(CONFIG["step_width"] - 1, )
    ARCH_BODY += "selected_step <= \>"

    # Handle fixed/generic step
    if set(CONFIG["steps"])&set(["generic_forward", "generic_backward"]):
        INTERFACE["generics"] += [
            {
                "name" : "increment",
                "type" : "integer"
            }
        ]
        if "generic_forward" in CONFIG["steps"]:
            INTERFACE["ports"] += [
                {
                    "name" : "step_generic_forward",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]
            ARCH_BODY +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_forward = '1'\nelse "
        if "generic_backward" in CONFIG["steps"]:
            INTERFACE["ports"] += [
                {
                    "name" : "step_generic_backward",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]
            ARCH_BODY +="std_logic_vector(to_unsigned(increment, selected_step'length)) when step_generic_backward = '1'\nelse "

    # Handle fetched/data step
    if set(CONFIG["steps"])&set(["fetched_forward", "fetched_backward"]):
        INTERFACE["ports"] += [
            {
                "name" : "data_in" ,
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["step_width"] - 1, ),
                "direction" : "in"
            }
        ]
        if "fetched_forward" in CONFIG["steps"]:
            INTERFACE["ports"] += [
                {
                    "name" : "step_fetched_forward",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]
            ARCH_BODY += "data_in when step_fetched_forward = '1'\nelse "
        if "fetched_backward" in CONFIG["steps"]:
            INTERFACE["ports"] += [
                {
                    "name" : "step_fetched_backward",
                    "type" : "std_logic",
                    "direction" : "in"
                }
            ]
            ARCH_BODY += "data_in when step_fetched_backward = '1'\nelse "

    ARCH_BODY += "(others => '0');\<\n"


    ARCH_HEAD += "signal step_forward, step_backward : std_logic;\n"
    ARCH_BODY += "step_forward <= \>"
    if "generic_forward" in CONFIG["steps"]:
        ARCH_BODY +="'1' when step_generic_forward = '1'\nelse "
    if "fetched_forward" in CONFIG["steps"]:
        ARCH_BODY += "'1' when step_fetched_forward = '1'\nelse "
    ARCH_BODY += "'0';\n"


    ARCH_BODY += "step_backward <= \>"
    if "generic_backward" in CONFIG["steps"]:
        ARCH_BODY +="'1' when step_generic_backward = '1'\nelse "
    if "fetched_backward" in CONFIG["steps"]:
        ARCH_BODY += "'1' when step_fetched_backward = '1'\nelse "
    ARCH_BODY += "'0';\n"

def generate_outset_adder_acc():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        {
            "name" : "reset",
            "type" : "std_logic",
            "direction" : "in"
        }
    ]

    ARCH_HEAD += "signal curr_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["offset_width"] - 1, )
    ARCH_HEAD += "signal last_offset : std_logic_vector(%i downto 0);\n"%(CONFIG["offset_width"] - 1, )

    ARCH_BODY += "curr_offset <=\>std_logic_vector( to_unsigned( to_integer( unsigned( last_offset ) ) + to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_forward = '1'\nelse "
    ARCH_BODY += "std_logic_vector( to_unsigned( to_integer( unsigned( last_offset ) ) - to_integer( unsigned( selected_step ) ), curr_offset'length) ) when step_backward = '1'\nelse "
    ARCH_BODY += "last_offset;\<\n"

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 1,
            "sync_forces"   : 0,
            "has_enable"    : True
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    ARCH_BODY += "offset_acc : entity work.%s(arch)\>\n"%(reg_name)
    ARCH_BODY += "generic map (\>\n"
    ARCH_BODY += "asyn_0_value => 0,\n"
    ARCH_BODY += "data_width => %i\n"%(CONFIG["offset_width"])
    ARCH_BODY += "\<)\n"
    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "enable => step_forward or step_backward,\n"
    ARCH_BODY += "trigger => clock,\n"
    ARCH_BODY += "data_in => curr_offset,\n"
    ARCH_BODY += "data_out => last_offset,\n"
    ARCH_BODY += "asyn_reset_sel(0) => reset\n"
    ARCH_BODY += "\<);\n\<"

def generate_base_adders():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["generics"] += [
        {
            "name" : "base",
            "type" : "integer"
        }
    ]
    INTERFACE["ports"] += [
        {
            "name" : "addr_fetch",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
            "direction" : "out"
        },
        {
            "name" : "addr_store",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
            "direction" : "out"
        },
    ]

    delay_interface, delay_name = delay.generate_HDL(
        {},
        OUTPUT_PATH,
        "delay",
        True,
        False
    )

    ARCH_HEAD += "signal pre_addr_fetch, pre_addr_store : std_logic_vector(%i downto 0);"%(CONFIG["addr_width"] - 1, )

    ARCH_BODY += "pre_addr_fetch <= std_logic_vector(to_unsigned(base + to_integer(unsigned(curr_offset)), pre_addr_fetch'length));\n\n"

    # Generate fetch buffer
    ARCH_BODY += "pre_addr_fetch_dalay : entity work.%s(arch)\>\n"%(delay_name)

    ARCH_BODY += "generic map (\>"
    ARCH_BODY += "delay_width => %i,"%(CONFIG["addr_width"])
    # delay of 1, translates to delay until next raising edge
    ARCH_BODY += "delay_depth => 1"
    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => pre_addr_fetch,\n"
    ARCH_BODY += "data_out => pre_addr_store\n"
    ARCH_BODY += "\<);\n\<\n"

    ARCH_BODY += "addr_fetch <= pre_addr_store;\n\n"

    ARCH_BODY += "pre_addr_store_delay : entity work.%s(arch)\>\n"%(delay_name)

    ARCH_BODY += "generic map (\>"
    ARCH_BODY += "delay_width => %i,"%(CONFIG["addr_width"])
    # delay of 1 + exe_stages,
    #   1 to get past the fetch/read stage(s)
    #   exe_stages to get past the exe stage(s) of the pipeline
    ARCH_BODY += "delay_depth => %i" %(1 + CONFIG["exe_stages"])
    ARCH_BODY += "\<)\n"

    ARCH_BODY += "port map (\n\>"
    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => pre_addr_store,\n"
    ARCH_BODY += "data_out => addr_store\n"
    ARCH_BODY += "\<);\n\<\n"
