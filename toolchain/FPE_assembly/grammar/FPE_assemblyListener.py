# Generated from ..\\grammar\\FPE_assembly.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FPE_assemblyParser import FPE_assemblyParser
else:
    from FPE_assemblyParser import FPE_assemblyParser

# This class defines a complete listener for a parse tree produced by FPE_assemblyParser.
class FPE_assemblyListener(ParseTreeListener):

    # Enter a parse tree produced by FPE_assemblyParser#statement.
    def enterStatement(self, ctx:FPE_assemblyParser.StatementContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#statement.
    def exitStatement(self, ctx:FPE_assemblyParser.StatementContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#scope.
    def enterScope(self, ctx:FPE_assemblyParser.ScopeContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#scope.
    def exitScope(self, ctx:FPE_assemblyParser.ScopeContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#label.
    def enterLabel(self, ctx:FPE_assemblyParser.LabelContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#label.
    def exitLabel(self, ctx:FPE_assemblyParser.LabelContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#zol.
    def enterZol(self, ctx:FPE_assemblyParser.ZolContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#zol.
    def exitZol(self, ctx:FPE_assemblyParser.ZolContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#operation.
    def enterOperation(self, ctx:FPE_assemblyParser.OperationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#operation.
    def exitOperation(self, ctx:FPE_assemblyParser.OperationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#void_operation.
    def enterVoid_operation(self, ctx:FPE_assemblyParser.Void_operationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#void_operation.
    def exitVoid_operation(self, ctx:FPE_assemblyParser.Void_operationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#void_0f_0s.
    def enterVoid_0f_0s(self, ctx:FPE_assemblyParser.Void_0f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#void_0f_0s.
    def exitVoid_0f_0s(self, ctx:FPE_assemblyParser.Void_0f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#void_0f_0s_mnemonic.
    def enterVoid_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Void_0f_0s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#void_0f_0s_mnemonic.
    def exitVoid_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Void_0f_0s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#pc_operation.
    def enterPc_operation(self, ctx:FPE_assemblyParser.Pc_operationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#pc_operation.
    def exitPc_operation(self, ctx:FPE_assemblyParser.Pc_operationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#pc_0f_0s.
    def enterPc_0f_0s(self, ctx:FPE_assemblyParser.Pc_0f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#pc_0f_0s.
    def exitPc_0f_0s(self, ctx:FPE_assemblyParser.Pc_0f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#pc_0f_0s_mnemonic.
    def enterPc_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Pc_0f_0s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#pc_0f_0s_mnemonic.
    def exitPc_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Pc_0f_0s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_operation.
    def enterBam_operation(self, ctx:FPE_assemblyParser.Bam_operationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_operation.
    def exitBam_operation(self, ctx:FPE_assemblyParser.Bam_operationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_0f_0s.
    def enterBam_0f_0s(self, ctx:FPE_assemblyParser.Bam_0f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_0f_0s.
    def exitBam_0f_0s(self, ctx:FPE_assemblyParser.Bam_0f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_0f_0s_mnemonic.
    def enterBam_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Bam_0f_0s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_0f_0s_mnemonic.
    def exitBam_0f_0s_mnemonic(self, ctx:FPE_assemblyParser.Bam_0f_0s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_1f_0s.
    def enterBam_1f_0s(self, ctx:FPE_assemblyParser.Bam_1f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_1f_0s.
    def exitBam_1f_0s(self, ctx:FPE_assemblyParser.Bam_1f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_1f_0s_mnemonic.
    def enterBam_1f_0s_mnemonic(self, ctx:FPE_assemblyParser.Bam_1f_0s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_1f_0s_mnemonic.
    def exitBam_1f_0s_mnemonic(self, ctx:FPE_assemblyParser.Bam_1f_0s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_operation.
    def enterAlu_operation(self, ctx:FPE_assemblyParser.Alu_operationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_operation.
    def exitAlu_operation(self, ctx:FPE_assemblyParser.Alu_operationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_1f_1s.
    def enterAlu_1f_1s(self, ctx:FPE_assemblyParser.Alu_1f_1sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_1f_1s.
    def exitAlu_1f_1s(self, ctx:FPE_assemblyParser.Alu_1f_1sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_1f_1s_mnemonic.
    def enterAlu_1f_1s_mnemonic(self, ctx:FPE_assemblyParser.Alu_1f_1s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_1f_1s_mnemonic.
    def exitAlu_1f_1s_mnemonic(self, ctx:FPE_assemblyParser.Alu_1f_1s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_2f_0s.
    def enterAlu_2f_0s(self, ctx:FPE_assemblyParser.Alu_2f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_2f_0s.
    def exitAlu_2f_0s(self, ctx:FPE_assemblyParser.Alu_2f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_2f_0s_mnemonic.
    def enterAlu_2f_0s_mnemonic(self, ctx:FPE_assemblyParser.Alu_2f_0s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_2f_0s_mnemonic.
    def exitAlu_2f_0s_mnemonic(self, ctx:FPE_assemblyParser.Alu_2f_0s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_2f_1s.
    def enterAlu_2f_1s(self, ctx:FPE_assemblyParser.Alu_2f_1sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_2f_1s.
    def exitAlu_2f_1s(self, ctx:FPE_assemblyParser.Alu_2f_1sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_2f_1s_mnemonic.
    def enterAlu_2f_1s_mnemonic(self, ctx:FPE_assemblyParser.Alu_2f_1s_mnemonicContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_2f_1s_mnemonic.
    def exitAlu_2f_1s_mnemonic(self, ctx:FPE_assemblyParser.Alu_2f_1s_mnemonicContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_fetch.
    def enterAlu_fetch(self, ctx:FPE_assemblyParser.Alu_fetchContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_fetch.
    def exitAlu_fetch(self, ctx:FPE_assemblyParser.Alu_fetchContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#alu_store.
    def enterAlu_store(self, ctx:FPE_assemblyParser.Alu_storeContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#alu_store.
    def exitAlu_store(self, ctx:FPE_assemblyParser.Alu_storeContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#mem_fetch.
    def enterMem_fetch(self, ctx:FPE_assemblyParser.Mem_fetchContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#mem_fetch.
    def exitMem_fetch(self, ctx:FPE_assemblyParser.Mem_fetchContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#mem_store.
    def enterMem_store(self, ctx:FPE_assemblyParser.Mem_storeContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#mem_store.
    def exitMem_store(self, ctx:FPE_assemblyParser.Mem_storeContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#imm_access.
    def enterImm_access(self, ctx:FPE_assemblyParser.Imm_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#imm_access.
    def exitImm_access(self, ctx:FPE_assemblyParser.Imm_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#get_access.
    def enterGet_access(self, ctx:FPE_assemblyParser.Get_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#get_access.
    def exitGet_access(self, ctx:FPE_assemblyParser.Get_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#put_access.
    def enterPut_access(self, ctx:FPE_assemblyParser.Put_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#put_access.
    def exitPut_access(self, ctx:FPE_assemblyParser.Put_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#reg_access.
    def enterReg_access(self, ctx:FPE_assemblyParser.Reg_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#reg_access.
    def exitReg_access(self, ctx:FPE_assemblyParser.Reg_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#ram_access.
    def enterRam_access(self, ctx:FPE_assemblyParser.Ram_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#ram_access.
    def exitRam_access(self, ctx:FPE_assemblyParser.Ram_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#rom_access.
    def enterRom_access(self, ctx:FPE_assemblyParser.Rom_accessContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#rom_access.
    def exitRom_access(self, ctx:FPE_assemblyParser.Rom_accessContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#mem_addr.
    def enterMem_addr(self, ctx:FPE_assemblyParser.Mem_addrContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#mem_addr.
    def exitMem_addr(self, ctx:FPE_assemblyParser.Mem_addrContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#encoded_addr.
    def enterEncoded_addr(self, ctx:FPE_assemblyParser.Encoded_addrContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#encoded_addr.
    def exitEncoded_addr(self, ctx:FPE_assemblyParser.Encoded_addrContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#bam_addr.
    def enterBam_addr(self, ctx:FPE_assemblyParser.Bam_addrContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#bam_addr.
    def exitBam_addr(self, ctx:FPE_assemblyParser.Bam_addrContext):
        pass


