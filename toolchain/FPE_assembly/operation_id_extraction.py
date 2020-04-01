from .grammar.FPE_assemblyParser import FPE_assemblyParser as parser
from .get_component import get_component

def get_operation_id(ctx):
    if type(ctx) == parser.OperationContext:
        return get_operation_id_operation(ctx)
    else:
        try:
            return get_operation_id(ctx.parentCtx)
        except Exception as e:
            raise ValueError("Unsupported ctx given, " + str(type(ctx)) )

def get_operation_id_operation(ctx):
    get_operation_id_encoded_addr.addr = 0
    if   ctx.void_operation() != None:
        return get_operation_id_void_operation(ctx.void_operation())
    elif ctx.pc_operation  () != None:
        return get_operation_id_pc_operation  (ctx.pc_operation  ())
    elif ctx.bam_operation () != None:
        return get_operation_id_bam_operation (ctx.bam_operation ())
    elif ctx.alu_operation () != None:
        return get_operation_id_alu_operation (ctx.alu_operation ())
    else:
        raise AttributeError("operation with no supported attribute")

####################################################################

def get_operation_id_void_operation(ctx):
    if   ctx.void_0f_0s() != None:
        return get_operation_id_void_0f_0s(ctx.void_0f_0s())
    else:
        raise AttributeError("void_operation with no supported attribute")

def get_operation_id_void_0f_0s(ctx):
    return "#".join([
        ctx.void_0f_0s_mnemonic().getText().upper(),
        "|".join([]),
        get_component(ctx),
        "|".join([]),
    ])

####################################################################

def get_operation_id_pc_operation(ctx):
    if   ctx.pc_0f_0s() != None:
        return get_operation_id_pc_0f_0s(ctx.pc_0f_0s())
    else:
        raise AttributeError("pc_operation with no supported attribute")

def get_operation_id_pc_0f_0s(ctx):
    return "#".join([
        ctx.pc_0f_0s_mnemonic().getText().upper(),
        "|".join([get_operation_id_IMM_access(None)]),
        get_component(ctx),
        "|".join([]),
    ])

####################################################################

def get_operation_id_bam_operation(ctx):
    if   ctx.bam_0f_0s() != None:
        return get_operation_id_bam_0f_0s(ctx.bam_0f_0s())
    elif ctx.bam_1f_0s() != None:
        return get_operation_id_bam_1f_0s(ctx.bam_1f_0s())
    else:
        raise AttributeError("bam_operation with no supported attribute")

def get_operation_id_bam_0f_0s(ctx):
    return "#".join([
        ctx.bam_0f_0s_mnemonic().getText().upper(),
        "|".join([]),
        get_component(ctx),
        "|".join([]),
    ])

def get_operation_id_bam_1f_0s(ctx):
    return "#".join([
        ctx.bam_1f_0s_mnemonic().getText().upper(),
        "|".join([get_operation_id_mem_fetch(ctx.mem_fetch()), ]),
        get_component(ctx),
        "|".join([]),
    ])


####################################################################

def get_operation_id_alu_operation(ctx):
    if   ctx.alu_1f_1s() != None:
        return get_operation_id_alu_1f_1s(ctx.alu_1f_1s())
    elif ctx.alu_2f_0s() != None:
        return get_operation_id_alu_2f_0s(ctx.alu_2f_0s())
    elif ctx.alu_2f_1s() != None:
        return get_operation_id_alu_2f_1s(ctx.alu_2f_1s())
    else:
        raise AttributeError("alu_operation with no supported attribute")

def get_operation_id_alu_1f_1s(ctx):
    return "#".join([
        ctx.alu_1f_1s_mnemonic().getText().upper(),
        "|".join([get_operation_id_alu_fetch(ctx.alu_fetch()), ]),
        get_component(ctx),
        "|".join([get_operation_id_alu_store(ctx.alu_store()), ]),
    ])

def get_operation_id_alu_2f_0s(ctx):
    return "#".join([
        ctx.alu_2f_0s_mnemonic().getText().upper(),
        "|".join([get_operation_id_alu_fetch(ctx.alu_fetch(0)), get_operation_id_alu_fetch(ctx.alu_fetch(1))]),
        get_component(ctx),
        "|".join([]),
    ])

def get_operation_id_alu_2f_1s(ctx):
    return "#".join([
        ctx.alu_2f_1s_mnemonic().getText().upper(),
        "|".join([get_operation_id_alu_fetch(ctx.alu_fetch(0)), get_operation_id_alu_fetch(ctx.alu_fetch(1))]),
        get_component(ctx),
        "|".join([get_operation_id_alu_store(ctx.alu_store()), ]),
    ])

def get_operation_id_alu_fetch(ctx):
    if ctx.ACC() != None:
        return "ACC"
    elif ctx.mem_fetch() != None:
        return get_operation_id_mem_fetch(ctx.mem_fetch())
    else:
        raise AttributeError("alu_fetch with no supported attribute")

def get_operation_id_alu_store(ctx):
    if ctx.ACC() != None:
        return "ACC"
    elif ctx.mem_store() != None:
        return get_operation_id_mem_store(ctx.mem_store())
    else:
        raise AttributeError("alu_store with no supported attribute")

####################################################################

def get_operation_id_mem_fetch(ctx):
    if   ctx.imm_access() != None:
        return get_operation_id_IMM_access(ctx.imm_access())
    elif ctx.get_access() != None:
        return get_operation_id_GET_access(ctx.get_access())
    elif ctx.reg_access() != None:
        return get_operation_id_REG_access(ctx.reg_access())
    elif ctx.ram_access() != None:
        return get_operation_id_RAM_access(ctx.ram_access())
    elif ctx.rom_access() != None:
        return get_operation_id_ROM_access(ctx.rom_access())
    else:
        raise AttributeError("mem_fetch with no supported attribute")

def get_operation_id_mem_store(ctx):
    if   ctx.put_access() != None:
        return get_operation_id_PUT_access(ctx.put_access())
    elif ctx.reg_access() != None:
        return get_operation_id_REG_access(ctx.reg_access())
    elif ctx.ram_access() != None:
        return get_operation_id_RAM_access(ctx.ram_access())
    else:
        raise AttributeError("mem_store with no supported attribute")

def get_operation_id_IMM_access(ctx):
    return "IMM" + get_operation_id_encoded_addr(None)

def get_operation_id_GET_access(ctx):
    if   ctx.GET() != None:
        return "GET" + get_operation_id_mem_addr(ctx.mem_addr())
    elif ctx.GET_ADV() != None:
        return "GET" + get_operation_id_mem_addr(ctx.mem_addr()) + "ADV"
    else:
        raise AttributeError("GET_access with no supported attribute")

def get_operation_id_PUT_access(ctx):
    if   ctx.PUT() != None:
        return "PUT" + get_operation_id_mem_addr(ctx.mem_addr())
    else:
        raise AttributeError("PUT_access with no supported attribute")

def get_operation_id_REG_access(ctx):
    if   ctx.REG() != None:
        return "REG" + get_operation_id_mem_addr(ctx.mem_addr())
    else:
        raise AttributeError("REG_access with no supported attribute")

def get_operation_id_RAM_access(ctx):
    if   ctx.RAM() != None:
        return "RAM" + get_operation_id_mem_addr(ctx.mem_addr())
    else:
        raise AttributeError("RAM_access with no supported attribute")

def get_operation_id_ROM_access(ctx):
    if   ctx.ROM() != None:
        return "ROM" + get_operation_id_mem_addr(ctx.mem_addr())
    else:
        raise AttributeError("ROM_access with no supported attribute")

####################################################################

def get_operation_id_mem_addr(ctx):
    if   ctx.encoded_addr() != None:
        return get_operation_id_encoded_addr(ctx.encoded_addr())
    elif ctx.bam_addr() != None:
        return get_operation_id_bam_addr(ctx.bam_addr())
    else:
        raise ValueError("mem_addr ctx without any supported operation")

def get_operation_id_encoded_addr(ctx):
    rtnStr = "[" + str(get_operation_id_encoded_addr.addr) + "]"
    get_operation_id_encoded_addr.addr += 1
    return rtnStr

def get_operation_id_bam_addr(ctx):
    if   ctx.BAM() != None:
        return "[" + get_component(ctx) + "]"
    elif ctx.BAM_ADV() != None:
        return "[" + get_component(ctx) + "]" + "ADV"
    else:
        raise AttributeError("GET_access with no supported attribute")
