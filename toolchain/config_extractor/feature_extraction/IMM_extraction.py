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
        this.values = set()
        this.data_width = 0

    def get_updated_config(this):
        if len(this.values):
            this.config["data_memories"]["IMM"] = {}
            this.config["data_memories"]["IMM"]["depth"] = len(this.values)
            this.config["data_memories"]["IMM"]["data_width"] = this.data_width
            this.config["data_memories"]["IMM"]["addr_width"] = tc_utils.unsigned.width(this.config["data_memories"]["IMM"]["depth"] - 1)
        elif len(this.values) != 0:
            raise ValueError("Immedate values found but no IMM declared within config")
        return this.config


    def enterOp_pc_jump(this, ctx):
        this.values.add(ctx.jump_label().IDENTIFER().getText())
        this.data_width = max(
            [
                this.config["program_fetch"]["addr_width"],
                this.data_width,
            ]
        )

    def enterAccess_imm(this, ctx):
        value = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        # Check that value can be encoded in data width
        if value < 0:
            this.data_width = max(
                [
                    tc_utils.twos_comp.width(value),
                    this.data_width,
                ]
            )
        else:
            this.data_width = max(
                [
                    tc_utils.unsigned.width(value),
                    this.data_width,
                ]
            )

        this.values.add(value)
