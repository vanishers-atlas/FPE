# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

from FPE.toolchain.FPE_assembly.interface.error_reporting import ctx_start
from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

class extractor(ParseTreeListener):

    def __init__(this):
        pass

    def final_check(this):
        pass


    def enterAccess_get(this, ctx):
        this.enclosing_ctx = ctx
        this.mods = []


    def enterAccess_get_mod(this, ctx):
        mod = ctx.getText()
        # Handle signel use flag mods
        if mod in ["ADV"]:
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

            # Store valid mod
            this.mods.append(mod)
        else:
            raise NotImplementedError("Unknown mod encountered, %s"%(mod))
