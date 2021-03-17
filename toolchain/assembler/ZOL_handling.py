# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context, encoding):
        this.program_context = program_context
        this.count_encoding = encoding
        this.PC = 0
        this.ZOLs = {}
        this.ZOL_stack = []
        this.ZOL_id = 0

    def get_output(this):
        return this.ZOLs

    def enterState_zol(this, ctx):
        ZOL_name = "bound_ZOL_%i"%(this.ZOL_id, )
        this.ZOL_id += 1

        this.ZOL_stack.append(ZOL_name)
        this.ZOLs[this.ZOL_stack[-1]] = {
            "start" : this.PC,
            "end"   : None,
        }

        if   this.count_encoding[ZOL_name]["type"] == "biased_tally":
            this.ZOLs[this.ZOL_stack[-1]]["count"] = "\"%s\""%(
                tc_utils.biased_tally.encode(
                    asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1,
                    this.count_encoding[this.ZOL_stack[-1]]["tallies"],
                    this.count_encoding[this.ZOL_stack[-1]]["bais" ],
                    this.count_encoding[this.ZOL_stack[-1]]["range"]
                ),
            )
        elif this.count_encoding[ZOL_name]["type"] == "unsigned":
            this.ZOLs[this.ZOL_stack[-1]]["count"] = "\"%s\""%(
                tc_utils.unsigned.encode(
                    asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1,
                    this.count_encoding[this.ZOL_stack[-1]]["bits"],
                ),
            )
        else:
            raise ValueError("Unknown ZOL type, " + str(this.count_encoding[ZOL_name]["type"]))

    def exitState_zol(this, ctx):
        this.ZOLs[this.ZOL_stack[-1]]["end"] = this.PC - 1
        this.ZOL_stack = this.ZOL_stack[:-1]


    def enterOperation(this, ctx):
        this.PC += 1
