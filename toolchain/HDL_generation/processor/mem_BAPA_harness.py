# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import itertools as it
import math
import re

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import demux

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    config["num_blocks"] = 1
    config["reads"] = []
    config["writes"] = []

    for instr in instr_set:
        read = 0
        for access in asm_utils.instr_fetches(instr):
            if asm_utils.access_mem(access) == instr_id:
                mods = asm_utils.access_mods(access)
                if "BAPA" in mods.keys():
                    BAPA_factor = int(mods["BAPA"])
                    config["num_blocks"] = max(config["num_blocks"],BAPA_factor)
                else:
                    BAPA_factor = 1

                try:
                    config["reads"][read]["min"] = min(config["reads"][read]["min"], BAPA_factor)
                    config["reads"][read]["max"] = max(config["reads"][read]["max"], BAPA_factor)
                except IndexError:
                    config["reads"].append({
                        "min" : BAPA_factor,
                        "max" : BAPA_factor,
                    })

                read += 1

        write = 0
        for access in asm_utils.instr_stores(instr):
            if asm_utils.access_mem(access) == instr_id:
                mods = asm_utils.access_mods(access)
                if "BAPA" in mods.keys():
                    BAPA_factor = int(mods["BAPA"])
                    config["num_blocks"] = max(config["num_blocks"],BAPA_factor)
                else:
                    BAPA_factor = 1

                try:
                    config["writes"][write]["min"] = min(config["writes"][write]["min"], BAPA_factor)
                    config["writes"][write]["max"] = max(config["writes"][write]["max"], BAPA_factor)
                except IndexError:
                    config["writes"].append({
                        "min" : BAPA_factor,
                        "max" : BAPA_factor,
                    })

                write += 1

    return config

read_addr_patern = re.compile("read_(\d+)_addr")
read_data_patern = re.compile("read_(\d+)_word_(\d+)")
write_addr_patern = re.compile("write_(\d+)_addr")
write_data_patern = re.compile("write_(\d+)_word_(\d+)")

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()


    # Gather pathway ports
    read_addr_ports = []
    read_data_ports = []
    write_addr_ports = []
    write_data_ports = []
    for port in interface["ports"]:
        match = read_addr_patern.fullmatch(port)
        if match:
            read_addr_ports.append(int(match.group(1)))
            continue

        match = read_data_patern.fullmatch(port)
        if match:
            read_data_ports.append( (int(match.group(1)), int(match.group(2)), ) )
            continue

        match = write_addr_patern.fullmatch(port)
        if match:
            write_addr_ports.append(int(match.group(1)))
            continue

        match = write_data_patern.fullmatch(port)
        if match:
            write_data_ports.append( (int(match.group(1)), int(match.group(2)), ) )
            continue

    # Loop over all instructions and generate paths for all found pathway ports
    for instr in instr_set:
        fetches = asm_utils.instr_fetches(instr)
        reads   = [fetch for fetch, access in enumerate(fetches) if asm_utils.access_mem(access) == instr_id ]
        stores = asm_utils.instr_stores(instr)
        writes = [store for store, access in enumerate(stores) if asm_utils.access_mem(access) == instr_id ]

        # Handle read_addr_ports
        for read in read_addr_ports:
            if read < len(reads):
                fetch = reads[read]
                dataMesh.connect_sink(sink="%sread_%i_addr"%(instr_prefix, read, ),
                    channel="%sfetch_addr_%i"%(lane, fetch, ),
                    condition=instr,
                    stage="fetch", inplace_channel=True,
                    padding_type="unsigned", width=config["addr_width"]
                )

        # Handle read_data_ports
        for read, word in read_data_ports:
            if read < len(reads):
                fetch = reads[read]
                read_mods = asm_utils.access_mods(fetches[fetch])
                if word == 0 or "BAPA" in read_mods and word < int(read_mods["BAPA"]):
                    dataMesh.connect_driver(driver="%sread_%i_word_%i"%(instr_prefix, read, word, ),
                        channel="%sfetch_data_%i_word_%i"%(lane, fetch, word, ),
                        condition=instr,
                        stage="exe", inplace_channel=True,
                        padding_type=config["signal_padding"], width=config["data_width"]
                    )


        # Handle write_data_ports
        for write in write_addr_ports:
            if write < len(writes):
                store = writes[write]
                dataMesh.connect_sink(sink="%swrite_%i_addr"%(instr_prefix, write, ),
                    channel="%sstore_addr_%i"%(lane, store, ),
                    condition=instr,
                    stage="store", inplace_channel=True,
                    padding_type="unsigned", width=config["addr_width"]
                )


        # Handle write_data_ports
        for write, word in write_data_ports:
            if write < len(writes):
                store = writes[write]
                write_mods = asm_utils.access_mods(stores[store])
                if word == 0 or "BAPA" in write_mods and word < int(write_mods["BAPA"]):
                    dataMesh.connect_sink(sink="%swrite_%i_word_%i"%(instr_prefix, write, word, ),
                        channel="%sstore_data_%i_word_%i"%(lane, store, word, ),
                        condition=instr,
                        stage="store", inplace_channel=True,
                        padding_type=config["signal_padding"], width=config["data_width"]
                    )


    return dataMesh

write_enable_pattern = re.compile("write_(\d+)_enable_(\d+)")

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle write_enable_controls
    for port in interface["ports"]:
        match = write_enable_pattern.fullmatch(port)
        if match:
            write = int(match.group(1))
            block_size = int(match.group(2))

            values = { "0" : [], "1" : [], }
            for instr in instr_set:
                writes = [ store for store in asm_utils.instr_stores(instr) if asm_utils.access_mem(store) == instr_id ]
                write_mods = [asm_utils.access_mods(store) for store in writes]

                # none parallel access
                if block_size == 1 and len(writes) > write and not ( len(write_mods) > write and "BAPA" in write_mods[write].keys()):
                    values["1"].append(instr)
                # parallel access
                elif len(write_mods) > write and "BAPA" in write_mods[write].keys() and int(write_mods[write]["BAPA"]) == block_size:
                    values["1"].append(instr)
                else:
                    values["0"].append(instr)
            gen_utils.add_control(controls, "store", instr_prefix + "write_%i_enable_%i"%(write, block_size), values, "std_logic")
    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["num_blocks"]) == int, "num_blocks must be an int"
    assert config_in["num_blocks"] > 0, "num_blocks must be greater than 0"
    assert math.log(config_in["num_blocks"], 2) % 1 == 0, "num_blocks must be a power of 2"
    config_out["num_blocks"] = config_in["num_blocks"]

    assert type(config_in["reads"]) == list, "reads must be a list"
    assert len(config_in["reads"]) > 0, "reads cab't be empty"
    config_out["reads"] = []
    for index, details in enumerate(config_in["reads"]):
        assert type(details["min"]) == int, "min must be an int"
        assert details["min"] > 0, "min must be greater than 0"
        assert math.log(details["min"], 2) % 1 == 0, "min must be a power of 2"

        assert type(details["max"]) == int, "max must be an int"
        assert details["max"] > 0, "max must be greater than 0"
        assert math.log(details["max"], 2) % 1 == 0, "max must be a power of 2"

        assert details["max"] >- details["min"], "max must be greater than or equal min"

        config_out["reads"].append( {
            "min" : details["min"],
            "max" : details["max"],
        } )

    assert type(config_in["writes"]) == list, "writes must be a list"
    config_out["writes"] = []
    for index, details in enumerate(config_in["writes"]):
        assert type(details["min"]) == int, "min must be an int"
        assert details["min"] > 0, "min must be greater than 0"
        assert math.log(details["min"], 2) % 1 == 0, "min must be a power of 2"

        assert type(details["max"]) == int, "max must be an int"
        assert details["max"] > 0, "max must be greater than 0"
        assert math.log(details["max"], 2) % 1 == 0, "max must be a power of 2"

        assert details["max"] >- details["min"], "max must be greater than or equal min"

        config_out["writes"].append( {
            "min" : details["min"],
            "max" : details["max"],
        } )

    assert type(config_in["stallable"]) == bool, "stallable must be a bool"
    config_out["stallable"] = config_in["stallable"]

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

        com_det.add_generic("data_width", "integer")
        com_det.add_generic("block_addr_width", "integer")

        com_det.add_port("clock", "std_logic", "in")

        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_head += "signal stall : std_logic;\n"
            com_det.arch_body += "stall <= stall_in;\n"

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Generation Module Code
        gen_reads(gen_det, com_det)
        gen_writes(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_reads(gen_det, com_det):

    # Generate 2 input mux for mux tree(s)
    mux_interface, mux_name = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # Generate registor to act a output buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force"  : False,
            "has_sync_force"   : False,
            "has_enable"    : gen_det.config["stallable"],
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    block_addr_bits = int(math.log(gen_det.config["num_blocks"], 2))

    for read, details in enumerate(gen_det.config["reads"]):
        lg_min = int(math.log(details["min"], 2))
        lg_max = int(math.log(details["max"], 2))

        # Handle addr ports
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector(block_addr_width + %i downto 0)"%(block_addr_bits - 1, ), "in")

        for block in range(gen_det.config["num_blocks"]):
            com_det.add_port("block_%i_read_%i_addr"%(block, read, ), "std_logic_vector(block_addr_width - 1 downto 0)", "out")
            com_det.arch_body += "block_%i_read_%i_addr <= read_%i_addr(read_%i_addr'left downto %i);\n"%(block, read, read, read, block_addr_bits,)

        com_det.arch_body += "\n"


        # Handle data ports
        for word in range(details["max"]):
            com_det.add_port("read_%i_word_%i"%(read, word,), "std_logic_vector(data_width - 1 downto 0)", "out")
            com_det.arch_head += "signal read_%i_word_%i_reg_in : std_logic_vector(data_width - 1 downto 0);\n"%(read, word,)

            com_det.arch_body += " read_%i_word_%i_reg : entity work.%s(arch)@>\n"%(read, word, reg_name)
            com_det.arch_body += "generic map (data_width => data_width)\n"
            com_det.arch_body += "port map (\n@>"
            com_det.arch_body += "clock => clock,\n"
            if gen_det.config["stallable"]:
                com_det.arch_body += "enable  => not stall,\n"
            com_det.arch_body += "data_in  => read_%i_word_%i_reg_in,\n"%(read, word,)
            com_det.arch_body += "data_out => read_%i_word_%i\n"%(read, word,)
            com_det.arch_body += "@<);\n@<\n"

        com_det.arch_body += "\n"

        for block in range(gen_det.config["num_blocks"]):
            com_det.add_port("block_%i_read_%i_data"%(block, read, ), "std_logic_vector(data_width - 1 downto 0)", "in")

        ###########################################################################################
        # Generate the mux tree(s) for this read
        # To decrease the number of muxes used the mux tree(s) is(are) arranged with
        # With the addr's MSBs used at the leaves with the addr bit becoming less sif.
        # Towards the root(s). This enables all read to be pulled from the same mux
        # tree(S), instead of requiring a tree per word.
        # The reason for the strange plaralization is that when BAPR_min is greater than one
        # root muxed are omitted to reduce mux usage, this leads to what eould have been a
        # signal tree being split into subtrees
        ###########################################################################################
        mux_tree_signals = { block_addr_bits : [ "block_%i_read_%i_data"%(block, read, ) for block in range(gen_det.config["num_blocks"]) ], }

        for addr_bit in reversed(range(lg_min, block_addr_bits)):
            num_muxes = int(len(mux_tree_signals[addr_bit + 1])/2)
            mux_tree_signals[addr_bit] = []
            for mux_index in range(num_muxes):
                # Create new tree datasignal
                com_det.arch_head += "signal read_%i_mux_%i_%i_out : std_logic_vector(data_width - 1 downto 0);\n"%(read, addr_bit, mux_index, )
                mux_tree_signals[addr_bit].append("read_%i_mux_%i_%i_out"%(read, addr_bit, mux_index, ))

                # Instancate mux
                com_det.arch_body += "read_%i_mux_%i_%i : entity work.%s(arch)@>\n"%(read, addr_bit, mux_index, mux_name, )

                com_det.arch_body += "generic map (data_width => data_width)\n"

                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => read_%i_addr(%i),\n"%(read, addr_bit, )
                com_det.arch_body += "data_in_0 => %s,\n"%(mux_tree_signals[addr_bit + 1][mux_index], )
                com_det.arch_body += "data_in_1 => %s,\n"%(mux_tree_signals[addr_bit + 1][mux_index + num_muxes], )
                com_det.arch_body += "data_out => read_%i_mux_%i_%i_out\n"%(read, addr_bit, mux_index, )

                com_det.arch_body += "@<);\n@<\n"

        # Connect up root(s) for mux tree
        start_word = 0
        for stage, lg_end_word in enumerate(range(lg_min, lg_max + 1)):
            end_word = 2 ** lg_end_word
            for word in range(start_word, end_word):
                com_det.arch_body += "read_%i_word_%i_reg_in <= %s;\n"%(read, word, mux_tree_signals[lg_min + stage][word])
            start_word = end_word

        com_det.arch_body += "\n\n"

def gen_writes(gen_det, com_det):
    # Generate 2 input mux for mux tree(s)
    mux_interface, mux_name = mux.generate_HDL(
        {
            "inputs"  : 2,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    block_addr_bits = int(math.log(gen_det.config["num_blocks"], 2))

    for write, details in enumerate(gen_det.config["writes"]):
        lg_min = int(math.log(details["min"], 2))
        lg_max = int(math.log(details["max"], 2))

        # Handle addr ports
        com_det.add_port("write_%i_addr"%(write, ), "std_logic_vector(block_addr_width + %i downto 0)"%(block_addr_bits - 1, ), "in")

        for block in range(gen_det.config["num_blocks"]):
            com_det.add_port("block_%i_write_%i_addr"%(block, write, ), "std_logic_vector(block_addr_width - 1 downto 0)", "out")
            com_det.arch_body += "block_%i_write_%i_addr <= write_%i_addr(write_%i_addr'left downto %i);\n"%(block, write, write, write, block_addr_bits,)

        com_det.arch_body += "\n"

        # Handle write enables ports
        enable_demux_signals = {}
        for lg_block_size in range(lg_min, lg_max + 1):
            block_size = 2 ** lg_block_size
            com_det.add_port("write_%i_enable_%i"%(write, block_size, ), "std_logic", "in")

            num_regions = int(gen_det.config["num_blocks"]/block_size)

            if num_regions == 1:
                enable_demux_signals[block_size] = ["write_%i_enable_%i"%(write, block_size, ), ]
            else:
                enable_demux_signals[block_size] = []

                demux_interface, demux_name = demux.generate_HDL(
                    {
                        "outputs"  : num_regions,
                    },
                    output_path=gen_det.output_path,
                    module_name=None,
                    concat_naming=False,
                    force_generation=gen_det.force_generation
                )

                # Instancate demux
                com_det.arch_body += "write_%i_enable_%i_demux : entity work.%s(arch)@>\n"%(write, block_size, demux_name, )

                com_det.arch_body += "generic map (data_width => 1)\n"

                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel => write_%i_addr(%i downto %i),\n"%(write, lg_block_size + int(math.log(num_regions, 2)) - 1, lg_block_size, )
                com_det.arch_body += "data_in(0) => write_%i_enable_%i,\n"%(write, block_size, )

                for region in range(num_regions):
                    com_det.arch_head += "signal write_%i_enable_%i_demux_out_%i : std_logic;\n"%(write, block_size, region, )
                    com_det.arch_body += "data_out_%i(0) => write_%i_enable_%i_demux_out_%i,\n"%(region, write, block_size, region, )

                    enable_demux_signals[block_size].append("write_%i_enable_%i_demux_out_%i"%(write, block_size, region, ) )

                com_det.arch_body.drop_last(2)
                com_det.arch_body += "\n@<);\n@<\n"

        for block in range(gen_det.config["num_blocks"]):
            com_det.add_port("block_%i_write_%i_enable"%(block, write, ), "std_logic", "out")
            normalized_block = block/gen_det.config["num_blocks"]
            terms = []
            for lg_block_size in range(lg_min, lg_max + 1):
                block_size = 2 ** lg_block_size
                index = math.floor(normalized_block*len(enable_demux_signals[block_size]))
                terms.append(enable_demux_signals[block_size][index])
            com_det.arch_body += "block_%i_write_%i_enable <= %s;\n"%(block, write, " or ".join(terms))

        # Handle data ports
        for word in range(details["max"]):
            com_det.add_port("write_%i_word_%i"%(write, word,), "std_logic_vector(data_width - 1 downto 0)", "in")

        for block in range(gen_det.config["num_blocks"]):
            com_det.add_port("block_%i_write_%i_data"%(block, write, ), "std_logic_vector(data_width - 1 downto 0)", "out")

        # Generate mux chain(s)
        mux_chain_sel_terms = ["write_%i_enable_%i"%(write, 2**lg_block_size, ) for lg_block_size in range(lg_min + 1, lg_max + 1) ]
        mux_chain_signals = [ ]
        for  word in range(details["min"]):
            com_det.arch_head += "signal write_%i_word_%i_muxed : std_logic_vector(data_width - 1 downto 0);\n"%(write, word, )
            com_det.arch_body += "write_%i_word_%i_muxed <=  write_%i_word_%i;\n"%(write, word, write, word, )
            mux_chain_signals.append("write_%i_word_%i_muxed"%(write, word, ))

        block_size = details["min"]
        while block_size < gen_det.config["num_blocks"]:
            for index in range(block_size):
                word = index + block_size
                if len(mux_chain_sel_terms) > 0:
                    # Instancate mux
                    com_det.arch_head += "signal write_%i_word_%i_muxed : std_logic_vector(data_width - 1 downto 0);\n"%(write, word, )

                    com_det.arch_body += "write_%i_word_%i_mux : entity work.%s(arch)@>\n"%(write, word, mux_name, )

                    com_det.arch_body += "generic map (data_width => data_width)\n"

                    com_det.arch_body += "port map (\n@>"
                    com_det.arch_body += "sel(0) => %s,\n"%(" or ".join(mux_chain_sel_terms), )
                    com_det.arch_body += "data_in_0 => %s,\n"%(mux_chain_signals[index], )
                    com_det.arch_body += "data_in_1 => write_%i_word_%i,\n"%(write, word, )
                    com_det.arch_body += "data_out => write_%i_word_%i_muxed\n"%(write, word, )

                    com_det.arch_body += "@<);\n@<\n"

                    mux_chain_signals.append("write_%i_word_%i_muxed"%(write, word, ))
                else:
                    mux_chain_signals.append(mux_chain_signals[index])

            # Double block_size to step thought the powers of 2
            block_size *= 2
            # Drop smallest block size from sel signal as it has been handled
            try:
                mux_chain_sel_terms.pop(0)
            # Catch and kill indexError which arises from there a larger wrtie blocks then write block
            # Eg a mem written to in signal words before read in large blocks
            except IndexError:
                pass


        # Generate up output of mux chain(s)
        for block, signal in zip(range(gen_det.config["num_blocks"]), it.cycle(mux_chain_signals)):
            com_det.arch_body += "block_%i_write_%i_data <= %s;\n"%(block, write, signal, )
