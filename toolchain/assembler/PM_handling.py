from antlr4 import *

import itertools as it

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

####################################################################

class handler(ParseTreeListener):
    def __init__(this, config, program_context):
        this.config = config
        this.program_context = program_context
        this.program = []

    def get_output(this):
        # Determine filler opcode
        filler = [
            op_value
            for op_id, op_value in this.config["instr_set"].items()
            if FPEA.instr_mnemonic(op_id).upper() == "NOP"
        ]
        if filler != []:
            filler = filler[0] << sum(this.config["instruction_decoder"]["addr_widths"].values())
        else:
            filler = 0

        # Record the end of the program
        program_end = len(this.program) - 1

        # Fill unused space at the end of the PM with filler opcode
        while len(this.program) < this.config["program_fetch"]["program_length"]:
            this.program.append(filler)

        return program_end, this.program


    def enterOperation(this, ctx):
        this.addresses = []

    def exitOperation(this, ctx):
        instr = this.config["instr_set"][FPEA.generate_instr(ctx, this.program_context)]
        for addr, (k, width) in zip(
            it.chain(this.addresses, it.repeat(0)),
            sorted(
                this.config["instruction_decoder"]["addr_widths"].items(),
                 key=lambda kv: kv[0]
            )
        ):
            instr <<= width
            instr += addr

        this.program.append(instr)

    def enterOp_pc_jump(this, ctx):
        imm_addr = this.program_context["IMM_addr_map"][ this.program_context["label_pc_map"][ctx.jump_label().getText()] ]
        this.addresses.append(imm_addr)


    def enterAccess_imm(this, ctx):
        imm_addr = this.program_context["IMM_addr_map"][
            FPEA.evaluate_expr(ctx.expr(), this.program_context)
        ]
        this.addresses.append(imm_addr)


    def enterAddr_literal(this, ctx):
        this.addresses.append(FPEA.evaluate_expr(ctx.expr(), this.program_context))
