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
        this.ZOL_id = 0
        this.finished_ZOLs = {}
        this.unfinished_ZOLs = []

    def get_output(this):
        assert(len(this.unfinished_ZOLs) == 0)
        return this.finished_ZOLs

    def enterState_zol(this, ctx):
        ZOL_name = "bound_ZOL_%i"%(this.ZOL_id, )
        this.ZOL_id += 1

        overwrites = asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1

        # Check for specail case of a single iteretion
        overwrite_to_PC = overwrites == 0

        # Overwrite overwrites for specail case of a single iteretion.
        # Any encodeable value would work, but used 1 makes testing and debug simpler.
        # as both the overwrite and fallthrough behavour can be seen quickly
        if  overwrite_to_PC:
            overwrites = 1

        # Work out encoded value of overwrite based of ZOL type
        if this.iterations_encodings[ZOL_name]["type"] == "biased_tally":
            overwrites_encoded = '"' + tc_utils.biased_tally.encode(
                overwrites,
                this.iterations_encodings[ZOL_name]["tallies"],
                this.iterations_encodings[ZOL_name]["bias"],
                this.iterations_encodings[ZOL_name]["range"]
            ) + '"'
        elif this.iterations_encodings[ZOL_name]["type"] == "unsigned":
            overwrites_encoded = '"' + tc_utils.unsigned.encode(
                overwrites,
                this.iterations_encodings[ZOL_name]["width"]
            ) + '"'
        else:
            raise ValueError("unknown encoding type, " + this.iterations_encodings[ZOL_name]["type"])

        # Handle specail case of a single iteretion
        # marking the PC overwrite value to be set to the instruction just after the loop
        if  overwrite_to_PC:
            this.unfinished_ZOLs.append((
                ZOL_name,
                {
                    "start" : None,
                    "end"   : None,
                    "iterations" : overwrites_encoded,
                },
            ))
        # Handle general case
        # Setting the PC overwrite value to current PC, ie the PC of the first instruction of the loop
        else:
            this.unfinished_ZOLs.append((
                ZOL_name,
                {
                    "start" : this.PC,
                    "end"   : None,
                    "iterations" : overwrites_encoded,
                },
            ))

    def exitState_zol(this, ctx):
        ZOL_name, ZOL_details = this.unfinished_ZOLs.pop()

        # Set marked PC overwrite values to the current PC, ie the first instruction after the loop
        if ZOL_details["start"] == None:
            ZOL_details["start"] = this.PC

        # Set the end value to the loop, to PC - 1, ie the last instruction in the loop
        # - 1 as this.PC is incremented on entering an operation
        ZOL_details["end"] = this.PC - 1

        this.finished_ZOLs[ZOL_name] = ZOL_details


    def enterOperation(this, ctx):
        this.PC += 1
