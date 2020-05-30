import re

def instr_mnemonic(op_id):
    return op_id.split("#")[0]

####################################################################

def instr_srcs(op_id):
    if op_id.split("#")[1] != "":
        return [
            store
            for store in op_id.split("#")[1].split("~")
        ]
    else:
        return []

def instr_fetchs(op_id):
    return [
        src
        for src in instr_srcs(op_id)
        if src.lower() != "acc"
    ]

def instr_fetch_addrs(op_id):
    return [
        "addr_%s"%(fetch.split("'")[1].split(";")[0])
        if fetch.split("'")[1].split(";")[0].isdigit()
        else "addr"
        for fetch in instr_fetchs(op_id)
    ]


def instr_fetch_access_coms(op_id):
    return [
        fetch.split("'")[0]
        for fetch in instr_fetchs(op_id)
    ]

def instr_fetch_access_srcs(op_id):
    paths_used = []
    rtn_data = []
    for com in instr_fetch_access_coms(op_id):
        rtn_data.append(
            "read_%i_data"%(
                paths_used.count(com),
            )
        )
        paths_used.append(com)
    return rtn_data

def instr_fetch_access_dsts(op_id):
    exe_com =  instr_exe_com(op_id)
    if exe_com == "":
        return []
    elif exe_com.startswith(("ALU")):
        return [
            "in_%i"%(index)
            for index, src in enumerate(instr_fetchs(op_id))
        ]
    elif exe_com.startswith(("BAM_")):
        return [
            "data_in"
            for src in instr_fetchs(op_id)
        ]
    elif exe_com == "PC":
        return [
            "jump_value"
            for src in instr_fetchs(op_id)
        ]
    else:
        raise NotImplementedError("Unknown ese_com, %s"%(exe_com))

def instr_fetch_access_mods(op_id):
    return [
        fetch.split("'")[2].split("@")
        for fetch in instr_fetchs(op_id)
    ]


def instr_fetch_addr_coms(op_id):
    return [
        "ID"
        if fetch.split("'")[1].split(";")[0].isdigit()
        else fetch.split("'")[1].split(";")[0]
        for fetch in instr_fetchs(op_id)
    ]

def instr_fetch_addr_srcs(op_id):
    return [
        "addr_%s_fetch"%(fetch.split("'")[1].split(";")[1])
        if fetch.split("'")[1].split(";")[1].isdigit()
        else "addr_fetch"
        for fetch in instr_fetchs(op_id)
    ]

def instr_fetch_addr_dsts(op_id):
    paths_used = []
    rtn_data = []
    for com in instr_fetch_access_coms(op_id):
        rtn_data.append(
            "read_%i_addr"%(
                paths_used.count(com),
            )
        )
        paths_used.append(com)
    return rtn_data

def instr_fetch_addr_mods(op_id):
    return [
        fetch.split("'")[1].split(";")[2].split(":")
        for fetch in instr_fetchs(op_id)
    ]


####################################################################

def instr_exe_com(op_id):
    return op_id.split("#")[2]

####################################################################

def instr_dests(op_id):
    if op_id.split("#")[3] != "":
        return [
            store
            for store in op_id.split("#")[3].split("~")
        ]
    else:
        return []

def instr_stores(op_id):
    return [
        dest
        for dest in instr_dests(op_id)
        if dest.lower() != "acc"
    ]

def instr_store_addrs(op_id):
    return [
        "addr_%s"%(fetch.split("'")[1].split(";")[0])
        if fetch.split("'")[1].split(";")[0].isdigit()
        else "addr"
        for fetch in instr_stores(op_id)
    ]


def instr_store_access_coms(op_id):
    return [
        store.split("'")[0]
        for store in instr_stores(op_id)
    ]

def instr_store_access_srcs(op_id):
    exe_com =  instr_exe_com(op_id)
    if exe_com.startswith(("ALU")):
        return [
            "out_%i"%(index)
            for index, src in enumerate(instr_stores(op_id))
        ]
    elif exe_com.startswith(("BAM_", "PC")):
        return []
    else:
        raise NotImplementedError("Unknown ese_com, %s"%(exe_com))

def instr_store_access_dsts(op_id):
    paths_used = []
    rtn_data = []
    for com in instr_store_access_coms(op_id):
        rtn_data.append(
            "write_%i_data"%(
                paths_used.count(com),
            )
        )
        paths_used.append(com)
    return rtn_data

def instr_store_access_mods(op_id):
    raise NotImplementedError()
    return [store.split("]")[1].split("|") for store in instr_stores(op_id) ]


def instr_store_addr_coms(op_id):
    return [
        "ID"
        if fetch.split("'")[1].split(";")[0].isdigit()
        else fetch.split("'")[1].split(";")[0]
        for fetch in instr_stores(op_id)
    ]

def instr_store_addr_srcs(op_id):
    return [
        "addr_%s_store"%(store.split("'")[1].split(";")[1])
        if store.split("'")[1].split(";")[1].isdigit()
        else "addr_store"
        for store in instr_stores(op_id)
    ]

def instr_store_addr_dsts(op_id):
    paths_used = []
    rtn_data = []
    for component in instr_store_access_coms(op_id):
        rtn_data.append(
            "write_%i_addr"%(
                paths_used.count(component),
            )
        )
        paths_used.append(component)
    return rtn_data

def instr_store_addr_mods(op_id):
    return [
        store.split("'")[1].split(";")[2].split(":")
        for store in instr_stores(op_id)
    ]

####################################################################

def instr_mods(op_id):
    return op_id.split("#")[4].split("~")
