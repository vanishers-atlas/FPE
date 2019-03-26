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
        this.use_BROM = para.getBool("use_BROM")
        this.data_values= para.getString("data_values")
        this.conc_reads = para.getInt("conc_reads", gt = 0)
        this.data_width = para.getInt("data_width", gt = 0)
        this.depth      = para.getInt("depth"     , gt = 0)
        this.addr_width = calulateAddrWidth(this.depth)

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
    ports += "--Addr Ports\n"
    for read_Num in range(para.conc_reads):
        ports += "addr_%i : in std_logic_vector(%s downto 0);\n"%(read_Num, para.addr_width - 1)
    ports += "\n--Read Ports\n"
    for i in range(para.conc_reads - 1):
        ports += "data_%i : out std_logic_vector(%s downto 0);\n"%(read_Num, para.data_width - 1)
    ports += "data_%i : out std_logic_vector(%s downto 0)\n"%(para.conc_reads - 1, para.data_width - 1)
    ports += "\b);\n"
    return ports

def genNonHardwareData(para, signals, imports):
    #Add imports for ** operaters
    imports += "use ieee.math_real.all;\n"
    imports += "use std.textio.all;\n"

    #Generate inferal data type
    signals += "type mem_type is array (0 to %i) of std_logic_vector (%i downto 0);\n"%(para.depth - 1, para.data_width - 1)

    signals += "\nimpure function init_mem(mif_filename : in string) return mem_type is\n\t"
    signals += "file mif_file : text open read_mode is mif_filename;\n"
    signals += "variable mif_line : line;\n"
    signals += "variable temp_bv  : bit_vector(%i downto 0);\n"%(para.data_width - 1)
    signals += "variable temp_mem : mem_type;\n"
    signals += "\bbegin\n\t"
    signals += "for index in mem_type'range loop\n\t"
    signals += "if ENDFILE(mif_file) then\n\t"
    signals += "exit;\n"
    signals += "\belse\n\t"
    signals += "readline(mif_file, mif_line);\n"
    signals += "read(mif_line, temp_bv);\n"
    signals += "temp_mem(index) := to_stdlogicvector(temp_bv);\n"
    signals += "\bend if;\n"
    signals += "\bend loop;\n"
    signals += "return temp_mem;\n"
    signals += "\bend function;\n"

    signals += "\nsignal data : mem_type  := init_mem(\"%s\");\n"%(para.data_values,)

    return signals, imports

def genNonHardwareRead(para, arch):
    arch += "--Read Handling\n"
    for read_Num in range(para.conc_reads):
        arch += "data_%i <= data(to_integer(unsigned(addr_%i)));\n"%(read_Num,read_Num)
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
    if not para.use_BROM:
        imports += "use ieee.numeric_std.all;\n"
        signals, imports = genNonHardwareData(para, signals, imports)
        arch = genNonHardwareRead (para, arch)
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
