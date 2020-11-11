# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(config_in["writes"] >= 1)
    config_out["writes"] = config_in["writes"]

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        generated_name = "REG"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iwr"%(config["writes"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

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

        gen_registers()
        gen_reads()
        gen_writes()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_registers():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

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

    ARCH_HEAD += "-- Register signals\n"
    ARCH_BODY += "-- Registers\n"

    for reg in range(CONFIG["depth"]):
        ARCH_HEAD += "signal reg_%i_in  : std_logic_vector(%i downto 0);\n"%(reg, CONFIG["data_width"] - 1)
        ARCH_HEAD += "signal reg_%i_out : std_logic_vector(%i downto 0);\n"%(reg, CONFIG["data_width"] - 1)
        ARCH_HEAD += "signal reg_%i_enable : std_logic;\n"%(reg, )

        ARCH_BODY += "reg_%i : entity work.%s(arch)\>\n"%(reg, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"], )
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "enable  => reg_%i_enable,\n"%(reg, )
        ARCH_BODY += "data_in  => reg_%i_in,\n"%(reg, )
        ARCH_BODY += "data_out => reg_%i_out\n"%(reg, )
        ARCH_BODY += "\<);\n\<\n"

def gen_reads():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    reg_interface, reg_name = register.generate_HDL(
        {
            "async_forces"  : 0,
            "sync_forces"   : 0,
            "has_enable"    : CONFIG["stallable"]
        },
        OUTPUT_PATH,
        "register",
        True,
        False
    )

    ARCH_BODY += "-- Read buffers\n"

    for read in range(CONFIG["reads"]):
        # Declare port
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

        # Generate output buffers
        ARCH_HEAD += "signal read_%i_buffer_in : std_logic_vector(%i downto 0);\n"%(read, CONFIG["data_width"] - 1)

        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"

        if CONFIG["stallable"]:
            ARCH_BODY += "enable  => not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => read_%i_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )

        ARCH_BODY += "\<);\n\<"

        ARCH_BODY += "read_%i_buffer_in <=\>"%(read, )
        for reg in range(CONFIG["depth"]):
            ARCH_BODY += "reg_%i_out when read_%i_addr = \"%s\"\nelse "%(reg, read, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
        ARCH_BODY += "(others => 'X');\n\<"

        ARCH_BODY += "\n"

def gen_writes():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    for write in range(CONFIG["writes"]):
        # Declare port
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

    if CONFIG["writes"] == 1:
        for reg in range(CONFIG["depth"]):
            ARCH_BODY += "reg_%i_in <= write_0_data;\n"%(reg, )
            if CONFIG["stallable"]:
                ARCH_BODY += "reg_%i_enable <= write_0_enable and not stall when write_0_addr = \"%s\" else '0';\n"%(reg, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
            else:
                ARCH_BODY += "reg_%i_enable <= write_0_enable when write_0_addr = \"%s\" else '0';\n"%(reg, bin(reg)[2:].rjust(CONFIG["addr_width"], "0"))
    else:
        raise NotImplementedError()
