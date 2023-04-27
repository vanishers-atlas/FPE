# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.FINNR import _utils as meas_utils

import os

import generate_network

if __name__ == "__main__":
    # Generate network
    network_name = "FINN_scaled_max"
    input_dims = {
        "width"  : 8,
        "height" : 8,
        "depth"  : 6,
    }
    layers = [
        {
            "type" : "conv",
            "kernals" : 16,
            "packing_factor" : None,
        },
        {
            "type" : "conv",
            "kernals" : 16,
            "packing_factor" : None,
        },
        {
            "type" : "pool",
            "packing_factor" : None,
        },
        {
            "type" : "conv",
            "kernals" : 32,
            "packing_factor" : None,
        },
        {
            "type" : "conv",
            "kernals" : 32,
            "packing_factor" : None,
        },
        {
            "type" : "pool",
            "packing_factor" : None,
        },
        {
            "type" : "conv",
            "kernals" : 64,
            "packing_factor" : None,
        },
        {
            "type" : "conv",
            "kernals" : 64,
            "packing_factor" : None,
        },
        {
            "type" : "pool",
            "packing_factor" : None,
        },
        {
            "type" : "dense",
            "neurons" : 128,
            "packing_factor" : None,
        },
        {
            "type" : "acc",
            "neurons" : 10,
            "packing_factor" : None,
        },
    ]
    network_folder = generate_network.generation_network(network_name, input_dims, layers)

    # Measure the generated network's area nad timing
    dir_pathway = os.path.dirname(__file__)
    meas_utils.impl_and_simulate_network(network_name, network_folder, dir_pathway)
