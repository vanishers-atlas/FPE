from .grammar.FPE_assemblyParser import FPE_assemblyParser as parser

def get_component(ctx):
    if   type(ctx) == parser.OperationContext:
        return get_component_operation(ctx)
    elif type(ctx) == parser.Mem_fetchContext:
        return get_component_mem_fetch(ctx)
    elif type(ctx) == parser.Mem_storeContext:
        return get_component_mem_store(ctx)
    elif type(ctx) == parser.Mem_addrContext:
        return get_component_mem_addr (ctx)
    else:
        if ctx.parentCtx != None:
            return get_component(ctx.parentCtx)
        else:
            raise ValueError("Unsupported ctx given, " + str(type(ctx)) )

####################################################################

def get_component_operation(ctx):
    if   ctx.void_operation() != None:
        return get_component_void_operation(ctx.void_operation())
    elif ctx.pc_operation  () != None:
        return get_component_pc_operation  (ctx.pc_operation  ())
    elif ctx.bam_operation () != None:
        return get_component_bam_operation (ctx.bam_operation ())
    elif ctx.alu_operation () != None:
        return get_component_alu_operation (ctx.alu_operation ())
    else:
        raise AttributeError("operation with no supported attribute")

def get_component_void_operation(ctx):
    return ""

def get_component_pc_operation(ctx):
    return "PC"

def get_component_bam_operation(ctx):
  return "BAM_" + str(int(ctx.children[0].NUMBER().getText()))

def get_component_alu_operation(ctx):
    return "ALU"

####################################################################

def get_component_mem_fetch(ctx):
    if   ctx.imm_access() != None:
        return get_component_imm_access(ctx.imm_access())
    elif ctx.get_access() != None:
        return get_component_get_access(ctx.get_access())
    elif ctx.reg_access() != None:
        return get_component_reg_access(ctx.reg_access())
    elif ctx.ram_access() != None:
        return get_component_ram_access(ctx.ram_access())
    elif ctx.rom_access() != None:
        return get_component_rom_access(ctx.rom_access())
    else:
        raise AttributeError("mem_fetch with no supported attribute")

def get_component_mem_store(ctx):
    if   ctx.put_access() != None:
        return get_component_put_access(ctx.put_access())
    elif ctx.reg_access() != None:
        return get_component_reg_access(ctx.reg_access())
    elif ctx.ram_access() != None:
        return get_component_ram_access(ctx.ram_access())
    else:
        raise AttributeError("mem_store with no supported attribute")

def get_component_imm_access(ctx):
    return "IMM"

def get_component_get_access(ctx):
    return "GET"

def get_component_put_access(ctx):
    return "PUT"

def get_component_reg_access(ctx):
    return "REG"

def get_component_ram_access(ctx):
    return "RAM"

def get_component_rom_access(ctx):
    return "ROM"

####################################################################

def get_component_mem_addr(ctx):
    if   ctx.encoded_addr() != None:
        return get_component_encoded_addr(ctx.encoded_addr())
    elif ctx.bam_addr() != None:
        return get_component_bam_addr(ctx.bam_addr())
    else:
        raise AttributeError("mem_addr with no supported attribute")

def get_component_encoded_addr(ctx):
    return "ID"

def get_component_bam_addr(ctx):
    return "BAM_" + str(int(ctx.NUMBER().getText()))
