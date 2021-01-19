# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.tests import utils

if __name__ == "__main__":
    from toolchain.tests.SISD.memories.UNSIGNED import RAM, REG
else:
    from . import RAM
    from . import REG

test_sets = [
    RAM,
    REG,
]


def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
