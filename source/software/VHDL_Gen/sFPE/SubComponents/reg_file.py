def calulateAddrWidth(num_regs):
    import math
    return math.ceil(math.log(num_regs, 2))

class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes
        this.conc_reads = para.getInt("conc_reads", gt = 0)
        this.number_reg = para.getInt("number_reg", gt = 0)
        this.data_width = para.getInt("data_width", gt = 0)
        this.reg_addr_width = calulateAddrWidth(this.number_reg)

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

    #Generate Read ports
    data_ports = "--Read Data Ports\n"
    addr_ports = "\n--Read Address Ports\n"
    for i in range(para.conc_reads):
        suffix = "_%i"%(i,)
        if(para.conc_reads == 1):
            suffix = ""
        data_ports += "read_data%s : out std_logic_vector(%i downto 0);\n"%(suffix, para.data_width - 1)
        addr_ports += "read_addr%s : in  std_logic_vector(%i downto 0);\n"%(suffix, para.reg_addr_width - 1)
    ports += data_ports + addr_ports

    #Generate write ports
    ports += "\n--Write Ports\n"
    ports += "write_data : in std_logic_vector(%i downto 0);\n"%(para.data_width - 1,)
    ports += "write_addr : in std_logic_vector(%i downto 0);\n"%(para.reg_addr_width - 1,)
    ports += "write_enable : in std_logic\n"

    ports += "\b);\n"
    return ports

def genRegisters(para, settings, arch, signals, imports):
    #Create Register VHDL
    settings.moduleName = "reg_FFEA"
    settings.jsonStr  = "{"
    settings.jsonStr += "\"has_reset\" : false,"
    settings.jsonStr += "\"has_preset\": false,"
    settings.jsonStr += "\"write_mode\": \"edge\","
    settings.jsonStr += "\"read_mode\" : \"always\""
    settings.jsonStr += "}"
    import register
    register.generate(settings)

    #Import Created Register
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    signals += "--Register Output Signals\n"
    signals_d1 = "\n--Register Write Signals\n"
    arch += "--Registers\n"
    for reg in range(para.number_reg):
        #Create in and out signals
        signals += "signal reg_%i_out : std_logic_vector(%i downto 0);\n"%(reg, para.data_width - 1)
        signals_d1 += "signal reg_%i_write : std_logic;\n"%(reg,)

        #Add register to arch
        arch += "reg_%i : %s\n\t"%(reg, settings.moduleName)
        arch += "generic map (data_width => %i)\n"%(para.data_width,)
        arch += "port map (\n\t"
        arch += "write_enable => reg_%i_write,\n"%(reg,)
        arch += "data_in   => write_data,\n"
        arch += "data_out  => reg_%i_out\n"%(reg,)
        arch += "\b);\n\b\n"
    signals += signals_d1
    return arch, signals, imports

def genReadPaths(para, settings, arch, signals, imports):
    # Create Read Mux VHDL
    settings.moduleName = "mux_%i"%(para.number_reg,)
    settings.jsonStr = "{ \"number_inputs\" : %i, \"binary_select\" : true}"%(para.number_reg,)
    import mux
    if mux.generate(settings)[0] != para.reg_addr_width:
        raise ValueError("Mux address width not equal reg file addr width\n")

    # Import Created mux
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    #Add Read Muxes to arch
    arch += "--Read Muxes\n"
    for read_op in range(para.conc_reads):
        #Add mux to architecture
        arch += "Read_%i_mux : %s\n\t"%(read_op, settings.moduleName)
        arch += "generic map (data_width => %i)\n"%(para.data_width,)
        arch += "port map (\n\t"
        for reg in range(para.number_reg):
            arch += "input_%i => reg_%i_out,\n"%(reg, reg)
        arch += "input_select => read_addr_%i,\n"%(read_op,)
        arch += "data_out  => read_data_%i\n"%(read_op,)
        arch += "\b);\n\b\n"
    return arch, signals, imports

def genWritePath(para, settings, arch, signals, imports):
    # Create Write demux VHDL
    settings.moduleName = "demux_%i"%(para.number_reg,)
    settings.jsonStr = "{ \"number_outputs\" : %i, \"binary_select\" : true}"%(para.number_reg,)
    import demux
    if demux.generate(settings)[0] != para.reg_addr_width:
        raise ValueError("Demux address width not equal reg file addr width\n")

    #Import Created mux
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    #Add demux to architecture
    arch += "-- Write enable demux\n"
    arch += "write_demux : %s\n\t"%(settings.moduleName,)
    arch += "generic map (data_width => 1)\n"
    arch += "port map (\n\t"
    for reg in range(para.number_reg):
        arch += "output_%i(0) => reg_%i_write,\n"%(reg, reg)
    arch += "output_select => write_addr,\n"
    arch += "data_in(0)  => write_enable\n"
    arch += "\b);\n\b"

    return arch, signals, imports

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
    arch, signals, imports = genRegisters(para, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genReadPaths(para, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genWritePath(para, copy.copy(settings), arch, signals, imports)

    #Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

    return para.reg_addr_width

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
