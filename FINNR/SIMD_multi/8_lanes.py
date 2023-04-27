# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.FINNR import _utils as meas_utils

from generate_network import generation_network

import os
import math

if __name__ == "__main__":
    # Generate network
    network_name = "FINN_scaled_8_lane"
    input_dims = {
        "width"  : 8,
        "height" : 8,
        "depth"  : 6,
        "lanes" : 8,
    }
    layers = [
        {
            "type" : "conv",
            "kernals" : 16,
        },
        {
            "type" : "conv",
            "kernals" : 16,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "conv",
            "kernals" : 32,
        },
        {
            "type" : "conv",
            "kernals" : 32,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "conv",
            "kernals" : 64,
        },
        {
            "type" : "conv",
            "kernals" : 64,
        },
        {
            "type" : "pool",
        },
        {
            "type" : "dense",
            "neurons" : 128,
        },
        {
            "type" : "acc",
            "neurons" : 10,
        },
    ]
    network_folder = generation_network(network_name, input_dims, layers)

    # Measure the generated network's area nad timing
    dir_pathway = os.path.dirname(__file__)
    meas_utils.impl_and_simulate_network(network_name, network_folder, dir_pathway)
