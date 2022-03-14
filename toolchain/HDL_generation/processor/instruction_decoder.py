# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))


import itertools as it
import copy

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import alu_dsp48e1

from FPE.toolchain.HDL_generation.basic import delay
from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    config_out["stallable"] = config_in["stallable"]

    # Handle instr_set section of config
    assert(len(config_in["instr_set"]) > 0)
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])

    # Handle program_flow section of config
    config_out["program_flow"] = {}
    assert(type(config_in["program_flow"]["ZOLs"]) == type({}))
    config_out["program_flow"]["ZOLs"] = copy.deepcopy(config_in["program_flow"]["ZOLs"])

    # Handle instruction decoder section of config
    config_out["instr_decoder"] = {}

    assert(config_in["instr_decoder"]["instr_width"] > 0)
    config_out["instr_decoder"]["instr_width"] = config_in["instr_decoder"]["instr_width"]

    assert(config_in["instr_decoder"]["opcode_width"] > 0)
    config_out["instr_decoder"]["opcode_width"] = config_in["instr_decoder"]["opcode_width"]

    assert(type(config_in["instr_decoder"]["addr_widths"]) == type([]))
    config_out["instr_decoder"]["addr_widths"] = []
    for width in config_in["instr_decoder"]["addr_widths"]:
        assert(width > 0)
        config_out["instr_decoder"]["addr_widths"].append(width)

    config_out["controls"] = config_in["controls"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = ""

        raise NotImplementedError()

        return generated_name
    else:
        return module_name

#####################################################################

def generate_HDL(config, output_path, module_name=None, concat_naming=False, force_generation=False):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION

    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"


    # Moves parameters into global scope
    CONFIG = preprocess_config(config)
    OUTPUT_PATH = output_path
    MODULE_NAME = handle_module_name(module_name, CONFIG)
    CONCAT_NAMING = concat_naming
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
        INTERFACE = { "ports" : { }, "generics" : { } }

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

        # Generation Module Code
        define_decode_table_type()
        compute_instr_sections()
        generate_input_ports()
        generate_fetch_signals()
        generate_exe_signals()
        generate_store_signals()

        # Save code to file
        gen_utils.generate_files(OUTPUT_PATH, MODULE_NAME, IMPORTS, ARCH_HEAD, ARCH_BODY, INTERFACE)

        return INTERFACE, MODULE_NAME

#####################################################################

def generate_std_logic_signal(sig_name, value_opcode_table):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    # Declare control port
    INTERFACE["ports"][sig_name] = {
        "type" : "std_logic",
        "direction" : "out",
    }

    # Buffer port
    interface, reg = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : CONFIG["stallable"],
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_HEAD += "signal pre_%s : std_logic;\n"%(sig_name, )

    ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(sig_name, reg, )

    ARCH_BODY += "generic map (data_width => 1)\n"

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "enable => not stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0)  => pre_%s,\n"%(sig_name, )
    ARCH_BODY += "data_out(0) => %s\n"%(sig_name, )

    ARCH_BODY += "\<);\n\<"

    # Built decode table
    opcode_value_table = {}
    for opcode in range(2**INSTR_SECTIONS["opcode"]["width"]):
        values = [
            value
            for value, opcodes in value_opcode_table.items()
            if  opcode in opcodes
        ]

        if   len(values) == 0:
            opcode_value_table[opcode] = 'U'
        elif len(values) == 1:
            opcode_value_table[opcode] = values[0]
        else:
            raise ValueError("Multiple values, %s, for signal, %s, for opcode, %i]"%(
                    str(values),
                    sig_name,
                    opcode,
                )
            )

    # Add decode table
    ARCH_HEAD += "constant %s_decode_table : decode_table := (\>\n"%(sig_name, )
    # Working decode table, in as rows of 8 values
    for i in range(2**max([INSTR_SECTIONS["opcode"]["width"] - 3, 0])):
        for j in range(2**min([INSTR_SECTIONS["opcode"]["width"], 3])):
            ARCH_HEAD += "\'%s\',\t"%(opcode_value_table[8*i + j])
        ARCH_HEAD += "\n"
    ARCH_HEAD.drop_last_X(3)
    ARCH_HEAD += "\n\<);\n\n"

    ARCH_BODY += "pre_%s <= 'U' when %s /= '1' else %s_decode_table(%s);\n\n"%(sig_name, INPUT_SIGNALS["enable"], sig_name, INPUT_SIGNALS["OPCODE"])

def generate_std_logic_vector_signal(sig_name, vec_len, value_opcode_table):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    assert(vec_len >= 0)

    # Declare control port
    INTERFACE["ports"][sig_name] = {
        "type" : "std_logic_vector",
        "width": vec_len,
        "direction" : "out",
    }

    # Buffer port
    interface, reg = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : CONFIG["stallable"],
            "force_on_init" : False
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_HEAD += "signal pre_%s : std_logic_vector(%i downto 0);\n"%(sig_name, vec_len - 1)

    ARCH_BODY += "%s_buffer : entity work.%s(arch)\>\n"%(sig_name, reg, )

    ARCH_BODY += "generic map (data_width => %i)\n"%(vec_len, )

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "enable => not stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => pre_%s,\n"%(sig_name, )
    ARCH_BODY += "data_out => %s\n"%(sig_name, )

    ARCH_BODY += "\<);\n\<"

    # Built decode table
    opcode_value_table = {}
    for opcode in range(2**INSTR_SECTIONS["opcode"]["width"]):
        values = [
            list(value)
            for value, opcodes in value_opcode_table.items()
            if  opcode in opcodes
        ]

        if   len(values) == 0:
            opcode_value_table[opcode] = ['U']*vec_len
        elif len(values) == 1:
            opcode_value_table[opcode] = list(values[0])
            # Reverse as bit are number right to the left not left to right
            opcode_value_table[opcode].reverse()

        else:
            raise ValueError("Multiple values, %s, for signal, %s, for opcode, %i]"%(
                    str(values),
                    sig_name,
                    opcode,
                )
            )

    # Add decode table
    for bit in range(vec_len):
        ARCH_HEAD += "constant %s_bit_%i_decode_table : decode_table := (\>\n"%(sig_name, bit, )
        # Working decode table, in as rows of 8 values
        for i in range(2**max([INSTR_SECTIONS["opcode"]["width"] - 3, 0])):
            for j in range(2**min([INSTR_SECTIONS["opcode"]["width"], 3])):
                ARCH_HEAD += "\'%s\',\t"%(opcode_value_table[8*i + j][bit])
            ARCH_HEAD += "\n"
        ARCH_HEAD.drop_last_X(3)
        ARCH_HEAD += "\n\<);\n"

        ARCH_BODY += "pre_%s(%i) <= 'U' when %s /= '1' else %s_bit_%i_decode_table(%s);\n"%(
            sig_name,
            bit,
            INPUT_SIGNALS["enable"],
            sig_name,
            bit,
            INPUT_SIGNALS["OPCODE"]
        )

    ARCH_HEAD += "\n"
    ARCH_BODY += "\n"

def generate_input_signals_delay(stage):
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ARCH_HEAD += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(stage, CONFIG["instr_decoder"]["instr_width"]  - 1, )

    interface, name = delay.generate_HDL(
        {
            "width" : CONFIG["instr_decoder"]["instr_width"],
            "depth" : 1,
            "stallable" : CONFIG["stallable"],
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "%s_instr_delay : entity work.%s(arch)\>\n"%(stage, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in  => %s,\n"%(INPUT_SIGNALS["instr"], )
    ARCH_BODY += "data_out => %s_instr_delay_out\n"%(stage, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["instr"] = "%s_instr_delay_out"%(stage, )

    ARCH_HEAD += "signal %s_enable_delay_out : std_logic;\n"%(stage, )

    interface, name = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "stallable" : CONFIG["stallable"],
        },
        OUTPUT_PATH,
        module_name=None,
        concat_naming=False,
        force_generation=FORCE_GENERATION
    )

    ARCH_BODY += "%s_enable_delay : entity work.%s(arch)\>\n"%(stage, name)

    ARCH_BODY += "port map (\n\>"

    if CONFIG["stallable"]:
        ARCH_BODY += "stall => stall,\n"

    ARCH_BODY += "clock => clock,\n"
    ARCH_BODY += "data_in(0) => %s,\n"%(INPUT_SIGNALS["enable"], )
    ARCH_BODY += "data_out(0) => %s_enable_delay_out\n"%(stage, )

    ARCH_BODY += "\<);\<\n\n"

    INPUT_SIGNALS["enable"] = "%s_enable_delay_out"%(stage, )

    ARCH_HEAD += "signal %s_opcode : integer;\n\n"%(stage, )
    ARCH_BODY += "%s_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        stage,
        INPUT_SIGNALS["instr"],
        INSTR_SECTIONS["opcode"]["range"],
    )
    INPUT_SIGNALS["OPCODE"] = "%s_opcode"%(stage, )

#####################################################################

def define_decode_table_type():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY

    ARCH_HEAD += "type decode_table is array(0 to %i) of std_logic;\n\n"%(
        2**CONFIG["instr_decoder"]["opcode_width"] - 1,
    )

def compute_instr_sections():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global DELAY_INTERFACE, DELAY_NAME
    global INPUT_SIGNALS, INSTR_SECTIONS

    INSTR_SECTIONS = {}

    # Handle opcode
    INSTR_SECTIONS["opcode"] = {
        "width" : CONFIG["instr_decoder"]["opcode_width"],
        "range" : "%i downto %i"%(CONFIG["instr_decoder"]["instr_width"] - 1,  CONFIG["instr_decoder"]["instr_width"] - CONFIG["instr_decoder"]["opcode_width"])
    }

    # Section off addrs
    INSTR_SECTIONS["addrs"] = []
    addr_start = CONFIG["instr_decoder"]["instr_width"] - CONFIG["instr_decoder"]["opcode_width"]
    for width in CONFIG["instr_decoder"]["addr_widths"]:
        INSTR_SECTIONS["addrs"].append( {
            "width" : width,
            "range" : "%i downto %i"%(addr_start - 1,  addr_start - width)
        } )
        addr_start -= width

def generate_input_ports():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    INTERFACE["ports"]["clock"] = {
        "type" : "std_logic",
        "direction" : "in",
    }
    INTERFACE["ports"]["enable"] = {
        "type" : "std_logic",
        "direction" : "in",
    }
    INTERFACE["ports"]["instr"] = {
        "type" : "std_logic_vector",
        "width": CONFIG["instr_decoder"]["instr_width"],
        "direction" : "in",
    }

    INPUT_SIGNALS = {}
    INPUT_SIGNALS["instr"] = "instr"
    INPUT_SIGNALS["enable"] = "enable"

    ARCH_HEAD += "signal input_opcode : integer;\n\n"
    ARCH_BODY += "input_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        INPUT_SIGNALS["instr"],
        INSTR_SECTIONS["opcode"]["range"],
    )
    INPUT_SIGNALS["OPCODE"] = "input_opcode"

    if CONFIG["stallable"]:
        INTERFACE["ports"]["stall"] = {
            "name" : "stall" ,
            "type" : "std_logic",
            "direction" : "in",
        }


def generate_fetch_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Handle fetch signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(CONFIG["controls"], "fetch").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        value_opcode_table = {}
        for value, instrs in control_values.items():
            value_opcode_table[value] = [CONFIG["instr_set"][instr] for instr in instrs]

        if   control_type == "std_logic":
            generate_std_logic_signal(control_signal, value_opcode_table)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            generate_std_logic_vector_signal(control_signal, control_width, value_opcode_table)
        else:
            raise ValueError("Unknown control_type, " + control_type)

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("fetch")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle fetch addrs
    for addr, dic in enumerate(INSTR_SECTIONS["addrs"]):
        width = dic["width"]
        section = dic["range"]

        INTERFACE["ports"]["addr_%i_fetch"%(addr)] = {
            "type" : "std_logic_vector",
            "width": width,
            "direction" : "out",
        }

        ARCH_BODY += "addr_%i_fetch <= %s(%s);\n"%(addr, INPUT_SIGNALS["instr"], section)
    ARCH_BODY += "\n"

exe_lib_lookup = {
    "ALU" : alu_dsp48e1,
}

def generate_exe_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Handle exe signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(CONFIG["controls"], "exe").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        value_opcode_table = {}
        for value, instrs in control_values.items():
            value_opcode_table[value] = [CONFIG["instr_set"][instr] for instr in instrs]

        if   control_type == "std_logic":
            generate_std_logic_signal(control_signal, value_opcode_table)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            generate_std_logic_vector_signal(control_signal, control_width, value_opcode_table)
        else:
            raise ValueError("Unknown control_type, " + control_type)


    # # Handle uncondional jumping signal
    # if any([ asm_utils.instr_mnemonic(instr) == "JMP" for instr in CONFIG["instr_set"]]):
    #     sig_name = "jump_uncondional"
    #     value_opcode_table = { "1" : [], "0" : []}
    #     for instr_id, instr_val in CONFIG["instr_set"].items():
    #         if asm_utils.instr_mnemonic(instr_id) == "JMP":
    #             value_opcode_table["1"].append(instr_val)
    #         else:
    #             value_opcode_table["0"].append(instr_val)
    #
    #     # Check the signal varies
    #     value_opcode_table = {
    #         k : v
    #         for k, v in value_opcode_table.items()
    #         if len(v) > 0
    #     }
    #     if len(value_opcode_table) > 1:
    #         generate_std_logic_signal(sig_name, value_opcode_table)
    #
    # # Handle condional jumping signals
    # statuses = set()
    # for instr in CONFIG["instr_set"]:
    #     if "ALU" in asm_utils.instr_exe_units(instr) and "PC" in asm_utils.instr_exe_units(instr):
    #         statuses.add(jump_status_map[ asm_utils.instr_mnemonic(instr)])
    # exe = "ALU"
    # for statuses in statuses:
    #     for status in statuses:
    #         sig_name = "jump_%s_%s"%(exe, status)
    #         value_opcode_table = { "1" : [], "0" : []}
    #         for instr_id, instr_val in CONFIG["instr_set"].items():
    #             mnemonic = asm_utils.instr_mnemonic(instr_id)
    #
    #             if (
    #                 mnemonic in jump_mnemonic_jump_statuses_map # instr in a jump
    #                 and jump_mnemonic_jump_statuses_map[mnemonic]["exe"] == exe # jump uses status(es) from curr exe unit
    #                 and status in jump_mnemonic_jump_statuses_map[mnemonic]["statuses"] # jump uses current status
    #             ):
    #                 value_opcode_table["1"].append(instr_val)
    #             else:
    #                 value_opcode_table["0"].append(instr_val)
    #
    #         # Check the signal varies
    #         value_opcode_table = {
    #             k : v
    #             for k, v in value_opcode_table.items()
    #             if len(v) > 0
    #         }
    #         if len(value_opcode_table) > 1:
    #             generate_std_logic_signal(sig_name, value_opcode_table)

    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("exe")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

exe_update_mnemonics_map = {
    "ALU" :  ["UCMP", "SCMP", ],
}

def generate_store_signals():
    global CONFIG, OUTPUT_PATH, MODULE_NAME, CONCAT_NAMING, FORCE_GENERATION
    global INTERFACE, IMPORTS, ARCH_HEAD, ARCH_BODY
    global INPUT_SIGNALS, INSTR_SECTIONS

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################

    # Handle exe signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(CONFIG["controls"], "store").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        value_opcode_table = {}
        for value, instrs in control_values.items():
            value_opcode_table[value] = [CONFIG["instr_set"][instr] for instr in instrs]

        if   control_type == "std_logic":
            generate_std_logic_signal(control_signal, value_opcode_table)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            generate_std_logic_vector_signal(control_signal, control_width, value_opcode_table)
        else:
            raise ValueError("Unknown control_type, " + control_type)


    ####################################################################
    # Buffer INPUT_SIGNALS for next stage
    ####################################################################
    generate_input_signals_delay("store")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle store addrs
    for addr, dic in enumerate(INSTR_SECTIONS["addrs"]):
        width = dic["width"]
        section = dic["range"]

        INTERFACE["ports"]["addr_%i_store"%(addr)] = {
            "type" : "std_logic_vector",
            "width": width,
            "direction" : "out",
        }


        ARCH_BODY += "addr_%i_store <= %s(%s);\n"%(addr, INPUT_SIGNALS["instr"], section)
    ARCH_BODY += "\n"
