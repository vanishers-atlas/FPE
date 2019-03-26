# Documentation for RAM

## Parameters

#### General Parameters
* data_width, *integer*, [0<]
  - The core's data Width

#### Immediate Value ROM (IMM) parameters
* IMM_depth, *integer*, [0<=]
  - The number of elements in the Immediate Value ROM
* IMM_values, *string*,
	- a path to a file containing the data values for mmediate Value ROM
* IMM_use_BROM, *boolean*
  - Determines if the Immediate Value ROM is build using the native BROMs on the chip
