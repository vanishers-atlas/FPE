# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import comms
    import memories
    import ZOL
    import rep_bank
    import BAM
    import ALU
    import jumping
else:
    from . import comms
    from . import memories
    from . import ZOL
    from . import rep_bank
    from . import BAM
    from . import ALU
    from . import jumping


test_sets = [
    comms,
    memories,
    ZOL,
    rep_bank,
    BAM,
    ALU,
    #jumping,
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
