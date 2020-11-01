# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

import math


def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = "FIFO_%iw_%id"%(config["width"], config["depth"])

        return generated_name
    else:
        return module_name

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    #import json
    #print(json.dumps(config_in, indent=2, sort_keys=True))

    raise NotImplementedError()

    #print(json.dumps(config_out, indent=2, sort_keys=True))
    #exit()

    return config_out

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = ""

        raise NotImplementedError()

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
        INTERFACE = {
            "ports" : [],
            "generics" : []
        }

        # Include extremely commom libs
        IMPORTS += [
            {
                "library" : "ieee",
                "package" : "std_logic_1164",
                "parts" : "all"
            }
        ]

        # Generation Module Code
        generate_FIFOs()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_FIFOs():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    # Include normal ports
    INTERFACE["ports"] += [
        {   "name" : "clock",   "type" : "std_logic",   "direction" : "in" },
        {   "name" : "clear",   "type" : "std_logic",   "direction" : "in" },
        {   "name" : "data_in",     "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1, ),    "direction" : "in"  },
        {   "name" : "data_out",    "type" : "std_logic_vector(%i downto 0)"%(CONFIG["width"] - 1, ),    "direction" : "out"     },
        {   "name" : "data_write",  "type" : "std_logic",   "direction" : "in"  },
        {   "name" : "data_read",   "type" : "std_logic",   "direction" : "in"  },
        {   "name" : "data_write_ready",   "type" : "std_logic",   "direction" : "out"     },
        {   "name" : "data_read_ready",    "type" : "std_logic",   "direction" : "out"     },
        {   "name" : "full",    "type" : "std_logic",   "direction" : "out"     },
        {   "name" : "empty",   "type" : "std_logic",   "direction" : "out"     },
    ]

    # Decompose depth into sum of FIFO_generator depths
    assert(isinstance(CONFIG["depth"], int) and CONFIG["depth"] > 0)
    fifo_gens = []
    rem_depth = CONFIG["depth"]
    GEN_MAX = 2 ** 17
    GEN_MIN = 2 ** 4
    while rem_depth > 0:
        if rem_depth > GEN_MAX:
            rem_depth -= GEN_MAX
            fifo_gens.append(
                {
                    "depth" : GEN_MAX,
                    "full_level"  : None,
                    "empty_level" : None,
                }
            )
        elif rem_depth >= GEN_MIN :
            depth = 2 ** math.floor(math.log(rem_depth,2))
            rem_depth -= depth
            fifo_gens.append(
                {
                    "depth" : depth,
                    "full_level"  : None,
                    "empty_level" : None,
                }
            )
        else: # rem_depth < GEN_MIN
            fifo_gens.append(
                {
                    "depth" : GEN_MIN,
                    "full_level"  : None,
                    "empty_level" : None,
                }
            )
            rem_depth -= GEN_MIN

    # Handle remainer using prog
    if rem_depth != 0:
        fifo_gens[ 0]["full_level" ] = fifo_gens[ 0]["depth"] + rem_depth
        fifo_gens[-1]["empty_level"] = fifo_gens[-1]["depth"] + rem_depth

    # Declare FIFO_generator compoments
    included_fifo_gens = []
    for fifo_gen in fifo_gens:
        name =  "FIFO_gen_%i_%i"%(CONFIG["width"], fifo_gen["depth"])
        if fifo_gen["full_level"] != None:
            name += "_f%i"%(fifo_gen["full_level"])
        if fifo_gen["empty_level"] != None:
            name += "_e%i"%(fifo_gen["empty_level"])

        if name not in included_fifo_gens:
            included_fifo_gens.append(name)

            ARCH_HEAD += "\ncomponent %s\n\>"%(name,)
            ARCH_HEAD += "port (\n\>"
            ARCH_HEAD += "clk   : in  std_logic;\n"
            ARCH_HEAD += "srst  : in  std_logic;\n"
            ARCH_HEAD += "din   : in  std_logic_vector(%i downto 0);\n"%(CONFIG["width"] - 1, )
            ARCH_HEAD += "wr_en : in  std_logic;\n"
            ARCH_HEAD += "dout  : out std_logic_vector(%i downto 0);\n"%(CONFIG["width"] - 1, )
            ARCH_HEAD += "rd_en : in  std_logic;\n"
            ARCH_HEAD += "full  : out std_logic;\n"
            ARCH_HEAD += "empty : out std_logic;\n"
            if fifo_gen["full_level"] != None:
                ARCH_HEAD += "prog_full  : out std_logic;\n"
            if fifo_gen["empty_level"] != None:
                ARCH_HEAD += "prog_empty : out std_logic;\n"

            ARCH_HEAD.drop_last_X(2)
            ARCH_HEAD += "\<\n);"
            ARCH_HEAD += "\<\nend component;\n"

    # Instancate FIFO_generator compoments
    for fifo_count, fifo_gen in enumerate(fifo_gens):
        name =  "FIFO_gen_%i_%i"%(CONFIG["width"], fifo_gen["depth"])
        if fifo_gen["full_level"] != None:
            name += "_f%i"%(fifo_gen["full_level"])
        if fifo_gen["empty_level"] != None:
            name += "_e%i"%(fifo_gen["empty_level"])

        ARCH_HEAD += "\n-- FIFO_gen_%i signals\n"%(fifo_count,)
        ARCH_HEAD += "signal FIFO_gen_%i_data_in  : std_logic_vector(%i downto 0);\n"%(fifo_count, CONFIG["width"] - 1)
        ARCH_HEAD += "signal FIFO_gen_%i_data_out : std_logic_vector(%i downto 0);\n"%(fifo_count, CONFIG["width"] - 1)
        ARCH_HEAD += "signal FIFO_gen_%i_write : std_logic;\n"%(fifo_count,)
        ARCH_HEAD += "signal FIFO_gen_%i_read  : std_logic;\n"%(fifo_count,)
        ARCH_HEAD += "signal FIFO_gen_%i_full  : std_logic;\n"%(fifo_count,)
        ARCH_HEAD += "signal FIFO_gen_%i_empty : std_logic;\n"%(fifo_count,)

        ARCH_BODY += "\nFIFO_gen_%i : %s\n\>"%(fifo_count, name)
        ARCH_BODY += "port map (\n\>"
        ARCH_BODY += "clk   => clock,\n"
        ARCH_BODY += "srst  => clear,\n"
        ARCH_BODY += "din   => FIFO_gen_%i_data_in,\n"%(fifo_count,)
        ARCH_BODY += "wr_en => FIFO_gen_%i_write,\n"%(fifo_count,)
        ARCH_BODY += "dout  => FIFO_gen_%i_data_out,\n"%(fifo_count,)
        ARCH_BODY += "rd_en => FIFO_gen_%i_read,\n"%(fifo_count,)
        ARCH_BODY += "full  => FIFO_gen_%i_full, \n"%(fifo_count,)
        ARCH_BODY += "empty => FIFO_gen_%i_empty,\n"%(fifo_count,)

        if fifo_gen["full_level"] != None:
            ARCH_HEAD += "signal FIFO_gen_%i_prog_full : std_logic;\n"%(fifo_count,)
            ARCH_BODY += "prog_full  => FIFO_gen_%i_prog_full,\n"%(fifo_count,)
        if fifo_gen["empty_level"] != None:
            ARCH_HEAD += "signal FIFO_gen_%i_prog_empty : std_logic;\n"%(fifo_count,)
            ARCH_BODY += "prog_empty => FIFO_gen_%i_prog_empty,\n"%(fifo_count,)

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\<\n"

        if fifo_count == 0:
            ARCH_BODY += "FIFO_gen_0_data_in <= data_in;\n"
            ARCH_BODY += "FIFO_gen_0_write   <= data_write;\n"
            ARCH_BODY += "data_write_ready   <= not FIFO_gen_0_full;\n"
        else:
            ARCH_BODY += "FIFO_gen_%i_data_in <= FIFO_gen_%i_data_out;\n"%(fifo_count, fifo_count - 1)
            ARCH_BODY += "FIFO_gen_%i_write <= (not FIFO_gen_%i_empty) and (not FIFO_gen_%i_full);\n"%(fifo_count    , fifo_count - 1, fifo_count)
            ARCH_BODY += "FIFO_gen_%i_read  <= (not FIFO_gen_%i_empty) and (not FIFO_gen_%i_full);\n"%(fifo_count - 1, fifo_count - 1, fifo_count)

    # Handle last FIFO_gen to data output
    ARCH_BODY += "data_out <= FIFO_gen_%i_data_out;\n"%(len(fifo_gens) - 1)
    ARCH_BODY += "FIFO_gen_%i_read <= data_read;\n"%(len(fifo_gens) - 1)
    ARCH_BODY += "data_read_ready <= not FIFO_gen_%i_empty;\n"%(len(fifo_gens) - 1)


    # Handle states
    ARCH_BODY += "\n"
    ARCH_BODY += "full  <= %s;\n"%(
        " and ".join(
            [
                "FIFO_gen_%i_prog_full"%(fifo_count,)
                if fifo_gen["full_level"] != None else
                "FIFO_gen_%i_full"%(fifo_count,)
                for fifo_count, fifo_gen in enumerate(fifo_gens)
            ]
        )
    )
    ARCH_BODY += "empty <= %s;\n"%(
        " and ".join(
            [
                "FIFO_gen_%i_prog_empty"%(fifo_count,)
                if fifo_gen["empty_level"] != None else
                "FIFO_gen_%i_empty"%(fifo_count,)
                for fifo_count, fifo_gen in enumerate(fifo_gens)
            ]
        )
    )

if __name__ == "__main__":
    generate_HDL(
        {
            "depth" : 32 + 16 + 8,
            "width" : 1,
        },
        ".",
        "FIFO",
        GENERATE_NAME=True,
        force_generation=True
    )
