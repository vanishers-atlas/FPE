def calulateAddrWidth(num_FIFOs):
    import math
    return math.ceil(math.log(num_FIFOs, 2))

class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        this.number_FIFOs = para.getInt("number_FIFOs", gt = 0)
        this.addr_width   = calulateAddrWidth(this.number_FIFOs)

        this.data_width = para.getInt("data_width", gt = 0)

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
    ports += "port (\n\t"

    ports += "--FIFO Data Ports\n"
    ports_d1 = "\n--FIFO Update Ports\n"
    for fifo in range(para.number_FIFOs):
        ports += "FIFO_%i : out std_logic_vector(%i downto 0);\n"%(fifo, para.data_width - 1)
        ports_d1 += "update_FIFO_%i : out std_logic;\n"%(fifo,)
    ports += ports_d1

    ports += "\n--sFPE Ports\n"
    ports += "data    : in std_logic_vector(%i downto 0);\n"%(para.data_width - 1,)
    ports += "address : in std_logic_vector(%i downto 0);\n"%(para.addr_width - 1,)
    ports += "enable  : in std_logic;\n"

    ports += "\nclock : in std_logic\n"
    ports += "\b);\n"
    return ports

def genUpdateSignal(para, arch, signals):
    #Add Update signal
    signals += "--Update signal\n"
    signals += "signal update : std_logic;\n"

    #Add generating logic
    arch += "--Generate update signal\n"
    arch += "update <= '1' when enable = '1' and clock = '0' else '0';\n"
    return arch, signals

def genDemux(para, settings, arch, imports):
    #Create Demux VHDL
    import demux
    settings.moduleName = "demux_%i"%(para.number_FIFOs,)
    settings.jsonStr = "{\"number_outputs\" : %i, \"binary_select\" : true}"%(para.number_FIFOs,)
    if demux.generate(settings)[0] != para.addr_width:
        raise ValueError("Demux addr width not equal com put addr width\n")

    #Import Created Demux to VHDL
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    #Add Update demux
    arch += "\n--Demux Update\n"
    arch += "update_demux : %s\n\t"%(settings.moduleName,)
    arch += "generic map (data_width => 1)\n"
    arch += "port map (\n\t"
    for fifo in range(para.number_FIFOs):
        arch += "output_%i(0) => update_FIFO_%i,\n"%(fifo, fifo)
    arch += "data_in(0)  => update,\n"
    arch += "output_select => address\n"
    arch += "\b);\n\b"

    #Add Data demux
    arch += "\n--Demux Data\n"
    arch += "data_demux : %s\n\t"%(settings.moduleName,)
    arch += "generic map (data_width => %i)\n"%(para.data_width,)
    arch += "port map (\n\t"
    for fifo in range(para.number_FIFOs):
        arch += "output_%i => FIFO_%i,\n"%(fifo, fifo)
    arch += "data_in  => data,\n"
    arch += "output_select => address\n"
    arch += "\b);\n\b"

    return arch, imports

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
    sys.path.append(settings.pathRoot + "\\ComComp")
    imports += "\nlibrary work;\n"
    arch, signals = genUpdateSignal(para, arch, signals)
    arch, imports = genDemux(para, copy.copy(settings), arch, imports)

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
    pathRoot = sys.path[0] + "\\..\\.."
    sys.path.append(pathRoot)

    #Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput()
    settings.pathRoot = pathRoot
    generate(settings)
