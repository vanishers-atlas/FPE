import antlr4
from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl


def token_to_text(token):
    if   type(token) == CommonToken:
        return token.source[1].strdata[token.start:token.stop + 1]
    elif type(token) == TerminalNodeImpl:
        return token.getText()
    else:
        raise TypeError("Unsupported token type, %s"%(type(token), ) )
