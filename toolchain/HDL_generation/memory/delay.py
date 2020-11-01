# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    assert(config_in["width"] >= 1)
    config_out["width"] = config_in["width"]

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        generated_name = "delay"

        generated_name += "_%iw"%(config["width"])

        generated_name += "_%id"%(config["depth"])

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
                "parts" : "all"
            }
        ]

        # Generation Module Code
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            },
            {
                "name" : "data_in",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1,),
                "direction" : "in"
            },
            {
                "name" : "data_out",
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1,),
                "direction" : "out"
            }

        ]

        # Delay of depth 0, is a wire
        if CONFIG["depth"] == 0:
            ARCH_BODY += "data_out <= data_in;\n"
        # Delay of depth 1, is a registor
        elif CONFIG["depth"] == 1:

            from FPE.toolchain.HDL_generation.memory import register

            reg_interface, reg_name = register.generate_HDL(
                {
                    "async_forces"  : 0,
                    "sync_forces"   : 0,
                    "has_enable"    : False
                },
                OUTPUT_PATH,
                "register",
                True,
                False
            )

            ARCH_BODY += "delay_reg : entity work.%s(arch)\>\n"%(reg_name)
            ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["width"])
            ARCH_BODY += "port map (\n\>"
            ARCH_BODY += "trigger => clock,\n"
            ARCH_BODY += "data_in  => data_in,\n"
            ARCH_BODY += "data_out => data_out\n"
            ARCH_BODY += "\<);\n\<"
        # Delay of depth 2+. is a shift reg
        else:
            ARCH_HEAD += "type data_array is array(%i downto 0) of std_logic_vector(%i downto 0);\n"%(CONFIG["depth"] - 1, CONFIG["width"] - 1)
            ARCH_HEAD += "signal data : data_array;\n"

            ARCH_BODY += "process (clock)\>\n"
            ARCH_BODY += "\<begin\>\n"

            ARCH_BODY += "if rising_edge(clock) then\>\n"
            ARCH_BODY += "data(data'left - 1 downto 0) <= data(data'left downto 1);\n"
            ARCH_BODY += "data(data'left) <= data_in;\n"

            ARCH_BODY += "\<end if;\n"

            ARCH_BODY += "\<end process;\n"

            ARCH_BODY += "data_out <= data(0);\n"

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME
