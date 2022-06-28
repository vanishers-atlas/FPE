# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import re
import copy


from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor  import ALU_packer
from FPE.toolchain.HDL_generation.processor  import ALU_unpacker

from FPE.toolchain.HDL_generation.processor  import ALU_core_passthrough
from FPE.toolchain.HDL_generation.processor  import ALU_core_dsp48e1

from FPE.toolchain.HDL_generation.processor  import ALU_shifter

#####################################################################

core_module_LUT = {
    "passthrough"    : ALU_core_passthrough,
    "dsp48e1"   : ALU_core_dsp48e1,
}

def add_inst_config(instr_id, instr_set, config):
    # Determine core type
    only_passthrough_ops_used = True
    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

            if   mnemonic in [
                "MOV", "LSH", "RSH", "LRL", "RRL",
                "PMOV", "PLSH", "PRSH", "PLRL", "PRRL",
                "JEQ", "JNE", "JGT", "JGE", "JLT", "JLE",
            ]:
                pass
            elif mnemonic in [
                "ADD", "MUL", "SUB", "UCMP", "SCMP",
                "PADD", "PSUB",
                "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
                "PNOT", "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR",
            ]:
                only_passthrough_ops_used = False
            else:
                raise ValueError("Unsupported mnemonic, " + mnemonic)
    if only_passthrough_ops_used:
        config["core_type"] = "passthrough"
    else:
        config["core_type"] = "dsp48e1"


    # Check for optional modules
    shifter_used = False
    for instr in instr_set:
        mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
        if mnemonic in ["LSH", "RSH", "LRL", "RRL", "PLSH", "PRSH", "PLRL", "PRRL", ]:
            shifter_used = True


    # Get config from subcomponents
    config["packer"] = copy.deepcopy(ALU_packer.add_inst_config(instr_id, instr_set, config))
    config["core"] = copy.deepcopy(core_module_LUT[config["core_type"]].add_inst_config(instr_id, instr_set, config))
    config["unpacker"] = copy.deepcopy(ALU_unpacker.add_inst_config(instr_id, instr_set, config))

    if shifter_used:
        config["shifter"] = copy.deepcopy(ALU_shifter.add_inst_config(instr_id, instr_set, config))

    return config

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    pathways = gen_utils.init_datapaths()

    # Get pathways from subcomponents
    packer_pathways = ALU_packer.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    pathways = gen_utils.merge_datapaths(pathways, packer_pathways)
    unpacker_pathways = ALU_unpacker.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    pathways = gen_utils.merge_datapaths(pathways, unpacker_pathways)
    if "shifter" in  config.keys():
        shifter_pathways = ALU_shifter.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
        pathways = gen_utils.merge_datapaths(pathways, shifter_pathways)

    return pathways

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    packer_controls = ALU_packer.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    controls = gen_utils.merge_controls(controls, packer_controls)

    core_controls = core_module_LUT[config["core_type"]].get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    controls = gen_utils.merge_controls(controls, core_controls)

    unpacker_controls = ALU_unpacker.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    controls = gen_utils.merge_controls(controls, unpacker_controls)

    if "shifter" in  config.keys():
        shifter_controls = ALU_shifter.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
        controls = gen_utils.merge_controls(controls, shifter_controls)

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["data_width"]) == int, "data_width must be an int"
    assert config_in["data_width"] >= 1, "data_width must be greater than 0"
    config_out["data_width"] = config_in["data_width"]

    assert type(config_in["stallable"]) == bool, "stallable must be a bool"
    config_out["stallable"] = config_in["stallable"]

    assert type(config_in["signal_padding"]) == str, "signal_padding must be an str"
    assert config_in["signal_padding"] in ["unsigned", "signed", ], "Unknown signal_padding, %s"%(config_in["signal_padding"], )
    config_out["signal_padding"] = config_in["signal_padding"]


    # Check config of sub units
    if "shifter" in config_in.keys():
        if __debug__: ALU_shifter.preprocess_config(config_in["shifter"])
        config_out["shifter"] = config_in["shifter"]

    if __debug__: ALU_packer.preprocess_config(config_in["packer"])
    config_out["packer"] = config_in["packer"]

    assert type(config_in["core_type"]) == str, "core_type must be a str"
    assert config_in["core_type"] in core_module_LUT.keys(), "Unknown core type, " + config_in["core_type"]
    config_out["core_type"] = config_in["core_type"]

    if __debug__: core_module_LUT[config_out["core_type"]].preprocess_config(config_in["core"])
    config_out["core"] = config_in["core"]

    if __debug__: ALU_unpacker.preprocess_config(config_in["unpacker"])
    config_out["unpacker"] = config_in["unpacker"]

    if "shifter" in config_in.keys():
        if __debug__: ALU_unpacker.preprocess_config(config_in["shifter"])
        config_out["shifter"] = config_in["shifter"]

    return config_out

def handle_module_name(module_name, config):
    if module_name == None:
        generated_name = "ALU"

        generated_name += "_%i"%config["data_width"]

        if config["stallable"]:
            generated_name += "_stallable"
        else:
            generated_name += "_nonstallable"

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
        gen_packer(gen_det, com_det)
        gen_core(gen_det, com_det)
        gen_unpacker(gen_det, com_det)

        gen_shifter(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name

#####################################################################

def gen_common_ports(gen_det, com_det):
    com_det.add_port("clock", "std_logic", "in")
    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")
        com_det.arch_head += "signal stall : std_logic;\n"
        com_det.arch_body += "stall <= stall_in;\n"

#####################################################################

packer_fanin_signals = {
    "clock" : "clock",
    "stall_in" : "stall"
}
packer_ripple_up_signals = [
    ( re.compile("fetched_(\d+)_word_(\d+)"), lambda m : "packer_fetched_%s_word_%s"%(m.group(1), m.group(2), ) ),
    ( re.compile("input_(\d+)_(\d+)_source_sel"), lambda m : "packer_input_%s_%s_source_sel"%(m.group(1), m.group(2), ) ),
    ( re.compile("input_(\d+)_packing_sel"), lambda m : "packer_input_%s_packing_sel"%(m.group(1), ) ),
    ( re.compile("input_(\d+)_block_size_sel"), lambda m : "packer_input_%s_block_size_sel"%(m.group(1), ) ),
]
packer_internal_inputs = [
    ( re.compile("acc_word_(\d+)"), lambda m : "unpacker_acc_word_%s"%(m.group(1), ) ),
    ( re.compile("shifter_word_(\d+)"), lambda m : "shifter_result_word_%s"%(m.group(1), ) )
]
packer_internal_output = [
    ( re.compile("result_(\d+)"), lambda m : "operand_%s_packed"%(m.group(1), ) ),
]

def gen_packer(gen_det, com_det):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_packer"
    else:
        module_name = None

    sub_interface, sub_name = ALU_packer.generate_HDL(
        gen_det.config["packer"],
        gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("packer", sub_interface)

    com_det.arch_body += "packer : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "port map (\n\>"

    # Handle fanin signals
    for port, signal in packer_fanin_signals.items():
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal)

    # Handle ripple up signals
    for rule, transform in packer_ripple_up_signals:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.add_port(transform(match), "std_logic_vector", details["direction"], details["width"])
                except KeyError:
                    com_det.add_port(transform(match), "std_logic", details["direction"])

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal inputs
    for rule, transform in packer_internal_inputs:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal outputs
    for rule, transform in packer_internal_output:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(transform(match), details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : std_logic;\n"%(transform(match), )

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )


    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"

    # Pass operand widths to core
    operand = 0
    gen_det.config["core"]["operand_widths"] = []
    while "result_%i"%(operand, ) in sub_interface["ports"].keys():
        gen_det.config["core"]["operand_widths"].append(sub_interface["ports"]["result_%i"%(operand, )]["width"])
        operand += 1

#####################################################################

core_fanin_signals = {
    "clock" : "clock",
    "stall_in" : "stall"
}
core_ripple_up_signals = [
    ( re.compile("acc_enable")      , lambda m : "core_acc_enable" ),
    ( re.compile("update_statuses") , lambda m : "core_update_statuses" ),
    ( re.compile("CMP_sel"), lambda m : "core_CMP_sel" ),
    ( re.compile("hold_operand_signs"), lambda m : "core_hold_operand_signs" ),
    ( re.compile("jump_not_equal")  , lambda m : "core_jump_not_equal" ),
    ( re.compile("jump_greater"), lambda m : "core_jump_greater" ),
    ( re.compile("jump_lesser") , lambda m : "core_jump_lesser" ),
    ( re.compile("jump_equal")  , lambda m : "core_jump_equal" ),
    ( re.compile("jump_taken")  , lambda m : "core_jump_taken" ),
    ( re.compile("op_mode") , lambda m : "core_op_mode" ),
    ( re.compile("ALU_mode"), lambda m : "core_ALU_mode" ),
]

core_internal_inputs = [
    ( re.compile("operand_(\d+)"), lambda m : "operand_%s_packed"%(m.group(1), ) ),
]
core_internal_output = [
    ( re.compile("result_(\d+)"), lambda m : "core_result_%s"%(m.group(1), ) ),
]

def gen_core(gen_det, com_det):

    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_core"
    else:
        module_name = None

    sub_interface, sub_name = core_module_LUT[gen_det.config["core_type"]].generate_HDL(
        gen_det.config["core"],
        gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("core", sub_interface)

    com_det.arch_body += "core : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "port map (\n\>"

    # Handle fanin signals
    for port, signal in packer_fanin_signals.items():
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal)

    # Handle ripple up signals
    for rule, transform in core_ripple_up_signals:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.add_port(transform(match), "std_logic_vector", details["direction"], details["width"])
                except KeyError:
                    com_det.add_port(transform(match), "std_logic", details["direction"])

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal inputs
    for rule, transform in core_internal_inputs:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal outputs
    for rule, transform in core_internal_output:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(transform(match), details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : std_logic;\n"%(transform(match), )

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"

    # Pass result widths to unpacker
    operand = 0
    gen_det.config["unpacker"]["result_widths"] = []
    while "result_%i"%(operand, ) in sub_interface["ports"].keys():
        gen_det.config["unpacker"]["result_widths"].append(sub_interface["ports"]["result_%i"%(operand, )]["width"])
        operand += 1


#####################################################################

unpacker_fanin_signals = {
    "clock" : "clock",
    "stall_in" : "stall"
}
unpacker_ripple_up_signals = [
    ( re.compile("enable"), lambda m : "unpacker_enable" ),
    ( re.compile("stored_(\d+)_word_(\d+)"), lambda m : "result_%s_word_%s"%(m.group(1), m.group(2), ) ),
    ( re.compile("([\d\w]+)_word_(\d+)_sel"), lambda m : "unpacker_%s_word_%s_sel"%(m.group(1), m.group(2), ) ),
]
unpacker_internal_inputs = [
    ( re.compile("result_(\d+)"), lambda m : "core_result_%s"%(m.group(1), ) ),
]
unpacker_internal_output = [
    ( re.compile("acc_word_(\d+)"), lambda m : "unpacker_acc_word_%s"%(m.group(1), ) ),
]

def gen_unpacker(gen_det, com_det):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_unpacker"
    else:
        module_name = None

    sub_interface, sub_name = ALU_unpacker.generate_HDL(
        gen_det.config["unpacker"],
        gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("unpacker", sub_interface)

    com_det.arch_body += "unpacker : entity work.%s(arch)\>\n"%(sub_name, )

    com_det.arch_body += "port map (\n\>"

    # Handle fanin signals
    for port, signal in packer_fanin_signals.items():
        if port in sub_interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal)

    # Handle ripple up signals
    for rule, transform in unpacker_ripple_up_signals:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.add_port(transform(match), "std_logic_vector", details["direction"], details["width"])
                except KeyError:
                    com_det.add_port(transform(match), "std_logic", details["direction"])

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal inputs
    for rule, transform in unpacker_internal_inputs:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

    # Handle internal outputs
    for rule, transform in unpacker_internal_output:
        for port in sub_interface["ports"].keys():
            match = rule.fullmatch(port)
            if match:
                details = sub_interface["ports"][port]

                try:
                    com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(transform(match), details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s : std_logic;\n"%(transform(match), )

                com_det.arch_body += "%s => %s,\n"%(port, transform(match), )


    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\n\<);\n\<\n"


#####################################################################

shifter_fanin_signals = {
    "clock" : "clock",
    "stall_in" : "stall"
}
shifter_ripple_up_signals = [
    ( re.compile("fetched_word_(\d+)"), lambda m : "shifter_fetched_word_%s"%(m.group(1), ) ),
    ( re.compile("word_(\d+)_operand_sel"), lambda m : "shifter_word_%s_operand_sel"%(m.group(1), ) ),
    ( re.compile("word_(\d+)_shift_sel"), lambda m : "shifter_word_%s_shift_sel"%(m.group(1), ) ),
]
shifter_internal_inputs = [
    ( re.compile("acc_word_(\d+)"), lambda m : "unpacker_acc_word_%s"%(m.group(1), ) ),
]
shifter_internal_output = [
    ( re.compile("result_word_(\d+)"), lambda m : "shifter_result_word_%s"%(m.group(1), ) ),
]

def gen_shifter(gen_det, com_det):
    if "shifter" in gen_det.config.keys():
        if gen_det.concat_naming:
            module_name = gen_det.module_name + "_shifter"
        else:
            module_name = None

        sub_interface, sub_name = ALU_shifter.generate_HDL(
            gen_det.config["shifter"],
            gen_det.output_path,
            module_name=module_name,
            concat_naming=gen_det.concat_naming,
            force_generation=gen_det.force_generation
        )
        com_det.add_interface_item("shifter", sub_interface)

        com_det.arch_body += "shifter : entity work.%s(arch)\>\n"%(sub_name, )

        com_det.arch_body += "port map (\n\>"

        # Handle fanin signals
        for port, signal in packer_fanin_signals.items():
            if port in sub_interface["ports"]:
                com_det.arch_body += "%s => %s,\n"%(port, signal)

        # Handle ripple up signals
        for rule, transform in shifter_ripple_up_signals:
            for port in sub_interface["ports"].keys():
                match = rule.fullmatch(port)
                if match:
                    details = sub_interface["ports"][port]

                    try:
                        com_det.add_port(transform(match), "std_logic_vector", details["direction"], details["width"])
                    except KeyError:
                        com_det.add_port(transform(match), "std_logic", details["direction"])

                    com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

        # Handle internal inputs
        for rule, transform in shifter_internal_inputs:
            for port in sub_interface["ports"].keys():
                match = rule.fullmatch(port)
                if match:
                    com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

        # Handle internal outputs
        for rule, transform in shifter_internal_output:
            for port in sub_interface["ports"].keys():
                match = rule.fullmatch(port)
                if match:
                    details = sub_interface["ports"][port]

                    try:
                        com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(transform(match), details["width"] - 1, )
                    except KeyError:
                        com_det.arch_head += "signal %s : std_logic;\n"%(transform(match), )

                    com_det.arch_body += "%s => %s,\n"%(port, transform(match), )

        com_det.arch_body.drop_last_X(2)
        com_det.arch_body += "\n\<);\n\<\n"
