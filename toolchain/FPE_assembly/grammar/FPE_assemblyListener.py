# Generated from FPE_assembly.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FPE_assemblyParser import FPE_assemblyParser
else:
    from FPE_assemblyParser import FPE_assemblyParser

# This class defines a complete listener for a parse tree produced by FPE_assemblyParser.
class FPE_assemblyListener(ParseTreeListener):

    # Enter a parse tree produced by FPE_assemblyParser#expr.
    def enterExpr(self, ctx:FPE_assemblyParser.ExprContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#expr.
    def exitExpr(self, ctx:FPE_assemblyParser.ExprContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#expr_operand.
    def enterExpr_operand(self, ctx:FPE_assemblyParser.Expr_operandContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#expr_operand.
    def exitExpr_operand(self, ctx:FPE_assemblyParser.Expr_operandContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#jump_label.
    def enterJump_label(self, ctx:FPE_assemblyParser.Jump_labelContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#jump_label.
    def exitJump_label(self, ctx:FPE_assemblyParser.Jump_labelContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#scope.
    def enterScope(self, ctx:FPE_assemblyParser.ScopeContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#scope.
    def exitScope(self, ctx:FPE_assemblyParser.ScopeContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_fetch.
    def enterAccess_fetch(self, ctx:FPE_assemblyParser.Access_fetchContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_fetch.
    def exitAccess_fetch(self, ctx:FPE_assemblyParser.Access_fetchContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_store.
    def enterAccess_store(self, ctx:FPE_assemblyParser.Access_storeContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_store.
    def exitAccess_store(self, ctx:FPE_assemblyParser.Access_storeContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_imm.
    def enterAccess_imm(self, ctx:FPE_assemblyParser.Access_immContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_imm.
    def exitAccess_imm(self, ctx:FPE_assemblyParser.Access_immContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_get.
    def enterAccess_get(self, ctx:FPE_assemblyParser.Access_getContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_get.
    def exitAccess_get(self, ctx:FPE_assemblyParser.Access_getContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_get_mod.
    def enterAccess_get_mod(self, ctx:FPE_assemblyParser.Access_get_modContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_get_mod.
    def exitAccess_get_mod(self, ctx:FPE_assemblyParser.Access_get_modContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_put.
    def enterAccess_put(self, ctx:FPE_assemblyParser.Access_putContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_put.
    def exitAccess_put(self, ctx:FPE_assemblyParser.Access_putContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_reg.
    def enterAccess_reg(self, ctx:FPE_assemblyParser.Access_regContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_reg.
    def exitAccess_reg(self, ctx:FPE_assemblyParser.Access_regContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_ram.
    def enterAccess_ram(self, ctx:FPE_assemblyParser.Access_ramContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_ram.
    def exitAccess_ram(self, ctx:FPE_assemblyParser.Access_ramContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_rom.
    def enterAccess_rom(self, ctx:FPE_assemblyParser.Access_romContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_rom.
    def exitAccess_rom(self, ctx:FPE_assemblyParser.Access_romContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#addr.
    def enterAddr(self, ctx:FPE_assemblyParser.AddrContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#addr.
    def exitAddr(self, ctx:FPE_assemblyParser.AddrContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#addr_literal.
    def enterAddr_literal(self, ctx:FPE_assemblyParser.Addr_literalContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#addr_literal.
    def exitAddr_literal(self, ctx:FPE_assemblyParser.Addr_literalContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#addr_bam.
    def enterAddr_bam(self, ctx:FPE_assemblyParser.Addr_bamContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#addr_bam.
    def exitAddr_bam(self, ctx:FPE_assemblyParser.Addr_bamContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#addr_bam_mod.
    def enterAddr_bam_mod(self, ctx:FPE_assemblyParser.Addr_bam_modContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#addr_bam_mod.
    def exitAddr_bam_mod(self, ctx:FPE_assemblyParser.Addr_bam_modContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#statement.
    def enterStatement(self, ctx:FPE_assemblyParser.StatementContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#statement.
    def exitStatement(self, ctx:FPE_assemblyParser.StatementContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#state_zol.
    def enterState_zol(self, ctx:FPE_assemblyParser.State_zolContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#state_zol.
    def exitState_zol(self, ctx:FPE_assemblyParser.State_zolContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#state_jump_label.
    def enterState_jump_label(self, ctx:FPE_assemblyParser.State_jump_labelContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#state_jump_label.
    def exitState_jump_label(self, ctx:FPE_assemblyParser.State_jump_labelContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#state_constant.
    def enterState_constant(self, ctx:FPE_assemblyParser.State_constantContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#state_constant.
    def exitState_constant(self, ctx:FPE_assemblyParser.State_constantContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#operation.
    def enterOperation(self, ctx:FPE_assemblyParser.OperationContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#operation.
    def exitOperation(self, ctx:FPE_assemblyParser.OperationContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_void.
    def enterOp_void(self, ctx:FPE_assemblyParser.Op_voidContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_void.
    def exitOp_void(self, ctx:FPE_assemblyParser.Op_voidContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_void_nop.
    def enterOp_void_nop(self, ctx:FPE_assemblyParser.Op_void_nopContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_void_nop.
    def exitOp_void_nop(self, ctx:FPE_assemblyParser.Op_void_nopContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_pc.
    def enterOp_pc(self, ctx:FPE_assemblyParser.Op_pcContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_pc.
    def exitOp_pc(self, ctx:FPE_assemblyParser.Op_pcContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_pc_jump.
    def enterOp_pc_jump(self, ctx:FPE_assemblyParser.Op_pc_jumpContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_pc_jump.
    def exitOp_pc_jump(self, ctx:FPE_assemblyParser.Op_pc_jumpContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_bam.
    def enterOp_bam(self, ctx:FPE_assemblyParser.Op_bamContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_bam.
    def exitOp_bam(self, ctx:FPE_assemblyParser.Op_bamContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_bam_reset.
    def enterOp_bam_reset(self, ctx:FPE_assemblyParser.Op_bam_resetContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_bam_reset.
    def exitOp_bam_reset(self, ctx:FPE_assemblyParser.Op_bam_resetContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_bam_seek.
    def enterOp_bam_seek(self, ctx:FPE_assemblyParser.Op_bam_seekContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_bam_seek.
    def exitOp_bam_seek(self, ctx:FPE_assemblyParser.Op_bam_seekContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_bam_seek_mod.
    def enterOp_bam_seek_mod(self, ctx:FPE_assemblyParser.Op_bam_seek_modContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_bam_seek_mod.
    def exitOp_bam_seek_mod(self, ctx:FPE_assemblyParser.Op_bam_seek_modContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_alu.
    def enterOp_alu(self, ctx:FPE_assemblyParser.Op_aluContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_alu.
    def exitOp_alu(self, ctx:FPE_assemblyParser.Op_aluContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_alu_1f_1s.
    def enterOp_alu_1f_1s(self, ctx:FPE_assemblyParser.Op_alu_1f_1sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_alu_1f_1s.
    def exitOp_alu_1f_1s(self, ctx:FPE_assemblyParser.Op_alu_1f_1sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_alu_1f_1e_1s.
    def enterOp_alu_1f_1e_1s(self, ctx:FPE_assemblyParser.Op_alu_1f_1e_1sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_alu_1f_1e_1s.
    def exitOp_alu_1f_1e_1s(self, ctx:FPE_assemblyParser.Op_alu_1f_1e_1sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_alu_2f_0s.
    def enterOp_alu_2f_0s(self, ctx:FPE_assemblyParser.Op_alu_2f_0sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_alu_2f_0s.
    def exitOp_alu_2f_0s(self, ctx:FPE_assemblyParser.Op_alu_2f_0sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#op_alu_2f_1s.
    def enterOp_alu_2f_1s(self, ctx:FPE_assemblyParser.Op_alu_2f_1sContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#op_alu_2f_1s.
    def exitOp_alu_2f_1s(self, ctx:FPE_assemblyParser.Op_alu_2f_1sContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_fetch_alu.
    def enterAccess_fetch_alu(self, ctx:FPE_assemblyParser.Access_fetch_aluContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_fetch_alu.
    def exitAccess_fetch_alu(self, ctx:FPE_assemblyParser.Access_fetch_aluContext):
        pass


    # Enter a parse tree produced by FPE_assemblyParser#access_store_alu.
    def enterAccess_store_alu(self, ctx:FPE_assemblyParser.Access_store_aluContext):
        pass

    # Exit a parse tree produced by FPE_assemblyParser#access_store_alu.
    def exitAccess_store_alu(self, ctx:FPE_assemblyParser.Access_store_aluContext):
        pass


