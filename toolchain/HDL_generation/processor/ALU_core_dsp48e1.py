# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import warnings

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.basic import mux
from FPE.toolchain.HDL_generation.basic import register

#####################################################################

def add_inst_config(instr_id, instr_set, config):
    required_operands = 0
    DSP_mult_used = False
    DSP_C_used = False
    DSP_AB_used = False

    statuses = set()
    jumps = set()
    unsigned_compare = False
    signed_compare = False
    not_equal_jump_present = False
    sign_0_sources = set()
    sign_1_sources = set()

    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))

            if   mnemonic in ["MOV", "LSH", "RSH", "LRL", "RRL", "NOT", "PMOV", "PLSH", "PRSH", "PLRL", "PRRL", "PNOT", ]:
                required_operands = max(required_operands, 1)
                DSP_C_used = True
            elif mnemonic in ["ADD", "AND", "NAND", "OR", "NOR", "XOR", "XNOR", "PADD", "PAND", "PAND", "PNAND", "POR", "PNOR", "PXOR", "PXNOR", ]:
                required_operands = max(required_operands, 2)
                DSP_C_used = True
                DSP_AB_used = True
            elif mnemonic in ["MUL", ]:
                required_operands = max(required_operands, 2)
                DSP_mult_used = True
            elif mnemonic in ["SUB", "PSUB", ]:
                required_operands = max(required_operands, 2)
                DSP_C_used = True
                DSP_AB_used = True
            elif mnemonic in ["UCMP", ]:
                required_operands = max(required_operands, 2)
                DSP_C_used = True
                DSP_AB_used = True
                unsigned_compare = True

            elif mnemonic in ["SCMP", ]:
                required_operands = max(required_operands, 2)
                DSP_C_used = True
                DSP_AB_used = True
                signed_compare = True

                operands = asm_utils.instr_operands(instr)
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if operand_0_is_acc:
                    sign_0_sources.add("acc")
                else:
                    sign_0_sources.add("operand")

                if operand_1_is_acc:
                    sign_1_sources.add("acc")
                else:
                    sign_1_sources.add("operand")

            elif mnemonic in ["JEQ", ]:
                statuses.add("zero")

                jumps.add("equal")
            elif mnemonic in ["JNE", ]:
                not_equal_jump_present = True
            elif mnemonic in ["JGT", ]:
                statuses.add("zero")

                jumps.add("greater")
            elif mnemonic in ["JGE", ]:
                statuses.add("zero")

                jumps.add("greater")
                jumps.add("equal")
            elif mnemonic in ["JLT", ]:
                jumps.add("lesser")
            elif mnemonic in ["JLE", ]:
                statuses.add("zero")

                jumps.add("lesser")
                jumps.add("equal")
            else:
                raise ValueError("Unsupported mnemonic, " + mnemonic)

    if not_equal_jump_present:
        if "greater" in jumps or "lesser" in jumps:
            statuses.add("zero")

            jumps.add("greater")
            jumps.add("lesser")
        else:
            statuses.add("zero")

            jumps.add("not_equal")

    config["statuses"] = sorted(statuses)
    config["jumps"] = sorted(jumps)
    config["unsigned_compare"] = unsigned_compare
    config["signed_compare"] = signed_compare

    config["required_operands"] = required_operands
    config["operand_widths"] = [ 1 for _ in range(required_operands) ]

    config["DSP_mult_used"] = DSP_mult_used
    config["DSP_C_used"] = DSP_C_used
    config["DSP_AB_used"] = DSP_AB_used

    config["sign_0_sources"] = list(sign_0_sources)
    config["sign_1_sources"] = list(sign_1_sources)

    return config

def get_inst_dataMesh(instr_id, instr_prefix, instr_set, interface, config, lane):
    dataMesh = gen_utils.DataMesh()

    # Handle fetched_operand ports
    for instr in instr_set:
        if asm_utils.instr_mnemonic(instr)  in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
            dataMesh.connect_sink(sink="PC_jump_value",
                channel="%sfetch_data_0_word_0"%(lane, ),
                condition=instr,
                stage="exe", inplace_channel=True,
                padding_type="unsigned", width=config["jump_width"]
            )

    return dataMesh

def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    controls = {}

    # Handle acc_enable control
    acc_enable = { "0" : [], "1" : [], }
    for instr in instr_set:
        mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
        if   mnemonic in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
            acc_enable["0"].append(instr)
        elif instr_id in asm_utils.instr_exe_units(instr):
            acc_enable["1"].append(instr)
        else:
            acc_enable["0"].append(instr)
    gen_utils.add_control(controls, "exe", instr_prefix + "core_acc_enable", acc_enable, "std_logic")

    # Handle update_statuses control
    if "core_update_statuses" in interface["ports"].keys():
        update_statuses = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["UCMP", "SCMP", ]:
                update_statuses["1"].append(instr)
            else:
                update_statuses["0"].append(instr)
        gen_utils.add_control(controls, "store", instr_prefix + "core_update_statuses", update_statuses, "std_logic")

    # Handle jump controls
    if "core_CMP_sel" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["SCMP", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "store", instr_prefix + "core_CMP_sel", values, "std_logic")

    if "core_hold_operand_signs" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["SCMP", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "core_hold_operand_signs", values, "std_logic")

    if "core_jump_not_equal" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JNE", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "core_jump_not_equal", values, "std_logic")

    if "core_jump_equal" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JEQ", "JGE", "JLE", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "core_jump_equal", values, "std_logic")

    if "core_jump_greater" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JGT", "JGE", "JNE", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "core_jump_greater", values, "std_logic")

    if "core_jump_lesser" in interface["ports"].keys():
        values = { "0" : [], "1" : [], }
        for instr in instr_set:
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            if   mnemonic in ["JLT", "JLE", "JNE", ]:
                values["1"].append(instr)
            else:
                values["0"].append(instr)
        gen_utils.add_control(controls, "exe", instr_prefix + "core_jump_lesser", values, "std_logic")

    # Handle DSP controls
    ALU_mode = {}
    op_mode = {}
    for instr in instr_set:
        if instr_id in asm_utils.instr_exe_units(instr):
            mnemonic, *mnemonic_parts = asm_utils.mnemonic_decompose(asm_utils.instr_mnemonic(instr))
            operands = asm_utils.instr_operands(instr)

            # Pass through slice opers
            if   mnemonic in ["MOV", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"

                if not operand_0_is_acc:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => C   Y => 0   X => 0
                    try:
                        op_mode["0110000"].append(instr)
                    except Exception as e:
                        op_mode["0110000"] = [instr, ]
                else:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => P   Y => 0   X => 0
                    try:
                        op_mode["0100000"].append(instr)
                    except Exception as e:
                        op_mode["0100000"] = [instr, ]
            elif mnemonic in ["PMOV", ]:
                # P => Z + Y + X + CarryIn
                try:
                    ALU_mode["0000"].append(instr)
                except KeyError:
                    ALU_mode["0000"] = [instr, ]

                # Z => C   Y => 0   X => 0
                try:
                    op_mode["0110000"].append(instr)
                except Exception as e:
                    op_mode["0110000"] = [instr, ]
            elif mnemonic in ["LSH", "RSH", "LRL", "RRL", "PMOV", "PLSH", "PRSH", "PLRL", "PRRL", ]:
                # P => Z + Y + X + CarryIn
                try:
                    ALU_mode["0000"].append(instr)
                except KeyError:
                    ALU_mode["0000"] = [instr, ]

                # Z => C   Y => 0   X => 0
                try:
                    op_mode["0110000"].append(instr)
                except Exception as e:
                    op_mode["0110000"] = [instr, ]

            # Arithmetic Operations
            elif mnemonic in ["MUL", ]:
                # P => Z + Y + X + CarryIn
                try:
                    ALU_mode["0000"].append(instr)
                except KeyError:
                    ALU_mode["0000"] = [instr, ]

                # Z => 0   Y => M   X => M
                try:
                    op_mode["0000101"].append(instr)
                except Exception as e:
                    op_mode["0000101"] = [instr, ]
            elif mnemonic in ["ADD", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => C   Y => 0   X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => C   Y => 0   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => P   Y => 0   X => A:B
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => Z + Y + X + CarryIn
                    try:
                        ALU_mode["0000"].append(instr)
                    except KeyError:
                        ALU_mode["0000"] = [instr, ]

                    # Z => P   Y => 0   X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["PADD", ]:
                # P => Z + Y + X + CarryIn
                try:
                    ALU_mode["0000"].append(instr)
                except KeyError:
                    ALU_mode["0000"] = [instr, ]

                # Z => C   Y => 0   X => A:B
                try:
                    op_mode["0110011"].append(instr)
                except Exception as e:
                    op_mode["0110011"] = [instr, ]
            elif mnemonic in ["SUB", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => C   Y => 0   X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => C   Y => 0   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => P   Y => 0   X => A:B
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => P   Y => 0   X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["PSUB", ]:
                # P => Z - (Y + X + CarryIn)
                try:
                    ALU_mode["0011"].append(instr)
                except KeyError:
                    ALU_mode["0011"] = [instr, ]

                # Z => C   Y => 0   X => A:B
                try:
                    op_mode["0110011"].append(instr)
                except Exception as e:
                    op_mode["0110011"] = [instr, ]

            # jumping and comparism operations
            elif mnemonic in ["UCMP", "SCMP", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => C   Y => 0   X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => C   Y => 0   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => P   Y => 0   X => A:B
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => Z - (Y + X + CarryIn)
                    try:
                        ALU_mode["0011"].append(instr)
                    except KeyError:
                        ALU_mode["0011"] = [instr, ]

                    # Z => P   Y => 0   X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["JEQ", "JNE", "JGT", "JGE", "JLT", "JLE", ]:
                pass

            # Logical Operations
            elif mnemonic in ["NOT", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"

                if not operand_0_is_acc:
                    # P => X OR (NOT Z)
                    try:
                        ALU_mode["1101"].append(instr)
                    except KeyError:
                        ALU_mode["1101"] = [instr, ]

                    # Z => C   Y => all 1s   X => 0
                    try:
                        op_mode["0111000"].append(instr)
                    except Exception as e:
                        op_mode["0111000"] = [instr, ]
                else:
                    # P => X OR (NOT Z)
                    try:
                        ALU_mode["1101"].append(instr)
                    except KeyError:
                        ALU_mode["1101"] = [instr, ]

                    # Z => P   Y => all 1s   X => 0
                    try:
                        op_mode["0101000"].append(instr)
                    except Exception as e:
                        op_mode["0101000"] = [instr, ]
            elif mnemonic in ["PNOT", ]:
                # P => X OR (NOT Z)
                try:
                    ALU_mode["1101"].append(instr)
                except KeyError:
                    ALU_mode["1101"] = [instr, ]

                # Z => C   Y => all 1s   X => 0
                try:
                    op_mode["0111000"].append(instr)
                except Exception as e:
                    op_mode["0111000"] = [instr, ]

            elif mnemonic in ["AND", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => C   Y => used with ALU to select and   X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => C   Y => used with ALU to select and   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => P   Y => used with ALU to select and   X => A:B
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => P   Y => used with ALU to select and   X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["PAND", ]:
                # P => X and/or Z depening on Y op mod
                try:
                    ALU_mode["1100"].append(instr)
                except KeyError:
                    ALU_mode["1100"] = [instr, ]

                # Z => C   Y => used with ALU to select and   X => A:B
                try:
                    op_mode["0110011"].append(instr)
                except Exception as e:
                    op_mode["0110011"] = [instr, ]

            elif mnemonic in ["NAND", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => C   Y => used with ALU to select and   X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => C   Y => used with ALU to select and   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => P   Y => used with ALU to select and   X => A:B
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => P   Y => used with ALU to select and   X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["PNAND", ]:
                # P => X and/or Z depening on Y op mod
                try:
                    ALU_mode["1110"].append(instr)
                except KeyError:
                    ALU_mode["1110"] = [instr, ]

                # Z => C   Y => used with ALU to select and   X => A:B
                try:
                    op_mode["0110011"].append(instr)
                except Exception as e:
                    op_mode["0110011"] = [instr, ]

            elif mnemonic in ["OR", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => C   Y => used with ALU to select or   X => A:B
                    try:
                        op_mode["0111011"].append(instr)
                    except Exception as e:
                        op_mode["0111011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => C   Y => used with ALU to select or   X => P
                    try:
                        op_mode["0111010"].append(instr)
                    except Exception as e:
                        op_mode["0111010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => P   Y => used with ALU to select or   X => A:B
                    try:
                        op_mode["0101011"].append(instr)
                    except Exception as e:
                        op_mode["0101011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1100"].append(instr)
                    except KeyError:
                        ALU_mode["1100"] = [instr, ]

                    # Z => P   Y => used with ALU to select or   X => P
                    try:
                        op_mode["0101010"].append(instr)
                    except Exception as e:
                        op_mode["0101010"] = [instr, ]
            elif mnemonic in ["POR", ]:
                # P => X and/or Z depening on Y op mod
                try:
                    ALU_mode["1100"].append(instr)
                except KeyError:
                    ALU_mode["1100"] = [instr, ]

                # Z => C   Y => used with ALU to select or   X => A:B
                try:
                    op_mode["0111011"].append(instr)
                except Exception as e:
                    op_mode["0111011"] = [instr, ]

            elif mnemonic in ["NOR", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => C   Y => used with ALU to select or   X => A:B
                    try:
                        op_mode["0111011"].append(instr)
                    except Exception as e:
                        op_mode["0111011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => C   Y => used with ALU to select or   X => P
                    try:
                        op_mode["0111010"].append(instr)
                    except Exception as e:
                        op_mode["0111010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => P   Y => used with ALU to select or   X => A:B
                    try:
                        op_mode["0101011"].append(instr)
                    except Exception as e:
                        op_mode["0101011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    # P => X and/or Z depening on Y op mod
                    try:
                        ALU_mode["1110"].append(instr)
                    except KeyError:
                        ALU_mode["1110"] = [instr, ]

                    # Z => P   Y => used with ALU to select or   X => P
                    try:
                        op_mode["0101010"].append(instr)
                    except Exception as e:
                        op_mode["0101010"] = [instr, ]
            elif mnemonic in ["PNOR", ]:
                # P => X and/or Z depening on Y op mod
                try:
                    ALU_mode["1110"].append(instr)
                except KeyError:
                    ALU_mode["1110"] = [instr, ]

                # Z => C   Y => used with ALU to select or   X => A:B
                try:
                    op_mode["0111011"].append(instr)
                except Exception as e:
                    op_mode["0111011"] = [instr, ]

            elif mnemonic in ["XOR", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    #  P => X XOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => C   Y => 0  X => A:B
                    try:
                        op_mode["0110011"].append(instr)
                    except Exception as e:
                        op_mode["0110011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    #  P => X XOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => C   Y => 0   X => P
                    try:
                        op_mode["0110010"].append(instr)
                    except Exception as e:
                        op_mode["0110010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    #  P => X XOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => P   Y => 0  X => A:B
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        op_mode["0100011"].append(instr)
                    except Exception as e:
                        op_mode["0100011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    #  P => X XOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => P   Y => 0  X => P
                    try:
                        op_mode["0100010"].append(instr)
                    except Exception as e:
                        op_mode["0100010"] = [instr, ]
            elif mnemonic in ["PXOR", ]:
                # P => X XOR Z
                # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                try:
                    ALU_mode["0100"].append(instr)
                except KeyError:
                    ALU_mode["0100"] = [instr, ]

                # Z => C   Y => 0   X => A:B
                try:
                    op_mode["0110011"].append(instr)
                except Exception as e:
                    op_mode["0110011"] = [instr, ]

            elif mnemonic in ["XNOR", ]:
                operand_0_is_acc = asm_utils.access_is_internal(operands[0]) and asm_utils.access_internal(operands[0]) == "ACC"
                operand_1_is_acc = asm_utils.access_is_internal(operands[1]) and asm_utils.access_internal(operands[1]) == "ACC"

                if   not operand_0_is_acc and not operand_1_is_acc:
                    #  P => X XNOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => C   Y => used with ALU to select xnor  X => A:B
                    try:
                        op_mode["0111011"].append(instr)
                    except Exception as e:
                        op_mode["0111011"] = [instr, ]
                elif not operand_0_is_acc and operand_1_is_acc:
                    #  P => X XNOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => C   Y => used with ALU to select xnor   X => P
                    try:
                        op_mode["0111010"].append(instr)
                    except Exception as e:
                        op_mode["0111010"] = [instr, ]
                elif operand_0_is_acc and not operand_1_is_acc:
                    #  P => X XNOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => P   Y => used with ALU to select xnor  X => A:B
                    try:
                        op_mode["0101011"].append(instr)
                    except Exception as e:
                        op_mode["0101011"] = [instr, ]
                elif operand_0_is_acc and operand_1_is_acc:
                    #  P => X XNOR Z
                    # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                    try:
                        ALU_mode["0100"].append(instr)
                    except KeyError:
                        ALU_mode["0100"] = [instr, ]

                    # Z => P   Y => used with ALU to select xnor  X => P
                    try:
                        op_mode["0101010"].append(instr)
                    except Exception as e:
                        op_mode["0101010"] = [instr, ]
            elif mnemonic in ["PXNOR", ]:
                # P => X XOR Z
                # XOR throughfore 01XX, use 0100 as ID doesn't support don't care
                try:
                    ALU_mode["0100"].append(instr)
                except KeyError:
                    ALU_mode["0100"] = [instr, ]

                # Z => C   Y => used with ALU to select xnor   X => A:B
                try:
                    op_mode["0111011"].append(instr)
                except Exception as e:
                    op_mode["0111011"] = [instr, ]

            # Flag up unhandled mnemonic
            else:
                raise NotImplementedError(mnemonic)

    gen_utils.add_control(controls, "exe", instr_prefix + "core_ALU_mode", ALU_mode, "std_logic_vector", 4)
    gen_utils.add_control(controls, "exe", instr_prefix + "core_op_mode", op_mode, "std_logic_vector", 7)

    return controls

#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert type(config_in["data_width"]) == int, "data_width must be an int"
    assert config_in["data_width"] >= 1, "data_width must be greater than 0"
    config_out["data_width"] = config_in["data_width"]

    assert type(config_in["stallable"]) == bool, "stallable must be a bool"
    config_out["stallable"] = config_in["stallable"]

    assert type(config_in["required_operands"]) == int, "required_operands must be an int"
    assert config_in["required_operands"] > 0, "required_operands must be greater than 0"
    config_out["required_operands"] = config_in["required_operands"]

    assert type(config_in["operand_widths"]) == list, "operand_widths must be a list"
    assert len(config_in["operand_widths"]) == config_out["required_operands"], "lenght of operand_widths must match required_operands"
    if __debug__:
        for width in config_in["operand_widths"]:
            assert type(width) == int, "operand_widths must be ints"
            assert width > 0, "operand_widths must be greater than 0"
            assert width <= 48 , "operand_widths must be less than or great to 48"
    config_out["operand_widths"] = config_in["operand_widths"]

    assert type(config_in["statuses"]) == list, "statuses must be a list"
    if __debug__:
        for status in config_in["statuses"]:
            assert type(status) == str, "statuses must be strs"
            assert status in ["zero", "carry", ], "unknown status, %s"%(status, )
    config_out["statuses"] = config_in["statuses"]

    assert type(config_in["sign_0_sources"]) == list, "sign_0_sources must be a list"
    if __debug__:
        for src in config_in["sign_0_sources"]:
            assert type(src) == str, "src must be strs"
            assert src in ["acc", "operand", ], "unknown jump, %s"%(jump, )
    config_out["sign_0_sources"] = config_in["sign_0_sources"]

    assert type(config_in["sign_1_sources"]) == list, "sign_0_sources must be a list"
    if __debug__:
        for src in config_in["sign_1_sources"]:
            assert type(src) == str, "src must be strs"
            assert src in ["acc", "operand", ], "unknown jump, %s"%(jump, )
    config_out["sign_1_sources"] = config_in["sign_1_sources"]

    assert type(config_in["jumps"]) == list, "jumps must be a list"
    if __debug__:
        for jump in config_in["jumps"]:
            assert type(jump) == str, "jump must be strs"
            assert jump in ["greater", "lesser", "equal", "not_equal", ], "unknown jump, %s"%(jump, )
    config_out["jumps"] = config_in["jumps"]

    assert type(config_in["unsigned_compare"]) == bool, "unsigned_compare must be a bool"
    config_out["unsigned_compare"] = config_in["unsigned_compare"]

    assert type(config_in["signed_compare"]) == bool, "signed_compare must be a bool"
    config_out["signed_compare"] = config_in["signed_compare"]

    assert type(config_in["DSP_mult_used"]) == bool, "DSP_mult_used must be a bool"
    config_out["DSP_mult_used"] = config_in["DSP_mult_used"]

    assert type(config_in["DSP_C_used"]) == bool, "DSP_C_used must be a bool"
    config_out["DSP_C_used"] = config_in["DSP_C_used"]

    assert type(config_in["DSP_AB_used"]) == bool, "DSP_AB_used must be a bool"
    config_out["DSP_AB_used"] = config_in["DSP_AB_used"]

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

        # Include extremely commom libs
        com_det.add_import("ieee", "std_logic_1164", "all")

        # Generation Module Code
        handle_ports(gen_det, com_det)
        gen_DSP_slice(gen_det, com_det)
        handle_statuses_and_jumping(gen_det, com_det)

        # Save code to file
        gen_utils.generate_files(gen_det, com_det)

        return com_det.get_interface(), gen_det.module_name

#####################################################################

def handle_ports(gen_det, com_det):
    com_det.add_port("clock", "std_logic", "in")
    com_det.add_port("acc_enable", "std_logic", "in")
    if gen_det.config["stallable"]:
        com_det.add_port("stall_in", "std_logic", "in")

    for operand in range(gen_det.config["required_operands"]):
        com_det.add_port("operand_%i"%(operand, ), "std_logic_vector", "in", gen_det.config["operand_widths"][operand])

    # Handle slice controls
    com_det.add_port("op_mode", "std_logic_vector", "in", 7)
    com_det.arch_head += "signal DSP_op_mode : std_logic_vector(6 downto 0);\n"
    com_det.arch_body += "DSP_op_mode <= op_mode;\n\n"

    com_det.add_port("ALU_mode", "std_logic_vector", "in", 4)
    com_det.arch_head += "signal DSP_ALU_mode : std_logic_vector(3 downto 0);\n"
    com_det.arch_body += "DSP_ALU_mode <= ALU_mode;\n\n"

    # Handle DSP_C, which is always connected to operand 0
    if gen_det.config["DSP_C_used"]:
        C_width = gen_det.config["operand_widths"][0]
        com_det.arch_head += "signal DSP_C : std_logic_vector(47 downto 0);\n"
        com_det.arch_body += "DSP_C(%i downto 0) <= operand_0;\n"%(C_width - 1, )
        if C_width < 48:
            com_det.arch_body += "DSP_C(47 downto %i) <= (others => '0');\n"%(C_width, )
        com_det.arch_body += "\n"

    # Handle DSP_AB, which is always connected to operand 1
    if gen_det.config["DSP_AB_used"]:
        AB_width = gen_det.config["operand_widths"][1]
        com_det.arch_head += "signal DSP_AB : std_logic_vector(47 downto 0);\n"
        com_det.arch_body += "DSP_AB(%i downto 0) <= operand_1;\n"%(AB_width - 1, )
        if AB_width < 48:
            com_det.arch_body += "DSP_AB(47 downto %i) <= (others => '0');\n"%(AB_width, )
        com_det.arch_body += "\n"

    # Handle DSP_A and DSP_B
    if   gen_det.config["DSP_mult_used"] and gen_det.config["DSP_AB_used"]:
        # Mux between DSP_AB and operands
        com_det.arch_head += "signal DSP_A : std_logic_vector(29 downto 0);\n"
        com_det.arch_head += "signal DSP_B : std_logic_vector(17 downto 0);\n"

        com_det.arch_head += "signal DSP_AB_sel : std_logic;\n"
        com_det.arch_body += "DSP_AB_sel <= '1' when DSP_op_mode = \"0000101\" else '0';\n"

        A_width =  gen_det.config["operand_widths"][0]
        if A_width > 30:
            warnings.warn("operand 0 being trucated to 30 bits for multiplication")
            A_width = 30

        B_width =  gen_det.config["operand_widths"][1]
        if B_width > 18:
            warnings.warn("operand 1 being trucated to 18 bits for multiplication")
            B_width = 18

        AB_width = gen_det.config["operand_widths"][1]

        # Handle input data mux
        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs"  : 2,
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        if   AB_width <= 18:
            # As AB is handled wholely by DSP B there treat DSP A as if AB not used
            if A_width < 30:
                com_det.arch_body += "DSP_A(29 downto %i) <= (others => '0');\n\n"%(A_width, )
            com_det.arch_body += "DSP_A(%i downto 0) <= operand_0;\n\n"%(A_width - 1, )

            if AB_width == B_width:
                # As long as AB_width == B_width, B doesn't need muxing and can be handled as
                if B_width < 18:
                    com_det.arch_body += "DSP_B(17 downto %i) <= (others => '0');\n\n"%(A_width, )
                com_det.arch_body += "DSP_B(%i downto 0) <= operand_1;\n\n"%(B_width - 1, )
            else:
                raise NotImplementedError("Different AB_width and B_width not handled")
        elif AB_width <= 48:
            if B_width == 18:
                com_det.arch_body += "DSP_B(17 downto 0) <= operand_1(17 downto 0);\n\n"
            else:
                raise ValueError("AB_width > 18 but B_width != 18")

            muxed_width = max(A_width, AB_width - 18)

            if muxed_width < 30:
                com_det.arch_body += "DSP_A(29 downto %i) <= (others => '0');\n\n"%(A_width, )

            com_det.arch_body += "DSP_A_mux : entity work.%s(arch)@>\n"%(mux_name, )

            com_det.arch_body += "generic map (data_width => %i)\n"%(muxed_width, )

            com_det.arch_body += "port map (\n@>"

            com_det.arch_body += "sel(0) => DSP_AB_sel,\n"

            if AB_width - 18 == muxed_width:
                com_det.arch_body += "data_in_0 => operand_1(%i downto 18),\n"%(muxed_width + 17, )
            else:
                com_det.arch_body += "data_in_0(%i downto %i) => (others => '0'),\n"%(muxed_width - 1, AB_width - 18)
                com_det.arch_body += "data_in_0(%i downto 0) => operand_1(%i downto 18),\n"%(AB_width - 19, AB_width - 1)

            if A_width == muxed_width:
                com_det.arch_body += "data_in_1 => operand_0(%i downto 0),\n"%(A_width - 1, )
            else:
                com_det.arch_body += "data_in_1(%i downto %i) => (others => '0'),\n"%(muxed_width - 1, A_width)
                com_det.arch_body += "data_in_1(%i downto 0) => operand_0(%i downto 0),\n"%(A_width - 1, A_width - 1)

            com_det.arch_body += "data_out  => DSP_A(%i downto 0) \n"%(muxed_width - 1, )

            com_det.arch_body += "@<);\n@<\n"
        else:
            raise ValueError("AB can only be up to 48 bits in width")
    elif gen_det.config["DSP_mult_used"]:
        # Connect DSP_A and DSP_B to operands
        com_det.arch_head += "signal DSP_A : std_logic_vector(29 downto 0);\n"
        com_det.arch_head += "signal DSP_B : std_logic_vector(17 downto 0);\n"

        A_width =  gen_det.config["operand_widths"][0]
        B_width =  gen_det.config["operand_widths"][1]
        if A_width > 30:
            warnings.warn("operand 0 being trucated to 30 bits for multiplication")
            com_det.arch_body += "DSP_A <= operand_0(29 downto 0);\n\n"
        else:
            com_det.arch_body += "DSP_A(29 downto %i) <= (others => '0');\n\n"%(A_width, )
            com_det.arch_body += "DSP_A(%i downto 0) <= operand_0;\n\n"%(A_width - 1, )

        if B_width > 18:
            warnings.warn("operand 1 being trucated to 18 bits for multiplication")
            com_det.arch_body += "DSP_B <= operand_1(17 downto 0);\n\n"
        else:
            com_det.arch_body += "DSP_B(17 downto %i) <= (others => '0');\n\n"%(A_width, )
            com_det.arch_body += "DSP_B(%i downto 0) <= operand_1;\n\n"%(B_width - 1, )

    elif gen_det.config["DSP_AB_used"]:
        # Connect DSP_A and DSP_B to DSP_AB
        com_det.arch_head += "signal DSP_A : std_logic_vector(29 downto 0);\n"
        com_det.arch_head += "signal DSP_B : std_logic_vector(17 downto 0);\n"

        AB_width = gen_det.config["operand_widths"][1]
        if   AB_width <= 18:
            com_det.arch_body += "DSP_A(29 downto 0) <= (others => '0');\n"
            if AB_width < 18:
                com_det.arch_body += "DSP_B(17 downto %i) <= (others => '0');\n\n"%(AB_width, )
            com_det.arch_body += "DSP_B(%i downto 0) <= operand_1;\n\n"%(AB_width - 1, )
        elif AB_width <= 48:
            if AB_width < 48:
                com_det.arch_body += "DSP_A(29 downto %i) <= (others => '0');\n"%(AB_width - 18, )
            com_det.arch_body += "DSP_A(%i downto 0) <= operand_1(%i downto 18);\n"%(AB_width - 19, AB_width - 1, )
            com_det.arch_body += "DSP_B(17 downto 0) <= operand_1(17 downto 0);\n\n"
        else:
            raise ValueError("AB can only be up to 48 bits in width")

    # Handle DSP_P
    com_det.add_port("result_0", "std_logic_vector", "out", 48)
    com_det.arch_head += "signal DSP_P : std_logic_vector(47 downto 0);\n"
    com_det.arch_body += "result_0 <= DSP_P;\n\n"

def gen_DSP_slice(gen_det, com_det):
    com_det.add_import("UNISIM", "vcomponents", "all")

    com_det.arch_body  += "DSP48E1_inst : DSP48E1@>\n"

    com_det.arch_body  += "generic map (@>\n"

    # Disable cascading
    com_det.arch_body  += "-- Disable cascading \n"
    com_det.arch_body  += "A_INPUT => \"DIRECT\",\n"
    com_det.arch_body  += "B_INPUT => \"DIRECT\",\n"

    # Handle pre_adder
    com_det.arch_body  += "-- Disable pre_adder \n"
    com_det.arch_body  += "USE_DPORT => FALSE,\n"

    # Enable / Disable multiplier as needed
    gen_det.config["DSP_mult_used"]
    if not gen_det.config["DSP_mult_used"]:
        com_det.arch_body  += "-- Disable Multiplier \n"
        com_det.arch_body  += "USE_MULT => \"NONE\",\n"
    elif gen_det.config["DSP_mult_used"] and not gen_det.config["DSP_AB_used"]:
        com_det.arch_body  += "-- Enable Multiplier only\n"
        com_det.arch_body  += "USE_MULT => \"MULTIPLY\",\n"
    else: # gen_det.config["DSP_mult_used"] and gen_det.config["DSP_AB_used"]:
        com_det.arch_body  += "-- Enable DYNAMIC Multiplier\n"
        com_det.arch_body  += "USE_MULT => \"DYNAMIC\",\n"

    # Enable / Disable pattern Detector based on presentance of equal statuses
    if "zero" in gen_det.config["statuses"]:
        com_det.arch_body  += "-- Enable Pattern Detector \n"
        com_det.arch_body  += "USE_PATTERN_DETECT => \"PATDET\",\n"
        com_det.arch_body  += "AUTORESET_PATDET   => \"NO_RESET\",\n"

        # Set to only look at bits data_width -1 downto 0
        bin_mask = "1" * (48 - gen_det.config["data_width"]) + "0" * gen_det.config["data_width"]
        hex_mask = hex(int(bin_mask, 2))[2:]
        com_det.arch_body  += "MASK    => X\"%s\",\n"%(hex_mask, )
        # Set pattern to all ze4ros and testing for == 0
        com_det.arch_body  += "PATTERN => X\"000000000000\",\n"
        com_det.arch_body  += "SEL_MASK    => \"MASK\",\n"
        com_det.arch_body  += "SEL_PATTERN => \"PATTERN\",\n"
    else:
        com_det.arch_body  += "-- Disable Pattern Detector \n"
        com_det.arch_body  += "USE_PATTERN_DETECT => \"NO_PATDET\",\n"
        com_det.arch_body  += "AUTORESET_PATDET   => \"NO_RESET\",\n"
        com_det.arch_body  += "MASK    => X\"3fffffffffff\",\n"
        com_det.arch_body  += "PATTERN => X\"000000000000\",\n"
        com_det.arch_body  += "SEL_MASK    => \"MASK\",\n"
        com_det.arch_body  += "SEL_PATTERN => \"PATTERN\",\n"

    # Handle SIMD
    com_det.arch_body  += "-- Disable SIMD \n"
    com_det.arch_body  += "USE_SIMD => \"ONE48\",\n"

    # Handle Control registors
    com_det.arch_body  += "-- Handle Control registors\n"
    com_det.arch_body  += "ALUMODEREG => 0,\n"
    com_det.arch_body  += "OPMODEREG  => 0,\n"

    # Handle Data registors
    com_det.arch_body  += "-- Handle Data registors\n"
    if gen_det.config["DSP_mult_used"] or gen_det.config["DSP_AB_used"]:
        com_det.arch_body  += "AREG  => 0,\n"
        com_det.arch_body  += "ACASCREG   => 0,\n"
        com_det.arch_body  += "BREG  => 0,\n"
        com_det.arch_body  += "BCASCREG   => 0,\n"
    else:
        com_det.arch_body  += "AREG  => 1,\n"
        com_det.arch_body  += "ACASCREG   => 1,\n"
        com_det.arch_body  += "BREG  => 1,\n"
        com_det.arch_body  += "BCASCREG   => 1,\n"

    if gen_det.config["DSP_C_used"]:
        com_det.arch_body  += "CREG  => 0,\n"
    else:
        com_det.arch_body  += "CREG  => 1,\n"

    com_det.arch_body  += "DREG  => 1,\n"

    com_det.arch_body  += "CARRYINREG => 1,\n"

    com_det.arch_body  += "MREG  => 0,\n"
    com_det.arch_body  += "PREG  => 1,\n"

    # Registors on unused datapaths
    com_det.arch_body  += "ADREG => 0,\n"
    com_det.arch_body  += "INMODEREG  => 1,\n"
    com_det.arch_body  += "CARRYINSELREG => 1\n"

    com_det.arch_body  += "@<)\n"

    com_det.arch_body  += "port map (@>\n"

    # Disable casxading
    com_det.arch_body  += "-- Disable casxading \n"
    com_det.arch_body  += "ACIN => (others => '1'),\n"
    com_det.arch_body  += "BCIN => (others => '1'),\n"
    com_det.arch_body  += "PCIN => (others => '1'),\n"
    com_det.arch_body  += "CARRYCASCIN => '1',\n"
    com_det.arch_body  += "MULTSIGNIN  => '1',\n"
    com_det.arch_body  += "ACOUT => open,\n"
    com_det.arch_body  += "BCOUT => open,\n"
    com_det.arch_body  += "PCOUT => open,\n"
    com_det.arch_body  += "CARRYCASCOUT => open,\n"
    com_det.arch_body  += "MULTSIGNOUT  => open,\n"

    # Enable / Disable pattern Detector based on presentance of equal statuses
    if "zero" in gen_det.config["statuses"]:
        com_det.arch_head += "signal DSP_pattern_found : std_logic;\n"

        com_det.arch_body  += "-- Enable Pattern Detector\n"
        com_det.arch_body  += "OVERFLOW  => open,\n"
        com_det.arch_body  += "UNDERFLOW => open,\n"
        com_det.arch_body  += "PATTERNDETECT  => DSP_pattern_found,\n"
        com_det.arch_body  += "PATTERNBDETECT => open,\n"
    else:
        com_det.arch_body  += "-- Disable Pattern Detector\n"
        com_det.arch_body  += "OVERFLOW  => open,\n"
        com_det.arch_body  += "UNDERFLOW => open,\n"
        com_det.arch_body  += "PATTERNDETECT  => open,\n"
        com_det.arch_body  += "PATTERNBDETECT => open,\n"

    # Handle normal data output
    com_det.arch_body  += "-- Handle normal data output\n"
    com_det.arch_body  += "CARRYOUT => open,\n"

    com_det.arch_body  += "P => DSP_P,\n"

    # Handle Control ports
    com_det.arch_body  += "-- Handle Control ports\n"
    com_det.arch_body  += "CLK => clock,\n"

    # Generate required DSP control signals for each oper
    com_det.arch_body  += "ALUMODE => DSP_ALU_mode,\n"
    com_det.arch_body  += "OPMODE  => DSP_op_mode,\n"
    com_det.arch_body  += "INMODE  => (others => '0'),\n"
    com_det.arch_body  += "CARRYINSEL => (others => '0'),\n"

    # Handle data ports
    com_det.arch_body  += "-- Handle data input ports\n"
    if gen_det.config["DSP_mult_used"] or gen_det.config["DSP_AB_used"]:
        com_det.arch_body  += "A => DSP_A,\n"
        com_det.arch_body  += "B => DSP_B,\n"
    else:
        com_det.arch_body  += "A => (others => '1'),\n"
        com_det.arch_body  += "B => (others => '1'),\n"

    if gen_det.config["DSP_C_used"]:
        com_det.arch_body  += "C => DSP_C,\n"
    else:
        com_det.arch_body  += "C => (others => '1'),\n"

    com_det.arch_body  += "D => (others => '1'),\n"

    com_det.arch_body  += "CARRYIN => '1',\n"

    com_det.arch_body  += "-- Reset/Clock Enable: 1-bit (each) input: Reset/Clock Enable Inputs\n"
    com_det.arch_body  += "CEA1 => '0',\n"
    com_det.arch_body  += "CEA2 => '0',\n"
    com_det.arch_body  += "CEB1 => '0',\n"
    com_det.arch_body  += "CEB2 => '0',\n"
    com_det.arch_body  += "CEC  => '0',\n"
    com_det.arch_body  += "CEAD => '0',\n"
    com_det.arch_body  += "CED  => '0',\n"
    com_det.arch_body  += "CEM  => '0',\n"

    if gen_det.config["stallable"]:
        com_det.arch_body  += "CEP  => acc_enable and not stall_in,\n"
    else:
        com_det.arch_body  += "CEP  => acc_enable,\n"

    com_det.arch_body  += "CECTRL => '0',\n"
    com_det.arch_body  += "CEINMODE  => '0',\n"
    com_det.arch_body  += "CEALUMODE => '0',\n"
    com_det.arch_body  += "CECARRYIN => '0',\n"

    com_det.arch_body  += "RSTA => '0',\n"
    com_det.arch_body  += "RSTB => '0',\n"
    com_det.arch_body  += "RSTC => '0',\n"
    com_det.arch_body  += "RSTD => '0',\n"
    com_det.arch_body  += "RSTM => '0',\n"
    com_det.arch_body  += "RSTP => '0',\n"
    com_det.arch_body  += "RSTCTRL => '0',\n"
    com_det.arch_body  += "RSTINMODE => '0',\n"
    com_det.arch_body  += "RSTALLCARRYIN => '0',\n"
    com_det.arch_body  += "RSTALUMODE => '0'\n"
    com_det.arch_body  += "@<);\n"

    com_det.arch_body  += "@<\n"

def handle_statuses_and_jumping(gen_det, com_det):

    if len(gen_det.config["jumps"] ) != 0:
        reg_interface, reg_name = register.generate_HDL(
            {
                "has_async_force"  : False,
                "has_sync_force"   : False,
                "has_enable"    : True,
                "force_on_init" : False
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )

        _, mux_2 = mux.generate_HDL(
            {
                "inputs" : 2,
            },
            output_path=gen_det.output_path,
            module_name=None,
            concat_naming=False,
            force_generation=gen_det.force_generation
        )


        # Compute the statuses for status reg
        if gen_det.config["signed_compare"] and ("greater" in gen_det.config["jumps"] or "lesser" in gen_det.config["jumps"]):
            com_det.arch_head += "signal operand_0_sign, operand_0_sign_delayed : std_logic;\n"
            if   "acc" in gen_det.config["sign_0_sources"] and "operand" in gen_det.config["sign_0_sources"]:
                com_det.arch_body += "operand_0_sign_mux: entity work.%s(arch)@>\n"%(mux_2, )
                com_det.arch_body += "generic map (data_width => 1)\n"
                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => DSP_op_mode(4),\n"
                com_det.arch_body += "data_in_0(0) => DSP_P(%i),\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "data_in_1(0) => operand_0(%i),\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "data_out(0)  => operand_0_sign\n"
                com_det.arch_body += "@<);\n@<\n"
            elif "acc" in gen_det.config["sign_0_sources"] and "operand" in gen_det.config["sign_0_sources"]:
                com_det.arch_body += "operand_0_sign <= DSP_P(%i) a;\n\n"%(gen_det.config["data_width"] - 1, )
            elif "acc" not in gen_det.config["sign_0_sources"] and "operand" not in gen_det.config["sign_0_sources"]:
                com_det.arch_body += "operand_0_sign <= operand_0(%i);\n\n"%(gen_det.config["data_width"] - 1, )
            else:
                raise ValueError("Unknow combination of sources; %s"%(gen_det.config["sign_0_sources"],) )

            com_det.arch_head += "signal operand_1_sign, operand_1_sign_delayed : std_logic;\n"
            if   "acc" in gen_det.config["sign_1_sources"] and "operand" in gen_det.config["sign_1_sources"]:
                com_det.arch_body += "operand_1_sign_mux: entity work.%s(arch)@>\n"%(mux_2, )
                com_det.arch_body += "generic map (data_width => 1)\n"
                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => DSP_op_mode(0),\n"
                com_det.arch_body += "data_in_0(0) => DSP_P(%i),\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "data_in_1(0) => operand_1(%i),\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "data_out(0)  => operand_1_sign\n"
                com_det.arch_body += "@<);\n@<\n"
            elif "acc" in gen_det.config["sign_1_sources"] and "operand" in gen_det.config["sign_1_sources"]:
                com_det.arch_body += "operand_1_sign <= DSP_P(%i) a;\n\n"%(gen_det.config["data_width"] - 1, )
            elif "acc" not in gen_det.config["sign_1_sources"] and "operand" not in gen_det.config["sign_1_sources"]:
                com_det.arch_body += "operand_1_sign <= operand_1(%i);\n\n"%(gen_det.config["data_width"] - 1, )
            else:
                raise ValueError("Unknow combination of sources; %s"%(gen_det.config["sign_0_sources"],) )


            com_det.arch_body += "operand_sign_reg : entity work.%s(arch)@>\n"%(reg_name, )

            com_det.arch_body += "generic map (data_width => 2)\n"

            com_det.arch_body += "port map (\n@>"
            com_det.arch_body += "clock => clock,\n"

            com_det.add_port("hold_operand_signs", "std_logic", "in")
            if gen_det.config["stallable"]:
                com_det.arch_body  += "enable  => hold_operand_signs and not stall_in,\n"
            else:
                com_det.arch_body  += "enable  => hold_operand_signs,\n"

            com_det.arch_body += "data_in => (0 => operand_0_sign, 1 => operand_1_sign),\n"
            com_det.arch_body += "data_out(0) => operand_0_sign_delayed,\n"
            com_det.arch_body += "data_out(1) => operand_1_sign_delayed\n"

            com_det.arch_body += "@<);\n@<\n"

        status_reg_width = 0
        if "equal" in gen_det.config["jumps"] or "not_equal" in gen_det.config["jumps"] :
            status_reg_width += 1

            com_det.arch_head += "signal status_equals_next : std_logic;\n"
            com_det.arch_body  += "status_equals_next <= DSP_pattern_found;\n"


        if   gen_det.config["signed_compare"] and gen_det.config["unsigned_compare"] and ("greater" in gen_det.config["jumps"] or "lesser" in gen_det.config["jumps"]) :
            com_det.add_port("CMP_sel", "std_logic", "in")


        if "greater" in gen_det.config["jumps"]:
            status_reg_width += 1

            if gen_det.config["unsigned_compare"]:
                com_det.arch_head += "signal UCMP_greater : std_logic;\n"
                com_det.arch_body  += "UCMP_greater <= not DSP_P(%i) and not DSP_pattern_found;\n"%(gen_det.config["data_width"], )

            if gen_det.config["signed_compare"]:
                com_det.arch_head += "signal SCMP_greater : std_logic;\n"

                com_det.arch_body  += "SCMP_greater <=@>"
                # +ve - -ve; +ve < -ve
                com_det.arch_body += "( (not operand_0_sign_delayed and operand_1_sign_delayed)\n"
                # +ve - +ve => +ve, either A > B or A = B therefore check pattern match
                com_det.arch_body += "or (operand_0_sign_delayed and operand_1_sign_delayed and not DSP_P(%i) and not DSP_pattern_found)\n"%(gen_det.config["data_width"] - 1, )
                # -ve - -ve => +ve, either A > B or A = B therefore check pattern match)
                com_det.arch_body += "or (not operand_0_sign_delayed and not operand_1_sign_delayed and not DSP_P(%i) and not DSP_pattern_found)\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "@<);@<\n"


            com_det.arch_head += "signal status_greater_next : std_logic;\n"
            if   gen_det.config["signed_compare"] and gen_det.config["unsigned_compare"]:
                com_det.arch_body += "status_greater_next_mux: entity work.%s(arch)@>\n"%(mux_2, )
                com_det.arch_body += "generic map (data_width => 1)\n"
                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => CMP_sel,\n"
                com_det.arch_body += "data_in_0(0) => UCMP_greater,\n"
                com_det.arch_body += "data_in_1(0) => SCMP_greater,\n"
                com_det.arch_body += "data_out(0)  => status_greater_next\n"
                com_det.arch_body += "@<);\n@<\n"
            elif gen_det.config["signed_compare"]:
                com_det.arch_body  += "status_greater_next <= SCMP_greater;\n"
            elif gen_det.config["unsigned_compare"]:
                com_det.arch_body  += "status_greater_next <= UCMP_greater;\n"

        if "lesser" in gen_det.config["jumps"]:
            status_reg_width += 1

            if gen_det.config["unsigned_compare"]:
                com_det.arch_head += "signal UCMP_lesser : std_logic;\n"
                com_det.arch_body  += "UCMP_lesser <= DSP_P(%i);\n"%(gen_det.config["data_width"], )

            if gen_det.config["signed_compare"]:
                com_det.arch_head += "signal SCMP_lesser : std_logic;\n"
                com_det.arch_body  += "SCMP_lesser <=@>"
                # -ve - +ve; -ve < +ve
                com_det.arch_body += "( (operand_0_sign_delayed and not operand_1_sign_delayed)\n"
                # +ve - X => -ve, X either -ve and result overflowed (-ve < +ve) or X larger +ve (therefore <)
                com_det.arch_body += "or (operand_0_sign_delayed and DSP_P(%i))\n"%(gen_det.config["data_width"] - 1, )
                # X - +ve => -ve, X either -ve (-ve < +ve) or X smaller +ve (therefore <)
                com_det.arch_body += "or (not operand_1_sign_delayed and DSP_P(%i))\n"%(gen_det.config["data_width"] - 1, )
                com_det.arch_body += "@<);@<\n"

            com_det.arch_head += "signal status_lesser_next : std_logic;\n"
            if   gen_det.config["signed_compare"] and gen_det.config["unsigned_compare"]:
                com_det.arch_body += "status_lesser_next_mux: entity work.%s(arch)@>\n"%(mux_2, )
                com_det.arch_body += "generic map (data_width => 1)\n"
                com_det.arch_body += "port map (\n@>"
                com_det.arch_body += "sel(0) => CMP_sel,\n"
                com_det.arch_body += "data_in_0(0) => UCMP_lesser,\n"
                com_det.arch_body += "data_in_1(0) => SCMP_lesser,\n"
                com_det.arch_body += "data_out(0)  => status_lesser_next\n"
                com_det.arch_body += "@<);\n@<\n"
            elif gen_det.config["signed_compare"]:
                com_det.arch_body  += "status_lesser_next <= SCMP_lesser;\n"
            elif gen_det.config["unsigned_compare"]:
                com_det.arch_body  += "status_lesser_next <= UCMP_lesser;\n"

        # Generate status reg
        com_det.arch_body += "status_reg : entity work.%s(arch)@>\n"%(reg_name, )

        com_det.arch_body += "generic map (data_width => %i)\n"%(status_reg_width, )

        com_det.arch_body += "port map (\n@>"
        com_det.arch_body += "clock => clock,\n"

        com_det.add_port("update_statuses", "std_logic", "in")
        if gen_det.config["stallable"]:
            com_det.arch_body  += "enable  => update_statuses and not stall_in,\n"
        else:
            com_det.arch_body  += "enable  => update_statuses,\n"

        index = 0
        com_det.arch_body += "data_in => ("
        if "equal" in gen_det.config["jumps"] or "not_equal" in gen_det.config["jumps"] :
            com_det.arch_body += "%i => status_equals_next, "%(index, )
            index += 1
        if "greater" in gen_det.config["jumps"]:
            com_det.arch_body += "%i => status_greater_next, "%(index, )
            index += 1
        if "lesser" in gen_det.config["jumps"]:
            com_det.arch_body += "%i => status_lesser_next, "%(index, )
            index += 1
        com_det.arch_body.drop_last(2)
        com_det.arch_body += "),\n"

        index = 0
        if "equal" in gen_det.config["jumps"] or "not_equal" in gen_det.config["jumps"] :
            com_det.arch_head += "signal status_equals : std_logic;\n"
            com_det.arch_body += "data_out(%i) => status_equals,\n"%(index, )
            index += 1
        if "greater" in gen_det.config["jumps"]:
            com_det.arch_head += "signal status_greater : std_logic;\n"
            com_det.arch_body += "data_out(%i) => status_greater,\n"%(index, )
            index += 1
        if "lesser" in gen_det.config["jumps"]:
            com_det.arch_head += "signal status_lesser : std_logic;\n"
            com_det.arch_body += "data_out(%i) => status_lesser,\n"%(index, )
            index += 1

        com_det.arch_body.drop_last(2)
        com_det.arch_body += "\n@<);\n@<\n"

        # Declare and flag jump taken signel
        com_det.add_port("jump_taken", "std_logic", "out")
        com_det.add_interface_item("jump_drivers", ["ALU_core_jump_taken", ])

        # Generate jumping logic
        com_det.arch_body += "jump_taken <=@>"
        if "equal" in gen_det.config["jumps"] :
            com_det.add_port("jump_equal", "std_logic", "in")
            com_det.arch_body += "(jump_equal and status_equals)\n or "
        if "not_equal" in gen_det.config["jumps"] :
            com_det.add_port("jump_not_equal", "std_logic", "in")
            com_det.arch_body += "(jump_not_equal and not status_equals)\n or "
        if "greater" in gen_det.config["jumps"]:
            com_det.add_port("jump_greater", "std_logic", "in")
            com_det.arch_body += "(jump_greater and status_greater)\n or "
        if "lesser" in gen_det.config["jumps"]:
            com_det.add_port("jump_lesser", "std_logic", "in")
            com_det.arch_body += "(jump_lesser and status_lesser)\n or "
        com_det.arch_body.drop_last(5)
        com_det.arch_body += ";@<\n\n"
