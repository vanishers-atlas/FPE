# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils

####################################################################

class extractor(ParseTreeListener):

	def __init__(this, program_context, config):
		this.program_context = program_context
		this.config = config

	def get_updated_config(this):
		for BAM in this.config["address_sources"].values():
			# Handle step source
			if "steps_acc" not in BAM.keys():
				BAM["internal_step_type"] = "none"
			elif len(BAM["steps_acc"]) == 1:
				BAM["internal_step_type"] = "generic"
			else:
				BAM["internal_step_type"] = "ROM"
				BAM["interal_steps"] = len(BAM["steps_acc"])
			if "steps_acc" in BAM.keys() : del BAM["steps_acc"]

			# Handle base source
			if "bases_acc" not in BAM.keys() or len(BAM["bases_acc"]) <= 1:
				BAM["base_type"] = "generic"
			else:
				BAM["base_type"] = "ROM"
				BAM["internal_bases"] = len(BAM["bases_acc"])
			if "bases_acc" in BAM.keys() : del BAM["bases_acc"]

			BAM["movements"] = sorted(list(BAM["movements"]))
		return this.config


	def enterOp_bam_seek(this, ctx):
		BAM = asm_utils.get_component_op(ctx, this.program_context)[0]

		# Default to FORWARD
		if ctx.direction == None:
			direction = "forward"
		else:
			direction = asm_utils.token_to_text(ctx.direction).lower()

		# Record direction signal

		try:
			this.config["address_sources"][BAM]["movements"].add(("fetched", direction, ) )
		except KeyError:
			this.config["address_sources"][BAM]["movements"] = set([("fetched", direction, ), ] )

	def enterAddr_bam(this, ctx):
		BAM = asm_utils.get_component_addr(ctx, this.program_context)

		# default to forward
		direction = "forward"
		direction_given = False
		step_handled = False

		# Process mods
		for _mod_ctx in ctx.addr_bam_mod():
			if   _mod_ctx.addr_bam_dir_mod():
				mod_ctx = _mod_ctx.addr_bam_dir_mod()
				direction = asm_utils.token_to_text(mod_ctx.direction).lower()
				direction_given = True
			elif _mod_ctx.addr_bam_size_mod():
				mod_ctx = _mod_ctx.addr_bam_size_mod()

				step_handled = True
				step = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				try:
					this.config["address_sources"][BAM]["steps_acc"].add(step)
				except KeyError:
					this.config["address_sources"][BAM]["steps_acc"] = set((step,) )
			elif _mod_ctx.addr_bam_base_mod():
				mod_ctx = _mod_ctx.addr_bam_base_mod()

				base = asm_utils.evaluate_expr(mod_ctx.expr(), this.program_context)
				try:
					this.config["address_sources"][BAM]["bases_acc"].add(base)
				except KeyError:
					this.config["address_sources"][BAM]["bases_acc"] = set((base,) )
			else:
				raise ValueError("mod_ctx with unknown subrule at %s"%(asm_utils.ctx_start(_mod_ctx), ) )

		if direction_given and not step_handled:
			try:
				this.config["address_sources"][BAM]["steps_acc"].add(None)
			except KeyError:
				this.config["address_sources"][BAM]["steps_acc"] = set((None,) )

		if direction_given or step_handled:
			try:
				this.config["address_sources"][BAM]["movements"].add(("internal", direction, ) )
			except KeyError:
				this.config["address_sources"][BAM]["movements"] = set([("internal", direction, ), ] )
