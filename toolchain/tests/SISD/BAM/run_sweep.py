# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils


if __name__ == "__main__":
    import fetch
    import fetch_stalling

    import store
    import store_stalling

    import stated_base
    import stated_step

    import multi_base
else:
    from . import fetch
    from . import fetch_stalling

    from . import store
    from . import store_stalling

    from . import stated_base
    from . import stated_step

    from . import multi_base
test_sets = [
    fetch,
    fetch_stalling,

    store,
    store_stalling,

    stated_base,
    stated_step,

    multi_base
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
