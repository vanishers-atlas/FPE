# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import ripple_basic
    import cascade_basic
    import counter_basic

    import seekable
    import counter_seekable_settable

    import ripple_single_iteration
    import cascade_single_iteration
    import counter_single_iteration
else:
    from . import ripple_basic
    from . import cascade_basic
    from . import counter_basic

    from . import seekable
    from . import counter_seekable_settable

    from . import ripple_single_iteration
    from . import cascade_single_iteration
    from . import counter_single_iteration

test_sets = [
    ripple_basic,
    cascade_basic,
    counter_basic,

    seekable,
    counter_seekable_settable,

    ripple_single_iteration,
    cascade_single_iteration,
    counter_single_iteration,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
