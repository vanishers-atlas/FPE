# Documentation for ROM

## Parameters
* data_values, *string*,
	- a path to a file containing the data values for each ROM address
* use_BROM, *boolean*
  - Determines if the ROM is build using the native BROMs on the chip
* conc_reads, *integer*, [0<],
  - the number of addr and data ports
* data_width, *integer*, [0<],
	- the data width of the output data ports
* depth, *integer*, [0<,],
	- the number of words in the ROM

## Returned Parameters
* addr_width, *integer*,
  - the address width required to access all bits in the ROM

## Ports
* addr_X, *in std_logic_vector(addr_width-1 downto 0)*,
  - the addr to be red
  - numbered by their address, starting at 0 up to num_reads - 1
* data_X, *out std_logic_vector(data_width-1 downto 0)*,
  - the read from addr_X
  - numbered by their address, starting at 0 up to num_reads - 1
