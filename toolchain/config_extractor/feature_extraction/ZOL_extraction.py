# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils


####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.ZOL_id = 0

    def get_updated_config(this):
        return this.config


    def enterState_zol(this, ctx):
        interations = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        # Handke ZOL type schemes
        # Always ripple (old scheme)
        if   this.config["program_flow"]["bound_ZOL_tracker_type"].lower() == "ripple":
            this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                "tracker_type" : "ripple",
                "iterations"  : interations,
                "seekable"     : False,
            }
        # Always cascade
        elif this.config["program_flow"]["bound_ZOL_tracker_type"].lower() == "cascade":
            this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                "tracker_type" : "cascade",
                "iterations"  : interations,
                "seekable"     : False,
            }
        # dynamical select maybe ripple and cascade based on interations
        elif this.config["program_flow"]["bound_ZOL_tracker_type"].lower() == "dynamic":
            if interations < 64:
                this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                    "tracker_type" : "ripple",
                    "iterations"  : interations,
                    "seekable"     : False,
                }
            else:
                this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                    "tracker_type" : "cascade",
                    "iterations"  : interations,
                    "seekable"     : False,
                }
        elif this.config["program_flow"]["bound_ZOL_tracker_type"].lower() == "counter":
            this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                "tracker_type" : "counter",
                "iterations"   : interations,
                "seekable"     : False,
                "settable"     : False,
            }

        # unknown type scheme
        else:
            raise ValueError("unknown ZOL_type_scheme. " + str(this.config["program_flow"]["bound_ZOL_tracker_type"]) )

        this.ZOL_id += 1
