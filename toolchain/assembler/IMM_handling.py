# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.values = set()

    def get_output(this):
        return {
            a : v
            for a, v in enumerate(this.values)
        }

    def enterOp_ZOL_seek(this, ctx):
        loop_label = asm_utils.token_to_text(ctx.loop_label.IDENTIFER())

        this.values.add(this.program_context["loop_labels"][loop_label]["start"])
        this.values.add(this.program_context["loop_labels"][loop_label]["end"])

    def enterOp_pc_jump(this, ctx):
        jump_label = asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())

        this.values.add(this.program_context["jump_labels"][jump_label])




    def enterAccess_imm(this, ctx):
        value = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        this.values.add(value)
