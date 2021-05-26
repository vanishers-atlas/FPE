############################################################################
# A hyper grammar extractor used to check all identiers declared within an
# FPE program are unique
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this):
        this.declared_identiers = {}

    def final_check(this):
        pass

    def enterIdent_dec(this, ctx):
        identier = asm_utils.token_to_text(ctx.IDENTIFER())

        # If first declaration of identier, store in case of second declaration
        if identier not in this.declared_identiers.keys():
            this.declared_identiers[identier] = ctx
        # If second declaration of identier, report error and exit
        else:
            raise SyntaxError( "Multiple declatation of the same identier, %s, at %s and %s\n"%(
                    identier,
                    asm_utils.ctx_start(this.declared_identiers[identier]),
                    asm_utils.ctx_start(ctx)
                )
            )
