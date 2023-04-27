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

        this.loop_id = 0

        assert "program_flow" in this.config.keys()
        if "hidden_ZOLs" not in this.config["program_flow"].keys():
            # This extractor isn't required so skip setup
            # As no ZOl statements in the program not processing should happen
            return

        assert "tracker_type" in this.config["program_flow"]["hidden_ZOLs"].keys()
        assert type(this.config["program_flow"]["hidden_ZOLs"]["tracker_type"]) == str
        assert this.config["program_flow"]["hidden_ZOLs"]["tracker_type"].lower() in ["ripple", "cascade", "dynamic", "counter", ]
        this.tracker_type = this.config["program_flow"]["hidden_ZOLs"]["tracker_type"].lower()

        assert "pune_single_iteration" in this.config["program_flow"]["hidden_ZOLs"].keys()
        assert type(this.config["program_flow"]["hidden_ZOLs"]["pune_single_iteration"]) == bool
        this.pune_singles = this.config["program_flow"]["hidden_ZOLs"]["pune_single_iteration"]

        this.config["program_flow"]["hidden_ZOLs"] = {}

    def get_updated_config(this):
        return this.config

    def enterState_zol(this, ctx):
        overwrites = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        if not (this.pune_singles and overwrites == 1):
            # Always ripple
            if   this.tracker_type == "ripple":
                this.config["program_flow"]["hidden_ZOLs"][this.loop_id] = {
                    "tracker_type" : "ripple",
                    "overwrites"  : overwrites,
                    "seekable"     : False,
                }
            # Always cascade
            elif this.tracker_type == "cascade":
                this.config["program_flow"]["hidden_ZOLs"][this.loop_id] = {
                    "tracker_type" : "cascade",
                    "overwrites"  : overwrites,
                    "seekable"     : False,
                }
            # dynamical select maybe ripple and cascade based on overwrites
            elif this.tracker_type == "dynamic":
                if overwrites < 64:
                    this.config["program_flow"]["hidden_ZOLs"][this.loop_id] = {
                        "tracker_type" : "ripple",
                        "overwrites"  : overwrites,
                        "seekable"     : False,
                    }
                else:
                    this.config["program_flow"]["hidden_ZOLs"][this.loop_id] = {
                        "tracker_type" : "cascade",
                        "overwrites"  : overwrites,
                        "seekable"     : False,
                    }
            elif this.tracker_type == "counter":
                this.config["program_flow"]["hidden_ZOLs"][this.loop_id] = {
                    "tracker_type" : "counter",
                    "overwrites"   : overwrites,
                    "seekable"     : False,
                    "settable"     : False,
                }
            # unknown type scheme
            else:
                raise ValueError("unknown ZOL hardware subtype. " + str(tracker_type) )

        this.loop_id += 1
