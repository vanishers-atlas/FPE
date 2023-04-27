# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import basic
    import basic_stalling

    import PALU
    import PALU_stalling
else:
    from . import basic
    from . import basic_stalling

    from . import PALU
    from . import PALU_stalling

test_sets = [
    basic,
    basic_stalling,

    #PALU,
    #PALU_stalling,
]


def run_sweep(path="."):
    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
