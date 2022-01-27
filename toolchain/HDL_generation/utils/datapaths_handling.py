from FPE.toolchain import utils as tc_utils

from .controls_handling import *
from .connection_handling import *

from FPE.toolchain.HDL_generation.basic import mux

# Current datapath structures
# datapath : {
#     meta_signal : {
#         "stage"   : str
#         "padding_type" : str,
#         "srcs" : {
#             instr : {
#               "signal" : str,
#               "width" : int | None,
#         }
#         "dsts" L {
#             signal : {
#                "width" : int | None,
#                "instrs" : [instr, ],
#            }
#         }
#     }
# }

def init_datapaths():
    datapath = {}

    return datapath

def add_datapath(datapath, meta_signal, stage, src_dst, instr, signal, padding_type, width=None):

    assert type(datapath) == dict
    assert type(meta_signal) == str
    assert type(stage) == str
    assert type(src_dst) == bool
    assert type(instr) == str
    assert type(signal) == str
    assert type(padding_type) == str
    assert width == None or type(width) == int

    if src_dst:
        # Source
        try:
            assert datapath[meta_signal]["stage"] == stage
            assert datapath[meta_signal]["padding_type"] == padding_type
            datapath[meta_signal]["srcs"][instr] = { "signal" : signal, "width" : width, }
        except KeyError:
            datapath[meta_signal] = {
                "stage" : stage,
                "padding_type" : padding_type,
                "srcs" : {
                    instr : { "signal" : signal, "width" : width, },
                },
                "dsts" : { },
            }
    else:
        # Destination
        try:
            assert datapath[meta_signal]["stage"] == stage
            assert datapath[meta_signal]["padding_type"] == padding_type
            assert datapath[meta_signal]["dsts"][signal]["width"] == width
            datapath[meta_signal]["dsts"][signal]["instrs"].append(instr)
        except KeyError:
            try:
                assert datapath[meta_signal]["stage"] == stage
                assert datapath[meta_signal]["padding_type"] == padding_type
                datapath[meta_signal]["dsts"][signal] = {
                    "width" : width,
                    "instrs" : [instr, ]
                }
            except KeyError:
                datapath[meta_signal] = {
                    "stage" : stage,
                    "padding_type" : padding_type,
                    "srcs" : { },
                    "dsts" : {
                        signal : {
                            "width" : width,
                            "instrs" : [instr, ]
                        }
                    },
                }

def merge_datapaths(A, B):
    C = init_datapaths()

    for meta_signal, meta_signal_details in A.items():
        stage = meta_signal_details["stage"]
        padding_type = meta_signal_details["padding_type"]
        for instr, instr_details in meta_signal_details["srcs"].items():
            width = instr_details["width"]
            signal = instr_details["signal"]
            add_datapath(C, meta_signal, stage, True, instr, signal, padding_type, width)
        for signal, signal_details in meta_signal_details["dsts"].items():
            width = signal_details["width"]
            for instr in signal_details["instrs"]:
                add_datapath(C, meta_signal, stage, False, instr, signal, padding_type, width)

    for meta_signal, meta_signal_details in B.items():
        stage = meta_signal_details["stage"]
        padding_type = meta_signal_details["padding_type"]
        for instr, instr_details in meta_signal_details["srcs"].items():
            width = instr_details["width"]
            signal = instr_details["signal"]
            add_datapath(C, meta_signal, stage, True, instr, signal, padding_type, width)
        for signal, signal_details in meta_signal_details["dsts"].items():
            width = signal_details["width"]
            for instr in signal_details["instrs"]:
                add_datapath(C, meta_signal, stage, False, instr, signal, padding_type, width)

    return C


def gen_datapath_muxes(DATAPATHS, OUTPUT_PATH, FORCE_GENERATION, ARCH_HEAD, ARCH_BODY):
    controls = init_controls()

    for meta_signal, meta_signal_details in DATAPATHS.items():
        stage = meta_signal_details["stage"]
        padding_type = meta_signal_details["padding_type"]
        for dst_signal, dst_details in meta_signal_details["dsts"].items():
            # unpack dst_details
            dst_width = dst_details["width"]
            instrs = dst_details["instrs"]

            # Build source table
            srcs = {}
            for instr in instrs:
                src_details = meta_signal_details["srcs"][instr]
                src_signal = src_details["signal"]
                src_width  = src_details["width"]
                try:
                    assert src_width == srcs[src_signal]["width"]
                    srcs[src_signal]["instrs"].append(instr)
                except KeyError:
                    srcs[src_signal] = {
                        "width"  : src_width,
                        "instrs" : [instr, ],
                    }

            # Connect srcs to dst
            num_input = len(srcs)
            if   num_input == 0:
                raise ValueError("dst_signal with no inputs, "%(dst_signal, ) )
            elif num_input == 1:
                # Single source therefor no muxing required
                ARCH_BODY += "%s <= %s;\n"%(dst_signal, connect_signals(src_signal, src_width, dst_width, padding_type), )
            else:
                # Multiple sources, therefore use mux

                # Generate mux component
                mux_interface, mux_name = mux.generate_HDL(
                    {
                        "inputs"  : num_input,
                    },
                    OUTPUT_PATH,
                    module_name=None,
                    concat_naming=False,
                    force_generation=FORCE_GENERATION
                )

                # Instaniate Mux, while generating control sel_signal
                control_signal = dst_signal + "_mux_sel"
                control_width = mux_interface["sel_width"]

                control_values = {}

                ARCH_HEAD += "signal %s : std_logic_vector(%i downto 0);\n"%(control_signal, control_width - 1, )

                ARCH_BODY += "%s_muz : entity work.%s(arch)\>\n"%(dst_signal, mux_name, )

                ARCH_BODY += "generic map (data_width => %i)\n"%(dst_width, )

                ARCH_BODY += "port map (\n\>"
                ARCH_BODY += "sel =>  %s,\n"%(control_signal, )

                for sel_value, (src_signal, src_details) in enumerate(srcs.items()):
                    control_value = tc_utils.unsigned.encode(sel_value, control_width)
                    control_values[control_value] = src_details["instrs"]

                    src_width = src_details["width"]

                    ARCH_BODY += "data_in_%i => %s,\n"%(
                        sel_value,
                        connect_signals(src_signal, src_width, dst_width, padding_type),
                    )

                ARCH_BODY += "data_out => %s\n"%(dst_signal)

                ARCH_BODY += "\<);\n\<\n"

                add_control(controls, stage, control_signal, control_values, "std_logic_vector", control_width)

    return controls, ARCH_HEAD, ARCH_BODY
