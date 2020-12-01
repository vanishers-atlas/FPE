# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser as parser

import math

class extractor(ParseTreeListener):

    def __init__(this, program_context):
        this.program_context = program_context

    def final_check(this):
        pass


    def enterOperation(this, ctx):
        # Black out none 1 block_size as each Operation can has a different one
        this.block_size = None


    def enterAccess_reg(this, ctx):
        this.check_access_block_size(ctx)

    def enterAccess_ram(this, ctx):
        this.check_access_block_size(ctx)

    def enterAccess_rom(this, ctx):
        this.check_access_block_size(ctx)

    def check_access_block_size(this, ctx):
        # Check for a block access
        if ctx.expr() != None:
            # Get block accesses size
            block_size = asm_utils.evaluate_expr(ctx.expr(), this.program_context)

            ## Check for valid block_size
            if block_size <= 0:
                raise SyntaxError(
                    "ERROR: An access' block size must evaluate to a positive number, not %i, at %s and %s\n"%
                    (
                        block_size,
                        asm_utils.ctx_start(this.declared_consts[const]),
                        asm_utils.ctx_start(ctx),
                    )
                )

            # No special handling needed for block of 1
            if block_size > 1:
                # If this is the first non one block size, use as block size of whole op
                if this.block_size == None:
                    # Check that blocksize is a power of 2
                    if math.log(block_size, 2) % 1 != 0:
                        raise SyntaxError(
                            "ERROR: A block size must be a power of two, at %s and %s\n"%
                            (
                                asm_utils.ctx_start(this.declared_consts[const]),
                                asm_utils.ctx_start(ctx),
                            )
                        )

                    this.block_size = block_size
                # Else check block size is same as other in operations
                else:
                    if this.block_size != block_size:
                        raise SyntaxError(
                            "ERROR: Only a signal non-one block size value can be used per operatation, at %s and %s\n"%
                            (
                                asm_utils.ctx_start(this.declared_consts[const]),
                                asm_utils.ctx_start(ctx),
                            )
                        )
