# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import math
import itertools as it
import re

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

def add_inst_config(instr_id, instr_set, config, reads, writes, min_read, max_read, min_write, max_write):
    packing_factor = max(max_read, max_write)

    return {
        "type" : "packed",
        "reads"  : reads,
        "writes" : writes,
        "stallable" : config["stallable"],
        "packing_factor" : packing_factor,
        "pipelined_writes" : config["pipelined_writes"] and max_read > max_write,
        "wrapped_mems" : {
            "num_blocks" : 1,
            "data_width" : (config["data_width"] * packing_factor),
            "depth" : math.ceil(config["depth"] / packing_factor),
        }
    }

read_addr_patern = re.compile("read_(\d+)_addr")
read_data_patern = re.compile("read_(\d+)_word_(\d+)")
write_addr_patern = re.compile("write_(\d+)_addr")
write_data_patern = re.compile("write_(\d+)_word_(\d+)")

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

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
                gen_utils.add_datapath_dest(pathways, "%sfetch_addr_%i"%(lane, fetch, ), "fetch", instr, "%sread_%i_addr"%(instr_prefix, read, ), "unsigned", config["addr_width"])

        # Handle read_data_ports
        for read, word in read_data_ports:
            if read < len(reads):
                fetch = reads[read]
                read_mods = asm_utils.access_mods(fetches[fetch])
                if word == 0 or "BAPA" in read_mods and word < int(read_mods["BAPA"]):
                    gen_utils.add_datapath_source(pathways, "%sfetch_data_%i_word_%i"%(lane, fetch, word, ), "exe", instr, "%sread_%i_word_%i"%(instr_prefix, read, word, ), config["signal_padding"], config["data_width"])



    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "type" in config_in.keys()
    assert config_in["type"] == "packed"

    assert "pipelined_writes" in config_in.keys()
    assert type(config_in["pipelined_writes"]) == bool
    config_out["pipelined_writes"] = config_in["pipelined_writes"]


    assert "packing_factor" in config_in.keys()
    assert type(config_in["packing_factor"]) == int
    assert config_in["packing_factor"] > 0
    # Maybe add po2 check
    config_out["packing_factor"] = config_in["packing_factor"]
    config_out["BAPA_addr_bits"] = int(math.log(config_out["packing_factor"], 2))


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

    config_out["wrapped_mems"] = {}

    assert "num_blocks" in config_in["wrapped_mems"].keys()
    assert type(config_in["wrapped_mems"]["num_blocks"]) == int
    assert config_in["wrapped_mems"]["num_blocks"] > 0
    config_out["wrapped_mems"]["num_blocks"] = config_in["wrapped_mems"]["num_blocks"]

    assert "data_width" in config_in["wrapped_mems"].keys()
    assert type(config_in["wrapped_mems"]["data_width"]) == int
    assert config_in["wrapped_mems"]["data_width"] > 0
    config_out["wrapped_mems"]["data_width"] = config_in["wrapped_mems"]["data_width"]

    assert "depth" in config_in["wrapped_mems"].keys()
    assert type(config_in["wrapped_mems"]["depth"]) == int
    assert config_in["wrapped_mems"]["depth"] > 0
    config_out["wrapped_mems"]["depth"] = config_in["wrapped_mems"]["depth"]

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
        com_det.add_generic("data_width", "integer")
        com_det.add_generic("block_addr_width", "integer")

        com_det.add_port("clock", "std_logic", "in")

        com_det.add_interface_item("BAPA_addr_bits", gen_det.config["BAPA_addr_bits"])

        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")
            com_det.arch_head += "signal stall : std_logic;\n"
            com_det.arch_body += "stall <= stall_in;\n"
            com_det.add_import("ieee", "std_logic_1164", "all")


        gen_det, com_det = handle_reads(gen_det, com_det)
        gen_det, com_det = gen_writes(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def handle_reads(gen_det, com_det):
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

    for read, details in enumerate(gen_det.config["reads"]):
        lg_min = int(math.log(details["min"], 2))
        lg_max = int(math.log(details["max"], 2))


        # Handle addr ports
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector(block_addr_width + %i - 1 downto 0)"%(gen_det.config["BAPA_addr_bits"], ), "in")
        com_det.add_port("block_0_read_%i_addr"%(read, ), "std_logic_vector(block_addr_width - 1 downto 0)", "out")

        com_det.arch_body += "block_0_read_%i_addr <= read_%i_addr(read_%i_addr'left downto %i);\n"%(read, read, read, gen_det.config["BAPA_addr_bits"],)

        com_det.arch_body += "\n"

        # Handle data ports
        for word in range(details["max"]):
            com_det.add_port("read_%i_word_%i"%(read, word,), "std_logic_vector(data_width - 1 downto 0)", "out")
            com_det.arch_head += "signal read_%i_word_%i_reg_in : std_logic_vector(data_width - 1 downto 0);\n"%(read, word,)

            com_det.arch_body += " read_%i_word_%i_reg : entity work.%s(arch)\>\n"%(read, word, reg_name)
            com_det.arch_body += "generic map (data_width => data_width)\n"
            com_det.arch_body += "port map (\n\>"
            com_det.arch_body += "clock => clock,\n"
            if gen_det.config["stallable"]:
                com_det.arch_body += "enable  => not stall,\n"
            com_det.arch_body += "data_in  => read_%i_word_%i_reg_in,\n"%(read, word,)
            com_det.arch_body += "data_out => read_%i_word_%i\n"%(read, word,)
            com_det.arch_body += "\<);\n\<\n"

        com_det.arch_body += "\n"

        com_det.add_port("block_0_read_%i_data"%(read, ), "std_logic_vector(%i * data_width - 1 downto 0)"%(gen_det.config["packing_factor"], ), "in")

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

        leftmost = gen_det.config["packing_factor"]
        mux_tree_signals = {
            gen_det.config["BAPA_addr_bits"] :
                [
                    "block_0_read_%i_data(%i * data_width - 1 downto %i * data_width)"%(
                        read,
                        leftmost - word,
                        leftmost - word - 1,
                    ) for word in range(gen_det.config["packing_factor"])
                ],
        }

        for addr_bit in reversed(range(lg_min, gen_det.config["BAPA_addr_bits"])):
            num_muxes = int(len(mux_tree_signals[addr_bit + 1])/2)
            mux_tree_signals[addr_bit] = []
            for mux_index in range(num_muxes):
                # Create new tree datasignal
                com_det.arch_head += "signal read_%i_mux_%i_%i_out : std_logic_vector(data_width - 1 downto 0);\n"%(read, addr_bit, mux_index, )
                mux_tree_signals[addr_bit].append("read_%i_mux_%i_%i_out"%(read, addr_bit, mux_index, ))

                # Instancate mux
                com_det.arch_body += "read_%i_mux_%i_%i : entity work.%s(arch)\>\n"%(read, addr_bit, mux_index, mux_name, )

                com_det.arch_body += "generic map (data_width => data_width)\n"

                com_det.arch_body += "port map (\n\>"
                com_det.arch_body += "sel(0) => read_%i_addr(%i),\n"%(read, addr_bit, )
                com_det.arch_body += "data_in_0 => %s,\n"%(mux_tree_signals[addr_bit + 1][mux_index], )
                com_det.arch_body += "data_in_1 => %s,\n"%(mux_tree_signals[addr_bit + 1][mux_index + num_muxes], )
                com_det.arch_body += "data_out => read_%i_mux_%i_%i_out\n"%(read, addr_bit, mux_index, )

                com_det.arch_body += "\<);\n\<\n"

        # Connect up root(s) for mux tree
        start_word = 0
        for stage, lg_end_word in enumerate(range(lg_min, lg_max + 1)):
            end_word = 2 ** lg_end_word
            for word in range(start_word, end_word):
                com_det.arch_body += "read_%i_word_%i_reg_in <= %s;\n"%(read, word, mux_tree_signals[lg_min + stage][word])
            start_word = end_word

        com_det.arch_body += "\n\n"

    return gen_det, com_det

def gen_writes(gen_det, com_det):
    for write, details in enumerate(gen_det.config["writes"]):
        lg_min = int(math.log(details["min"], 2))
        lg_max = int(math.log(details["max"], 2))

        # Handle addr ports
        com_det.add_port("write_%i_addr"%(write, ), "std_logic_vector(block_addr_width + %i - 1 downto 0)"%(gen_det.config["BAPA_addr_bits"], ), "in")
        com_det.add_port("block_0_write_%i_addr"%(write, ), "std_logic_vector(block_addr_width - 1 downto 0)", "out")

        com_det.arch_body += "block_0_write_%i_addr <= write_%i_addr(write_%i_addr'left downto %i);\n"%(write, write, write, gen_det.config["BAPA_addr_bits"],)

        com_det.arch_body += "\n"


        # Handle data ports
        for word in range(details["max"]):
            com_det.add_port("write_%i_word_%i"%(write, word,), "std_logic_vector(data_width - 1 downto 0)", "in")
        com_det.add_port("block_0_write_%i_data"%(write, ), "std_logic_vector(%i * data_width - 1 downto 0)"%(gen_det.config["packing_factor"], ), "out")

        if not gen_det.config["pipelined_writes"]:
            assert details["min"] == details["max"] and details["max"] == gen_det.config["packing_factor"]
            com_det.arch_body += "block_0_write_%i_data <= %s;\n"%(write, " & ".join(["write_%i_word_%i"%(write, word,) for word in range(gen_det.config["packing_factor"]) ]), )

            # Handle enables ports
            com_det.add_port("block_0_write_%i_enable"%(write, ), "std_logic", "out")
            com_det.add_port("write_%i_enable_%i"%(write, details["max"]), "std_logic", "in")
            com_det.arch_body += "block_0_write_%i_enable <= write_%i_enable_%i;\n"%(write, write, gen_det.config["packing_factor"], )
        else:
            raise NotImplementedEroor()


    return gen_det, com_det
