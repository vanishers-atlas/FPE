# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils

import itertools as it

####################################################################

class handler(ParseTreeListener):
	def __init__(this, program_context, config):
		this.program_context = program_context
		this.config = config

		this.steps = {}
		this.bases = {}

	def get_steps(this):
		steps = {}
		for bam, values in this.steps.items():
			steps[bam] = sorted(list(values))

		return steps

	def get_bases(this):
		bases = {}
		for bam, values in this.bases.items():
			bases[bam] = sorted(list(values))

		return bases

	def enterAddr_bam(this, ctx):
		BAM = asm_utils.get_component_addr(ctx, this.program_context)

		# Process mods
		for _mod_ctx in ctx.addr_bam_mod():
			if   _mod_ctx.addr_bam_dir_mod():
				pass
			elif _mod_ctx.addr_bam_size_mod():
				mod_ctx = _mod_ctx.addr_bam_size_mod()

				step = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				try:
					this.steps[BAM].add(step)
				except KeyError:
					this.steps[BAM] = set((step,) )
			elif _mod_ctx.addr_bam_base_mod():
				mod_ctx = _mod_ctx.addr_bam_base_mod()

				base = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				base_encoded = tc_utils.unsigned.encode(base, this.config["address_sources"][BAM]["addr_width"])
				try:
					this.bases[BAM].add(base_encoded)
				except KeyError:
					this.bases[BAM] = set((base_encoded,) )
			else:
				raise ValueError("mod_ctx with unknown subrule at %s"%(asm_utils.ctx_start(_mod_ctx), ) )
