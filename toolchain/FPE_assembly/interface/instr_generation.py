import antlr4

from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

from FPE.toolchain import FPE_assembly as asm_utils

def generate_instr(ctx, program_context):
    generate_instr_addr_literal.port = 0
    if type(ctx) == parser.OperationContext:
        return generate_instr_op(ctx, program_context)
    else:
        try:
            return generate_instr(ctx.parentCtx, program_context)
        except Exception as e:
            raise ValueError("Unsupported ctx given, " + str(type(ctx)) )

def generate_instr_op(ctx, program_context):
    if   ctx.op_void() != None:
        return generate_instr_op_void(ctx.op_void(), program_context)
    elif ctx.op_pc() != None:
        return generate_instr_op_pc(ctx.op_pc(), program_context)
    elif ctx.op_bam() != None:
        return generate_instr_op_bam(ctx.op_bam(), program_context)
    elif ctx.op_alu() != None:
        return generate_instr_op_alu(ctx.op_alu(), program_context)
    elif ctx.op_ZOL() != None:
        return generate_instr_op_ZOL(ctx.op_ZOL(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    asm_utils.ctx_start(ctx)
                )
            )

####################################################################

def generate_instr_op_void(ctx, program_context):
    if ctx.op_void_nop():
        return "#".join(
            [
                # Mnemonic
                "NOP",
                # Sources
                "~".join([]),
                # Exe
                asm_utils.get_component_op(ctx, program_context),
                # Dests
                "~".join([]),
                # Mods
                "~".join(sorted([]))
            ]
        )
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    asm_utils.ctx_start(ctx)
                )
            )

####################################################################

def generate_instr_op_pc(ctx, program_context):

    if ctx.op_pc_jump():
        return "#".join(
            [
                # Mnemonic
                asm_utils.token_to_text(ctx.op_pc_jump().mnemonic),
                # Sources
                "~".join(
                    [
                        generate_instr_access_imm(),
                    ]
                ),
                # Exe
                asm_utils.get_component_op(ctx, program_context),
                # Dests
                "~".join([]),
                # Mods
                "~".join(sorted([]))
            ]
        )
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    asm_utils.ctx_start(ctx)
                )
            )

####################################################################

def generate_instr_op_bam(ctx, program_context):
    if   ctx.op_bam_reset() != None:
        return generate_instr_op_bam_reset(ctx.op_bam_reset(), program_context)
    elif ctx.op_bam_seek() != None:
        return generate_instr_op_bam_seek(ctx.op_bam_seek(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    asm_utils.ctx_start(ctx)
                )
            )

def generate_instr_op_bam_reset(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            "BAM_RESET",
            # Sources
            "~".join([]),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_bam_seek(ctx, program_context):
    mods = []

    if ctx.step_mod == None:
        mods.append("FORWARD")
    else:
        mods.append(asm_utils.token_to_text(ctx.step_mod))

    return "#".join(
        [
            # Mnemonic
            "BAM_SEEK",
            # Sources
            generate_instr_access_fetch(ctx.access_fetch(), program_context),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted(mods))
        ]
    )

####################################################################

def generate_instr_op_alu(ctx, program_context):
    if   ctx.op_alu_1o_1r() != None:
        return generate_instr_op_alu_1o_1r(ctx.op_alu_1o_1r(), program_context)
    elif ctx.op_alu_1o_1e_1r() != None:
        return generate_instr_op_alu_1o_1e_1r(ctx.op_alu_1o_1e_1r(), program_context)
    elif ctx.op_alu_2o_0r() != None:
        return generate_instr_op_alu_2o_0r(ctx.op_alu_2o_0r(), program_context)
    elif ctx.op_alu_2o_1r() != None:
        return generate_instr_op_alu_2o_1r(ctx.op_alu_2o_1r(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    asm_utils.ctx_start(ctx)
                )
            )

def generate_instr_op_alu_1o_1r(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            asm_utils.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu_operand(ctx.alu_operand(), program_context)
                ]
            ),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu_result(ctx.alu_result(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_alu_1o_1e_1r(ctx, program_context):
    mods = []

    return "#".join(
        [
            # Mnemonic
            "@".join(
                [
                    asm_utils.token_to_text(ctx.mnemonic),
                    str(asm_utils.evaluate_expr(ctx.expr(), program_context))
                ]
            ),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu_operand(ctx.alu_operand(), program_context)
                ]
            ),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu_result(ctx.alu_result(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted(mods))
        ]
    )

def generate_instr_op_alu_2o_0r(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            asm_utils.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu_operand(access_ctx, program_context)
                    for access_ctx in ctx.alu_operand()
                ]
            ),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_alu_2o_1r(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            asm_utils.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu_operand(access_ctx, program_context)
                    for access_ctx in ctx.alu_operand()
                ]
            ),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu_result(ctx.alu_result(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted([]))
        ]
    )


def generate_instr_access_alu_operand(ctx, program_context):

    if   ctx.access_fetch():
        return generate_instr_access_fetch(ctx.access_fetch(), program_context)
    elif asm_utils.token_to_text(ctx.internal) == "ACC":
        return "ACC"
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def generate_instr_access_alu_result(ctx, program_context):

    if ctx.access_store():
        return generate_instr_access_store(ctx.access_store(), program_context)
    elif asm_utils.token_to_text(ctx.internal) == "ACC":
        return "ACC"
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )


####################################################################

def generate_instr_op_ZOL(ctx, program_context):
    if ctx.op_ZOL_set() != None:
        return generate_instr_op_ZOL_set(ctx.op_ZOL_set(), program_context)
    elif   ctx.op_ZOL_seek() != None:
        return generate_instr_op_ZOL_seek(ctx.op_ZOL_seek(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def generate_instr_op_ZOL_set(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            "ZOL_SET",
            # Sources
            "~".join([
                generate_instr_access_fetch(ctx.iterations, program_context)
            ]),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_ZOL_seek(ctx, program_context):
    return "#".join(
        [
            # Mnemonic
            "ZOL_SEEK",
            # Sources
            "~".join([
                generate_instr_access_imm(),
                generate_instr_access_imm()
            ]),
            # Exe
            asm_utils.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

####################################################################

def generate_instr_access_fetch(ctx, program_context):
    if   ctx.access_imm():
        return generate_instr_access_imm()
    elif ctx.access_get():
        return generate_instr_access_get(ctx.access_get(), program_context)
    elif ctx.access_reg():
        return generate_instr_access_reg(ctx.access_reg(), program_context)
    elif ctx.access_ram():
        return generate_instr_access_ram(ctx.access_ram(), program_context)
    elif ctx.access_rom_a():
        return generate_instr_access_rom_a(ctx.access_rom_a(), program_context)
    elif ctx.access_rom_b():
        return generate_instr_access_rom_b(ctx.access_rom_b(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def generate_instr_access_store(ctx, program_context):
    if   ctx.access_put():
        return generate_instr_access_put(ctx.access_put(), program_context)
    elif ctx.access_reg():
        return generate_instr_access_reg(ctx.access_reg(), program_context)
    elif ctx.access_ram():
        return generate_instr_access_ram(ctx.access_ram(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )


def generate_instr_access_imm():
    return "'".join(
        [
            # Mem
            "IMM",
            # Addr
            generate_instr_addr_literal(),
            # Mods
            "@".join( sorted( [] ) ),
        ]
    )

def generate_instr_access_get(ctx, program_context):

    mods = [ ]

    if ctx.advance_mod != None:
        advance_mod = asm_utils.token_to_text(ctx.advance_mod)
        # Remove default NO_ADV, if given
        if advance_mod != "NO_ADV":
            mods.append(asm_utils.token_to_text(ctx.advance_mod))

    return "'".join(
        [
            # Mem
            "GET",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted(mods) ),
        ]
    )

def generate_instr_access_put(ctx, program_context):
    return "'".join(
        [
            # Mem
            "PUT",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted( [] ) ),
        ]
    )

def generate_instr_access_reg(ctx, program_context):

    # Get all given mods
    mods = [ ]

    return "'".join(
        [
            # Mem
            "REG",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted( mods ) ),
        ]
    )

def generate_instr_access_ram(ctx, program_context):
    # Get all given mods
    mods = [ ]

    return "'".join(
        [
            # Mem
            "RAM",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted( mods ) ),
        ]
    )

def generate_instr_access_rom_a(ctx, program_context):
    # Get all given mods
    mods = [ ]

    return "'".join(
        [
            # Mem
            "ROM_A",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted( mods ) ),
        ]
    )

def generate_instr_access_rom_b(ctx, program_context):
    # Get all given mods
    mods = [ ]

    return "'".join(
        [
            # Mem
            "ROM_B",
            # Addr
            generate_instr_addr(ctx.addr(), program_context),
            # Mods
            "@".join( sorted( mods ) ),
        ]
    )


####################################################################

def generate_instr_addr(ctx, program_context):
    if   ctx.addr_literal():
        return generate_instr_addr_literal()
    elif ctx.addr_bam():
        return generate_instr_addr_bam(ctx.addr_bam(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                asm_utils.ctx_start(ctx),
            )
        )

def generate_instr_addr_literal():
    rtnStr = ";".join(
        [
            # Com
            "ID",
            # Port
            str(generate_instr_addr_literal.port),
            # Mods
            ":".join( sorted( [ ] ) )
        ]
    )
    generate_instr_addr_literal.port += 1
    return rtnStr

def generate_instr_addr_bam(ctx, program_context):
    mods = []

    if ctx.step_mod != None:
        mods.append(asm_utils.token_to_text(ctx.step_mod))

    return ";".join(
        [
            # Com
            asm_utils.get_component_addr(ctx, program_context),
            # Port
            "0",
            # Mods
            ":".join(
                sorted( mods )
            )
        ]
    )
