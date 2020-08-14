# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain import utils  as tc_utils

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
