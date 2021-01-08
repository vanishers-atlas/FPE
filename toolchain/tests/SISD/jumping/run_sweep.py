# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import JMP
    import UCMP
    import SCMP
    import UCMP_SCMP
else:
    from . import JMP
    from . import UCMP
    from . import SCMP
    from . import UCMP_SCMP


test_sets = [
    JMP,
    UCMP,
    SCMP,
    UCMP_SCMP,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
