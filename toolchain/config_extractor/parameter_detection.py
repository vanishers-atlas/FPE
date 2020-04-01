from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

####################################################################

class extractor(ParseTreeListener):

    def __init__(this):
        this.parameters = {
            "data_width" : None,

            "fetch_decode" : {},

            "address_sources" : { },

            "data_memories" : { },

            "execute_units" : { },
        }

    def return_findings(this):
        return this.parameters


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
        pass

    def exitOperation(this, ctx):
        pass


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
        pass

    def exitPc_0f_0s(this, ctx):
        pass


    def enterPc_0f_0s_mnemonic(this, ctx):
        pass

    def exitPc_0f_0s_mnemonic(this, ctx):
        pass


    def enterBam_operation(this, ctx):
        BAM = FPEA.get_component(ctx)
        this.parameters["address_sources"][BAM] = { }


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
        ALU = FPEA.get_component(ctx)
        this.parameters["execute_units"][ALU] = {}


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
        if ctx.imm_access() != None:
            this.parameters["data_memories"]["IMM"] = {}
        else:
            mem = FPEA.get_component(ctx)
            this.parameters["data_memories"][mem] = {
                "depth" : None
            }

    def exitMem_fetch(this, ctx):
        pass


    def enterMem_store(this, ctx):
        mem = FPEA.get_component(ctx)
        this.parameters["data_memories"][mem] = {
            "depth" : None
        }

    def exitMem_store(this, ctx):
        pass


    def enterImm_access(this, ctx):
        pass

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
        pass

    def exitEncoded_addr(this, ctx):
        pass


    def enterBam_addr(this, ctx):
        BAM = FPEA.get_component(ctx)
        this.parameters["address_sources"][BAM] = { }


    def exitBam_addr(this, ctx):
        pass
