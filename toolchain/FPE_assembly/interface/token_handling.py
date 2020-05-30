import antlr4

def token_to_text(token):
    if type(token) == antlr4.tree.Tree.TerminalNodeImpl:
        raise NotImplementedError("%s tokens are Unsupported"%(type(token)))
    return token.source[1].strdata[token.start:token.stop + 1]
