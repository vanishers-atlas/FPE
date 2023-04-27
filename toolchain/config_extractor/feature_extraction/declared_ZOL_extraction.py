# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain import utils  as tc_utils

####################################################################

class extractor(ParseTreeListener):

    def __init__(this, program_context, config):
        this.program_context = program_context
        this.config = config
        this.declared_ZOLs = {}

    def get_updated_config(this):
        this.config["program_flow"]["declared_ZOLs"] = this.declared_ZOLs
        return this.config


    def enterState_component(this, ctx):
        com_type = asm_utils.token_to_text(ctx.com_type)

        if   com_type == "ZOL_ripple":
            this.state_component_ZOL_ripple(ctx)
        elif com_type == "ZOL_cascade":
            this.state_component_ZOL_cascade(ctx)
        elif com_type == "ZOL_counter":
            this.state_component_ZOL_counter(ctx)
        else:
            raise ValueError("Unknown Component type, %s, at %s"%(
                com_type,
                asm_utils.ctx_start(ctx)
            ) )


    def state_component_ZOL_ripple(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        overwrites = None
        seekable = None

        for para_ctx in ctx.state_component_parameter():
            para_name = asm_utils.token_to_text(para_ctx.para_name)

            if para_name == "overwrites":
                try:
                    overwrites = asm_utils.evaluate_expr(para_ctx.expr(), this.program_context)
                except Exception as e:
                    raise SyntaxError("Zol ripple overwrites must be an expression")
            elif para_name == "seekable":
                try:
                    seekable = asm_utils.token_to_text(para_ctx.BOOL()).lower() =="true"
                except Exception as e:
                    raise SyntaxError("Zol ripple seekable must be a boolean")
            else:
                raise SyntaxError("Zol ripple Component declaration with unknown parameter, %s"%(para_name))

        if overwrites == None:
            raise SyntaxError("Zol ripple Component declaration without overwrites parameter")
        if seekable == None:
            raise SyntaxError("Zol ripple Component declaration without seekable parameter")

        this.declared_ZOLs[com_name] = {
            "tracker_type" : "ripple",
            "overwrites" : overwrites,
            "seekable" : seekable,
        }

    def state_component_ZOL_cascade(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        overwrites = None
        seekable = None

        for para_ctx in ctx.state_component_parameter():
            para_name = asm_utils.token_to_text(para_ctx.para_name)

            if para_name == "overwrites":
                try:
                    overwrites = asm_utils.evaluate_expr(para_ctx.expr(), this.program_context)
                except Exception as e:
                    raise SyntaxError("Zol cascade overwrites must be an expression")
            elif para_name == "seekable":
                try:
                    seekable = asm_utils.token_to_text(para_ctx.BOOL()).lower() =="true"
                except Exception as e:
                    raise SyntaxError("Zol cascade seekable must be a boolean")
            else:
                raise SyntaxError("Zol cascade Component declaration with unknown parameter, %s"%(para_name))

        if overwrites == None:
            raise SyntaxError("Zol cascade Component declaration without overwrites parameter")
        if seekable == None:
            raise SyntaxError("Zol cascade Component declaration without seekable parameter")

        this.declared_ZOLs[com_name] = {
            "tracker_type" : "cascade",
            "overwrites" : overwrites,
            "seekable" : seekable,
        }

    def state_component_ZOL_counter(this, ctx):
        com_name = asm_utils.token_to_text(ctx.com_name.IDENTIFER())

        overwrites = None
        seekable = None
        settable = None

        for para_ctx in ctx.state_component_parameter():
            para_name = asm_utils.token_to_text(para_ctx.para_name)

            if para_name == "overwrites":
                try:
                    overwrites = asm_utils.evaluate_expr(para_ctx.expr(), this.program_context)
                except Exception as e:
                    raise SyntaxError("Zol counter overwrites must be an expression")
            elif para_name == "settable":
                try:
                    settable = asm_utils.token_to_text(para_ctx.BOOL()).lower() =="true"
                except Exception as e:
                    raise SyntaxError("Zol counter settable must be a boolean")
            elif para_name == "seekable":
                try:
                    seekable = asm_utils.token_to_text(para_ctx.BOOL()).lower() =="true"
                except Exception as e:
                    raise SyntaxError("Zol counter seekable must be a boolean")
            else:
                raise SyntaxError("Zol counter Component declaration with unknown parameter, %s"%(para_name))

        if overwrites == None:
            raise SyntaxError("Zol counter Component declaration without overwrites parameter")
        if seekable == None:
            raise SyntaxError("Zol counter Component declaration without seekable parameter")
        if settable == None:
            raise SyntaxError("Zol counter Component declaration without settable parameter")

        this.declared_ZOLs[com_name] = {
            "tracker_type" : "counter",
            "overwrites" : overwrites,
            "seekable" : seekable,
            "settable" : settable,
        }
