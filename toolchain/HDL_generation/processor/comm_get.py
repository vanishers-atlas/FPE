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
from FPE.toolchain.HDL_generation.basic import RS_FF_latch as RS

#####################################################################

def add_inst_config(instr_id, instr_set, config):
    reads = 0
    for instr in instr_set:
        fetch_mems = [ asm_utils.access_mem(access) for access in asm_utils.instr_fetches(instr) ]
        reads = max(reads, fetch_mems.count(instr_id))
    config["reads"] = reads

    return config

read_addr_patern = re.compile("read_(\d+)_addr")
read_data_patern = re.compile("read_(\d+)_data")

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

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


    # Loop over all instructions and generate paths for all found pathway ports
    for instr in instr_set:
        reads = [fetch for fetch, access in enumerate(asm_utils.instr_fetches(instr)) if asm_utils.access_mem(access) == instr_id ]

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

read_adv_pattern = re.compile("read_(\d*)_adv")
read_enable_pattern = re.compile("read_(\d*)_enable")

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Gather controt ports
    read_adv_controls = []
    read_enable_controls = []
    for port in interface["ports"]:
        match = read_adv_pattern.fullmatch(port)
        if match:
            read_adv_controls.append(int(match.group(1)) )
            continue

        match = read_enable_pattern.fullmatch(port)
        if match:
            read_enable_controls.append(int(match.group(1)) )
            continue

    # Handle read_adv_controls
    for read in read_adv_controls:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            get_read_mods = [ asm_utils.access_mods(fetch) for fetch in asm_utils.instr_fetches(instr) if asm_utils.access_mem(fetch) == instr_id ]
            if len(get_read_mods) > read and "ADV" in get_read_mods[read].keys():
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "read_%i_adv"%(read, ), values, "std_logic")


    # Handle read_enable_controls
    for read in read_enable_controls:
        values = { "0" : [], "1" : [], }

        for instr in instr_set:
            fetch_mems = [asm_utils.access_mem(fetch) for fetch in asm_utils.instr_fetches(instr)]
            if fetch_mems.count(instr_id) > read:
                values["1"].append(instr)
            else:
                values["0"].append(instr)

        gen_utils.add_control(controls, "fetch", instr_prefix + "read_%i_enable"%(read, ), values, "std_logic")

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Stalling parameters
    assert type(config_in["FIFO_handshakes"]) == bool, "FIFO_handshakes must be a boolean"
    config_out["FIFO_handshakes"] = config_in["FIFO_handshakes"]

    assert type(config_in["stallable"]) == bool, "stallable must be a boolean"
    config_out["stallable"] = config_in["stallable"]

    if   config_in["FIFO_handshakes"]:
        config_out["stall_type"] = "ACTIVE"
    elif config_in["stallable"]:
        config_out["stall_type"] = "PASSIVE"
    else:
        config_out["stall_type"] = "NONE"

    # Data pori parameters
    assert type(config_in["reads"]) == int, "reads must be an int"
    assert config_in["reads"] > 0., "reads must be greater than 0"
    config_out["reads"] = config_in["reads"]

    assert type(config_in["FIFOs"]) == int, "FIFOs must be an int"
    assert config_in["FIFOs"] > 0., "FIFOs must be greater than 0"
    config_out["FIFOs"] = config_in["FIFOs"]

    # Datapath parametes
    assert type(config_in["data_width"]) == int, "data_width must be an int"
    assert config_in["data_width"] > 0., "data_width must be greater than 0"
    config_out["data_width"] = config_in["data_width"]

    config_out["addr_width"] = tc_utils.unsigned.width(config_out["FIFOs"] - 1)

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "GET"

        # Denote Data width, writes, and FIFOs parameters
        generated_name += "_%ir"%(config["reads"], )
        generated_name += "_%if"%(config["FIFOs"], )
        generated_name += "_%iw"%(config["data_width"], )
        generated_name += "_%s"%(config["stall_type"][0], )


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
        com_det.add_import("ieee", "Numeric_Std", "all")

        # Generation Module Code
        gen_ports(gen_det, com_det)
        gen_stalling_logic(gen_det, com_det)
        gen_FIFO_adv_logic(gen_det, com_det)
        gen_read_data_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_ports(gen_det, com_det):
    # Decalre clock and runnning ports
    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("running", "std_logic", "in")

    # Handle FIFO ports
    for FIFO in range(gen_det.config["FIFOs"]):
        com_det.add_port("FIFO_%i_data"%(FIFO, ), "std_logic_vector", "in", gen_det.config["data_width"])
        com_det.add_port("FIFO_%i_adv"%(FIFO, ), "std_logic", "out")
        if gen_det.config["FIFO_handshakes"]:
            com_det.add_port("FIFO_%i_valid"%(FIFO, ), "std_logic", "in")

    # Handle read ports
    for read in range(gen_det.config["reads"]):
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector", "in", gen_det.config["addr_width"])
        com_det.add_port("read_%i_data"%(read, ), "std_logic_vector", "out", gen_det.config["data_width"])
        com_det.add_port("read_%i_adv"%(read, ), "std_logic", "in")
        if gen_det.config["FIFO_handshakes"]:
            com_det.add_port("read_%i_enable"%(read, ), "std_logic", "in")

    # Handle stalling ports
    if gen_det.config["stall_type"] != "NONE":
        com_det.add_port("stall_in", "std_logic", "in")

    if   gen_det.config["stall_type"] == "ACTIVE":
        com_det.add_port("stall_out", "std_logic", "out")

def gen_stalling_logic(gen_det, com_det):
    # Generate FIFO validation logic
    if gen_det.config["stall_type"] != "NONE":
        com_det.arch_head += "signal stall : std_logic;\n"

        if gen_det.config["stall_type"] == "PASSIVE":
            com_det.arch_body += "stall <= stall_in;\n"
        elif gen_det.config["stall_type"] == "ACTIVE":

            com_det.arch_body += "\n-- FIFO_handshakes stall logic\n"

            com_det.arch_head += "signal generated_stall : std_logic;\n"

            com_det.arch_body += "stall <= stall_in or generated_stall;\n"
            com_det.arch_body += "stall_out <= generated_stall;\n"

            if gen_det.config["FIFOs"] == 1:
                # This code may need reworking, depending on how vivado handles many termed logic expressions
                com_det.arch_body += "generated_stall <= running and %s;\n"%(
                    " or ".join([
                        "(read_%i_enable and not FIFO_0_valid)"%(i, )
                        for i in range(gen_det.config["reads"])
                    ]),
                )
            else:#gen_det.config["FIFOs"] >  1:
                mux_interface, mux_name = mux.generate_HDL(
                    {
                        "inputs" : gen_det.config["FIFOs"]
                    },
                    output_path=gen_det.output_path,
                    module_name=None,
                    concat_naming=False,
                    force_generation=gen_det.force_generation
                )

                for read in range(gen_det.config["reads"]):
                    com_det.arch_head += "signal read_%i_FIFO_valid : std_logic;\n"%(read, )

                    com_det.arch_body += "read_%i_FIFO_valid_mux : entity work.%s(arch)@>\n"%(read, mux_name, )

                    com_det.arch_body += "generic map (data_width => 1)\n"

                    com_det.arch_body += "port map (\n@>"
                    com_det.arch_body += "sel => read_%i_addr,\n"%(read, )
                    for i in range(0, gen_det.config["FIFOs"]):
                        com_det.arch_body += "data_in_%i(0) => FIFO_%i_validated,\n"%(i, i, )
                    for i in range(gen_det.config["FIFOs"], mux_interface["number_inputs"]):
                        com_det.arch_body += "data_in_%i(0) => '0',\n"%(i, )
                    com_det.arch_body += "data_out(0) => read_%i_FIFO_valid\n"%(read, )

                    com_det.arch_body += "@<);\n@<\n"

                # This code may need reworking, depending on how vivado handles many termed logic expressions
                com_det.arch_body += "generated_stall <= running and %s;\n"%(
                    " or ".join([
                        "(read_%i_enable and not read_%i_FIFO_valid)"%(i, i, )
                        for i in range(gen_det.config["reads"])
                    ]),
                )

def gen_FIFO_adv_logic(gen_det, com_det):
    # FIFO_adv logic
    com_det.arch_body += "\n-- FIFO advance logic\n"
    if gen_det.config["FIFOs"] == 1:
        com_det.arch_head += "signal FIFO_0_adv_internal : std_logic;\n"

        # This code may need reworking, depending on how vivado handles many termed logic expressions
        com_det.arch_body += "FIFO_0_adv_internal <= running and %s;\n"%(
            " or ".join([
                "read_%i_adv"%(i, )
                for i in range(gen_det.config["reads"])
            ]),
        )
        if gen_det.config["stall_type"] == "NONE":
            com_det.arch_body += "FIFO_0_adv <= FIFO_0_adv_internal;\n"
        else:
            com_det.arch_body += "FIFO_0_adv <= FIFO_0_adv_internal and not stall;\n"

    else:#gen_det.config["FIFOs"] >  1:
        for FIFO in range(gen_det.config["FIFOs"]):
            com_det.arch_head += "signal FIFO_%i_adv_internal : std_logic;\n"%(FIFO, )
            com_det.arch_body += "FIFO_%i_adv_internal <= running and %s;\n"%(
                FIFO,
                " or ".join([
                    "(read_%i_adv and %s)"%(
                        read,
                        " and ".join([
                            "read_%i_addr(%i)"%(read, bit, ) if FIFO&2**bit
                            else "(not read_%i_addr(%i))"%(read, bit, )
                            for bit in range(gen_det.config["addr_width"])
                        ])
                    )
                    for read in range(gen_det.config["reads"])
                ]),
            )

            if gen_det.config["stall_type"] == "NONE":
                com_det.arch_body += "FIFO_%i_adv <= FIFO_%i_adv_internal;\n"%(FIFO, FIFO, )
            else:
                com_det.arch_body += "FIFO_%i_adv <= FIFO_%i_adv_internal and not stall ;\n"%(FIFO, FIFO, )


def gen_read_data_logic(gen_det, com_det):
    # Generate read_data buffer
    reg_interface, reg_name = register.generate_HDL(
        {
            "has_async_force" : False,
            "has_sync_force" : False,
            "has_enable"   : gen_det.config["stall_type"] != "NONE",
            "force_on_init" : False
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    # Generate read_data buffers
    com_det.arch_head += "\n-- read data signals\n"
    com_det.arch_body += "\n-- read data buffers\n"
    for read in range(gen_det.config["reads"]):
        com_det.arch_head += "signal read_%i_data_buffer_in : std_logic_vector(%i downto 0);\n"%(read, gen_det.config["data_width"] - 1)

        com_det.arch_body += "read_%i_buffer : entity work.%s(arch)@>\n"%(read, reg_name)

        com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

        com_det.arch_body += "port map (\n@>"
        com_det.arch_body += "clock => clock,\n"
        if gen_det.config["stall_type"] == "PASSIVE":
                com_det.arch_body += "enable => not stall,\n"
        elif gen_det.config["stall_type"] == "ACTIVE":
            com_det.arch_body += "enable => read_%i_enable and not stall,\n"%(read, )
        com_det.arch_body += "data_in  => read_%i_data_buffer_in,\n"%(read, )
        com_det.arch_body += "data_out => read_%i_data\n"%(read, )
        com_det.arch_body += "@<);\n@<\n"

    # read_data assignment logic
    com_det.arch_body += "\n-- read_data assignment logic\n"
    if gen_det.config["FIFOs"] == 1:
        for read in range(gen_det.config["reads"]):
            com_det.arch_body += "read_%i_data_buffer_in <= FIFO_0_data;\n"%(read, )
    else:#gen_det.config["FIFOs"] >  1:
        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs" : gen_det.config["FIFOs"]
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        for read in range(gen_det.config["reads"]):
            com_det.arch_body += "read_%i_data_mux : entity work.%s(arch)@>\n"%(read, mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(gen_det.config["data_width"])

            com_det.arch_body += "port map (\n@>"
            com_det.arch_body += "sel => read_%i_addr,\n"%(read, )
            for i in range(0, gen_det.config["FIFOs"]):
                com_det.arch_body += "data_in_%i => FIFO_%i_data,\n"%(i, i, )
            for i in range(gen_det.config["FIFOs"], mux_interface["number_inputs"]):
                com_det.arch_body += "data_in_%i => (others => '0'),\n"%(i, )
            com_det.arch_body += "data_out => read_%i_data_buffer_in\n"%(read, )

            com_det.arch_body += "@<);\n@<\n"
