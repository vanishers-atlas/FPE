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
        count = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

        # Handke ZOL type schemes
        # Always ripple (old scheme)
        if   this.config["program_flow"]["ZOL_type_scheme"].lower() == "ripple":
            this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                "type"  : "ripple",
                "count" : count
            }
        # Always cascade
        elif this.config["program_flow"]["ZOL_type_scheme"].lower() == "cascade":
            this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                "type"  : "cascade",
                "count" : count
            }
        # dynamical select maybe ripple and cascade based on count
        elif this.config["program_flow"]["ZOL_type_scheme"].lower() == "dynamic":
            if count < 64:
                this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                    "type"  : "ripple",
                    "count" : count
                }
            else:
                this.config["program_flow"]["ZOLs"]["bound_ZOL_%i"%(this.ZOL_id, )] = {
                    "type"  : "cascade",
                    "count" : count
                }
        # unknown type scheme
        else:
            raise ValueError("unknown ZOL_type_scheme. " + str(this.config["program_flow"]["ZOL_type_scheme"]) )

        this.ZOL_id += 1
