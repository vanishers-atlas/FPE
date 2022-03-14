# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

import itertools as it

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
            if asm_utils.instr_mnemonic(op_id).upper() == "NOP"
        ]
        if filler != []:
            filler = filler[0] << sum(this.config["instr_decoder"]["addr_widths"])
        else:
            filler = 0

        # Record the end of the program
        program_end = len(this.program) - 1

        # Fill unused space at the end of the PM with filler opcode
        while len(this.program) < this.config["program_flow"]["program_length"]:
            this.program.append(filler)

        return program_end, this.program


    def enterOperation(this, ctx):
        this.addresses = []

    def exitOperation(this, ctx):
        instr = this.config["instr_set"][asm_utils.generate_instr(ctx, this.program_context)]
        for addr, slot_width in zip(
            it.chain(this.addresses, it.repeat(0)),
            this.config["instr_decoder"]["addr_widths"]
        ):
            instr <<= slot_width
            instr += addr

        this.program.append(instr)

    def enterOp_pc_only_jump(this, ctx):
        imm_addr = this.program_context["IMM_addr_map"][ this.program_context["jump_labels"][asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())] ]
        this.addresses.append(imm_addr)

    def enterOp_pc_alu_jump(this, ctx):
        imm_addr = this.program_context["IMM_addr_map"][ this.program_context["jump_labels"][asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())] ]
        this.addresses.append(imm_addr)


    def enterOp_ZOL_seek(this, ctx):
        values = this.program_context["loop_labels"][asm_utils.token_to_text(ctx.loop_label.IDENTIFER())]
        start_imm_addr = this.program_context["IMM_addr_map"][values["start"]]
        end_imm_addr   = this.program_context["IMM_addr_map"][values["end"]]
        this.addresses.append(start_imm_addr)
        this.addresses.append(end_imm_addr)

    def enterAccess_imm(this, ctx):
        imm_addr = this.program_context["IMM_addr_map"][
            asm_utils.evaluate_expr(ctx.expr(), this.program_context)
        ]
        this.addresses.append(imm_addr)


    def enterAddr_literal(this, ctx):
        this.addresses.append(asm_utils.evaluate_expr(ctx.expr(), this.program_context))
