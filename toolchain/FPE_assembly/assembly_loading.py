from antlr4 import *

from .grammar.FPE_assemblyParser import FPE_assemblyParser
from .grammar.FPE_assemblyLexer  import FPE_assemblyLexer

def load_file(inputFile):
	input  = FileStream(inputFile)
	lexer  = FPE_assemblyLexer(input)
	stream = CommonTokenStream(lexer)
	parser = FPE_assemblyParser(stream)
	tree   = parser.scope()

	return tree
