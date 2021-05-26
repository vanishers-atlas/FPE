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
        if len(this.values) > 0:
            this.config["data_memories"]["IMM"] = {}
            this.config["data_memories"]["IMM"]["depth"] = len(this.values)
            this.config["data_memories"]["IMM"]["data_width"] = this.data_width
            this.config["data_memories"]["IMM"]["addr_width"] = tc_utils.unsigned.width(this.config["data_memories"]["IMM"]["depth"] - 1)
        return this.config


    def enterOp_pc_jump(this, ctx):
        jump_label = asm_utils.token_to_text(ctx.ident_ref().IDENTIFER())
        
        this.values.add(this.program_context["jump_labels"][jump_label])

        this.data_width = max(
            [
                this.config["program_flow"]["PC_width"],
                this.data_width,
            ]
        )

    def enterOp_ZOL_seek(this, ctx):
        loop_label = asm_utils.token_to_text(ctx.loop_label.IDENTIFER())

        this.values.add(this.program_context["loop_labels"][loop_label]["start"])
        this.values.add(this.program_context["loop_labels"][loop_label]["end"])

        this.data_width = max(
            [
                this.config["program_flow"]["PC_width"],
                this.data_width,
            ]
        )

    def enterAccess_imm(this, ctx):
        value = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        # Check that value can be encoded in data width
        if this.config["signal_padding"] == "unsigned":
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
        elif this.config["signal_padding"] == "signed":
            this.data_width = max(
                [
                    tc_utils.twos_comp.width(value),
                    this.data_width,
                ]
            )

        this.values.add(value)
