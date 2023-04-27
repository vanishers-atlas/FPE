# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import seekable
    import seekable_stalling

    import settable
    import settable_stalling
else:
    from . import seekable
    from . import seekable_stalling

    from . import settable
    from . import settable_stalling

test_sets = [
    seekable,
    seekable_stalling,

    settable,
    settable_stalling,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
