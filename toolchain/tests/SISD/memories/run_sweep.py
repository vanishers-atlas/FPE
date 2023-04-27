# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import ROM_A
    import ROM_A_stalling
    import ROM_B
    import ROM_B_stalling
    import DUAL_ROM
    import DUAL_ROM_stalling

    import RAM
    import RAM_stalling

    import REG_single_read
    import REG_single_read_stalling
    import REG_dual_read
    import REG_dual_read_stalling
else:
    from . import ROM_A
    from . import ROM_A_stalling
    from . import ROM_B
    from . import ROM_B_stalling
    from . import DUAL_ROM
    from . import DUAL_ROM_stalling

    from . import RAM
    from . import RAM_stalling

    from . import REG_single_read
    from . import REG_single_read_stalling
    from . import REG_dual_read
    from . import REG_dual_read_stalling

test_sets = [
    ROM_A,
    ROM_A_stalling,
    ROM_B,
    ROM_B_stalling,
    DUAL_ROM,
    DUAL_ROM_stalling,

    RAM,
    RAM_stalling,

    REG_single_read,
    REG_single_read_stalling,
    REG_dual_read,
    REG_dual_read_stalling,
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
