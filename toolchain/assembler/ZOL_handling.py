# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context, iterations_encodings):
        this.program_context = program_context
        this.iterations_encodings = iterations_encodings
        this.PC = 0
        this.ZOLs = {}
        this.ZOL_stack = []
        this.ZOL_id = 0

    def get_output(this):
        return this.ZOLs

    def enterState_zol(this, ctx):
        ZOL_name = "bound_ZOL_%i"%(this.ZOL_id, )
        this.ZOL_id += 1

        interations = asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1
        if   this.iterations_encodings[ZOL_name]["type"] == "biased_tally":
            iterations_encoded = '"' + tc_utils.biased_tally.encode(
                interations,
                this.iterations_encodings[ZOL_name]["tallies"],
                this.iterations_encodings[ZOL_name]["bias"],
                this.iterations_encodings[ZOL_name]["range"]
            ) + '"'
        elif this.iterations_encodings[ZOL_name]["type"] == "unsigned":
            iterations_encoded = '"' + tc_utils.unsigned.encode(
                interations,
                this.iterations_encodings[ZOL_name]["width"]
            ) + '"'
        else:
            raise ValueError("unknown encoding type, " + this.iterations_encodings[ZOL_name]["type"])

        this.ZOL_stack.append(ZOL_name)
        this.ZOLs[this.ZOL_stack[-1]] = {
            "start" : this.PC,
            "end"   : None,
            "iterations" : iterations_encoded,
        }

    def exitState_zol(this, ctx):
        this.ZOLs[this.ZOL_stack[-1]]["end"] = this.PC - 1
        this.ZOL_stack = this.ZOL_stack[:-1]


    def enterOperation(this, ctx):
        this.PC += 1
