from antlr4 import *

# import FPE assembly handling module
from ... import FPE_assembly as FPEA

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
        BAM = FPEA.get_component_op(ctx, this.program_context)

        # Record fetched firection signal
        for mod in [mod.getText().upper() for mod in ctx.op_bam_seek_mod()]:
            if mod == "FORWARD":
                try:
                    this.config["address_sources"][BAM]["steps"].add("fetched_forward")
                except KeyError:
                    this.config["address_sources"][BAM]["steps"]= set(["fetched_forward",])
            elif mod == "BACKWARD":
                try:
                    this.config["address_sources"][FPEA.get_component_op(ctx, this.program_context)]["steps"].add("fetched_backward")
                except KeyError:
                    this.config["address_sources"][FPEA.get_component_op(ctx, this.program_context)]["steps"]= set(["fetched_backward",])
            else:
                raise NotImplementedError("unknown mod, %s"%(mod))
        # Check fort defaulting to forward
        if not any(
            [
                mod.getText().upper() == "BACKWARD"
                for mod in ctx.op_bam_seek_mod()
            ]
        ):
            try:
                this.config["address_sources"][BAM]["steps"].add("fetched_forward")
            except KeyError:
                this.config["address_sources"][BAM]["steps"]= set(["fetched_forward",])

    def enterAddr_bam(this, ctx):
        BAM = FPEA.get_component_addr(ctx, this.program_context)
        # Record fetched firection signal
        for mod in [mod.getText().upper() for mod in ctx.addr_bam_mod()]:
            if mod == "FORWARD":
                try:
                    this.config["address_sources"][BAM]["steps"].add("generic_forward")
                except KeyError:
                    this.config["address_sources"][BAM]["steps"]= set(["generic_forward",])
            elif mod == "BACKWARD":
                try:
                    this.config["address_sources"][FPEA.get_component(ctx)]["steps"].add("generic_backward")
                except KeyError:
                    this.config["address_sources"][FPEA.get_component(ctx)]["steps"]= set(["generic_backward",])
            else:
                raise NotImplementedError("unknown mod, %s"%(mod))
