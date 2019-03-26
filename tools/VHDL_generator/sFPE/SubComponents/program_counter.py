class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        import math
        this.PC_wrap_value = para.getInt("PC_wrap_value", gt = 0)
        this.PC_width      = para.getInt("PC_width", gte = math.ceil(math.log(this.PC_wrap_value, 2)))
        this.overFlow_wrap = this.PC_wrap_value == 2**this.PC_width

        # Extract jumping enables
        this.required_status_inputs = set()
        this.jumps = set()
        for jump in para.getArray("jumps_enabled"):
            this.jumps.add(jump)

###s###############################################################################0

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
    return imports

def genEntity(signals, moduleName, ports):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"
    return arch

def genPorts(ports, para):
    ports += "port (\n\t"

    # Handle jump related ports
    if para.jumps:
        ports += "--Jump Ports\n"
        ports += "jump_occured : out std_logic;\n"
        ports += "jump_addr : in std_logic_vector(%i downto 0);\n"%(para.PC_width - 1,)
        for jump in para.jumps:
            ports += "%s : in std_logic;\n"%(jump, )

    # Handle status input ports
    if para.required_status_inputs:
        ports += "--status Ports\n"
        for port in para.required_status_inputs:
            ports += "status_%s : in std_logic;\n"%(port, )

    ports += "\n--General Ports\n"
    ports += "clock: in std_logic;\n"
    ports += "reset: in std_logic;\n"
    ports += "value : out std_logic_vector(%i downto 0)\n"%(para.PC_width - 1,)
    ports += "\b);\n"
    return ports

def genRegister(para, settings, arch, signals, imports):
    import sys
    sys.path.append(settings.pathRoot + "\\ComMem")

    # Create Register VHDL
    import register
    settings.moduleName = "reg_TFEA"
    settings.jsonStr  = "{"
    settings.jsonStr += "\"has_reset\" : true,"
    settings.jsonStr += "\"has_preset\": false,"
    settings.jsonStr += "\"write_mode\": \"edge\","
    settings.jsonStr += "\"read_mode\" : \"always\""
    settings.jsonStr += "}"
    register.generate(settings)

    # Import Created Register to VHDL
    imports += "\nlibrary work;\n"
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    # declare registor signals
    signals += "\n--Register Signals\n"
    signals += "signal notClock: std_logic;\n"
    signals += "signal next_PC : std_logic_vector(%i downto 0);\n"%(para.PC_width - 1,)
    signals += "signal curr_PC : std_logic_vector(%i downto 0);\n"%(para.PC_width - 1,)

    # Generate not clock signal
    arch += "\n--Generate not clock signal\n"
    arch += "notClock <= not clock;\n"

    # Add PC register
    arch += "\n--Store PC's Value\n"
    arch += "PC : %s\n\t"%(settings.moduleName,)
    arch += "generic map (data_width => %i)\n"%(para.PC_width,)
    arch += "port map (\n\t"
    arch += "reset => reset,\n"
    arch += "write_enable => notClock,\n"
    arch += "data_in   => next_PC,\n"
    arch += "data_out  => curr_PC\n"
    arch += "\b);\n\b"

    # Connect Value port to registor output
    arch += "\n--Connect Vvlue port to registor output\n"
    arch += "value <= curr_PC;\n"

    return arch, signals, imports

def genJumpLogic(para, arch, signals):
    if para.jumps:
        # Add internal jump signal
        signals += "\nsignal  internal_jump : std_logic;\n"
        arch += "\n--Connent jump_occured port to internal_jump\n"
        arch += "jump_occured <= internal_jump;\n"

        # Generate internal_jump signal
        arch += "\n--Generate internal_jump signal\n"
        arch += "jump_occured <= '1' when \n\t"
        connetor = "   "

        import copy
        jumps = copy.copy(para.jumps)

        # Handle unconditional jump
        if "jmp" in para.jumps:
            arch += "%sjmp = '1'\n"%(connetor, )
            connetor = "or "
            jumps.discard("jmp")

        # handle Jump if equal
        if "jeq" in para.jumps:
            arch += "%s(jeq = '1' and status_equal = '1')\n"%(connetor, )
            connetor = "or "
            jumps.discard("jeq")
            para.required_status_inputs.add("equal")

        # handle Jump if less
        if "jlt" in para.jumps:
            arch += "%s(jlt = '1' and status_less = '1')\n"%(connetor, )
            connetor = "or "
            jumps.discard("jlt")
            para.required_status_inputs.add("less")

        # handle Jump if greater
        if "jgt" in para.jumps:
            arch += "%s(jgt = '1' and status_equal = '0' and status_less = '0')\n"%(connetor, )
            connetor = "or "
            jumps.discard("jlt")
            para.required_status_inputs.add("equal")
            para.required_status_inputs.add("less")

        # Finish internal_jump generation
        arch += "\belse '0';\n"

        # Check for unknown jumps
        if jumps:
            str = ""
            for code in jumps:
                if str != "":
                    str += ", "
                str += code
            raise ValueError("Unknown jumps: %s\n"%(str, ))
    return arch, signals

def genUpdateLogic(para, arch, signals, imports):
    # Import numeric_std for adding
    imports += "use ieee.numeric_std.ALL;\n"

    # Add Update behavour
    arch += "\n--Generate next_PC\n"
    arch += "process(curr_PC, internal_jump)\n\t"
    arch += "variable PC_inc : integer := to_integer(unsigned(curr_PC));\n"
    arch += "\bbegin\n\t"

    # Handle Jumping
    if para.jumps:
        arch += "if internal_jump = '1' then\n\t"
        arch += "next_PC <= jump_addr;\n"
        arch += "\belse\n\t"

    # Handle incing
    arch += "PC_inc := PC_inc + 1;\n"
    # Handle wrapping
    if not para.overFlow_wrap:
        arch += "if PC_inc = %i then\n\t"%(para.PC_wrap_value, )
        arch += "PC_inc := 0;\n"
        arch += "\bend if;\n"
    arch += "next_PC <= std_logic_vector(to_unsigned(PC_inc, %i));\n"%(para.PC_width - 1, )

    # Close the jump if
    if para.jumps:
        arch +="\bend if;\n"

    arch += "\bend process;\n"

    return arch, signals, imports

#Root Generate function
def generate(settings):
    #Process passed json parameters
    para = parameters(settings.jsonStr)

    #Start creating VHDL
    import indentedString
    signals = indentedString.indentedString()
    imports = genImports(indentedString.indentedString())
    arch    = genArch(indentedString.indentedString())

    #Add entity behavour to arch string
    import copy
    arch, signals, imports = genRegister(para, copy.copy(settings), arch, signals, imports)
    arch, signals = genJumpLogic (para, arch, signals)
    arch, signals, imports = genUpdateLogic(para, arch, signals, imports)

    # Finished creating VHDL
    ports   = genPorts  (indentedString.indentedString(), para)
    enity   = genEntity (indentedString.indentedString(), settings.moduleName, ports)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + enity + signals + arch)

    # Return required status ports
    return list(para.required_status_inputs)

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    #Add Needed paths
    pathRoot = sys.path[0] + "\\..\\.."
    sys.path.append(pathRoot)

    #Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput(False)
    settings.pathRoot = pathRoot
    generate(settings)
