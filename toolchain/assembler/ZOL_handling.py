from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA
from .. import utils  as tc_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context, encoding):
        this.program_context = program_context
        this.encoding = encoding
        this.PC = 0
        this.ZOLs = {}
        this.curr_ZOL = []

    def get_output(this):
        return this.ZOLs


    def enterState_zol(this, ctx):
        this.curr_ZOL.append(len(this.ZOLs))
        this.ZOLs[this.curr_ZOL[-1]] = {
            "start" : this.PC,
            "end"   : None,
            "tally" : "\"%s\""%(
                tc_utils.biased_tally.encode(
                    FPEA.evaluate_expr(ctx.expr(), this.program_context) - 1,
                    this.encoding[this.curr_ZOL[-1]]["width"],
                    this.encoding[this.curr_ZOL[-1]]["bais" ],
                    this.encoding[this.curr_ZOL[-1]]["range"]
                ),
            )
        }

    def exitState_zol(this, ctx):
        this.ZOLs[this.curr_ZOL[-1]]["end"] = this.PC - 1
        this.curr_ZOL = this.curr_ZOL[:-1]


    def enterOperation(this, ctx):
        this.PC += 1
