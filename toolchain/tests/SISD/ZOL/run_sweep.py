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

    import cascade_basic
    import cascade_basic_stalling

    import counter_basic
    import counter_basic_stalling

    import seekable
    import seekable_stalling

    import counter_seekable_settable
    import counter_seekable_settable_stalling

    #import single_iteration_puned
    import single_iteration_ripple
    import single_iteration_cascade
    import single_iteration_counter

else:
    from . import ripple_basic
    from . import ripple_basic_stalling

    from . import cascade_basic
    from . import cascade_basic_stalling

    from . import counter_basic
    from . import counter_basic_stalling

    from . import seekable
    from . import seekable_stalling

    from . import counter_seekable_settable
    from . import counter_seekable_settable_stalling

    #from . import single_iteration_puned
    from . import single_iteration_ripple
    from . import single_iteration_cascade
    from . import single_iteration_counter

test_sets = [
    ripple_basic,
    ripple_basic_stalling,

    cascade_basic,
    cascade_basic_stalling,

    counter_basic,
    counter_basic_stalling,

    seekable,
    seekable_stalling,

    counter_seekable_settable,
    counter_seekable_settable_stalling,

    #single_iteration_puned,
    single_iteration_ripple,
    single_iteration_cascade,
    single_iteration_counter,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
