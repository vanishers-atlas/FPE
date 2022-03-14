###############################################################
# Instr decomposing
###############################################################
# Instr structure :
# Sections : Mnemonic Sources Execution_unit Dests Mods
# With "#" as section delimators
# With "~" as multiple delimators

def instr_mnemonic(instr):
    return instr.split("#")[0]

def instr_operands(instr):
    if instr.split("#")[1] != "":
        return instr.split("#")[1].split("~")
    else:
        return []

def instr_exe_units(instr):
    return instr.split("#")[2].split("~")

def instr_results(instr):
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

def instr_fetches(instr):
    return [
        src
        for src in instr_operands(instr)
        if not access_is_internal(src)
    ]

def instr_stores(instr):
    return [
        dest
        for dest in instr_results(instr)
        if not access_is_internal(dest)
    ]


def mnemonic_decompose(mnemonic):
    return mnemonic.split("~")


###############################################################
# Access decomposing
###############################################################
# Access structure :
# Sections : Mem Addr Mods
# With "'" as section delimators
# With "@" as multiple delimators

def access_is_internal(access):
    # ? used the mark internal, ie non fetched operands
    return access.startswith("?")

def access_internal(access):
    assert access_is_internal(access)
    return access.lstrip("?")


def access_mem(access):
    assert not access_is_internal(access)
    return access.split("'")[0]

def access_addr(access):
    assert not access_is_internal(access)
    return access.split("'")[1]

def access_mods(access):
    assert not access_is_internal(access)
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
