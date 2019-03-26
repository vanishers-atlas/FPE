def calulateAddrWidth(num_FIFOs):
    import math
    return math.ceil(math.log(num_FIFOs, 2))

class parameters:
    def __init__(this, jsonStr):
        # Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        # Extract json fields to object fields, checking as goes
        this.conc_reads   = para.getInt("conc_reads"  , gt = 0)
        this.conc_updates = para.getInt("conc_updates", gt = 0, lte = this.conc_reads)
        this.number_FIFOs = para.getInt("number_FIFOs", gt = 0)
        this.data_width   = para.getInt("data_width"  , gt = 0)

        # Calulate para derived values
        this.addr_width = calulateAddrWidth(this.number_FIFOs)

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
    # Generate FIFO ports
    ports += "--FIFO Data Ports\n"
    ports_d1 = "\n--FIFO Update Ports\n"
    update_ports = ""
    for fifo in range(para.number_FIFOs):
        ports += "FIFO_%i : in std_logic_vector(%i downto 0);\n"%(fifo, para.data_width - 1)
        ports_d1 += "update_FIFO_%i : out std_logic;\n"%(fifo,)
    ports += ports_d1

    # Generate read ports
    ports += "\n--Read Address Ports\n"
    ports_d1 = "\n--Read Data Ports\n"
    for opID in range(para.conc_reads):
        ports += "address_%i : in  std_logic_vector(%i downto 0);\n"%(opID, para.addr_width - 1)
        ports_d1 += "data_%i  : out std_logic_vector(%i downto 0);\n"%(opID, para.data_width - 1)
    ports += ports_d1

    # Generate update ports
    ports += "\n--Read Update Ports\n"
    for opID in range(para.conc_updates):
        ports += "update_%i : in std_logic;\n"%(opID, )

    ports += "\nclock : in std_logic\n"
    ports += "\b);\n"
    return ports

def genBuffers(para, settings, arch, signals, imports):
    # Create buffer Register VHDL
    settings.moduleName = "reg_FFEA"
    settings.jsonStr  = "{"
    settings.jsonStr += "\"has_reset\" : false,"
    settings.jsonStr += "\"has_preset\": false,"
    settings.jsonStr += "\"write_mode\": \"edge\","
    settings.jsonStr += "\"read_mode\" : \"always\""
    settings.jsonStr += "}"
    import register
    register.generate(settings)

    # Import Created Register to VHDL
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    # Generate FIFO ports Buffers
    signals +="--FIFO buffer signals\n"
    arch += "--Buffer FIFO ports\n"
    for fifo in range(para.number_FIFOs):
        # Declare buffer output signal
        signals += "signal FIFO_%i_buff_out : std_logic_vector(%i downto 0);\n"%(fifo,para.data_width - 1)

        # Instantiate buffer
        arch += "FIFO_%i_buff : %s\n\t"%(fifo, settings.moduleName)
        arch += "generic map (data_width => %i)\n"%(para.data_width, )
        arch += "port map (\n\t"
        arch += "write_enable => clock,\n"
        arch += "data_in   => FIFO_%i,\n"%(fifo, )
        arch += "data_out  => FIFO_%i_buff_out\n"%(fifo, )
        arch += "\b);\n\b"

    return arch, signals, imports

def genReadMuxes(para, settings, arch, imports):
    # Create Mux VHDL
    import mux
    settings.moduleName = "mux_%i"%(para.number_FIFOs, )
    settings.jsonStr = "{\"number_inputs\" : %i, \"binary_select\" : true}"%(para.number_FIFOs,)
    if mux.generate(settings)[0] != para.addr_width:
        raise ValueError("Mux address width doesn't match comm address width\n")

    # Import Created Mux to VHDL
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName, )

    arch += "\n--Read Muxes\n"
    for opID in range(para.conc_reads):
        # Instantiate mux
        arch += "read_mux_%i : %s\n\t"%(opID, settings.moduleName)
        arch += "generic map (data_width => %i)\n"%(para.data_width, )
        arch += "port map (\n\t"
        for fifo in range(para.number_FIFOs):
            arch += "input_%i => FIFO_%i_buff_out,\n"%(fifo, fifo)
        arch += "input_select => address_%i,\n"%(opID, )
        arch += "data_out  => data_%i\n"%(opID, )
        arch += "\b);\n\b"

    return arch, imports

def genUpdateDemuxes(para, settings, arch, signals, imports):
    # Create Demux VHDL
    import demux
    settings.moduleName = "demux_%i"%(para.number_FIFOs,)
    settings.jsonStr = "{\"number_outputs\" : %i, \"binary_select\" : true}"%(para.number_FIFOs,)
    if demux.generate(settings)[0] != para.addr_width:
        raise ValueError("Demux address width doesn't match comm address width\n")

    # Import Created Demux to VHDL
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    # Generate update_FIFO generation logic
    arch += "\n--Generate update_FIFO signals\n"
    signals += "\n--FIFO Update signals\n"
    for FIFO in range(para.number_FIFOs):
        # Start update_FIFO generation
        arch += "update_FIFO_%i <= "%(FIFO,)
        connect = ""
        for opID in range(para.conc_updates):
            # Declare inturnal signals
            signals += "signal update_FIFO_%i_%i : std_logic;\n"%(FIFO, opID)

            # Generate update_FIFO signal from inturnal ones
            arch += "%supdate_FIFO_%i_%i"%(connect, FIFO, opID)
            connect = " or "
        # End update_FIFO generation
        arch += ";\n"

    # Instantiate Demuxes
    arch += "\n--Demux fifo update\n"
    for opID in range(para.conc_updates):
        arch += "update_demux_%i : %s\n\t"%(opID, settings.moduleName)
        arch += "generic map (data_width => 1)\n"
        arch += "port map (\n\t"
        for fifo in range(para.number_FIFOs):
            arch += "output_%i(0) => update_FIFO_%i_%i,\n"%(fifo, fifo, opID)
        arch += "output_select => address_%i,\n"%(opID, )
        arch += "data_in(0)  => update_%i\n"%(opID, )
        arch += "\b);\n\b"
    return arch, signals, imports

# Root Generate function
def generate(settings):
    # Process passed json parameters
    para = parameters(settings.jsonStr)

    # Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports, para)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    # Support code of generater functions
    sys.path.append(settings.pathRoot + "\\ComComp")
    imports += "\nlibrary work;\n"

    # Generate VHDL
    import copy
    arch, signals, imports = genBuffers(para, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genUpdateDemuxes(para, copy.copy(settings), arch, signals, imports)
    arch, imports = genReadMuxes(para, copy.copy(settings), arch, imports)

    # Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

    # Return calulated addr width
    return para.addr_width

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    # Add Needed paths
    pathRoot = sys.path[0] + "\\..\\.."
    sys.path.append(pathRoot)

    # Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput()
    settings.pathRoot = pathRoot
    generate(settings)
