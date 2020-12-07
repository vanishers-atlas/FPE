import antlr4

from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

from FPE.toolchain.FPE_assembly.interface import error_reporting
from FPE.toolchain.FPE_assembly.interface import evaluate_expr
from FPE.toolchain.FPE_assembly.interface import get_component
from FPE.toolchain.FPE_assembly.interface import token_handling

def generate_instr(ctx, program_context):
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
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    error_reporting.ctx_start(ctx)
                )
            )

####################################################################

def generate_instr_op_void(ctx, program_context):
    generate_instr_addr_literal.port = 0
    if ctx.op_void_nop():
        return "#".join(
            [
                # Mnemonic
                "NOP",
                # Sources
                "~".join([]),
                # Exe
                get_component.get_component_op(ctx, program_context),
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
                    error_reporting.ctx_start(ctx)
                )
            )

####################################################################

def generate_instr_op_pc(ctx, program_context):
    generate_instr_addr_literal.port = 0
    if ctx.op_pc_jump():
        return "#".join(
            [
                # Mnemonic
                token_handling.token_to_text(ctx.op_pc_jump().mnemonic),
                # Sources
                "~".join(
                    [
                        generate_instr_access_imm(),
                    ]
                ),
                # Exe
                get_component.get_component_op(ctx, program_context),
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
                    error_reporting.ctx_start(ctx)
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
                    error_reporting.ctx_start(ctx)
                )
            )

def generate_instr_op_bam_reset(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            # Mnemonic
            "BAM_RESET",
            # Sources
            "~".join([]),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_bam_seek(ctx, program_context):
    generate_instr_addr_literal.port = 0

    # Get all mods
    mods = [mod.getText() for mod in ctx.op_bam_seek_mod()]

    # include "FORWARD" as default direction if one is not given
    if "BACKWARD" not in mods and "FORWARD" not in mods:
        mods.append("FORWARD")

    return "#".join(
        [
            # Mnemonic
            "BAM_SEEK",
            # Sources
            generate_instr_access(ctx.access_fetch(), program_context),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted(mods))
        ]
    )

####################################################################

def generate_instr_op_alu(ctx, program_context):
    if   ctx.op_alu_1f_1s() != None:
        return generate_instr_op_alu_1f_1s(ctx.op_alu_1f_1s(), program_context)
    elif ctx.op_alu_shifts() != None:
        return generate_instr_op_alu_shifts(ctx.op_alu_shifts(), program_context)
    elif ctx.op_alu_2f_0s() != None:
        return generate_instr_op_alu_2f_0s(ctx.op_alu_2f_0s(), program_context)
    elif ctx.op_alu_2f_1s() != None:
        return generate_instr_op_alu_2f_1s(ctx.op_alu_2f_1s(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
                (
                    type(ctx),
                    error_reporting.ctx_start(ctx)
                )
            )

def generate_instr_op_alu_1f_1s(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            # Mnemonic
            token_handling.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_fetch_alu(), program_context)
                ]
            ),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_store_alu(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_alu_shifts(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            # Mnemonic
            "%s_%s"%(
                token_handling.token_to_text(ctx.mnemonic),
                evaluate_expr(ctx.expr(), program_context)
            ),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_fetch_alu(), program_context)
                ]
            ),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_store_alu(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_alu_2f_0s(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            # Mnemonic
            token_handling.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu(access_ctx, program_context)
                    for access_ctx in ctx.access_fetch_alu()
                ]
            ),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join([]),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_op_alu_2f_1s(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            # Mnemonic
            token_handling.token_to_text(ctx.mnemonic),
            # Sources
            "~".join(
                [
                    generate_instr_access_alu(access_ctx, program_context)
                    for access_ctx in ctx.access_fetch_alu()
                ]
            ),
            # Exe
            get_component.get_component_op(ctx, program_context),
            # Dests
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_store_alu(), program_context)
                ]
            ),
            # Mods
            "~".join(sorted([]))
        ]
    )

def generate_instr_access_alu(ctx, program_context):

    if   hasattr(ctx, "access_fetch") and ctx.access_fetch():
        return generate_instr_access(ctx.access_fetch(), program_context)
    elif hasattr(ctx, "access_store") and ctx.access_store():
        return generate_instr_access(ctx.access_store(), program_context)
    # Check for ACC tegister
    elif str(ctx.children[0]) == "ACC":
        return "ACC"
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                error_reporting.ctx_start(ctx),
            )
        )


####################################################################

def generate_instr_access(ctx, program_context):
    if   hasattr(ctx, "access_imm") and ctx.access_imm():
        return generate_instr_access_imm()
    elif hasattr(ctx, "access_get") and ctx.access_get():
        return generate_instr_access_get(ctx.access_get(), program_context)
    elif hasattr(ctx, "access_put") and ctx.access_put():
        return generate_instr_access_put(ctx.access_put(), program_context)
    elif hasattr(ctx, "access_reg") and ctx.access_reg():
        return generate_instr_access_reg(ctx.access_reg(), program_context)
    elif hasattr(ctx, "access_ram") and ctx.access_ram():
        return generate_instr_access_ram(ctx.access_ram(), program_context)
    elif hasattr(ctx, "access_rom") and ctx.access_rom():
        return generate_instr_access_rom(ctx.access_rom(), program_context)
    else:
        raise NotImplementedError(
            "%s without a supported subrule at %s"%
            (
                type(ctx),
                error_reporting.ctx_start(ctx),
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
    # Get all given mods
    mods = [
        mod.getText().upper()
        for mod in ctx.access_get_mod()
    ]

    # Add default NO_ADV, if neither NO_ADV nor ADV is given
    if "NO_ADV" not in mods and "ADV" not in mods:
        mods.append("NO_ADV")

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

    # Handle speacil syntax for block access mod
    block_size = 1
    if ctx.expr() != None:
        block_size = evaluate_expr(ctx.expr(), program_context)
    mods.append("block_size;%i"%(block_size,))

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

    # Handle speacil syntax for block access mod
    block_size = 1
    if ctx.expr() != None:
        block_size = evaluate_expr(ctx.expr(), program_context)
    mods.append("block_size;%i"%(block_size,))

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

def generate_instr_access_rom(ctx, program_context):
    # Get all given mods
    mods = [ ]

    # Handle speacil syntax for block access mod
    block_size = 1
    if ctx.expr() != None:
        block_size = evaluate_expr(ctx.expr(), program_context)
    mods.append("block_size;%i"%(block_size,))

    return "'".join(
        [
            # Mem
            "ROM",
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
                error_reporting.ctx_start(ctx),
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
    return ";".join(
        [
            # Com
            get_component.get_component_addr(ctx, program_context),
            # Port
            "0",
            # Mods
            ":".join(
                sorted(
                    [
                        mod.getText()
                        for mod in ctx.addr_bam_mod()
                    ]
                )
            )
        ]
    )
