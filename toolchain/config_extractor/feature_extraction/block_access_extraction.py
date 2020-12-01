# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils


####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config

        # Create sets for all block access
        try:
            this.config["data_memories"]["REG"]["block_reads"] = set()
            this.config["data_memories"]["REG"]["block_writes"] = set()
        except:
            pass
        try:
            this.config["data_memories"]["RAM"]["block_reads"] = set()
            this.config["data_memories"]["RAM"]["block_writes"] = set()
        except:
            pass
        try:
            this.config["data_memories"]["ROM"]["block_reads"] = set()
        except:
            pass

    def get_updated_config(this):
        # Convert sets to lists for all block access
        try:
            this.config["data_memories"]["REG"]["block_reads"] = list(sorted(this.config["data_memories"]["REG"]["block_reads"]))
            this.config["data_memories"]["REG"]["block_writes"] = list(sorted(this.config["data_memories"]["REG"]["block_writes"]))
        except:
            pass
        try:
            this.config["data_memories"]["RAM"]["block_reads"] = list(sorted(this.config["data_memories"]["RAM"]["block_reads"]))
            this.config["data_memories"]["RAM"]["block_writes"] = list(sorted(this.config["data_memories"]["RAM"]["block_writes"]))
        except:
            pass
        try:
            this.config["data_memories"]["ROM"]["block_reads"] = list(sorted(this.config["data_memories"]["ROM"]["block_reads"]))
        except:
            pass

        return this.config

    # Mark access type to know which block list to update
    def enterAccess_fetch(this, ctx):
        this.access_type = "read"

    def enterAccess_store(this, ctx):
        this.access_type = "write"

    # Handle block accesses
    def enterAccess_reg(this, ctx):
        if ctx.expr() != None:
            # Get block accesses size
            block_size = asm_utils.evaluate_expr(ctx.expr(), this.program_context)
        else:
            block_size = 1

        if this.access_type == "read":
            this.config["data_memories"]["REG"]["block_reads"].add(block_size)
        elif this.access_type == "write":
            this.config["data_memories"]["REG"]["block_writes"].add(block_size)
        else:
            raise NotImplementedError("Unknowned access type " + this.access_type)

    def enterAccess_ram(this, ctx):
        if ctx.expr() != None:
            # Get block accesses size
            block_size = asm_utils.evaluate_expr(ctx.expr(), this.program_context)
        else:
            block_size = 1

        if this.access_type == "read":
            this.config["data_memories"]["RAM"]["block_reads"].add(block_size)
        elif this.access_type == "write":
            this.config["data_memories"]["RAM"]["block_writes"].add(block_size)
        else:
            raise NotImplementedError("Unknowned access type " + this.access_type)


    def enterAccess_rom(this, ctx):
        if ctx.expr() != None:
            # Get block accesses size
            block_size = asm_utils.evaluate_expr(ctx.expr(), this.program_context)
        else:
            block_size = 1

        if this.access_type == "read":
            this.config["data_memories"]["ROM"]["block_reads"].add(block_size)
        else:
            raise NotImplementedError("Unknowned access type " + this.access_type)
