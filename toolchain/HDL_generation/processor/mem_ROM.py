# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re
import math
import copy

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import dist_ROM
from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import mux

from FPE.toolchain.HDL_generation.processor  import mem_BAPA_harness

from warnings import warn

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    BAPA_used = False

    reads = 0
    for instr in instr_set:
        count = 0
        for access in asm_utils.instr_fetches(instr):
            if asm_utils.access_mem(access) == instr_id:
                count += 1

                if "BAPA" in asm_utils.access_mods(access):
                    BAPA_used = True
        reads = max(reads, count)

    config["buffer_reads"] = True
    config["reads"] = reads
    if BAPA_used:
        config["BAPA"] = mem_BAPA_harness.add_inst_config(instr_id, instr_set, { "stallable" : config["stallable"] })


    return config

read_addr_patern = re.compile("read_(\\d+)_addr")
read_data_patern = re.compile("read_(\\d+)_data")

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    if "BAPA" in config.keys():
        dataMesh = mem_BAPA_harness.get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane)
    else:
        # Gather pathway ports
        read_addr_ports = []
        read_data_ports = []
        for port in interface["ports"]:
            match = read_addr_patern.fullmatch(port)
            if match:
                read_addr_ports.append(int(match.group(1)))
                continue

            match = read_data_patern.fullmatch(port)
            if match:
                read_data_ports.append(int(match.group(1)))
                continue


        # Loop over all instructions and add found dataMesh ports
        for instr in instr_set:
            reads = [fetch for fetch, access in enumerate(asm_utils.instr_fetches(instr)) if asm_utils.access_mem(access) == instr_id ]

            # Handle read_addr_port
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
            for read in read_data_ports:
                if read < len(reads):
                    fetch = reads[read]
                    dataMesh.connect_driver(driver="%sread_%i_data"%(instr_prefix, read, ),
                        channel="%sfetch_data_%i_word_0"%(lane, fetch, ),
                        condition=instr,
                        stage="exe", inplace_channel=True,
                        padding_type=config["signal_padding"], width=config["data_width"]
                    )

    return dataMesh

write_enables_pattern = re.compile("write_(\\d+)_enable")

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    if "BAPA" in config.keys():
        controls = mem_BAPA_harness.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    else:
        pass

    return controls


#####################################################################

possible_BRAMs = [
    {
        "width" : 1,
        "depth" : 16 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 2,
        "depth" : 8 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 4,
        "depth" : 4 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 9,
        "depth" : 2 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    },
    {
        "width" : 18,
        "depth" : 1 * 2 ** 10,
        "total_mem" : 18 * 2 ** 10,
        "primitive"  : "RAMB18E1"
    }
]

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["stallable"]) == bool, "stallable must be a boolean"
    config_out["stallable"] = config_in["stallable"]

    assert type(config_in["reads"]) == int, "reads must be an int"
    assert config_in["reads"] > 0., "reads must be greater than 0"
    config_out["reads"] = config_in["reads"]

    assert type(config_in["buffer_reads"]) == bool, "buffer_reads must be a bool"
    config_out["buffer_reads"] = config_in["buffer_reads"]

    if "BAPA" in config_in.keys():
        if __debug__: mem_BAPA_harness.preprocess_config(config_in["BAPA"])
        config_out["BAPA"] = config_in["BAPA"]

    # Check data type
    assert(type(config_in["type"]) == type(""))
    assert(config_in["type"] in ["DIST", "BLOCK"])
    if   config_in["type"] == "DIST":
        assert(config_in["depth"] >= 1)
        config_out["depth"] = config_in["depth"]
        config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)

        assert(config_in["data_width"] >= 1)
        config_out["data_width"] = config_in["data_width"]
    elif config_in["type"] == "BLOCK":
        assert(config_in["depth"] >= 1)
        assert(config_in["data_width"] >= 1)
        mem_rquired = config_in["depth"] * config_in["data_width"]

        # Check all possible block_sizes and select the most mem effisanct one
        tilings = []
        for BRAM in possible_BRAMs:
            subwords = math.ceil(config_in["data_width"] / BRAM["width"])
            addr_banks = math.ceil(config_in["depth"] / BRAM["depth"])

            total_mem = subwords * addr_banks * BRAM["total_mem"]
            wasted_mem = total_mem - mem_rquired

            tilings.append(
                {
                    "subwords" : subwords,
                    "addr_banks" : addr_banks,
                    "wasted_mem" : wasted_mem,
                    "BRAM_width" : BRAM["width"],
                    "BRAM_depth" : BRAM["depth"],
                    "BRAM_primitive"  : BRAM["primitive"],
                }
            )

        # Filter for lowest wasted_mem, to use less hards
        best_wasted_mem = min([
            tiling["wasted_mem"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["wasted_mem"] == best_wasted_mem
        ]

        # Filter for lowest addr_banks, to save of dataMesh
        lowest_rows = min([
            tiling["addr_banks"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["addr_banks"] == lowest_rows
        ]

        # Filter for lowest subwords, to reduce signal count
        lowest_rows = min([
            tiling["subwords"]
            for tiling in tilings
        ])
        tilings = [
            tiling
            for tiling in tilings
            if tiling["subwords"] == lowest_rows
        ]

        # If multiple options left usage the first one
        tiling = tilings[0]

        config_out["subwords"] = tiling["subwords"]
        config_out["addr_banks"] = tiling["addr_banks"]
        config_out["BRAM_width"] = tiling["BRAM_width"]
        config_out["BRAM_depth"] = tiling["BRAM_depth"]
        config_out["BRAM_primitive"]  = tiling["BRAM_primitive"]
        config_out["BRAM_addr_width"] = tc_utils.unsigned.width(config_out["BRAM_depth"] - 1)

        config_out["data_width"] = tiling["subwords"] * tiling["BRAM_width"]

        config_out["depth"] = tiling["addr_banks"] * tiling["BRAM_depth"]
        config_out["addr_width"] = tc_utils.unsigned.width(config_out["depth"] - 1)
    else:
        raise ValueError("Unknown RAM type, %s"%(config_in["type"], ) )
    config_out["type"] = config_in["type"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "ROM"

        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%id"%(config["depth"], )

        if config["stallable"]:
            generated_name += "_S"
        else:
            generated_name += "_N"

        if config["type"] == "DIST":
            generated_name += "_D"
        elif config["type"] == "BLOCK":
            generated_name += "_B"
        else:
            raise ValueError("Unknown RAM type, %s"%(config_in["type"], ) )

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

        if "BAPA" in gen_det.config.keys():
            com_det.add_port("clock", "std_logic", "in")
            if gen_det.config["stallable"]:
                com_det.add_port("stall_in", "std_logic", "in")
                com_det.arch_head += "signal stall : std_logic;\n"
                com_det.arch_body += "stall <= stall_in;\n"

            gen_BAPA_ROM(gen_det, com_det)
        else:
            gen_ports(gen_det, com_det)

            if   gen_det.config["type"] == "DIST":
                gen_wordwise_distributed_ROM(gen_det, com_det)
            elif gen_det.config["type"] == "BLOCK":
                gen_wordwise_block_ROM(gen_det, com_det)


        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

hardness_fanin_signals = ["clock", "stall_in"]
hardness_ripple_up_addrs = [
    re.compile("read_(\\d+)_addr"),
]
hardness_ripple_up_signals = [
    re.compile("read_(\\d+)_word_(\\d+)"),
]
hardness_internal_signals = [
    re.compile("block_(\\d+)_read_(\\d+)_addr"),
    re.compile("block_(\\d+)_read_(\\d+)_data"),
]

subblock_fanin_signals = ["clock", "stall_in"]
subblock_ripple_up_generics = [
    re.compile("init_mif"),
]
subblock_internal_signals = [
    re.compile("read_(\\d+)_addr"),
    re.compile("read_(\\d+)_data"),
]

def gen_BAPA_ROM(gen_det, com_det):
    # Compute subblock details
    num_subblocks = gen_det.config["BAPA"]["num_blocks"]
    subblock_depth = math.ceil(gen_det.config["depth"]/num_subblocks)
    subblock_addr_width = tc_utils.unsigned.width(subblock_depth - 1)

    subblock_config = copy.deepcopy(gen_det.config)
    # Remove BAPA from subblock_config as BAPA is being handled in this super component
    del subblock_config["BAPA"]
    # overwrite depth
    subblock_config["depth"] = subblock_depth
    # Tell subblock to not buffer its reads, as the BAPA harness handles that in a BAPA mem
    subblock_config["buffer_reads"] = False

    # Generate BAPA harness
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_BAPA_harness"
    else:
        module_name = None

    harness_interface, harness_name = mem_BAPA_harness.generate_HDL(
        config=gen_det.config["BAPA"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    # Instancate BAPA harness
    com_det.arch_body += "BAPA_harness : entity work.%s(arch)@>\n"%(harness_name, )

    com_det.arch_body += "generic map (@>\n"
    com_det.arch_body += "data_width => %i,\n"%(gen_det.config["data_width"], )
    com_det.arch_body += "block_addr_width => %i\n"%(subblock_addr_width, )
    com_det.arch_body += "@<)\n"

    com_det.arch_body += "port map (\n@>"

    # Handle fanin signals
    for signal in hardness_fanin_signals:
        if signal in harness_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(signal, signal)

    # Handle ripple up addrs
    for rule in hardness_ripple_up_addrs:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            width = gen_det.config["addr_width"]
            com_det.add_port(port, "std_logic_vector", details["direction"], width)

            # Connect harness port to rippled port
            if subblock_config["depth"] == 1:
                com_det.arch_body += "%s => \"0\" & %s,\n"%(port, port)
            else:
                com_det.arch_body += "%s => %s,\n"%(port, port)

    # Handle ripple up signals
    for rule in hardness_ripple_up_signals:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            # Handle generic controlled ports
            if details["type"].startswith("std_logic_vector("):
                if details["type"].startswith("std_logic_vector(data_width"):
                    width = gen_det.config["data_width"]
                else:
                    raise ValueError("Unknown std_logic_vector type in harness interface, " + details["type"])

                com_det.add_port(port, "std_logic_vector", details["direction"], width)
            # Ripple up non generic controlled ports untouched
            else:
                com_det.add_port(port, details["type"], details["direction"])

            # Connect harness port to rippled port
            com_det.arch_body += "%s => %s,\n"%(port, port)

    # Handle internal signals
    for rule in hardness_internal_signals:
        for port in [port for port in harness_interface["ports"].keys() if rule.fullmatch(port) ]:
            details = harness_interface["ports"][port]

            # Handle generic controlled ports
            if details["type"].startswith("std_logic_vector("):
                if details["type"].startswith("std_logic_vector(block_addr_width"):
                    width = subblock_addr_width
                elif details["type"].startswith("std_logic_vector(data_width"):
                    width = gen_det.config["data_width"]
                else:
                    raise ValueError("Unknown std_logic_vector type in harness interface, " + details["type"])
            # Handle non generic controlled ports
            else:
                try:
                    width = details["width"]
                except KeyError:
                    width = None

            # Connect harness port to internal signal
            if width == None:
                com_det.arch_head += "signal %s : std_logic;\n"%(port, )
            else:
                com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(port, width - 1, )
            com_det.arch_body += "%s => %s,\n"%(port, port)

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "\n@<);\n@<\n"

    # Generate subblock
    if gen_det.concat_naming :
        module_name = gen_det.module_name + "_subblock"
    else:
        module_name = None

    subblock_interface, subblock_name = generate_HDL(
        config=subblock_config,
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    # Instancate sub blocks
    for subblock in range(num_subblocks):
        com_det.arch_body += "subblock_%i : entity work.%s(arch)@>\n"%(subblock, subblock_name, )

        if len(subblock_interface["generics"]) != 0:
            com_det.arch_body += "generic map (@>\n"

            # Handle ripple up generics
            for rule in subblock_ripple_up_generics:
                for generic in [generic for generic in subblock_interface["generics"].keys() if rule.fullmatch(generic) ]:
                    details = subblock_interface["generics"][generic]

                    ripped_generic = "subblock_%i_%s"%(subblock, generic,)
                    com_det.add_generic(ripped_generic, details["type"])

                    # Connect harness port to rippled port
                    com_det.arch_body += "%s => %s,\n"%(generic, ripped_generic)

            com_det.arch_body.drop_last(2)
            com_det.arch_body += "@<)\n"

        com_det.arch_body += "port map (\n@>"

        # Handle fanin signals
        for signal in subblock_fanin_signals:
            if signal in subblock_interface["ports"]:
                com_det.arch_body += "%s => %s,\n"%(signal, signal)

        # Handle internal signals
        for rule in subblock_internal_signals:
            for port in [port for port in subblock_interface["ports"].keys() if rule.fullmatch(port) ]:
                details = subblock_interface["ports"][port]

                com_det.arch_body += "%s => block_%i_%s,\n"%(port, subblock, port, )


        com_det.arch_body.drop_last(2)
        com_det.arch_body += "\n@<);\n@<\n"


#####################################################################

def gen_ports(gen_det, com_det):

    # Handle common ports
    com_det.add_port("clock", "std_logic", "in")
    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")
        com_det.arch_head += "signal stall : std_logic;\n"
        com_det.arch_body += "stall <= stall_in;\n"

    # Declare read ports
    for read in range(gen_det.config["reads"]):
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector", "in", gen_det.config["addr_width"])
        com_det.add_port("read_%i_data"%(read, ), "std_logic_vector", "out", gen_det.config["data_width"])


def gen_wordwise_distributed_ROM(gen_det, com_det):

    # Generation Module Code
    com_det.add_generic("init_mif", "string")

    if gen_det.config["reads"] <= 3:
        # Generate a basic ROM to handle be having
        rom_interface, rom_name = dist_ROM.generate_HDL(
            {
                "depth" : gen_det.config["depth"],
                "reads" : gen_det.config["reads"],
                "synchronous" : gen_det.config["buffer_reads"],
                "has_enable" : gen_det.config["stallable"],
                "init_type" : "MIF"
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        # Instancate ROM
        com_det.arch_body += "dist_ROM : entity work.%s(arch)@>\n"%(rom_name,)

        com_det.arch_body += "generic map (@>\n"
        com_det.arch_body += "data_width => %i,\n"%(gen_det.config["data_width"], )
        com_det.arch_body += "init_mif => init_mif\n"
        com_det.arch_body += "@<)\n"

        com_det.arch_body += "port map (\n@>"
        if gen_det.config["buffer_reads"]:
            com_det.arch_body += "clock => clock,\n"
        if gen_det.config["stallable"]:
            com_det.arch_body += "read_enable => not stall,\n"

        com_det.arch_body += ",\n".join([
            "read_%i_addr => read_%i_addr,\nread_%i_data => read_%i_data"%(
                read, read, read, read,
            )
            for read in range(gen_det.config["reads"])
        ])
        com_det.arch_body += "@<);\n@<\n"
    else:
        raise NotIMplementedError("Support for 4+ reads does adding")

def gen_wordwise_block_ROM(gen_det, com_det):

    warn("BLOCK type ROMs currently lack a means to init they value, so aren't feactural, but can given area costs")
    com_det.add_import("UNISIM", "vcomponents", "all")

    # Generate BRAM
    if gen_det.config["reads"] <= 2:
        if gen_det.config["BRAM_primitive"] == "RAMB18E1":
            BRAM_HEAD, BRAM_BODY = gen_RAMB18E1(gen_det, gen_det.config["reads"])
        else:
            raise ValueError("Unknown BRAM_primitive, %s"%(str(gen_det.config["BRAM_primitive"]), ) )

        # Generate template code for all subwords in an addr_1ank
        BANK_HEAD = gen_utils.indented_string()
        BANK_BODY = gen_utils.indented_string()

        # Declare bank wide addr and data signals
        for read in range(gen_det.config["reads"]):
            BANK_HEAD += "signal BRAM_bank_BANKNAME_addr_%i : std_logic_vector(%i downto 0);\n"%(
                read,
                gen_det.config["addr_width"] - 1,
            )
            BANK_HEAD += "signal BRAM_bank_BANKNAME_data_%i : std_logic_vector(%i downto 0);\n"%(
                read,
                gen_det.config["data_width"] - 1,
            )

        # Include BRAMs each all subwords
        for subword in range(gen_det.config["subwords"]):
            BANK_HEAD += str(BRAM_HEAD).replace("SUBWORDNAME", str(subword))
            BANK_BODY += str(BRAM_BODY).replace("SUBWORDNAME", str(subword))

            # Connect subword BRAM up the bank width signals
            for read in range(gen_det.config["reads"]):
                if gen_det.config["BRAM_addr_width"] >= 14:
                    BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_addr_%i <= BRAM_bank_BANKNAME_addr_%i(13 downto 0);\n".replace(
                        "SUBWORDNAME", str(subword)
                    )%(read, read, )
                else:
                    BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_addr_%i(13 downto %i) <= BRAM_bank_BANKNAME_addr_%i(%i downto 0);\n".replace(
                        "SUBWORDNAME", str(subword)
                    )%(
                        read,
                        14 - gen_det.config["BRAM_addr_width"],
                        read,
                        gen_det.config["BRAM_addr_width"]  - 1,
                    )
                    BANK_BODY += "BRAM_BANKNAME_SUBWORDNAME_addr_%i(%i downto 0) <= (others => '0');\n\n".replace(
                        "SUBWORDNAME", str(subword)
                    )%(
                        read,
                        14 - gen_det.config["BRAM_addr_width"] - 1,
                    )
                BANK_BODY += "BRAM_bank_BANKNAME_data_%i(%i downto %i) <= BRAM_BANKNAME_SUBWORDNAME_data_%i;\n\n".replace(
                    "SUBWORDNAME", str(subword)
                )%(
                    read,
                    ((subword + 1) * gen_det.config["BRAM_width"]) - 1,
                    (subword * gen_det.config["BRAM_width"]),
                    read,
                )


        # Generate addr_banks as needed
        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs" : 2
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )
        mux_outputs = [[]]
        for bank in range(gen_det.config["addr_banks"]):
            com_det.arch_head += str(BANK_HEAD).replace("BANKNAME", str(bank))
            com_det.arch_body += str(BANK_BODY).replace("BANKNAME", str(bank))

            # Connect up bank's addr ports
            for read in range(gen_det.config["reads"]):
                com_det.arch_body += "BRAM_bank_BANKNAME_addr_%i <= read_%i_addr;\n".replace(
                    "BANKNAME", str(bank)
                )%(read, read, )

            # Connect up bank's data ports
            for read in range(gen_det.config["reads"]):
                com_det.arch_head += "signal banks_BANKNAME_to_BANKNAME_data_%i : std_logic_vector(%i downto 0);\n".replace(
                    "BANKNAME", str(bank)
                )%(
                    read,
                    gen_det.config["data_width"] - 1,
                )
                com_det.arch_body += "banks_BANKNAME_to_BANKNAME_data_%i <= BRAM_bank_BANKNAME_data_%i;\n".replace(
                    "BANKNAME", str(bank)
                )%(read, read, )

            # Add muxs as needed
            mux_outputs[0].append((bank, bank))
            for level in range(len(mux_outputs)):
                if len(mux_outputs[level]) == 2:
                    start_bank_A, end_bank_A = mux_outputs[level][0]
                    start_bank_B, end_bank_B = mux_outputs[level][1]

                    for read in range(gen_det.config["reads"]):
                        com_det.arch_head += "signal banks_%i_to_%i_data_%i : std_logic_vector(%i downto 0);\n"%(
                            start_bank_A,
                            end_bank_B,
                            read,
                            gen_det.config["data_width"]  - 1,
                        )

                        com_det.arch_body += "banks_%i_to_%i_data_%i_muz : entity work.%s(arch)@>\n"%(
                            start_bank_A, end_bank_B, read, mux_name,
                        )

                        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

                        com_det.arch_body += "port map (\n@>"
                        com_det.arch_body += "sel(0) => read_%i_addr(%i),\n"%(read, gen_det.config["BRAM_addr_width"] + level, )
                        com_det.arch_body += "data_in_0 => banks_%i_to_%i_data_%i,\n"%(start_bank_A, end_bank_A, read, )
                        com_det.arch_body += "data_in_1 => banks_%i_to_%i_data_%i,\n"%(start_bank_B, end_bank_B, read, )
                        com_det.arch_body += "data_out => banks_%i_to_%i_data_%i\n"%(start_bank_A, end_bank_B, read, )

                        com_det.arch_body += "@<);\n@<\n"

                    # Update mux mux_outputs
                    mux_outputs[level] = []
                    try:
                        mux_outputs[level + 1].append((start_bank_A, end_bank_B))
                    except IndexError:
                        mux_outputs.append([(start_bank_A, end_bank_B)])

        # Handle imbalances mux trees
        if any([ len(mux_outputs[level]) != 0 for level in range(len(mux_outputs) - 1) ]):
            for level in range(len(mux_outputs)):
                if len(mux_outputs[level]) != 0:
                    start_bank_A, end_bank_A = mux_outputs[level][0]
                    if len(mux_outputs[level]) == 1:
                        start_bank_B = end_bank_A + 1
                        end_bank_B = start_bank_B + end_bank_A - start_bank_A
                    else:
                        assert(len(mux_outputs[level]) == 2)
                        start_bank_B, end_bank_B = mux_outputs[level][1]

                    for read in range(gen_det.config["reads"]):
                        com_det.arch_head += "signal banks_%i_to_%i_data_%i : std_logic_vector(%i downto 0);\n"%(
                            start_bank_A,
                            end_bank_B,
                            read,
                            gen_det.config["data_width"]  - 1,
                        )

                        com_det.arch_body += "banks_%i_to_%i_data_%i_muz : entity work.%s(arch)@>\n"%(
                            start_bank_A, end_bank_B, read, mux_name,
                        )

                        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

                        com_det.arch_body += "port map (\n@>"
                        com_det.arch_body += "sel(0) => read_%i_addr(%i),\n"%(read, gen_det.config["BRAM_addr_width"] + level, )

                        com_det.arch_body += "data_in_0 => banks_%i_to_%i_data_%i,\n"%(start_bank_A, end_bank_A, read, )
                        if len(mux_outputs[level]) == 1:
                            com_det.arch_body += "data_in_1 => (others => 'U'),\n"
                        else:
                            com_det.arch_body += "data_in_1 => banks_%i_to_%i_data_%i,\n"%(start_bank_B, end_bank_B, read, )
                        com_det.arch_body += "data_out => banks_%i_to_%i_data_%i\n"%(start_bank_A, end_bank_B, read, )

                        com_det.arch_body += "@<);\n@<\n"

                    # Update mux mux_outputs
                    mux_outputs[level] = []
                    try:
                        mux_outputs[level + 1].append((start_bank_A, end_bank_B))
                    except IndexError:
                        mux_outputs.append([(start_bank_A, end_bank_B)])
        mux_output = mux_outputs[-1][0]

        if gen_det.config["buffer_reads"]:
            # connect data output to a registor
            reg_interface, reg_name = register.generate_HDL(
                {
                    "has_async_force" : False,
                    "has_sync_force" : False,
                    "has_enable"   : gen_det.config["stallable"],
                    "force_on_init" : False
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            for read in range(gen_det.config["reads"]):
                com_det.arch_body += "read_%i_buffer : entity work.%s(arch)@>\n"%(read, reg_name, )

                com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "clock => clock,\n"
                if gen_det.config["stallable"]:
                    com_det.arch_body += "enable => not stall_in,\n"
                com_det.arch_body += "data_in  => banks_0_to_%i_data_%i,\n"%(mux_output[1], read, )
                com_det.arch_body += "data_out => read_%i_data\n"%(read, )
                com_det.arch_body += "@<);\n@<\n"
        else:
            # connect data output straight to port
            for read in range(gen_det.config["reads"]):
                com_det.arch_body += "read_%i_data <= banks_0_to_%i_data_%i,\n"%(read, mux_output[1], read, )

    else:#gen_det.config["reads"] >= 3
        raise NOtImplementedError("More than 2 reads to a BRAM isn't supported")

def gen_RAMB18E1(gen_det, reads):

    BRAM_HEAD = gen_utils.indented_string()
    BRAM_BODY = gen_utils.indented_string()

    BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME : RAMB18E1\n@>"

    BRAM_BODY += "generic map (@>\n"

    # BRAM_BODY += "\n-- Initialization File: RAM initialization file\n"
    # BRAM_BODY += "INIT_FILE => \"NONE\",\n"

    # BRAM_BODY += "\n-- INITP_00 to INITP_07: Initial contents of parity memory array\n"
    # BRAM_BODY += "INITP_00 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_01 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_02 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_03 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_04 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_05 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_06 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INITP_07 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"

    # BRAM_BODY += "\n-- INIT_00 to INIT_3F: Initial contents of data memory array\n"
    # BRAM_BODY += "INIT_00 => X\"000000000000000000000000000000000000000000000000FEDCBA9876543210\",\n"
    # BRAM_BODY += "INIT_01 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_02 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_03 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_04 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_05 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_06 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_07 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_08 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_09 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_0F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_10 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_11 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_12 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_13 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_14 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_15 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_16 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_17 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_18 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_19 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_1F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_20 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_21 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_22 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_23 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_24 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_25 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_26 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_27 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_28 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_29 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_2F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_31 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_30 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_32 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_33 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_34 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_35 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_36 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_37 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_38 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_39 => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3A => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3B => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3C => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3D => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3E => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"
    # BRAM_BODY += "INIT_3F => X\"0000000000000000000000000000000000000000000000000000000000000000\",\n"

    BRAM_BODY += "\n-- INIT_A, INIT_B: Initial values on output ports\n"
    BRAM_BODY += "INIT_A => X\"00000\",\n"
    BRAM_BODY += "INIT_B => X\"00000\",\n"

    BRAM_BODY += "\n-- DOA_REG, DOB_REG: Optional output register (0 or 1)\n"
    BRAM_BODY += "DOA_REG => 0,\n"
    BRAM_BODY += "DOB_REG => 0,\n"

    BRAM_BODY += "-- RSTREG_PRIORITY_A, RSTREG_PRIORITY_B: Reset or enable priority (\"RSTREG\" or \"REGCE\")\n"
    BRAM_BODY += "RSTREG_PRIORITY_A => \"RSTREG\",\n"
    BRAM_BODY += "RSTREG_PRIORITY_B => \"RSTREG\",\n"

    BRAM_BODY += "-- SRVAL_A, SRVAL_B: Set/reset value for output\n"
    BRAM_BODY += "SRVAL_A => X\"00000\",\n"
    BRAM_BODY += "SRVAL_B => X\"00000\",\n"

    BRAM_BODY += "\n-- Address Collision Mode: \"PERFORMANCE\" or \"DELAYED_WRITE\"\n"
    BRAM_BODY += "RDADDR_COLLISION_HWCONFIG => \"DELAYED_WRITE\",\n"

    BRAM_BODY += "\n-- Collision check: Values (\"ALL\", \"WARNING_ONLY\", \"GENERATE_X_ONLY\" or \"NONE\")\n"
    BRAM_BODY += "SIM_COLLISION_CHECK => \"NONE\",\n"

    BRAM_BODY += "-- WriteMode: Value on output upon a write (\"WRITE_FIRST\", \"READ_FIRST\", or \"NO_CHANGE\")\n"
    BRAM_BODY += "WRITE_MODE_A => \"WRITE_FIRST\",\n"
    BRAM_BODY += "WRITE_MODE_B => \"WRITE_FIRST\",\n"

    BRAM_BODY += "\n-- RAM Mode: \"SDP\" or \"TDP\"\n"
    BRAM_BODY += "RAM_MODE => \"TDP\",\n"

    BRAM_BODY += "\n-- READ_WIDTH_A/B, WRITE_WIDTH_A/B: Read/write width per port\n"
    BRAM_BODY += "READ_WIDTH_A  => %i,\n"%(gen_det.config["BRAM_width"], )
    BRAM_BODY += "READ_WIDTH_B  => %i,\n"%(gen_det.config["BRAM_width"], )
    BRAM_BODY += "WRITE_WIDTH_A => 0,\n"
    BRAM_BODY += "WRITE_WIDTH_B => 0,\n"

    BRAM_BODY += "-- Simulation Device: Must be set to \"7SERIES\" for simulation behavior\n"
    BRAM_BODY += "SIM_DEVICE => \"7SERIES\"\n"

    BRAM_BODY += "@<)\n"



    BRAM_BODY += "port map (@>\n"

    BRAM_BODY += "-- Port A, Read only\n"
    BRAM_BODY += "CLKARDCLK     => clock,\n"

    BRAM_BODY += "WEA           => \"00\",\n"
    if gen_det.config["stallable"]:
        BRAM_BODY += "ENARDEN 		=> not stall_in,\n"
    else:
        BRAM_BODY += "ENARDEN 		=> '1',\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_addr_0 : std_logic_vector(13 downto 0);\n"
    BRAM_BODY += "ADDRARDADDR(13 downto 0)   => BRAM_BANKNAME_SUBWORDNAME_addr_0,\n"

    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_DO_A : std_logic_vector(15 downto 0);\n"
    BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_PO_A : std_logic_vector( 1 downto 0);\n"
    BRAM_BODY += "DOADO         => BRAM_BANKNAME_SUBWORDNAME_DO_A,\n"
    BRAM_BODY += "DOPADOP	 	=> BRAM_BANKNAME_SUBWORDNAME_PO_A,\n"

    BRAM_BODY += "DIADI         => (others => '1'),\n"
    BRAM_BODY += "DIPADIP		=> (others => '1'),\n"

    BRAM_BODY += "REGCEAREGCE 	=> '0',\n"
    BRAM_BODY += "RSTRAMARSTRAM => '0',\n"
    BRAM_BODY += "RSTREGARSTREG => '0',\n"

    if reads == 2:
        BRAM_BODY += "-- Port B, Read only\n"
        BRAM_BODY += "CLKBWRCLK 	=> clock,\n"

        BRAM_BODY += "WEBWE           => \"0000\",\n"
        if gen_det.config["stallable"]:
            BRAM_BODY += "ENBWREN 		=> not stall_in,\n"
        else:
            BRAM_BODY += "ENBWREN 		=> '1',\n"

        BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_addr_1 : std_logic_vector(13 downto 0);\n"
        BRAM_BODY += "ADDRBWRADDR(13 downto 0)   => BRAM_BANKNAME_SUBWORDNAME_addr_1,\n"

        BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_DO_B : std_logic_vector(15 downto 0);\n"
        BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_PO_B : std_logic_vector( 1 downto 0);\n"
        BRAM_BODY += "DOBDO			=> BRAM_BANKNAME_SUBWORDNAME_DO_B,\n"
        BRAM_BODY += "DOPBDOP       => BRAM_BANKNAME_SUBWORDNAME_PO_B,\n"
    else:
        BRAM_BODY += "-- Port B, Unused\n"
        BRAM_BODY += "CLKBWRCLK 	=> '0',\n"

        BRAM_BODY += "WEBWE         => \"0000\",\n"
        BRAM_BODY += "ENBWREN 		=> '0',\n"

        BRAM_BODY += "ADDRBWRADDR	=> (others => '1'),\n"

        BRAM_BODY += "DOBDO			=> open,\n"
        BRAM_BODY += "DOPBDOP       => open,\n"

    BRAM_BODY += "DIBDI			=> (others => '1'),\n"
    BRAM_BODY += "DIPBDIP	    => (others => '1'),\n"

    BRAM_BODY += "REGCEB 		=> '0',\n"
    BRAM_BODY += "RSTRAMB 		=> '0',\n"
    BRAM_BODY += "RSTREGB 		=> '0'\n"


    BRAM_BODY += "@<);\n@<\n"

    for dst, scr  in zip(range(reads), ["A", "B"]):
        BRAM_HEAD += "signal BRAM_BANKNAME_SUBWORDNAME_data_%i : std_logic_vector(%i downto 0);\n"%(
            dst,
            gen_det.config["BRAM_width"] - 1,
        )
        if   gen_det.config["BRAM_width"] ==  1:
            BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_data_%i <= BRAM_BANKNAME_SUBWORDNAME_DO_%s(0 downto 0);\n\n"%(
                dst, scr,
            )
        elif gen_det.config["BRAM_width"] ==  2:
            BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_data_%i <= BRAM_BANKNAME_SUBWORDNAME_DO_%s(1 downto 0);\n\n"%(
                dst, scr,
            )
        elif gen_det.config["BRAM_width"] ==  4:
            BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_data_%i <= BRAM_BANKNAME_SUBWORDNAME_DO_%s(3 downto 0);\n\n"%(
                dst, scr,
            )
        elif gen_det.config["BRAM_width"] ==  9:
            BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_data_%i <= BRAM_BANKNAME_SUBWORDNAME_PO_%s(0 downto 0) & BRAM_BANKNAME_SUBWORDNAME_DO_%s(7 downto 0);\n\n"%(
                dst, scr, scr,
            )
        elif gen_det.config["BRAM_width"] == 18:
            BRAM_BODY += "BRAM_BANKNAME_SUBWORDNAME_data_%i <= BRAM_BANKNAME_SUBWORDNAME_PO_%s & BRAM_BANKNAME_SUBWORDNAME_DO_%s;\n\n"%(
                dst, scr, scr,
            )
        else:
            raise ValueError("Unknown BRAM_width, %i"%(BRAM_width, ) )

    return BRAM_HEAD, BRAM_BODY
