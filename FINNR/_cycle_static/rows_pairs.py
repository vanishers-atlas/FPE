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
network_name = "FINN_scaled_rows_pairs"
input_dims = {
  "width"  : 8,
  "height" : 8,
  "depth"  : 6
}
FPEs = [
    {
        "type" : "conv_row",
        "kernals" : 16,
    },
    {
        "type" : "conv_row",
        "kernals" : 16,
    },
    {
        "type" : "pool_pair",
    },
    {
        "type" : "conv_row",
        "kernals" : 32,
    },
    {
        "type" : "conv_row",
        "kernals" : 32,
    },
    {
        "type" : "pool_pair",
    },
    {
        "type" : "conv_row",
        "kernals" : 64,
    },
    {
        "type" : "conv_row",
        "kernals" : 64,
    },
    {
        "type" : "pool_pair",
    },
    {
        "type" : "dense_batch",
        "neurons" : 128,
        "batch_size" : lambda w, h, d : w * d
    },
    {
        "type" : "acc_batch",
        "neurons" : 10,
        "batch_size" : lambda w, h, d : int(d/8)
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
