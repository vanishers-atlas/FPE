# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils
####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context

        # Create a blank para_file
        this.para_file = {
            "signal_padding" : None,

            "SIMD" : {
                "lanes" : None,
            },

            "program_flow" : {
                "ZOLs" : { },
            },

            "instr_decoder"  : { },

            "address_sources" : { },

            "data_memories" : { },

            "execute_units" : { },
        }
        this.para_context = {
            "ZOLs" : { },
        }

    def return_findings(this):
        return this.para_file, this.para_context

    #################################################################################

    def enterState_component(this, ctx):
        com_type = asm_utils.token_to_text(ctx.com_type)

        if   com_type == "ZOL_ripple":
            this.state_component_ZOL_ripple(ctx)
        elif com_type == "ZOL_cascade":
            this.state_component_ZOL_cascade(ctx)
        elif com_type == "ZOL_counter":
            this.state_component_ZOL_counter(ctx)
        else:
            raise ValueError("Unknown Component type, %s, at %s"%(
                com_type,
                asm_utils.ctx_start(ctx)
            ) )


    def state_component_ZOL_ripple(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        this.para_context["ZOLs"][com_name] = {
            "iterations" : "int",
            "seekable" : "bool",
        }

    def state_component_ZOL_cascade(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        this.para_context["ZOLs"][com_name] = {
            "iterations" : "int",
            "seekable" : "bool",
        }

    def state_component_ZOL_counter(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        this.para_context["ZOLs"][com_name] = {
            "iterations" : "int",
            "seekable" : "bool",
            "settable" : "bool",
        }

    #################################################################################

    def enterOp_bam(this, ctx):
        BAM = asm_utils.get_component_op(ctx, this.program_context)
        # Ensure BAM exists
        if BAM not in this.para_file["address_sources"]:
            this.para_file["address_sources"][BAM] = {}

        # Ensure required para_file are in ALU
        if "offset_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["step_max"] = None

    #################################################################################

    def enterOp_alu(this, ctx):
        ALU = asm_utils.get_component_op(ctx, this.program_context)
        # Ensure ALU exists
        if ALU not in this.para_file["execute_units"]:
            this.para_file["execute_units"][ALU] = {}

        # Ensure required para_file are in ALU
        if "data_width" not in this.para_file["execute_units"][ALU]:
            this.para_file["execute_units"][ALU]["data_width" ] = None

    #################################################################################

    def enterAccess_fetch(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)

        if mem == "IMM":
            this.IMM_handling(mem)
        elif mem in ["GET", "PUT"]:
            this.comm_handling(mem)
        elif mem in ["ROM_A", "ROM_B", "RAM", "REG"]:
            this.basic_mem_handling(mem)
        else:
            raise ValueError("Unknown mem used in fatch access, " + str(mem))

    def enterAccess_store(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)

        if mem in ["PUT"]:
            this.comm_handling(mem)
        elif mem in ["RAM", "REG"]:
            this.basic_mem_handling(mem)
        else:
            raise ValueError("Unknown mem used in store access, " + str(mem))


    def IMM_handling(this, mem):
        # Ensure mem is declared in config
        if mem not in this.para_file["data_memories"]:
            this.para_file["data_memories"][mem] = {}

    def comm_handling(this, mem):
        # Ensure mem is declared in config
        if mem not in this.para_file["data_memories"]:
            this.para_file["data_memories"][mem] = {}

        # Ensure required para_file are in mem
        if "data_width" not in this.para_file["data_memories"][mem]:
            this.para_file["data_memories"][mem]["data_width"] = None
        if "FIFOs" not in this.para_file["data_memories"][mem]:
            this.para_file["data_memories"][mem]["FIFOs"] = None
        if "FIFO_handshakes" not in this.para_file["data_memories"][mem]:
            this.para_file["data_memories"][mem]["FIFO_handshakes"] = None

    def basic_mem_handling(this, mem):
        # Ensure mem is declared in config
        if mem not in this.para_file["data_memories"]:
            this.para_file["data_memories"][mem] = {}

        # Ensure required para_file are in mem
        if "data_width" not in this.para_file["data_memories"][mem]:
            this.para_file["data_memories"][mem]["data_width" ] = None
        if "depth" not in this.para_file["data_memories"][mem]:
            this.para_file["data_memories"][mem]["depth" ] = None

    #################################################################################

    def enterAddr_bam(this, ctx):
        BAM = asm_utils.get_component_addr(ctx, this.program_context)
        # Ensure BAM exists
        if BAM not in this.para_file["address_sources"]:
            this.para_file["address_sources"][BAM] = {}

        # Ensure required para_file are in ALU
        if "offset_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.para_file["address_sources"][BAM]:
            this.para_file["address_sources"][BAM]["step_max"] = None

    #################################################################################

    def enterState_zol(this, ctx):
        this.para_file["program_flow"]["bound_ZOL_tracker_type"] = "dynamic"
