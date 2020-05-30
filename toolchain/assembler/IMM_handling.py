from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.IMM = set()
        for pc_value in program_context["label_pc_map"].values():
            this.IMM.add(pc_value)

    def get_output(this):
        return {a : v for a, v in enumerate(this.IMM)}, {v : a for a, v in enumerate(this.IMM)}

    def enterAccess_imm(this, ctx):
        imm_value = FPEA.evaluate_expr(ctx.expr(), this.program_context)

        # Add Imm value to Imm mem
        this.IMM.add(imm_value)
