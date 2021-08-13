# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils


if __name__ == "__main__":
    import put_single_channel
    import put_single_channel_FIFO_handshakes

    import get_single_channel
    import get_single_channel_put_FIFO_handshakes
    import get_single_channel_get_FIFO_handshakes
    import get_single_channel_both_FIFO_handshakes
else:
    from . import put_single_channel
    from . import put_single_channel_FIFO_handshakes

    from . import get_single_channel
    from . import get_single_channel_put_FIFO_handshakes
    from . import get_single_channel_get_FIFO_handshakes
    from . import get_single_channel_both_FIFO_handshakes


test_sets = [
    put_single_channel,
    put_single_channel_FIFO_handshakes,

    get_single_channel,
    get_single_channel_put_FIFO_handshakes,
    get_single_channel_get_FIFO_handshakes,
    get_single_channel_both_FIFO_handshakes,
]

def run_sweep(path="."):

    return utils.run_sweep_branch(__file__.split("\\")[-2], path, test_sets)

if __name__ == "__main__":
    exit( run_sweep() )
