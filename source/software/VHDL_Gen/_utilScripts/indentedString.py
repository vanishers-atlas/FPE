import os

SHIFT_OUT = chr(0x0E)
SHIFT_IN  = chr(0x0F)

class indentedString:
    def __init__(self):
        self.str = ""
        self.newline = True

    def addString(this, string):
        result = indentedString()
        result.str = this.str
        result.newline = this.newline

        #Process string
        for char in string:
            #Convert starting tabs and backspaces
            if result.newline:
                if char == "\t":
                    result.str += SHIFT_IN
                    continue
                elif char == "\b":
                    result.str += SHIFT_OUT
                    continue
                else:
                    result.newline = False

            #Add other chars to string
            result.str += char
            if char == "\n":
                result.newline = True
        return result

    def concateSections(A, B):
        result = indentedString()
        result.str  = A.str
        result.str += B.str
        result.newline = B.newline
        return result

    def __add__(A, B):
        if type(B) == type(""):
            return A.addString(B)
        else:
            return A.concateSections(B)

    def __str__(this):
        str = ""
        indentation = 0
        newline = True
        for char in this.str:
            #Convert starting tabs and backspaces
            if newline:
                if char == SHIFT_IN:
                    indentation += 1
                    continue
                elif char == SHIFT_OUT:
                    indentation -= 1
                    #if(indentation < 0):
                        #raise SyntaxWarning("Indentation can't be negitive\n")
                    continue
                else:
                    newline = False

                #Indent at the start of the line
                for i in range(indentation):
                    str += "\t"

            #Add other chars to string
            str += char
            if char == "\n":
                newline = True
        return str
