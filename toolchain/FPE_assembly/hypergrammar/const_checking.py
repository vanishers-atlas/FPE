# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.declared_consts = {}

    def final_check(this):
        pass


    # Checking on exit not enter to exclude definations using themselves in their const_expr
    def exitState_constant(this, ctx):
        const = ctx.IDENTIFER().getText()

        # Check for multiple declarations of a label
        if const in this.declared_consts.keys():
            raise SyntaxError(
                "ERROR: Multiple declarations of const, %s, at %s and %s\n"%
                (
                    const,
                    asm_utils.ctx_start(this.declared_consts[const]),
                    asm_utils.ctx_start(ctx),
                )
            )
        else:
            this.declared_consts[const] = ctx


    def enterExpr_operand(this, ctx):
        if ctx.IDENTIFER() != None:
            const = ctx.IDENTIFER().getText()
            if const not in this.declared_consts.keys():
                raise SyntaxError(
                    "ERROR: Referancing undeclared const, %s, at %s\n"%
                    (
                        const,
                        asm_utils.ctx_start(ctx),
                    )
                )
