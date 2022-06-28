# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import AB_only_narrow
    import AB_only_mid
    import AB_only_stalling

    import MUL_only_narrow
    import MUL_only_mid
    import MUL_only_wide
    import MUL_only_stalling

    import AB_MUL_narrow
    import AB_MUL_mid
    import AB_MUL_wide
    import AB_MUL_stalling

    import PALU
    import PALU_stalling
else:
    from . import AB_only_narrow
    from . import AB_only_mid
    from . import AB_only_stalling

    from . import MUL_only_narrow
    from . import MUL_only_mid
    from . import MUL_only_wide
    from . import MUL_only_stalling

    from . import AB_MUL_narrow
    from . import AB_MUL_mid
    from . import AB_MUL_wide
    from . import AB_MUL_stalling

    from . import PALU
    from . import PALU_stalling


test_sets = [
    AB_only_narrow,
    AB_only_mid,
    AB_only_stalling,

    MUL_only_narrow,
    MUL_only_mid,
    MUL_only_wide,
    MUL_only_stalling,

    AB_MUL_narrow,
    AB_MUL_mid,
    AB_MUL_wide,
    AB_MUL_stalling,

    PALU,
    PALU_stalling,
]


def run_sweep(path="."):
    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
