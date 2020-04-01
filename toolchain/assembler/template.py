from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

####################################################################

class handler(ParseTreeListener):

    def __init__(this, output_path, generic, config):
        this.output_path = output_path
        this.generic = generic
        this.config = config

    def get_output(this):
        return


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


    def enterTiming_operation(this, ctx):
        pass

    def exitTiming_operation(this, ctx):
        pass


    def enterNop(this, ctx):
        pass

    def exitNop(this, ctx):
        pass


    def enterJump_operation(this, ctx):
        pass

    def exitJump_operation(this, ctx):
        pass


    def enterJmp(this, ctx):
        pass

    def exitJmp(this, ctx):
        pass


    def enterJlt(this, ctx):
        pass

    def exitJlt(this, ctx):
        pass


    def enterBam_operation(this, ctx):
        pass

    def exitBam_operation(this, ctx):
        pass


    def enterBam_rst(this, ctx):
        pass

    def exitBam_rst(this, ctx):
        pass


    def enterBam_adv(this, ctx):
        pass

    def exitBam_adv(this, ctx):
        pass


    def enterAlu_operation(this, ctx):
        pass

    def exitAlu_operation(this, ctx):
        pass


    def enterAlu_mov(this, ctx):
        pass

    def exitAlu_mov(this, ctx):
        pass


    def enterAlu_and(this, ctx):
        pass

    def exitAlu_and(this, ctx):
        pass


    def enterAlu_add_acc(this, ctx):
        pass

    def exitAlu_add_acc(this, ctx):
        pass


    def enterAlu_load_acc(this, ctx):
        pass

    def exitAlu_load_acc(this, ctx):
        pass


    def enterAlu_lcmp_acc(this, ctx):
        pass

    def exitAlu_lcmp_acc(this, ctx):
        pass


    def enterMem_read(this, ctx):
        pass

    def exitMem_read(this, ctx):
        pass


    def enterMem_write(this, ctx):
        pass

    def exitMem_write(this, ctx):
        pass


    def enterImm(this, ctx):
        pass

    def exitImm(this, ctx):
        pass


    def enterGet(this, ctx):
        pass

    def exitGet(this, ctx):
        pass


    def enterPut(this, ctx):
        pass

    def exitPut(this, ctx):
        pass


    def enterReg(this, ctx):
        pass

    def exitReg(this, ctx):
        pass


    def enterRam(this, ctx):
        pass

    def exitRam(this, ctx):
        pass


    def enterRom(this, ctx):
        pass

    def exitRom(this, ctx):
        pass


    def enterAddr(this, ctx):
        pass

    def exitAddr(this, ctx):
        pass


    def enterEncoded_addr(this, ctx):
        pass

    def exitEncoded_addr(this, ctx):
        pass


    def enterBam_read(this, ctx):
        pass

    def exitBam_read(this, ctx):
        pass
