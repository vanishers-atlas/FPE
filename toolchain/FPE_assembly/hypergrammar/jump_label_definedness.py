############################################################################
# A hyper grammar extractor used to check all identiers jumped to within an
# FPE program are declared somewhere within the program as a jump label
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this):
        this.declared_identiers = []
        this.referenced_identiers = {}

    def final_check(this):
        for identier, locations in this.referenced_identiers.items():
            if identier not in this.declared_identiers:
                raise SyntaxError(
                    "ERROR: Jump label, %s, referanced but never declared. Referenced %s\n"%
                    (
                        identier,
                        ", ".join(
                            [
                                asm_utils.ctx_start(ctx)
                                for ctx in this.referenced_identiers[identier]
                            ]
                        ),
                    )
                )

    def enterState_jump_label(this, ctx):
        identier = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())
        this.declared_identiers.append(identier)

    def enterOp_pc_jump(this, ctx):
        identier = asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())

        if identier not in this.referenced_identiers.keys():
            this.referenced_identiers[identier] = []

        this.referenced_identiers[identier].append(ctx)
