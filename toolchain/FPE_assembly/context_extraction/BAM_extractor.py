from antlr4 import ParseTreeListener

from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"BAM_steps" : {},
			"BAM_bases" : {},
		}


	def get_updated_program_context(this):
		BAM_steps = {}
		for k, vs in this.program_context["BAM_steps"].items():
			if len(vs) > 1:
				BAM_steps[k] = sorted(list(vs))
		this.program_context["BAM_steps"] = BAM_steps

		BAM_bases = {}
		for k, vs in this.program_context["BAM_bases"].items():
			if len(vs) > 1:
				BAM_bases[k] = sorted(list(vs))
		this.program_context["BAM_bases"] = BAM_bases

		return this.program_context

	def enterAddr_bam(this, ctx):
		BAM = asm_utils.get_component_addr(ctx, this.program_context)

		for _mod_ctx in ctx.addr_bam_mod():
			if   _mod_ctx.addr_bam_dir_mod():
				pass
			elif _mod_ctx.addr_bam_size_mod():
				mod_ctx = _mod_ctx.addr_bam_size_mod()

				step = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				try:
					this.program_context["BAM_steps"][BAM].add(step)
				except KeyError:
					this.program_context["BAM_steps"][BAM] = set((step,) )

			elif _mod_ctx.addr_bam_base_mod():
				mod_ctx = _mod_ctx.addr_bam_base_mod()

				base = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				try:
					this.program_context["BAM_bases"][BAM].add(base)
				except KeyError:
					this.program_context["BAM_bases"][BAM] = set((base,) )
			else:
				raise ValueError("mod_ctx with unknown subrule at %s"%(asm_utils.ctx_start(_mod_ctx), ) )
