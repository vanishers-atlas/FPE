# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils
####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context

        # Create a blank para_file
        this.rollcall = {
            "signal_padding" : None,

            "external_stall" : None,
            "report_stall" : None,

            "SIMD" : {
                "lanes" : None,
                "force_lanes" : False,
            },

            "program_flow" : {
            },

            "instr_decoder"  : { },

            "address_sources" : { },

            "data_memories" : { },

            "execute_units" : { },
        }

    def return_findings(this):
        return this.rollcall

    #################################################################################

    def enterOp_bam(this, ctx):
        BAM = asm_utils.get_component_op(ctx, this.program_context)[0]
        # Ensure BAM exists
        if BAM not in this.rollcall["address_sources"]:
            this.rollcall["address_sources"][BAM] = {}

        # Ensure required para_file are in ALU
        if "offset_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["step_max"] = None

    #################################################################################

    def enterOp_alu(this, ctx):
        ALU = asm_utils.get_component_op(ctx, this.program_context)
        assert len(ALU) == 1
        ALU = ALU[0]
        # Ensure ALU exists
        if ALU not in this.rollcall["execute_units"]:
            this.rollcall["execute_units"][ALU] = {}

        # Ensure required para_file are in ALU
        if "data_width" not in this.rollcall["execute_units"][ALU]:
            this.rollcall["execute_units"][ALU]["data_width" ] = None

    #################################################################################

    def enterAccess_fetch(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        this.handle_fetch(mem)

    def enterBap_fetch(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        this.handle_fetch(mem)

    def enterAccess_store(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        this.handle_store(mem)

    def enterAccess_store(this, ctx):
        mem = asm_utils.get_component_access(ctx, this.program_context)
        this.handle_store(mem)

    def handle_fetch(this, mem):
        if mem == "IMM":
            pass
        elif mem in ["GET", "PUT"]:
            this.comm_handling(mem)
        elif mem in ["ROM_A", "ROM_B", "RAM", "REG"]:
            this.basic_mem_handling(mem)
        else:
            raise ValueError("Unknown mem used in fatch access, " + str(mem))

    def handle_store(this, mem):
        if mem in ["PUT"]:
            this.comm_handling(mem)
        elif mem in ["RAM", "REG"]:
            this.basic_mem_handling(mem)
        else:
            raise ValueError("Unknown mem used in store access, " + str(mem))

    def comm_handling(this, mem):
        # Ensure mem is declared in config
        if mem not in this.rollcall["data_memories"]:
            this.rollcall["data_memories"][mem] = { "cross_lane" : False }

        # Ensure required para_file are in mem
        if "data_width" not in this.rollcall["data_memories"][mem]:
            this.rollcall["data_memories"][mem]["data_width"] = None
        if "FIFOs" not in this.rollcall["data_memories"][mem]:
            this.rollcall["data_memories"][mem]["FIFOs"] = None
        if "FIFO_handshakes" not in this.rollcall["data_memories"][mem]:
            this.rollcall["data_memories"][mem]["FIFO_handshakes"] = None

    def basic_mem_handling(this, mem):
        # Ensure mem is declared in config
        if mem not in this.rollcall["data_memories"]:
            this.rollcall["data_memories"][mem] = { "cross_lane" : False }

        # Handle ROM and RAM type parameter
        if mem in ["ROM_A", "ROM_B", "RAM"]:
            if "type" not in this.rollcall["data_memories"][mem]:
                this.rollcall["data_memories"][mem]["type"] = None

        # Ensure required para_file are in mem
        if "data_width" not in this.rollcall["data_memories"][mem]:
            this.rollcall["data_memories"][mem]["data_width" ] = None
        if "depth" not in this.rollcall["data_memories"][mem]:
            this.rollcall["data_memories"][mem]["depth" ] = None

    #################################################################################

    def enterAddr_bam(this, ctx):
        BAM = asm_utils.get_component_addr(ctx, this.program_context)
        # Ensure BAM exists
        if BAM not in this.rollcall["address_sources"]:
            this.rollcall["address_sources"][BAM] = {}

        # Ensure required para_file are in ALU
        if "offset_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["offset_max"] = None
        if "addr_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["addr_max"] = None
        if "step_max" not in this.rollcall["address_sources"][BAM]:
            this.rollcall["address_sources"][BAM]["step_max"] = None

    #################################################################################

    def enterState_zol(this, ctx):
        this.rollcall["program_flow"]["hidden_ZOLs"] = {}

        this.rollcall["program_flow"]["hidden_ZOLs"]["tracker_type"] = None
        this.rollcall["program_flow"]["hidden_ZOLs"]["pune_single_iteration"] = None

    def enterState_rep(this, ctx):
        this.rollcall["program_flow"]["rep_bank"] = {}

        this.rollcall["program_flow"]["rep_bank"]["subtype"] = None
        this.rollcall["program_flow"]["rep_bank"]["stall_on_id_change"] = None
