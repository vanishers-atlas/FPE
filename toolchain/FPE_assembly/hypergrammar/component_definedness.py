############################################################################
# A hyper grammar extractor used to check all identiers an operation is
# accessed from are already declared as a component
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

    def enterState_component(this, ctx):
        identier = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        this.declared_identiers.append(identier)


    def enterOp_component(this, ctx):
        identier = asm_utils.token_to_text(ctx.children[0].children[0].exe_com.IDENTIFER())

        if identier not in this.declared_identiers:
            raise SyntaxError(
                "ERROR: Undeclared compounent, %s, referenced at %s\n"%
                (
                    identier,
                    asm_utils.ctx_start(ctx)
                )
            )
