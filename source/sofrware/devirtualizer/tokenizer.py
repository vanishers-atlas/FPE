import re
class tokenizer:
    def setInputStr(this, string):
        this.scr = string
        this.index = 0
        this.line  = 1
        this.pos   = 1

    def __init__(this, string):
        this.setInputStr(string)

    def incIndex(this, numChars):
        incedChars = 0
        #Check for end of string
        while this.index + 1 < len(this.scr) and incedChars < numChars:
            #Handle newlines line and pos
            if this.scr[this.index] == "\n":
                this.line += 1
                this.pos   = 1
            else:
                this.pos += 1

            this.index += 1
            incedChars += 1
        return incedChars

    def skipWhitespace(this):
        while this.scr[this.index].isspace() and this.incIndex(1) == 1:
            pass

    def location(this):
        return (this.line, this.pos)

    def checkforTokens(this, regexs):
        results = []
        for regex in regexs:
            result = regex.match(this.scr, this.index)
            if result:
                results.append((result.span()[1] - result.span()[0], result.group()))
            else:
                results.append((0,""))
        return results

    def tokensRemain(this):
        return this.index + 1 < len(this.scr)
