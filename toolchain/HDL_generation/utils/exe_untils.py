from FPE.toolchain import FPE_assembly as asm_utils

def get_exe_operation_code(op_id):
    return "#".join(
        [
            asm_utils.instr_mnemonic(op_id),
            "~".join(
                [
                    "acc" if src.lower() == "acc"
                    else "fetch"
                    for src in asm_utils.instr_srcs(op_id)
                ]
            ),
            "~".join(
                [
                    "acc" if dst.lower() == "acc"
                    else "store"
                    for dst in asm_utils.instr_dests(op_id)
                ]
            ),
        ]
    )

def decode_num_fetchs(exe_op):
    return len(
        [
            True
            for src in exe_op.split("#")[1].split("~")
            if src == "fetch"
        ]
    )

def decode_num_stores(exe_op):
    return len(
        [
            True
            for src in exe_op.split("#")[2].split("~")
            if src == "store"
        ]
    )
