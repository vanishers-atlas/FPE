# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

from FPE.toolchain.FPE_assembly.utils.error_reporting import ctx_start
from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

class extractor(ParseTreeListener):

    def __init__(this):
        pass


    def final_check(this):
        pass


    def enterConst_expr(this, ctx):
        pass

    def exitConst_expr(this, ctx):
        pass


    def enterConstant(this, ctx):
        pass

    def exitConstant(this, ctx):
        pass


    def enterScope(this, ctx):
        pass

    def exitScope(this, ctx):
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
        pass

    def exitImm_access(this, ctx):
        pass


    def enterGet_access(this, ctx):
        pass

    def exitGet_access(this, ctx):
        pass


    def enterGet_access_mod(this, ctx):
        pass

    def exitGet_access_mod(this, ctx):
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


    def enterId_addr(this, ctx):
        pass

    def exitId_addr(this, ctx):
        pass


    def enterBam_addr(this, ctx):
        pass

    def exitBam_addr(this, ctx):
        pass


    def enterBam_addr_mod(this, ctx):
        pass

    def exitBam_addr_mod(this, ctx):
        pass


    def enterStatement(this, ctx):
        pass

    def exitStatement(this, ctx):
        pass


    def enterZol_statement(this, ctx):
        pass

    def exitZol_statement(this, ctx):
        pass


    def enterJump_target_def(this, ctx):
        pass

    def exitJump_target_def(this, ctx):
        pass


    def enterConstant_def(this, ctx):
        pass

    def exitConstant_def(this, ctx):
        pass


    def enterOperation(this, ctx):
        pass

    def exitOperation(this, ctx):
        pass


    def enterVoid_op(this, ctx):
        pass

    def exitVoid_op(this, ctx):
        pass


    def enterNop(this, ctx):
        pass

    def exitNop(this, ctx):
        pass


    def enterPc_op(this, ctx):
        pass

    def exitPc_op(this, ctx):
        pass


    def enterUncon_jump(this, ctx):
        pass

    def exitUncon_jump(this, ctx):
        pass


    def enterCon_jump(this, ctx):
        pass

    def exitCon_jump(this, ctx):
        pass


    def enterJump_target(this, ctx):
        pass

    def exitJump_target(this, ctx):
        pass


    def enterBam_op(this, ctx):
        pass

    def exitBam_op(this, ctx):
        pass


    def enterBam_reset(this, ctx):
        pass

    def exitBam_reset(this, ctx):
        pass


    def enterBam_seek(this, ctx):
        pass

    def exitBam_seek(this, ctx):
        pass


    def enterBam_seek_mod(this, ctx):
        pass

    def exitBam_seek_mod(this, ctx):
        pass


    def enterAlu_op(this, ctx):
        pass

    def exitAlu_op(this, ctx):
        pass


    def enterAlu_1f_1s(this, ctx):
        pass

    def exitAlu_1f_1s(this, ctx):
        pass


    def enterAlu_2f_0s(this, ctx):
        pass

    def exitAlu_2f_0s(this, ctx):
        pass


    def enterAlu_2f_1s(this, ctx):
        pass

    def exitAlu_2f_1s(this, ctx):
        pass


    def enterAlu_fetch(this, ctx):
        pass

    def exitAlu_fetch(this, ctx):
        pass


    def enterAlu_store(this, ctx):
        pass

    def exitAlu_store(this, ctx):
        pass
