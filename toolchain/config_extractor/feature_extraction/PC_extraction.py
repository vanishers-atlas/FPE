from antlr4 import *

# import FPE assembly handling module
from ... import FPE_assembly as FPEA

# import toolchain utils for computing widths
from ... import utils as tc_utils

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.PC = 0

    def get_updated_config(this):
        this.config["program_fetch"]["program_length"] = this.PC
        this.config["program_fetch"]["addr_width"] = tc_utils.unsigned.width(this.config["program_fetch"]["program_length"] - 1)
        return this.config


    def enterOperation(this, ctx):
        this.PC += 1
