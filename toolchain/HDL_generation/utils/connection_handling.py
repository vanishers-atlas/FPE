def connect_signals(src, src_width, dst_width):
    if dst_width > src_width:
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
