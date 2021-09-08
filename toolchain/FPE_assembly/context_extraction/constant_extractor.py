from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"constants" : {},
		}


	def get_updated_program_context(this):
		return this.program_context


	def enterState_constant(this, ctx):
		const_name = asm_utils.token_to_text(ctx.ident_dec().IDENTIFER())

		assert(const_name not in this.program_context["constants"].keys())
		this.program_context["constants"][const_name] = asm_utils.evaluate_expr(ctx.expr(), this.program_context)
