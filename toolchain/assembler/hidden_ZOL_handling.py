# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context, overwrites_encoding):
        this.program_context = program_context
        this.overwrites_encoding = overwrites_encoding

        this.PC = 0
        this.loop_id = 0
        this.skip_ends = 0
        this.finished_loops = {}
        this.unfinished_loops = []

    def get_output(this):
        assert(len(this.unfinished_loops) == 0)
        return this.finished_loops

    def enterState_zol(this, ctx):
        loop_name = "hidden_ZOL_%i"%(this.loop_id, )
        this.loop_id += 1

        if loop_name not in this.overwrites_encoding.keys():
            return

        overwrites = asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1

        # Check for specail case of a single iteretion
        overwrite_to_PC = overwrites == 0

        # Overwrite overwrites for specail case of a single iteretion.
        # Any encodeable value would work, but used 1 makes testing and debug simpler.
        # as both the overwrite and fallthrough behavour can be seen quickly
        if  overwrite_to_PC:
            overwrites = 1

        # Work out encoded value of overwrite based of ZOL type
        if this.overwrites_encoding[loop_name]["type"] == "biased_tally":
            overwrites_encoded = tc_utils.biased_tally.encode(
                overwrites,
                this.overwrites_encoding[loop_name]["tallies"],
                this.overwrites_encoding[loop_name]["bias"],
                this.overwrites_encoding[loop_name]["range"]
            )
        elif this.overwrites_encoding[loop_name]["type"] == "unsigned":
            overwrites_encoded = tc_utils.unsigned.encode(
                overwrites,
                this.overwrites_encoding[loop_name]["width"]
            )
        else:
            raise ValueError("unknown encoding type, " + this.overwrites_encoding[loop_name]["type"])

        # Handle specail case of a single iteretion
        # marking the PC overwrite value to be set to the instruction just after the loop
        if  overwrite_to_PC:
            this.unfinished_loops.append((
                loop_name,
                {
                    "overwrite_value" : None,
                    "check_value"   : None,
                    "overwrites" : overwrites_encoded,
                },
            ))
        # Handle general case
        # Setting the PC overwrite value to current PC, ie the PC of the first instruction of the loop
        else:
            this.unfinished_loops.append((
                loop_name,
                {
                    "overwrite_value" : this.PC,
                    "check_value"   : None,
                    "overwrites" : overwrites_encoded,
                },
            ))

    def exitState_zol(this, ctx):

        if len(this.unfinished_loops) == 0 or this.unfinished_loops[-1][0] not in this.overwrites_encoding.keys():
            return

        loop_name, loop_details = this.unfinished_loops.pop()

        # Set marked PC overwrite values to the current PC, ie the first instruction after the loop
        if loop_details["overwrite_value"] == None:
            loop_details["overwrite_value"] = this.PC

        # Set the end value to the loop, to PC - 1, ie the last instruction in the loop
        # - 1 as this.PC is incremented on entering an operation
        loop_details["check_value"] = this.PC - 1

        this.finished_loops[loop_name] = loop_details


    def enterOperation(this, ctx):
        this.PC += 1
