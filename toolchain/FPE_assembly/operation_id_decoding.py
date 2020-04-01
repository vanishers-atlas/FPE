import re

def decode_mnemonic(op_id):
    return op_id.split("#")[0]

####################################################################

def decode_data_sources(op_id):
    return op_id.split("#")[1].split("|") if op_id.split("#")[1] != "" else []


def decode_fetchs(op_id):
    return [ src for src in decode_data_sources(op_id) if "[" in src and "]" in src ]

def decode_fetch_components(op_id):
    return [fetch.split("[")[0] for fetch in decode_fetchs(op_id) ]

def decode_fetch_mods(op_id):
    return [fetch.split("]")[1].split("|") for fetch in decode_fetchs(op_id) ]


def decode_fetch_addresses(op_id):
    rtn = []
    for store in decode_fetchs(op_id):
        addr = store.split("[")[1].split("]")[0]
        if addr.isdigit():
            rtn.append("ID_addr_%s"%(addr))
        else:
            rtn.append("%s_address"%(addr))
    return rtn

def decode_fetch_address_components(op_id):
    rtn = []
    for store in decode_fetchs(op_id):
        addr = store.split("[")[1].split("]")[0]
        if addr.isdigit():
            rtn.append("ID")
        else:
            rtn.append(addr)
    return rtn

def decode_fetch_address_mods(op_id):
    return [store.split("]")[1].split("|") for store in decode_fetchs(op_id)]


def decode_fetch_paths(op_id):
    paths_used = []
    rtn_data = []
    for component in decode_fetch_components(op_id):
        rtn_data.append(component + "_read_" + str(paths_used.count(component)) )
        paths_used.append(component)
    return rtn_data

####################################################################

def decode_exe_component(op_id):
    return op_id.split("#")[2]


def decode_exe_inputs(op_id):
    component = decode_exe_component(op_id)
    return ["%s_in_%i"%(component, p) for p in range(len(decode_fetchs(op_id)))]

####################################################################

def decode_data_dests(op_id):
    return op_id.split("#")[3].split("|") if op_id.split("#")[3] != "" else []


def decode_stores(op_id):
    return [ dst for dst in decode_data_dests(op_id) if "[" in dst and "]" in dst ]

def decode_store_components(op_id):
    return [store.split("[")[0] for store in decode_stores(op_id) ]

def decode_store_mods(op_id):
    return [store.split("]")[1].split("|") for store in decode_stores(op_id) ]


def decode_store_addresses(op_id):
    rtn = []
    for store in decode_stores(op_id):
        addr = store.split("[")[1].split("]")[0]
        if addr.isdigit():
            rtn.append("ID_addr_%s"%(addr))
        else:
            rtn.append("%s_address"%(addr))
    return rtn

def decode_store_address_components(op_id):
    rtn = []
    for store in decode_stores(op_id):
        addr = store.split("[")[1].split("]")[0]
        if addr.isdigit():
            rtn.append("ID")
        else:
            rtn.append(addr)
    return rtn

def decode_store_address_mods(op_id):
    return [store.split("]")[1].split("|") for store in decode_stores(op_id)]


def decode_store_paths(op_id):
    paths_used = []
    rtn_data = []
    for component in decode_store_components(op_id):
        rtn_data.append(component + "_write_" + str(paths_used.count(component)) )
        paths_used.append(component)
    return rtn_data

####################################################################

def decode_num_encoded_addrs(op_id):
    return len(re.findall (r"\[(\d*)\]", op_id))
