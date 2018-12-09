from enum import Enum, auto
class dataTypes(Enum):
    string = auto()
    number = auto()

class ASNodeType(Enum):
    #Sub Blocks
    literal  = auto()
    variable = auto()
    expression  = auto()
    conditional = auto()

    #Script Blocks
    codeBlock  = auto()
    sequential = auto()
class ASNode():
    def __init__(this, type):
        this.type = type

    def addChild(this, childNode):
        try:
            this.children.append(childNode)
        except Exception as e:
            this.children = []
            this.children.append(childNode)

import re

def createASTree_Expression(VCString):
    return ASNode(ASNodeType.expression)

def createASTree_CodeBlock(tok):
    root = ASNode(ASNodeType.codeBlock)

    #Check for openning {
    tok.skipWhitespace()
    if tok.checkforTokens( (re.compile("{"),) )[0][0] != 1:
        print("Line %i Col %i: Error: Expected {" % tok.location())
        exit(1)
    tok.incIndex(1)

    regexs = (
        re.compile("[^@}^]*"), #Regex for code str literal
        re.compile("\^[\d\D]"),#Regex for catching char escapses in code str literal
        re.compile("@"),    #Regex for dropin statements
        re.compile("}")     #Regex for end of codeBlock statements
        )

    #Loop until returned out by finding a } token
    buff = ""
    while True:
        #Get next token
        tokens = tok.checkforTokens(regexs)

        #handle found tokens
        #Handle code str literal token
        if tokens[0][0] != 0:
            tok.incIndex(tokens[0][0])
            buff += tokens[0][1]
        #Handle char escapes
        elif tokens[1][0] != 0:
            escapedChar = tokens[1][1][1]
            #Warning about unknown char escapes
            if escapedChar != "}" and escapedChar != "^" and escapedChar != "@":
                print("Line %i Col %i: Warning: Unknown Char escape, %s, reading as %s" % (tok.location() + (tokens[1][1],tokens[1][1][1])) )

            buff += escapedChar
            tok.incIndex(2)
        #Handle dropin expression statement token
        elif tokens[2][0] != 0:
            #Finish preceding str literal node
            if buff != "":
                node = ASNode(ASNodeType.literal)
                node.dataType = dataTypes.string
                node.data = buff
                root.addChild(node)
                buff = ""
            tok.incIndex(1)
            root.addChild(createASTree_Expression(tok))
        #Handle closing }
        elif tokens[3][0] != 0:
            #Finish str literal node
            if buff != "":
                node = ASNode(ASNodeType.literal)
                node.dataType = dataTypes.string
                node.data = buff
                root.addChild(node)
                buff = ""
            tok.incIndex(1)
            return root
        #No valids tokens found
        else:
            print("Line %i Col %i: Error: No valid tokens could be found" % tok.location())
            exit(1)

import tokenizer
def createASTree(VirtualCodeString):
    tok = tokenizer.tokenizer(VirtualCodeString)

    root = ASNode(ASNodeType.sequential)

    regexs = (
        re.compile("(int|float|string)[ \t]"), #Regex for dataTypes
        re.compile("code[\s{]"), #Regex for codeBlock
        )

    #Loop until full code is processed
    tok.skipWhitespace()
    while tok.tokensRemain():
        print("Looping at rode")
        #Get next token
        tokens = tok.checkforTokens(regexs)

        #handle found tokens
        #Found code block start
        if tokens[0][0] == 4:
            print("Code block token found")
            tok.incIndex(4)
            root.addChild(createASTree_CodeBlock(tok))
        #No valids tokens found
        else:
            print("Line %i Col %i: Error: No valid tokens could be found" % tok.location())
            exit(1)

        #Skip whitespace
        tok.skipWhitespace()

    return root
