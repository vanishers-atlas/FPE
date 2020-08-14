# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context
        this.parameters = {
            "SIMD" : {
                "lanes" : None,
            },

            "program_fetch" : { },

            "instruction_decoder"  : { },

            "address_sources" : { },

            "data_memories" : { },

            "execute_units" : { },
        }

    def return_findings(this):
        return this.parameters


    def enterOp_bam(this, ctx):
        BAM = asm_utils.get_component_op(ctx, this.program_context)
        # Ensure BAM exists
        if BAM not in this.parameters["address_sources"]:
            this.parameters["address_sources"][BAM] = {}

        # Ensure required parameters are in ALU
        if "offset_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["step_max"] = None


    def enterOp_alu(this, ctx):
        ALU = asm_utils.get_component_op(ctx, this.program_context)
        # Ensure ALU exists
        if ALU not in this.parameters["execute_units"]:
            this.parameters["execute_units"][ALU] = {}

        # Ensure required parameters are in ALU
        if "data_width" not in this.parameters["execute_units"][ALU]:
            this.parameters["execute_units"][ALU]["data_width" ] = None


    def enterAccess_fetch(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        if mem != "IMM":
            # Ensure mem exists
            if mem not in this.parameters["data_memories"]:
                this.parameters["data_memories"][mem] = {}

            # Ensure required parameters are in mem
            if "data_width" not in this.parameters["data_memories"][mem]:
                this.parameters["data_memories"][mem]["data_width" ] = None
            if "depth" not in this.parameters["data_memories"][mem]:
                this.parameters["data_memories"][mem]["depth" ] = None

    def enterAccess_store(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        # Ensure mem exists
        if mem not in this.parameters["data_memories"]:
            this.parameters["data_memories"][mem] = {}

        # Ensure required parameters are in mem
        if "data_width" not in this.parameters["data_memories"][mem]:
            this.parameters["data_memories"][mem]["data_width" ] = None
        if "depth" not in this.parameters["data_memories"][mem]:
            this.parameters["data_memories"][mem]["depth" ] = None


    def enterAddr_bam(this, ctx):
        BAM = asm_utils.get_component_addr(ctx, this.program_context)
        # Ensure BAM exists
        if BAM not in this.parameters["address_sources"]:
            this.parameters["address_sources"][BAM] = {}

        # Ensure required parameters are in ALU
        if "offset_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.parameters["address_sources"][BAM]:
            this.parameters["address_sources"][BAM]["step_max"] = None
