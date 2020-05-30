def ctx_start(ctx):
    return "Line %i Col %i"%(
        ctx.start.line,
        ctx.start.column,
    )

def ctx_end(ctx):
    return "Line %i Col %i"%(
        ctx.end.line,
        ctx.end.column,
    )
