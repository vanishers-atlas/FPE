import warnings

def decomposeInstr(instrStr):
    # Split into mnemonic and accesses
    raw_accesses = instrStr.split("_")
    mnemonic = raw_accesses[0]
    del raw_accesses[0]

    # Process raw_accesses
    accesses = []
    for access in raw_accesses:
        # Split access into addr, addr mods, mem, and mem mods sections
        addr, mem = access.split(":")
        try:
            addr, addr_mods = addr.split("'")
            addr_mods = addr_mods.split("|")
        except ValueError: addr_mods = []
        try:
            mem, mem_mods = mem.split("'")
            mem_mods = mem_mods.split("|")
        except ValueError: mem_mods = []

        # Record what the access break down into
        accesses.append({"addr" : addr, "addr_mods" : addr_mods, "mem" : mem, "mem_mods" : mem_mods})

    # Return decomposed instruction
    return mnemonic, accesses

class readInstrSetJson:
    def processAddrMods(this, access, instr):
        for mod in access["addr_mods"]:
            # Warn of unknown addr mod
            warnings.warn("instr \"%s\" contains an unknown mod \"%s\" on addr %s\n"%(instr, mod, access["addr"]))

    def processMemMods(this, access, instr):
        for mod in access["mem_mods"]:
            # Handle COM GET a specific mods
            if access["mem"] == "GET":
                # Check for update mod
                if mod == "update":
                    # Make sure Get is in mem mods
                    if not "GET" in this.mem_mods:
                        this.mem_mods["GET"] = {}
                    # Make sure update set is in mem_mods[GET]
                    if not "update" in this.mem_mods["GET"]:
                        this.mem_mods["GET"]["update"] = set()
                    # Record mod occurance
                    this.mem_mods["GET"]["update"].add(access["addr"])
                # Warn of unknown mod for COM GET
                else:
                    warnings.warn("instr \"%s\" contains an unknown mod \"%s\" on mem GET\n"%(instr, mod))
            # Warn of unknown mem mod
            else:
                warnings.warn("instr \"%s\" contains an unknown mod \"%s\" on mem %s\n"%(instr, mod, acces["mem"]))

    def processInstr(this, instr):
        mnemonic, accesses = decomposeInstr(instr)

        # Record all used Mnemonics
        this.mnemonics.add(mnemonic)

        # Extract accesses from Instr
        for access in accesses:
            # Record all addrs and mems in instrSet
            this.addrs.add(access["addr"])
            this.mems.add(access["mem"])

            # Record all accesses in instrSet
            if not access["addr"] in this.accesses:
                this.accesses[access["addr"]] = set()
            this.accesses[access["addr"]].add(access["mem"])
            if not access["mem"] in this.accesses:
                this.accesses[access["mem"]] = set()
            this.accesses[access["mem"]].add(access["addr"])

            # Process Mods
            this.processAddrMods(access, instr)
            this.processMemMods (access, instr)

    def __init__(this, jsonStr):
        import json
        this.instrSet = json.loads(jsonStr)

        # Init mnemonics
        this.mnemonics = set()

        # Init addrs
        this.mems  = set()
        this.addrs = set()

        # Init accesses
        this.accesses = {}

        # Init mods
        this.mem_mods  = {}
        this.addr_mods = {}

        # Scan Instruction Set
        for instr, opcode in this.instrSet.items():
            # Check all opcodes and greater than 0
            if opcode <= 0:
                raise ValueError("%s, assigned non-positive opcode\n"%(instr, ) )

            # Process instr
            this.processInstr(instr)
