# Generated from templated_json.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .templated_json_parser import templated_json_parser
else:
    from templated_json_parser import templated_json_parser

# This class defines a complete listener for a parse tree produced by templated_jsonParser.
class transformionListener(ParseTreeListener):
    def __init__(this, templated_values):
          this.templated_values = templated_values
          this.json = {}
          this.entries = [this.json, ]

    def return_json(this):
      assert len(this.entries) == 1
      return this.json


    def exitEntry(this, ctx):
        assert len(this.entries) >= 2
        key = ctx.key.getText()[1:-1]
        value = this.entries[-1]

        this.entries[-2][key] = value
        this.entries = this.entries[:-1]
        

    def enterValue_json(this, ctx):
        if   ctx.NUM():
            text = ctx.NUM().getText()
            this.entries.append(int(text))
        elif ctx.BOOL():
            text = ctx.BOOL().getText()
            this.entries.append(text.lower == "false")
        elif ctx.string():
            text = ctx.string().getText()
            this.entries.append(text[1:-1])
        elif ctx.NULL():
            this.entries.append(None)
        elif ctx.obj():
            this.entries.append({})
        else:
            raise ValueError("Unknown json_value subrule")

    def enterValue_placehold(this, ctx):
        placeholder = ctx.PLACEHOLDER().getText()[1:]
        try:
            this.entries.append(this.templated_values[placeholder])
        except KeyError as e:
            raise KeyError("Couldn't find requested placeholder, " + placeholder + "in supplied list")

    def enterValue_expr(this, ctx):
        value = evaluate_expr(ctx.expr(), this.templated_values)
        this.entries.append(value)

    def enterValue_concat(this, ctx):
        concat = ""
        for lesf in ctx.concat_leaf():
            if   lesf.string():
                concat += lesf.string().getText()[1:-1]
            elif lesf.expr():
                result = evaluate_expr(lesf.expr(), this.templated_values)
                concat += str(result)
            elif lesf.PLACEHOLDER():
                placeholder = ctx.PLACEHOLDER().getText()[1:]
                try:
                    concat += this.templated_values[placeholder]
                except KeyError as e:
                    raise KeyError("Couldn't find requested placeholder, " + placeholder + "in supplied list")
            else:
                raise NotImplementedError("unknown concat_leaf type")

        assert concat != ""
        this.entries.append(concat)


def evaluate_expr(ctx, templated_values):
    if type(ctx) != templated_json_parser.ExprContext:
        raise TypeError("Only takes templated_jsonParser.ExprContext as input, was passed %s"%(type(ctx)))

    # Handle leaf terms of const_exprs
    if   ctx.expr_leaf() != None:
        leaf_ctx = ctx.expr_leaf()
        if   leaf_ctx.NUM():
            text = leaf_ctx.NUM().getText()
            return int(text)
        elif leaf_ctx.PLACEHOLDER():
            placeholder = leaf_ctx.PLACEHOLDER().getText()[1:]
            try:
                return templated_values[placeholder]
            except KeyError as e:
                raise KeyError("Couldn't find requested placeholder, " + placeholder + "in supplied list")
        else:
            raise NotImplementedError("unknown expr_leaf type")
    # Handle additive operations
    elif ctx.additive != None:
        # Get sides of the operation
        lhs = evaluate_expr(ctx.expr()[0], templated_values)
        rhs = evaluate_expr(ctx.expr()[1], templated_values)

        # Lookup operation and carry it out
        operation = ctx.additive.text
        if   operation == "+": return lhs + rhs
        elif operation == "-": return lhs - rhs
        else:
            raise NotImplementedError("Const_exprContext with an unhandled additive operation, %s"%(operation) )
    # Handle multiplicative operations
    elif ctx.multiplicative != None:
        # Get sides of the operation
        lhs = evaluate_expr(ctx.expr()[0], templated_values)
        rhs = evaluate_expr(ctx.expr()[1], templated_values)

        # Lookup operation and carry it out
        operation = ctx.multiplicative.text
        if   operation == "*": return lhs * rhs
        elif operation == "/": return int(lhs / rhs)
        elif operation == "%": return lhs % rhs
        else:
            raise NotImplementedError("Const_exprContext with an unhandled multiplicative operation, %s"%(operation) )
    # Handle bracket wrapper const_expr
    elif len(ctx.expr()) == 1 and ctx.ORB and ctx.CRB:
        return evaluate_expr(ctx.expr()[0], templated_values)
    # Catch un new/handled rules
    else:
        for k,v in ctx.__dict__.items():
            raise NotImplementedError("Unknown subrule for ExorContext")
