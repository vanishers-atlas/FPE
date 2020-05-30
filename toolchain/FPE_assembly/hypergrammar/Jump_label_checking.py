# Generated from FPE_assembly.g4 by ANTLR 4.7.2
from antlr4 import *

from ..utils.error_reporting import ctx_start
from ..grammar.FPE_assemblyParser import FPE_assemblyParser as parser

class extractor(ParseTreeListener):

    def __init__(this):
        this.declared_labels = {}
        this.referanced_labels = {}

    def final_check(this):
        # Check every referanced label is declared
        for label in this.referanced_labels.keys():
            if label not in this.declared_labels:
                raise SyntaxError(
                    "ERROR: Jump label, %s, referanced but never declared. Refernaced %s\n"%
                    (
                        label,
                        ", ".join(
                            [
                                ctx_start(ctx)
                                for ctx in this.referanced_labels[label]
                            ]
                        ),
                    )
                )


    def enterJump_label(this, ctx):
        label = ctx.IDENTIFER().getText()

        # Handle jump label declarations
        if type(ctx.parentCtx) == parser.State_jump_labelContext:
            # Check for multiple declarations of a label
            if label in this.declared_labels.keys():
                raise SyntaxError(
                    "ERROR: Multiple declarations of jump label, %s, at %s and  %s\n"%
                    (
                        label,
                        ctx_start(this.declared_labels[label]),
                        ctx_start(ctx.parentCtx),
                    )
                )
            else:
                this.declared_labels[label] = ctx.parentCtx
        # Handle jump label referance
        elif type(ctx.parentCtx) == parser.Op_pc_jumpContext:
            try:
                this.referanced_labels[label].append(ctx)
            except KeyError:
                this.referanced_labels[label] = [ctx]
        # Flag unsupported usage
        else:
            raise NotImplementedError(
                "jump label ctx with unsupported parent, %s"%(
                    type(ctx.parentCtx),
                )
            )
