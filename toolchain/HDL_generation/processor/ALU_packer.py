# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re
import math

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    fetched_operands = set()
    internal_operands = {}
    supported_packings = []

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            operands = asm_utils.instr_operands(instr)

            if   mnemonic in ["MOV", "ADD", "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR", ]:
                # 1non-parallel, commutative operations

                # Handle operands
                for index, operand in enumerate(operands):
                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # No change of behavour based on commutative usage
                        # therefore fetch via index, even if internal operand(s) before this fetched operand

                        # Record required port(s)
                        fetched_operands.add((index, 0, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))
                        except IndexError:
                            while len(supported_packings) < index + 1:
                                supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # acc handled by core for non parallel, non multiple operations so pass
                        pass
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
                pass
            elif mnemonic in ["MUL", ]:
                # non-parallel, multiple operation

                # Handle operands
                for index, operand in enumerate(operands):
                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # Record required port(s)
                        fetched_operands.add((index, 0, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # Record required port(s)
                        try:
                            internal_operands["acc"] = max(internal_operands["acc", ], 1)
                        except KeyError:
                            internal_operands["acc"] = 1

                        try:
                            supported_packings[index].add(( ("acc", ), ("unpadded", ), 1, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("acc", ), ("unpadded", ), 1, ))

                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["LSH", "RSH", "LRL", "RRL", ]:
                # non-parallel, shift operations

                # Handle operands
                for index, operand in enumerate(operands):
                    # Record required port(s)
                    try:
                        internal_operands["shifter"] = max(internal_operands["shifter"], 1)
                    except KeyError:
                        internal_operands["shifter"] = 1

                    # Record required padding
                    try:
                        supported_packings[index].add(( ("shifter", ), ("unpadded", ), 1 ))
                    except IndexError:
                        supported_packings.append(set())
                        supported_packings[index].add(( ("shifter", ), ("unpadded", ), 1 ))
            elif mnemonic in ["SUB", "UCMP", "SCMP", ]:
                # non-parallel, non-commutative operations

                # Handle operands
                for index, operand in enumerate(operands):
                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # Record required port(s)
                        fetched_operands.add((index, 0, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), 1, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # acc handled by core for non parallel, non multiple operations so pass
                        pass
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["PMOV", "PNOT", "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR", ]:
                # non-padding-parallel, commutative operations

                num_words = int(mnemonic_parts[-1])

                # Handle operands
                for index, operand in enumerate(operands):
                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # No change of behavour based on commutative usage
                        # therefore fetch via index, even if internal operand(s) before this fetched operand

                        # Record required port(s)
                        for word in range(num_words):
                            fetched_operands.add((index, word, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), ("unpadded", ), num_words, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # Record required port(s)
                        try:
                            internal_operands["acc"] = max(internal_operands["acc", ], num_words)
                        except KeyError:
                            internal_operands["acc"] = num_words

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("acc", ), ("unpadded", ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("acc", ), ("unpadded", ), num_words, ))
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["PLSH", "PRSH", "PLRL", "PRRL", ]:
                # parallel shift operations

                num_words = int(mnemonic_parts[-1])

                # Handle operands
                for index, operand in enumerate(operands):
                    # Record required port(s)
                    try:
                        internal_operands["shifter"] = max(internal_operands["shifter"], num_words)
                    except KeyError:
                        internal_operands["shifter"] = num_words

                    # Record required padding
                    try:
                        supported_packings[index].add(( ("shifter", ), ("unpadded", ), num_words, ))
                    except IndexError:
                        supported_packings.append(set())
                        supported_packings[index].add(( ("shifter", ), ("unpadded", ), num_words, ))
            elif mnemonic in ["PADD", ]:
                # monopadded parallel, commutative operations

                num_words = int(mnemonic_parts[-1])

                # Handle operands
                for index, operand in enumerate(operands):
                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # No change of behavour based on commutative usage
                        # therefore fetch via index, even if internal operand(s) before this fetched operand

                        # Record required port(s)
                        for word in range(num_words):
                            fetched_operands.add((index, word, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), ("single_zero", ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), ("single_zero", ), num_words, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # Record required port(s)
                        try:
                            internal_operands["acc"] = max(internal_operands["acc", ], num_words)
                        except KeyError:
                            internal_operands["acc"] = num_words

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("acc", ), ("single_zero", ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("acc", ), ("single_zero", ), num_words, ))

                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            elif mnemonic in ["PSUB", ]:
                # single bit padded parallel, non-commutative operations

                num_words = int(mnemonic_parts[-1])

                # Handle operands
                for index, operand in enumerate(operands):
                    if   index == 0:
                        padding_type = "single_one"
                    elif index == 1:
                        padding_type = "single_zero"
                    else:
                        raise ValueError("Only 2 operands are supported for PSUB")

                    # Check for fetched operand
                    if   not asm_utils.access_is_internal(operand):
                        # Record required port(s)
                        for word in range(num_words):
                            fetched_operands.add((index, word, ))

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("fetched", index, ), (padding_type, ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("fetched", index, ), (padding_type, ), num_words, ))

                    # Check knew internals - acc
                    elif asm_utils.access_internal(operand) in ["ACC", ]:
                        # Record required port(s)
                        try:
                            internal_operands["acc"] = max(internal_operands["acc", ], num_words)
                        except KeyError:
                            internal_operands["acc"] = num_words

                        # Record required padding
                        try:
                            supported_packings[index].add(( ("acc", ), (padding_type, ), num_words, ))
                        except IndexError:
                            supported_packings.append(set())
                            supported_packings[index].add(( ("acc", ), (padding_type, ), num_words, ))
                    # Flag up any unknown cases
                    else:
                        raise ValueError("Unknown internal, " + asm_utils.access_internal(operand))
            else:
                raise ValueError("Unsupported mnemonic, " + mnemonic)
    config["fetched_operands"] = list(fetched_operands)
    config["internal_operands"] = internal_operands
    config["supported_packings"] = [ list(v) for v in supported_packings ]

    return config

fetched_operand_pattern = re.compile("packer_fetched_(\d*)_word_(\d*)")
def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    # Handle fetched_operand ports
    for port in interface["ports"]:
        match = fetched_operand_pattern.fullmatch(port)
        if match:
            operand = int(match.group(1))
            word = int(match.group(2))
            for instr in instr_set:
                if instr_id in asm_utils.instr_exe_units(instr):
                    operands = asm_utils.instr_operands(instr)
                    if len(operands) > operand and not asm_utils.access_is_internal(operands[operand]):
                        fetches = [ asm_utils.access_is_internal(operand) for operand in operands ]
                        fetch = fetches[:operand].count(False)

                        operand_mods = asm_utils.access_mods(operands[operand])
                        if word == 0 or "BAPA" in operand_mods and word < int(operand_mods["BAPA"]):
                            gen_utils.add_datapath_dest(pathways, "%sfetch_data_%i_word_%i"%(lane, fetch, word),
                                "exe", instr, instr_prefix + port, config["signal_padding"], interface["ports"][port]["width"]
                            )

    return pathways

block_size_sel_pattern =  re.compile("packer_input_(\d*)_block_size_sel")
source_sel_pattern = re.compile("packer_input_(\d*)_(\d*)_source_sel")
packing_sel_pattern = re.compile("packer_input_(\d*)_packing_sel")
def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle block_size_sel controls
    for port in interface["ports"]:
        match = block_size_sel_pattern.fullmatch(port)
        if match:
            operand = int(match.group(1))
            largest_block_size = 2**interface["ports"][port]["width"]

            values = { }
            for instr in instr_set:
                mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    # Compute number of words
                    if mnemonic in [
                        "PMOV", "PNOT", "PADD", "PSUB", "PMUL",
                        "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR",
                        "PLSH", "PRSH", "PLRL", "PRRL",
                    ]:
                        num_words = int(mnemonic_parts[-1])
                    else:
                        num_words = 1
                    value = num_words - 1

                key = tc_utils.unsigned.encode(value, interface["ports"][port]["width"])
                try:
                    values[key].append(instr)
                except KeyError:
                    values[key] = [instr, ]
            gen_utils.add_control(controls, "exe", instr_prefix + port, values, "std_logic_vector", interface["ports"][port]["width"])


    # Handle source_sel controls
    for port in interface["ports"]:
        match = source_sel_pattern.fullmatch(port)
        if match:
            operand = int(match.group(1))
            word = int(match.group(2))

            map = interface["packer"]["input_%i_%i_source_map"%(operand, word)]

            values = { }
            for instr in instr_set:
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    operands = asm_utils.instr_operands(instr)
                    mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

                    # Compute number of words
                    if mnemonic in [
                        "PMOV", "PNOT", "PADD", "PSUB", "PMUL",
                        "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR",
                        "PLSH", "PRSH", "PLRL", "PRRL",
                    ]:
                        num_words = int(mnemonic_parts[-1])
                    else:
                        num_words = 1

                    if operand < len(operands) and word < num_words:
                        if   mnemonic in ["LSH", "RSH", "LRL", "RRL", "PLSH", "PRSH", "PLRL", "PRRL", ]:
                            value = map["shifter"]
                        elif not asm_utils.access_is_internal(operands[operand]):
                            value = map["fetched_%i"%(operand, )]
                        else:
                            internal = asm_utils.access_internal(operands[operand])
                            if internal == "ACC":
                                if  mnemonic in [
                                    "MOV", "ADD", "SUB", "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR", ]:
                                    # Acc handled within core therefore skip this key
                                    continue
                                else:
                                    value = map["acc"]
                            else:
                                raise ValueError("Unknown internal %s"%(internal, ) )
                key = tc_utils.unsigned.encode(value, interface["ports"][port]["width"])
                try:
                    values[key].append(instr)
                except KeyError:
                    values[key] = [instr, ]
            gen_utils.add_control(controls, "exe", instr_prefix + port, values, "std_logic_vector", interface["ports"][port]["width"])


    # Handle packing_sel controls
    for port in interface["ports"]:
        match = packing_sel_pattern.fullmatch(port)
        if match:
            input = match.group(1)

            map = interface["packer"]["input_%s_packing_map"%(input, )]

            values = { }
            for instr in instr_set:
                value = 0
                if instr_id in asm_utils.instr_exe_units(instr):
                    mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

                    if   mnemonic in ["MOV", "LSH", "RSH", "LRL", "RRL", "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR", "ADD", "SUB", ]:
                        value = map["unpadded"]
                    elif mnemonic in ["PMOV", "PLSH", "PRSH", "PLRL", "PRRL", "PNOT", "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR", ]:
                        value = map["unpadded"]
                    elif mnemonic in ["PADD", ]:
                        value = map["single_zero"]
                    elif mnemonic in ["PSUB", ]:
                        if   input == "0":
                            value = map["single_one"]
                        elif input == "1":
                            value = map["single_zero"]
                        else:
                            raise ValueError("Only 2 operands are supported for PSUB")
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
    assert type(config_in["fetched_operands"]) == list, "fetched_operands must be a list"
    if __debug__:
        for operand in config_in["fetched_operands"]:
            assert type(operand) == tuple
            assert len(operand) == 2
            assert type(operand[0]) == int
            assert operand[0] >= 0
            assert type(operand[1]) == int
            assert operand[1] >= 0
    config_out["fetched_operands"] = sorted(config_in["fetched_operands"], key = lambda x: (x[0], x[1]))

    assert type(config_in["internal_operands"]) == dict, "internal_operands must be a dict"
    if __debug__:
        for signal, words in config_in["internal_operands"].items():
            assert signal in ["acc", "shifter", ]
            assert type(words) == int
            assert words > 0
    config_out["internal_operands"] = config_in["internal_operands"]

    assert type(config_in["supported_packings"]) == list, "supported_packings must be a list"
    if __debug__:
        for packings in config_in["supported_packings"]:
            for details in packings:
                assert len(details) == 3
                source = details[0]
                packing = details[1]
                num_words = details[2]

                assert type(source) == tuple
                if len(source) == 1:
                    assert source[0] in ["acc", "shifter", ]
                elif len(source) == 2:
                    assert source[0] in ["fetched", ]
                    assert type(source[1]) == int
                    assert source[1] >= 0
                else:
                    raise ValueError("unknown sourse, %s"%(source, ) )

                assert len(packing) == 1
                assert packing[0] in ["unpadded", "single_one", "single_zero", ]

                assert type(num_words) == int
                assert num_words >= 0
    supported_packings = []
    for operand, pathways in enumerate(config_in["supported_packings"]):
        for pathway in pathways:
            source_signal = pathway[0][0]
            if source_signal in ["fetched", ]:
                source_signal = "fetched_%i"%(pathway[0][1], )
            packing_mode = pathway[1][0]
            num_words = pathway[2]

            # Handle packings
            try:
                supported_packings[operand]["packings"][packing_mode] = max(supported_packings[operand]["packings"][packing_mode], num_words)
            except IndexError:
                supported_packings.append(
                    {
                        "sources" : [],
                        "packings": {},
                    },
                )
                supported_packings[operand]["packings"][packing_mode] = num_words
            except KeyError:
                supported_packings[operand]["packings"][packing_mode] = num_words

            for word in range(num_words):
                # Handle sources
                try:
                    supported_packings[operand]["sources"][word].add(source_signal)
                except IndexError:
                    supported_packings[operand]["sources"].append(set())
                    supported_packings[operand]["sources"][word].add(source_signal)

    config_out["supported_packings"] = [
        {
            "sources" : [ sorted(word) for word in operand["sources"] ],
            "packings": operand["packings"],
        }
        for operand in supported_packings
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
        gen_packer(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_packer(gen_det, com_det):
    # Declare required ports
    # Store results
    for operand, word in gen_det.config["fetched_operands"]:
        com_det.add_port("fetched_%i_word_%i"%(operand, word, ), "std_logic_vector", "in", gen_det.config["data_width"])

    # Internal results
    for operand in sorted(gen_det.config["internal_operands"]):
        for word in range(gen_det.config["internal_operands"][operand]):
            com_det.add_port("%s_word_%i"%(operand, word, ), "std_logic_vector", "in", gen_det.config["data_width"])

    # Generate packing muxes
    # Handle input data mux
    _, mux_2 = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    for operand, operand_details in enumerate(gen_det.config["supported_packings"]):
        for word, sources in enumerate(operand_details["sources"]):
            com_det.arch_head += "signal input_%i_%i_source : std_logic_vector(%i downto 0);\n"%(operand, word, gen_det.config["data_width"] - 1)
            if len(sources) == 1:
                com_det.arch_body += "input_%i_%i_source <= %s_word_%i;\n\n"%(operand, word, sources[0], word, )
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

                com_det.arch_body += "input_%i_%i_source_mux : entity work.%s(arch)\>\n"%(operand, word, mux_name, )

                com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

                com_det.arch_body += "port map (\n\>"

                com_det.add_port("input_%i_%i_source_sel"%(operand, word, ), "std_logic_vector", "in", mux_interface["sel_width"])
                com_det.arch_body += "sel => input_%i_%i_source_sel,\n"%(operand, word, )

                sel_map = {}
                for sel_val, signal in enumerate(sources):
                    com_det.arch_body += "data_in_%i => %s_word_%i,\n"%(sel_val, signal, word, )
                    sel_map[signal] = sel_val
                com_det.add_interface_item("input_%i_%i_source_map"%(operand, word, ), sel_map)

                for input in range(len(sources), mux_interface["number_inputs"]):
                    com_det.arch_body += "data_in_%i => (others => 'U'),\n"%(input, )

                com_det.arch_body += "data_out  => input_%i_%i_source \n"%(operand, word, )

                com_det.arch_body += "\<);\n\<\n"

        # Compute packed width
        packed_width = 0
        if "unpadded" in operand_details["packings"]:
            words = operand_details["packings"]["unpadded"]
            packed_width = max(packed_width, gen_det.config["data_width"] * words)
        if "single_one" in operand_details["packings"]:
            words = operand_details["packings"]["single_one"]
            packed_width = max(packed_width, gen_det.config["data_width"] * words + words - 1 )
        if "single_zero" in operand_details["packings"]:
            words = operand_details["packings"]["single_zero"]
            packed_width = max(packed_width, gen_det.config["data_width"] * words + words - 1 )

        # Handle packings
        max_words = 0
        if "unpadded" in operand_details["packings"]:
            max_words = max(max_words, operand_details["packings"]["unpadded"])
        if "single_one" in operand_details["packings"]:
            max_words = max(max_words, operand_details["packings"]["single_one"])
        if "single_zero" in operand_details["packings"]:
            max_words = max(max_words, operand_details["packings"]["single_zero"])
        if max_words != 1:
            num_block_sizes = int(math.log(max_words, 2) + 1)
            # Using 1 bit per block_size (less 1) over unsigned, to make internal decoding logic simpaler
            block_size_sel_width = num_block_sizes - 1
            com_det.add_port("input_%i_block_size_sel"%(operand, ), "std_logic_vector", "in", block_size_sel_width)

        packings = {}
        if "unpadded" in operand_details["packings"]:
            com_det.arch_head += "signal input_%i_unpadded : std_logic_vector(%i downto 0);\n"%(operand, packed_width - 1, )
            packings["unpadded"] = "input_%i_unpadded"%(operand, )

            LSB = 0
            MSB = LSB + gen_det.config["data_width"]
            com_det.arch_body += "input_%i_unpadded(%i downto %i) <= input_%i_0_source;\n"%(operand, MSB - 1, LSB, operand)
            LSB = MSB

            word = 1
            sel_bit = 0
            while word < operand_details["packings"]["unpadded"]:
                for _ in range(word):
                    MSB = LSB + gen_det.config["data_width"]

                    com_det.arch_body += "input_%i_unpadded_word_%i_mux : entity work.%s(arch)\>\n"%(operand, word, mux_2, )

                    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

                    com_det.arch_body += "port map (\n\>"

                    com_det.arch_body += "sel(0) => input_%i_block_size_sel(%i),\n"%(operand, sel_bit, )

                    com_det.arch_body += "data_in_0 => (others => '0'),\n"
                    com_det.arch_body += "data_in_1 => input_%i_%i_source,\n"%(operand, word, )

                    com_det.arch_body += "data_out  => input_%i_unpadded(%i downto %i)\n"%(operand, MSB - 1, LSB, )

                    com_det.arch_body += "\<);\n\<\n"

                    LSB = MSB
                    word += 1
                sel_bit += 1
            if packed_width > LSB:
                com_det.arch_body += "input_%i_unpadded(%i downto %i) <= (others => '0');\n"%(operand, packed_width - 1, LSB, )
            com_det.arch_body += "\n"
        if "single_one" in operand_details["packings"]:
            com_det.arch_head += "signal input_%i_single_one : std_logic_vector(%i downto 0);\n"%(operand, packed_width - 1, )
            packings["single_one"] = "input_%i_single_one"%(operand, )

            LSB = 0
            MSB = LSB + gen_det.config["data_width"]
            com_det.arch_body += "input_%i_single_one(%i downto %i) <= input_%i_0_source;\n"%(operand, MSB - 1, LSB, operand, )
            LSB = MSB

            word = 1
            sel_bit = 0
            while word < operand_details["packings"]["single_one"]:
                for _ in range(word):
                    com_det.arch_body += "input_%i_single_one(%i) <= '1';\n"%(operand, LSB, )
                    LSB += 1

                    MSB = LSB + gen_det.config["data_width"]

                    com_det.arch_body += "input_%i_single_one_word_%i_mux : entity work.%s(arch)\>\n"%(operand, word, mux_2, )

                    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

                    com_det.arch_body += "port map (\n\>"

                    com_det.arch_body += "sel(0) => input_%i_block_size_sel(%i),\n"%(operand, sel_bit, )

                    com_det.arch_body += "data_in_0 => (others => '0'),\n"
                    com_det.arch_body += "data_in_1 => input_%i_%i_source,\n"%(operand, word, )

                    com_det.arch_body += "data_out  => input_%i_single_one(%i downto %i)\n"%(operand, MSB - 1, LSB, )

                    com_det.arch_body += "\<);\n\<\n"

                    LSB = MSB
                    word += 1
                sel_bit += 1
            if packed_width > LSB:
                com_det.arch_body += "input_%i_single_one(%i downto %i) <= (others => '0');\n"%(operand, packed_width - 1, LSB, )
            com_det.arch_body += "\n"
        if "single_zero" in operand_details["packings"]:
            com_det.arch_head += "signal input_%i_single_zero : std_logic_vector(%i downto 0);\n"%(operand, packed_width - 1, )
            packings["single_zero"] = "input_%i_single_zero"%(operand, )

            LSB = 0
            MSB = LSB + gen_det.config["data_width"]
            com_det.arch_body += "input_%i_single_zero(%i downto %i) <= input_%i_0_source;\n"%(operand, MSB - 1, LSB, operand, )
            LSB = MSB

            word = 1
            sel_bit = 0
            while word < operand_details["packings"]["single_zero"]:
                for _ in range(word):
                    com_det.arch_body += "input_%i_single_zero(%i) <= '0';\n"%(operand, LSB, )
                    LSB += 1

                    MSB = LSB + gen_det.config["data_width"]

                    com_det.arch_body += "input_%i_single_zero_word_%i_mux : entity work.%s(arch)\>\n"%(operand, word, mux_2, )

                    com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"], )

                    com_det.arch_body += "port map (\n\>"

                    com_det.arch_body += "sel(0) => input_%i_block_size_sel(%i),\n"%(operand, sel_bit, )

                    com_det.arch_body += "data_in_0 => (others => '0'),\n"
                    com_det.arch_body += "data_in_1 => input_%i_%i_source,\n"%(operand, word, )

                    com_det.arch_body += "data_out  => input_%i_single_zero(%i downto %i)\n"%(operand, MSB - 1, LSB, )

                    com_det.arch_body += "\<);\n\<\n"

                    LSB = MSB
                    word += 1
                sel_bit += 1
            if packed_width > LSB:
                com_det.arch_body += "input_%i_single_zero(%i downto %i) <= (others => '0');\n"%(operand, packed_width - 1, LSB, )
            com_det.arch_body += "\n"
        # Handle packings mux
        com_det.add_port("result_%i"%(operand, ), "std_logic_vector", "out", packed_width)
        if len(packings) == 1:
            com_det.arch_body += "result_%i <= %s;\n\n"%(operand, list(packings.values())[0], )
        else:
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs"  : len(packings),
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            com_det.arch_body += "input_%i_packing_mux : entity work.%s(arch)\>\n"%(operand, mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(packed_width, )

            com_det.arch_body += "port map (\n\>"

            com_det.add_port("input_%i_packing_sel"%(operand, ), "std_logic_vector", "in", mux_interface["sel_width"])
            com_det.arch_body += "sel => input_%i_packing_sel ,\n"%(operand, )

            sel_map = {}
            for sel_val, (packing_type, packed_signal) in enumerate(packings.items()):
                com_det.arch_body += "data_in_%i => %s,\n"%(sel_val, packed_signal, )
                sel_map[packing_type] = sel_val
            com_det.add_interface_item("input_%i_packing_map"%(operand, ), sel_map)

            for input in range(len(packings), mux_interface["number_inputs"]):
                com_det.arch_body += "data_in_%i => (others => 'U'),\n"%(input, )

            com_det.arch_body += "data_out  => result_%i \n"%(operand, )

            com_det.arch_body += "\<);\n\<\n"
