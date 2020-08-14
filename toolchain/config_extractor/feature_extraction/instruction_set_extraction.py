# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain import utils  as tc_utils

####################################################################

class extractor(ParseTreeListener):
    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.config["instruction_decoder"]["addr_widths"] = {}

        this.instr_set = set()

    def get_updated_config(this):
        this.config["instr_set"] = {}

        this.config["instruction_decoder"]["opcode_width"] = 0
        for opcode, op_id in enumerate(sorted(this.instr_set)):
            this.config["instr_set"][op_id] = opcode
            this.config["instruction_decoder"]["opcode_width"] = max(
                [
                    tc_utils.unsigned.width(opcode),
                    this.config["instruction_decoder"]["opcode_width"],
                ]
            )

        return this.config


    def enterOperation(this, ctx):
        instr = asm_utils.generate_instr(ctx, this.program_context)
        this.instr_set.add(instr)
        this.addr_literals = 0


    def enterOp_pc_jump(this, ctx):
        this.enterAddr_literal(ctx, mem="IMM")

    def enterAccess_imm(this, ctx):
        this.enterAddr_literal(ctx, mem="IMM")

    def enterAddr_literal(this, ctx, mem=None):
        if mem == None:
            mem = asm_utils.get_component_access(ctx, this.program_context)
        try:
            this.config["instruction_decoder"]["addr_widths"]["addr_%i"%(this.addr_literals)] = max(
                [
                    this.config["instruction_decoder"]["addr_widths"]["addr_%i"%(this.addr_literals)],
                    this.config["data_memories"][mem]["addr_width"]
                ]
            )
        except KeyError:
            this.config["instruction_decoder"]["addr_widths"]["addr_%i"%(this.addr_literals)] = this.config["data_memories"][mem]["addr_width"]
        this.addr_literals += 1
