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
    import ripple_basic_stalling
    import ripple_single_iteration

    import cascade_basic
    import cascade_basic_stalling
    import cascade_single_iteration

    import counter_basic
    import counter_basic_stalling
    import counter_single_iteration

    import single_iteration_puned

else:
    from . import ripple_basic
    from . import ripple_basic_stalling
    from . import ripple_single_iteration

    from . import cascade_basic
    from . import cascade_basic_stalling
    from . import cascade_single_iteration

    from . import counter_basic
    from . import counter_basic_stalling
    from . import counter_single_iteration

    from . import single_iteration_puned

test_sets = [
    ripple_basic,
    ripple_basic_stalling,
    ripple_single_iteration,

    cascade_basic,
    cascade_basic_stalling,
    cascade_single_iteration,

    counter_basic,
    counter_basic_stalling,
    counter_single_iteration,

    single_iteration_puned,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
