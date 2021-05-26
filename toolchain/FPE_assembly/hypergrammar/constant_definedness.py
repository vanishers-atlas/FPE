############################################################################
# A hyper grammar extractor used to check all identiers referenced as part
# of an expr within an FPE program are already declared as a constant
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this):
        this.declared_identiers = []

    def final_check(this):
        pass

    def exitState_constant(this, ctx):
        identier = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())
        this.declared_identiers.append(identier)

    def enterExpr_operand(this, ctx):
        if ctx.ident_ref() != None:
            identier = asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())
            if identier not in this.declared_identiers:
                raise SyntaxError(
                    "ERROR: Undeclared constant, %s, referenced at %s\n"%
                    (
                        identier,
                        asm_utils.ctx_start(ctx)
                    )
                )
