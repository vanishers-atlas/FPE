# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context


    def final_check(this):
        pass


    def enterOp_bam_seek(this, ctx):
        this.enclosing_ctx = ctx
        this.mods = []

    def enterOp_bam_seek_mod(this, ctx):
        mod = ctx.getText()

        # Handle signel use flag mods
        if mod in ["FORWARD", "BACKWARD"]:
            # Check for repeats
            if mod in this.mods:
                raise SyntaxError(
                    "ERROR: Multiple occurances of a single use mod, %s, in access from %s to %s"%
                    (
                        mod,
                        asm_utils.ctx_start(this.enclosing_ctx),
                        asm_utils.ctx_end  (this.enclosing_ctx),
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
                        asm_utils.ctx_start(this.enclosing_ctx),
                        asm_utils.ctx_end  (this.enclosing_ctx),
                    )
                )
        else:
            raise NotImplementedError("unknown mod, " + mod)
