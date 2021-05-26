# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config

    def get_updated_config(this):
        for addr in this.config["address_sources"].values():
            try:
                addr["steps"] = sorted(list(addr["steps"]))
            except Exception:
                addr["steps"] = []

        return this.config


    def enterOp_bam_seek(this, ctx):
        BAM = asm_utils.get_component_op(ctx, this.program_context)

        # Defualt to FORWARD
        if ctx.step_mod == None:
            step_mod = "FORWARD"
        else:
            step_mod = asm_utils.token_to_text(ctx.step_mod)

        # Record fetched direction signal
        if step_mod == "FORWARD":
            try:
                this.config["address_sources"][BAM]["steps"].add("fetched_forward")
            except KeyError:
                this.config["address_sources"][BAM]["steps"] = set(["fetched_forward",])
        elif step_mod == "BACKWARD":
            try:
                this.config["address_sources"][BAM]["steps"].add("fetched_backward")
            except KeyError:
                this.config["address_sources"][BAM]["steps"] = set(["fetched_backward",])
        else:
            raise NotImplementedError("unknown mod, %s"%(step_mod))


    def enterAddr_bam(this, ctx):
        BAM = asm_utils.get_component_addr(ctx, this.program_context)

        # Defualt to FORWARD
        if ctx.step_mod == None:
            step_mod = "FORWARD"
        else:
            step_mod = asm_utils.token_to_text(ctx.step_mod)

        # Record fetched direction signal
        if step_mod == "FORWARD":
            try:
                this.config["address_sources"][BAM]["steps"].add("generic_forward")
            except KeyError:
                this.config["address_sources"][BAM]["steps"] = set(["generic_forward",])
        elif step_mod == "BACKWARD":
            try:
                this.config["address_sources"][BAM]["steps"].add("generic_backward")
            except KeyError:
                this.config["address_sources"][BAM]["steps"] = set(["generic_backward",])
        else:
            raise NotImplementedError("unknown mod, %s"%(step_mod))
