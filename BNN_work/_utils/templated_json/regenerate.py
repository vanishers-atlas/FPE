import os
os.system("java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 .\\templated_json_lexer.g4 -o .")
os.system("java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 .\\templated_json_parser.g4 -o .")
