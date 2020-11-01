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

    assert(config_in["depth"] >= 1)
    config_out["depth"] = config_in["depth"]

    assert(config_in["data_width"] >= 1)
    config_out["data_width"] = config_in["data_width"]

    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:

        #import json
        #print(json.dumps(config, indent=2, sort_keys=True))

        generated_name = "ROM"

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
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]
        IMPORTS += [ {"library" : "ieee", "package" : "Numeric_Std", "parts" : "all"} ]

        # Generation Module Code
        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]
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

    IMPORTS += [ {"library" : "ieee", "package" : "std_logic_textio", "parts" : "all"} ]
    IMPORTS += [ {"library" : "STD", "package" : "textio", "parts" : "all"} ]

    # Declare internal data array
    ARCH_HEAD += "type data_array is array (%i downto 0) of std_logic_vector(%i downto 0);\n"%(CONFIG["depth"] - 1, CONFIG["data_width"] - 1)

    ARCH_HEAD += "impure function init_mem(mem_file_name : in string) return data_array is\n\>"

    ARCH_HEAD += "-- Declare file handle\n"
    ARCH_HEAD += "file mem_file : text;\n"

    ARCH_HEAD += "-- Declare variables to decode input mem file\n"
    ARCH_HEAD += "variable data_line : line;\n"
    ARCH_HEAD += "variable value     : std_logic_vector(%i downto 0);\n"%(CONFIG["data_width"] - 1.)

    ARCH_HEAD += "-- Declare variable to build output in\n"
    ARCH_HEAD += "variable temp_mem : data_array;\n\<"

    ARCH_HEAD += "begin\n\>"

    ARCH_HEAD += "-- open passed file\n"
    ARCH_HEAD += "file_open(mem_file, mem_file_name,  read_mode);\n"

    ARCH_HEAD += "if data_array'ascending then\>\n"

    ARCH_HEAD += "for i in data_array'range loop\n\>"
    ARCH_HEAD += "readline(mem_file, data_line);\n"
    ARCH_HEAD += "read(data_line, value);\n"
    ARCH_HEAD += "temp_mem(i) := value;\n"

    ARCH_HEAD += "\<end loop;\n"

    ARCH_HEAD += "\<else\>\n"

    ARCH_HEAD += "for i in data_array'reverse_range loop\n\>"
    ARCH_HEAD += "readline(mem_file, data_line);\n"
    ARCH_HEAD += "read(data_line, value);\n"
    ARCH_HEAD += "temp_mem(i) := value;\n"

    ARCH_HEAD += "\<end loop;\n"

    ARCH_HEAD += "\<end if;\n"

    ARCH_HEAD += "return temp_mem;\n"

    ARCH_HEAD += "\<end function;\n"

    ARCH_HEAD += "signal data : data_array := init_mem(mem_file);\n"

def gen_reads():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

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
        ARCH_HEAD += "signal read_%i_addr_int  : integer;\n"%(read)


        ARCH_BODY += "read_%i_addr_int <= to_integer(unsigned(read_%i_addr));\n"%(read, read)
        ARCH_BODY += "read_%i_buffer_in <= data(read_%i_addr_int) when 0 <= read_%i_addr_int and read_%i_addr_int < data'Length else (others => 'U');\n"%(read, read, read, read)

        ARCH_BODY += "read_%i_buffer : entity work.%s(arch)\>\n"%(read, reg_name)
        ARCH_BODY += "generic map (data_width => %i)\n"%(CONFIG["data_width"])
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "trigger => clock,\n"
        ARCH_BODY += "data_in  => read_%i_buffer_in,\n"%(read, )
        ARCH_BODY += "data_out => read_%i_data\n"%(read, )
        ARCH_BODY += "\<);\n\<"
