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

def preprocess_config(config_in):
    config_out = {}

    assert(type(config_in["depth"]) == int)
    assert(config_in["depth"] > 0)
    config_out["addr_width"] = tc_utils.unsigned.width(config_in["depth"] - 1)
    config_out["depth"] = 2**config_out["addr_width"]

    if "width" in config_in.keys():
        assert(type(config_in["width"]) == int)
        assert(config_in["width"] > 0)
        config_out["width"] = config_in["width"]

    assert(type(config_in["reads"]) == int)
    assert(0 < config_in["reads"] and config_in["reads"] < 4)
    config_out["reads"] = config_in["reads"]

    assert(type(config_in["synchronous"]) == bool)
    config_out["synchronous"] = config_in["synchronous"]

    assert(type(config_in["has_enable"]) == bool)
    config_out["has_enable"] = config_in["has_enable"]

    assert(type(config_in["init_type"]) == str)
    assert(config_in["init_type"] in ["MIF", "GENERIC_INT", "GENERIC_STD"])
    config_out["init_type"] = config_in["init_type"]

    if __debug__ and config_in["init_type"] in config_in["init_type"] in ["GENERIC_STD"]:
        assert("width" in config_in.keys())

    return config_out

def handle_module_name(module_name, config,):
    if module_name == None:

        generated_name = "dist_ROM"

        generated_name += "_%id"%(config["depth"])

        if "width" in config.keys():
            generated_name += "_%iw"%(config["width"])

        generated_name += "_%ir"%(config["reads"])

        if   not config["synchronous"] and not config["has_enable"]:
            generated_name += "_AA"
        elif not config["synchronous"] and config["has_enable"]:
            generated_name += "_AR"
        elif config["synchronous"] and not config["has_enable"]:
            generated_name += "_SA"
        elif config["synchronous"] and config["has_enable"]:
            generated_name += "_SE"

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
        com_det.add_interface_item("addr_width", gen_det.config["addr_width"])

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")
        com_det.add_import("ieee", "Numeric_Std", "all")

        # Generation Module Code
        gen_generate_ports(gen_det, com_det)
        gen_value_array(gen_det, com_det)
        gen_read_logic(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_generate_ports(gen_det, com_det):
    # Declare commom ports and generates
    if "width" not in gen_det.config.keys():
        com_det.add_generic("data_width", "integer")

    if gen_det.config["synchronous"]:
        com_det.add_port("clock", "std_logic", "in")


    if gen_det.config["has_enable"]:
        com_det.add_port("read_enable", "std_logic", "in")

    # Handle read ports
    for read in range(gen_det.config["reads"]):
        com_det.add_port("read_%i_addr"%(read, ), "std_logic_vector(%i downto 0)"%(gen_det.config["addr_width"] - 1), "in")
        if "width" not in gen_det.config.keys():
            com_det.add_port("read_%i_data"%(read, ), "std_logic_vector(data_width - 1 downto 0)", "out")
        else:
            com_det.add_port("read_%i_data"%(read, ), "std_logic_vector(%i downto 0)"%(gen_det.config["width"] - 1), "out")

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

    # Handle initing the array
    if   gen_det.config["init_type"] == "MIF":
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
            com_det.add_generic("init_%i"%(addr, ), "std_logic_vector(%i downto 0)"%(gen_det.config["width"] - 1, ))

        com_det.arch_head += "signal internal_data : data_array := (@>%s@<\n);\n\n"%(
            ",\n".join([
                "init_%i"%(addr, )
                for addr in range(gen_det.config["depth"])
            ])
        )
    else:
        raise ValueError("Unknown init_type, %s"%(gen_det.config["init_type"]))

def gen_read_logic(gen_det, com_det):
    com_det.arch_body += "\n-- Read behavour\n"
    for read in range(gen_det.config["reads"]):
        # Setup sensativity listTo_int
        if   not gen_det.config["synchronous"] and not gen_det.config["has_enable"]:
            com_det.arch_body += "process (read_%i_addr)@>\n"%(read, )
        elif not gen_det.config["synchronous"] and gen_det.config["has_enable"]:
            com_det.arch_body += "process (read_%i_addr, read_enable)@>\n"%(read, )
        else:#gen_det.config["synchronous"] and not gen_det.config["has_enable"]:
            com_det.arch_body += "process (clock)@>\n"
        com_det.arch_body += "@<begin@>\n"

        # Handle clock gating for synchronous
        if gen_det.config["synchronous"]:
            com_det.arch_body += "if rising_edge(clock) then@>\n"

        # Handle enable gating for enable
        if gen_det.config["has_enable"]:
            com_det.arch_body += "if read_enable = '1' then@>\n"

        com_det.arch_body += "read_%i_data <= internal_data(to_integer(unsigned(read_%i_addr)));\n"%(read, read, )

        # Close enable gating if
        if gen_det.config["has_enable"]:
            com_det.arch_body += "@<end if;\n"

        # Close Clock gating if
        if gen_det.config["synchronous"]:
            com_det.arch_body += "@<end if;\n"

        com_det.arch_body += "@<end process;\n\n"
