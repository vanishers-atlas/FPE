# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.FINNR import _utils as meas_utils

import os
import math

import generate_network

# Generate network
network_name = "FINN_scaled_frames"
input_dims = {
  "width"  : 8,
  "height" : 8,
  "depth"  : 6
}
FPEs = [
    {
        "type" : "conv_frame",
        "kernals" : 16,
    },
    {
        "type" : "conv_frame",
        "kernals" : 16,
    },
    {
        "type" : "pool_frame",
    },
    {
        "type" : "conv_frame",
        "kernals" : 32,
    },
    {
        "type" : "conv_frame",
        "kernals" : 32,
    },
    {
        "type" : "pool_frame",
    },
    {
        "type" : "conv_frame",
        "kernals" : 64,
    },
    {
        "type" : "conv_frame",
        "kernals" : 64,
    },
    {
        "type" : "pool_frame",
    },
    {
        "type" : "dense_frame",
        "neurons" : 128,
    },
    {
        "type" : "acc_frame",
        "neurons" : 10,
    },
]
buffers = [
  {
      "type" : "FIFO",
      "data_width" : 1,
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  },
  {
      "type" : "FIFO",
  }
]
network_folder = generate_network.generation_network(network_name, input_dims, FPEs, buffers)

# Measure the generated network's area nad timing
dir_pathway = os.path.dirname(__file__)
meas_utils.impl_and_simulate_network(network_name, network_folder, dir_pathway)
