from antlr4 import *

from FPE.toolchain.FPE_assembly.interface.evaluate_expr import evaluate_expr

from FPE.toolchain.FPE_assembly import grammar
from FPE.toolchain.FPE_assembly import hypergrammar

def load_file(inputFile):
	input  = FileStream(inputFile)
	lexer  = grammar.lexer(input)
	stream = CommonTokenStream(lexer)
	parser = grammar.parser(stream)
	tree   = parser.scope()

	program_context = {
		"program_tree"	: tree,
	}

	# Check asm rules not enforced by grammar
	walker = ParseTreeWalker()
	for hyper_rule in hypergrammar.hyper_rules:
		extractor = hyper_rule.extractor()
		walker.walk(extractor, tree)
		extractor.final_check()

	# Preload all const def
	extractor = const_def_estactor(program_context)
	walker.walk(extractor, program_context["program_tree"])
	program_context = extractor.get_updated_program_context()

	return program_context

class const_def_estactor(ParseTreeListener):

	def __init__(this, program_context):
		this.program_context = {
			**program_context,
			"constants" : {},
		}


	def get_updated_program_context(this):
		return this.program_context


	def enterState_constant(this, ctx):
		identifer = ctx.IDENTIFER().getText()
		this.program_context["constants"][identifer] = evaluate_expr(ctx.expr(), this.program_context)
