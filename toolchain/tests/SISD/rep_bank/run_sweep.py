# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import preloaded_never
    import preloaded_never_stalling

    import preloaded_never
    import preloaded_never_stalling

else:
    from . import preloaded_never
    from . import preloaded_never_stalling

    from . import preloaded_never
    from . import preloaded_never_stalling

test_sets = [
    preloaded_never,
    preloaded_never_stalling,

    preloaded_never,
    preloaded_never_stalling,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
