# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils


####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.config["program_fetch"]["ZOLs"] = []

    def get_updated_config(this):
        return this.config


    def enterState_zol(this, ctx):
        this.config["program_fetch"]["ZOLs"].append(asm_utils.evaluate_expr(ctx.expr(), this.program_context))
