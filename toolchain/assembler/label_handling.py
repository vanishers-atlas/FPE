from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA
from ..FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

####################################################################

class handler(ParseTreeListener):

    def __init__(this):
        this.PC = 0
        this.declared_labels = {}
        this.referanced_labels = set()

    def get_output(this):
        LUT = {}
        for label in this.referanced_labels:
            LUT[label] = this.declared_labels[label]
        return LUT


    def enterOperation(this, ctx):
        this.PC += 1

    def enterJump_label(this, ctx):
        label = ctx.IDENTIFER().getText()

        # Handle jump label declarations
        if type(ctx.parentCtx) == parser.State_jump_labelContext:
            this.declared_labels[label] = this.PC
        # Handle jump label referance
        elif type(ctx.parentCtx) == parser.Op_pc_jumpContext:
            this.referanced_labels.add(label)
        # Flag unsupported usage
        else:
            raise NotImplementedError(
                "jump label ctx with unsupported parent, %s"%(
                    type(ctx.parentCtx),
                )
            )
