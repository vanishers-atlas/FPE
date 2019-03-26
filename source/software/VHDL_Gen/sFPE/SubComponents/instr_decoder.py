import InstrSet

class readParaJson:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        this.op_code_width = para.getInt("op_code_width", gt = 0)
        this.addr_widths = para.getJSON("addr_widths")
        for addr, width in this.addr_widths.items():
            if width <= 0:
                raise ValueError("%s_addr myst have a positive width\n"%(addr, ))

##################################################################################0

def genPackage(package, moduleName, ports):
    package += "--Include packages used in package declaration\n"
    package += "library ieee;\n"
    package += "use ieee.std_logic_1164.all;\n\n"
    package += "package " + moduleName + "_pkg is\n\t"
    package += "component " + moduleName + " is\n\t"
    package += ports
    package += "\bend component;\n"
    package += "\bend package;\n\n"
    package += "----------------------------------------------------------------------------------------------\n\n"
    return package

def printToFile(outputfile, force, fileText):
    import os
    outputfile += ".vhd"
    if not force and os.path.isfile(outputfile):
        raise FileExistsError(outputfile + " already exists")
    print("Creating " + outputfile)
    f = open(outputfile, "w")
    f.write(str(fileText))
    f.close()

##################################################################################

def genImports(imports):
    imports += "--Include packages used in implanentation\n"
    imports += "library ieee;\n"
    imports += "use ieee.std_logic_1164.ALL;\n"
    imports += "use ieee.numeric_std.ALL;\n"
    return imports

def genEntity(signals, moduleName, ports, para):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"
    return arch

def genPorts(ports, para, instr):
    ports += "port (\n\t"

    # Generate data addr ports
    ports += "--Data Address Ports\n"
    for addr in instr.addrs - set(["res"]):
        ports += "%s_addr : out std_logic_vector(%i downto 0);\n"%(addr, para.addr_widths[addr] - 1)
    ports += "\n"

    # Generate Com Get update ports
    if "update" in para.mem_controls["GET"]:
        ports += "--Comm get update Ports\n"
        for addr in  para.mem_controls["GET"]["update" ]:
            ports += "%s_update : out std_logic;\n"%(addr, )
        ports += "\n"

    # Generate data select ports
    if para.data_selects:
        for addr, accesses in para.data_selects.items():
            ports += "--%s Select Ports\n"%(addr, )
            for mem in accesses:
                ports += "%s_sel_%s : out std_logic;\n"%(addr, mem)
            ports += "\n"

    # Generate ALU Control ports
    ports_d1 = ""
    control_widths = { "carry_in_sel" : 3, "carry_in" : 1, "ALU_mode" : 4, "op_mode" : 7, "in_mode" : 5 }
    for control in para.used_ALU_controls:
        if para.used_ALU_controls[control] == None:
            ports_d1 += "control_%s : out std_logic_vector(%i downto 0);\n"%(control, control_widths[control] - 1)
    # output ALU Control ports
    if ports_d1:
        ports += "--ALU Control Ports\n"
        ports += ports_d1
        ports += "\n"

    # Generate Write Back ports
    ports += "--Write Back Ports\n"
    ports += "res_addr : out std_logic_vector(%i downto 0);\n"%(para.addr_widths["res"] - 1, )
    for mem in instr.accesses["res"]:
        ports += "res_sel_%s : out std_logic;\n"%(mem, )
    ports += "\n"

    # Generate status reg update ports
    if para.status_reg:
        ports += "--Status Registor Update Port\n"
        ports += "status_update : out std_logic;\n"
        ports += "\n"

    # Generate jump ports
    if para.jumps:
        ports += "--Jump Ports\n"
        for jump in para.jumps:
            ports += "%s : out std_logic;\n"%(jump, )
        ports += "\n"

    # Input instr
    ports += "--Input instruction Port\n"
    ports += "instr : in std_logic_vector(%i downto 0)\n"%(para.instr_width - 1,)

    ports += "\b);\n"
    return ports

def processInstrSet(instr, para):
    import copy

    # Calulate instr_width
    para.instr_width = para.op_code_width + sum(para.addr_widths.values())

    # Handle mem mods
    para.mem_controls = {}
    if "GET" in instr.mem_mods and "update" in instr.mem_mods["GET"]:
        para.mem_controls["GET"] = {}
        para.mem_controls["GET"]["update"] = []
        for addr in instr.mem_mods["GET"]["update"]:
            para.mem_controls["GET"]["update"].append(addr)

    # Compute data select ports
    para.data_selects = {}
    # Loop over addrs
    # res addr has selects for all opiton so handled seperately
    for addr in (instr.addrs - set(["res"])):
        # Add normal mem accesses to options
        import copy
        options = copy.copy(instr.accesses[addr])

        # If an addr had more than 1 option
        # create select signal for each memory access
        if len(options) > 1:
            para.data_selects[addr] = []
            for option in options:
                para.data_selects[addr].append(option)

    # Generate status reg update ports
    para.status_reg = instr.mnemonics & set(["CMP"])

    # Calulate what jump ports are needed
    para.jumps = []
    if instr.mnemonics & set(["JMP"]):
        para.jumps.append("jmp")
    if instr.mnemonics & set(["JEQ", "JLE", "JGE"]):
        para.jumps.append("jeq")
    if instr.mnemonics & set(["JGT", "JGE", "JNE"]):
        para.jumps.append("jgt")
    if instr.mnemonics & set(["JLT", "JLE", "JNE"]):
        para.jumps.append("jlt")

    # Calulate for ALU control ports are needed
    used_ALU_controls = { "carry_in_sel" : set(), "carry_in" : set(), "ALU_mode" : set(), "op_mode" : set(), "in_mode" : set() }
    non_ALU_mnemonics =  set(["JMP", "JEQ", "JNE", "JLT", "JLE", "JGT", "JGE"])
    for mnemonic in instr.mnemonics:
        # Filter out non ALU mnmoneics
        if mnemonic in non_ALU_mnemonics :
            pass
        elif mnemonic == "MOV":
            # X <= 0, Y <= 0, Z <= C
            used_ALU_controls["op_mode"].add(0b0110000)
            # Cin = 0
            used_ALU_controls["carry_in"].add(0)
            used_ALU_controls["carry_in_sel"].add(0b000)
            # Op = Z - (X + Y + Cin)
            used_ALU_controls["ALU_mode"].add(0b0011)
        elif mnemonic == "CMP":
            # X <= A:B, Y <= 0, Z <= C
            used_ALU_controls["op_mode"].add(0b0110011)
            # Cin = 0
            used_ALU_controls["carry_in"].add(0)
            used_ALU_controls["carry_in_sel"].add(0b000)
            # Op = Z - (X + Y + Cin)
            used_ALU_controls["ALU_mode"].add(0b0011)
        else:
            raise ValueError("Unknown mnemonic, \"%s\", encountered\n"%(mnemonic, ))

    # Tidy up used_ALU_controls into formused by ALU
    para.used_ALU_controls = {}
    for control_set in used_ALU_controls:
        numValues = len(used_ALU_controls[control_set])
        # Only 1 value used copy control_set across as fixed value
        if numValues == 1:
            para.used_ALU_controls[control_set] = list(used_ALU_controls[control_set])[0]
        # More then 1 value used copy control_set as port
        elif numValues > 1:
            para.used_ALU_controls[control_set] =  None

def genOpcodeAndAddrExtraction(para, instr, signals, arch):
    # Declare OpCode signal
    signals += "--Extracted op_code Signal\n"
    signals += "signal op_code : integer;\n"
    # Create extracting logic
    arch += "-- Extract op_code and addrs from instr\n"

    # Extract op_code
    start = para.instr_width - 1
    end = para.instr_width - para.op_code_width
    arch += "op_code <= to_integer(unsigned(instr(%i downto %i)));\n"%(start, end)

    # Extract res addr
    start = end - 1
    end =  start + 1 - para.addr_widths["res"]
    arch += "res_addr <= instr(%i downto %i);\n"%(start, end)

    # Get all data addrs and sort into ABC order
    addrs = list(instr.addrs - set(["res"]))
    addrs.sort()

    # Extract data addrs
    for addr in addrs:
        start = end - 1
        end = start + 1 - para.addr_widths[addr]
        arch += "%s_addr <= instr(%i downto %i);\n"%(addr, start, end)

    return arch, signals

def genOpcodeDecoding(para, instr, arch):
    from itertools import islice

    arch += "\n--Handle Data Access decoding\n"
    # Generate Comm Get update signals
    if "update" in para.mem_controls["GET"]:
        arch += "--Generate Comm Get update signals\n"
        for addr in  para.mem_controls["GET"]["update" ]:
            arch += "%s_update <= '1' when "%(addr, )
            start = ""; end = "\n\t"
            for instrStr, opcode in instr.instrSet.items():
                _, accesses = InstrSet.decomposeInstr(instrStr)
                for access in accesses:
                    if access["mem"] == "GET" and "update" in access["mem_mods"]:
                        arch += "%sop_code = %i%s"%(start, opcode, end)
                        start = "or "; end = "\n"
            arch += "\belse '0';\n"
        arch += "\n"

    # Generate data_selects signals
    for addr, accesses in para.data_selects.items():
        arch += "--Generate %s select signals\n"%(addr, )
        for mem in accesses:
            arch += "%s_sel_%s <= '1' when "%(addr, mem)
            start = ""; end = "\n\t"
            # Handle concat select
            if mem == "concat":
                for instrStr, opcode in instr.instrSet.items():
                    _, instr_accesses = InstrSet.decomposeInstr(instrStr)
                    for instr_access in instr_accesses:
                        if instr_access["addr"] == "a" and "concat" in instr_access["addr_mods"]:
                            arch += "%sop_code = %i%s"%(start, opcode, end)
                            start = "or "; end = "\n"
            # Handle normal Mem accesses
            else:
                for instrStr, opcode in instr.instrSet.items():
                    _, instr_accesses = InstrSet.decomposeInstr(instrStr)
                    for instr_access in instr_accesses:
                        if instr_access["addr"] == addr and instr_access["mem"] == mem:
                            arch += "%sop_code = %i%s"%(start, opcode, end)
                            start = "or "; end = "\n"
            arch += "\belse '0';\n"
        arch += "\n"

    # Generate ALU control signals
    # Generate op_mode if using port
    if "op_mode" in para.used_ALU_controls and para.used_ALU_controls["op_mode"] == None:
        arch += "--Generate op_mode signal\n"

        # Build list of values and conditions
        values = []
        # X <= 0, Y <= 0, Z <= C mode
        mode_mnemonics = set(["MOV"])
        if instr.mnemonics & mode_mnemonics:
            # Build condition
            lines = ["%i"%(0b0110000, ) ]
            connect = ""
            for instrStr, opcode in instr.instrSet.items():
                mnemonic, _ = InstrSet.decomposeInstr(instrStr)
                if mnemonic in mode_mnemonics:
                    lines.append("%sop_code = %i"%(connect, opcode))
                    connect = "or "
            # Add value and condition to list
            values.append(lines)

        # X <= A:B, Y <= 0, Z <= C mode
        mode_mnemonics = set(["CMP"])
        if instr.mnemonics & mode_mnemonics:
            # Build condition
            lines = ["%i"%(0b0110011, ) ]
            connect = ""
            for instrStr, opcode in instr.instrSet.items():
                mnemonic, _ = InstrSet.decomposeInstr(instrStr)
                if mnemonic in mode_mnemonics:
                    lines.append("%sop_code = %i"%(connect, opcode))
                    connect = "or "
            # Add value and condition to list
            values.append(lines)

        # Convert list to VHDL
        arch += "control_op_mode <= "
        backup = ""
        for value in islice(values, 1, None):
            arch += "%sstd_logic_vector(to_unsigned(%s, 7)) when %s\n\t"%(backup, value[0],  value[1])
            backup = "\b"
            for line in islice(value, 2, None):
                arch += "%s\n"%(line, )
        arch += "\belse std_logic_vector(to_unsigned(%s, 7));\n\n"%(values[0][0], )

    # Generate Result destination select signals
    arch += "--Generate Result destination select signals\n"
    for mem in instr.accesses["res"]:
        arch += "res_sel_%s <= '1' when "%(mem, )
        start = ""; end = "\n\t"
        for instrStr, opcode in instr.instrSet.items():
            _, accesses = InstrSet.decomposeInstr(instrStr)
            for access in accesses:
                if access["mem"] == mem:
                    arch += "%sop_code = %i%s"%(start, opcode, end)
                    start = "or "; end = "\n"
        arch += "\belse '0';\n"

    # Generate Status Registor Update signal
    if para.status_reg:
        arch += "\n--Generate Status Registor Update signal\n"
        arch += "status_update <= '1' when "
        start = ""; end = "\n\t"
        for instrStr, opcode in instr.instrSet.items():
            mnmoneic, _ = InstrSet.decomposeInstr(instrStr)
            for access in accesses:
                if mnmoneic == "CMP":
                    arch += "%sop_code = %i%s"%(start, opcode, end)
                    start = "or "; end = "\n"
        arch += "\belse '0';\n"

    # Generate jump signals
    arch += "\n--Generate Jump signals\n"
    for jump in para.jumps:
        arch += "%s <= '1' when "%(jump, )
        start = ""; end = "\n\t"
        for instrStr, opcode in instr.instrSet.items():
            mnmoneic, _ = InstrSet.decomposeInstr(instrStr)
            if mnmoneic == jump.upper():
                arch += "%sop_code = %i%s"%(start, opcode, end)
                start = "or "; end = "\n"
        arch += "\belse '0';\n"
    return arch

#Root Generate function
def generate(settings):
    # Process passed json parameters
    para  = readParaJson(settings.jsonStr)
    instr = InstrSet.readInstrSetJson(settings.instrJson)
    processInstrSet(instr, para)

    #Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para, instr)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports, para)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    #Add entity behavour to arch string
    arch, signals = genOpcodeAndAddrExtraction(para, instr, signals, arch)
    arch = genOpcodeDecoding(para, instr, arch)

    # Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

    return para.instr_width, para.mem_controls, para.data_selects, para.used_ALU_controls, para.status_reg, para.jumps

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    # Add Needed paths
    pathRoot = sys.path[0] + "\\.."
    sys.path.append(pathRoot)

    # Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput(True)
    settings.pathRoot = pathRoot
    generate(settings)
