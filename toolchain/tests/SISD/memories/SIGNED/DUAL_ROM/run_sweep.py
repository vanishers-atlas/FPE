# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

def run_sweep(path="."):
    test_name = __file__.split("\\")[-2]

    return utils.run_sweep_leaf(path, test_name)

if __name__ == "__main__":
    exit(run_sweep())
