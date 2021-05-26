from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

from FPE.toolchain import FPE_assembly as asm_utils

def get_component_addr(ctx, program_context):
    if   type(ctx) == parser.Addr_literalContext:
        return get_component_addr_literal(ctx, program_context)
    elif type(ctx) == parser.Addr_bamContext:
        return get_component_addr_bam(ctx, program_context)
    else:
        try:
            return get_component_addr(ctx.parentCtx, program_context)
        except (AttributeError, TypeError):
            raise TypeError(
                "%s is unsupported by get_component_op"%
                (
                    type(ctx),
                )
            )


def get_component_addr_literal(ctx, program_context):
    return "ID"

def get_component_addr_bam(ctx, program_context):
    if ctx.expr():
        return "BAM_%i"%(asm_utils.evaluate_expr(ctx.expr(), program_context) )
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )


################################################################

def get_component_access(ctx, program_context):
    if   type(ctx) == parser.Access_fetchContext:
        return get_component_access_fetch(ctx, program_context)
    elif type(ctx) == parser.Access_storeContext:
        return get_component_access_store(ctx, program_context)
    else:
        try:
            return get_component_access(ctx.parentCtx, program_context)
        except (AttributeError, TypeError):
            raise TypeError(
                "%s is unsupported by get_component_access"%
                (
                    type(ctx),
                )
            )


def get_component_access_fetch(ctx, program_context):
    if   ctx.access_imm():
        return get_component_access_imm(ctx.access_imm(), program_context)
    elif ctx.access_get():
        return get_component_access_get(ctx.access_get(), program_context)
    elif ctx.access_reg():
        return get_component_access_reg(ctx.access_reg(), program_context)
    elif ctx.access_ram():
        return get_component_access_ram(ctx.access_ram(), program_context)
    elif ctx.access_rom_a():
        return get_component_access_rom_a(ctx.access_rom_a(), program_context)
    elif ctx.access_rom_b():
        return get_component_access_rom_b(ctx.access_rom_b(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def get_component_access_store(ctx, program_context):
    if   ctx.access_put():
        return get_component_access_put(ctx.access_put(), program_context)
    elif ctx.access_reg():
        return get_component_access_reg(ctx.access_reg(), program_context)
    elif ctx.access_ram():
        return get_component_access_ram(ctx.access_ram(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )


def get_component_access_imm(ctx, program_context):
    return "IMM"

def get_component_access_get(ctx, program_context):
    return "GET"

def get_component_access_put(ctx, program_context):
    return "PUT"

def get_component_access_reg(ctx, program_context):
    return "REG"

def get_component_access_ram(ctx, program_context):
    return "RAM"

def get_component_access_rom_a(ctx, program_context):
    return "ROM_A"

def get_component_access_rom_b(ctx, program_context):
    return "ROM_B"

################################################################

def get_component_op(ctx, program_context):
    if   type(ctx) == parser.Op_bamContext:
        return get_component_op_bam(ctx, program_context)
    elif type(ctx) == parser.Op_aluContext:
        return get_component_op_alu(ctx, program_context)
    elif type(ctx) == parser.Op_voidContext:
        return get_component_op_void(ctx, program_context)
    elif type(ctx) == parser.Op_pcContext:
        return get_component_op_pc(ctx, program_context)
    elif type(ctx) == parser.Op_ZOLContext:
        return get_component_op_ZOL(ctx, program_context)
    else:
        try:
            return get_component_op(ctx.parentCtx, program_context)
        except (AttributeError, TypeError):
            raise TypeError(
                "%s is unsupported by get_component_op"%
                (
                    type(ctx),
                )
            )


def get_component_op_bam(ctx, program_context):
    if any(
        [
            ctx.op_bam_reset(),
            ctx.op_bam_seek(),
        ]
    ):
        child_ctx = ctx.children[0]
        if child_ctx.expr():
            return "BAM_%i"%(
                asm_utils.evaluate_expr(child_ctx.expr(), program_context)
            )
        else:
            raise NotImplementedError(
                "%s without a supported subrule at %s"%
                (
                    type(child_ctx),
                    asm_utils.ctx_start(child_ctx),
                )
            )
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def get_component_op_alu(ctx, program_context):
    if any(
        [
            ctx.op_alu_1o_1r(),
            ctx.op_alu_1o_1e_1r(),
            ctx.op_alu_2o_0r(),
            ctx.op_alu_2o_1r(),
        ]
    ):
        return "ALU"
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx)),
            )

def get_component_op_void(ctx, program_context):
    return ""

def get_component_op_pc(ctx, program_context):
    if any(
        [
            ctx.op_pc_jump(),
        ]
    ):
        return "PC"
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx)),
            )

def get_component_op_ZOL(ctx, program_context):
    if any(
        [
            ctx.op_ZOL_seek(),
            ctx.op_ZOL_set(),
        ]
    ):
        return asm_utils.token_to_text(ctx.children[0].exe_com.IDENTIFER())
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx)),
            )
