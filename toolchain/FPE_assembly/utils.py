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

####################################################################

def decode_number_literal(num_str):
    if   num_str.startswith("0b") or num_str.startswith("0B"):
        return int(num_str[2:], 2)
    elif num_str.startswith("0x") or num_str.startswith("0X"):
        return int(num_str[2:], 16)
    else:
        return int(num_str)
