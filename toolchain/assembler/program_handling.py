from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

####################################################################

class handler(ParseTreeListener):
    def __init__(this, config, label_pc_map, IMM_addr_map):
        this.config = config
        this.label_pc_map = label_pc_map
        this.IMM_addr_map = IMM_addr_map
        this.program = []

    def get_output(this):
        # Determine filler opcode
        if "NOP###" in this.config["instr_set"]:
            this.config["instr_set"]["NOP###"] << (this.config["addr_width"] *this.config["fetch_decode"]["encoded_addrs"])
        else:
            filler = 0

        # Fill unused space at the end of the PM with filler opcode
        program_end = len(this.program) - 1
        while len(this.program) < this.config["fetch_decode"]["program_length"]:
            this.program.append(filler)

        return program_end, this.program


    def enterStatement(this, ctx):
        pass

    def exitStatement(this, ctx):
        pass


    def enterScope(this, ctx):
        pass

    def exitScope(this, ctx):
        pass


    def enterLabel(this, ctx):
        pass

    def exitLabel(this, ctx):
        pass


    def enterZol(this, ctx):
        pass

    def exitZol(this, ctx):
        pass


    def enterOperation(this, ctx):
        this.addresses = []

    def exitOperation(this, ctx):
        instr = this.config["instr_set"][FPEA.get_operation_id(ctx)]
        for i in range(this.config["fetch_decode"]["encoded_addrs"]):
            instr <<= this.config["addr_width"]
            if i < len(this.addresses):
                instr += this.addresses[i]

        this.program.append(instr)


    def enterVoid_operation(this, ctx):
        pass

    def exitVoid_operation(this, ctx):
        pass


    def enterVoid_0f_0s(this, ctx):
        pass

    def exitVoid_0f_0s(this, ctx):
        pass


    def enterVoid_0f_0s_mnemonic(this, ctx):
        pass

    def exitVoid_0f_0s_mnemonic(this, ctx):
        pass


    def enterPc_operation(this, ctx):
        pass

    def exitPc_operation(this, ctx):
        pass


    def enterPc_0f_0s(this, ctx):
        imm_addr = this.IMM_addr_map[this.label_pc_map[ctx.STRING().getText()]]
        this.addresses.append(imm_addr)

    def exitPc_0f_0s(this, ctx):
        pass


    def enterPc_0f_0s_mnemonic(this, ctx):
        pass

    def exitPc_0f_0s_mnemonic(this, ctx):
        pass


    def enterBam_operation(this, ctx):
        pass

    def exitBam_operation(this, ctx):
        pass


    def enterBam_0f_0s(this, ctx):
        pass

    def exitBam_0f_0s(this, ctx):
        pass


    def enterBam_0f_0s_mnemonic(this, ctx):
        pass

    def exitBam_0f_0s_mnemonic(this, ctx):
        pass


    def enterBam_1f_0s(this, ctx):
        pass

    def exitBam_1f_0s(this, ctx):
        pass


    def enterBam_1f_0s_mnemonic(this, ctx):
        pass

    def exitBam_1f_0s_mnemonic(this, ctx):
        pass


    def enterAlu_operation(this, ctx):
        pass

    def exitAlu_operation(this, ctx):
        pass


    def enterAlu_1f_1s(this, ctx):
        pass

    def exitAlu_1f_1s(this, ctx):
        pass


    def enterAlu_1f_1s_mnemonic(this, ctx):
        pass

    def exitAlu_1f_1s_mnemonic(this, ctx):
        pass


    def enterAlu_2f_0s(this, ctx):
        pass

    def exitAlu_2f_0s(this, ctx):
        pass


    def enterAlu_2f_0s_mnemonic(this, ctx):
        pass

    def exitAlu_2f_0s_mnemonic(this, ctx):
        pass


    def enterAlu_2f_1s(this, ctx):
        pass

    def exitAlu_2f_1s(this, ctx):
        pass


    def enterAlu_2f_1s_mnemonic(this, ctx):
        pass

    def exitAlu_2f_1s_mnemonic(this, ctx):
        pass


    def enterAlu_fetch(this, ctx):
        pass

    def exitAlu_fetch(this, ctx):
        pass


    def enterAlu_store(this, ctx):
        pass

    def exitAlu_store(this, ctx):
        pass


    def enterMem_fetch(this, ctx):
        pass

    def exitMem_fetch(this, ctx):
        pass


    def enterMem_store(this, ctx):
        pass

    def exitMem_store(this, ctx):
        pass


    def enterImm_access(this, ctx):
        imm_addr = this.IMM_addr_map[FPEA.decode_number_literal(ctx.NUMBER().getText())]
        this.addresses.append(imm_addr)


    def exitImm_access(this, ctx):
        pass


    def enterGet_access(this, ctx):
        pass

    def exitGet_access(this, ctx):
        pass


    def enterPut_access(this, ctx):
        pass

    def exitPut_access(this, ctx):
        pass


    def enterReg_access(this, ctx):
        pass

    def exitReg_access(this, ctx):
        pass


    def enterRam_access(this, ctx):
        pass

    def exitRam_access(this, ctx):
        pass


    def enterRom_access(this, ctx):
        pass

    def exitRom_access(this, ctx):
        pass


    def enterMem_addr(this, ctx):
        pass

    def exitMem_addr(this, ctx):
        pass


    def enterEncoded_addr(this, ctx):
        this.addresses.append(FPEA.decode_number_literal(ctx.NUMBER().getText()))

    def exitEncoded_addr(this, ctx):
        pass


    def enterBam_addr(this, ctx):
        pass

    def exitBam_addr(this, ctx):
        pass
