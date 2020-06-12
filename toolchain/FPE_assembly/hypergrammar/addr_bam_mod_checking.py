# Generated from FPE_assembly.g4 by ANTLR 4.7.2
from antlr4 import *

from ..interface.error_reporting import ctx_start
from ..grammar.FPE_assemblyParser import FPE_assemblyParser as parser


class extractor(ParseTreeListener):

    def __init__(this):
        pass


    def final_check(this):
        pass


    def enterAddr_bam(this, ctx):
        this.enclosing_ctx = ctx
        this.mods = []

    def enterAddr_bam_mod(this, ctx):
        mod = ctx.getText()

        # Handle signel use flag mods
        if mod in ["FORWARD", "BACKWARD"]:
            # Check for repeats
            if mod in this.mods:
                raise SyntaxError(
                    "ERROR: Multiple occurances of a single use mod, %s, in access from %s to %s"%
                    (
                        mod,
                        ctx_start(this.enclosing_ctx),
                        ctx_end  (this.enclosing_ctx),
                    )
                )


            # Check for signed, unsigned mutual exclusion
            exclusions = {
                "FORWARD" : set(
                    [
                        "BACKWARD"
                    ]
                ),
                "BACKWARD" : set(
                    [
                        "FORWARD"
                    ]
                ),
            }
            overlap = set(this.mods) & exclusions[mod]
            if overlap != set():
                raise SyntaxError(
                    "ERROE: $s excludes mod(s) already used in BAM SEEK operation from %s to %s"%
                    (
                        mod,
                        ctx_start(this.enclosing_ctx),
                        ctx_end  (this.enclosing_ctx),
                    )
                )
        else:
            raise NotImplementedError("unknown mod, " + mod)
