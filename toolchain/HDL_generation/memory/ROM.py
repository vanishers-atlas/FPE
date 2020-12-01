# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.memory import register

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    assert(config_in["reads"] >= 1)
    config_out["reads"] = config_in["reads"]

    assert(type(config_in["block_reads"]) == type([]))
    config_out["block_reads"] = []
    for block_write in config_in["block_reads"]:
        assert(block_write >= 1)
        config_out["block_reads"].append(block_write)

    if len(config_out["block_reads"]) == 1:
        config_out["block_read_sel"] = None
    else:
        config_out["block_read_sel"] =  tc_utils.unsigned.width(len(config_out["block_reads"]) - 1)

    config_out["block_size"] = max( config_out["block_reads"] )
    config_out["word_addr_width"] = tc_utils.unsigned.width(config_out["block_size"] - 1)


    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        generated_name = "ROM"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%ir"%(config["reads"], )
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
            },
        ]

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

        gen_value_array()
        gen_reads()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def gen_value_array():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Example generic
    INTERFACE["generics"] += [
        {
            "name" : "mem_file",
            "type" : "string"
        }
    ]

    IMPORTS += [
        {
            "library" : "ieee",
            "package" : "std_logic_textio",
            "parts" : "all"
        },
        {
            "library" : "STD",
            "package" : "textio",
            "parts" : "all"
        }
    ]

    # Declare internal data types
    ARCH_HEAD += "type data_array is array (%i downto 0) of std_logic_vector(%i downto 0);\n"%(
        CONFIG["depth"] / CONFIG["block_size"] - 1,
        CONFIG["block_size"] * CONFIG["data_width"] - 1,
    )

    # Define function for loading values into data_array
    ARCH_HEAD += "impure function init_mem(mem_file_name : in string) return data_array is\n\>"

    ARCH_HEAD += "-- Declare file handle\n"
    ARCH_HEAD += "file mem_file : text;\n"

    ARCH_HEAD += "-- Declare variables to decode input mem file\n"
    ARCH_HEAD += "variable data_line : line;\n"
    ARCH_HEAD += "variable word_value : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1.)

    ARCH_HEAD += "-- Declare variable to build output in\n"
    ARCH_HEAD += "variable block_value : std_logic_vector(%i downto 0);\n"%(
        CONFIG["block_size"] * CONFIG["data_width"] - 1
    )
    ARCH_HEAD += "variable temp_mem : data_array;\n\<"

    ARCH_HEAD += "begin\n\>"

    ARCH_HEAD += "-- open passed file\n"
    ARCH_HEAD += "file_open(mem_file, mem_file_name,  read_mode);\n"

    ARCH_HEAD += "for b in data_array'reverse_range loop\n\>"

    for word in range(CONFIG["block_size"]):
        ARCH_HEAD += "readline(mem_file, data_line);\n"
        ARCH_HEAD += "read(data_line, word_value);\n"
        ARCH_HEAD += "block_value(%i downto %i) := word_value;\n"%(
            (CONFIG["block_size"] - word) * CONFIG["data_width"] - 1,
            (CONFIG["block_size"] - (word + 1) ) * CONFIG["data_width"],
        )

    ARCH_HEAD += "temp_mem(b) := block_value;\n"

    ARCH_HEAD += "\<end loop;\n"

    ARCH_HEAD += "return temp_mem;\n"

    ARCH_HEAD += "\<end function;\n"

    # Create internal data array
    ARCH_HEAD += "signal data : data_array := init_mem(mem_file);\n"

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

    for read in range(CONFIG["reads"]):
        # Declare ports
        INTERFACE["ports"] += [
            {
                "name" : "read_%i_addr"%(read, ),
                "type" : "std_logic_vector(%i downto 0)"%(CONFIG["addr_width"] - 1, ),
                "direction" : "in"
            },
            *[
                {
                    "name" : "read_%i_data_word_%i"%(read, word),
                    "type" : "std_logic_vector(%i downto 0)"%(CONFIG["data_width"] - 1, ),
                    "direction" : "out"
                }
                for word in range(max(CONFIG["block_reads"]))
            ],
        ]

        if CONFIG["block_read_sel"] != None:
            INTERFACE["ports"] += [
                {
                    "name" : "read_%i_block_sel"%(read, ),
                    "type" : "std_logic_vector(%i downto 0)"%(CONFIG["block_read_sel"] - 1, ),
                    "direction" : "in"
                },
            ]


        # Handle read addr
        ARCH_HEAD += "signal read_%i_addr_block : std_logic_vector(%i downto 0);\n"%(
            read, CONFIG["addr_width"] - CONFIG["word_addr_width"] - 1
        )
        ARCH_BODY += "read_%i_addr_block <= read_%i_addr(%i downto %i);\n"%(
        read, read, CONFIG["addr_width"] - 1, CONFIG["word_addr_width"]
        )

        ARCH_HEAD += "signal read_%i_addr_word  : std_logic_vector(%i downto 0);\n"%(
            read, CONFIG["word_addr_width"] - 1
        )
        ARCH_BODY += "read_%i_addr_word  <= read_%i_addr(%i downto 0);\n"%(
            read, read, CONFIG["word_addr_width"] - 1
        )

        ARCH_HEAD += "signal read_%i_addr_block_int  : integer;\n"%(read)
        ARCH_BODY += "read_%i_addr_block_int <= to_integer(unsigned(read_%i_addr_block));\n"%(read, read)

        # Generate output buffers
        ARCH_HEAD += "signal read_%i_buffer_in, read_%i_buffer_out : std_logic_vector(%i downto 0);\n"%(
            read, read,
            CONFIG["block_size"] * CONFIG["data_width"] - 1
        )

        # Map data into buffer
        ARCH_BODY += "\n-- Read map proccess\n"
        if CONFIG["block_read_sel"] == None:
            ARCH_BODY += "process (clock, read_%i_addr)\>\n"%(read, )
        else:
            ARCH_BODY += "process (clock, read_%i_addr, read_%i_block_sel)\>\n"%(read, read,)
        ARCH_BODY += "\<begin\>\n"

        if CONFIG["stallable"]:
            ARCH_BODY += "if stall /= '1' then\>\n"

        ARCH_BODY += "-- Blank out buffer input\n"
        ARCH_BODY += "read_%i_buffer_in <= (others => 'U');\n\n"%(
            read,
        )

        ARCH_BODY += "-- Check that block addr is valid\n"
        ARCH_BODY += "if 0 <= read_%i_addr_block_int and read_%i_addr_block_int < data'Length then\>\n"%(
            read,
            read,
        )

        if CONFIG["block_read_sel"] == None:
            ARCH_BODY += "read_%i_buffer_in <= data(read_%i_addr_block_int);\n"%(
                read, read,
            )
        else:
            ARCH_BODY += "-- handle different block sizes\n"
            for block_read_sel_val, read_size in enumerate(CONFIG["block_reads"]):
                ARCH_BODY += "if read_%i_block_sel = \"%s\" then\>\n"%(
                    read,
                    tc_utils.unsigned.encode(block_read_sel_val, CONFIG["block_read_sel"]),
                )
                subblock_addr_width = tc_utils.unsigned.width(int(CONFIG["block_size"]/read_size) - 1)

                if int(CONFIG["block_size"]/read_size) == 1:
                    ARCH_BODY += "read_%i_buffer_in <= data(read_%i_addr_block_int);\n"%(
                        read, read,
                    )
                else:
                    ARCH_BODY += "-- handle different subblocks\n"
                    for subblock in range(int(CONFIG["block_size"]/read_size)):
                        ARCH_BODY += "if read_%i_addr_word(%i downto %i) = \"%s\" then\>\n"%(
                            read,
                            CONFIG["word_addr_width"] - 1,
                            CONFIG["word_addr_width"] - subblock_addr_width,
                            tc_utils.unsigned.encode(subblock, subblock_addr_width),
                        )

                        ARCH_BODY += "read_%i_buffer_in(%i downto %i) <= data(read_%i_addr_block_int)(%i downto %i);\n"%(
                            read,
                            CONFIG["block_size"] * CONFIG["data_width"] - 1,
                            (CONFIG["block_size"] - read_size) * CONFIG["data_width"],
                            read,
                            (CONFIG["block_size"] - subblock*read_size) * CONFIG["data_width"] - 1,
                            (CONFIG["block_size"] - (subblock + 1)*read_size) * CONFIG["data_width"],
                        )
                        ARCH_BODY += "\<els"
                    ARCH_BODY.drop_last_X(3)
                    ARCH_BODY += "end if;\n"
                ARCH_BODY += "\<els"
            ARCH_BODY.drop_last_X(3)
            ARCH_BODY += "end if;\n"

        ARCH_BODY += "\<end if;\n"

        if CONFIG["stallable"]:
            ARCH_BODY += "\<end if;\n"

        ARCH_BODY += "\<end process;\n"

        # Instance read data buffer
        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)

        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["block_size"] * CONFIG["data_width"])

        ARCH_BODY += "port map (\n\>"

        if CONFIG["stallable"]:
            ARCH_BODY += "enable  => not stall,\n"

        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => read_%i_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_buffer_out\n"%(read, )

        ARCH_BODY += "\<);\n\<"

        # Map data out of buffer
        for word in range(max(CONFIG["block_reads"])):
            ARCH_BODY += "read_%i_data_word_%i <= read_%i_buffer_out(%i downto %i);\n"%(
                read, word, read,
                (CONFIG["block_size"] - word) * CONFIG["data_width"] - 1,
                (CONFIG["block_size"] - (word + 1)) * CONFIG["data_width"],
            )
