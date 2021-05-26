############################################################################
# A hyper grammar extractor used to check all identiers passed as parameter
# keys within a component declaration are unique with that component
# declaration
############################################################################
# Assumes only that the program passes the antlr grammar
############################################################################

from antlr4 import ParseTreeListener
from FPE.toolchain import FPE_assembly as asm_utils

class extractor(ParseTreeListener):

    def __init__(this):
        pass

    def final_check(this):
        pass

    def enterState_component(this, ctx):
        declared_parameters = {}
        for parameter_ctx in ctx.state_component_parameter():
            parameter = asm_utils.token_to_text(parameter_ctx.para_name)

            # If first occurance of parameter, store in case of second occurance
            if parameter not in declared_parameters.keys():
                declared_parameters[parameter] = parameter_ctx
            # If second occurance of parameter, report error and exit
            else:
                raise SyntaxError( "Multiple declatation of the same parameter, %s, at %s and %s\n"%(
                        parameter,
                        asm_utils.ctx_start(declared_parameters[parameter]),
                        asm_utils.ctx_start(parameter_ctx)
                    )
                )
