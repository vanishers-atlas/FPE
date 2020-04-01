import json

def parser_preamble(config):
	global parser, lexer, keywords, parser_sub_rules
	parser  = "grammar FPE_assembly;\n\n"
	parser += "/* Parser Rules */\n\n"

	parser += "\tscope : OCB ( scope | delay | label | statement )* CCB ;\n\n"
	parser += "\tlabel : STRING COLON ;\n\n"
	parser += "\tdelay : DELAY ORB STRING ( COMMA STRING)* CRB SEMICOLON ;\n"
	parser += "\ttiming_mod : ( BEFORE | AFTER ) COLON STRING ;\n\n"

	# Generate statement rule
	statements = [x.lower() for x in config.keys() if x.lower() in ["wrapper", "operation"] ]
	parser += "\tstatement : %s ;\n\n"%(" | ".join(statements), )

def generater_lexer ():
	global parser, lexer, keywords, parser_sub_rules

	lexer  = "\n\n/* lexer Rules */\n\n"

	lexer += "\t/* Bracket Tokens */\n"
	lexer += "\t\tOAB : '<' ;\n"
	lexer += "\t\tCAB : '>' ;\n"
	lexer += "\t\tOCB : '{' ;\n"
	lexer += "\t\tCCB : '}' ;\n"
	lexer += "\t\tORB : '(' ;\n"
	lexer += "\t\tCRB : ')' ;\n"
	lexer += "\t\tOSB : '[' ;\n"
	lexer += "\t\tCSB : ']' ;\n\n"

	lexer += "\t/* Special character Tokens */\n"
	lexer += "\t\tSEMICOLON : ';' ;\n"
	lexer += "\t\tCOLON : ':' ;\n"
	lexer += "\t\tCOMMA : ',' ;\n\n"

	lexer += "\t/* Caseless Fragments */\n"
	lexer += "\t\tfragment A : ('a'|'A') ;\n"
	lexer += "\t\tfragment B : ('b'|'B') ;\n"
	lexer += "\t\tfragment C : ('c'|'C') ;\n"
	lexer += "\t\tfragment D : ('d'|'D') ;\n"
	lexer += "\t\tfragment E : ('e'|'E') ;\n"
	lexer += "\t\tfragment F : ('f'|'F') ;\n"
	lexer += "\t\tfragment G : ('g'|'G') ;\n"
	lexer += "\t\tfragment H : ('h'|'H') ;\n"
	lexer += "\t\tfragment I : ('i'|'I') ;\n"
	lexer += "\t\tfragment J : ('j'|'J') ;\n"
	lexer += "\t\tfragment K : ('k'|'K') ;\n"
	lexer += "\t\tfragment L : ('l'|'L') ;\n"
	lexer += "\t\tfragment M : ('m'|'M') ;\n"
	lexer += "\t\tfragment N : ('n'|'N') ;\n"
	lexer += "\t\tfragment O : ('o'|'O') ;\n"
	lexer += "\t\tfragment P : ('p'|'P') ;\n"
	lexer += "\t\tfragment Q : ('q'|'Q') ;\n"
	lexer += "\t\tfragment R : ('r'|'R') ;\n"
	lexer += "\t\tfragment S : ('s'|'S') ;\n"
	lexer += "\t\tfragment T : ('t'|'T') ;\n"
	lexer += "\t\tfragment U : ('u'|'U') ;\n"
	lexer += "\t\tfragment V : ('v'|'V') ;\n"
	lexer += "\t\tfragment W : ('w'|'W') ;\n"
	lexer += "\t\tfragment X : ('x'|'X') ;\n"
	lexer += "\t\tfragment Y : ('y'|'Y') ;\n"
	lexer += "\t\tfragment Z : ('z'|'Z') ;\n\n"

	lexer += "\t/* Number Handling */\n"
	lexer += "\t\tfragment BIN : '0' B [0-1]+ ;\n"
	lexer += "\t\tfragment OCT : '0' O [0-7]+ ;\n"
	lexer += "\t\tfragment HEX : '0' X [0-9A-Fa-f]+ ;\n"
	lexer += "\t\tfragment DEC : [+-]? [0-9]+ ;\n\n"
	lexer += "\t\tNUMBER : (BIN | OCT | HEX | DEC) ;\n"

	# Handle mnemonics
	lexer += "\n\t/* Keyword tokens */\n"
	lexer += "\t\tDELAY  : D E L A Y ;\n"
	lexer += "\t\tAFTER  : A F T E R ;\n"
	lexer += "\t\tBEFORE : B E F O R E ;\n"
	for keyword in sorted(list(keywords)):
		lexer += "\t\t%s : %s ;\n"%(keyword, " ".join(keyword))

	# Standard end for antlr lexer
	lexer += "\n\t/* General String Handling */\n"
	lexer += "\t\tSTRING : [_a-zA-Z][_a-zA-Z0-9]* ;\n\n"

	lexer += "\t/* Whitespace and comment Skipping */\n"
	lexer += "\t\tMUTL_LINE_COMMENT : '//*' .*? '*//' -> skip ;\n"
	lexer += "\t\tSING_LINE_COMMENT : '//' .*? [\\n\\r]+ -> skip ;\n"
	lexer += "\t\tWHITESPACE : [ \\t\\n\\r]+ -> skip ;\n"

#########################################################################

data_types = ["NUMBER", "STRING", "src", "dst"]

def create_wrapper_rules():
	global parser, lexer, keywords, parser_sub_rules

	parser += "\n\twrapper : %s ;\n\n"%(
		" | ".join(
			["%s_wrapper"%(n.lower(), ) for n in config["wrapper"].keys()]
		),
	)

	for rule_name, sub_config in config["wrapper"].items():
		parser_sub_rules = ""
		rule_name = "%s_wrapper"%(rule_name.lower(), )
		parser += "\t\t%s :"%(rule_name, )
		handle_mnemonics  (rule_name, sub_config)
		handle_com_selext (rule_name, sub_config)
		handle_address    (rule_name, sub_config)
		handle_operands   (rule_name, sub_config)
		handle_mods       (rule_name, sub_config)
		parser += " scope ;\n"
		parser += parser_sub_rules + "\n"

def create_operation_rules():
	global parser, lexer, keywords, parser_sub_rules

	parser += "\n\toperation : %s ;\n\n"%(
		" | ".join(
			["%s_operation"%(n.lower(), ) for n in config["operation"].keys()]
		),
	)

	for rule_name, sub_config in config["operation"].items():
		parser_sub_rules = ""
		rule_name = "%s_operation"%(rule_name.lower(), )
		parser += "\t\t%s :"%(rule_name, )
		handle_mnemonics  (rule_name, sub_config)
		handle_com_selext (rule_name, sub_config)
		handle_address    (rule_name, sub_config)
		handle_operands   (rule_name, sub_config)
		handle_mods       (rule_name, sub_config)
		parser += " SEMICOLON ;\n"
		parser += parser_sub_rules + "\n"

def generate_access_rules():
	global parser, lexer, keywords, parser_sub_rules

	# Generate scr and dest access list
	parser += "\tsrc : %s ;\n"%(
		" | ".join(
			[
				"%s_access"%(n.lower(), )
				for n in config["access"].keys()
				if "is_src" in config["access"][n] and config["access"][n]["is_src"] == True
			]
			# Add imm access as a possible src
			 + ["imm_access"]
		,)
	)

	parser += "\tdst : %s ;\n"%(
		" | ".join(
			[
				"%s_access"%(n.lower(), )
				for n in config["access"].keys()
				if "is_dst" in config["access"][n] and config["access"][n]["is_dst"] == True
			]
		,)
	)

	parser += "\n\t\timm_access : NUMBER ;\n"

	for sub_rule_name, sub_config in config["access"].items():
		parser_sub_rules = ""
		sub_rule_name = "%s_access"%(sub_rule_name.lower(), )
		parser += "\n\t\t%s :"%(sub_rule_name, )
		handle_mnemonics  (sub_rule_name, sub_config)
		handle_com_selext (sub_rule_name, sub_config)
		handle_address    (sub_rule_name, sub_config)
		handle_operands   (sub_rule_name, sub_config)
		handle_mods       (sub_rule_name, sub_config)
		parser += " ;\n"
		parser += parser_sub_rules + "\n"

#########################################################################

def handle_mnemonics(rule_name, config):
	global parser, lexer, keywords, parser_sub_rules

	if "mnemonics" not in config or len(config["mnemonics"]) == 0:
		raise ValueError("No mnemoics provides for rule %s\n"%(rule_name, ))

	# Generate rule fragment
	parser += " %s_mnemonic"%(rule_name, )
	parser_sub_rules += "\t\t%s_mnemonic : %s ;\n"%(rule_name, " | ".join([mnemonic.upper() for mnemonic in config["mnemonics"] ]))

	# Record keyword to lexer later
	for m in config["mnemonics"]:
		keywords.add(m.upper())

def handle_com_selext(rule_name, config):
	global parser, lexer, keywords, parser_sub_rules

	if "comp_select" in config and len(config["comp_select"]) != 0:
		# Add syntac to rule
		parser += " OSB  %s_comp_select CSB"%(rule_name, )

		# create sub rule
		for select_type in config["comp_select"]:
			if select_type not in data_types:
				raise ValueError("Unknown component select type, " + str(select_type))
			parser_sub_rules += "\t\t%s_comp_select : %s ;\n"%(rule_name, " | ".join(config["comp_select"]))

def handle_address(rule_name, config):
	global parser, lexer, keywords, parser_sub_rules

	if "address" in config and len(config["address"]) != 0:
		# Add syntac to rule
		parser += " OSB  %s_address CSB"%(rule_name, )

		# create sub rule
		for address_type in config["address"]:
			if address_type not in data_types:
				raise ValueError("Unknown address type, " + str(address_type))
			parser_sub_rules += "\t\t%s_address : %s ;\n"%(rule_name, " | ".join(config["address"]))

def handle_operands(rule_name, config):
	global parser, lexer, keywords, parser_sub_rules

	if "operands" in config and len(config["operands"]) != 0:
		parser += " ORB"

		# Interate over all operands
		for index, operand_types in enumerate(config["operands"]):
			if index != 0: parser += " COMMA"
			parser += " %s_operand_%i"%(rule_name, index)

			# create sub rule
			for operand_type in operand_types:
				if operand_type not in data_types:
					raise ValueError("Unknown address type, " + str(operand_type))
			parser_sub_rules += "\t\t%s_operand_%i : %s ;\n"%(rule_name, index, " | ".join(operand_types))

		parser += " CRB"

def handle_mods(rule_name, config):
	global parser, lexer, keywords, parser_sub_rules

	mod_types = []

	if "mods" in config and len(config["mods"]) != 0:
		mod_types.append("%s_mod"%(rule_name, ))
	if "timing_mods" in config and config["timing_mods"] == True:
		mod_types.append("timing_mod")

	if len(mod_types) != 0:
		parser += " ( OAB ( %s ) ( COMMA ( %s ) )* CAB )?"%(" | ".join(mod_types), " | ".join(mod_types))

	if "mods" in config and len(config["mods"]) != 0:
		# create sub rule
		mod_options = []
		for mod in config["mods"]:
			keywords.add(mod["flag"].upper())
			if "value" in mod:
				if mod["value"] not in ["STRING", "NUMBER"]:
					raise ValueError("Mod Values can only be STRING or NUMBER.receice %s"%(mod["value"], ))
				mod_options.append("( %s COLON %s )"%(mod["flag"].upper(), mod["value"]))
			else:
				mod_options.append("%s"%(mod["flag"].upper(),))


		parser_sub_rules += "\t\t%s_mod : %s ;\n"%(rule_name, " | ".join(mod_options))

#########################################################################

import os

if __name__ == "__main__":
	with open("FPE_grammar.json", "r") as f:
		config = json.loads(f.read())

	keywords = set()
	parser_preamble(config)

	# Generate wrapper rules
	if "wrapper" in config.keys() and len(config["wrapper"]) != 0:
		create_wrapper_rules()

	# Generate statement rules
	if "operation" in config.keys() and len(config["operation"]) != 0:
		create_operation_rules()

	# Generate access rules
	if "access" in config.keys() and len(config["access"]) != 0:
		generate_access_rules()

	generater_lexer ()

	with open("..\\grammar\\FPE_assembly.g4", "w") as f:
		f.write(parser + lexer)

	os.system("java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 ..\\grammar\\FPE_assembly.g4 -o ..\\grammar\\")
