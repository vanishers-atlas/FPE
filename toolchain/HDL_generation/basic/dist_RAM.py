# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    raise NotImplementedError()

    return config

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataFlow()

    raise NotImplementedError()

    return dataMesh

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    raise NotImplementedError()

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert(type(config_in["depth"]) == type(0))
    assert(config_in["depth"] > 0)
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)
    config_out["depth"] = 2**config_out["addr_width"]

    assert(type(config_in["ports_config"]) == type(""))
    assert(config_in["ports_config"] in ["SINGLE", "SIMPLE_DUAL", "DUAL", "QUAD"])
    config_out["ports_config"] = config_in["ports_config"]

    assert type(config_in["synchronicity"]) == str
    assert config_in["synchronicity"] in ["NONE", "READ_ONLY", "WRITE_ONLY", "READ_WRITE", ]
    config_out["synchronicity"] = config_in["synchronicity"]

    if config_in["synchronicity"] == "READ_WRITE":
        assert(type(config_in["write_before_read"]) == type(True))
        config_out["write_before_read"] = config_in["write_before_read"]

    assert(type(config_in["enabled_reads"]) == type(True))
    config_out["enabled_reads"] = config_in["enabled_reads"]

    assert(type(config_in["init_type"]) == type(""))
    assert(config_in["init_type"] in ["NONE", "MIF", "GENERIC_INT", "GENERIC_STD"])
    config_out["init_type"] = config_in["init_type"]

    if config_in["init_type"] in ["GENERIC_STD"]:
        assert(type(config_in["width"]) == int)
        assert(config_in["width"] > 0)
        config_out["width"] = config_in["width"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:

        generated_name = "dist_RAM"

        generated_name += "_%id"%(config["depth"])


        if "width" in config.keys():
            generated_name += "_%iw"%(config["width"])

        generated_name += "_%s"%(config["ports_config"])

        if   config["synchronicity"] == "NONE":
            generated_name += "_N"
        elif config["synchronicity"] == "READ_ONLY":
            generated_name += "_R"
        elif config["synchronicity"] == "WRITE_ONLY":
            generated_name += "_W"
        elif config["synchronicity"] == "READ_WRITE":
            if config["write_before_read"]:
                generated_name += "_FW"
            else:
                generated_name += "_FR"
        else:
            raise ValueError("Unknown synchronicity, %s"%(config["synchronicity"]))

        if config["enabled_reads"]:
            generated_name += "_RE"


        if config["init_type"] != "NONE":
            generated_name += "_%s"%(config["init_type"])

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
        com_det.add_interface_item("addr_width", gen_det.config["addr_width"])
        gen_det, com_det = gen_generate_common_ports(gen_det, com_det)
        gen_det, com_det = gen_value_array(gen_det, com_det)
        gen_det, com_det = gen_write_read_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_generate_common_ports(gen_det, com_det):

    if gen_det.config["synchronicity"] != "NONE":
        com_det.add_port("clock", "std_logic", "in")
    if gen_det.config["enabled_reads"]:
        com_det.add_port("read_enable", "std_logic", "in")
    com_det.add_port("write_enable", "std_logic", "in")

    if "width" not in gen_det.config.keys():
        com_det.add_generic("data_width", "integer")
        if   gen_det.config["ports_config"] == "SINGLE":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector(data_width - 1 downto 0)", "out")
            com_det.add_port("write_data", "std_logic_vector(data_width - 1 downto 0)", "in")

        elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
            com_det.add_port("write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("write_data", "std_logic_vector(data_width - 1 downto 0)", "in")

            com_det.add_port("read_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_data", "std_logic_vector(data_width - 1 downto 0)", "out")
        elif gen_det.config["ports_config"] == "DUAL":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector(data_width - 1 downto 0)", "out")
            com_det.add_port("write_data", "std_logic_vector(data_width - 1 downto 0)", "in")

            com_det.add_port("read_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_data", "std_logic_vector(data_width - 1 downto 0)", "out")
        elif gen_det.config["ports_config"] == "QUAD":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector(data_width - 1 downto 0)", "out")
            com_det.add_port("write_data", "std_logic_vector(data_width - 1 downto 0)", "in")

            com_det.add_port("read_0_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_0_data", "std_logic_vector(data_width - 1 downto 0)", "out")

            com_det.add_port("read_1_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_1_data", "std_logic_vector(data_width - 1 downto 0)", "out")

            com_det.add_port("read_2_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_2_data", "std_logic_vector(data_width - 1 downto 0)", "out")
        else:
            raise ValueError("Unknown ports_config, %s"%(gen_det.config["ports_config"]))
    else:
        if   gen_det.config["ports_config"] == "SINGLE":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector", "out", gen_det.config["width"])
            com_det.add_port("write_data", "std_logic_vector", "in", gen_det.config["width"])
        elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
            com_det.add_port("write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("write_data", "std_logic_vector", "in", gen_det.config["width"])

            com_det.add_port("read_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_data", "std_logic_vector", "out", gen_det.config["width"])
        elif gen_det.config["ports_config"] == "DUAL":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector", "out", gen_det.config["width"])
            com_det.add_port("write_data", "std_logic_vector", "in", gen_det.config["width"])

            com_det.add_port("read_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_data", "std_logic_vector", "out", gen_det.config["width"])
        elif gen_det.config["ports_config"] == "QUAD":
            com_det.add_port("read_write_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_write_data", "std_logic_vector", "out", gen_det.config["width"])
            com_det.add_port("write_data", "std_logic_vector", "in", gen_det.config["width"])

            com_det.add_port("read_0_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_0_data", "std_logic_vector", "out", gen_det.config["width"])

            com_det.add_port("read_1_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_1_data", "std_logic_vector", "out", gen_det.config["width"])

            com_det.add_port("read_2_addr", "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1, ), "in")
            com_det.add_port("read_2_data", "std_logic_vector", "out", gen_det.config["width"])
        else:
            raise ValueError("Unknown init_type, %s"%(gen_det.config["ports_config"]))

    return gen_det, com_det


def gen_value_array(gen_det, com_det):
    # Declare internal array type
    com_det.arch_head += "-- Data array type and handling\n"
    if "width" not in gen_det.config.keys():
        com_det.arch_head += "type data_array is array (0 to %i) of std_logic_vector(data_width - 1 downto 0);\n\n" % (
            gen_det.config["depth"] - 1,
        )
    else:
        com_det.arch_head += "type data_array is array (0 to %i) of std_logic_vector(%i downto 0);\n\n" % (
            gen_det.config["depth"] - 1,
            gen_det.config["width"] - 1,
        )

    # Handle initing the array`
    if   gen_det.config["init_type"] == "NONE":
        com_det.arch_head += "signal internal_data : data_array;\n\n"
    elif gen_det.config["init_type"] == "MIF":
        com_det.add_import("ieee", "std_logic_textio", "all")
        com_det.add_import("STD", "textio", "all")

        com_det.add_generic("init_mif", "string")

        # split reading mem file into lots of 1024 (2^10), to prevent vivado loop limit licking in
        loop_counts = []
        acc = gen_det.config["depth"]
        while acc > 0:
            loop_counts.append(acc % 1024)
            acc = int(acc / 1024)

        # Define function for loading values into data_array
        com_det.arch_head += "impure function init_mem(mem_file_name : in string) return data_array is\n@>"

        com_det.arch_head += "-- Declare file handle\n"
        com_det.arch_head += "file mem_file : text;\n"

        com_det.arch_head += "-- Declare variables to decode input mem file\n"
        com_det.arch_head += "variable addr : integer := 0;\n"
        com_det.arch_head += "variable data_line : line;\n"
        com_det.arch_head += "variable word_value : std_logic_vector(data_width - 1 downto 0);\n"

        com_det.arch_head += "-- Declare variables loop variables\n"
        for counter in range(len(loop_counts) + 1):
            com_det.arch_head += "variable counter_%i : integer;\n" % (counter,)

        com_det.arch_head += "variable temp_mem : data_array;\n@<"

        com_det.arch_head += "begin\n@>"

        com_det.arch_head += "-- open passed file\n"
        com_det.arch_head += "file_open(mem_file, mem_file_name,  read_mode);\n"

        for power, count in enumerate(loop_counts):
            if count != 0:
                for counter in range(power):
                    com_det.arch_head += "counter_%i  := 0;\n" % (counter + 1,)
                    com_det.arch_head += "for counter_%i in 0 to 1023 loop\n@>" % (counter + 1,)

                com_det.arch_head += "counter_0  := 0;\n"
                com_det.arch_head += "for counter_0 in 0 to %i loop\n@>" % (count - 1,)
                com_det.arch_head += "readline(mem_file, data_line);\n"
                com_det.arch_head += "read(data_line, word_value);\n"
                com_det.arch_head += "temp_mem(addr) := word_value;\n"
                com_det.arch_head += "addr := addr + 1;\n"
                com_det.arch_head += "@<end loop;\n"

                for counter in range(power):
                    com_det.arch_head += "@<end loop;\n"

        com_det.arch_head += "return temp_mem;\n"

        com_det.arch_head += "@<end function;\n\n"

        # Create internal data array
        com_det.arch_head += "signal internal_data : data_array := init_mem(init_mif);\n\n"
    elif gen_det.config["init_type"] == "GENERIC_INT":
        for addr in range(gen_det.config["depth"]):
            com_det.add_generic("init_%i"%(addr, ), "integer")

        com_det.arch_head += "signal internal_data : data_array := (@>%s@<\n);\n\n"%(
            ",\n".join([
                "std_logic_vector(to_unsigned(init_%i, data_width - 1))"%(addr, )
                for addr in range(gen_det.config["depth"])
            ])
        )
    elif gen_det.config["init_type"] == "GENERIC_STD":
        for addr in range(gen_det.config["depth"]):
            com_det.add_generic("init_%i"%(addr, ), "std_logic_vector", gen_det.config["width"])

        com_det.arch_head += "signal internal_data : data_array := (@>%s@<\n);\n\n"%(
            ",\n".join([
                "init_%i"%(addr, )
                for addr in range(gen_det.config["depth"])
            ])
        )
    else:
        raise ValueError("Unknown init_type, %s"%(gen_det.config["init_type"]))

    return gen_det, com_det

#####################################################################

def gen_write_read_logic(gen_det, com_det):
    if   gen_det.config["synchronicity"] == "NONE":
        if   gen_det.config["ports_config"] == "SINGLE":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
        elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "DUAL":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "QUAD":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_0")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_1")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_2")
    elif gen_det.config["synchronicity"] == "READ_ONLY":
        if   gen_det.config["ports_config"] == "SINGLE":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
        elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "DUAL":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "QUAD":
            gen_det, com_det = gen_async_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_0")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_1")
            gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_2")
    elif gen_det.config["synchronicity"] == "WRITE_ONLY":
        if   gen_det.config["ports_config"] == "SINGLE":
            gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
        elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
            gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "DUAL":
            gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read")
        elif gen_det.config["ports_config"] == "QUAD":
            gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_write")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_0")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_1")
            gen_det, com_det = gen_async_read_logic(gen_det, com_det, "read_2")
    elif gen_det.config["synchronicity"] == "READ_WRITE":
        if not gen_det.config["write_before_read"]:
            if   gen_det.config["ports_config"] == "SINGLE":
                gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
            elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
                gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read")
            elif gen_det.config["ports_config"] == "DUAL":
                gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read")
            elif gen_det.config["ports_config"] == "QUAD":
                gen_det, com_det = gen_sync_write_logic(gen_det, com_det, "read_write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_write")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_0")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_1")
                gen_det, com_det = gen_sync_read_logic(gen_det, com_det, "read_2")
        else:
            if   gen_det.config["ports_config"] == "SINGLE":
                gen_det, com_det = gen_write_before_read_logic(gen_det, com_det, "read_write", True, [])
            elif gen_det.config["ports_config"] == "SIMPLE_DUAL":
                gen_det, com_det = gen_write_before_read_logic(gen_det, com_det, "write", False, ["read", ])
            elif gen_det.config["ports_config"] == "DUAL":
                gen_det, com_det = gen_write_before_read_logic(gen_det, com_det, "read_write", True,["read", ])
            elif gen_det.config["ports_config"] == "QUAD":
                gen_det, com_det = gen_write_before_read_logic(gen_det, com_det, "read_write", True, ["read_0", "read_1", "read_2", ])
    else:
        raise ValueError("Unknown synchronicity, %s"%(gen_det.config["synchronicity"]))

    return gen_det, com_det

#####################################################################

def gen_async_read_logic(gen_det, com_det, read_name):

    assert type(read_name) == str

    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "process (%s_addr, %s_enable, internal_data)@>\n"%(read_name, read_name,)
    else:
        com_det.arch_body += "process (%s_addr, internal_data)@>\n"%(read_name, )
    com_det.arch_body += "@<begin@>\n"
    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "if read_enable = '1' then@>\n"

    com_det.arch_body += "%s_data <= internal_data(to_integer(unsigned(%s_addr)));\n"%(read_name, read_name, )
    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "@<end if;\n"
    com_det.arch_body += "@<end process;\n\n"

    return gen_det, com_det

def gen_sync_read_logic(gen_det, com_det, read_name):

    assert type(read_name) == str

    com_det.arch_body += "process (clock)@>\n"
    com_det.arch_body += "@<begin@>\n"
    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "if rising_edge(clock) and %s_enable = '1' then@>\n"%(read_name, )
    else:
        com_det.arch_body += "if rising_edge(clock) then@>\n"
    com_det.arch_body += "%s_data <= internal_data(to_integer(unsigned(%s_addr)));\n"%(read_name, read_name, )
    com_det.arch_body += "@<end if;\n"
    com_det.arch_body += "@<end process;\n\n"

    return gen_det, com_det

#####################################################################

def gen_async_write_logic(gen_det, com_det, write_name):

    assert type(write_name) == str

    com_det.arch_body += "process (%s_addr, %s_data, write_enable)@>\n"%(write_name, write_name, write_name)
    com_det.arch_body += "@<begin@>\n"
    com_det.arch_body += "if write_enable = '1' then@>\n"
    com_det.arch_body += "internal_data(to_integer(unsigned(%s_addr))) <= write_data;\n"%(write_name, )
    com_det.arch_body += "@<end if;\n"
    com_det.arch_body += "@<end process;\n\n"

    return gen_det, com_det

def gen_sync_write_logic(gen_det, com_det, write_name):

    assert type(write_name) == str

    com_det.arch_body += "process (clock)@>\n"
    com_det.arch_body += "@<begin@>\n"
    com_det.arch_body += "if rising_edge(clock) and write_enable = '1' then@>\n"
    com_det.arch_body += "internal_data(to_integer(unsigned(%s_addr))) <= write_data;\n"%(write_name, )
    com_det.arch_body += "@<end if;\n"
    com_det.arch_body += "@<end process;\n\n"

    return gen_det, com_det

#####################################################################

def gen_write_before_read_logic(gen_det, com_det, write_name, write_read, reads):

    assert type(write_name) == str
    assert type(write_read) == bool
    assert type(reads) == list
    assert all([type(read) == str for read in reads])

    com_det.arch_body += "process (clock)@>\n"
    com_det.arch_body += "@<begin@>\n"

    com_det.arch_body += "if rising_edge(clock) then@>\n"

    # Write logic
    com_det.arch_body += "if write_enable = '1' then@>\n"
    com_det.arch_body += "internal_data(to_integer(unsigned(%s_addr))) <= write_data;\n"%(write_name, )
    if write_read:
        com_det.arch_body += "%s_data <= write_data;\n"%(write_name, )
    com_det.arch_body += "@<end if;\n\n"

    # Read logic
    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "if read_enable = '1' then@>\n"
    for read in reads:
        com_det.arch_body += "if write_enable = '1' and %s_addr = %s_addr then@>\n"%(read, write_name, )
        com_det.arch_body += "%s_data <= write_data;\n"%(read, )
        com_det.arch_body += "@<else@>\n"
        com_det.arch_body += "%s_data <= internal_data(to_integer(unsigned(%s_addr)));\n"%(read, read, )
        com_det.arch_body += "@<end if;\n"
    if gen_det.config["enabled_reads"]:
        com_det.arch_body += "@<end if;\n"

    com_det.arch_body += "@<end if;\n"

    com_det.arch_body += "@<end process;\n\n"

    return gen_det, com_det
