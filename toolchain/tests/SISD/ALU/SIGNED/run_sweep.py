# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

if __name__ == "__main__":
    import passthrough_core

    import DSP_core_AB_only_narrow
    import DSP_core_AB_only_mid

    import DSP_core_MUL_only_narrow
    import DSP_core_MUL_only_mid
    import DSP_core_MUL_only_wide

    import DSP_core_AB_MUL_narrow
    import DSP_core_AB_MUL_mid
    import DSP_core_AB_MUL_wide

    import PALU_passthrough_core
    import PALU_DSP_core
else:
    from . import passthrough_core

    from . import DSP_core_AB_only_narrow
    from . import DSP_core_AB_only_mid

    from . import DSP_core_MUL_only_narrow
    from . import DSP_core_MUL_only_mid
    from . import DSP_core_MUL_only_wide

    from . import DSP_core_AB_MUL_narrow
    from . import DSP_core_AB_MUL_mid
    from . import DSP_core_AB_MUL_wide

    from . import PALU_passthrough_core
    from . import PALU_DSP_core


test_sets = [
    passthrough_core,

    DSP_core_AB_only_narrow,
    DSP_core_AB_only_mid,

    DSP_core_MUL_only_narrow,
    DSP_core_MUL_only_mid,
    DSP_core_MUL_only_wide,

    DSP_core_AB_MUL_narrow,
    DSP_core_AB_MUL_mid,
    DSP_core_AB_MUL_wide,

    PALU_passthrough_core,
    PALU_DSP_core,
]


def run_sweep(path="."):
    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
