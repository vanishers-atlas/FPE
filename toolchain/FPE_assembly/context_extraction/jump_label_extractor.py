from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"jump_labels" : {},
		}
		this.PC_next = 0 # First operations is alway PC 0

	def get_updated_program_context(this):
		return this.program_context

	# Increment PC_next every operation
	def enterOperation(this, ctx):
		this.PC_next += 1

	# Store the PC_next for every jump label
	def enterState_jump_label(this, ctx):
		label_name = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())

		assert(label_name not in this.program_context["jump_labels"].keys())
		this.program_context["jump_labels"][label_name] = this.PC_next
