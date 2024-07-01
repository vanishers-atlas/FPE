# Generated from .\templated_json_parser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .templated_json_parser import templated_json_parser
else:
    from templated_json_parser import templated_json_parser

# This class defines a complete listener for a parse tree produced by templated_json_parser.
class templated_json_parserListener(ParseTreeListener):

    # Enter a parse tree produced by templated_json_parser#string.
    def enterString(self, ctx:templated_json_parser.StringContext):
        pass

    # Exit a parse tree produced by templated_json_parser#string.
    def exitString(self, ctx:templated_json_parser.StringContext):
        pass


    # Enter a parse tree produced by templated_json_parser#escaped_chars.
    def enterEscaped_chars(self, ctx:templated_json_parser.Escaped_charsContext):
        pass

    # Exit a parse tree produced by templated_json_parser#escaped_chars.
    def exitEscaped_chars(self, ctx:templated_json_parser.Escaped_charsContext):
        pass


    # Enter a parse tree produced by templated_json_parser#obj.
    def enterObj(self, ctx:templated_json_parser.ObjContext):
        pass

    # Exit a parse tree produced by templated_json_parser#obj.
    def exitObj(self, ctx:templated_json_parser.ObjContext):
        pass


    # Enter a parse tree produced by templated_json_parser#entry.
    def enterEntry(self, ctx:templated_json_parser.EntryContext):
        pass

    # Exit a parse tree produced by templated_json_parser#entry.
    def exitEntry(self, ctx:templated_json_parser.EntryContext):
        pass


    # Enter a parse tree produced by templated_json_parser#value.
    def enterValue(self, ctx:templated_json_parser.ValueContext):
        pass

    # Exit a parse tree produced by templated_json_parser#value.
    def exitValue(self, ctx:templated_json_parser.ValueContext):
        pass


    # Enter a parse tree produced by templated_json_parser#value_json.
    def enterValue_json(self, ctx:templated_json_parser.Value_jsonContext):
        pass

    # Exit a parse tree produced by templated_json_parser#value_json.
    def exitValue_json(self, ctx:templated_json_parser.Value_jsonContext):
        pass


    # Enter a parse tree produced by templated_json_parser#value_placehold.
    def enterValue_placehold(self, ctx:templated_json_parser.Value_placeholdContext):
        pass

    # Exit a parse tree produced by templated_json_parser#value_placehold.
    def exitValue_placehold(self, ctx:templated_json_parser.Value_placeholdContext):
        pass


    # Enter a parse tree produced by templated_json_parser#value_expr.
    def enterValue_expr(self, ctx:templated_json_parser.Value_exprContext):
        pass

    # Exit a parse tree produced by templated_json_parser#value_expr.
    def exitValue_expr(self, ctx:templated_json_parser.Value_exprContext):
        pass


    # Enter a parse tree produced by templated_json_parser#expr.
    def enterExpr(self, ctx:templated_json_parser.ExprContext):
        pass

    # Exit a parse tree produced by templated_json_parser#expr.
    def exitExpr(self, ctx:templated_json_parser.ExprContext):
        pass


    # Enter a parse tree produced by templated_json_parser#expr_leaf.
    def enterExpr_leaf(self, ctx:templated_json_parser.Expr_leafContext):
        pass

    # Exit a parse tree produced by templated_json_parser#expr_leaf.
    def exitExpr_leaf(self, ctx:templated_json_parser.Expr_leafContext):
        pass


    # Enter a parse tree produced by templated_json_parser#value_concat.
    def enterValue_concat(self, ctx:templated_json_parser.Value_concatContext):
        pass

    # Exit a parse tree produced by templated_json_parser#value_concat.
    def exitValue_concat(self, ctx:templated_json_parser.Value_concatContext):
        pass


    # Enter a parse tree produced by templated_json_parser#concat_leaf.
    def enterConcat_leaf(self, ctx:templated_json_parser.Concat_leafContext):
        pass

    # Exit a parse tree produced by templated_json_parser#concat_leaf.
    def exitConcat_leaf(self, ctx:templated_json_parser.Concat_leafContext):
        pass


