import antlr4

from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

from FPE.toolchain.FPE_assembly.interface import error_reporting
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
                "NOP",
                "~".join([]),
                get_component.get_component_op(ctx, program_context),
                "~".join([]),
                "~".join( sorted( [] ) ),
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
                token_handling.token_to_text(ctx.op_pc_jump().mnemonic),
                "~".join([
                    generate_instr_access_imm(),
                ]),
                get_component.get_component_op(ctx, program_context),
                "~".join([]),
                "~".join( sorted( [] ) ),
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
            "RESET",
            "~".join([]),
            get_component.get_component_op(ctx, program_context),
            "~".join([]),
            "~".join( sorted( [] ) ),
        ]
    )

def generate_instr_op_bam_seek(ctx, program_context):
    generate_instr_addr_literal.port = 0

    # Get all mods
    mods = set([mod.getText() for mod in ctx.op_bam_seek_mod()])
    # include default mods it not already over
    if not any([mod == "BACKWARD" for mod in mods]):
        mods.add("FORWARD")

    return "#".join(
        [

            "SEEK",
            generate_instr_access(ctx.access_fetch(), program_context),
            get_component.get_component_op(ctx, program_context),
            "~".join([]),
            "~".join( sorted( mods ) ),
        ]
    )

####################################################################

def generate_instr_op_alu(ctx, program_context):
    if   ctx.op_alu_1f_1s() != None:
        return generate_instr_op_alu_1f_1s(ctx.op_alu_1f_1s(), program_context)
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
            token_handling.token_to_text(ctx.mnemonic),
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_fetch_alu(), program_context)
                ]
            ),
            get_component.get_component_op(ctx, program_context),
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_store_alu(), program_context)
                ]
            ),
            "~".join( sorted( [] ) ),
        ]
    )

def generate_instr_op_alu_2f_0s(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            token_handling.token_to_text(ctx.mnemonic),
            "~".join(
                [
                    generate_instr_access_alu(access_ctx, program_context)
                    for access_ctx in ctx.access_fetch_alu()
                ]
            ),
            get_component.get_component_op(ctx, program_context),
            "~".join([]),
            "~".join( sorted( [] ) ),
        ]
    )

def generate_instr_op_alu_2f_1s(ctx, program_context):
    generate_instr_addr_literal.port = 0
    return "#".join(
        [
            token_handling.token_to_text(ctx.mnemonic),
            "~".join(
                [
                    generate_instr_access_alu(access_ctx, program_context)
                    for access_ctx in ctx.access_fetch_alu()
                ]
            ),
            get_component.get_component_op(ctx, program_context),
            "~".join(
                [
                    generate_instr_access_alu(ctx.access_store_alu(), program_context)
                ]
            ),
            "~".join( sorted( [] ) ),
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
            "IMM",
            generate_instr_addr_literal(),
            "@".join( sorted( [] ) ),
        ]
    )

def generate_instr_access_get(ctx, program_context):
    return "'".join(
        [
            "GET",
            generate_instr_addr(ctx.addr(), program_context),
            "@".join(
                sorted(
                    [
                        mod.getText().upper()
                        for mod in ctx.access_get_mod()
                        # skip default 'mods'
                        if mod.getText().upper() not in ['NO_ADV']
                    ]
                )
            ),
        ]
    )

def generate_instr_access_put(ctx, program_context):
    return "'".join(
        [
            "PUT",
            generate_instr_addr(ctx.addr(), program_context),
            "@".join( sorted( [] ) ),
        ]
    )

def generate_instr_access_reg(ctx, program_context):
    return "'".join(
        [
            "REG",
            generate_instr_addr(ctx.addr(), program_context),
            "@".join( sorted( [] ) ),
        ]
    )

def generate_instr_access_ram(ctx, program_context):
    return "'".join(
        [
            "RAM",
            generate_instr_addr(ctx.addr(), program_context),
            "@".join( sorted( [] ) ),
        ]
    )


def generate_instr_access_rom(ctx, program_context):
    return "'".join(
        [
            "ROM",
            generate_instr_addr(ctx.addr(), program_context),
            "@".join([]),
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
            "ID",
            str(generate_instr_addr_literal.port),
            ":".join( sorted( [ ] ) )
        ]
    )
    generate_instr_addr_literal.port += 1
    return rtnStr

def generate_instr_addr_bam(ctx, program_context):
    return ";".join(
        [
            get_component.get_component_addr(ctx, program_context),
            "",
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
