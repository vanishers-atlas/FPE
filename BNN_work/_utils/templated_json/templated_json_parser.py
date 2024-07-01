# Generated from .\templated_json_parser.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3 ")
        buf.write("m\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\3\2")
        buf.write("\3\2\7\2\36\n\2\f\2\16\2!\13\2\3\2\3\2\3\3\3\3\3\4\3\4")
        buf.write("\3\4\3\4\7\4+\n\4\f\4\16\4.\13\4\3\4\3\4\3\5\3\5\3\5\3")
        buf.write("\5\3\6\3\6\3\6\3\6\5\6:\n\6\3\7\3\7\3\7\3\7\3\7\5\7A\n")
        buf.write("\7\3\b\3\b\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\5\n")
        buf.write("O\n\n\3\n\3\n\3\n\3\n\3\n\3\n\7\nW\n\n\f\n\16\nZ\13\n")
        buf.write("\3\13\3\13\3\13\5\13_\n\13\3\f\3\f\3\f\6\fd\n\f\r\f\16")
        buf.write("\fe\3\r\3\r\3\r\5\rk\n\r\3\r\2\3\22\16\2\4\6\b\n\f\16")
        buf.write("\20\22\24\26\30\2\5\4\2\26\33\35\36\3\2\f\16\3\2\17\20")
        buf.write("\2r\2\32\3\2\2\2\4$\3\2\2\2\6&\3\2\2\2\b\61\3\2\2\2\n")
        buf.write("9\3\2\2\2\f@\3\2\2\2\16B\3\2\2\2\20D\3\2\2\2\22N\3\2\2")
        buf.write("\2\24^\3\2\2\2\26`\3\2\2\2\30j\3\2\2\2\32\37\7\25\2\2")
        buf.write("\33\36\5\4\3\2\34\36\7 \2\2\35\33\3\2\2\2\35\34\3\2\2")
        buf.write("\2\36!\3\2\2\2\37\35\3\2\2\2\37 \3\2\2\2 \"\3\2\2\2!\37")
        buf.write("\3\2\2\2\"#\7\37\2\2#\3\3\2\2\2$%\t\2\2\2%\5\3\2\2\2&")
        buf.write("\'\7\b\2\2\',\5\b\5\2()\7\6\2\2)+\5\b\5\2*(\3\2\2\2+.")
        buf.write("\3\2\2\2,*\3\2\2\2,-\3\2\2\2-/\3\2\2\2.,\3\2\2\2/\60\7")
        buf.write("\t\2\2\60\7\3\2\2\2\61\62\5\2\2\2\62\63\7\7\2\2\63\64")
        buf.write("\5\n\6\2\64\t\3\2\2\2\65:\5\f\7\2\66:\5\16\b\2\67:\5\26")
        buf.write("\f\28:\5\20\t\29\65\3\2\2\29\66\3\2\2\29\67\3\2\2\298")
        buf.write("\3\2\2\2:\13\3\2\2\2;A\7\3\2\2<A\7\4\2\2=A\7\5\2\2>A\5")
        buf.write("\2\2\2?A\5\6\4\2@;\3\2\2\2@<\3\2\2\2@=\3\2\2\2@>\3\2\2")
        buf.write("\2@?\3\2\2\2A\r\3\2\2\2BC\7\24\2\2C\17\3\2\2\2DE\7\n\2")
        buf.write("\2EF\5\22\n\2FG\7\13\2\2G\21\3\2\2\2HI\b\n\1\2IJ\7\n\2")
        buf.write("\2JK\5\22\n\2KL\7\13\2\2LO\3\2\2\2MO\5\24\13\2NH\3\2\2")
        buf.write("\2NM\3\2\2\2OX\3\2\2\2PQ\f\5\2\2QR\t\3\2\2RW\5\22\n\6")
        buf.write("ST\f\4\2\2TU\t\4\2\2UW\5\22\n\5VP\3\2\2\2VS\3\2\2\2WZ")
        buf.write("\3\2\2\2XV\3\2\2\2XY\3\2\2\2Y\23\3\2\2\2ZX\3\2\2\2[_\5")
        buf.write("\2\2\2\\_\7\24\2\2]_\7\3\2\2^[\3\2\2\2^\\\3\2\2\2^]\3")
        buf.write("\2\2\2_\25\3\2\2\2`c\5\30\r\2ab\7\21\2\2bd\5\30\r\2ca")
        buf.write("\3\2\2\2de\3\2\2\2ec\3\2\2\2ef\3\2\2\2f\27\3\2\2\2gk\5")
        buf.write("\2\2\2hk\5\22\n\2ik\7\24\2\2jg\3\2\2\2jh\3\2\2\2ji\3\2")
        buf.write("\2\2k\31\3\2\2\2\r\35\37,9@NVX^ej")
        return buf.getvalue()


class templated_json_parser ( Parser ):

    grammarFileName = "templated_json_parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'null'", "','", 
                     "':'", "'{'", "'}'", "'('", "')'", "'^'", "'*'", "'/'", 
                     "'+'", "'-'", "'&'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'\\\"'", "'\\\\'", "'\\/'", "'\\b'", 
                     "'\\f'", "'\\n'", "'\\r'", "'\\t'" ]

    symbolicNames = [ "<INVALID>", "NUM", "BOOL", "NULL", "COMMA", "COLON", 
                      "OCB", "CCB", "ORB", "CRB", "EXP", "MUL", "DIV", "ADD", 
                      "SUB", "AMP", "SING_LINE_COMMENT", "WHITESPACE", "PLACEHOLDER", 
                      "OSQ", "EQM", "EBSL", "EFSL", "EBSP", "EFF", "ENL", 
                      "ECR", "EHT", "EHC", "CSQ", "NEC" ]

    RULE_string = 0
    RULE_escaped_chars = 1
    RULE_obj = 2
    RULE_entry = 3
    RULE_value = 4
    RULE_value_json = 5
    RULE_value_placehold = 6
    RULE_value_expr = 7
    RULE_expr = 8
    RULE_expr_leaf = 9
    RULE_value_concat = 10
    RULE_concat_leaf = 11

    ruleNames =  [ "string", "escaped_chars", "obj", "entry", "value", "value_json", 
                   "value_placehold", "value_expr", "expr", "expr_leaf", 
                   "value_concat", "concat_leaf" ]

    EOF = Token.EOF
    NUM=1
    BOOL=2
    NULL=3
    COMMA=4
    COLON=5
    OCB=6
    CCB=7
    ORB=8
    CRB=9
    EXP=10
    MUL=11
    DIV=12
    ADD=13
    SUB=14
    AMP=15
    SING_LINE_COMMENT=16
    WHITESPACE=17
    PLACEHOLDER=18
    OSQ=19
    EQM=20
    EBSL=21
    EFSL=22
    EBSP=23
    EFF=24
    ENL=25
    ECR=26
    EHT=27
    EHC=28
    CSQ=29
    NEC=30

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StringContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OSQ(self):
            return self.getToken(templated_json_parser.OSQ, 0)

        def CSQ(self):
            return self.getToken(templated_json_parser.CSQ, 0)

        def escaped_chars(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(templated_json_parser.Escaped_charsContext)
            else:
                return self.getTypedRuleContext(templated_json_parser.Escaped_charsContext,i)


        def NEC(self, i:int=None):
            if i is None:
                return self.getTokens(templated_json_parser.NEC)
            else:
                return self.getToken(templated_json_parser.NEC, i)

        def getRuleIndex(self):
            return templated_json_parser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)




    def string(self):

        localctx = templated_json_parser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_string)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(templated_json_parser.OSQ)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << templated_json_parser.EQM) | (1 << templated_json_parser.EBSL) | (1 << templated_json_parser.EFSL) | (1 << templated_json_parser.EBSP) | (1 << templated_json_parser.EFF) | (1 << templated_json_parser.ENL) | (1 << templated_json_parser.EHT) | (1 << templated_json_parser.EHC) | (1 << templated_json_parser.NEC))) != 0):
                self.state = 27
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [templated_json_parser.EQM, templated_json_parser.EBSL, templated_json_parser.EFSL, templated_json_parser.EBSP, templated_json_parser.EFF, templated_json_parser.ENL, templated_json_parser.EHT, templated_json_parser.EHC]:
                    self.state = 25
                    self.escaped_chars()
                    pass
                elif token in [templated_json_parser.NEC]:
                    self.state = 26
                    self.match(templated_json_parser.NEC)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
            self.match(templated_json_parser.CSQ)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Escaped_charsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQM(self):
            return self.getToken(templated_json_parser.EQM, 0)

        def EBSL(self):
            return self.getToken(templated_json_parser.EBSL, 0)

        def EFSL(self):
            return self.getToken(templated_json_parser.EFSL, 0)

        def EBSP(self):
            return self.getToken(templated_json_parser.EBSP, 0)

        def EFF(self):
            return self.getToken(templated_json_parser.EFF, 0)

        def ENL(self):
            return self.getToken(templated_json_parser.ENL, 0)

        def EHC(self):
            return self.getToken(templated_json_parser.EHC, 0)

        def EHT(self):
            return self.getToken(templated_json_parser.EHT, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_escaped_chars

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEscaped_chars" ):
                listener.enterEscaped_chars(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEscaped_chars" ):
                listener.exitEscaped_chars(self)




    def escaped_chars(self):

        localctx = templated_json_parser.Escaped_charsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_escaped_chars)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << templated_json_parser.EQM) | (1 << templated_json_parser.EBSL) | (1 << templated_json_parser.EFSL) | (1 << templated_json_parser.EBSP) | (1 << templated_json_parser.EFF) | (1 << templated_json_parser.ENL) | (1 << templated_json_parser.EHT) | (1 << templated_json_parser.EHC))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OCB(self):
            return self.getToken(templated_json_parser.OCB, 0)

        def entry(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(templated_json_parser.EntryContext)
            else:
                return self.getTypedRuleContext(templated_json_parser.EntryContext,i)


        def CCB(self):
            return self.getToken(templated_json_parser.CCB, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(templated_json_parser.COMMA)
            else:
                return self.getToken(templated_json_parser.COMMA, i)

        def getRuleIndex(self):
            return templated_json_parser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)




    def obj(self):

        localctx = templated_json_parser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(templated_json_parser.OCB)
            self.state = 37
            self.entry()
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==templated_json_parser.COMMA:
                self.state = 38
                self.match(templated_json_parser.COMMA)
                self.state = 39
                self.entry()
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 45
            self.match(templated_json_parser.CCB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EntryContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.key = None # StringContext

        def COLON(self):
            return self.getToken(templated_json_parser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(templated_json_parser.ValueContext,0)


        def string(self):
            return self.getTypedRuleContext(templated_json_parser.StringContext,0)


        def getRuleIndex(self):
            return templated_json_parser.RULE_entry

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEntry" ):
                listener.enterEntry(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEntry" ):
                listener.exitEntry(self)




    def entry(self):

        localctx = templated_json_parser.EntryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_entry)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            localctx.key = self.string()
            self.state = 48
            self.match(templated_json_parser.COLON)
            self.state = 49
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value_json(self):
            return self.getTypedRuleContext(templated_json_parser.Value_jsonContext,0)


        def value_placehold(self):
            return self.getTypedRuleContext(templated_json_parser.Value_placeholdContext,0)


        def value_concat(self):
            return self.getTypedRuleContext(templated_json_parser.Value_concatContext,0)


        def value_expr(self):
            return self.getTypedRuleContext(templated_json_parser.Value_exprContext,0)


        def getRuleIndex(self):
            return templated_json_parser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = templated_json_parser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 55
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.value_json()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.value_placehold()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 53
                self.value_concat()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 54
                self.value_expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Value_jsonContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUM(self):
            return self.getToken(templated_json_parser.NUM, 0)

        def BOOL(self):
            return self.getToken(templated_json_parser.BOOL, 0)

        def NULL(self):
            return self.getToken(templated_json_parser.NULL, 0)

        def string(self):
            return self.getTypedRuleContext(templated_json_parser.StringContext,0)


        def obj(self):
            return self.getTypedRuleContext(templated_json_parser.ObjContext,0)


        def getRuleIndex(self):
            return templated_json_parser.RULE_value_json

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue_json" ):
                listener.enterValue_json(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue_json" ):
                listener.exitValue_json(self)




    def value_json(self):

        localctx = templated_json_parser.Value_jsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_value_json)
        try:
            self.state = 62
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [templated_json_parser.NUM]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(templated_json_parser.NUM)
                pass
            elif token in [templated_json_parser.BOOL]:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.match(templated_json_parser.BOOL)
                pass
            elif token in [templated_json_parser.NULL]:
                self.enterOuterAlt(localctx, 3)
                self.state = 59
                self.match(templated_json_parser.NULL)
                pass
            elif token in [templated_json_parser.OSQ]:
                self.enterOuterAlt(localctx, 4)
                self.state = 60
                self.string()
                pass
            elif token in [templated_json_parser.OCB]:
                self.enterOuterAlt(localctx, 5)
                self.state = 61
                self.obj()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Value_placeholdContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLACEHOLDER(self):
            return self.getToken(templated_json_parser.PLACEHOLDER, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_value_placehold

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue_placehold" ):
                listener.enterValue_placehold(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue_placehold" ):
                listener.exitValue_placehold(self)




    def value_placehold(self):

        localctx = templated_json_parser.Value_placeholdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_value_placehold)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(templated_json_parser.PLACEHOLDER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Value_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ORB(self):
            return self.getToken(templated_json_parser.ORB, 0)

        def expr(self):
            return self.getTypedRuleContext(templated_json_parser.ExprContext,0)


        def CRB(self):
            return self.getToken(templated_json_parser.CRB, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_value_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue_expr" ):
                listener.enterValue_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue_expr" ):
                listener.exitValue_expr(self)




    def value_expr(self):

        localctx = templated_json_parser.Value_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_value_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(templated_json_parser.ORB)
            self.state = 67
            self.expr(0)
            self.state = 68
            self.match(templated_json_parser.CRB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.multiplicative = None # Token
            self.additive = None # Token

        def ORB(self):
            return self.getToken(templated_json_parser.ORB, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(templated_json_parser.ExprContext)
            else:
                return self.getTypedRuleContext(templated_json_parser.ExprContext,i)


        def CRB(self):
            return self.getToken(templated_json_parser.CRB, 0)

        def expr_leaf(self):
            return self.getTypedRuleContext(templated_json_parser.Expr_leafContext,0)


        def EXP(self):
            return self.getToken(templated_json_parser.EXP, 0)

        def MUL(self):
            return self.getToken(templated_json_parser.MUL, 0)

        def DIV(self):
            return self.getToken(templated_json_parser.DIV, 0)

        def ADD(self):
            return self.getToken(templated_json_parser.ADD, 0)

        def SUB(self):
            return self.getToken(templated_json_parser.SUB, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = templated_json_parser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [templated_json_parser.ORB]:
                self.state = 71
                self.match(templated_json_parser.ORB)
                self.state = 72
                self.expr(0)
                self.state = 73
                self.match(templated_json_parser.CRB)
                pass
            elif token in [templated_json_parser.NUM, templated_json_parser.PLACEHOLDER, templated_json_parser.OSQ]:
                self.state = 75
                self.expr_leaf()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 86
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 84
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                    if la_ == 1:
                        localctx = templated_json_parser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 78
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 79
                        localctx.multiplicative = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << templated_json_parser.EXP) | (1 << templated_json_parser.MUL) | (1 << templated_json_parser.DIV))) != 0)):
                            localctx.multiplicative = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 80
                        self.expr(4)
                        pass

                    elif la_ == 2:
                        localctx = templated_json_parser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 81
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 82
                        localctx.additive = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==templated_json_parser.ADD or _la==templated_json_parser.SUB):
                            localctx.additive = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 83
                        self.expr(3)
                        pass

             
                self.state = 88
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Expr_leafContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(templated_json_parser.StringContext,0)


        def PLACEHOLDER(self):
            return self.getToken(templated_json_parser.PLACEHOLDER, 0)

        def NUM(self):
            return self.getToken(templated_json_parser.NUM, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_expr_leaf

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_leaf" ):
                listener.enterExpr_leaf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_leaf" ):
                listener.exitExpr_leaf(self)




    def expr_leaf(self):

        localctx = templated_json_parser.Expr_leafContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_expr_leaf)
        try:
            self.state = 92
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [templated_json_parser.OSQ]:
                self.enterOuterAlt(localctx, 1)
                self.state = 89
                self.string()
                pass
            elif token in [templated_json_parser.PLACEHOLDER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 90
                self.match(templated_json_parser.PLACEHOLDER)
                pass
            elif token in [templated_json_parser.NUM]:
                self.enterOuterAlt(localctx, 3)
                self.state = 91
                self.match(templated_json_parser.NUM)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Value_concatContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def concat_leaf(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(templated_json_parser.Concat_leafContext)
            else:
                return self.getTypedRuleContext(templated_json_parser.Concat_leafContext,i)


        def AMP(self, i:int=None):
            if i is None:
                return self.getTokens(templated_json_parser.AMP)
            else:
                return self.getToken(templated_json_parser.AMP, i)

        def getRuleIndex(self):
            return templated_json_parser.RULE_value_concat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue_concat" ):
                listener.enterValue_concat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue_concat" ):
                listener.exitValue_concat(self)




    def value_concat(self):

        localctx = templated_json_parser.Value_concatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_value_concat)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.concat_leaf()
            self.state = 97 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 95
                self.match(templated_json_parser.AMP)
                self.state = 96
                self.concat_leaf()
                self.state = 99 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==templated_json_parser.AMP):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Concat_leafContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(templated_json_parser.StringContext,0)


        def expr(self):
            return self.getTypedRuleContext(templated_json_parser.ExprContext,0)


        def PLACEHOLDER(self):
            return self.getToken(templated_json_parser.PLACEHOLDER, 0)

        def getRuleIndex(self):
            return templated_json_parser.RULE_concat_leaf

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConcat_leaf" ):
                listener.enterConcat_leaf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConcat_leaf" ):
                listener.exitConcat_leaf(self)




    def concat_leaf(self):

        localctx = templated_json_parser.Concat_leafContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_concat_leaf)
        try:
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 101
                self.string()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.expr(0)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 103
                self.match(templated_json_parser.PLACEHOLDER)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[8] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         




