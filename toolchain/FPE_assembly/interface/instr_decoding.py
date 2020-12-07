import re

###############################################################
# Instr decomposing
###############################################################
# Instr structure :
# Sections : Mnemonic Sources Execution_unit Dests Mods
# With "#" as section delimators
# With "~" as multiple delimators

def instr_mnemonic(instr):
    return instr.split("#")[0]

def instr_srcs(instr):
    if instr.split("#")[1] != "":
        return instr.split("#")[1].split("~")
    else:
        return []

def instr_exe_unit(instr):
    return instr.split("#")[2]

def instr_dests(instr):
    if instr.split("#")[3] != "":
        return instr.split("#")[3].split("~")
    else:
        return []

def instr_mods(instr):
    mods = {}
    mod_strs = instr.split("#")[4]
    if mod_strs != "":
        for mod_str in mod_strs.split("~"):
            mod = mod_str.split("'")
            if   len(mod) == 1:
                mods[mod[0]] = None
            elif len(mod) == 2:
                mods[mod[0]] = mod[1]
            else:
                raise NotImplenentedError()
    return mods

exe_internals = {
    "ALU" : ["ACC"],
}

def instr_fetches(instr):
    return [
        src
        for src in instr_srcs(instr)
        if
        (
            instr_exe_unit(instr) not in exe_internals.keys()
            or src not in exe_internals[instr_exe_unit(instr)]
        )
    ]

def instr_stores(instr):
    return [
        dest
        for dest in instr_dests(instr)
        if
        (
            instr_exe_unit(instr) in exe_internals.keys()
            and dest not in exe_internals[instr_exe_unit(instr)]
        )
    ]

###############################################################
# Access decomposing
###############################################################
# Access structure :
# Sections : Mem Addr Mods
# With "'" as section delimators
# With "@" as multiple delimators

def access_mem(access):
    return access.split("'")[0]

def access_addr(access):
    return access.split("'")[1]

def access_mods(access):
    mods = {}
    mod_strs = access.split("'")[2]
    if mod_strs != "":
        for mod_str in mod_strs.split("@"):
            mod = mod_str.split(";")
            if   len(mod) == 1:
                mods[mod[0]] = None
            elif len(mod) == 2:
                mods[mod[0]] = mod[1]
            else:
                raise NotImplenentedError()
    return mods


###############################################################
# Addr decomposing
###############################################################
# Addr structure :
# Sections : Com Port Mods
# With ";" as section delimators
# With ":" as multiple delimators

def addr_com(addr):
    return addr.split(";")[0]

def addr_port(addr):
    return addr.split(";")[1]

def addr_mods(addr):
    mods = {}
    mod_strs = addr.split(";")[2]
    if mod_strs != "":
        for mod_str in mod_strs.split(":"):
            mod = mod_str.split("?")
            if   len(mod) == 1:
                mods[mod[0]] = None
            elif len(mod) == 2:
                mods[mod[0]] = mod[1]
            else:
                raise NotImplenentedError()
    return mods
