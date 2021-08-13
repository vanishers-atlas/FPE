# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(type(config_in["depth"]) == type(0))
    assert(config_in["depth"] > 0)
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)
    config_out["depth"] = 2**config_out["addr_width"]

    assert(type(config_in["reads"]) == type(0))
    assert(0 < config_in["reads"] and config_in["reads"] < 4)
    config_out["reads"] = config_in["reads"]

    assert(type(config_in["synchronous"]) == type(True))
    config_out["synchronous"] = config_in["synchronous"]

    assert(type(config_in["has_enable"]) == type(True))
    config_out["has_enable"] = config_in["has_enable"]

    assert(type(config_in["init_type"]) == type(""))
    assert(config_in["init_type"] in ["MIF", "GENERICS"])
    config_out["init_type"] = config_in["init_type"]

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        generated_name = "dist_ROM"

        generated_name += "_%id"%(config["depth"])

        generated_name += "_%ir"%(config["reads"])

        if   not config["synchronous"] and not config["has_enable"]:
            generated_name += "_AA"
        elif not config["synchronous"] and config["has_enable"]:
            generated_name += "_AR"
        elif config["synchronous"] and not config["has_enable"]:
            generated_name += "_SA"
        elif config["synchronous"] and config["has_enable"]:
            generated_name += "_SE"

        if config["init_type"] != "NONE":
            generated_name += "_%s"%(config["init_type"])

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

        # Declare and Setup internal array
        gen_generate_ports()
        gen_value_array()
        gen_read_logic()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_generate_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Include extremely commom libs
    IMPORTS += [
        {
            "library" : "ieee",
            "package" : "std_logic_1164",
            "parts" : "all"
        },
        {
            "library" : "ieee",
            "package" : "Numeric_Std",
            "parts" : "all"
        }
    ]

    # Declare commom ports and generates
    INTERFACE["generics"] += [
        {
            "name" : "data_width",
            "type" : "integer"
        }
    ]
    if CONFIG["synchronous"]:
        INTERFACE["ports"] += [
            {
                "name" : "clock",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]
    if CONFIG["has_enable"]:
        INTERFACE["ports"] += [
            {
                "name" : "read_enable",
                "type" : "std_logic",
                "direction" : "in"
            }
        ]

    # Handle read ports
    for read in range(CONFIG["reads"]):
        INTERFACE["ports"] += [
            {
                "name" : "read_%i_addr"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            {
                "name" : "read_%i_data"%(read, ),
                "type" : "std_logic_vector(data_width - 1 downto 0)",
                "direction" : "out"
            }
        ]

def gen_value_array():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Declare internal array type
    ARCH_HEAD += "-- Data array type and handling\n"
    ARCH_HEAD += "type data_array is array (0 to %i) of std_logic_vector(data_width - 1 downto 0);\n\n" % (
        CONFIG["depth"] - 1,
    )

    # Handle initing the array
    if   CONFIG["init_type"] == "MIF":
        IMPORTS += [
            {
                "library": "ieee",
                "package": "std_logic_textio",
                "parts": "all"
            },
            {
                "library": "STD",
                "package": "textio",
                "parts": "all"
            }
        ]

        INTERFACE["generics"] += [
            {
                "name": "init_mif",
                "type": "string"
            }
        ]

        # split reading mem file into lots of 1024 (2^10), to prevent vivado loop limit licking in
        loop_counts = []
        acc = CONFIG["depth"]
        while acc > 0:
            loop_counts.append(acc % 1024)
            acc = int(acc / 1024)

        # Define function for loading values into data_array
        ARCH_HEAD += "impure function init_mem(mem_file_name : in string) return data_array is\n\>"

        ARCH_HEAD += "-- Declare file handle\n"
        ARCH_HEAD += "file mem_file : text;\n"

        ARCH_HEAD += "-- Declare variables to decode input mem file\n"
        ARCH_HEAD += "variable addr : integer := 0;\n"
        ARCH_HEAD += "variable data_line : line;\n"
        ARCH_HEAD += "variable word_value : std_logic_vector(data_width - 1 downto 0);\n"

        ARCH_HEAD += "-- Declare variables loop variables\n"
        for counter in range(len(loop_counts) + 1):
            ARCH_HEAD += "variable counter_%i : integer;\n" % (counter,)

        ARCH_HEAD += "variable temp_mem : data_array;\n\<"

        ARCH_HEAD += "begin\n\>"

        ARCH_HEAD += "-- open passed file\n"
        ARCH_HEAD += "file_open(mem_file, mem_file_name,  read_mode);\n"

        for power, count in enumerate(loop_counts):
            if count != 0:
                for counter in range(power):
                    ARCH_HEAD += "counter_%i  := 0;\n" % (counter + 1,)
                    ARCH_HEAD += "for counter_%i in 0 to 1023 loop\n\>" % (counter + 1,)

                ARCH_HEAD += "counter_0  := 0;\n"
                ARCH_HEAD += "for counter_0 in 0 to %i loop\n\>" % (count - 1,)
                ARCH_HEAD += "readline(mem_file, data_line);\n"
                ARCH_HEAD += "read(data_line, word_value);\n"
                ARCH_HEAD += "temp_mem(addr) := word_value;\n"
                ARCH_HEAD += "addr := addr + 1;\n"
                ARCH_HEAD += "\<end loop;\n"

                for counter in range(power):
                    ARCH_HEAD += "\<end loop;\n"

        ARCH_HEAD += "return temp_mem;\n"

        ARCH_HEAD += "\<end function;\n\n"

        # Create internal data array
        ARCH_HEAD += "signal internal_data : data_array := init_mem(init_mif);\n\n"
    elif CONFIG["init_type"] == "GENERICS":
        INTERFACE["generics"] += [
            {
                "name": "init_%i"%(addr, ),
                "type": "integer"
            }
            for addr in range(CONFIG["depth"])
        ]

        ARCH_HEAD += "signal internal_data : data_array := (\>%s\<\n);\n\n"%(
            ",\n".join([
                "std_logic_vector(to_unsigned(init_%i, data_width - 1))"%(addr, )
                for addr in range(CONFIG["depth"])
            ])
        )
    else:
        raise ValueError("Unknown init_type, %s"%(CONFIG["init_type"]))

def gen_read_logic():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_BODY += "\n-- Read behavour\n"
    for read in range(CONFIG["reads"]):
        # Setup sensativity list
        if   not CONFIG["synchronous"] and not CONFIG["has_enable"]:
            ARCH_BODY += "process (read_%i_addr)\>\n"%(read, )
        elif not CONFIG["synchronous"] and CONFIG["has_enable"]:
            ARCH_BODY += "process (read_%i_addr, read_enable)\>\n"%(read, )
        else:#CONFIG["synchronous"] and not CONFIG["has_enable"]:
            ARCH_BODY += "process (clock)\>\n"
        ARCH_BODY += "\<begin\>\n"

        # Handle clock gating for synchronous
        if CONFIG["synchronous"]:
            ARCH_BODY += "if rising_edge(clock) then\>\n"

        # Handle enable gating for enable
        if CONFIG["has_enable"]:
            ARCH_BODY += "if read_enable = '1' then\>\n"

        ARCH_BODY += "read_%i_data <= internal_data(to_integer(unsigned(read_%i_addr)));\n"%(read, read, )

        # Close enable gating if
        if CONFIG["has_enable"]:
            ARCH_BODY += "\<end if;\n"

        # Close Clock gating if
        if CONFIG["synchronous"]:
            ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end process;\n\n"
