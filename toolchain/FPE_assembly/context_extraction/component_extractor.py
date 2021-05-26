from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"components" : {
				"ZOLs" : {}
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

			if   len(para_ctx.IDENTIFER()) == 2:
				parameters[para_name] = asm_utils.token_to_text(para_ctx.IDENTIFER()[1])
			elif para_ctx.expr() != None:
				parameters[para_name] = asm_utils.evaluate_expr(para_ctx.expr(), this.program_context)
			else:
				raise SyntaxError("Component parameter found without a know vqlue form, %s"%(
					asm_utils.ctx_start(para_ctx)
				))

		if   com_type in ["ZOL_ripple", "ZOL_cascade", "ZOL_counter"]:
			this.program_context["components"]["ZOLs"][com_name] = {
				"ctx" : ctx,
				"type" : com_type[4:], # Drop the ZOL_ from the com type to get the Zol type
				"parameters" : parameters,
			}
		else:
			raise ValueError("Unknown com_type, %s, at %s"(
				com_type,
				asm_utils.ctx_start(ctx)
			) )
