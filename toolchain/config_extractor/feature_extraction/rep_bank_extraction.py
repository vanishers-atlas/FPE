# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

import warnings

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils


####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config

        this.open_loops = []

        assert "program_flow" in this.config.keys()
        if "rep_bank" not in this.config["program_flow"].keys():
            # This extractor isn't required so skip setup
            # As no rep statements in the program not processing should happen
            return

        this.config["program_flow"]["rep_bank"]["loops"] = []

    def get_updated_config(this):
        return this.config

    def enterState_rep(this, ctx):
        overwrites = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        loop_id = len(this.config["program_flow"]["rep_bank"]["loops"])
        this.open_loops.append(loop_id)
        this.config["program_flow"]["rep_bank"]["loops"].append(
            {
                "overwrites" : overwrites,
            }
        )
