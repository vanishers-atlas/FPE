def calulateAddrWidth(depth):
    import math
    return math.ceil(math.log(depth - 1, 2))

class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        this.use_BRAM =  para.getBool("use_BRAM")
        this.conc_reads = para.getInt("conc_reads", gt = 0)
        this.data_width = para.getInt("data_width", gt = 0)
        this.depth      = para.getInt("depth"     , gt = 0)
        this.addr_width = calulateAddrWidth(this.depth)

        this.write_mode = para.getString("write_mode").lower()
        if not this.write_mode in ["high", "sync", "edge"]:
            raise ValueError("Unknown write_mode, \"%s\"\n"%(this.write_mode, ))

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
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"
    return arch

def genPorts(ports, para):
    ports += "port (\n\t"

    #Add Calulate read ports
    ports += "--Addr Ports\n"
    ports_d1 = "\n--Read Ports\n"
    for read_Num in range(para.conc_reads):
        ports += "read_addr_%i : in std_logic_vector(%i downto 0);\n"%(read_Num, para.addr_width - 1)
        ports_d1  += "read_data_%i : out std_logic_vector(%i downto 0);\n"%(read_Num, para.data_width - 1)
    ports += ports_d1

    #Add Calulate write ports
    ports += "\n--Write Ports\n"
    if para.write_mode == "sync":
        ports += "clock : in std_logic;\n"
    ports += "write_enable : in std_logic;\n"
    ports += "write_addr : in std_logic_vector(%i downto 0);\n"%(para.addr_width - 1,)
    ports += "write_data : in std_logic_vector(%i downto 0) \n"%(para.data_width - 1,)
    ports += "\b);\n"
    return ports

def genNonHardwareData(para, signals, imports):
    #Add imports for ** operaters
    imports += "use ieee.math_real.all;\n"
    imports += "use std.textio.all;\n"

    #Generate inferal data type
    signals += "type mem_type is array (0 to %i) of std_logic_vector(%i downto 0);\n"%(para.depth - 1, para.data_width - 1)
    signals += "\nsignal data : mem_type;\n"

    return signals, imports

def genNonHardwareRead(para, arch):
    arch += "--Read Handling\n"
    for read_Num in range(para.conc_reads):
        arch += "read_data_%i <= data(to_integer(unsigned(read_addr_%i)));\n"%(read_Num, read_Num)
    return arch

def genNonHardwareWrite(para, arch):
    arch += "\n--Write Handling\n"

    #Build sencitivity list
    arch += "process ("
    if para.write_mode == "sync":
        arch += "clock"
    else:
        arch += "write_enable"
        if para.write_mode == "high":
            arch += ", write_data"
    arch += ")\nbegin\n\t"

    #create write_enable behavour
    if para.write_mode == "high":
        arch += "if write_enable = '1' then\n\t"
    elif para.write_mode == "sync":
        arch += "if clock'event and clock = '1' and write_enable = '1' then\n\t"
    elif para.write_mode == "edge":
        arch += "if write_enable'event and write_enable = '1' then\n\t"
    else:
        raise ValueError("unknown write_mode \"%s\""%(para.write_mode, ))

    #perform write
    arch += "data(to_integer(unsigned(write_addr))) <= write_data;\n"

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
    if not para.use_BRAM:
        imports += "use ieee.numeric_std.all;\n"
        signals, imports = genNonHardwareData(para, signals, imports)
        arch = genNonHardwareRead (para, arch)
        arch = genNonHardwareWrite(para, arch)
    else:
        raise NotImplementedError()

    #Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

    return para.addr_width

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
