from ... import FPE_assembly as asm_utils

def get_exe_operation_code(op_id):
    return "#".join([
        asm_utils.decode_mnemonic(op_id),
        "|".join([
            src.lower()
            if not any([
                src.startswith(fetch + "[")
                for fetch in ["IMM", "GET", "REG", "RAM", "ROM"]
            ])
            else "fetch"
            for src in asm_utils.decode_data_sources(op_id)
        ]),
        "|".join([
            dst.lower()
            if not any([
                dst.startswith(store + "[")
                for store in ["PUT", "REG", "RAM"]
            ])
            else "store"
            for dst in asm_utils.decode_data_dests(op_id)
        ]),
    ])

def decode_num_fetchs(exe_op):
    return len([
        True
        for src in exe_op.split("#")[1].split("!")
        if src == "fetch"
    ])

def decode_num_stores(exe_op):
    return len([
        True
        for src in exe_op.split("#")[2].split("!")
        if src == "store"
    ])
