# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import A_in_0_B_in_1
    import A_in_0_acc_B_in_1_acc

    import C_in_0

    import S_in_0_C_shifter
    import S_in_0_acc_C_shifter_in_0

    import AB_in_1_B_AB_C_in_0
    import AB_in_1_A_AB_B_AB_C_in_0
else:
    from . import A_in_0_B_in_1
    from . import A_in_0_acc_B_in_1_acc

    from . import C_in_0

    from . import S_in_0_C_shifter
    from . import S_in_0_acc_C_shifter_in_0

    from . import AB_in_1_B_AB_C_in_0
    from . import AB_in_1_A_AB_B_AB_C_in_0

test_sets = [
    A_in_0_B_in_1,
    A_in_0_acc_B_in_1_acc,

    C_in_0,

    S_in_0_acc_C_shifter_in_0,
    S_in_0_C_shifter,

    AB_in_1_B_AB_C_in_0,
    AB_in_1_A_AB_B_AB_C_in_0,
]


def run_sweep(path="."):
    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
