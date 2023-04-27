# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 4
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.processor import ZOL_PC_interface

from FPE.toolchain.HDL_generation.processor import ZOL_tracker_ripple
from FPE.toolchain.HDL_generation.processor import ZOL_tracker_cascade
from FPE.toolchain.HDL_generation.processor import ZOL_tracker_counter

#####################################################################

def add_inst_config(instr_id, instr_set, config):
    tracker_mod = tracker_module_LUT[config["tracker_type"]]

    # Get config from subcomponents
    config = {
        **config,
        **ZOL_PC_interface.add_inst_config(instr_id, instr_set, config),
        **tracker_mod.add_inst_config(instr_id, instr_set, config),
    }

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()
    tracker_mod = tracker_module_LUT[config["tracker_type"]]

    # Get pathways from subcomponents
    interface_pathways = ZOL_PC_interface.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    tracker_pathways = tracker_mod.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    pathways = gen_utils.merge_datapaths(interface_pathways, tracker_pathways)

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    tracker_mod = tracker_module_LUT[config["tracker_type"]]

    # Get controls from subcomponents
    interface_controls = ZOL_PC_interface.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    tracker_controls = tracker_mod.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    controls = gen_utils.merge_controls(interface_controls, tracker_controls)

    return controls


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "tracker_type" in config_in.keys(), "Passed config lacks tracker_type key"
    assert type("tracker_type") is str, "tracker_type must be a string"
    assert config_in["tracker_type"] in tracker_module_LUT.keys(), "unknown tracker_type, " + config_in["tracker_type"]

    config_out["tracker_type"] = config_in["tracker_type"]

    # Have sub modules check config
    config_out["PC_interface"] = ZOL_PC_interface.preprocess_config(config_in)
    config_out["tracker"] = tracker_module_LUT[config_out["tracker_type"]].preprocess_config(config_in)

    assert "stallable" in config_in.keys(), "Passed config lacks stallable key"
    assert type(config_in["stallable"]) is bool, "stallable must be a boolean"

    config_out["stallable"] = config_in["stallable"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ZOL"

        # Include ZPC_interface name
        sub_name = ZOL_PC_interface.handle_module_name(None, config["PC_interface"])
        assert sub_name.startswith("ZOL_PC_interface")
        if sub_name.endswith("_stallable"):
            generated_name += sub_name[len("ZOL_PC_interface"):-len("_stallable")]
        else:
            generated_name += sub_name[len("ZOL_PC_interface"):]

        # Include tracker's name
        generated_name += "_"
        sub_name = tracker_module_LUT[config["tracker_type"]].handle_module_name(None, config["tracker"])
        assert sub_name.startswith("ZOL_tracker_")
        if sub_name.endswith("_stallable"):
            generated_name += sub_name[len("ZOL_tracker_"):-len("_stallable")]
        else:
            generated_name += sub_name[len("ZOL_tracker_"):]

        # Mark if stallable
        if config["stallable"]:
            generated_name += "_stallable"


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

        # Include common libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Setup common ports
        com_det.add_port("clock", "std_logic", "in")
        if gen_det.config["stallable"]:
            com_det.add_port("stall_in", "std_logic", "in")

        # Generation Module Code
        generate_PC_interface(gen_det, com_det)
        generate_tracker(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name



#####################################################################

fanin_PC_interface_ports = [ "clock", "stall_in", ]
ripple_up_PC_interface_ports = [
    "PC_value", "PC_running",
    "overwrite_PC_value", "overwrite_PC_enable",
    "seek_check_value", "seek_overwrite_value", "seek_enable"
]
internal_PC_interface_ports = [ "match_found", "overwrites_reached", ]

def generate_PC_interface(gen_det, com_det):
    # Generate PC_interface subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_PC_interface"
    else:
        module_name = None

    sub_interface, sub_name = ZOL_PC_interface.generate_HDL(
        config=gen_det.config["PC_interface"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    # Instancate PC_interface subunit
    com_det.arch_body += "-- PC interface handling\n"
    com_det.arch_body += "PC_interface : entity work.%s(arch)\>\n"%(sub_name, )

    if len(sub_interface["generics"]):
        com_det.arch_body += "generic map (\>\n"

        for generic, details in sub_interface["generics"].items():
            com_det.ripple_generic(generic, details)
            com_det.arch_body += "%s => %s,\n"%(generic, generic, )
        com_det.arch_body.drop_last_X(2)
        com_det.arch_body += ")\<\n"

    com_det.arch_body += "port map (\n\>"

    if __debug__:
        for port in sub_interface["ports"].keys():
            assert (    port in fanin_PC_interface_ports
                    or  port in ripple_up_PC_interface_ports
                    or  port in internal_PC_interface_ports
                ), "Unknown port in PC_interface, " + port

    # Handle fan in ports
    for port in fanin_PC_interface_ports:
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle ripple up ports
    for port in ripple_up_PC_interface_ports:
        if port in sub_interface["ports"]:
            com_det.ripple_port(port, sub_interface["ports"][port])
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle internal ports
    for port in internal_PC_interface_ports:
        if  port in sub_interface["ports"]:
            port_details = sub_interface["ports"][port]
            if port_details["direction"] == "out":
                com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"


#####################################################################

tracker_module_LUT = {
    "ripple"    : ZOL_tracker_ripple,
    "cascade"   : ZOL_tracker_cascade,
    "counter"   : ZOL_tracker_counter,
}

fanin_tracker_ports = [ "clock", "stall_in", "PC_running"]
ripple_up_tracker_ports = [ "set_overwrites", "set_enable", ]
internal_tracker_ports = [ "match_found", "overwrites_reached", ]

def generate_tracker(gen_det, com_det):
    # Generate PC_interface subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_tracker"
    else:
        module_name = None

    sub_interface, sub_name = tracker_module_LUT[gen_det.config["tracker_type"]].generate_HDL(
        config=gen_det.config["tracker"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    # Handle overwrites_encoding
    assert "overwrites_encoding" in sub_interface.keys()
    com_det.add_interface_item("overwrites_encoding", sub_interface["overwrites_encoding"])

    # Instancate PC_interface subunit
    com_det.arch_body += "-- overwrites tracker handling\n"
    com_det.arch_body += "tracker : entity work.%s(arch)\>\n"%(sub_name, )

    if len(sub_interface["generics"]):
        assert len(sub_interface["generics"]) == 1
        assert list(sub_interface["generics"].keys())[0] == "overwrites"
        com_det.ripple_generic("overwrites", sub_interface["generics"]["overwrites"])
        com_det.arch_body += "generic map ( overwrites => overwrites )\n"

    com_det.arch_body += "port map (\n\>"

    if __debug__:
        for port in sub_interface["ports"]:
            assert (    port in fanin_tracker_ports
                    or  port in ripple_up_tracker_ports
                    or  port in internal_tracker_ports
                ), "Unknown port in PC_interface, " + port

    # Handle fan in ports
    for port in fanin_tracker_ports:
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle ripple up ports
    for port in ripple_up_tracker_ports:
        if port in sub_interface["ports"]:
            com_det.ripple_port(port, sub_interface["ports"][port])
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle internal ports
    for port in internal_tracker_ports:
        if port in sub_interface["ports"]:
            port_details = sub_interface["ports"][port]
            if port_details["direction"] == "out":
                com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"
