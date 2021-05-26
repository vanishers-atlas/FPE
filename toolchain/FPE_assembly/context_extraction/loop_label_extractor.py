from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"loop_labels" : {},
		}
		this.PC_next = 0 # First operations is alway PC 0


	def get_updated_program_context(this):
		return this.program_context

	# Increment PC_value every operation
	def enterOperation(this, ctx):
		this.PC_next += 1

	# Capture PC_next on entering a loop as this is the PC value the loop
	# overwrites thes the PC to whiule repeating
	def enterState_loop_label(this, ctx):
		loop_name = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())
		assert(loop_name not in this.program_context["loop_labels"].keys())
		this.program_context["loop_labels"][loop_name] = {
			"start" : this.PC_next,
			"end" : None # Mark the end value as unset to debugging
			}

	# Capture PC_next - 1 on exiting a loop,
	# PC_next - 1 as PC_next points to the operation just after the loop within this function
	def exitState_loop_label(this, ctx):
		loop_name = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())
		this.program_context["loop_labels"][loop_name]["end"] = this.PC_next - 1
