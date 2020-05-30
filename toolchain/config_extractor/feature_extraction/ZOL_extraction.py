from antlr4 import *

# import FPE assembly handling module
from ... import FPE_assembly as FPEA

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.config["program_fetch"]["ZOLs"] = []

    def get_updated_config(this):
        return this.config


    def enterState_zol(this, ctx):
        this.config["program_fetch"]["ZOLs"].append(FPEA.evaluate_expr(ctx.expr(), this.program_context))
