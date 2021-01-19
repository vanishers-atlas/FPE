def connect_signals(src, src_width, dst_width, signal_padding):
    if dst_width > src_width:
        if signal_padding == "unsigned":
            return "(%s, others => '0')"%(
                ", ".join(
                    [
                        "%i => %s(%i)"%(
                            i,
                            src,
                            i
                        )
                        for i in range(src_width)
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
                        for i in range(src_width)
                    ]
                ),
                src,
                src
            )
        else:
            raise ValueError("%s not supported" %(signal_padding))
    elif dst_width == src_width:
        return src
    else: # dst_width < src_width
        return "(%s)"%(
            ", ".join(
                [
                    "%i => %s(%i)"%(
                        i,
                        src,
                        i
                    )
                    for i in range(dst_width)
                ]
            )
        )
