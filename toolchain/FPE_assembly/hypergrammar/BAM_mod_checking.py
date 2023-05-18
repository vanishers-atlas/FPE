############################################################################
# A hyper grammar extractor used to check all identiers an operation is
# accessed from are already declared as a component
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

import warnings
from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.BAM_mods = {}

    def final_check(this):
        for bam, mods in this.BAM_mods.items():
            if "step_solo" not in mods and "step_multi" not in mods:
                raise warnings.warn("WARNING: Bam is never stepped, consider replacing with an adrr literal or expression, BAM %s\n"%(bam, ) )
            if "step_solo" in mods and "step_multi" in mods:
                raise SyntaxError("ERROR: Bam cannot using both step_solo and step_multi mods, BAM %s\n"%(bam, ) )


    def enterAddr_bam(this, ctx):
        this.current_BAM = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        dir_mod = False
        step_mod = False
        base_mod = False
        for mod_ctx in ctx.addr_bam_mod():
            if   mod_ctx.addr_bam_dir_mod():
                # Check for multiple use of the single use mod
                if dir_mod:
                    raise SyntaxError("ERROR: BAM addr can only use the step_solo mod once per access, referenced at %s\n"%(asm_utils.ctx_start(ctx), ) )
                else:
                    dir_mod = True
            elif mod_ctx.addr_bam_size_mod():
                # Check for multiple use of the single use mod
                if step_mod:
                    raise SyntaxError("ERROR: BAM addr can only use the step_solo mod once per access, referenced at %s\n"%(asm_utils.ctx_start(ctx), ) )
                else:
                    step_mod = True

            elif mod_ctx.addr_bam_base_mod():
                # Check for multiple use of the single use mod
                if base_mod:
                    raise SyntaxError("ERROR: BAM addr can only use the base_multi mod once per access, referenced at %s\n"%(asm_utils.ctx_start(ctx), ) )
                else:
                    base_mod = True
            else:
                raise ValueError("mod_ctx with unknown subrule at line "%(asm_utils.ctx_start(mod_ctx), ) )
