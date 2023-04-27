def connect_signals(src, src_width, dst_width, signal_padding):
    if signal_padding == "unsigned":
        return "(%s, others => '0')"%(
            ", ".join(
                [
                    "%i => %s(%i)"%(
                        i,
                        src,
                        i
                    )
                    for i in range(min(src_width, dst_width))
                ]
            )
        )
    elif signal_padding == "signed":
        return "(%s, others => %s(%s'left))" % (
            ", ".join(
                [
                    "%i => %s(%i)" % (
                        i,
                        src,
                        i
                    )
                    for i in range(min(src_width, dst_width))
                ]
            ),
            src,
            src
        )
    else:
        raise ValueError("%s not supported" %(signal_padding))
