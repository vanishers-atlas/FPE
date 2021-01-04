from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

from FPE.toolchain.FPE_assembly import utils as asm_utils
from FPE.toolchain.FPE_assembly import interface as asm_inter

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
        return "BAM_%i"%(asm_inter.evaluate_expr(ctx.expr(), program_context) )
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
    elif ctx.access_rom():
        return get_component_access_rom(ctx.access_rom(), program_context)
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

def get_component_access_rom(ctx, program_context):
    return "ROM"

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
                asm_inter.evaluate_expr(child_ctx.expr(), program_context)
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
            ctx.op_alu_1f_1s(),
            ctx.op_alu_shifts(),
            ctx.op_alu_2f_0s(),
            ctx.op_alu_2f_1s(),
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
