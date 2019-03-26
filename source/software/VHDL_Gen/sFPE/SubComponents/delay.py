class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        import math
        #Extract json fields to object fields, checking as goes
        this.has_data_enable = para.getBool("has_data_enable")
        this.has_reset = para.getBool("has_reset")

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

def genEntity(signals, moduleName, ports, para):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"
    return arch

def genPorts(ports, para):
    ports += "generic (\n\t"
    if para.has_data_enable or para.has_reset:
        ports += "default_value : integer := 0;\n"
    ports += "data_width : integer := 8;\n"
    ports += "data_depth : integer := 64"
    ports += "\n\b);\n"
    ports += "port (\n\t"
    ports += "clock : in std_logic;\n"
    if para.has_reset :
        ports += "reset : in std_logic;\n"
    if para.has_data_enable:
        ports += "data_enable : in std_logic;\n"
    ports += "data_in  : in  std_logic_vector(data_width - 1 downto 0);\n"
    ports += "data_out : out std_logic_vector(data_width - 1 downto 0) \n"
    ports += "\b);\n"
    return ports

def genGenerticsChecking(para, arch, imports):
    #Add asserts for generics requirements
    arch += "assert (data_width > 0)\n\t"
    arch += "report \"data_width must be positive\"\n"
    arch += "severity failure;\n\b\n"

    arch += "assert (data_depth > 0)\n\t"
    arch += "report \"data_depth must be positive\"\n"
    arch += "severity failure;\n\b\n"

    if para.has_data_enable or para.has_reset:
        imports += "use ieee.numeric_std.all;\n\n"

        arch += "assert (default_value > 0)\n\t"
        arch += "report \"default_value must be positive\"\n"
        arch += "severity failure;\n\b\n"

        arch += "assert (default_value < 2 ** data_width)\n\t"
        arch += "report \"default_value to large to fill in data_width bits\"\n"
        arch += "severity failure;\n\b\n"
    return arch, imports

def genDelay(para, arch, signals):
    #Add SRL signals
    signals += "type delay_data is array (data_depth - 1 downto 0) of std_logic_vector (data_width - 1 downto 0);\n"
    signals += "signal data : delay_data;\n"

    #Add head outputing behavour
    arch += "--Output Delaysd data\n"
    arch += "data_out <= data(0);\n"

    #Add write behavour
    arch += "\n--Handle data inserting\n"
    arch += "process(clock)\n\t"
    arch += "\bbegin\n\t"
    arch += "if clock'event and clock = '1'"
    if para.has_reset:
        arch += " and reset = '0'"
    arch += " then\n\t"
    if para.has_data_enable:
        arch += "if data_enable = '1' then\n\t"
    arch += "data <= data(data'left - 1 downto 0) & data_in;\n"
    if para.has_data_enable:
        arch += "\belse\n\t"
        arch += "data <= data(data'left - 1 downto 0) & std_logic_vector(to_unsigned(default_value, data_width));\n"
        arch += "\bend if;\n"
    arch += "\bend if;\n"
    arch += "\bend process;\n"

    #Handle reset behavour
    if para.has_reset:
        arch += "\n--Handle reset\n"
        arch += "process(reset)\n\t"
        arch += "\bbegin\n\t"
        arch += "if reset = '1' then\n\t"
        arch += "data <= (others => std_logic_vector(to_unsigned(default_value, data_width)));\n"
        arch += "\bend if;\n"
        arch += "\bend process;\n"
    return arch, signals

#Root Generate function
def generate(settings):
    #Process passed json parameters
    para = parameters(settings.jsonStr)

    #Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports, para)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    #Add entity behavour to arch string
    import copy
    arch, imports = genGenerticsChecking(para, arch, imports)
    arch, signals = genDelay  (para, arch, signals)

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
