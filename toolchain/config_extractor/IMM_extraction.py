from antlr4 import *

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

# import toolchain utils for computing addr widths
from .. import utils

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, config):
        this.config = config
        this.values = set()
        this.encoding = "unset"

    def get_updated_config(this):
        if "IMM" in this.config["data_memories"]:
            this.config["data_memories"]["IMM"]["depth"] = len(this.values)
        elif len(this.values) != 0:
            raise ValueError("Immedate values found but no IMM declared within config")
        return this.config


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
        this.values.add(ctx.STRING().getText())

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
        if ctx.bam_1f_0s_mnemonic().getText().upper() in ["BAM_ADV"]:
            this.encoding = "twos_comp"

    def exitBam_1f_0s(this, ctx):
        this.encoding = "unset"


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
        value = FPEA.decode_number_literal(ctx.NUMBER().getText())

        # Check that value can be encoded in data width
        if this.encoding == "twos_comp":
          if not utils.twos_comp.encodeable(value, this.config["data_width"]):
              raise ValueError("Can't encode " + str(value) + ", using 2's comp, in " + str(this.config["data_width"]) + " bits")
        elif this.encoding == "unset":
          if value < 0:
              if not utils.twos_comp.encodeable(value, this.config["data_width"]):
                  raise ValueError("Can't encode " + str(value) + ", using 2's comp, in " + str(this.config["data_width"]) + " bits")
          else:
              if not utils.unsigned.encodeable(value, this.config["data_width"]):
                  raise ValueError("Can't encode " + str(value) + ", using unisgned, in " + str(this.config["data_width"]) + " bits")

        this.values.add(value)


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
        pass

    def exitBam_addr(this, ctx):
        pass
