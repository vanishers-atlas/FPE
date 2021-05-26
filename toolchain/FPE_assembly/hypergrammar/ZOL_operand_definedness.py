############################################################################
# A hyper grammar extractor used to check all identiers an operation is
# accessed from are already declared as a component
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context

    def final_check(this):
        pass


    def enterOp_ZOL(this, ctx):
        exe_com = asm_utils.token_to_text(ctx.children[0].exe_com.IDENTIFER())
        assert(exe_com in this.program_context["components"]["ZOLs"].keys())

    def enterOp_ZOL_seek(this, ctx):
        loop_label = asm_utils.token_to_text(ctx.loop_label.IDENTIFER())
        assert(loop_label in this.program_context["loop_labels"])

        exe_com = asm_utils.token_to_text(ctx.exe_com.IDENTIFER())
        try:
            if this.program_context["components"]["ZOLs"][exe_com]["parameters"]["seekable"].lower() != "true":
                raise SyntaxError("%s can't be seeked as parameter seekable isn't true"%(
                    exe_com
                ))
        except AttributeError:
            raise SyntaxError("%s can't be seeked as parameter seekable has to be a boolen true"%(
                exe_com
            ))
        except KeyError:
            raise SyntaxError("%s can't be seeked as parameter seekable is missing, to seek it must be true"%(
                exe_com
            ))

    def enterOp_ZOL_set(this, ctx):
        exe_com = asm_utils.token_to_text(ctx.exe_com.IDENTIFER())
        try:
            if this.program_context["components"]["ZOLs"][exe_com]["parameters"]["settable"].lower() != "true":
                raise SyntaxError("%s can't be set as parameter settable isn't true"%(
                    exe_com
                ))
        except AttributeError:
            raise SyntaxError("%s can't be set as parameter settable has to be a boolen true"%(
                exe_com
            ))
        except KeyError:
            raise SyntaxError("%s can't be set as parameter settable is missing, to set it must be true"%(
                exe_com
            ))
