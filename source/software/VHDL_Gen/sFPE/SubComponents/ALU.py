class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        # Extract widths
        this.a_width   = para.getInt("a_width"  , gte = 0, lte = 30)
        this.b_width   = para.getInt("b_width"  , gte = 0, lte = 18)
        this.c_width   = para.getInt("c_width"  , gte = 0, lte = 48)
        this.d_width   = para.getInt("d_width"  , gte = 0, lte = 25)
        this.res_width = para.getInt("res_width", gt  = 0, lte = 48)

        # Check there is data input
        if sum([this.a_width, this.b_width, this.c_width, this.d_width ]) == 0:
            raise ValueError("All data inputs to ALU have widths of 0\n")

        # Read in required statuses
        import warnings
        this.required_statuses = []
        for status in para.getArray("required_statuses"):
            if status in ["equal", "less"]:
                this.required_statuses.append(status)
            else:
                # Warn about unknown statuses
                warnings.warn("Unknown status, \"%s\", encounted in ALU\n"%(status, ))

        # Read in active control ports
        this.used_controls = {}
        for control, value in para.getJSON("controls").items():
            if control in ["carry_in_sel", "carry_in", "ALU_mode", "op_mode", "in_mode"]:
                this.used_controls[control] = value
            else:
                warnings.warn("Unknown control, \"%s\", encounted in ALU\n"%(control, ))

##################################################################################0

def genPackage(package, moduleName, ports):
    package += "--Include packages used in package declaration\n"
    package += "library ieee;\n"
    package += "use ieee.std_logic_1164.all;\n\n"
    package += "library UNISIM;\n"
    package += "use UNISIM.vcomponents.all;\n\n"
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

    imports += "Library UNISIM;\n"
    imports += "use UNISIM.vcomponents.all;\n"
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

def VHDLBool(bool):
    if bool: return "TRUE"
    else: return "FALSE"

def genPorts(ports, para):
    ports += "port (\n\t"

    # Handle data input ports
    ports += "--Data input data ports\n"
    for port in ["a", "b", "c", "d"]:
        if getattr(para, "%s_width"%(port, )) != 0:
            ports += "%s : in std_logic_vector(%i downto 0);\n"%(port,  getattr(para, "%s_width"%(port, )) - 1)

    ports += "\n--Data output port\n"
    # Handle result output port
    ports += "res : out std_logic_vector(%i downto 0);\n"%(para.res_width, )

    # Handle status output ports
    for status in para.required_statuses:
        ports += "status_%s : out std_logic;\n"%(status, )

    # Handle Control ports
    ports_d1 = ""
    control_widths = { "carry_in_sel" : 3, "carry_in" : 1, "ALU_mode" : 4, "op_mode" : 7, "in_mode" : 5 }
    for control in para.used_controls:
        # Select other the controls using ports
        if para.used_controls[control] == None:
            ports_d1 += "control_%s : in std_logic_vector(%i downto 0);\n"%(control, control_widths[control] - 1)
    if ports_d1:
        ports += "\n--Control ports\n"
        ports += ports_d1
        ports += "\n"

    ports += "clock : in std_logic;\n"
    ports += "reset : in std_logic\n"

    ports += "\b);\n"
    return ports

def genDSPSilce(para, arch, signals):
    arch += "--DSP Slice\n"
    arch += "DSP48E1_inst : DSP48E1\n\t"

    # Configure DSP to handle the instrSet
    arch += "generic map (\n\t"

    # Setup Data pipeline through DSP slice
    arch += "--Don't buffer output to give 2 clock cycle pipeline through DSP slice\n"
    arch += "PREG => 0,\n"

    if "equal" in para.required_statuses:
        # Configuration pattern match to check for zero
        arch += "\n--Setup pattern to check of zero result\n"
        arch += "USE_PATTERN_DETECT => \"PATDET\",\n"

    # Setup the multipler and preadder
    # As no mnemonics for multipling are supported yet
    # so set preadder and multipler not to be used
    arch += "\n--Disable preadder and multipler\n"
    arch += "USE_MULT => \"NONE\"\n"

    arch += "\b)\n"

    ####################################################################

    # Connect up the DSP to handle the instrSet
    arch += "port map (\n\t"
    arch += "clk => clock,\n"

    # Connect up data inputs
    arch += "\n--Set up Data Inputs ports\n"
    for port in set(["a", "b"]):
        width = getattr(para, "%s_width"%(port, ))
        if width:
            arch += "%s => %s,\n"%(port.upper(), port)
            arch += "CE%s1 => clock,\n"%(port.upper(), )
            arch += "CE%s2 => clock,\n"%(port.upper(), )
            arch += "RST%s => reset,\n"%(port.upper(), )
        else:
            arch += "%s => (others => '1'),\n"%(port.upper(), )
            arch += "CE%s1 => '0',\n"%(port.upper(), )
            arch += "CE%s2 => '0',\n"%(port.upper(), )
            arch += "RST%s => '0',\n"%(port.upper(), )
    for port in set(["c", "d"]):
        width = getattr(para, "%s_width"%(port, ))
        if width:
            arch += "%s => %s,\n"%(port.upper(), port)
            arch += "CE%s  => clock,\n"%(port.upper(), )
            arch += "RST%s => reset,\n"%(port.upper(), )
        else:
            arch += "%s => (others => '1'),\n"%(port.upper(), )
            arch += "CE%s  => '0',\n"%(port.upper(), )
            arch += "RST%s => '0',\n"%(port.upper(), )

    # Connect up output port
    arch += "\n--Set up Result Output ports\n"
    signals += "signal res_data : std_logic_vector(%i downto 0);\n"%(para.res_width - 1, )
    arch += "P(%i downto 0) => res_data,\n"%(para.res_width - 1, )
    if para.res_width != 48:
        arch += "P(47 downto %i) => open,\n"%(para.res_width, )
    arch += "CEP  => '0',\n"
    arch += "RSTP => '0',\n"

    # Connect up control ports
    arch += "\n--Set up Control ports\n"
    control_widths = { "ALU_mode" : 4, "in_mode" : 5 }

    # in_mode port
    if "in_mode" in para.used_controls:
        # Check if connected to a port
        if para.used_controls["in_mode"] == None:
            arch += "INMODE => control_in_mode,\n"
        else:
            arch += "INMODE => std_logic_vector(to_unsigned(%i, 4)),\n"%(para.used_controls["in_mode"], )
        arch += "CEINMODE => clock,\n"
        arch += "RSTINMODE => reset,\n"
    else:
        arch += "INMODE => (others => '1'),\n"
        arch += "CEINMODE  => '0',\n"
        arch += "RSTINMODE => '0',\n"

    # ALU_mode port
    if "ALU_mode" in para.used_controls:
        # Check if connected to a port
        if para.used_controls["ALU_mode"] == None:
            arch += "ALUMODE => control_ALU_mode,\n"
        else:
            arch += "ALUMODE => std_logic_vector(to_unsigned(%i, 4)),\n"%(para.used_controls["ALU_mode"], )
        arch += "CEALUMODE  => clock,\n"
        arch += "RSTALUMODE => reset,\n"
    else:
        arch += "ALUMODE => (others => '1'),\n"
        arch += "CEALUMODE  => '0',\n"
        arch += "RSTALUMODE => '0',\n"

    # Carry_in port
    if "carry_in" in para.used_controls:
        # Check if connected to a port
        if para.used_controls["carry_in"] == None:
            arch += "CARRYIN => control_carry_in,\n"
        else:
            arch += "CARRYIN => '%i',\n"%(para.used_controls["carry_in"], )
        arch += "CECARRYIN => clock,\n"
        arch += "RSTALLCARRYIN => reset,\n"
    else:
        arch += "CARRYIN => (others => '1'),\n"
        arch += "CECARRYIN => '0',\n"
        arch += "RSTALLCARRYIN => '0',\n"

    # carry_in_sel port
    if "carry_in_sel" in para.used_controls:
        # Check if connected to a port
        if para.used_controls["carry_in_sel"] == None:
            arch += "CARRYINSEL => control_carry_in_sel,\n"
        else:
            arch += "CARRYINSEL => std_logic_vector(to_unsigned(%i, 4)),\n"%(para.used_controls["carry_in_sel"], )
    # op_mode port
    if "op_mode" in para.used_controls:
        # Check if connected to a port
        if para.used_controls["op_mode"] == None:
            arch += "OPMODE => control_op_mode,\n"
        else:
            arch += "OPMODE => std_logic_vector(to_unsigned(%i, 7)),\n"%(para.used_controls["op_mode"], )
    # setup carry_in_sel's and op_mode's shared CE and RST ports
    if "carry_in_sel" in para.used_controls or "op_mode" in para.used_controls:
        arch += "CECTRL  => clock,\n"
        arch += "RSTCTRL => reset,\n"
    else:
        arch += "CECTRL  => '0',\n"
        arch += "RSTCTRL => '0',\n"

    # Handle pattern match outputs
    if "equal" in para.required_statuses:
        arch += "PATTERNDETECT  => status_equal,\n"
    else:
        arch += "PATTERNDETECT => open,\n"
    arch += "PATTERNBDETECT => open,\n"

    # Disable preadder and multiple ports
    arch += "\n--Disable Preadder and multiple ports\n"
    arch += "CEM  => '0',\n"
    arch += "CEAD => '0',\n"
    arch += "RSTM => '0',\n"
    arch += "MULTSIGNIN  => '1',\n"
    arch += "MULTSIGNOUT => open,\n"

    # Disable carryout, underflow, and underflow ports
    arch += "\n--carryout, underflow, and underflow ports\n"
    arch += "CARRYOUT   => open,\n"
    arch += "OVERFLOW   => open,\n"
    arch += "UNDERFLOW  => open,\n"

    # Disable cascade ports
    arch += "ACIN  => (others => '1'),\n"
    arch += "BCIN  => (others => '1'),\n"
    arch += "PCIN  => (others => '1'),\n"
    arch += "CARRYCASCIN => '1',\n"
    arch += "ACOUT  => open,\n"
    arch += "BCOUT  => open,\n"
    arch += "PCOUT  => open,\n"
    arch += "CARRYCASCOUT  => open\n"

    arch += "\b);\n"

    arch += "\n--Connect DSP to res port\n"
    arch += "res <= res_data;\n"

    if "less" in para.required_statuses:
        arch += "\n--Handle equals status"
        arch += "status_less <= res_data(%i)"%(para.res_width - 1, )
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
    arch, signals = genDSPSilce(para, arch, signals)

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
