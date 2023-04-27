# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.FINNR import _utils as meas_utils

import os
import math

import _generate_network as generate_network

# Generate network
network_name = "FINN_scaled//conv_row"
input_dims = {
  "width"  : 8,
  "height" : 8,
  "depth"  : 6
}
data_path = [
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 16,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 16,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
  {
      "type" : "pool",
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 32,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 32,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
  {
      "type" : "pool",
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 64,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*d, 2))
  },
  {
      "type" : "conv",
      "kernals" : 64,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
  {
      "type" : "pool",
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
  {
      "type" : "dense",
      "neurons" : 128,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
  {
      "type" : "acc",
      "neurons" : 10,
  },
  {
      "type" : "FIFO",
      "depth" : lambda w, h, d : 2**math.ceil(math.log(w*h*d, 2))
  },
]
network_folder = generate_network.generation_network(network_name, input_dims, data_path)

# Measure the generated network's area nad timing
dir_pathway = os.path.dirname(__file__)
meas_utils.impl_and_simulate_network(network_name, network_folder, dir_pathway)
