def oper_mnemonic(oper):
    return oper.split("#")[0]

def oper_srcs(oper):
    if oper.split("#")[1] != "":
        return oper.split("#")[1].split("~")
    else:
        return []

def oper_num_fetchs(oper):
    return len(
        [
            True
            for src in oper_srcs(oper)
            if src == "fetch"
        ]
    )

def oper_dests(oper):
    if oper.split("#")[2] != "":
        return oper.split("#")[1].split("~")
    else:
        return []

def oper_num_stores(oper):
    return len(
        [
            True
            for src in oper_dests(oper)
            if src == "store"
        ]
    )
