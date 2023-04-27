# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import REP_FSM_preloaded

from FPE.toolchain.HDL_generation.processor import REP_PC_interface

from FPE.toolchain.HDL_generation.processor import REP_loop_bank_preloaded

from FPE.toolchain.HDL_generation.processor import REP_tracker_bank_preloaded

#####################################################################

def add_inst_config(instr_id, instr_set, config):

    raise NotImplementedError()

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    raise NotImplementedError()

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    raise NotImplementedError()

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "PC_width" in config_in
    assert type(config_in["PC_width"]) == int
    assert config_in["PC_width"] > 0
    config_out["PC_width"] = config_in["PC_width"]

    assert "stallable" in config_in
    assert type(config_in["stallable"]) == bool
    config_out["stallable"] = config_in["stallable"]

    assert "subtype" in config_in
    assert type(config_in["subtype"]) == str
    assert config_in["subtype"].lower() in ["preloaded", ]
    config_out["subtype"] = config_in["subtype"].lower()

    config_out["FSM_config"] = FSM_submod_LUT[config_out["subtype"]].preprocess_config(config_in)
    config_out["PC_interface"] = REP_PC_interface.preprocess_config(config_in)
    config_out["loops_config"] = loop_submod_LUT[config_out["subtype"]].preprocess_config(config_in)
    config_out["trackers_config"] = tracker_submod_LUT[config_out["subtype"]].preprocess_config(config_in)

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "REP_bank"

        generated_name += "_" + config["subtype"]

        # Handle FSM
        sub_name = FSM_submod_LUT[config["subtype"]].handle_module_name(None, config["FSM_config"])
        assert sub_name.startswith("REP_FSM_")
        sub_name = sub_name[len("REP_FSM_"):]
        if sub_name.startswith(config["subtype"] + "_"):
            sub_name = sub_name[len(config["subtype"] + "_"):]
        if sub_name.endswith("_stallable"):
            sub_name = sub_name[:-len("_stallable")]
        generated_name += "_FSM_" + sub_name

        # Handle PC_interface
        sub_name = REP_PC_interface.handle_module_name(None, config["PC_interface"])
        assert sub_name.startswith("REP_PC_interface")
        sub_name = sub_name[len("REP_PC_interface"):]
        if sub_name.endswith("_stallable"):
            sub_name = sub_name[:-len("_stallable")]
        generated_name += "_PCI_" + sub_name

        # Include loop_storage name
        sub_name = loop_submod_LUT[config["subtype"]].handle_module_name(None, config["loops_config"])
        assert sub_name.startswith("REP_loop")
        sub_name = sub_name[len("REP_loop"):]
        if sub_name.startswith(config["subtype"] + "_"):
            sub_name = sub_name[len(config["subtype"] + "_"):]
        if sub_name.endswith("_stallable"):
            sub_name = sub_name[:-len("_stallable")]
        generated_name += "_loop_" + sub_name

        # Include tracker_bank name
        sub_name = tracker_submod_LUT[config["subtype"]].handle_module_name(None, config["trackers_config"])
        assert sub_name.startswith("REP_tracker")
        sub_name = sub_name[len("REP_tracker"):]
        if sub_name.startswith(config["subtype"] + "_"):
            sub_name = sub_name[len(config["subtype"] + "_"):]
        if sub_name.endswith("_stallable"):
            sub_name = sub_name[:-len("_stallable")]
        generated_name += "_tracker_" + sub_name

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

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Generation Module Code
        gen_common_ports(gen_det, com_det)
        gen_loop_id_FSM(gen_det, com_det)
        gen_PC_interface(gen_det, com_det)
        gen_loop_storage(gen_det, com_det)
        gen_trackers(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name


#####################################################################

def gen_common_ports(gen_det, com_det):

    com_det.add_port("clock", "std_logic", "in")

    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")


#####################################################################

FSM_submod_LUT = {
    "preloaded"    : REP_FSM_preloaded,
}

fanin_loop_id_FSM_ports = [
    "clock",
    "stall_in",
    "end_found",
    "last_iteration",
]

internal_loop_id_FSM_ports = [
    "loop_id", "loop_id_delayed",
]

ripple_up_loop_id_FSM_ports = [
    "stall_out",
]

def gen_loop_id_FSM(gen_det, com_det):
    # Generate FSM subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_FSM"
    else:
        module_name = None

    sub_interface, sub_name = FSM_submod_LUT[gen_det.config["subtype"]].generate_HDL(
        config=gen_det.config["FSM_config"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("rep_bank_preloaded_loop_id_encoding", sub_interface["preloaded_loop_id_encoding"])

    # Instancate FSM subunit
    com_det.arch_body += "-- Loop_id FSM subunit\n"
    com_det.arch_body += "loop_id_FSM : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "generic map (\>\n"

    for generic, details in sub_interface["generics"].items():
        assert generic == "starting_loop_id" or (generic.startswith("loop_") and generic.endswith(("_on_overwrite", "_on_fallthrough", "_on_overwrite_stall", "_on_fallthrough_stall")) )
        com_det.ripple_generic(generic, details)
        com_det.arch_body += "%s => %s,\n"%(generic, generic, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<)\n"

    com_det.arch_body += "port map (\n\>"

    if __debug__:
        for port in sub_interface["ports"].keys():
            assert (    port in fanin_loop_id_FSM_ports
                    or  port in ripple_up_loop_id_FSM_ports
                    or  port in internal_loop_id_FSM_ports
                ), "Unknown port in loop_id_FSM, " + port

    # Handle fan in ports
    for port in fanin_loop_id_FSM_ports:
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle ripple up ports
    for port in ripple_up_loop_id_FSM_ports:
        if port in sub_interface["ports"]:
            com_det.ripple_port(port, sub_interface["ports"][port])
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle internal ports
    for port in internal_loop_id_FSM_ports:
        if  port in sub_interface["ports"]:
            port_details = sub_interface["ports"][port]
            if port_details["direction"] == "out":
                try:
                    com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(port, port_details["type"], port_details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"

#####################################################################

fanin_PC_interface_ports = [
    "clock",
    "stall_in",
    "loop_start",
    "loop_end",
    "last_iteration",
]

ripple_up_PC_interface_ports = [
    "PC_value",
    "PC_running",
    "overwrite_enable",
    "overwrite_value",
]

internal_PC_interface_ports = [
    "end_found",
]


def gen_PC_interface(gen_det, com_det):
    # Generate PC_interface subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_PCI"
    else:
        module_name = None

    sub_interface, sub_name = REP_PC_interface.generate_HDL(
        config=gen_det.config["PC_interface"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    # Instancate FSM subunit
    com_det.arch_body += "-- PC-interface subunit\n"
    com_det.arch_body += "PC_interface : entity work.%s(arch)\>\n"%(sub_name, )

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
                try:
                    com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(port, port_details["type"], port_details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"

#####################################################################

loop_submod_LUT = {
    "preloaded"    : REP_loop_bank_preloaded,
}

fanin_loop_storage_ports = [
    "clock",
    "stall_in",
    "loop_id",
]

internal_loop_storage_ports = [
    "loop_start",
    "loop_end",
]

def gen_loop_storage(gen_det, com_det):
    # Generate loop_storage subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_loops"
    else:
        module_name = None

    sub_interface, sub_name = loop_submod_LUT[gen_det.config["subtype"]].generate_HDL(
        config=gen_det.config["loops_config"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("rep_bank_preloaded_pc_values_encoding", sub_interface["preloaded_pc_values_encoding"])

    # Instancate loop_storage subunit
    com_det.arch_body += "-- Loop storage subunit\n"
    com_det.arch_body += "loop_storage : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "generic map (\>\n"

    for generic, details in sub_interface["generics"].items():
        assert generic.startswith("loop_") and (generic.endswith("_start_value") or generic.endswith("_end_value"))
        com_det.ripple_generic(generic, details)
        com_det.arch_body += "%s => %s,\n"%(generic, generic, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\<\n)\n"

    com_det.arch_body += "port map (\n\>"

    if __debug__:
        for port in sub_interface["ports"].keys():
            assert (    port in fanin_loop_storage_ports
                    or  port in internal_loop_storage_ports
                ), "Unknown port in PC_interface, " + port

    # Handle fan in ports
    for port in fanin_loop_storage_ports:
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle internal ports
    for port in internal_loop_storage_ports:
        if  port in sub_interface["ports"]:
            port_details = sub_interface["ports"][port]
            if port_details["direction"] == "out":
                try:
                    com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(port, port_details["type"], port_details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"


#####################################################################

tracker_submod_LUT = {
    "preloaded"    : REP_tracker_bank_preloaded,
}

fanin_tracker_ports = [
    "clock",
    "stall_in",
    "loop_id",
    "loop_id_delayed",
]

internal_tracker_ports = [
    "last_iteration",
    "end_found",
]

def gen_trackers(gen_det, com_det):
    # Generate loop_storage subunit
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_trackers"
    else:
        module_name = None

    sub_interface, sub_name = tracker_submod_LUT[gen_det.config["subtype"]].generate_HDL(
        config=gen_det.config["trackers_config"],
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("rep_bank_preloaded_overwrites_encoding", sub_interface["preloaded_overwrites_encoding"])

    # Instancate trackers subunit
    com_det.arch_body += "-- trackers subunit\n"
    com_det.arch_body += "trackers : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "generic map (\>\n"

    for generic, details in sub_interface["generics"].items():
        assert generic.startswith("loop_") and generic.endswith("_overwrites")
        com_det.ripple_generic(generic, details)
        com_det.arch_body += "%s => %s,\n"%(generic, generic, )
    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<)\n"

    com_det.arch_body += "port map (\n\>"

    if __debug__:
        for port in sub_interface["ports"].keys():
            assert (    port in fanin_tracker_ports
                    or  port in internal_tracker_ports
                ), "Unknown port in PC_interface, " + port

    # Handle fan in ports
    for port in fanin_tracker_ports:
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    # Handle internal ports
    for port in internal_tracker_ports:
        if  port in sub_interface["ports"]:
            port_details = sub_interface["ports"][port]
            if port_details["direction"] == "out":
                try:
                    com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(port, port_details["type"], port_details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : %s;\n"%(port, port_details["type"], )
            com_det.arch_body += "%s => %s,\n"%(port, port, )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"
