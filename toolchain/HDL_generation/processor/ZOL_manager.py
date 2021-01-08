# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import ZOL_tracker

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(config_in["PC_width"] > 0)
    config_out["PC_width"] = config_in["PC_width"]

    assert(type(config_in["ZOLs"]) == type([]) )
    config_out["ZOLs"] = []
    for ZOL in config_in["ZOLs"]:

        assert(ZOL > 0)
        config_out["ZOLs"].append(ZOL)

    assert(type(config_in["stallable"]) == type(True))
    config_out["stallable"] = config_in["stallable"]

    return config_out

import zlib

def handle_module_name(module_name, config, generate_name):
    if generate_name == True:
        generated_name = "ZOL_manager"

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

        generated_name += "_%iw"%(config["PC_width"], )

        generated_name += "_%s"%str( hex( zlib.adler32(str(config["ZOLs"]).encode('utf-8')) )).lstrip("0x").zfill(8)

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

        # Include extremely commom libs
        IMPORTS += [ {"library" : "ieee", "package" : "std_logic_1164", "parts" : "all"} ]

        INTERFACE["ports"] += [ { "name" : "clock", "type" : "std_logic", "direction" : "in" } ]

        # Generation Module Code
        generate_loops()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_loops():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, GENERATE_NAME, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    INTERFACE["ports"] += [
        {
            "name" : "value_in",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
            "direction" : "in"
        },
        {
            "name" : "value_out",
            "type" : "std_logic_vector(%i downto 0)"%(CONFIG["PC_width"] - 1),
            "direction" : "out"
        },
        {
            "name" : "overwrite",
            "type" : "std_logic",
            "direction" : "out"
        },
        {
            "name" : "PC_running",
            "type" : "std_logic",
            "direction" : "in"
        },
    ]
    if CONFIG["stallable"]:
        INTERFACE["ports"] += [
            {
                "name" : "stall",
                "type" : "std_logic",
                "direction" : "in"
            },
        ]

    value_out = "value_out <= \>"
    overwrite = "overwrite <= \>"

    INTERFACE["delay_encoding"] = []
    for loop_id, loop_count in enumerate(CONFIG["ZOLs"]):
        interface, name = ZOL_tracker.generate_HDL(
            {
                "count" : loop_count,
                "width" : CONFIG["PC_width"],
                "stallable" : CONFIG["stallable"],
            },
            OUTPUT_PATH,
            "ZOL_tracker",
            True,
            True
        )
        INTERFACE["delay_encoding"].append(interface["delay_encoding"])

        ARCH_BODY += "tracker_%i : entity work.%s(arch)\n\>"%(loop_id, name)

        ARCH_BODY += "generic map (\>\n"
        for generic in interface["generics"]:
            INTERFACE["generics"] += [
                    {
                        "name" : "loop_%i_%s"%(loop_id, generic["name"]),
                        "type" : generic["type"]
                    }
                ]
            ARCH_BODY += "%s => loop_%i_%s,\n"%(generic["name"], loop_id, generic["name"])
        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n)\n"


        ARCH_HEAD += "signal tracker_%i_value_out : std_logic_vector(%i downto 0);\n"%(loop_id, CONFIG["PC_width"] - 1)
        ARCH_HEAD += "signal tracker_%i_overwrite : std_logic;\n"%(loop_id)

        ARCH_BODY += "port map (\>\n"

        if CONFIG["stallable"]:
            ARCH_BODY += "stall => stall,\n"

        ARCH_BODY += "clock => clock,\n"
        ARCH_BODY += "PC_running => PC_running,\n"
        ARCH_BODY += "value_in => value_in,\n"

        ARCH_BODY += "value_out => tracker_%i_value_out,\n"%(loop_id)
        ARCH_BODY += "overwrite => tracker_%i_overwrite,\n"%(loop_id)

        ARCH_BODY.drop_last_X(2)
        ARCH_BODY += "\<\n);\n"

        ARCH_BODY += "\<\n"

        value_out += "tracker_%i_value_out when tracker_%i_overwrite = '1'\nelse "%(loop_id, loop_id)
        overwrite    += "'1' when tracker_%i_overwrite = '1'\nelse "%(loop_id)

    value_out += "\<(others => '0');\n"
    overwrite    += "\<'0';\n"
    ARCH_BODY += value_out
    ARCH_BODY += overwrite
