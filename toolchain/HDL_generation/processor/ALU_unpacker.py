# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import register

#####################################################################


def add_inst_config(instr_id, instr_set, config):

    supported_unpackings = set()
    required_results = 0
    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            results = asm_utils.instr_results(instr)
            required_results = max(required_results, len(results))

            if   mnemonic in ["MOV", "NOT", "ADD", "MUL", "AND", "OR", "XOR", "LSH", "RSH", "LRL", "RRL", "SUB", "UCMP", "SCMP", ]:
                # non-parallel operations

                # Handle acc
                supported_unpackings.add((0, "unpadded", "acc", 1))

                # Handle results
                for index, result in enumerate(results):
                    # Check for stored results
                    if   not asm_utils.access_is_internal(result):
                        # Record required unpadding
                        supported_unpackings.add((index, "unpadded", "stored_%i"%(index, ), 1))
                    # Check knew internals - acc
                    elif asm_utils.access_internal(result) in ["ACC", ]:
                        assert index == 0
                        # acc already handled
                        pass
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(result))
            elif mnemonic in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
                pass
            elif mnemonic in ["PMOV", "PNOT", "PAND", "POR", "PXOR", "PLSH", "PRSH", "PLRL", "PRRL",]:
                # non-padding-parallel operations
                num_words = int(mnemonic_parts[-1])

                # Handle acc
                supported_unpackings.add((0, "unpadded", "acc", num_words))

                # Handle results
                for index, result in enumerate(results):
                    # Check for stored results
                    if   not asm_utils.access_is_internal(result):
                        # Record required unpadding
                        supported_unpackings.add((index, "unpadded", "stored_%i"%(index, ), num_words))
                    # Check knew internals - acc
                    elif asm_utils.access_internal(result) in ["ACC", ]:
                        assert index == 0
                        # acc already handled
                        pass
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(result))
            elif mnemonic in ["PADD", "PSUB", ]:
                # single-bit-padding-parallel operations

                num_words = int(mnemonic_parts[-1])

                # Handle acc
                supported_unpackings.add((0, "single_bit", "acc", num_words))

                # Handle results
                for index, result in enumerate(results):
                    # Check for stored results
                    if   not asm_utils.access_is_internal(result):
                        # Record required unpadding
                        supported_unpackings.add((index, "single_bit", "stored_%i"%(index, ), num_words))
                    # Check knew internals - acc
                    elif asm_utils.access_internal(result) in ["ACC", ]:
                        assert index == 0
                        # acc already handled
                        pass
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(result))
            else:
                # Flag up any unknown cases
                raise ValueError("Unsupported mnemonic, " + mnemonic)

    stored_results = set()
    internal_results = {}

    config["supported_unpackings"] = sorted(supported_unpackings)
    config["result_widths"] = [1 for _ in range(required_results) ]

    return config

stored_results_pattern = re.compile("result_(\d*)_word_(\d*)")
def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    # Handle stored_operand ports
    for port in interface["ports"]:
        match = stored_results_pattern.fullmatch(port)
        if match:
            store = int(match.group(1))
            word = int(match.group(2))
            for instr in instr_set:
                if instr_id in asm_utils.instr_exe_units(instr):
                    results = asm_utils.instr_results(instr)
                    if len(results) > store and not asm_utils.access_is_internal(results[store]):
                        result_mods = asm_utils.access_mods(results[store])
                        if word == 0 or "BAPA" in result_mods and word < int(result_mods["BAPA"]):
                            gen_utils.add_datapath_source(pathways, "%sstore_data_%i_word_%i"%(lane, store, word),
                                "store", instr, instr_prefix + port, config["signal_padding"], interface["ports"][port]["width"]
                            )

    return pathways

output_mux_sel_pattern = re.compile("unpacker_([\w\d]+)_word_(\d*)_sel")
def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle enable control
    enable = { "0" : [], "1" : [], }
    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            enable["1"].append(instr)
        else:
            enable["0"].append(instr)
    gen_utils.add_control(controls, "exe", instr_prefix + "unpacker_enable", enable, "std_logic")

    # Handle output_mux_sel control
    for port in interface["ports"]:
        match = output_mux_sel_pattern.fullmatch(port)
        if match:
            output = match.group(1)
            word = int(match.group(2))

            map = interface["unpacker"]["%s_word_%i_map"%(output, word, )]

            values = { }
            for instr in instr_set:
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

                    # Compute number of words
                    if mnemonic in ["PMOV", "PLSH", "PRSH", "PLRL", "PRRL", "PADD", "PSUB", "PNOT", "PAND", "POR", "PXOR", ]:
                        num_words = int(mnemonic_parts[-1])
                    else:
                        num_words = 1

                    if word < num_words:
                            if   mnemonic in ["MOV", "LSH", "RSH", "LRL", "RRL", "NOT", "AND", "OR", "XOR", "ADD", "SUB", ]:
                                value = map["0#unpadded"]
                            elif mnemonic in ["PMOV", "PLSH", "PRSH", "PLRL", "PRRL", "PNOT", "PAND", "POR", "PXOR", ]:
                                value = map["0#unpadded"]
                            elif mnemonic in ["PADD", "PSUB", ]:
                                value = map["0#single_bit"]
                            else:
                                raise ValueError("Unknown mnemonic %s"%(mnemonic, ) )
                key = tc_utils.unsigned.encode(value, interface["ports"][port]["width"])
                try:
                    values[key].append(instr)
                except KeyError:
                    values[key] = [instr, ]
            gen_utils.add_control(controls, "exe", instr_prefix + port, values, "std_logic_vector", interface["ports"][port]["width"])



    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["data_width"]) == int, "data_width must be an int"
    assert config_in["data_width"] >= 1, "data_width must be greater than 0"
    config_out["data_width"] = config_in["data_width"]

    assert type(config_in["signal_padding"]) == str, "signal_padding must be an str"
    assert config_in["signal_padding"] in ["unsigned", "signed", ], "Unknown signal_padding, %s"%(config_in["signal_padding"], )
    config_out["signal_padding"] = config_in["signal_padding"]

    # Check packing parameters
    assert type(config_in["supported_unpackings"]) == list, "supported_unpackings must be a list"
    if __debug__:
        for packing in config_in["supported_unpackings"]:
                assert len(packing) == 4
                result = packing[0]
                mode = packing[1]
                dest = packing[2]
                num_words = packing[3]

                assert type(result) == int
                assert result >= 0

                assert mode in ["unpadded", "single_bit", ]

                assert type(dest) == str
                assert dest in ["acc", ] or dest.startswith("stored_")

                assert type(num_words) == int
                assert num_words >= 0
    unpackings = []
    output_ports = {}
    for packing in config_in["supported_unpackings"]:
        result = packing[0]
        mode = packing[1]
        dest = packing[2]
        num_words = packing[3]

        # Compute unpackings
        try:
            unpackings[result][mode] = max(unpackings[result][mode], num_words)
        except KeyError:
            unpackings[result][mode] = num_words
        except IndexError:
            unpackings.append({mode : num_words })


        # Compute output_ports
        for word in range(num_words):
            try:
                output_ports[dest][word].add((result, mode, ))
            except IndexError:
                output_ports[dest].append(set())
                output_ports[dest][word].add((result, mode, ))
            except KeyError:
                output_ports[dest] = [set(), ]
                output_ports[dest][word].add((result, mode, ))

    config_out["unpackings"] = unpackings
    config_out["outputs"] = {
        k : [
            sorted(word) for word in v
        ]
        for k, v in output_ports.items()
    }

    assert type(config_in["result_widths"]) == list, "result_widths must be a list"
    assert len(config_in["result_widths"]) >= len(unpackings)
    config_out["result_widths"] = config_in["result_widths"]

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

        # Generation Module Code
        gen_unpacker(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name

#####################################################################

def gen_unpacker(gen_det, com_det):
    com_det.add_port("enable", "std_logic", "in")
    com_det.add_port("clock", "std_logic", "in")


    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : True,
            "force_on_init" : False
        },
        gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # Handle packings
    for result, packings in enumerate(gen_det.config["unpackings"]):
        # Declare result port
        com_det.add_port("result_%i"%(result, ), "std_logic_vector", "in", gen_det.config["result_widths"][result])

        # Handle packings
        if "unpadded" in packings.keys():
            LSM = 0
            for word in range(packings["unpadded"]):
                MSB = LSM + gen_det.config["data_width"]
                com_det.arch_head += "signal result_%i_unpadded_word_%i : std_logic_vector(%i downto 0);\n"%(result, word, gen_det.config["data_width"] - 1, )
                com_det.arch_body += "result_%i_unpadded_word_%i <= result_%i(%i downto %i);\n"%(result, word, result, MSB - 1, LSM, )
                LSM = MSB
            com_det.arch_body += "\n"
        if "single_bit" in packings.keys():
            LSM = 0
            for word in range(packings["unpadded"]):
                if word != 0:
                    LSM += 1
                MSB = LSM + gen_det.config["data_width"]
                com_det.arch_head += "signal result_%i_single_bit_word_%i : std_logic_vector(%i downto 0);\n"%(result, word, gen_det.config["data_width"] - 1, )
                com_det.arch_body += "result_%i_single_bit_word_%i <= result_%i(%i downto %i);\n"%(result, word, result, MSB - 1, LSM, )
                LSM = MSB
            com_det.arch_body += "\n"


    # Handle outputs
    for output, words in gen_det.config["outputs"].items():
        for word, sources in enumerate(words):
            # Declare output port
            com_det.add_port("%s_word_%i"%(output, word), "std_logic_vector", "out", gen_det.config["data_width"])

            # Handle output mapping
            if len(sources) == 1:
                result = sources[0][0]
                mode =  sources[0][1]
                com_det.arch_body += "%s_word_%i <= result_%i_%s_word_%i;\n\n"%(output, word, result, mode, word, )
            else:
                mux_interface, mux_name = mux.generate_HDL(
                    {
                        "inputs"  : len(sources),
                    },
                    gen_det.output_path,
                    module_name=None,
                    concat_naming=False,
                    force_generation=gen_det.force_generation
                )

                com_det.add_port("%s_word_%i_sel"%(output, word, ), "std_logic_vector", "in", mux_interface["sel_width"])
                com_det.arch_head += "signal %s_word_%i_sel_buffered : std_logic_vector(%i downto 0);\n"%(output, word, mux_interface["sel_width"] - 1, )

                com_det.arch_body += "%s_word_%i_sel_buffer : entity work.%s(arch)\>\n"%(output, word, reg_name, )
                com_det.arch_body += "generic map (data_width => %i)\n"%(mux_interface["sel_width"], )
                com_det.arch_body += "port map (\n\>"
                com_det.arch_body += "clock => clock,\n"
                com_det.arch_body += "enable  => enable,\n"
                com_det.arch_body += "data_in  => %s_word_%i_sel,\n"%(output, word, )
                com_det.arch_body += "data_out => %s_word_%i_sel_buffered\n"%(output, word, )
                com_det.arch_body += "\<);\n\<\n"

                com_det.arch_body += "%s_word_%i_mux : entity work.%s(arch)\>\n"%(output, word, mux_name, )

                com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

                com_det.arch_body += "port map (\n\>"

                com_det.arch_body += "sel => %s_word_%i_sel_buffered,\n"%(output, word, )

                sel_map = {}
                for sel_val, signal in enumerate(sources):
                    result = signal[0]
                    mode =  signal[1]
                    com_det.arch_body += "data_in_%i => result_%i_%s_word_%i,\n"%(sel_val, result, mode, word, )
                    sel_map["%i#%s"%(result, mode)] = sel_val
                com_det.add_interface_item("%s_word_%i_map"%(output, word, ), sel_map)

                for input in range(len(packings), mux_interface["number_inputs"]):
                    com_det.arch_body += "data_in_%i => (others => 'U'),\n"%(input, )

                com_det.arch_body += "data_out  => %s_word_%i \n"%(output, word, )

                com_det.arch_body += "\<);\n\<\n"
