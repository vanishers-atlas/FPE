import warnings
import copy

from FPE.toolchain import utils as tc_utils

from .controls_handling import *
from .connection_handling import *

from FPE.toolchain.HDL_generation.basic import mux


# Current datapath structure
# datapath : {
#     "srcs" : {
#         meta_signal : {
#             instr : {
#               "stage"   : str
#               "padding_type" : str,
#               "signal" : str,
#               "width" : int | None,
#             }
#         }
#     }
#     "dests" L {
#         signal : {
#             instr : {
#               "stage"   : str
#               "padding_type" : str,
#               meta_signal : str,
#               "width" : int | None,
#             }
#        }
#     }
# }

def init_datapaths():
    datapath = {
        "srcs" : {},
        "dests" : {},
    }

    return datapath


def add_datapath_source(datapath, meta_signal, stage, instr, signal, padding_type, width=None):
    assert type(datapath) == dict
    assert type(meta_signal) == str
    assert type(stage) == str
    assert type(instr) == str
    assert type(signal) == str
    assert type(padding_type) == str
    assert width == None or type(width) == int

    try:
        assert instr not in datapath["srcs"][meta_signal], "A meta signal ca only have 1 source per instr"
        datapath["srcs"][meta_signal][instr] = {
            "stage" : stage,
            "padding_type" : padding_type,
            "signal" : signal,
            "width" : width,
        }
    except KeyError:
        try:
            datapath["srcs"][meta_signal] = {
                instr : {
                    "stage" : stage,
                    "padding_type" : padding_type,
                    "signal" : signal,
                    "width" : width,
                },
            }
        except KeyError as e:
            datapath["srcs"] = {
                meta_signal : {
                    instr : {
                        "stage" : stage,
                        "padding_type" : padding_type,
                        "signal" : signal,
                        "width" : width,
                    },
                },
            }

def add_datapath_dest(datapath, meta_signal, stage, instr, signal, padding_type, width=None):
    assert type(datapath) == dict
    assert type(meta_signal) == str
    assert type(stage) == str
    assert type(instr) == str
    assert type(signal) == str
    assert type(padding_type) == str
    assert width == None or type(width) == int

    try:
        assert instr not in datapath["dests"][signal], "A destination can only access 1 meta signal per instr"
        datapath["dests"][signal][instr] = {
            "stage" : stage,
            "padding_type" : padding_type,
            "meta_signal" : meta_signal,
            "width" : width,
        }
    except KeyError:
        try:
            datapath["dests"][signal] = {
                instr : {
                    "stage" : stage,
                    "padding_type" : padding_type,
                    "meta_signal" : meta_signal,
                    "width" : width,
                },
            }
        except KeyError as e:
            datapath["dests"] = {
                signal : {
                    instr : {
                        "stage" : stage,
                        "padding_type" : padding_type,
                        "meta_signal" : meta_signal,
                        "width" : width,
                    },
                },
            }

def add_datapath(datapath, meta_signal, stage, src_dst, instr, signal, padding_type, width=None):
    warnings.warn("Use of add_datapath is discoiraged, instead please use add_datapath_source and add_datapath_dest")

    assert type(src_dst) == bool

    if src_dst:
        add_datapath_source(datapath, meta_signal, stage, instr, signal, padding_type, width)
    else:
        add_datapath_dest(datapath, meta_signal, stage, instr, signal, padding_type, width)


def merge_datapaths(A, B):
    C = copy.deepcopy(A)

    for meta_signal, instrs in B["srcs"].items():
        for instr, details in instrs.items():
            stage = details["stage"]
            padding_type = details["padding_type"]
            signal = details["signal"]
            width = details["width"]
            add_datapath_source(C, meta_signal, stage, instr, signal, padding_type, width)

    for signal, instrs in B["dests"].items():
        for instr, details in instrs.items():
            stage = details["stage"]
            padding_type = details["padding_type"]
            meta_signal = details["meta_signal"]
            width = details["width"]
            add_datapath_dest(C, meta_signal, stage, instr, signal, padding_type, width)

    return C


def gen_datapath_muxes(datapath, output_path, force_generation, arch_head, arch_body):
    controls = init_controls()

    for dst_signal, instrs in datapath["dests"].items():
        sources = {}
        dst_padding_type = None
        dst_width = None

        for instr, details in instrs.items():
            stage = details["stage"]
            padding_type = details["padding_type"]
            meta_signal = details["meta_signal"]
            width = details["width"]

            if dst_padding_type == None:
                dst_padding_type = padding_type
            else:
                assert dst_padding_type == padding_type

            if dst_width == None:
                dst_width = width
            else:
                assert dst_width == width

            source = datapath["srcs"][meta_signal][instr]
            assert source["stage"] == stage
            src_width = source["width"]
            src_signal = source["signal"]
            if source["padding_type"] != padding_type:
                warnings.warn("Warning: Mismatch of padding_types when connecting %s(%s) to %s(%s)"%(src_signal, source["padding_type"], dst_signal, dst_padding_type, ))
            try:
                sources[src_signal]["instrs"].append(instr)
            except KeyError:
                sources[src_signal] = {
                    "instrs" : [instr, ],
                    "width" : src_width,
                }

        num_input = len(sources)
        if   num_input == 0:
            raise ValueError("dst_signal with no inputs, "%(dst_signal, ) )
        elif num_input == 1:
            # Single source therefor no muxing required
            arch_body += "%s <= %s;\n\n"%(dst_signal, connect_signals(src_signal, src_width, dst_width, padding_type), )
        else:
            # Multiple sources, therefore use mux

            # Generate mux component
            mux_interface, mux_name = mux.generate_HDL(
                {
                    "inputs"  : num_input,
                },
                output_path,
                module_name=None,
                concat_naming=False,
                force_generation=force_generation
            )

            # Instaniate Mux, while generating control sel_signal
            control_signal = dst_signal + "_mux_sel"
            control_width = mux_interface["sel_width"]

            control_values = {}

            arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(control_signal, control_width - 1, )

            arch_body += "%s_muz : entity work.%s(arch)\>\n"%(dst_signal, mux_name, )

            arch_body += "generic map (data_width => %i)\n"%(dst_width, )

            arch_body += "port map (\n\>"
            arch_body += "sel =>  %s,\n"%(control_signal, )

            for sel_value, (src_signal, src_details) in enumerate(sources.items()):
                control_value = tc_utils.unsigned.encode(sel_value, control_width)
                control_values[control_value] = src_details["instrs"]

                src_width = src_details["width"]

                arch_body += "data_in_%i => %s,\n"%(
                    sel_value,
                    connect_signals(src_signal, src_width, dst_width, padding_type),
                )

            for sel_value in range(len(sources), mux_interface["number_inputs"]):
                arch_body += "data_in_%i => (others => '0'),\n"%(sel_value, )

            arch_body += "data_out => %s\n"%(dst_signal)

            arch_body += "\<);\n\<\n"

            add_control(controls, stage, control_signal, control_values, "std_logic_vector", control_width)

    return controls, arch_head, arch_body
