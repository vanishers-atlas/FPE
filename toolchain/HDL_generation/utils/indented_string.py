SHIFT_OUT = chr(0x0E)
SHIFT_IN  = chr(0x0F)

class IndentedString:
    def __init__(self):
        self.str = ""

    def drop_last_X(this, X):
        this.str = this.str[0:-X]

    def append_string(this, string):
        result = IndentedString()
        result.str = this.str

        # Process string chars
        it = iter(string)
        try:
            while True:
                char = it.__next__()

                # Covert custom escape sequences into shift chars
                if char == "\\":
                    try:
                        char = it.__next__()
                        if char == ">":
                            result.str += SHIFT_IN
                        elif char == "<":
                            result.str += SHIFT_OUT
                        else:
                            result.str += "\\" + char
                    except StopIteration:
                        result.str += "\\"
                # Copy across non escape sequences chars
                else:
                    result.str += char
        except Exception as e:
            pass
        return result

    def concate(A, B):
        result = IndentedString()
        result.str = A.str + B.str
        return result

    def __add__(A, B):
        if type(B) == type(""):
            return A.append_string(B)
        else:
            return A.concate(B)

    def __str__(this):
        str = ""
        indentation = 0

        for char in this.str:
            # Track shift ins
            if char == SHIFT_IN:
                indentation += 1
                str += "\t"
            # Track shift outs
            elif char == SHIFT_OUT:
                if str[-1] == "\t":
                    str = str[0:-1]

                indentation -= 1
                if(indentation < 0):
                    import warnings
                    warnings.warn("Indentation went negitive be negitive\n")
            # Indent at the start new lines
            elif char == "\n":
                str += "\n"
                for i in range(indentation):
                    str += "\t"
            #Add other chars to string
            else:
                str += char
        return str
