class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        import math
        #Extract json fields to object fields, checking as goes
        this.empty_value_mode = para.getInt("empty_value_mode", gte = 0, lte = 2)

        this.full_port_enabled  =  para.getBool("full_port_enabled")
        this.empty_port_enabled =  para.getBool("empty_port_enabled")
        this.almost_full_port_enabled  =  para.getBool("almost_full_port_enabled")
        this.almost_empty_port_enabled =  para.getBool("almost_empty_port_enabled")
        this.overflow_protection  =  para.getBool("overflow_protection")
        this.underflow_protection =  para.getBool("underflow_protection")
        this.has_status_ports = this.full_port_enabled  or this.empty_port_enabled or this.almost_full_port_enabled  or this.almost_empty_port_enabled
        this.has_empty = this.empty_port_enabled or this.underflow_protection or not this.use_BRAM or this.empty_value_mode != 3
        this.has_full  = this.full_port_enabled  or this.overflow_protection  or not this.use_BRAM

        this.use_BRAM =  para.getBool("use_BRAM")
        if this.use_BRAM:
            raise NotImplementedError()


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

def jsonBool(bool):
    if bool:
        return "true"
    else:
        return "false"

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
    firstGeneneric = True
    if para.almost_full_port_enabled:
        if firstGeneneric:
            ports += "generic (\n\t"
            firstGeneneric = False
        else:
            ports += ";\n"
        ports += "almost_Full_offset : integer := 0"
    if para.almost_empty_port_enabled:
        if firstGeneneric:
            ports += "generic (\n\t"
            firstGeneneric = False
        else:
            ports += ";\n"
        ports += "almost_empty_offset: integer := 0"
    if para.empty_value_mode == 2:
        if firstGeneneric:
            ports += "generic (\n\t"
            firstGeneneric = False
        else:
            ports += ";\n"
        ports += "empty_value: integer := 0"
    if not para.use_BRAM:
        if firstGeneneric:
            ports += "generic (\n\t"
            firstGeneneric = False
        else:
            ports += ";\n"
        ports += "data_width : integer := 8;\n"
        ports += "data_depth : integer := 64"
        data_width = "data_width - 1"
    else:
        raise NotImplementedError()
    ports += "\n\b);\n"
    ports += "port (\n\t"
    ports += "clock  : in std_logic;\n"
    if para.has_status_ports:
        ports += "\n--Status Ports\n"
    if para.has_full:
        ports += "full  : in std_logic;\n"
    if para.has_empty:
        ports += "empty : in std_logic;\n"
    if para.almost_full_port_enabled:
        ports += "almost_full  : in std_logic;\n"
    if para.almost_empty_port_enabled:
        ports += "almost_empty : in std_logic;\n"

    ports += "\n--Data Ports\n"
    ports += "write_enable: in  std_logic;\n"
    ports += "update_output  : in  std_logic;\n"
    ports += "write_data  : in  std_logic_vector(%s downto 0);\n"%(data_width,)
    ports += "data_out    : out std_logic_vector(%s downto 0) \n"%(data_width,)
    ports += "\b);\n"
    return ports

def genGenerticsChecking(para, arch, imports):
    if not para.use_BRAM:
        #Add asserts for generics requirements
        arch += "assert (data_width > 0)\n\t"
        arch += "report \"data_width must be positive\"\n"
        arch += "severity failure;\n\b\n"

        arch += "assert (data_depth > 0)\n\t"
        arch += "report \"data_depth must be positive\"\n"
        arch += "severity failure;\n\b\n"
    if para.almost_full_port_enabled:
        arch += "assert (almost_Full_offset > 0)\n\t"
        arch += "report \"almost_Full_offset must be positive\"\n"
        arch += "severity failure;\n\b\n"

        if not para.use_BRAM:
            arch += "assert (almost_Full_offset < data_depth)\n\t"
            arch += "report \"almost_Full_offset must be less then data_depth\"\n"
            arch += "severity failure;\n\b\n"
        else:
            raise NotImplementedError();
    if para.almost_empty_port_enabled:
        arch += "assert (almost_empty_offset > 0)\n\t"
        arch += "report \"almost_empty_offset must be positive\"\n"
        arch += "severity failure;\n\b\n"

        if not para.use_BRAM:
            arch += "assert (almost_empty_offset < data_depth)\n\t"
            arch += "report \"almost_empty_offset must be less then data_depth\"\n"
            arch += "severity failure;\n\b\n"
        else:
            raise NotImplementedError();
    if para.empty_value_mode == 2:
        arch += "assert (empty_value > 0)\n\t"
        arch += "report \"empty_value must be positive\"\n"
        arch += "severity failure;\n\b\n"

        if not para.use_BRAM:
            imports += "use ieee.numeric_std.all;\n\n"
            arch += "assert (empty_value < 2 ** data_width)\n\t"
            arch += "report \"empty_value to large to fill in data_width bits\"\n"
            arch += "severity failure;\n\b\n"
        else:
            raise NotImplementedError();
    return arch, imports

def genInternalSignals(para, arch, signals):
    if not para.use_BRAM:
        data_width = "data_width - 1"
    else:
        raise NotImplementedError();
    signals += "--Internal Signals\n"
    signals += "signal head_value : std_logic_vector(%s downto 0);\n"%(data_width,)
    signals += "signal accecpted_update : std_logic;\n"
    signals += "signal accecpted_write  : std_logic;\n"
    if para.has_status_ports:
        arch += "--Connect up status ports\n"
    if para.full_port_enabled:
        signals += "signal internal_full  : in std_logic := '0';\n"
        arch += "full  <= internal_full;\n"
    if para.empty_port_enabled:
        signals += "signal internal_empty : in std_logic := '1';\n"
        arch += "empty <= internal_empty;\n"
    if para.almost_full_port_enabled:
        signals += "signal internal_almost_full  : in std_logic := '0';\n"
        arch += "almost_full  <= internal_almost_full;\n"
    if para.almost_empty_port_enabled:
        signals += "signal internal_almost_empty : in std_logic := '1';\n"
        arch += "almost_empty <= internal_almost_empty;\n"
    return arch, signals

def genOverFlowProtection(para, arch):
    arch += "\n--Handle write enable signal\n"
    if para.overflow_protection:
        arch += "accecpted_write <= write_enable;\n"
    else:
        arch += "accecpted_write <= '1' when internal_full = '0' and write_enable = '1' else '0';\n"
    return arch

def genUnderFlowProtection(para, arch):
    arch += "\n--Handle update_output signal\n"
    if para.overflow_protection:
        arch += "accecpted_update <= update_output;\n"
    else:
        arch += "accecpted_update <= '1' when internal_empty = '0' and update_output = '1' else '0';\n"
    return arch

def genBuffer(para, settings, arch, signals, imports):
    #Create Register VHDL
    import register
    settings.moduleName += "_buf"
    settings.jsonStr  = "{"
    settings.jsonStr += "\"has_reset\" : %s,"%(jsonBool(para.empty_value_mode == 0),)
    settings.jsonStr += "\"has_preset\": %s,"%(jsonBool(para.empty_value_mode == 1),)
    settings.jsonStr += "\"write_mode\": 2,"
    settings.jsonStr += "\"read_mode\" : 0"
    settings.jsonStr += "}"
    register.generate(settings)

    #Import buffer VHDL into fifo
    imports += "\nlibrary work\n"
    imports += "use work.%s_pkg.all;\n"%(settings.moduleName,)

    #Add buffer to arch
    if not para.use_BRAM:
        data_width = "data_width - 1"
    else:
        data_width = "%i"%(para.data_width - 1)
    arch += "\n--Output buffer\n"
    arch += "buf: %s\n\t"%(settings.moduleName,)
    arch += "generic map ( data_width => %s)\n"%(data_width,)
    arch += "port map (\n\t"
    if para.empty_value_mode == 0:
        arch += "reset => buf_in;\n"
    elif para.empty_value_mode == 1:
        arch += "preset => internal_empty;\n"
    if para.empty_value_mode == 2:
        signals += "signal buf_in : std_logic_vector(%s downto 0);\n"%(data_width,)
        arch += "data_in => buf_in;\n"
    else:
        arch += "data_in => head_value;\n"
    arch += "write_enable => clock\n"
    arch += "\b)\n\b"

    #Add generic empty value insertion
    if para.empty_value_mode == 2:
        arch += "--Insert generic empty value when fifo is empty\n"
        arch += "buf_in => std_logic_vector(to_unsigned(empty_value, buf_in'length)) when internal_empty = '1' else head_value;\n"
    return arch, signals, imports

def genNonHardwareData(para, arch, signals):
    #Add SRL signals
    signals += "\n--SRL signals\n"
    signals += "type SRL is array (data_depth - 1 downto 0) of std_logic_vector (data_width - 1 downto 0);\n"
    signals += "signal SRL_data : SRL;"
    signals += "signal SRL_head : integer range 0 to data_depth - 1 := 0;\n"

    #Add write behavour
    arch += "\n--Handle writing data to fifo\n"
    arch += "process(clock)\n"
    arch += "begin\n\t"
    arch += "if clock'event and clock '1' and accecpted_write = '1' then\n\t"
    arch += "SRL_data <= SRL_data(SRL_data'left - 1 downto 0) & write_data;\n"
    arch += "\bend if;"
    arch += "\bend process;"

    #Add head outputing behavour
    arch += "\n--Output head to buffer\n"
    arch += "head_value => SRL_data(SRL_head)\n"

    #Handle SRL_head updating
    arch += "\n--Update SRL_head\n"
    arch += "process(clock)\n"
    arch += "begin\n\t"
    arch += "if clock'event and clock '1' then\n\t"
    arch += "if accecpted_write '1' and accecpted_update = '0' then\n\t"
    arch += "if internal_empty = '1' then\n\t"
    arch += "internal_empty => '0'\n"
    arch += "\belse\n\t"
    arch += "SRL_head <= SRL_head + 1;\n"
    arch += "\bend if;\n"
    arch += "\belsif accecpted_write '0' and accecpted_update = '1' then\n\t"
    arch += "if internal_full = '1' then\n\t"
    arch += "internal_full => '0'\n"
    arch += "\belse\n\t"
    arch += "SRL_head <= SRL_head - 1;\n"
    arch += "\bend if;\n"
    arch += "\bend if;\n"
    arch += "\bend if;\n"
    arch += "\bend process;\n"

    #Handle inturnal state updating
    if para.almost_full_port_enabled or para.almost_empty_port_enabled:
        arch += "\n--Update internal status signals\n"
    if para.almost_full_port_enabled:
        signals += "signal internal_almost_full  : in std_logic;\n"
        arch += "internal_almost_full  <= '1' when SRL_head + almost_Full_offset <= data_depth - 1  else '0';\n"
    if para.almost_empty_port_enabled:
        signals += "signal internal_almost_empty : in std_logic;\n"
        arch += "internal_almost_empty <= '1' when SRL_head - almost_Full_offset <= 0  else '0';\n"

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
    arch, signals = genInternalSignals  (para, arch, signals)
    arch = genOverFlowProtection (para, arch)
    arch = genUnderFlowProtection(para, arch)
    arch, signals, imports = genBuffer(para, copy.copy(settings), arch, signals, imports)
    if not para.use_BRAM:
        arch, signals = genNonHardwareData(para, arch, signals)
    else:
        raise NotImplementedError()

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
