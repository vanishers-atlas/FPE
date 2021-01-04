from FPE.toolchain.FPE_assembly.grammar.FPE_assemblyParser import FPE_assemblyParser

from FPE.toolchain.FPE_assembly import utils as asm_utils

def evaluate_expr(ctx, program_context):
    if type(ctx) != FPE_assemblyParser.ExprContext:
        raise TypeError("Only takes FPE_assemblyParser.Const_exprContext as input, was passed %s"%(type(ctx)))

    # Handle leaf terms of const_exprs
    if   ctx.expr_operand() != None:
        return evaluate_expr_operand(ctx.expr_operand(), program_context)
    # Handle additive operations
    elif ctx.additive != None:
        # Get sides of the operation
        lhs = evaluate_expr(ctx.expr()[0], program_context)
        rhs = evaluate_expr(ctx.expr()[1], program_context)

        # Lookup operation and carry it out
        operation = asm_utils.token_to_text(ctx.additive)
        if   operation == "+": return lhs + rhs
        elif operation == "-": return lhs - rhs
        else:
            raise NotImplementedError("Const_exprContext with an unhandled additive operation, %s"%(operation) )
    # Handle multiplicative operations
    elif ctx.multiplicative != None:
        # Get sides of the operation
        lhs = evaluate_expr(ctx.expr()[0], program_context)
        rhs = evaluate_expr(ctx.expr()[1], program_context)

        # Lookup operation and carry it out
        operation = asm_utils.token_to_text(ctx.multiplicative)
        if   operation == "*": return lhs * rhs
        elif operation == "/": return int(lhs / rhs)
        elif operation == "%": return lhs % rhs
        else:
            raise NotImplementedError("Const_exprContext with an unhandled multiplicative operation, %s"%(operation) )
    # Handle bracket wrapper const_expr
    elif (   len(ctx.children) == 3
        and ctx.ORB() != None
        and ctx.expr()!= None
        and ctx.CRB() != None
    ):
        return evaluate_expr(ctx.children[1], program_context)
    # Catch un new/handled rules
    else:
        for k,v in ctx.__dict__.items():
            print(k,v)
        raise NotImplementedError("Const_exprContext using an unknown rule")

def evaluate_expr_operand(ctx, program_context):
    if type(ctx) != FPE_assemblyParser.Expr_operandContext:
        raise TypeError("Once takes FPE_assemblyParser.ConstantContext as input")

    operand = ctx.getText()
    if   ctx.DEC_NUM() != None:
        return int(operand, 10)
    elif ctx.BIN_NUM() != None:
        return int(operand[2:], 2)
    elif ctx.OCT_NUM() != None:
        return int(operand[2:], 8)
    elif ctx.HEX_NUM() != None:
        return int(operand[2:], 16)
    elif ctx.IDENTIFER() != None:
        return program_context["constants"][operand]
    else:
        raise NotImplementedError("ConstantContext using an unknown rule")
