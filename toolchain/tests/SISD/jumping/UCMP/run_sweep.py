# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import JEQ
    import JLT
    import JGT
    import JLE
    import JGE
    import JNE
else:
    from . import JEQ
    from . import JLT
    from . import JGT
    from . import JLE
    from . import JGE
    from . import JNE


test_sets = [
    JEQ,
    JLT,
    JGT,
    JLE,
    JGE,
    JNE,
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
