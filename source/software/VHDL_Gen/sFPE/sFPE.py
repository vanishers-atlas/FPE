class readParaJson:
    def __init__(this, jsonStr):
        # Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        # Instruction Decoder Parameters
        this.op_code_width = para.getInt("op_code_width", gt = 0)

        # Program Memory parameters
        this.PM_depth    = para.getInt("PM_depth", gt = 0)
        this.PM_values   = para.getString("IMM_values")
        this.PM_use_BROM = para.getBool("IMM_use_BROM")

        # Program Counter parameters
        this.PC_wrap_value = para.getInt("PC_wrap_value", gt = 0)
        this.PC_width      = para.getInt("PC_width", gt = 0)

        # Immediate Value ROM parameters
        this.IMM_depth    = para.getInt("IMM_depth", gte = 0)
        if this.IMM_depth: this.IMM_width = para.getInt("IMM_width", gt = 0)
        this.IMM_values   = para.getString("IMM_values")
        this.IMM_use_BROM = para.getBool("IMM_use_BROM")

        # Comm Get parameters
        this.CG_channels = para.getInt("CG_channels", gt = 0)
        this.CG_width    = para.getInt("CG_width"   , gt = 0, lte = 48)

        # Comm Put parameters
        this.CP_channels = para.getInt("CP_channels", gt = 0)
        this.CP_width    = para.getInt("CP_width"   , gt = 0)

        # Register File parameters
        this.REG_depth = para.getInt("REG_depth" , gte = 0)
        if this.REG_depth: this.REG_width = para.getInt("REG_width", gt = 0)

        # Data RAM parameters
        this.MEM_depth    = para.getInt("MEM_depth", gte = 0)
        if this.MEM_depth: this.MEM_width = para.getInt("MEM_width", gt = 0)
        this.MEM_use_BRAM = para.getBool("MEM_use_BRAM")

        # ALU parameters
        this.ALU_a_width   = para.getInt("a_width"  , gte = 0)
        this.ALU_b_width   = para.getInt("b_width"  , gte = 0)
        this.ALU_c_width   = para.getInt("c_width"  , gte = 0)
        this.ALU_d_width   = para.getInt("d_width"  , gte = 0)
        this.ALU_res_width = para.getInt("res_width", gt  = 0)
        this.res_width = this.ALU_res_width

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
    if bool: return "true"
    else: return "false"

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

    # Add Comm Get Port
    ports += "--Comm Get Data Ports\n"
    ports_d1 = "\n--Comm Get Update Ports\n"
    for channel in range(para.CG_channels):
        ports += "CG_channel_%i : in std_logic_vector(%i downto 0);\n"%(channel, para.CG_width - 1)
        ports_d1 += "CG_channel_update_%i : out std_logic;\n"%(channel, )
    ports += ports_d1

    # Add Comm Put Port
    ports += "\n--Comm Put Data Ports\n"
    ports_d1 = "\n--Comm Put Write Ports\n"
    for channel in range(para.CP_channels):
        ports += "CP_channel_%i : out std_logic_vector(%i downto 0);\n"%(channel, para.CP_width - 1)
        ports_d1 += "CP_channel_write_%i : out std_logic;\n"%(channel, )
    ports += ports_d1

    # Generate General Ports
    ports += "\n--General Ports\n"
    ports += "clock : in std_logic;\n"
    ports += "reset : in std_logic\n"
    ports += "\b);\n"
    return ports

def genDelayVHDL(para, settings, imports):
    #Create Delay VHDL
    import delay
    settings.moduleName += "_delay"
    settings.jsonStr  = "{"
    settings.jsonStr += "\"has_data_enable\"  : false,"
    settings.jsonStr += "\"has_reset\" : true"
    settings.jsonStr += "}"
    delay.generate(settings)

    #Import Created delay to VHDL
    imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

    return imports

##################################################################################
##                   MEMORY GEN FUNCTIONS
##################################################################################

def genCommGet(para, instr, settings, arch, signals, imports):
    if "GET" in instr.mems:
        # Check read only
        if "res" in instr.accesses["GET"]:
            raise AssertionError("Comm Get can't be accessed by res addr\n")

        # Check can update FIFOs
        if not instr.mem_mods["GET"]["update"]:
            raise AssertionError("Comm Get can't exist without at least one update signal\n")

        arch += "--###########################################################\n"
        arch += "--##                        Comm Get                       ##\n"
        arch += "--###########################################################\n"

        # Generate Comm get subunit
        import copy
        subsetting = copy.copy(settings)
        subsetting.moduleName += "_comm_get"
        subsetting.jsonStr  = "{"
        subsetting.jsonStr += "\"conc_reads\"  : %i,"%(len(instr.accesses["GET"]), )
        subsetting.jsonStr += "\"data_width\"  : %i,"%(para.CG_width, )
        subsetting.jsonStr += "\"conc_updates\": %i,"%(len(instr.mem_mods["GET"]["update"]), )
        subsetting.jsonStr += "\"number_FIFOs\": %i" %(para.CG_channels, )
        subsetting.jsonStr += "}"
        import comm_get
        para.GET_addr_width = comm_get.generate(subsetting)

        # import subunit vhdl
        imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

        # Instantiate Comm get in sFPE
        arch += "\ncomm_get: %s\n\t"%(subsetting.moduleName,)
        arch += "port map (\n\t"

        # Connect up FIFO ports
        arch += "--FIFO Ports\n"
        arch_d1 = ""
        for cnannel in range(para.CG_channels):
            arch += "FIFO_%i => CG_channel_%i,\n"%(cnannel, cnannel)
            arch_d1 += "update_FIFO_%i => CG_channel_update_%i,\n"%(cnannel, cnannel)
        arch += arch_d1

        # Connect up sFPE ports
        arch += "\n--sFPE Ports\n"
        arch_d1 = arch_d2 = ""
        readID = 0

        # Start with read ops with updates
        for addr in instr.mem_mods["GET"]["update"]:
            arch += "address_%i => %s_addr_buff_out(%i downto 0),\n"%(readID, addr, para.GET_addr_width - 1)
            arch_d1 += "data_%i => %s_GET_buff_in,\n"%(readID, addr)
            arch_d2 += "update_%i => GET_update_buff_%s_out,\n"%(readID, addr)
            readID += 1

        # Add read ops without an update
        for addr in (instr.accesses["GET"] - instr.mem_mods["GET"]["update"]):
            arch += "address_%i => %s_addr_buff_out(%i downto 0),\n"%(readID, addr, para.GET_addr_width - 1)
            arch_d1 += "data_%i => %s_GET_buff_in,\n"%(readID, addr)
            readID += 1
        arch += arch_d1 + arch_d2

        arch += "\nclock => clock\n"
        arch +="\b);\n\b"

        # Generate comm get output buffers
        signals += "--Comm Get -> Data Select signals\n"
        signals_d1 = ""
        for addr in instr.accesses["GET"]:
                # Declare com get to Data Select signals
            signals += "signal %s_GET_buff_in  : std_logic_vector(%i downto 0);\n"%(addr, para.CG_width - 1)
            signals_d1 += "signal %s_GET_buff_out : std_logic_vector(%i downto 0);\n"%(addr, para.CG_width - 1)

            # Instantiate com get to Data Select bufffers
            arch += "\n%s_GET_buff : %s\n\t"%(addr, settings.moduleName + "_delay",)
            arch += "generic map (\n\t"
            arch += "default_value => 0,\n"
            arch += "data_width => %i,\n"%(para.CG_width, )
            arch += "data_depth => 1\n"
            arch += "\b)\n"
            arch += "port map(\n\t"
            arch += "clock => clock,\n"
            arch += "reset => reset,\n"
            arch += "data_in  => %s_GET_buff_in,\n"%(addr, )
            arch += "data_out => %s_GET_buff_out\n"%(addr, )
            arch += "\b);\n\b"
        signals += signals_d1

    return arch, signals, imports

def genImmROM (para, instr, settings, arch, signals, imports):
    if "IMM" in instr.mems:
        # Check read only
        if "res" in instr.accesses["IMM"]:
            raise AssertionError("res addr can't access IMM ROM\n")

        arch += "\n--###########################################################\n"
        arch += "--##                         Imm ROM                       ##\n"
        arch += "--###########################################################\n"

        # Create IMM ROM vhdl
        import copy
        subsetting = copy.copy(settings)
        subsetting.moduleName += "_IMM"
        subsetting.jsonStr  = "{"
        subsetting.jsonStr += "\"data_values\": \"%s\","%(para.IMM_values, )
        subsetting.jsonStr += "\"use_BROM\": %s,"%(jsonBool(para.IMM_use_BROM), )
        subsetting.jsonStr += "\"conc_reads\": %s,"%(len(instr.accesses["IMM"]), )
        subsetting.jsonStr += "\"data_width\": %i,"%(para.IMM_width, )
        subsetting.jsonStr += "\"depth\": %i"%(para.IMM_depth, )
        subsetting.jsonStr += "}"
        import ROM
        para.IMM_addr_width = ROM.generate(subsetting)

        # Import Created VHDL
        imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

        # Instantiate IMM ROM
        arch += "\nIMM_ROM: %s\n\t"%(subsetting.moduleName,)
        arch += "port map (\n\t"
        readID = 0; comma = arch_d1 = ""
        for addr in instr.accesses["IMM"]:
            arch += "addr_%i => %s_addr_buff_out(%i downto 0),\n"%(readID, addr,  para.IMM_addr_width - 1)
            arch_d1 += "%sdata_%i => %s_IMM_buff_in"%(comma, readID, addr)
            readID += 1; comma = ",\n"
        arch += arch_d1
        arch +="\n\b);\n\b"

        # Generate IMM ROM output buffers
        signals += "\n--Imm Mem -> Data Select signals\n"
        signals_d1 = ""
        for addr in instr.accesses["IMM"]:
            # Declare Imm Mem to Data Select signals
            signals += "signal %s_IMM_buff_in  : std_logic_vector(%i downto 0);\n"%(addr, para.IMM_width - 1)
            signals_d1 += "signal %s_IMM_buff_out : std_logic_vector(%i downto 0);\n"%(addr, para.IMM_width - 1)

            # Instantiate Imm Mem to Data Select bufffers
            arch += "\n%s_IMM_buff : %s\n\t"%(addr, settings.moduleName + "_delay",)
            arch += "generic map (\n\t"
            arch += "default_value => 0,\n"
            arch += "data_width => %i,\n"%(para.IMM_width, )
            arch += "data_depth => 1\n"
            arch += "\b)\n"
            arch += "port map(\n\t"
            arch += "clock => clock,\n"
            arch += "reset => reset,\n"
            arch += "data_in  => %s_IMM_buff_in,\n"%(addr, )
            arch += "data_out => %s_IMM_buff_out\n"%(addr, )
            arch += "\b);\n\b"
        signals += signals_d1
    return arch, signals, imports

def genRegFile(para, instr, settings, arch, signals, imports):
    if "REG" in instr.mems:
        # Check can write to
        if not "res" in instr.accesses["REG"]:
            raise AssertionError("Reg FIle can't be used without writing to it\n")

        arch += "\n--###########################################################\n"
        arch += "--##                        Reg File                       ##\n"
        arch += "--###########################################################\n"

        # Generate Reg File subunit
        import copy
        subsetting = copy.copy(settings)
        subsetting.moduleName += "_reg_file"
        subsetting.jsonStr  = "{"
        subsetting.jsonStr += "\"conc_reads\": %i,"%(len(instr.accesses["REG"]- set(["res"])), )
        subsetting.jsonStr += "\"number_reg\": %i,"%(para.REG_depth, )
        subsetting.jsonStr += "\"data_width\": %i"%(para.REG_width, )
        subsetting.jsonStr += "}"
        import reg_file
        para.REG_addr_width = reg_file.generate(subsetting)

        # import Reg File subunit
        imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

        # Instantiate Reg File
        arch += "\n--Reg File\n"
        arch += "Reg_File: %s\n\t"%(subsetting.moduleName,)
        arch += "port map (\n\t"

        # Connect up read ports
        readID = 0; arch_d1 = ""
        for addr in (instr.accesses["REG"] - set(["res"])):
            arch += "read_addr_%i => %s_addr_buff_out(%i downto 0),\n"%(readID, addr, para.REG_addr_width - 1)
            arch_d1 += "read_data_%i => %s_REG_buff_in,\n"%(readID, addr)
            readID += 1
        arch += arch_d1

        # Connect up write addrs
        arch += "write_addr => res_addr_buff_out(%i downto 0),\n"%(para.REG_addr_width - 1, )
        if para.REG_width <= para.res_width:
            # Drop extra data
            arch += "write_data => result_buff_out(%i downto 0),\n"%(para.REG_width - 1, )
        else:
            # Zero out unwritable bits
            arch += "write_data => (%i downto 0 <= result_buff_out, others <= '0')\n"%(para.res_width - 1, )
            # Warn about having unwritable bits
            import warnings
            warnings.warn("Reg File width is less than result width, can't write full reg file width\n")
        arch += "write_enable => res_sel_buff_REG_out\n"
        arch +="\b);\n\b"

        # Generate output buffers
        signals += "\n--Reg File -> Data Select signals\n"
        signals_d1 = ""
        for addr in (instr.accesses["REG"] - set(["res"])):
            # Declare Buffer signals
            signals += "signal %s_REG_buff_in  : std_logic_vector(%i downto 0);\n"%(addr,para.REG_width - 1)
            signals_d1 += "signal %s_REG_buff_out : std_logic_vector(%i downto 0);\n"%(addr,para.REG_width - 1)

            # Instantiate buffers
            arch += "\n%s_REG_buff : %s\n\t"%(addr, settings.moduleName + "_delay",)
            arch += "generic map (\n\t"
            arch += "default_value => 0,\n"
            arch += "data_width => %i,\n"%(para.REG_width, )
            arch += "data_depth => 1\n"
            arch += "\b)\n"
            arch += "port map(\n\t"
            arch += "clock => clock,\n"
            arch += "reset => reset,\n"
            arch += "data_in  => %s_REG_buff_in,\n"%(addr, )
            arch += "data_out => %s_REG_buff_out\n"%(addr, )
            arch += "\b);\n\b"

        signals += signals_d1
    return arch, signals, imports

def genDataMem(para, instr, settings, arch, signals, imports):
    if "MEM" in instr.mems:
        # Check can write to
        if not "res" in instr.accesses["MEM"]:
            raise AssertionError("Data Mem can't be used without writing to it\n")

        arch += "\n--###########################################################\n"
        arch += "--##                        Data Mem                       ##\n"
        arch += "--###########################################################\n"

        # Generate Data Mem subunit
        import copy
        subsetting = copy.copy(settings)
        subsetting.moduleName += "_data_mem"
        subsetting.jsonStr  = "{"
        subsetting.jsonStr += "\"use_BRAM\": %s,"%(jsonBool(para.MEM_use_BRAM), )
        subsetting.jsonStr += "\"conc_reads\": %s,"%(len(instr.accesses["MEM"] - set(["res"])), )
        subsetting.jsonStr += "\"data_width\": %i,"%(para.REG_width, )
        subsetting.jsonStr += "\"depth\": %i,"%(para.MEM_depth, )
        subsetting.jsonStr += "\"write_mode\" : \"edge\""
        subsetting.jsonStr += "}"
        import RAM
        para.MEM_addr_width = RAM.generate(subsetting)

        # import Data Mem subunit
        imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

        # Instantiate Data Mem subunit
        arch += "\nData_Mem: %s\n\t"%(subsetting.moduleName, )
        arch += "port map (\n\t"

        # Connect up read addrs
        readID = 0; arch_d1 = ""
        for addr in (instr.accesses["MEM"]  - set(["res"])):
            arch += "read_addr_%i => %s_addr_buff_out(%i downto 0),\n"%(readID, addr, para.MEM_addr_width - 1)
            arch_d1 += "read_data_%i => %s_MEM_buff_in,\n"%(readID, addr)
            readID += 1
        arch += arch_d1

        # Connect up write addrs
        arch += "write_addr => res_addr_buff_out(%i downto 0),\n"%(para.REG_addr_width - 1, )

        if para.MEM_width <= para.res_width:
            # Drop extra data
            arch += "write_data => result_buff_out(%i downto 0),\n"%(para.MEM_width - 1, )
        else:
            # Tie unused imputs to 0
            arch += "write_data => (%i downto 0 <= result_buff_out, others <= '0'),\n"%(para.res_width - 1, )
            # Warn about having unwritable bits
            import warnings
            warnings.warn("Data Mem's width is less than result width, can't write full data mem width\n")
        arch += "write_enable => res_sel_buff_MEM_out\n"
        arch +="\b);\n\b"

        # Generate output buffers
        signals += "\n--Data Mem -> Data Select signals\n"
        signals_d1 = ""
        for addr in (instr.accesses["MEM"] - set(["res"])):
            # Declare Buffer signals
            signals += "signal %s_MEM_buff_in  : std_logic_vector(%i downto 0);\n"%(addr, para.MEM_width - 1)
            signals_d1 += "signal %s_MEM_buff_out : std_logic_vector(%i downto 0);\n"%(addr, para.MEM_width - 1)

            # Instantiate buffers
            arch += "\n%s_MEM_buff : %s\n\t"%(addr, settings.moduleName + "_delay",)
            arch += "generic map (\n\t"
            arch += "default_value => 0,\n"
            arch += "data_width => %i,\n"%(para.MEM_width, )
            arch += "data_depth => 1\n"
            arch += "\b)\n"
            arch += "port map(\n\t"
            arch += "clock => clock,\n"
            arch += "reset => reset,\n"
            arch += "data_in  => %s_MEM_buff_in,\n"%(addr, )
            arch += "data_out => %s_MEM_buff_out\n"%(addr, )
            arch += "\b);\n\b"

        signals += signals_d1
    return arch, signals, imports

def genCommPut(para, instr, settings, arch, signals, imports):
    if "PUT" in instr.mems:
        # Check can only write to
        if instr.accesses["PUT"] ^ set(["res"]):
            raise AssertionError("Comm Put can only be accessed by result address\n")

        arch += "\n--###########################################################\n"
        arch += "--##                        Comm Put                       ##\n"
        arch += "--###########################################################\n"

        # Generate Comm Put subunit
        settings.moduleName += "_comm_put"
        settings.jsonStr  = "{"
        settings.jsonStr += "\"data_width\"  : %i,"%(para.CP_width, )
        settings.jsonStr += "\"number_FIFOs\": %i" %(para.CP_channels, )
        settings.jsonStr += "}"
        import comm_put
        para.PUT_addr_width = comm_put.generate(settings)

        # import Comm Put subunit
        imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

        # Instantiate Comm Put subunit
        arch += "\ncomm_put: %s\n\t"%(settings.moduleName,)
        arch += "port map (\n\t"

        arch += "--FIFO Ports\n"
        arch_d1 = ""
        for channal in range(para.CP_channels):
            arch += "FIFO_%i => CP_channel_%i,\n"%(channal, channal)
            arch_d1 += "update_FIFO_%i => CP_channel_write_%i,\n"%(channal, channal)

        arch += "\n--sFPE Ports\n"
        arch += "address => res_addr_buff_out(%i downto 0),\n"%(para.PUT_addr_width - 1,)
        arch += "enable => res_sel_buff_PUT_out,\n"
        if para.CP_width <= para.res_width:
            arch += "data => result_buff_out(%i downto 0),\n"%(para.CP_width - 1, )
        else:
            arch += "data => (%i downto 0 <= result_buff_out, others <= '0'),\n"%(para.res_width - 1, )
            # Warn about having unwritable bits
            import warnings
            warnings.warn("Comm Put's width is less than result width, can't write full comm put width\n")

        arch += "\nclock => clock\n"
        arch +="\b);\n\b"

    return arch, signals, imports

##################################################################################
##                   Instr Decoder GEN FUNCTIONS
##################################################################################

def genInstrDecoder(para, instr, settings, arch, signals, imports):
    arch += "--###########################################################\n"
    arch += "--##                       Instr Decode                    ##\n"
    arch += "--###########################################################\n"

    # Generate instr decoder subUnit
    import copy
    subsetting = copy.copy(settings)
    subsetting.moduleName += "_instr_decoder"
    subsetting.jsonStr  = "{"
    subsetting.jsonStr += "\"op_code_width\" : %i,"%(para.op_code_width, )
    subsetting.jsonStr += "\"addr_widths\" : {"
    comma = ""
    for addr in instr.addrs:
        # Caluate each addr addr width
        access_widths = set()
        for mem in  instr.accesses[addr]:
            access_widths.add(getattr(para, "%s_addr_width"%(mem, )))
        setattr(para, "%s_addr_width"%(addr, ), max(access_widths))

        subsetting.jsonStr += "%s\"%s\" : %i"%(comma, addr, getattr(para, "%s_addr_width"%(addr, )))
        comma =", "
    subsetting.jsonStr += "}"
    subsetting.jsonStr += "}"
    import instr_decoder
    para.instr_width, para.mem_controls, para.data_selects, para.used_ALU_controls, para.status_reg, para.jumps = instr_decoder.generate(subsetting)

    # import instr decoder subUnit
    imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

    # Instantiate instr decoder to arch
    arch += "\n--Instruction Decoder\n"
    arch += "ID: %s\n\t"%(subsetting.moduleName,)
    arch += "port map (\n\t"

    # Connect data addr ports to buffs
    arch += "--Connect data addr ports to buffers\n"
    for addr in instr.addrs - set(["res"]):
        arch += "%s_addr => %s_addr_buff_in,\n"%(addr, addr)
    arch += "\n"

    # Connect Comm Get update ports to buff
    if "update" in para.mem_controls["GET"]:
        arch += "--Connect Comm Get update ports to buffer\n"
        for addr in  para.mem_controls["GET"]["update" ]:
            arch += "%s_update => GET_update_buff_%s_in,\n"%(addr, addr)
        arch += "\n"

    # Connect Data Sel ports to buffs
    if para.data_selects:
        for addr, selects in para.data_selects.items():
            arch += "--Connect %s Data Sel ports to buffers\n"%(addr, )
            for select in selects:
                arch += "%s_sel_%s => %s_sel_buff_%s_in,\n"%(addr, select, addr, select)
            arch += "\n"

    # Connect ALU Control ports to buffs
    arch_d1 = ""
    for control in para.used_ALU_controls:
        if para.used_ALU_controls[control] == None:
            arch_d1 += "control_%s => control_%s_buff_in,\n"%(control, control)
    # output ALU Control ports
    if arch_d1:
        arch += "--Connect ALU Control Ports to buffers\n"
        arch += arch_d1
        arch += "\n"

    # Connect result write back ports to buffs
    arch += "---Connect Write Back Ports to buffers\n"
    arch += "res_addr => res_addr_buff_in,\n"
    for mem in instr.accesses["res"]:
        arch += "res_sel_%s => res_sel_buff_%s_in,\n"%(mem, mem)
    arch += "\n"

    # Connect status update port to buff
    if para.status_reg:
        arch += "--Connect status update port to buffer\n"
        arch += "status_update => status_update_buff_in,\n"
        arch += "\n"

    # Connect jump ports to buff
    if para.jumps:
        arch += "--Connect jump ports to buffer\n"
        for jump in para.jumps:
            arch += "%s => jump_buff_%s_in,\n"%(jump, jump)
        arch += "\n"

    # Connect instr port to buff
    arch += "--Connect instr ports to buffer\n"
    arch += "instr => instr_buff_out\n"

    arch +="\b);\n\b"

    return arch, signals, imports

def genDataAddrBuffers(para, instr, settings, arch, signals):
    signals += "\n--Instr Decoder -> Data Memories Addr signals\n"
    arch += "\n--Instr Decoder -> Data Memories Addr buffers\n"

    signals_d1 = ""
    for addr in (instr.addrs - set(["res"])):
        signals += "signal %s_addr_buff_in  : std_logic_vector(%i downto 0);\n"%(addr, getattr(para, "%s_addr_width"%(addr, )) - 1)
        signals_d1 += "signal %s_addr_buff_out : std_logic_vector(%i downto 0);\n"%(addr, getattr(para, "%s_addr_width"%(addr, )) - 1)

        arch += "%s_addr_buff : %s\n\t"%(addr, settings.moduleName + "_delay")
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => %i,\n"%(getattr(para, "%s_addr_width"%(addr, )), )
        arch += "data_depth => 1\n"
        arch += "\b)\n"
        arch += "port map(\n\t"
        arch += "clock => clock,\n"
        if para.jumps:
            arch += "reset => jump_or_reset,\n"
        else:
            arch += "reset => reset,\n"
        arch += "data_in  => %s_addr_buff_in,\n"%(addr, )
        arch += "data_out => %s_addr_buff_out\n"%(addr, )
        arch += "\b);\n\b"
    signals += signals_d1
    return arch, signals

def genMemControlsBuffers(para, instr, settings, arch, signals):
    # Handle Comm Get update
    if "GET" in para.mem_controls and "update" in para.mem_controls["GET"]:
        signals += "\n--Instr Decoder ->  GET update signals\n"

        #Create a single buffer for all updates
        arch += "\n--Instr Decoder -> GET update buffer\n"
        arch += "GET_update_buff : %s\n\t"%(settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => %i,\n"%(len(para.mem_controls["GET"]["update"]), )
        arch += "data_depth => 1\n"
        arch += "\b)\n"
        arch += "port map(\n\t"

        # Handle com get update
        signals_d1 = arch_d1 = ""
        index = 0
        for addr in para.mem_controls["GET"]["update"]:
            # Def buffer signals
            signals += "signal GET_update_buff_%s_in  : std_logic;\n"%(addr, )
            signals_d1 += "signal GET_update_buff_%s_out : std_logic;\n"%(addr, )

            # Connect buffer signals
            arch += "data_in(%i) => GET_update_buff_%s_in,\n"%(index, addr)
            arch_d1 += "data_out(%i)  => GET_update_buff_%s_out,\n"%(index, addr)
            index += 1
        arch += arch_d1
        signals += signals_d1
        arch += "clock => clock,\n"
        if para.jumps:
            arch += "reset => jump_or_reset\n"
        else:
            arch += "reset => reset\n"
        arch += "\b);\n\b"

    return arch, signals

def genDataSelectBuffers(para, instr, settings, arch, signals):
    # Loop over all addr with data selects
    for addr, accesses in para.data_selects.items():
        signals_d1 = ""
        signals += "\n--Instr Decoder -> %s Data Select signals\n"%(addr,)

        # Create one buffer per data addr
        arch += "\n--Instr Decoder -> %s Data Select buffer\n"%(addr,)
        arch += "%s_sel_buff : %s\n\t"%(addr, settings.moduleName + "_delay")
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => %i,\n"%(len(accesses), )
        arch += "data_depth => 2\n"
        arch += "\b)\n"
        arch += "port map(\n\t"

        # Handle each mem type within with sel
        signals_d1 = arch_d1 = ""
        index = 0
        for mem in accesses:
            # Def buffer signals
            signals += "signal %s_sel_buff_%s_in  : std_logic;\n"%(addr, mem)
            signals_d1 += "signal %s_sel_buff_%s_out : std_logic;\n"%(addr, mem)

            # Connect buffer signals
            arch += "data_in(%i) => %s_sel_buff_%s_in,\n"%(index, addr, mem)
            arch_d1 += "data_out(%i) => %s_sel_buff_%s_out,\n"%(index, addr, mem)
            index += 1
        arch += arch_d1
        signals += signals_d1

        arch += "clock => clock,\n"
        if para.jumps:
            arch += "reset => jump_or_reset\n"
        else:
            arch += "reset => reset\n"
        arch += "\b);\n\b"
    return arch, signals

def genALUBuffers(para, instr, settings, arch, signals):
    signals_d1 = ""

    control_widths = { "carry_in_sel" : 3, "carry_in" : 1, "ALU_mode" : 4, "op_mode" : 7, "in_mode" : 5 }
    # Loop over all possible ALU control ports
    for control in para.used_ALU_controls:
        # Select other the controls using ports
        if para.used_ALU_controls[control] == None:
            # Declare needed signals
            signals_d1 += "signal control_%s_buff_in  : std_logic_vector(%i downto 0);\n"%(control, control_widths[control] - 1)
            signals_d1 += "signal control_%s_buff_out : std_logic_vector(%i downto 0);\n"%(control, control_widths[control] - 1)

            # Instantiate needed buffer
            arch += "\n--Instr Decoder -> ALU control %s Buffer\n"%(control, )
            arch += "control_%s_buff : %s\n\t"%(control, settings.moduleName + "_delay")
            arch += "generic map (\n\t"
            arch += "default_value => 0,\n"
            arch += "data_width => %i,\n"%(control_widths[control], )
            arch += "data_depth => 3\n"
            arch += "\b)\n"
            arch += "port map(\n\t"
            arch += "clock => clock,\n"
            if para.jumps:
                arch += "reset => jump_or_reset,\n"
            else:
                arch += "reset => reset,\n"
            arch += "data_in  => control_%s_buff_in,\n"%(control, )
            arch += "data_out => control_%s_buff_out\n"%(control, )
            arch += "\b);\n\b"
    # If there were signals add their declaration to VHDL
    if signals_d1:
        signals += "\n--Instr Decoder -> ALU control signals\n"
        signals += signals_d1
    return arch, signals

def genResWriteBackBuffers(para, instr, settings, arch, signals):
    signals += "\n--Instr Decoder -> Data Write Back signals\n"
    arch += "\n--Instr Decoder -> Data Write Back buffers\n"

    # Handle res addr
    signals += "signal res_addr_buff_in  : std_logic_vector(%i downto 0);\n"%(para.res_addr_width, )
    signals += "signal res_addr_buff_mid : std_logic_vector(%i downto 0);\n"%(para.res_addr_width, )
    signals += "signal res_addr_buff_out : std_logic_vector(%i downto 0);\n"%(para.res_addr_width, )

    # Create a single (2 stage) buffer for res addr
    arch += "res_addr_buff_first : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(para.res_addr_width, )
    arch += "data_depth => 3\n"
    arch += "\b)\n"
    arch += "port map(\n\t"
    arch += "clock => clock,\n"
    if para.jumps:
        arch += "reset => jump_or_reset,\n"
    else:
        arch += "reset => reset,\n"
    arch += "data_in  => res_addr_buff_in,\n"
    arch += "data_out => res_addr_buff_mid\n"
    arch += "\b);\n\b"

    arch += "res_addr_buff_last : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(para.res_addr_width, )
    arch += "data_depth => 3\n"
    arch += "\b)\n"
    arch += "port map(\n\t"
    arch += "clock => clock,\n"
    arch += "reset => reset,\n"
    arch += "data_in  => res_addr_buff_mid,\n"
    arch += "data_out => res_addr_buff_out\n"
    arch += "\b);\n\b"

    # Create a single (2 stage) buffer for all res selects
    arch += "\nres_select_buff_first : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(len(instr.accesses["res"]), )
    arch += "data_depth => 3\n"
    arch += "\b)\n"
    arch += "port map(\n\t"

    arch_d2  = "res_select_buff_last : %s\n\t"%(settings.moduleName + "_delay", )
    arch_d2 += "generic map (\n\t"
    arch_d2 += "default_value => 0,\n"
    arch_d2 += "data_width => %i,\n"%(len(instr.accesses["res"]), )
    arch_d2 += "data_depth => 3\n"
    arch_d2 += "\b)\n"
    arch_d2 += "port map(\n\t"

    arch_d1 = arch_d3 = ""
    signals_d1 = signals_d2 = ""
    index = 0
    for mem in instr.accesses["res"]:
        # Def buffer signals
        signals += "signal res_sel_buff_%s_in  : std_logic;\n"%(mem, )
        signals_d1 += "signal res_sel_buff_%s_mid : std_logic;\n"%(mem, )
        signals_d2 += "signal res_sel_buff_%s_out : std_logic;\n"%(mem, )

        # Connect buffer signals
        arch += "data_in(%i) => res_sel_buff_%s_in,\n"%(index, mem)
        arch_d2 += "data_in(%i) => res_sel_buff_%s_mid,\n"%(index, mem)
        arch_d1 += "data_out(%i) => res_sel_buff_%s_mid,\n"%(index, mem)
        arch_d3 += "data_out(%i) => res_sel_buff_%s_out,\n"%(index, mem)
        index += 1
    signals += signals_d1 + signals_d2
    arch += arch_d1
    arch_d2 += arch_d3

    arch += "clock => clock,\n"
    if para.jumps:
        arch += "reset => jump_or_reset\n"
    else:
        arch += "reset => reset\n"
    arch +="\b);\n\b"

    arch_d2 += "clock => clock,\n"
    arch_d2 += "reset => reset\n"
    arch_d2 += "\b);\n"

    arch += arch_d2

    return arch, signals

def genStatusRegisterBuffers(para, instr, settings, arch, signals):
    if para.status_reg:
        signals += "\n--Instr Decoder -> Status Register signals\n"
        arch += "\n--Instr Decoder -> Status Register buffers\n"

        signals += "signal status_update_buff_in  : std_logic;\n"
        signals += "signal status_update_buff_mid : std_logic;\n"
        signals += "signal status_update_buff_out : std_logic;\n"

        arch += "status_update_buff_first : %s\n\t"%(settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => 1,\n"
        arch += "data_depth => 3\n"
        arch += "\b)\n"
        arch += "port map(\n\t"
        arch += "clock => clock,\n"
        if para.jumps:
            arch += "reset => jump_or_reset,\n"
        else:
            arch += "reset => reset,\n"
        arch += "data_in(0)  => status_update_buff_in,\n"
        arch += "data_out(0) => status_update_buff_mid\n"
        arch += "\b);\n\b"

        arch += "status_update_buff_last : %s\n\t"%(settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => 1,\n"
        arch += "data_depth => 3\n"
        arch += "\b)\n"
        arch += "port map(\n\t"
        arch += "clock => clock,\n"
        arch += "reset => reset,\n"
        arch += "data_in(0)  => status_update_buff_mid,\n"
        arch += "data_out(0) => status_update_buff_out\n"
        arch += "\b);\n\b"
    return arch, signals

def genProgramCounterBuffers(para, instr, settings, arch, signals):
    if para.jumps:
        signals += "\n--Instr Decoder -> Program Counter signals\n"
        arch += "\n--Instr Decoder -> Program Counter buffers\n"

        # Create only single buffer for all jump signals
        arch += "jump_buff : %s\n\t"%(settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => %i,\n"%(len(para.jumps))
        arch += "data_depth => 3\n"
        arch += "\b)\n"
        arch += "port map(\n\t"

        arch_d1 = signals_d1 = ""
        index = 0
        # Loop over each jump signal
        for jump in para.jumps:
            # Declare signals in and out of buff
            signals += "signal jump_buff_%s_in  : std_logic;\n"%(jump, )
            signals_d1 += "signal jump_buff_%s_out : std_logic;\n"%(jump, )

            # Connect in and out signals to buffer
            arch += "data_in(%i) => jump_buff_%s_in,\n"%(index, jump)
            arch_d1 += "data_out(%i) => jump_buff_%s_out,\n"%(index, jump)
            index += 1
        signals += signals_d1
        arch += arch_d1

        arch += "clock => clock,\n"
        if para.jumps:
            arch += "reset => jump_or_reset\n"
        else:
            arch += "reset => reset\n"

        arch +="\b);\n\b"
    return arch, signals

##################################################################################
##                        Instr Fetch GEN FUNCTIONS
##################################################################################

def genProgramMemory(para, instr, settings, arch, signals, imports):
    arch += "\n--###########################################################\n"
    arch += "--##                    Program Memory                     ##\n"
    arch += "--###########################################################\n"

    # Create Program Memory vhdl
    import copy
    subsetting = copy.copy(settings)
    subsetting.moduleName += "_prog_mem"
    subsetting.jsonStr  = "{"
    subsetting.jsonStr += "\"data_values\": \"%s\","%(para.PM_values, )
    subsetting.jsonStr += "\"use_BROM\": %s,"%(jsonBool(para.PM_use_BROM), )
    subsetting.jsonStr += "\"conc_reads\": 1,"
    subsetting.jsonStr += "\"data_width\": %i,"%(para.instr_width, )
    subsetting.jsonStr += "\"depth\": %i"%(para.PM_depth, )
    subsetting.jsonStr += "}"
    import ROM
    para.PM_addr_width = ROM.generate(subsetting)

    # Import Created VHDL
    imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

    # Instantiate Program Memory
    arch += "\n--Program Memory \n"
    arch += "PM: %s\n\t"%(subsetting.moduleName,)
    arch += "port map (\n\t"
    arch += "addr_0 => PC_buff_out,\n"
    arch += "data_0 => instr_buff_in\n"
    arch +="\b);\n\b"

    # Declare Program Memory to Instr Decoder signal
    signals += "\n--Program Memory  -> Instr Decoder signals\n"
    signals += "signal instr_buff_in  : std_logic_vector(%i downto 0);\n"%(para.instr_width - 1, )
    signals += "signal instr_buff_out : std_logic_vector(%i downto 0);\n"%(para.instr_width - 1, )

    # Instantiate Program Memory to Instr Decoder buffer
    arch += "\n--Program Memory -> Instr Decoder buffer\n"
    arch += "instr_buff : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(para.instr_width, )
    arch += "data_depth => 1\n"
    arch += "\b)\n"
    arch += "port map(\n\t"
    arch += "clock => clock,\n"
    arch += "reset => reset,\n"
    arch += "data_in  => instr_buff_in,\n"
    arch += "data_out => instr_buff_out\n"
    arch += "\b);\n\b"

    return arch, signals, imports

def genProgramCounter(para, instr, settings, arch, signals, imports):
    arch += "\n--###########################################################\n"
    arch += "--##                   Program Counter                     ##\n"
    arch += "--###########################################################\n"

    # Create Program Counter vhdl
    import copy
    subsetting = copy.copy(settings)
    subsetting.moduleName += "_prog_counter"
    subsetting.jsonStr  = "{"
    subsetting.jsonStr += "\"PC_wrap_value\": %i,"%(para.PC_wrap_value, )
    subsetting.jsonStr += "\"PC_width\"     : %i,"%(para.PC_width, )
    subsetting.jsonStr += "\"jumps_enabled\": ["
    comma = ""
    for jump in para.jumps:
        subsetting.jsonStr += "%s\"%s\""%(comma, jump)
        comma = ", "
    subsetting.jsonStr += "]"
    subsetting.jsonStr += "}"
    import program_counter
    para.required_statuses = program_counter.generate(subsetting)

    # Import Created VHDL
    imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

    # Instantiate Program Counter
    arch += "\n--Program Counter \n"
    arch += "PC: %s\n\t"%(subsetting.moduleName,)
    arch += "port map (\n\t"

    # Handle jump related ports
    if para.jumps:
        arch += "--jump ports\n"
        arch += "jump_occured => jumped_buff_in,\n"
        if para.PC_width > para.c_width:
            #Warning about not being able to jump to all PC values
            import warnings
            warnings.warn("PC jump_addr isn't wide enough to jump to all possible PC calues\n")
            arch += "jump_addr => (%i downto 0 <= c_selected_buff_out, others <= '0'),\n"%(para.c_width - 1, )
        else:
            arch += "jump_addr => c_selected_buff_out(%i downto 0),\n"%(para.PC_width - 1, )
        for jump in para.jumps:
            arch += "%s => jump_buff_%s_out,\n"%(jump, jump)
        arch += "\n"

    # Handle status input ports
    if para.required_statuses:
        arch += "--status ports\n"
        for port in para.required_statuses:
            arch += "status_%s => status_reg_%s_out,\n"%(port, port)
        arch += "\n"

    arch += "--General Ports\n"
    arch += "clock => clock,\n"
    arch += "reset => reset,\n"
    arch += "value => PC_buff_in\n"
    arch +="\b);\n\b"

    # Declare reseting of buffers after a Jump occures
    if para.jumps:
        signals += "\n--Jump occured signals\n"
        signals += "signal jumped_buff_in  : std_logic;\n"
        signals += "signal jumped_buff_out : std_logic;\n"
        signals += "signal jump_or_reset : std_logic;\n"

        # Instance Jump occured buffer
        arch += "\n--Jump occured buffer\n"
        arch += "jumped_buff : %s\n\t"%(settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => 1,\n"
        arch += "data_depth => 1\n"
        arch += "\b)\n"
        arch += "port map(\n\t"
        arch += "clock => clock,\n"
        arch += "reset => reset,\n"
        arch += "data_in(0)  => jumped_buff_in,\n"
        arch += "data_out(0) => jumped_buff_out\n"
        arch += "\b);\n\b"

        # Generate jump_or_reset signal
        arch += "\n--Generate jump_or_reset signal\n"
        arch += "jump_or_reset <= jumped_buff_out or reset;\n"

    # Add Program Counter to Program Memory signals to sPFE
    signals += "\n--Program Counter -> Program Memory signals\n"
    signals += "signal PC_buff_in  : std_logic_vector(%i downto 0);\n"%(para.PC_width - 1, )
    signals += "signal PC_buff_out : std_logic_vector(%i downto 0);\n"%(para.PC_width - 1, )

    # Add Program Counter to Program Memory buffer to sPFE
    arch += "\n--Program Counter -> Program Memory buffer\n"
    arch += "PC_buff : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(para.PC_width, )
    arch += "data_depth => 1\n"
    arch += "\b)\n"
    arch += "port map(\n\t"
    arch += "clock => clock,\n"
    arch += "reset => reset,\n"
    arch += "data_in  => PC_buff_in,\n"
    arch += "data_out => PC_buff_out\n"
    arch += "\b);\n\b"

    return arch, signals, imports

def genStatusRegister(para, instr, settings, arch, signals, imports):
    if not para.required_statuses:
        if para.status_reg:
            import warnings
            warnings.warn("Instruction Decoder is updating a non existing status register\n")
    else:
        arch += "\n--###########################################################\n"
        arch += "--##                    Status Register                    ##\n"
        arch += "--###########################################################\n"

        # Add status register to arch
        settings.moduleName += "_status_reg"
        settings.jsonStr  = "{"
        settings.jsonStr += "\"has_reset\" : false,"
        settings.jsonStr += "\"has_preset\": false,"
        settings.jsonStr += "\"read_mode\" : \"always\","
        settings.jsonStr += "\"write_mode\": \"edge\""
        settings.jsonStr += "}"
        import register
        register.generate(settings)

        # Import Created VHDL
        imports += "use work.%s_pkg.ALL;\n"%(settings.moduleName,)

        # Instantiate status register
        arch += "\n--status register\n"
        arch += "SR: %s\n\t"%(settings.moduleName,)
        arch += "generic map (data_width => %i)\n"%(len(para.required_statuses))
        arch += "port map (\n\t"

        signals += "\n--Status Register Signals\n"
        arch_d1 = signals_d1 = ""
        index = 0
        for status in para.required_statuses:
            # Declare in aned out signals
            signals += "signal status_reg_%s_in  : std_logic;\n"%(status, )
            signals_d1 += "signal status_reg_%s_out : std_logic;\n"%(status, )

            # Connect status singals to reg
            arch += "data_in(%i) => status_reg_%s_in,\n"%(index, status)
            arch_d1 = "data_out(%i) => status_reg_%s_out,\n"%(index, status)
            index += 1
        signals += signals_d1
        arch += arch_d1

        arch += "write_enable => status_update_buff_out\n"
        arch += "\b);\n\b"

    return arch, signals, imports

##################################################################################
##                   DATA Path and ALU GEN FUNCTIONS
##################################################################################

def genDataSelect(para, instr, settings, arch, signals, imports):
    import mux
    import copy

    arch += "\n--###########################################################\n"
    arch += "--##                      Data select                      ##\n"
    arch += "--###########################################################\n"

    included_mux_widths = []

    signals_d1 = ""
    signals += "\n--Data Select -> ALU Signals\n"
    # Loop over all data addrs
    for addr in instr.addrs - set(["res"]):
        arch += "-- %s data select\n"%(addr, )
        # Check if a mux is needed or not
        if not addr in para.data_selects:
            # Buffer width is that of the single mem
            mem = list(instr.accesses[addr])[0]
            if mem == "GET": setattr(para, "%s_width"%(addr, ), para.CG_width)
            else: setattr(para, "%s_width"%(addr, ), getattr(para, "%s_width"%(mem, )) )
            # Connect the only access straight to the buff
            arch += "%s_selected_buff_in <= %s_%s_buff_out;\n"%(addr, addr, list(instr.accesses[addr])[0])
        else:
            # Create mux on first use
            if not len(para.data_selects[addr]) in included_mux_widths:
                included_mux_widths.append(len(para.data_selects[addr]))

                # Generate Mux vhdl
                subsetting = copy.copy(settings)
                subsetting.moduleName = "priority_mux_%i"%(len(para.data_selects[addr]), )
                subsetting.jsonStr = "{\"number_inputs\" : %i, \"binary_select\" : false}"%(len(para.data_selects[addr]), )
                mux.generate(subsetting)

                # import mux into sFPE
                imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

            # Loop over look selects mems
            setattr(para, "%s_width"%(addr, ), 0)
            index = 0
            arch_d1 = arch_d2 = ""
            for select in para.data_selects[addr]:
                # Get mem width
                if select == "GET": MEM_width = para.CG_width
                else: MEM_width = getattr(para, "%s_width"%(select, ) )
                # Select the largest mem width to be the buffer width
                if getattr(para, "%s_width"%(addr, )) < MEM_width: setattr(para, "%s_width"%(addr, ), MEM_width)

                arch_d1 += "input_%i => %s_%s_buff_out,\n"%(index, addr, select)
                arch_d2 += "select_%i => %s_sel_buff_%s_out,\n"%(index, addr, select)
                index += 1
            # Instantiate mux
            arch += "%s_data_mux : priority_mux_%i\n\t"%(addr, len(para.data_selects[addr]))
            arch += "generic map (data_width => %i)\n"%(getattr(para, "%s_width"%(addr, )), )
            arch += "port map (\n\t"
            arch += arch_d1 + arch_d2
            arch += "data_out => %s_selected_buff_in\n"%(addr, )
            arch += "\b);\n\b"

        # Declare Data select signals
        signals += "signal %s_selected_buff_in : std_logic_vector(%i downto 0);\n"%(addr,  getattr(para, "%s_width"%(addr, )) - 1)
        signals_d1 += "signal %s_selected_buff_out : std_logic_vector(%i downto 0);\n"%(addr, getattr(para, "%s_width"%(addr, )) - 1)

        # Generate Data select buff
        arch += "\n-- %s data select buff\n"%(addr, )
        arch += "%s_selected_buff : %s\n\t"%(addr, settings.moduleName + "_delay", )
        arch += "generic map (\n\t"
        arch += "default_value => 0,\n"
        arch += "data_width => %i,\n"%(getattr(para, "%s_width"%(addr, )), )
        arch += "data_depth => 1\n"
        arch += "\b)\n"
        arch += "port map(\n\t"
        arch += "clock => clock,\n"
        arch += "reset => reset,\n"
        arch += "data_in  => %s_selected_buff_in,\n"%(addr, )
        arch += "data_out => %s_selected_buff_out\n"%(addr, )
        arch += "\b);\n\b"
    signals += signals_d1

    return arch, signals, imports

def genALU(para, instr, settings, arch, signals, imports):
    arch += "\n--###########################################################\n"
    arch += "--##                           ALU                          ##\n"
    arch += "--###########################################################\n"

    import copy
    subsetting = copy.copy(settings)

    #Generate ALU subunit
    subsetting.moduleName += "_ALU"
    subsetting.jsonStr  = "{"
    # Pass widths
    for addr in ["a", "b", "c", "d", "res"]:
        subsetting.jsonStr += "\"%s_width\" : %i,"%(addr, getattr(para, "ALU_%s_width"%(addr, )), )
    # Pass required statuses
    comma = ""
    subsetting.jsonStr += "\"required_statuses\" : ["
    for status in para.required_statuses:
        subsetting.jsonStr += "%s\"%s\""%(comma, status)
        comma = ", "
    subsetting.jsonStr += "],"
    # Pass required control ports
    comma = ""
    subsetting.jsonStr += "\"controls\" : {"
    for control, mode in para.used_ALU_controls.items():
        if mode == None:
            subsetting.jsonStr += "%s\"%s\" : null"%(comma, control)
        else:
            subsetting.jsonStr += "%s\"%s\" : %i"%(comma, control, mode)
        comma = ", "
    subsetting.jsonStr += "}"
    subsetting.jsonStr += "}"
    import ALU
    ALU.generate(subsetting)

    # import ALU subunit
    imports += "use work.%s_pkg.ALL;\n"%(subsetting.moduleName, )

    # Instance ALU subunit to arch
    arch += "ALU: %s\n\t"%(subsetting.moduleName,)
    arch += "port map (\n\t"

    # Handle data input ports
    arch += "--Connect up data ports\n"
    for addr in ["a", "b", "c", "d"]:
        # Check if the ALU port exists for addr
        if getattr(para, "ALU_%s_width"%(addr, )) != 0:
            if getattr(para, "ALU_%s_width"%(addr, )) > getattr(para, "%s_width"%(addr, )):
                arch += "%s => (%i downto 0 <= %s_selected_buff_out, others '0').\n"%(addr, getattr(para, "%s_width"%(addr, )) - 1, addr)
            else:
                arch += "%s => %s_selected_buff_out(%i downto 0),\n"%(addr, addr, getattr(para, "%s_width"%(addr, )) - 1)

    # Handle Data output port
    arch += "\n--Data output ports\n"
    arch += "res => result_buff_in,\n"
    for status in para.required_statuses:
        arch += "status_%s => status_reg_%s_in,\n"%(status, status)

    # Handle Control ports
    arch_d1 = ""
    control_widths = { "carry_in_sel" : 3, "carry_in" : 1, "ALU_mode" : 4, "op_mode" : 7, "in_mode" : 5 }
    for control in para.used_ALU_controls:
        # Select other the controls using ports
        if para.used_ALU_controls[control] == None:
            arch_d1 += "control_%s => control_%s_buff_out,\n"%(control, control)
    if arch_d1:
        arch += "\n--Control ports\n"
        arch += arch_d1
        arch += "\n"

    arch += "clock => clock,\n"
    arch += "reset => reset\n"
    arch +="\b);\n\b"

    # Declare data result signals
    signals += "\n--ALU -> Data Write Back signals\n"
    signals += "signal result_buff_in  : std_logic_vector(%i downto 0);\n"%(para.res_width, )
    signals += "signal result_buff_out : std_logic_vector(%i downto 0);\n"%(para.res_width, )

    # Generate Data result buff
    arch += "\n--ALU -> Data Write Back buffer\n"
    arch += "result_buff : %s\n\t"%(settings.moduleName + "_delay", )
    arch += "generic map (\n\t"
    arch += "default_value => 0,\n"
    arch += "data_width => %i,\n"%(para.res_width, )
    arch += "data_depth => 1\n"
    arch += "\b)\n"
    arch += "port map(\n\t"
    arch += "clock => clock,\n"
    arch += "reset => reset,\n"
    arch += "data_in  => result_buff_in,\n"
    arch += "data_out => result_buff_out\n"
    arch += "\b);\n\b"

    return arch, signals, imports

##################################################################################

# Root Generate function
def generate(settings):
    # Process passed json parameters
    import InstrSet
    para  = readParaJson(settings.jsonStr)
    instr = InstrSet.readInstrSetJson(settings.instrJson)

    # Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports, para)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    # Support Code for generating sub units
    sys.path.append(settings.pathRoot + "\\ComComp")
    sys.path.append(settings.pathRoot + "\\ComMem")
    sys.path.append(settings.pathRoot + "\\sFPE\\SubComponents")
    imports += "\nlibrary work;\n"

    import copy
    # Generate delay buffer vhdl
    imports = genDelayVHDL(para, copy.copy(settings), imports)

    # Create Data Merories to get their addr widths
    arch, signals, imports = genCommGet(para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genImmROM (para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genRegFile(para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genDataMem(para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genCommPut(para, instr, copy.copy(settings), arch, signals, imports)

    # Create Instruction Decoder and it's buffers
    arch, signals, imports = genInstrDecoder(para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals = genDataAddrBuffers      (para, instr, copy.copy(settings), arch, signals)
    arch, signals = genMemControlsBuffers   (para, instr, copy.copy(settings), arch, signals)
    arch, signals = genDataSelectBuffers    (para, instr, copy.copy(settings), arch, signals)
    arch, signals = genALUBuffers           (para, instr, copy.copy(settings), arch, signals)
    arch, signals = genResWriteBackBuffers  (para, instr, copy.copy(settings), arch, signals)
    arch, signals = genStatusRegisterBuffers(para, instr, copy.copy(settings), arch, signals)
    arch, signals = genProgramCounterBuffers(para, instr, copy.copy(settings), arch, signals)

    # Crate data Select
    arch, signals, imports = genDataSelect(para, instr, copy.copy(settings), arch, signals, imports)

    # Create Instr fetch path and it's buffers
    arch, signals, imports = genProgramMemory (para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genProgramCounter(para, instr, copy.copy(settings), arch, signals, imports)
    arch, signals, imports = genStatusRegister(para, instr, copy.copy(settings), arch, signals, imports)

    # Generation ALU
    arch, signals, imports = genALU(para, instr, copy.copy(settings), arch, signals, imports)

    # Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    # Add Needed paths
    pathRoot = sys.path[0] + "\\.."
    sys.path.append(pathRoot)

    # Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput(True)
    settings.pathRoot = pathRoot
    generate(settings)
