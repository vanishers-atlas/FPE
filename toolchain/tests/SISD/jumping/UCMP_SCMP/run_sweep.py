# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import JEQ
    import JLT
    import JGT
    import JLE
    import JGE
    import JNE

    import JEQ_stalling
    import JLT_stalling
    import JGT_stalling
    import JLE_stalling
    import JGE_stalling
    import JNE_stalling

    import JNE_JEQ
    import JNE_JEQ_stalling

    import JNE_JLT
    import JNE_JLE
    import JNE_JGT
    import JNE_JGE

    import JNE_JLT_stalling
    import JNE_JLE_stalling
    import JNE_JGT_stalling
    import JNE_JGE_stalling
else:
    from . import JEQ
    from . import JLT
    from . import JGT
    from . import JLE
    from . import JGE
    from . import JNE

    from . import JEQ_stalling
    from . import JLT_stalling
    from . import JGT_stalling
    from . import JLE_stalling
    from . import JGE_stalling
    from . import JNE_stalling

    from . import JNE_JEQ
    from . import JNE_JEQ_stalling

    from . import JNE_JLT
    from . import JNE_JLE
    from . import JNE_JGT
    from . import JNE_JGE

    from . import JNE_JLT_stalling
    from . import JNE_JLE_stalling
    from . import JNE_JGT_stalling
    from . import JNE_JGE_stalling


test_sets = [
    JEQ, JEQ_stalling,
    JLT, JLT_stalling,
    JGT, JGT_stalling,
    JLE, JLE_stalling,
    JGE, JGE_stalling,
    JNE,JNE_stalling,
    JNE_JEQ, JNE_JEQ_stalling,

    JNE_JLT, JNE_JLT_stalling,
    JNE_JLE, JNE_JLE_stalling,
    JNE_JGT, JNE_JGT_stalling,
    JNE_JGE, JNE_JGE_stalling,
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
