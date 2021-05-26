from antlr4 import *

from FPE.toolchain.FPE_assembly import grammar
from FPE.toolchain.FPE_assembly import hypergrammar
from FPE.toolchain.FPE_assembly import context_extraction

def load_file(inputFile):
	input  = FileStream(inputFile)
	lexer  = grammar.lexer(input)
	stream = CommonTokenStream(lexer)
	parser = grammar.parser(stream)
	tree   = parser.scope()
	walker = ParseTreeWalker()

	# Check precontext 'hyper-grammar rules,
	for rules in hypergrammar.precontext_rules:
		extractor = rules.extractor()
		walker.walk(extractor, tree)
		extractor.final_check()

	# Generate program context
	# Use antlr 4 tree as program tree
	program_context = {
		"program_tree" : tree
	}
	# Run context extractors to generate the rest of the program context
	for extractor_type in context_extraction.extractors:
		extractor = extractor_type.extractor(program_context)
		walker.walk(extractor, program_context["program_tree"])
		program_context = extractor.get_updated_program_context()


	# Check precontext 'hyper-grammar rules,
	for hyper_rule in hypergrammar.postcontext_rules:
		extractor = hyper_rule.extractor(program_context)
		walker.walk(extractor, tree)
		extractor.final_check()

	return program_context
