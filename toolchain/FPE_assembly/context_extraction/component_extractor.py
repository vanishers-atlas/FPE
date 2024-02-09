from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"components" : {
				"declared_ZOLs" : {}
			},
		}

	def get_updated_program_context(this):
		return this.program_context


	def enterState_component(this, ctx):
		com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())
		com_type = asm_utils.token_to_text(ctx.com_type)

		# Exteract component parameters
		parameters = {}
		for para_ctx in ctx.state_component_parameter():
			para_name = asm_utils.token_to_text(para_ctx.para_name)

			assert(para_name not in parameters.keys())

			if   para_ctx.expr() != None:
				parameters[para_name] = asm_utils.evaluate_expr(para_ctx.expr(), this.program_context)
			elif para_ctx.BOOL() != None:
				parameters[para_name] = asm_utils.token_to_text(para_ctx.BOOL()).lower() == "true"
			else:
				raise SyntaxError("Component parameter found without a know vqlue form, %s"%(
					asm_utils.ctx_start(para_ctx)
				))

		if   com_type in ["ZOL_ripple", "ZOL_cascade", "ZOL_counter"]:
			this.program_context["components"]["declared_ZOLs"][com_name] = {
				"ctx" : ctx,
				"parameters" : parameters,
			}
		else:
			raise ValueError("Unknown com_type, %s, at %s"%(
				com_type,
				asm_utils.ctx_start(ctx)
			) )
