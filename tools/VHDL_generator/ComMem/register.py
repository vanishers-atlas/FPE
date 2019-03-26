class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        this.has_reset  = para.getBool("has_reset")
        this.has_preset = para.getBool("has_preset")

        # Get and translate write
        this.write_mode = para.getString("write_mode").lower()
        if not this.write_mode in ["high", "sync", "edge"]:
            raise ValueError("Unknown write_mode, \"%s\"\n"%(this.write_mode, ))

        this.read_mode = para.getString("read_mode").lower()
        if not this.read_mode in ["high", "sync", "always"]:
            raise ValueError("Unknown read_mode, \"%s\"\n"%(this.read_mode, ))


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
    return imports

def genEntity(signals, moduleName, ports):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    signals += "signal storedValue : std_logic_vector(data_width-1 downto 0);\n"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"

    #Add asserts for relationships before generics
    arch += "assert (data_width > 0)\n\t"
    arch += "report \"data_width must be positive\"\n"
    arch += "severity failure;\n\b\n"

    return arch

def genPorts(ports, para):
    ports += "generic (\n\t"
    ports += "data_width : integer := 8\n"
    ports += "\b);\n"
    ports += "port (\n\t"
    if para.write_mode == "sync" or para.read_mode == "sync":
        ports += "clock : in std_logic;\n"
    if para.has_reset:
        ports += "reset : in std_logic;\n"
    if para.has_preset:
        ports += "preset : in std_logic;\n"
    ports += "--Data ports\n"
    ports += "write_enable : in std_logic;\n"
    if para.read_mode != "always":
        ports += "read_enable: in std_logic;\n"
    ports += "data_in   : in  std_logic_vector(data_width-1 downto 0);\n"
    ports += "data_out  : out std_logic_vector(data_width-1 downto 0)\n"
    ports += "\b);\n"
    return ports

def genOutputBehavour(para, arch):
    arch += "\n--Handle output of storedValue\n"

    # Check if process is required
    if para.read_mode != "always":
        #Build sencitivity list
        arch += "process ("
        if para.read_mode == "high":
            arch += "storedValue, read_enable"
        elif para.read_mode == "sync":
            arch += "clock"
        else:
            raise ValueError("unknown read mode %s"%(para.read_mode, ))
        arch += ")\nbegin\n\t"

        if para.read_mode == "sync":
            #Only check read_enable on clock raising edge
            arch += "if clock'event and clock = '1' then"
        arch += "if read_enable = '1' then\n\t"
    arch += "data_out <= storedValue;\n"
    # End process
    if para.read_mode != "always":
        arch += "\belse\n\t"
        arch += "data_out <= (others => 'Z');\n"
        arch += "\bend if;\n"
        if para.read_mode == "sync":
            #Close raising edge detection if
            arch += "\bend if;\n"
        arch += "\bend process;\n"
    return arch

def genStoredValueUpdating(para, arch):
    arch += "\n--Hanlde stored Value updating behavour\n"
    arch += "process ("
    #Build sencitivity list
    if para.write_mode == "sync":
        arch += "clock"
    else:
        arch += "write_enable"
        if para.write_mode == "high":
            arch += ", data_in"
    if para.has_reset:
        arch += ", reset"
    if para.has_preset:
        arch += ", preset"
    arch += ")\nbegin\n\t"

    #create reset behavour
    if para.has_reset:
        arch += "if reset = '1' then\n\t"
        arch += "storedValue <= (others => '0');\n"
        arch += "\bels"

    #create preset behavour
    if para.has_preset:
        arch += "if preset = '1' then\n\t"
        arch += "storedValue <= (others => '1');\n"
        arch += "\bels"

    #create read behavour
    if para.write_mode == "high":
        arch += "if write_enable = '1' then\n\t"
    elif para.write_mode == "edge":
        arch += "if write_enable'event and write_enable = '1' then\n\t"
    elif para.write_mode == "sync":
        arch += "if clock'event and clock = '1' and write_enable = '1' then\n\t"
    else:
        raise ValueError("Unknown write_mode \"%s\""%(para.write_mode, ))
    arch += "storedValue <= data_in;\n"
    arch += "\bend if;\n"

    arch += "\bend process;\n"
    return arch

#Root Generate function
def generate(settings):
    #Process passed json parameters
    para = parameters(settings.jsonStr)

    #Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    #Add entity behavour to arch string
    arch = genOutputBehavour(para, arch)
    arch = genStoredValueUpdating(para, arch)

    #Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    #Add Needed paths
    pathRoot = sys.path[0] + "\\.."
    sys.path.append(pathRoot)

    #Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput()
    settings.pathRoot = pathRoot
    generate(settings)
