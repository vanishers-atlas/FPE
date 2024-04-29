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

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    fetched_operands = set()
    internal_operands = {}
    supported_shifts = set()

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            operands = asm_utils.instr_operands(instr)

            if mnemonic in ["LSH", "RSH", "LRL", "RRL", ]:
                # non-parallel, shift operations
                assert len(mnemonic_parts) == 1
                bits = int(mnemonic_parts[0])

                # Handle operand
                assert len(operands) == 1
                operand = operands[0]

                # Check for fetched operand
                if   not asm_utils.access_is_internal(operand):
                    # Record required port(s)
                    fetched_operands.add(0)

                    # Record required shifts
                    supported_shifts.add( ( ("fetched", ), (mnemonic, bits, ), 1, ) )
                # Check knew internals - acc
                elif asm_utils.access_internal(operand) in ["ACC", ]:
                    # Record required port(s)
                    try:
                        internal_operands["acc"] = max(internal_operands["acc"], 1)
                    except KeyError:
                        internal_operands["acc"] = 1

                    # Record required shifts
                    supported_shifts.add( ( ("acc", ), (mnemonic, bits, ), 1, ) )
                # Flag up any unknown cases
                else:
                    raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["PLSH", "PRSH", "PLRL", "PRRL", ]:
                # Handle operand
                assert len(operands) == 1
                operand = operands[0]

                # parallel shift operations
                assert len(mnemonic_parts) == 2
                bits = int(mnemonic_parts[0])
                num_words = int(mnemonic_parts[1])

                # Handle operand
                assert len(operands) == 1
                operand = operands[0]

                # Check for fetched operand
                if   not asm_utils.access_is_internal(operand):
                    # Record required port(s)
                    for word in range(num_words):
                        fetched_operands.add(word)

                    # Record required shifts
                    supported_shifts.add( ( ("fetched", ), (mnemonic[1:], bits, ), num_words, ) )
                # Check knew internals - acc
                elif asm_utils.access_internal(operand) in ["ACC", ]:
                    # Record required port(s)
                    try:
                        internal_operands["acc"] = max(internal_operands["acc"], num_words)
                    except KeyError:
                        internal_operands["acc"] = num_words

                    # Record required shifts
                    supported_shifts.add( ( ("acc", ), (mnemonic[1:], bits, ), num_words, ) )
                # Flag up any unknown cases
                else:
                    raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))

    config["fetched_operands"] = list(fetched_operands)
    config["internal_operands"] = internal_operands
    config["supported_shifts"] = list(supported_shifts)

    return config

SHIFTER_MNEMONICS = (
    "LSH", "PLSH",
    "RSH", "PRSH",
    "LRL", "PLRL",
    "RRL", "PRRL",
)

fetched_operand_pattern = re.compile("shifter_fetched_word_(\\d*)")
def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    # Handle fetched_operand ports
    for port in interface["ports"]:
        match = fetched_operand_pattern.fullmatch(port)
        if match:
            word = int(match.group(1))
            for instr in instr_set:
                if (instr_id in asm_utils.instr_exe_units(instr)
                    and asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))[0] in SHIFTER_MNEMONICS
                ):
                    operands = asm_utils.instr_operands(instr)
                    if len(operands) > 0 and not asm_utils.access_is_internal(operands[0]):
                        operand_mods = asm_utils.access_mods(operands[0])
                        if word == 0 or "BAPA" in operand_mods and word < int(operand_mods["BAPA"]):
                            dataMesh.connect_sink(sink=instr_prefix + port,
                                channel="%sfetch_data_0_word_%i"%(lane, word),
                                condition=instr,
                                stage="exe", inplace_channel=True,
                                padding_type=config["signal_padding"], width=interface["ports"][port]["width"]
                            )

    return dataMesh

operand_sel_map_pattern = re.compile("shifter_word_(\\d*)_operand_sel")
shift_sel_pattern = re.compile("shifter_word_(\\d*)_shift_sel")
def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle source_sel controls
    for port in interface["ports"]:
        match = operand_sel_map_pattern.fullmatch(port)
        if match:
            word = int(match.group(1))
            map = interface["shifter"]["word_%i_operand_map"%(word, )]

            values = { }
            for instr in instr_set:
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    operands = asm_utils.instr_operands(instr)
                    mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

                    if mnemonic_parts[0] in ["LSH", "RSH", "LRL", "RRL", "PLSH", "PRSH", "PLRL", "PRRL", ]:
                        # Compute number of words
                        if mnemonic_parts[0] in ["PLSH", "PRSH", "PLRL", "PRRL", ]:
                            num_words = int(mnemonic_parts[-1])
                        else:
                            num_words = 1

                        if word < num_words:
                            if not asm_utils.access_is_internal(operands[0]):
                                value = map["fetched"]
                            else:
                                internal = asm_utils.access_internal(operands[0])
                                if internal == "ACC":
                                    value = map["acc"]
                                else:
                                    raise ValueError("Unknown internal %s"%(internal, ) )
                key = tc_utils.unsigned.encode(value, interface["ports"][port]["width"])
                try:
                    values[key].append(instr)
                except KeyError:
                    values[key] = [instr, ]
            gen_utils.add_control(controls, "exe", instr_prefix + port, values, "std_logic_vector", interface["ports"][port]["width"])

    # Handle source_sel controls
    for port in interface["ports"]:
        match = shift_sel_pattern.fullmatch(port)
        if match:
            word = int(match.group(1))
            map = interface["shifter"]["word_%i_shift_map"%(word, )]

            values = { }
            for instr in instr_set:
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    operands = asm_utils.instr_operands(instr)
                    mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

                    if mnemonic_parts[0] in ["LSH", "RSH", "LRL", "RRL", "PLSH", "PRSH", "PLRL", "PRRL", ]:
                        # Compute number of words
                        bits = mnemonic_parts[1]
                        if mnemonic_parts[0] in ["PLSH", "PRSH", "PLRL", "PRRL", ]:
                            num_words = int(mnemonic_parts[-1])
                            shift = mnemonic_parts[0][1:]
                        else:
                            num_words = 1
                            shift = mnemonic_parts[0]

                        if word < num_words:
                            value = map["%s#%s"%(shift, bits)]
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

    assert type(config_in["fetched_operands"]) == list, "fetched_operands must be a list"
    if __debug__:
        for operand in config_in["fetched_operands"]:
            assert type(operand) == int
            assert operand >= 0
    config_out["fetched_operands"] = sorted(config_in["fetched_operands"])

    assert type(config_in["internal_operands"]) == dict, "internal_operands must be a dict"
    if __debug__:
        for signal, words in config_in["internal_operands"].items():
            assert signal in ["acc", ]
            assert type(words) == int
            assert words > 0
    config_out["internal_operands"] = config_in["internal_operands"]

    assert type(config_in["supported_shifts"]) == list, "supported_packings must be a list"
    if __debug__:
        for source, shift, num_words in config_in["supported_shifts"]:
            assert type(source) == tuple
            assert len(source) == 1
            assert source[0] in ["acc", "fetched", ]

            assert len(shift) == 2
            assert shift[0] in ["LSH", "RSH", "LRL", "RRL", ]
            assert type(shift[1]) == int
            assert shift[1] > 0
            assert shift[1] < config_out["data_width"]

            assert type(num_words) == int
            assert num_words >= 0
    supported_shifts = []
    for source, shift, num_words in config_in["supported_shifts"]:
        for word in range(num_words):
            try:
                supported_shifts[word]["sources"].add(source[0])
                # Make sure the bits is in range

                supported_shifts[word]["shifts"].add(shift)
            except IndexError:
                supported_shifts.append(
                    {
                        "sources" : set(),
                        "shifts" : set(),
                    }
                )
                supported_shifts[word]["sources"].add(source[0])
                supported_shifts[word]["shifts"].add(shift)
    config_out["supported_packings"] = [
        {
            "sources" : sorted(word["sources"]),
            "shifts": sorted(word["shifts"]),
        }
        for word in supported_shifts
    ]

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
        gen_input_handling(gen_det, com_det)
        gen_shifting(gen_det, com_det)


        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_input_handling(gen_det, com_det):
    # Declare required ports
    # Fetched operands
    for word in gen_det.config["fetched_operands"]:
        com_det.add_port("fetched_word_%i"%(word, ), "std_logic_vector", "in", gen_det.config["data_width"])

    # Internal operands
    for operand in sorted(gen_det.config["internal_operands"]):
        for word in range(gen_det.config["internal_operands"][operand]):
            com_det.add_port("%s_word_%i"%(operand, word, ), "std_logic_vector", "in", gen_det.config["data_width"])

    # Handle input mux
    for word, word_details in enumerate(gen_det.config["supported_packings"]):
        sources = word_details["sources"]
        com_det.arch_head += "signal word_%i_muxed : std_logic_vector(%i downto 0);\n"%(word, gen_det.config["data_width"] - 1)
        if len(sources) == 1:
            com_det.arch_body += "word_%i_muxed <= %s_word_%i;\n\n"%(word, sources[0], word, )
        else:
            # Handle input data mux
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs"  : len(sources),
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            com_det.arch_body += "word_%i_operand_mux : entity work.%s(arch)@>\n"%(word, mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

            com_det.arch_body += "port map (\n@>"

            com_det.add_port("word_%i_operand_sel"%(word, ), "std_logic_vector", "in", mux_interface["sel_width"])
            com_det.arch_body += "sel => word_%i_operand_sel,\n"%(word, )

            sel_map = {}
            for sel_val, signal in enumerate(sources):
                com_det.arch_body += "data_in_%i => %s_word_%i,\n"%(sel_val, signal, word, )
                sel_map[signal] = sel_val
            com_det.add_interface_item("word_%i_operand_map"%(word, ), sel_map)

            for input in range(len(sources), mux_interface["number_inputs"]):
                com_det.arch_body += "data_in_%i => (others => 'U'),\n"%(input, )

            com_det.arch_body += "data_out  => word_%i_muxed \n"%(word, )

            com_det.arch_body += "@<);\n@<\n"

def gen_shifting(gen_det, com_det):
    for word, word_details in enumerate(gen_det.config["supported_packings"]):
        shifts = word_details["shifts"]

        shifted_signals = {}
        for shift in word_details["shifts"]:
            type = shift[0]
            bits = shift[1]

            if   type == "LSH":
                com_det.arch_head += "signal %s_%i_word_%i : std_logic_vector(%i downto 0);\n"%(type, bits, word, gen_det.config["data_width"] - 1)
                shifted_signals[shift] = "%s_%i_word_%i"%(type, bits, word, )

                com_det.arch_body += "%s_%i_word_%i(%i downto %i) <= word_%i_muxed(%i downto 0);\n"%(
                        type, bits, word, gen_det.config["data_width"] - 1, bits,
                        word, gen_det.config["data_width"] - (bits + 1),
                    )
                com_det.arch_body += "%s_%i_word_%i(%i downto 0) <= (others => '0');\n\n"%(
                        type, bits, word, bits - 1
                    )
            elif type == "RSH":
                com_det.arch_head += "signal %s_%i_word_%i : std_logic_vector(%i downto 0);\n"%(type, bits, word, gen_det.config["data_width"] - 1)
                shifted_signals[shift] = "%s_%i_word_%i"%(type, bits, word, )

                com_det.arch_body += "%s_%i_word_%i(%i downto 0) <= word_%i_muxed(%i downto %i);\n"%(
                        type, bits, word, gen_det.config["data_width"] - (bits + 1),
                        word, gen_det.config["data_width"] - 1, bits,
                    )
                if   gen_det.config["signal_padding"] == "unsigned":
                    com_det.arch_body += "%s_%i_word_%i(%i downto %i) <= (others => '0');\n\n"%(
                            type, bits, word, gen_det.config["data_width"] - 1, gen_det.config["data_width"] - bits,
                        )
                elif gen_det.config["signal_padding"] == "signed":
                    com_det.arch_body += "%s_%i_word_%i(%i downto %i) <= (others => word_%i_muxed(%i));\n\n"%(
                            type, bits, word,
                            gen_det.config["data_width"] - 1, gen_det.config["data_width"] - bits,
                            word, gen_det.config["data_width"] - 1,
                        )
                else:
                    raise ValueError("Unknown signal_padding, %s"%(gen_det.config["signal_padding"], ))
            elif type == "LRL":
                # LRL and RRL can be equivalent
                # As all LRL are processed before RRL, no need to check of equivalent RRL here
                com_det.arch_head += "signal %s_%i_word_%i : std_logic_vector(%i downto 0);\n"%(type, bits, word, gen_det.config["data_width"] - 1)
                shifted_signals[shift] = "%s_%i_word_%i"%(type, bits, word, )

                com_det.arch_body += "%s_%i_word_%i(%i downto %i) <= word_%i_muxed(%i downto 0);\n"%(
                        type, bits, word, gen_det.config["data_width"] - 1, bits,
                        word, gen_det.config["data_width"] - (bits + 1),
                    )
                com_det.arch_body += "%s_%i_word_%i(%i downto 0) <= word_%i_muxed(%i downto %i);\n\n"%(
                        type, bits, word, bits - 1,
                        word, gen_det.config["data_width"] - 1, gen_det.config["data_width"] - (bits),
                    )
            elif type == "RRL":
                # LRL and RRL can be equivalent
                # As all LRL are processed before check for equivalent LRL here
                equivalent_roll = ("LRL", gen_det.config["data_width"] - bits, )
                if equivalent_roll in shifted_signals.keys():
                    shifted_signals[shift] = "%s_%i_word_%i"%(equivalent_roll[0], equivalent_roll[1], word, )
                else:
                    com_det.arch_head += "signal %s_%i_word_%i : std_logic_vector(%i downto 0);\n"%(type, bits, word, gen_det.config["data_width"] - 1)
                    shifted_signals[shift] = "%s_%i_word_%i"%(type, bits, word, )

                    com_det.arch_body += "%s_%i_word_%i(%i downto 0) <= word_%i_muxed(%i downto %i);\n"%(
                            type, bits, word, gen_det.config["data_width"] - (bits + 1),
                            word, gen_det.config["data_width"] - 1, bits,
                        )
                    com_det.arch_body += "%s_%i_word_%i(%i downto %i) <= word_%i_muxed(%i downto 0);\n\n"%(
                            type, bits, word, gen_det.config["data_width"] - 1, gen_det.config["data_width"] - bits,
                            word, bits - 1,
                        )
            else:
                raise ValueError("Unknown shift type, %s"%(type, ))

        com_det.add_port("result_word_%i"%(word, ), "std_logic_vector", "out", gen_det.config["data_width"])
        if len(set(shifted_signals.values())) == 1:
            com_det.arch_body += "result_word_%i <= %s;\n"%(word, shifted_signals[word_details["shifts"][0]], )
        else:
            # Handle input data mux
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs"  : len(set(shifted_signals.values())),
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            com_det.arch_body += "word_%i_shift_mux : entity work.%s(arch)@>\n"%(word, mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

            com_det.arch_body += "port map (\n@>"

            com_det.add_port("word_%i_shift_sel"%(word, ), "std_logic_vector", "in", mux_interface["sel_width"])
            com_det.arch_body += "sel => word_%i_shift_sel,\n"%(word, )

            signal_sel_map = {}
            for sel_val, signal in enumerate(sorted(set(shifted_signals.values()))):
                com_det.arch_body += "data_in_%i => %s,\n"%(sel_val, signal, )
                signal_sel_map[signal] = sel_val
            sel_map = { "%s#%i"%(shift[0], shift[1], ) : signal_sel_map[signal] for shift, signal in shifted_signals.items()}
            com_det.add_interface_item("word_%i_shift_map"%(word, ), sel_map)

            for input in range(len(set(shifted_signals.values())), mux_interface["number_inputs"]):
                com_det.arch_body += "data_in_%i => (others => 'U'),\n"%(input, )

            com_det.arch_body += "data_out  => result_word_%i \n"%(word, )

            com_det.arch_body += "@<);\n@<\n"
