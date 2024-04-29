# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import itertools as it
import copy

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import ALU
from FPE.toolchain.HDL_generation.processor import comm_get as GET
from FPE.toolchain.HDL_generation.processor import comm_put as PUT
from FPE.toolchain.HDL_generation.processor import mem_RAM as RAM
from FPE.toolchain.HDL_generation.processor import mem_ROM as ROM
from FPE.toolchain.HDL_generation.processor import mem_regfile as REG
from FPE.toolchain.HDL_generation.processor import block_access_manager as BAM
from FPE.toolchain.HDL_generation.processor import instruction_decoder as ID
from FPE.toolchain.HDL_generation.processor import program_counter as PC
from FPE.toolchain.HDL_generation.processor import zero_overhead_loop as ZOL
from FPE.toolchain.HDL_generation.processor import repeat_bank as REP

from FPE.toolchain.HDL_generation.basic import register
from FPE.toolchain.HDL_generation.basic import delay
from FPE.toolchain.HDL_generation.basic import mux

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    # Handle stallable
    assert type(config_in["report_stall"]) == bool, "report_stall must be bool"
    config_out["report_stall"] = config_in["report_stall"]

    assert type(config_in["external_stall"]) == bool, "external_stall must be bool"
    config_out["external_stall"] = config_in["external_stall"]
    config_out["stallable"] = config_in["external_stall"]

    # Start with basic pipeline
    config_out["pipeline_stages"] = ["PM", "ID", "FETCH", "EXE", "STORE"]

    # Handle SIMD section of config
    config_out["SIMD"] = {}

    assert type(config_in["SIMD"]["lanes"]) == int, "SIMD.lanes must be an int"
    assert config_in["SIMD"]["lanes"] > 0, "SIMD.lanes must be greater than 0"
    config_out["SIMD"]["lanes"] = config_in["SIMD"]["lanes"]

    assert type(config_in["SIMD"]["force_lanes"]) == bool, "SIMD.force_lanes must be a bool"

    if config_out["SIMD"]["lanes"] == 1 and config_in["SIMD"]["force_lanes"] == False:
        config_out["SIMD"]["lanes_names"] = [""]
    else:
        config_out["SIMD"]["lanes_names"] = [
            "LANE_%i_"%(l)
            for l in range(config_in["SIMD"]["lanes"])
        ]


    # Handle instr_set section of config
    assert type(config_in["instr_set"]) == dict, "instr_set must be a dict"
    config_out["instr_set"] = copy.deepcopy(config_in["instr_set"])


    # Handle program_flow section of config
    assert type(config_in["program_flow"]) == dict, "program_flow must be a dict"
    config_out["program_flow"] = {
        "jump_drivers" : []
    }

    assert "PC_width" in config_in["program_flow"].keys()
    assert type(config_in["program_flow"]["PC_width"]) == int
    assert config_in["program_flow"]["PC_width"] > 0
    config_out["program_flow"]["PC_width"] = config_in["program_flow"]["PC_width"]

    assert "program_length" in config_in["program_flow"].keys()
    assert type(config_in["program_flow"]["program_length"]) == int
    assert config_in["program_flow"]["program_length"] > 0
    config_out["program_flow"]["program_length"] = config_in["program_flow"]["program_length"]

    if "hidden_ZOLs" in config_in["program_flow"].keys():
        assert type(config_in["program_flow"]["hidden_ZOLs"]) == dict
        config_out["program_flow"]["hidden_ZOLs"] = copy.deepcopy(config_in["program_flow"]["hidden_ZOLs"])

    if "declared_ZOLs" in config_in["program_flow"].keys():
        assert type(config_in["program_flow"]["declared_ZOLs"]) == dict
        config_out["program_flow"]["declared_ZOLs"] = copy.deepcopy(config_in["program_flow"]["declared_ZOLs"])

    if "rep_bank" in config_in["program_flow"].keys():
        assert type(config_in["program_flow"]["rep_bank"]) == dict
        config_out["program_flow"]["rep_bank"] = {}

        assert "subtype" in config_in["program_flow"]["rep_bank"].keys()
        assert type(config_in["program_flow"]["rep_bank"]["subtype"]) == str
        config_out["program_flow"]["rep_bank"]["subtype"] = config_in["program_flow"]["rep_bank"]["subtype"]

        assert "stall_on_id_change" in config_in["program_flow"]["rep_bank"].keys()
        assert type(config_in["program_flow"]["rep_bank"]["stall_on_id_change"]) == str
        config_out["program_flow"]["rep_bank"]["stall_on_id_change"] = config_in["program_flow"]["rep_bank"]["stall_on_id_change"]

        assert type(config_in["program_flow"]["rep_bank"]["loops"]) == list
        config_out["program_flow"]["rep_bank"]["loops"] = copy.deepcopy(config_in["program_flow"]["rep_bank"]["loops"])


    # Handle instr_decoder section of config
    assert type(config_in["instr_decoder"]) == dict, "instr_decoder must be a dict"
    config_out["instr_decoder"] = copy.deepcopy(config_in["instr_decoder"])

    assert type(config_in["instr_decoder"]["addr_widths"]) == list, "instr_decoder.addr_widths must be a list"
    assert all([type(width) == int for width in config_in["instr_decoder"]["addr_widths"]]), "instr_decoder.addr_widths must integers"
    assert all([width > 0 for width in config_in["instr_decoder"]["addr_widths"]]), "instr_decoder.addr_widths must be greater than 0"

    assert type(config_in["instr_decoder"]["opcode_width"]) == int , "instr_decoder.opcode_width must integers"
    assert config_in["instr_decoder"]["opcode_width"] > 0, "instr_decoder.opcode_width must be greater than 0"

    config_out["instr_decoder"]["instr_width"] = sum(config_in["instr_decoder"]["addr_widths"]) + config_in["instr_decoder"]["opcode_width"]


    # Handle address_sources section of config
    assert type(config_in["address_sources"]) == dict, "address_sources must be a dict"
    config_out["address_sources"] = copy.deepcopy(config_in["address_sources"])


    # Handle data_memory section of config
    assert type(config_in["data_memories"]) == dict, "data_memories must be a dict"
    config_out["data_memories"] = copy.deepcopy(config_in["data_memories"])


    # Handle execute_units section of config
    assert type(config_in["execute_units"]) == dict, "execute_units must be a dict"
    config_out["execute_units"] = copy.deepcopy(config_in["execute_units"])


    # Set the signal padding option
    assert type(config_in["signal_padding"]) == str, "signal_padding must be a str"
    config_out["signal_padding"] = config_in["signal_padding"]


    # Stallable compution
    # This sections may need moved into their subcomponents if stalling condition become more complex
    if "GET" in config_in["data_memories"].keys():
        assert type(config_in["data_memories"]["GET"]["FIFO_handshakes"]) == bool, "data_memories.GET.FIFO_handshakes must be bool"
        if config_in["data_memories"]["GET"]["FIFO_handshakes"] == True:
            config_out["stallable"] = True

    if "PUT" in config_in["data_memories"].keys():
        assert type(config_in["data_memories"]["PUT"]["FIFO_handshakes"]) == bool, "data_memories.PUT.FIFO_handshakes must be bool"
        if config_in["data_memories"]["PUT"]["FIFO_handshakes"] == True:
            config_out["stallable"] = True

    if "rep_bank" in config_in["program_flow"].keys():
        assert type(config_in["program_flow"]["rep_bank"]["stall_on_id_change"]) == str
        if config_in["program_flow"]["rep_bank"]["stall_on_id_change"] in ["ALWAYS", "CONDITIONALLY", ]:
            config_out["stallable"] = True

    assert not config_out["report_stall"] or config_out["report_stall"] and config_out["stallable"], "Cant report_stall in a non-stalling FPE"

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
        controls = gen_utils.init_controls()
        dataMesh = gen_utils.DataMesh()

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Generate VHDL
        gen_non_pipelined_signals(gen_det, com_det)
        controls, dataMesh = gen_execute_units(gen_det, com_det, controls, dataMesh)
        controls, dataMesh = gen_data_memories(gen_det, com_det, controls, dataMesh)
        controls, dataMesh = gen_addr_sources(gen_det, com_det, controls, dataMesh)
        controls, dataMesh = gen_predecode_pipeline(gen_det, com_det, controls, dataMesh)
        controls = handle_datamesh(gen_det, com_det, controls, dataMesh)
        gen_instr_decoder(gen_det, com_det, controls)
        gen_stall_signals(gen_det, com_det)
        gen_running_delays(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name

#####################################################################

def gen_non_pipelined_signals(gen_det, com_det):
    # Create global clock
    com_det.add_port("clock", "std_logic", "in")

    # Step up stall fields
    gen_det.config["stall_sources"] = []
    gen_det.config["stalls"] = {}
    if gen_det.config["stallable"]:
        gen_det.config["stalls"]["stall_all_src"] = []


def gen_stall_signals(gen_det, com_det):

    # Handle external stall ifpresent
    if gen_det.config["external_stall"]:
        com_det.add_port("external_stall", "std_logic", "in")
        gen_det.config["stall_sources"].append("external_stall")

    # Create stall signals
    for stall_signal, excluced_srcs in gen_det.config["stalls"].items():
        com_det.arch_head += "signal %s : std_logic;\n"%(stall_signal, )
        sources = [s for s in gen_det.config["stall_sources"] if s not in excluced_srcs]

        # TODO: looking into a way to selectively mark compoenets as stable instead of a blanket FPE wide  flag
        #assert len(sources) != 0, "Stall without sources " + stall_signal
        if len(sources) == 0:
            com_det.arch_body += "%s <= '0';\n"%(stall_signal, )
        else:
            com_det.arch_body += "%s <= %s;\n"%(stall_signal, " or ".join(sources) )

    # Handle reporing stall
    if gen_det.config["report_stall"]:
        com_det.add_port("report_stall", "std_logic", "out")
        com_det.arch_body += "report_stall <= stall_all_src;\n"

#####################################################################

exe_lib_lookup = {
    "ALU" : ALU,
}

exe_predeclared_ports = {
    "clock" : "clock",
    "stall_in" : "stall_all_src",
}

def gen_execute_units(gen_det, com_det, controls, dataMesh):

    com_det.arch_body += "\n-- Exe components\n"

    # Loinstr over all exe components
    for exe, config in gen_det.config["execute_units"].items():
        # Generate exe code
        if gen_det.concat_naming:
            module_name = gen_det.module_name + "_" + exe
        else:
            module_name = None

        config = exe_lib_lookup[exe].add_inst_config(
            exe,
            gen_det.config["instr_set"],
            {
                **config,
                "jump_width" : gen_det.config["program_flow"]["PC_width"],
                "signal_padding" : gen_det.config["signal_padding"],
                "stallable" : gen_det.config["stallable"],
            }
        )
        sub_interface, sub_name = exe_lib_lookup[exe].generate_HDL(
            config,
            output_path=gen_det.output_path,
            module_name=module_name,
            concat_naming=gen_det.concat_naming,
            force_generation=gen_det.force_generation
        )
        if "jump_drivers" in sub_interface:
            gen_det.config["program_flow"]["jump_drivers"] += sub_interface["jump_drivers"]


        exe_controls = exe_lib_lookup[exe].get_inst_controls(exe, exe + "_", gen_det.config["instr_set"], sub_interface, config)
        controls = gen_utils.merge_controls( controls, exe_controls )
        control_ports = { k[len(exe + "_"):] : k for k in exe_controls["exe"].keys() }


        # instantiate exe for each lane
        for lane in gen_det.config["SIMD"]["lanes_names"]:
            inst = lane + exe

            com_det.arch_body += "\n%s : entity work.%s(arch)@>\n"%(inst, sub_name)

            com_det.arch_body += "port map (@>\n"

            # Loop over all ports
            for port in sorted(sub_interface["ports"].keys()):
                # Handle predeclared ports
                if   port in exe_predeclared_ports.keys():
                    com_det.arch_body += "%s => %s,\n"%(port, exe_predeclared_ports[port], )
                # Handle control ports
                elif port in control_ports.keys():
                    # Declare control singal during first lane only
                    if lane == gen_det.config["SIMD"]["lanes_names"][0]:
                        detail = sub_interface["ports"][port]
                        try:
                            com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(control_ports[port], detail["type"], detail["width"] -1, )
                        except KeyError:
                            com_det.arch_head += "signal %s : %s;\n"%(control_ports[port], detail["type"])

                    com_det.arch_body += "%s => %s,\n"%(port, control_ports[port], )
                # Handle non-predeclared ports
                else:
                    detail = sub_interface["ports"][port]
                    try:
                        com_det.arch_head += "signal %s_%s : %s(%i downto 0);\n"%(inst, port, detail["type"], detail["width"] -1, )
                    except KeyError:
                        com_det.arch_head += "signal %s_%s : %s;\n"%(inst, port, detail["type"])
                    com_det.arch_body += "%s => %s_%s,\n"%(port, inst, port)

            com_det.arch_body.drop_last(2)
            com_det.arch_body += "@<\n);\n"
            com_det.arch_body += "@<\n"

            # Check for stall out port
            if "stall_out" in sub_interface["ports"].keys():
                gen_det.config["stall_sources"].append("%s_stall_out"%(inst, ))


            dataMesh = dataMesh.merge(exe_lib_lookup[exe].get_inst_dataMesh(exe, inst + "_", gen_det.config["instr_set"], sub_interface, config, lane) )

    return controls, dataMesh


#####################################################################

mem_lib_lookup = {
    "GET" : GET,
    "PUT" : PUT,
    "REG" : REG,
    "RAM" : RAM,
    "IMM" : ROM,
    "ROM_A" : ROM,
    "ROM_B" : ROM,
}

mem_predeclared_ports_all_mems = {
    "clock" : "clock",
    "stall_in" : "stall_all_src",
}

mem_predeclared_ports_per_mem = {
    "GET" : {
        "running" : "running_FETCH",
    },
    "PUT" : {
        "running" : "running_STORE",
    },
    "REG" : { },
    "RAM" : { },
    "IMM" : { },
    "ROM_A" : { },
    "ROM_B" : { },
}

def gen_data_memories(gen_det, com_det, controls, dataMesh):

    com_det.arch_body += "\n-- Memories components\n"
    # Interate over all data memories
    for mem, config in gen_det.config["data_memories"].items():
        # Generate memory code
        if gen_det.concat_naming:
            module_name = gen_det.module_name + "_" + mem
        else:
            module_name = None

        config = mem_lib_lookup[mem].add_inst_config(
            mem,
            gen_det.config["instr_set"],
            {
                **config,
                "signal_padding" : gen_det.config["signal_padding"],
                "stallable" : gen_det.config["stallable"],
            }
        )
        sub_interface, sub_name = mem_lib_lookup[mem].generate_HDL(
            config=config,
            output_path=gen_det.output_path,
            module_name=module_name,
            concat_naming=gen_det.concat_naming,
            force_generation=gen_det.force_generation
        )

        mem_controls = mem_lib_lookup[mem].get_inst_controls(mem, mem + "_", gen_det.config["instr_set"], sub_interface, config)
        controls = gen_utils.merge_controls( controls, mem_controls )
        control_ports = {}
        try:
            for control in mem_controls["fetch"].keys():
                control_ports[control[len(mem + "_"):]] = control
        except KeyError:
            pass
        try:
            for control in mem_controls["store"].keys():
                control_ports[control[len(mem + "_"):]] = control
        except KeyError:
            pass


        if gen_det.config["data_memories"][mem]["cross_lane"]:
            instance_data_mem(gen_det, com_det, mem, mem, sub_name, sub_interface, control_ports, True)

            # Handle dataMesh and controls
            unlaned_dataMesh = mem_lib_lookup[mem].get_inst_dataMesh(mem, mem + "_", gen_det.config["instr_set"], sub_interface, config, gen_det.config["SIMD"]["lanes_names"][0])
            laned_dataMesh = gen_utils.DataMesh()

            # Add lane fanning out code
            assert len(gen_det.config["SIMD"]["lanes_names"][1:]) == 0

            laned_dataMesh = unlaned_dataMesh
            # for vbus_name, vbus in unlaned_dataMesh.get_all_vbuses().items():
            #     for lane in gen_det.config["SIMD"]["lanes_names"][1:]:
            #         new_vbus_name = vbus_name.replace(gen_det.config["SIMD"]["lanes_names"][0], lane)
            #         laned_dataMesh.add_vbus(new_vbus_name, copy.deepcopy(vbus))

            dataMesh = dataMesh.merge(laned_dataMesh)

        else:
            for lane in gen_det.config["SIMD"]["lanes_names"]:
                inst = lane + mem
                instance_data_mem(gen_det, com_det, mem, lane + mem, sub_name, sub_interface, control_ports, lane == gen_det.config["SIMD"]["lanes_names"][0])

                # Handle dataMesh and controls
                lansd_dataMesh = mem_lib_lookup[mem].get_inst_dataMesh(mem, inst + "_", gen_det.config["instr_set"], sub_interface, config, lane)
                dataMesh = dataMesh.merge(lansd_dataMesh)

    return controls, dataMesh

def instance_data_mem(gen_det, com_det, mem, inst, sub_name, sub_interface, control_ports, declare_controls):

    # instantiate memory
    com_det.arch_body += "\n%s : entity work.%s(arch)@>\n"%(inst, sub_name)

    if len(sub_interface["generics"]) != 0:
        com_det.arch_body += "generic map (@>\n"

        for generic in sorted(sub_interface["generics"]):
            details = sub_interface["generics"][generic]
            com_det.ripple_generic(inst + "_" + generic, details)
            com_det.arch_body += "%s => %s_%s,\n"%(generic, inst, generic)

        com_det.arch_body.drop_last(2)
        com_det.arch_body += "@<\n)\n"

    com_det.arch_body += "port map (@>\n"

    # Handle all ports
    for port in sorted(sub_interface["ports"].keys()):
        # Handle predeclared common to all mems ports
        if   port in mem_predeclared_ports_all_mems.keys():
            com_det.arch_body += "%s => %s,\n"%(port, mem_predeclared_ports_all_mems[port], )
        # Handle predeclared for spific mem ports
        elif port in mem_predeclared_ports_per_mem[mem].keys():
            com_det.arch_body += "%s => %s,\n"%(port, mem_predeclared_ports_per_mem[mem][port], )
        # Handle control ports
        elif port in control_ports.keys():
            if declare_controls:
                detail = sub_interface["ports"][port]
                try:
                    com_det.arch_head += "signal %s : %s(%i downto 0);\n"%(control_ports[port], detail["type"], detail["width"] -1, )
                except KeyError:
                    com_det.arch_head += "signal %s : %s;\n"%(control_ports[port], detail["type"])

            com_det.arch_body += "%s => %s,\n"%(port, control_ports[port], )
        # Handle rippled up ports
        elif port.startswith("FIFO_"):
            com_det.ripple_port(inst + "_" + port, sub_interface["ports"][port])
            com_det.arch_body += "%s => %s_%s,\n"%(port, inst, port)
        else:
            detail = sub_interface["ports"][port]
            try:
                com_det.arch_head += "signal %s_%s : %s(%i downto 0);\n"%(inst, port, detail["type"], detail["width"] - 1, )
            except KeyError:
                com_det.arch_head += "signal %s_%s : %s;\n"%(inst, port, detail["type"])

            com_det.arch_body += "%s => %s_%s,\n"%(port, inst, port)

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "@<\n);\n"

    com_det.arch_body += "@<\n"

    # Check for stall out port
    if "stall_out" in sub_interface["ports"].keys():
        gen_det.config["stall_sources"].append("%s_stall_out"%(inst, ))

#####################################################################

addr_sources_predeclared_ports = {
    "clock" : "clock" ,
    "stall_in" : "stall_all_src",
}

def gen_addr_sources(gen_det, com_det, controls, dataMesh):

    com_det.arch_body += "\n-- Address components\n"
    for bam, config in gen_det.config["address_sources"].items():
        if gen_det.concat_naming:
            module_name = gen_det.module_name + "_" + bam
        else:
            module_name = None

        config = BAM.add_inst_config(
            bam,
            gen_det.config["instr_set"],
            {
                **config,
                "signal_padding" : gen_det.config["signal_padding"],
                "stallable" : gen_det.config["stallable"],
            }
        )
        interface, name = BAM.generate_HDL(
            config=config,
            output_path=gen_det.output_path,
            module_name=module_name,
            concat_naming=gen_det.concat_naming,
            force_generation=gen_det.force_generation
        )
        if "required_stages" in interface.keys():
            # Shgould be replaced with a more rebust way to accumalte require stages,
            # however as this the only place a stage may be added and for time this hardcoding is being used, Sorry. Nat
            assert interface["required_stages"] == ["prefetch",]
            gen_det.config["pipeline_stages"] = ["PM", "ID", "PREFETCH", "FETCH", "EXE", "STORE"]

        com_det.arch_body += "\n%s : entity work.%s(arch)@>\n"%(bam, name)

        if len(interface["generics"]) != 0:
            com_det.arch_body += "generic map (@>\n"

            for generic in sorted(interface["generics"]):
                details = interface["generics"][generic]
                com_det.ripple_generic(bam + "_" + generic, details)
                com_det.arch_body += "%s => %s_%s,\n"%(generic, bam, generic)

            com_det.arch_body.drop_last(2)
            com_det.arch_body += "@<\n)\n"

        com_det.arch_body += "port map (@>\n"

        # Handle predeclared ports
        for port, signal in addr_sources_predeclared_ports.items():
            if port in interface["ports"].keys():
                com_det.arch_body += "%s => %s,\n"%(port, signal)

        # Handle non predeclared ports
        for port in sorted(interface["ports"].keys()):
            if port not in addr_sources_predeclared_ports.keys():
                details = interface["ports"][port]
                try:
                    com_det.arch_head += "signal %s_%s : %s(%i downto 0);\n"%(bam, port, details["type"], details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s_%s : %s;\n"%(bam, port, details["type"], )

                com_det.arch_body += "%s => %s_%s,\n"%(port, bam, port, )

        com_det.arch_body.drop_last(2)
        com_det.arch_body += "@<\n);\n"

        com_det.arch_body += "@<\n"

        # Check for stall out port
        if "stall_out" in interface["ports"].keys():
            gen_det.config["stall_sources"].append("%s_stall_out"%(bam, ))

        controls = gen_utils.merge_controls( controls, BAM.get_inst_controls(bam, bam + "_", gen_det.config["instr_set"], interface, config) )

        # Handle dataMesh and controls
        unlaned_dataMesh = BAM.get_inst_dataMesh(bam, bam + "_", gen_det.config["instr_set"], interface, config, gen_det.config["SIMD"]["lanes_names"][0])
        laned_dataMesh = gen_utils.DataMesh()

        # Add lane fanning out code
        assert len(gen_det.config["SIMD"]["lanes_names"][1:]) == 0
        laned_dataMesh = unlaned_dataMesh
        # for vbus_name, vbus in undataMesh.get_all_vbuses().items():
        #     for lane in gen_det.config["SIMD"]["lanes_names"][1:]:
        #         new_vbus_name = vbus_name.replace(gen_det.config["SIMD"]["lanes_names"][0], lane)
        #         laned_dataMesh.add_vbus(new_vbus_name, copy.deepcopy(vbus))

        dataMesh = dataMesh.merge(laned_dataMesh)

    return controls, dataMesh

#####################################################################

def gen_predecode_pipeline(gen_det, com_det, controls, dataMesh):

    com_det.arch_body += "\n-- Program fetch components\n"

    controls, dataMesh = gen_program_counter(gen_det, com_det, controls, dataMesh)

    if "hidden_ZOLs" in gen_det.config["program_flow"].keys() and len(gen_det.config["program_flow"]["hidden_ZOLs"]):
        controls, dataMesh = gen_hidden_ZOLs(gen_det, com_det, controls, dataMesh)

    if "declared_ZOLs" in gen_det.config["program_flow"].keys() and len(gen_det.config["program_flow"]["declared_ZOLs"]):
        controls, dataMesh = gen_declared_ZOLs(gen_det, com_det, controls, dataMesh)

    if "rep_bank" in gen_det.config["program_flow"].keys() and len(gen_det.config["program_flow"]["rep_bank"]["loops"]):
        controls, dataMesh = gen_repeat_bank_loops(gen_det, com_det, controls, dataMesh)

    gen_program_memory(gen_det, com_det)

    return controls, dataMesh

PC_predeclared_ports = {
    "clock" : "clock",
    "stall_in" : "stall_all_src",
    "kickoff" : "kickoff",
}

def gen_program_counter(gen_det, com_det, controls, dataMesh):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_PC"
    else:
        module_name = None

    config = PC.add_inst_config(
        "PC",
        gen_det.config["instr_set"],
        {
            **gen_det.config["program_flow"],

            "stallable" : gen_det.config["stallable"],
        }
    )

    interface, name = PC.generate_HDL(
        config=config,
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    # controls
    dataMesh = dataMesh.merge(PC.get_inst_dataMesh("PC", "", gen_det.config["instr_set"], interface, config, gen_det.config["SIMD"]["lanes_names"][0]) )
    controls  = gen_utils.merge_controls( controls , PC.get_inst_controls("PC", "", gen_det.config["instr_set"], interface, config) )

    gen_det.config["program_flow"]["PC_width"] = interface["ports"]["value"]["width"]

    com_det.arch_body += "\nPC : entity work.%s(arch)@>\n"%(name)

    if len(interface["generics"]) != 0:
        com_det.arch_body += "generic map (@>\n"

        for generic in sorted(interface["generics"].keys()):
            details = interface["generics"][generic]
            com_det.ripple_generic("PC_" + generic, details)
            com_det.arch_body += "%s => PC_%s,\n"%(generic, generic)

        com_det.arch_body.drop_last(2)
        com_det.arch_body += "@<\n)\n"

    com_det.arch_body += "port map (@>\n"

    # Handle predeclared ports
    for port, signal in PC_predeclared_ports.items():
        if port in interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal)

    # Handle non predeclared ports
    for port, details  in interface["ports"].items():
        if port not in PC_predeclared_ports.keys():
            try:
                com_det.arch_head += "signal PC_%s : %s(%i downto 0);\n"%(port, details["type"], details["width"] - 1, )
            except KeyError:
                com_det.arch_head += "signal PC_%s : %s;\n"%(port, details["type"])
            com_det.arch_body += "%s => PC_%s,\n"%(port, port)

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "@<\n);\n"

    com_det.arch_body += "@<\n\n"

    for port, signal in enumerate(config["overwrite_sources"]):
        com_det.arch_head += "signal %s_value : std_logic_vector(%i downto 0);\n"%(signal, gen_det.config["program_flow"]["PC_width"] - 1, )
        com_det.arch_body += "PC_overwrite_source_%i_value <= %s_value;\n\n"%(port, signal, )

        com_det.arch_head += "signal %s_overwrite : std_logic;\n"%(signal, )
        com_det.arch_body += "PC_overwrite_source_%i_enable <= %s_overwrite;\n"%(port, signal, )

    if "PC_only_jump" in config["jump_drivers"]:
        com_det.arch_head += "signal PC_only_jump : std_logic;\n"
    for port, signal in enumerate(config["jump_drivers"]):
        com_det.arch_body += "PC_jump_driver_%i <= %s;\n"%(port, signal, )


    # Handle kickoff input
    com_det.add_port("kickoff", "std_logic", "in")

    return controls, dataMesh

# Key is port name, value signal name
ZOL_predeclared_ports = {
    "clock" : "clock",
    "stall_in" : "stall_all_src",
    "PC_value" : "PC_value",
    "PC_running" : "PC_running",
}

ZOL_declared_ports = [
    "overwrite_PC_enable", "overwrite_PC_value",
    "seek_check_value", "seek_overwrite_value", "seek_enable",
    "set_overwrites", "set_enable",
]

def gen_hidden_ZOLs(gen_det, com_det, controls, dataMesh):
    ZOLs = {"hidden_ZOL_" + str(k) : v for k, v in gen_det.config["program_flow"]["hidden_ZOLs"].items()}

    controls, dataMesh, overwrites_encoding, overwrite_signal, value_signal = gen_zero_overhead_loops(gen_det, com_det, controls, dataMesh, ZOLs, "hidden_ZOLs")
    com_det.add_interface_item("hidden_ZOLs_overwrites_encoding", overwrites_encoding)
    com_det.arch_body += "hidden_ZOLs_overwrite <= %s;\n"%(overwrite_signal, )
    com_det.arch_body += "hidden_ZOLs_value <= %s;\n\n"%(value_signal, )

    return controls, dataMesh

def gen_declared_ZOLs(gen_det, com_det, controls, dataMesh):
    ZOLs = gen_det.config["program_flow"]["declared_ZOLs"]

    controls, dataMesh, overwrites_encoding, overwrite_signal, value_signal = gen_zero_overhead_loops(gen_det, com_det, controls, dataMesh, ZOLs, "declared_ZOLs")
    com_det.add_interface_item("declared_ZOLs_overwrites_encoding", overwrites_encoding)
    com_det.arch_body += "declared_ZOLs_overwrite <= %s;\n"%(overwrite_signal, )
    com_det.arch_body += "declared_ZOLs_value <= %s;\n\n"%(value_signal, )

    return controls, dataMesh

def gen_zero_overhead_loops(gen_det, com_det, controls, dataMesh, ZOLs, muxing_prefix):

    overwrites_encoding = {}

    # Generate ZOL hardward
    for ZOL_name, ZOL_details in ZOLs.items():
        if gen_det.concat_naming:
            module_name = gen_det.module_name + "_" + ZOL_name
        else:
            module_name = None

        ZOL_details = ZOL.add_inst_config(ZOL_name, gen_det.config["instr_set"], ZOL_details)
        interface, name = ZOL.generate_HDL(
            {
                **ZOL_details,
                "PC_width"  : gen_det.config["program_flow"]["PC_width"],
                "signal_padding" : gen_det.config["signal_padding"],
                "stallable" : gen_det.config["stallable"],
            },
            output_path=gen_det.output_path,
            module_name=module_name,
            concat_naming=gen_det.concat_naming,
            force_generation=gen_det.force_generation
        )
        overwrites_encoding[ZOL_name] = interface["overwrites_encoding"]


        com_det.arch_body += "\n%s : entity work.%s(arch)@>\n"%(ZOL_name, name, )

        if len(interface["generics"]) != 0:
            com_det.arch_body += "generic map (@>\n"

            for generic in sorted(interface["generics"].keys()):
                details = interface["generics"][generic]
                com_det.ripple_generic(ZOL_name + "_" + generic, details)
                com_det.arch_body += "%s => %s_%s,\n"%(generic, ZOL_name, generic, )

            com_det.arch_body.drop_last(2)
            com_det.arch_body += "@<\n)\n"

        com_det.arch_body += "port map (@>\n"

        if __debug__:
            for port in interface["ports"]:
                assert (    port in ZOL_predeclared_ports.keys()
                        or  port in ZOL_declared_ports
                    ), "Unknown Port, " + port

        # Handle predeclared ports
        for port, signal in ZOL_predeclared_ports.items():
            if port in interface["ports"]:
                com_det.arch_body += "%s => %s,\n"%(port, signal, )

        # Handle declared ports
        for port in ZOL_declared_ports:
            if port in interface["ports"]:
                details = interface["ports"][port]
                try:
                    com_det.arch_head += "signal %s_%s : %s(%i downto 0);\n"%(ZOL_name, port, details["type"], details["width"] - 1, )
                except KeyError:
                    com_det.arch_head += "signal %s_%s : %s;\n"%(ZOL_name, port, details["type"], )
                com_det.arch_body += "%s => %s_%s,\n"%(port, ZOL_name, port, )

        com_det.arch_body.drop_last(2)
        com_det.arch_body += "@<\n);\n"

        com_det.arch_body += "@<\n\n"

        # Handle dataMesh and controls
        dataMesh = dataMesh.merge(ZOL.get_inst_dataMesh(ZOL_name, ZOL_name + "_", gen_det.config["instr_set"], interface, ZOL_details, gen_det.config["SIMD"]["lanes_names"][0]))
        controls = gen_utils.merge_controls(controls, ZOL.get_inst_controls(ZOL_name, ZOL_name + "_", gen_det.config["instr_set"], interface, ZOL_details) )

    # Build mux tree for ZOL overwrite and values
    if len(ZOLs) == 1:
        # Connect end of mux and or tree to PC
        overwrite_signal = "%s_overwrite_PC_enable"%(list(ZOLs.keys())[0], )
        value_signal = "%s_overwrite_PC_value"%(list(ZOLs.keys())[0], )
    elif len(ZOLs) > 1:
        _, mux_2 = mux.generate_HDL(
            {
                "inputs" : 2
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )


        lavel = 0
        value_width = gen_det.config["program_flow"]["PC_width"]
        mux_ends = [(zol + "_overwrite_PC_enable", zol + "_overwrite_PC_value", ) for zol in ZOLs.keys() ]
        while len(mux_ends) > 1:
            mux_ends_new = []
            for pair, ((a_enable, a_value), (b_enable, b_value)) in enumerate(zip(mux_ends[0::2], mux_ends[1::2])):
                com_det.arch_head += "signal %s_overwrite_%i_%i : std_logic;\n"%(muxing_prefix, lavel, pair, )
                com_det.arch_body += "%s_overwrite_%i_%i <=  %s or %s;\n"%(muxing_prefix, lavel, pair, a_enable, b_enable, )

                com_det.arch_body += "%s_value_mux_%i_%i : entity work.%s(arch)@>\n"%(muxing_prefix, lavel, pair, mux_2, )
                com_det.arch_body += "generic map (data_width => %i)\n"%(value_width, )
                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => %s,\n"%(b_enable, )
                com_det.arch_body += "data_in_0 => %s,\n"%(a_value, )
                com_det.arch_body += "data_in_1 => %s,\n"%(b_value, )

                com_det.arch_head += "signal %s_value_mux_%i_%i_out : std_logic_vector(%i downto 0);\n"%(muxing_prefix, lavel, pair, value_width - 1, )
                com_det.arch_body += "data_out => %s_value_mux_%i_%i_out\n"%(muxing_prefix, lavel, pair, )

                com_det.arch_body += "@<);\n@<\n"

                mux_ends_new.append(("%s_overwrite_%i_%i"%(muxing_prefix, lavel, pair, ), "%s_value_mux_%i_%i_out"%(muxing_prefix, lavel, pair, ), ) )

            if len(mux_ends) % 2 == 1:
                mux_ends_new.append(mux_ends[-1])

            mux_ends = mux_ends_new
            lavel += 1

        overwrite_signal = mux_ends[0][0]
        value_signal = mux_ends[0][1]

    return controls, dataMesh, overwrites_encoding, overwrite_signal, value_signal

repeat_bank_predeclared_ports = {
    "clock" : "clock",
    "stall_in" : "stall_rep_bank",
    "PC_value" : "PC_value",
    "PC_running" : "PC_running",
    "overwrite_value" : "rep_bank_overwrite_value",
    "overwrite_enable" : "rep_bank_overwrite_overwrite",
}

repeat_bank_declared_ports = [
    "stall_out",
]

def gen_repeat_bank_loops(gen_det, com_det, controls, dataMesh):
    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_" + "repeat_bank"
    else:
        module_name = None

    interface, name = REP.generate_HDL(
        {
            "subtype" : gen_det.config["program_flow"]["rep_bank"]["subtype"],
            "stall_on_id_change"  : gen_det.config["program_flow"]["rep_bank"]["stall_on_id_change"],
            "loops" : gen_det.config["program_flow"]["rep_bank"]["loops"],
            "PC_width"  : gen_det.config["program_flow"]["PC_width"],
            "stallable" : gen_det.config["stallable"],
        },
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )
    com_det.add_interface_item("rep_bank_preloaded_loop_id_encoding", interface["rep_bank_preloaded_loop_id_encoding"])
    com_det.add_interface_item("rep_bank_preloaded_pc_values_encoding", interface["rep_bank_preloaded_pc_values_encoding"])
    com_det.add_interface_item("rep_bank_preloaded_overwrites_encoding", interface["rep_bank_preloaded_overwrites_encoding"])

    com_det.arch_body += "repeat_bank : entity work.%s(arch)@>\n"%(name, )

    com_det.arch_body += "generic map (@>\n"

    for generic in sorted(interface["generics"].keys()):
        details = interface["generics"][generic]
        com_det.ripple_generic("rep_bank_" + generic, details, )
        com_det.arch_body += "%s => rep_bank_%s,\n"%(generic, generic, )

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "@<\n)\n"

    com_det.arch_body += "port map (@>\n"

    if __debug__:
        for port in interface["ports"]:
            assert (    port in repeat_bank_predeclared_ports.keys()
                    or  port in repeat_bank_declared_ports
                ), "Unknown Port, " + port

    # Handle predeclared ports
    for port, signal in repeat_bank_predeclared_ports.items():
        if port in interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal, )

    # Handle declared ports
    for port in repeat_bank_declared_ports:
        if port in interface["ports"]:
            details = interface["ports"][port]
            try:
                com_det.arch_head += "signal rep_bank_%s : %s(%i downto 0);\n"%(port, details["type"], details["width"] - 1, )
            except KeyError:
                com_det.arch_head += "signal rep_bank_%s : %s;\n"%(port, details["type"], )
            com_det.arch_body += "%s => rep_bank_%s,\n"%(port, port, )

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "@<\n);\n"

    com_det.arch_body += "@<\n\n"

    # Update stalling structs
    if "stall_out" in interface["ports"].keys():
        gen_det.config["stall_sources"].append("rep_bank_stall_out")
    if "stall_in" in interface["ports"].keys():
        gen_det.config["stalls"]["stall_rep_bank"] = ["rep_bank_stall_out", ]


    return controls, dataMesh

def gen_program_memory(gen_det, com_det):

    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_PM"
    else:
        module_name = None

    interface, name = ROM.generate_HDL(
        {
            "depth" : gen_det.config["program_flow"]["program_length"],
            "addr_width" : gen_det.config["program_flow"]["PC_width"],
            "data_width" : gen_det.config["instr_decoder"]["instr_width"],
            "buffer_reads" : True,
            "type" : "DIST",
            "reads" : 1,
            "stallable" : gen_det.config["stallable"],
        },
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "\nPM : entity work.%s(arch)@>\n"%(name)
    com_det.add_generic("PM_init_mif", "string")

    com_det.arch_body += "generic map (@>\n"
    com_det.arch_body += "init_mif => PM_init_mif\n"
    com_det.arch_body += "@<)\n"

    com_det.arch_head += "signal PM_addr : std_logic_vector(%i downto 0);\n"%( gen_det.config["program_flow"]["PC_width"] - 1)
    com_det.arch_head += "signal PM_data : std_logic_vector(%i downto 0);\n"%( gen_det.config["instr_decoder"]["instr_width"] - 1)

    com_det.arch_body += "port map (@>\n"
    com_det.arch_body += "clock => clock,\n"
    if gen_det.config["stallable"]:
        com_det.arch_body += "stall_in => stall_all_src,\n"
    com_det.arch_body += "read_0_addr => PM_addr,\n"
    com_det.arch_body += "read_0_data => PM_data\n"
    com_det.arch_body += "@<);\n"

    com_det.arch_body += "@<\n"

    com_det.arch_body += "PM_addr <= PC_value;\n"

#####################################################################

def handle_datamesh(gen_det, com_det, controls, dataMesh):

    # Declare data paths for ID addrs
    # needs to happen before ID is generated so ID can be passed the mux controls
    dataMesh = declare_ID_addrs(gen_det, com_det, dataMesh)

    controls = gen_datapath_muxes(gen_det, com_det, controls, dataMesh)

    return controls


def declare_ID_addrs(gen_det, com_det, dataMesh):
    for instr in gen_det.config["instr_set"]:
        ID_addr = 0
        for read, access in enumerate(asm_utils.instr_fetches(instr)):
            addr_com = asm_utils.addr_com(asm_utils.access_addr(access))
            # Handle addresses from the instruction decoder
            if addr_com == "ID":
                for lane in gen_det.config["SIMD"]["lanes_names"]:
                    dataMesh.connect_driver(driver="ID_addr_%i_fetch"%(ID_addr, ),
                        channel="%sfetch_addr_%i"%(lane, read),
                        condition=instr,
                        stage="fetch", inplace_channel=True,
                        padding_type="unsigned", width=gen_det.config["instr_decoder"]["addr_widths"][ID_addr]
                    )
                ID_addr += 1
            # Handle addresses from a Block access manager, stated base/step
            elif gen_det.config["address_sources"][addr_com]["base_type"] == "ROM":
                for lane in gen_det.config["SIMD"]["lanes_names"]:
                    dataMesh.connect_driver(driver="ID_addr_%i_prefetch"%(ID_addr, ),
                        channel="%sprefetch_addr_%i"%(lane, read, ),
                        condition=instr,
                        stage="prefetch", inplace_channel=True,
                        padding_type="unsigned", width=gen_det.config["instr_decoder"]["addr_widths"][ID_addr]
                    )
                ID_addr += 1

        for write, access in enumerate(asm_utils.instr_stores(instr)):
            addr_com = asm_utils.addr_com(asm_utils.access_addr(access))
            # Handle addresses from the instruction decoder
            if addr_com == "ID":
                for lane in gen_det.config["SIMD"]["lanes_names"]:
                    dataMesh.connect_driver(driver="ID_addr_%i_store"%(ID_addr, ),
                        channel="%sstore_addr_%i"%(lane, write),
                        condition=instr,
                        stage="store", inplace_channel=True,
                        padding_type="unsigned", width=gen_det.config["instr_decoder"]["addr_widths"][ID_addr]
                    )

                ID_addr += 1
            # Handle addresses from a Block access manager, stated base/step
            elif gen_det.config["address_sources"][addr_com]["base_type"] == "ROM":
                for lane in gen_det.config["SIMD"]["lanes_names"]:
                    dataMesh.connect_driver(driver="ID_addr_%i_prefetch"%(ID_addr, ),
                        channel="%sprefetch_addr_%i"%(lane, write, ),
                        condition=instr,
                        stage="prefetch", inplace_channel=True,
                        padding_type="unsigned", width=gen_det.config["instr_decoder"]["addr_widths"][ID_addr]
                    )
                ID_addr += 1

    return dataMesh

def gen_datapath_muxes(gen_det, com_det, controls, dataMesh):

    datapaths = dataMesh.compute_datapaths()

    # Henerate connection VHDL for each sink
    for sink, details in datapaths.items():
        # Group together all the conditions that map to the same source
        sources = {}
        for condition, connection in details.get_connections():
            try:
                sources[connection.end()].append(condition)
            except KeyError:
                sources[connection.end()] = [condition, ]

        # Cennection required connection
        sink_width = details.get_fixed_width()
        num_sources = len(sources.keys())
        assert num_sources > 0
        if num_sources == 1:
            source = list(sources.keys())[0]
            connection = details.get_connection(sources[source][0])
            source_width = connection.width()
            padding_type = connection.padding_type()

            com_det.arch_body += "%s <= %s;\n\n"%(
                sink,
                gen_utils.connect_signals(source, source_width, sink_width, padding_type),
            )
        else:
            # Generate mux component
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs"  : num_sources,
                },
                output_path=gen_det.output_path,
                module_name=None,
                concat_naming=False,
                force_generation=gen_det.force_generation
            )

            # Instaniate Mux, while generating control sel_signal
            control_signal = sink + "_mux_sel"
            control_width = mux_interface["sel_width"]

            com_det.arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(control_signal, control_width - 1, )
            com_det.arch_head += "signal %s_mux_out : std_logic_vector(%i downto 0);\n"%(sink, sink_width - 1, )

            com_det.arch_body += "%s_mux : entity work.%s(arch)@>\n"%(sink, mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(sink_width, )

            com_det.arch_body += "port map (\n@>"
            com_det.arch_body += "sel =>  %s,\n"%(control_signal, )

            # Handle connected input ports
            control_values = {}
            for sel_value, (source, instrs) in enumerate(sources.items()):
                details.get_connection(sources[source][0])

                source_width = max([details.get_connection(instr).width() for instr in instrs])
                padding_type = details.get_connection(instrs[0]).padding_type()
                if __debug__:
                    for instr in instrs[1:]:
                        assert padding_type == details.get_connection(instr).padding_type()

                control_value = tc_utils.unsigned.encode(sel_value, control_width)
                control_values[control_value] = instrs

                com_det.arch_body += "data_in_%i => %s,\n"%(
                    sel_value,
                    gen_utils.connect_signals(source, source_width, sink_width, padding_type),
                )

            # Pull down unconnected input ports
            for sel_value in range(num_sources, mux_interface["number_inputs"]):
                com_det.arch_body += "data_in_%i => (others => '0'),\n"%(sel_value, )

            com_det.arch_body += "data_out => %s_mux_out\n"%(sink)

            com_det.arch_body += "@<);\n@<\n"

            # Connect mux output to sink signal
            com_det.arch_body += "%s <= %s_mux_out;\n"%(sink, sink, )

            # Default any inused instrs to all 0
            gen_utils.add_control(controls, details.get_stage(), control_signal, control_values, "std_logic_vector", control_width)

    return controls

#####################################################################

ID_predeclared_ports = {
    "clock" : "clock",
    "stall_in" : "stall_all_src",
}

ID_non_fanout_ports = [
    "instr",
    "enable",
]

def gen_instr_decoder(gen_det, com_det, controls):

    if gen_det.concat_naming:
        module_name = gen_det.module_name + "_ID"
    else:
        module_name = None

    interface, name = ID.generate_HDL(
        {
            **gen_det.config,
            "controls" : controls
        },
        output_path=gen_det.output_path,
        module_name=module_name,
        concat_naming=gen_det.concat_naming,
        force_generation=gen_det.force_generation
    )

    com_det.arch_body += "\nID : entity work.%s(arch)@>\n"%(name, )

    com_det.arch_body += "port map (@>\n"

    # Handle predeclared ports
    for port, signal in ID_predeclared_ports.items():
        if port in interface["ports"]:
            com_det.arch_body += "%s => %s,\n"%(port, signal, )

    # Handle prefixed ports
    for port in sorted(interface["ports"].keys()):
        if port not in ID_predeclared_ports.keys():
            details = interface["ports"][port]
            try:
                com_det.arch_head += "signal ID_%s : %s(%i downto 0);\n"%(port, details["type"], details["width"] - 1, )
            except Exception as e:
                com_det.arch_head += "signal ID_%s : %s;\n"%(port, details["type"], )
            com_det.arch_body += "%s => ID_%s,\n"%(port, port, )

    com_det.arch_body.drop_last(2)
    com_det.arch_body += "@<\n);\n"

    com_det.arch_body += "@<\n"

    com_det.arch_body += "ID_instr <= PM_data;\n"
    com_det.arch_body += "ID_enable <= running_ID;\n"

    # Handle PC control signals
    for port in sorted(interface["ports"]):
        if port.startswith("jump_") or (port.startswith("update_") and port.endswith("_statuses")):
            com_det.arch_body += "PC_%s <= ID_%s;\n"%(port, port, )

    # Handle fanning out control signals
    for port in sorted(interface["ports"]):
        if (
            port not in ID_predeclared_ports.keys()
            and port not in ID_non_fanout_ports
            and not port.startswith("addr_")
            and not port.startswith("jump_")
            and not (port.startswith("update_") and port.endswith("_statuses"))
        ):
            com_det.arch_body += "%s <= ID_%s;\n"%(port, port, )

#####################################################################

def gen_running_delays(gen_det, com_det):

    # Handle running output
    com_det.add_port("running", "std_logic", "out")
    com_det.arch_body += "running <= PC_running;\n\n"

    # Declare each stage's running signal
    for stage in gen_det.config["pipeline_stages"]:
        com_det.arch_head += "signal running_%s : std_logic;\n"%(stage, )

    com_det.arch_body += "running_%s <= PC_running;\n"%(gen_det.config["pipeline_stages"][0], )

    DELAY_INTERFACE, DELAY_NAME = delay.generate_HDL(
        {
            "width" : 1,
            "depth" : 1,
            "has_enable" : gen_det.config["stallable"],
            "inited" : True,
        },
        output_path=gen_det.output_path,
        module_name=None,
        concat_naming=False,
        force_generation=gen_det.force_generation
    )

    for i, (stage_in, stage_out) in enumerate(zip(gen_det.config["pipeline_stages"][:-1], gen_det.config["pipeline_stages"][1:])):
        com_det.arch_body += "running_delay_%i : entity work.%s(arch)@>\n"%(i, DELAY_NAME, )

        com_det.arch_body += "generic map (init_value => 0)\n"

        com_det.arch_body += "port map (\n@>"

        com_det.arch_body += "clock => clock,\n"
        if gen_det.config["stallable"]:
            com_det.arch_body += "enable => not stall_all_src,\n"
        com_det.arch_body += "data_in (0) => running_%s,\n"%(stage_in, )
        com_det.arch_body += "data_out(0) => running_%s\n"%(stage_out, )
        com_det.arch_body += "@<);@<\n\n"
