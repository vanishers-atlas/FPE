# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.IMM = set()
        for pc_value in program_context["label_pc_map"].values():
            this.IMM.add(pc_value)

    def get_output(this):
        return {
            a : v
            for a, v in enumerate(this.IMM)
        }

    def enterAccess_imm(this, ctx):
        imm_value = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        # Add Imm value to Imm mem
        this.IMM.add(imm_value)
