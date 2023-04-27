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

from FPE.toolchain.HDL_generation.basic import delay
from FPE.toolchain.HDL_generation.basic import dist_ROM

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

    # Check and preprocess parameters
    assert type(config) == dict, "config must be a dict"
    assert type(output_path) == str, "output_path must be a str"
    assert module_name == None or type(module_name) == str, "module_name must ne a string or None"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"
    if __debug__ and concat_naming == True:
        assert type(module_name) == str and module_name != "", "When using concat_naming, and a non blank module name is required"

    config = preprocess_config(config)
    module_name = handle_module_name(module_name, config)

    # Combine parameters into generation_details class for easy passing to functons
    gen_det = gen_utils.generation_details(config, output_path, module_name, concat_naming, force_generation)

    # Load return variables from pre-existing file if allowed and can
    try:
        return gen_utils.load_files(gen_det)
    except gen_utils.FilesInvalid:
        # Init component_details
        com_det = gen_utils.component_details()

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_import("ieee", "numeric_std", "all")

        # Generation Module Code
        define_decode_table_type(gen_det, com_det)
        compute_instr_sections(gen_det, com_det)
        generate_input_ports(gen_det, com_det)
        generate_fetch_signals(gen_det, com_det)
        generate_exe_signals(gen_det, com_det)
        generate_store_signals(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def generate_input_signals_delay(gen_det, com_det, stage):

    com_det.arch_head += "signal %s_instr_delay_out : std_logic_vector(%i downto 0);\n"%(stage, gen_det.config["instr_decoder"]["instr_width"]  - 1, )

    interface, name = delay.generate_HDL(
        {
            "width" : gen_det.config["instr_decoder"]["instr_width"],
            "depth" : 1,
            "has_enable" : gen_det.config["stallable"],
            "inited" : False,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "%s_instr_delay : entity work.%s(arch)\>\n"%(stage, name)

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall_in,\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "data_in  => %s,\n"%(gen_det.input_signals["instr"], )
    com_det.arch_body += "data_out => %s_instr_delay_out\n"%(stage, )

    com_det.arch_body += "\<);\<\n\n"

    gen_det.input_signals["instr"] = "%s_instr_delay_out"%(stage, )

    com_det.arch_head += "signal %s_enable_delay_out : std_logic;\n"%(stage, )

    interface, name = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "has_enable" : gen_det.config["stallable"],
            "inited" : False,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "%s_enable_delay : entity work.%s(arch)\>\n"%(stage, name)

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall_in,\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "data_in(0) => %s,\n"%(gen_det.input_signals["enable"], )
    com_det.arch_body += "data_out(0) => %s_enable_delay_out\n"%(stage, )

    com_det.arch_body += "\<);\<\n\n"

    gen_det.input_signals["enable"] = "%s_enable_delay_out"%(stage, )

    com_det.arch_head += "signal %s_opcode : integer;\n\n"%(stage, )
    com_det.arch_body += "%s_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        stage,
        gen_det.input_signals["instr"],
        gen_det.instr_sections["opcode"]["range"],
    )
    gen_det.input_signals["opcode"] = "%s_opcode"%(stage, )


def init_decoder_rom(gen_det, com_det):
    return {
        "slices" : {},
        "next_bit" : 0,
        "content": { instr : "" for instr in gen_det.config["instr_set"] },
    }

def handle_std_logic_signal(gen_det, com_det, decoder_rom, sig_name, control_values):
    # Handle fanout and port creation
    com_det.add_port(sig_name, "std_logic", "out")
    decoder_rom["slices"][sig_name] = decoder_rom["next_bit"]
    decoder_rom["next_bit"] += 1

    # Default any missing instrs to 0
    for instr in gen_det.config["instr_set"]:
        match_found = False
        for instrs in control_values.values():
            if instr in instrs:
                match_found = True
                break
        if match_found == False:
            control_values["0"].append(instr)

    # Append control_values to decoder_rom
    for value, instrs in control_values.items():
        for instr in instrs:
            decoder_rom["content"][instr] += value

def handle_std_logic_vector_signal(gen_det, com_det, decoder_rom, sig_name, vec_len, control_values):
    # Handle fanout and port creation
    com_det.add_port(sig_name, "std_logic_vector", "out", vec_len)
    decoder_rom["slices"][sig_name] = (decoder_rom["next_bit"], decoder_rom["next_bit"] + vec_len - 1)
    decoder_rom["next_bit"] += vec_len

    # Default any missing instrs to all 0s
    for instr in gen_det.config["instr_set"]:
        match_found = False
        for instrs in control_values.values():
            if instr in instrs:
                match_found = True
                break
        if match_found == False:
            try:
                control_values["0"*vec_len].append(instr)
            except Exception as e:
                control_values["0"*vec_len] = [instr, ]

    # Append control_values to decoder_rom
    for value, instrs in control_values.items():
        for instr in instrs:
            decoder_rom["content"][instr] += value[::-1]

def implement_decoder_rom(gen_det, com_det, decoder_rom, stage):

    rom_width = decoder_rom["next_bit"]
    rom_interface, rom_name = dist_ROM.generate_HDL(
        {
            "depth" : len(decoder_rom["content"]),
            "reads" : 1,
            "width" : rom_width,
            "synchronous" : False,
            "has_enable" : False,
            "init_type" : "GENERIC_STD"
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_head += "signal control_signals_%s : std_logic_vector(%i downto 0);\n"%(stage, rom_width- 1, )
    com_det.arch_head += "signal control_signals_%s_buffered : std_logic_vector(%i downto 0);\n"%(stage, rom_width- 1, )

    # Instancate ROM
    com_det.arch_body += "decode_ROM_%s : entity work.%s(arch)\>\n"%(stage, rom_name,)

    com_det.arch_body += "generic map (\>\n"
    rev_instr_set = {v : k for k, v in gen_det.config["instr_set"].items()}
    for addr in range(2**rom_interface["addr_width"]):
        try:
            com_det.arch_body += "init_%i => \"%s\",\n"%(addr, decoder_rom["content"][rev_instr_set[addr]][::-1], )
        except Exception as e:
            com_det.arch_body += "init_%i => \"%s\",\n"%(addr, "0"*rom_width, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<)\n"

    com_det.arch_body += "port map (\n\>"
    com_det.arch_body += "read_0_addr => %s(%s),\n"%(gen_det.input_signals["instr"], gen_det.instr_sections["opcode"]["range"], )
    com_det.arch_body += "read_0_data => control_signals_%s\n"%(stage, )

    com_det.arch_body += "\<);\n\<\n"

    # Instancate buffer
    interface, name = delay.generate_HDL(
        {
            "width" : rom_width,
            "depth" : 1,
            "has_enable" : gen_det.config["stallable"],
            "inited" : False,
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "control_signals_%s_delay : entity work.%s(arch)\>\n"%(stage, name)

    com_det.arch_body += "port map (\n\>"

    if gen_det.config["stallable"]:
        com_det.arch_body += "enable => not stall_in,\n"

    com_det.arch_body += "clock => clock,\n"
    com_det.arch_body += "data_in  => control_signals_%s,\n"%(stage, )
    com_det.arch_body += "data_out => control_signals_%s_buffered\n"%(stage, )

    com_det.arch_body += "\<);\<\n\n"

    # Slice up ROM output and connect to control ports
    for port, slice in decoder_rom["slices"].items():
        if   type(slice) == int:
            com_det.arch_body += "%s <= control_signals_%s_buffered(%i);\n"%(port, stage, slice, )
        elif type(slice) == tuple:
            com_det.arch_body += "%s <= control_signals_%s_buffered(%i downto %i);\n"%(port, stage, slice[1], slice[0], )
        else:
            raise ValueError("unknown slice type")


#####################################################################

def define_decode_table_type(gen_det, com_det):
    com_det.arch_head += "type decode_table is array(0 to %i) of std_logic;\n\n"%(
        2**gen_det.config["instr_decoder"]["opcode_width"] - 1,
    )

def compute_instr_sections(gen_det, com_det):
    gen_det.instr_sections = {}

    # Handle opcode
    gen_det.instr_sections["opcode"] = {
        "width" : gen_det.config["instr_decoder"]["opcode_width"],
        "range" : "%i downto %i"%(gen_det.config["instr_decoder"]["instr_width"] - 1,  gen_det.config["instr_decoder"]["instr_width"] - gen_det.config["instr_decoder"]["opcode_width"])
    }

    # Section off addrs
    gen_det.instr_sections["addrs"] = []
    addr_start = gen_det.config["instr_decoder"]["instr_width"] - gen_det.config["instr_decoder"]["opcode_width"]
    for width in gen_det.config["instr_decoder"]["addr_widths"]:
        gen_det.instr_sections["addrs"].append( {
            "width" : width,
            "range" : "%i downto %i"%(addr_start - 1,  addr_start - width)
        } )
        addr_start -= width

def generate_input_ports(gen_det, com_det):

    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("enable", "std_logic", "in")
    com_det.add_port("instr", "std_logic_vector", "in", gen_det.config["instr_decoder"]["instr_width"])

    gen_det.input_signals = {}
    gen_det.input_signals["instr"] = "instr"
    gen_det.input_signals["enable"] = "enable"

    com_det.arch_head += "signal input_opcode : integer;\n\n"
    com_det.arch_body += "input_opcode <= to_integer(unsigned(%s(%s)));\n\n"%(
        gen_det.input_signals["instr"],
        gen_det.instr_sections["opcode"]["range"],
    )
    gen_det.input_signals["opcode"] = "input_opcode"

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")


def generate_fetch_signals(gen_det, com_det):

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################
    decoder_rom = init_decoder_rom(gen_det, com_det)

    # Handle fetch signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(gen_det.config["controls"], "fetch").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        if   control_type == "std_logic":
            handle_std_logic_signal(gen_det, com_det, decoder_rom, control_signal, control_values)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            handle_std_logic_vector_signal(gen_det, com_det, decoder_rom, control_signal, control_width, control_values)
        else:
            raise ValueError("Unknown control_type, " + control_type)

    if len(gen_utils.get_controls(gen_det.config["controls"], "fetch")) != 0:
        implement_decoder_rom(gen_det, com_det, decoder_rom, "fetch")

    ####################################################################
    # Buffer gen_det.input_signals for next stage
    ####################################################################
    generate_input_signals_delay(gen_det, com_det, "fetch")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle fetch addrs
    for addr, dic in enumerate(gen_det.instr_sections["addrs"]):
        width = dic["width"]
        section = dic["range"]

        com_det.add_port("addr_%i_fetch"%(addr), "std_logic_vector", "out", width)

        com_det.arch_body += "addr_%i_fetch <= %s(%s);\n"%(addr, gen_det.input_signals["instr"], section)
    com_det.arch_body += "\n"

def generate_exe_signals(gen_det, com_det):

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################
    decoder_rom = init_decoder_rom(gen_det, com_det)

    # Handle exe signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(gen_det.config["controls"], "exe").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        if   control_type == "std_logic":
            handle_std_logic_signal(gen_det, com_det, decoder_rom, control_signal, control_values)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            handle_std_logic_vector_signal(gen_det, com_det, decoder_rom, control_signal, control_width, control_values)
        else:
            raise ValueError("Unknown control_type, " + control_type)

    if False:
        # Handle uncondional jumping signal
        if any([ asm_utils.instr_mnemonic(instr) == "JMP" for instr in gen_det.config["instr_set"]]):
            sig_name = "jump_uncondional"
            value_opcode_table = { "1" : [], "0" : []}
            for instr_id, instr_val in gen_det.config["instr_set"].items():
                if asm_utils.instr_mnemonic(instr_id) == "JMP":
                    value_opcode_table["1"].append(instr_val)
                else:
                    value_opcode_table["0"].append(instr_val)

            # Check the signal varies
            value_opcode_table = {
                k : v
                for k, v in value_opcode_table.items()
                if len(v) > 0
            }
            if len(value_opcode_table) > 1:
                handle_std_logic_signal(gen_det, com_det, decoder_rom, sig_name, control_values)

        # Handle condional jumping signals
        statuses = set()
        for instr in gen_det.config["instr_set"]:
            if "ALU" in asm_utils.instr_exe_units(instr) and "PC" in asm_utils.instr_exe_units(instr):
                statuses.add(jump_status_map[ asm_utils.instr_mnemonic(instr)])
        exe = "ALU"
        for statuses in statuses:
            for status in statuses:
                sig_name = "jump_%s_%s"%(exe, status)
                value_opcode_table = { "1" : [], "0" : []}
                for instr_id, instr_val in gen_det.config["instr_set"].items():
                    mnemonic = asm_utils.instr_mnemonic(instr_id)

                    if (
                        mnemonic in jump_mnemonic_jump_statuses_map # instr in a jump
                        and jump_mnemonic_jump_statuses_map[mnemonic]["exe"] == exe # jump uses status(es) from curr exe unit
                        and status in jump_mnemonic_jump_statuses_map[mnemonic]["statuses"] # jump uses current status
                    ):
                        value_opcode_table["1"].append(instr_val)
                    else:
                        value_opcode_table["0"].append(instr_val)

                # Check the signal varies
                value_opcode_table = {
                    k : v
                    for k, v in value_opcode_table.items()
                    if len(v) > 0
                }
                if len(value_opcode_table) > 1:
                    handle_std_logic_signal(gen_det, com_det, decoder_rom, sig_name, control_values)

    if len(gen_utils.get_controls(gen_det.config["controls"], "exe")) != 0:
        implement_decoder_rom(gen_det, com_det, decoder_rom, "exe")

    ####################################################################
    # Buffer gen_det.input_signals for next stage
    ####################################################################
    generate_input_signals_delay(gen_det, com_det, "exe")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

exe_update_mnemonics_map = {
    "ALU" :  ["UCMP", "SCMP", ],
}

def generate_store_signals(gen_det, com_det):

    ####################################################################
    # Compute then buffer controls based on opcode
    ####################################################################
    decoder_rom = init_decoder_rom(gen_det, com_det)

    # Handle exe signals defined using new control method
    for control_signal, control_details in gen_utils.get_controls(gen_det.config["controls"], "store").items():
        # Extract control_details
        control_values = control_details["values"]
        control_type = control_details["type"]

        if   control_type == "std_logic":
            handle_std_logic_signal(gen_det, com_det, decoder_rom, control_signal, control_values)
        elif control_type == "std_logic_vector":
            control_width = control_details["width"]
            handle_std_logic_vector_signal(gen_det, com_det, decoder_rom, control_signal, control_width, control_values)
        else:
            raise ValueError("Unknown control_type, " + control_type)

    if len(gen_utils.get_controls(gen_det.config["controls"], "store")) != 0:
        implement_decoder_rom(gen_det, com_det, decoder_rom, "store")

    ####################################################################
    # Buffer gen_det.input_signals for next stage
    ####################################################################
    generate_input_signals_delay(gen_det, com_det, "store")

    ####################################################################
    # Output controls that are directly part of instr
    ####################################################################

    # Handle store addrs
    for addr, dic in enumerate(gen_det.instr_sections["addrs"]):
        width = dic["width"]
        section = dic["range"]

        com_det.add_port("addr_%i_store"%(addr), "std_logic_vector", "out", width)


        com_det.arch_body += "addr_%i_store <= %s(%s);\n"%(addr, gen_det.input_signals["instr"], section)
    com_det.arch_body += "\n"
