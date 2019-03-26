# Documentation for RAM

## Parameters
* use_BRAM, *boolean*
  - Determines if the RAM is build using the native BRAMs on the chip
* write_mode, *string*, ["high", "sync", "edge"]
	- "high": write_enable is active high
	- "sync": write_enable is synchronized to the clock raising edge
	- "edge": write_enable is raising edge triggered
* conc_reads, *integer*, [0<],
  - the number of addr and data ports
* data_width, *integer*, [0<],
  - the data width of the output data ports
* depth, *integer*, [0<],
  - the number of words in the RAM
  - Is only a guaranteed minimum, using BRAMs may give larger depths

## Returned Parameters
* addr_width, *integer*,
  - the address width required to access all bits in the RAM

## Ports
* clock, *in std_logic*,
	- the clock signal used for timings
####  Read ports
* read_addr_X, *in std_logic_vector(data_width-1 downto 0)*,
  - the addr to be red from
  - numbered by their address, starting at 0 up to conc_reads - 1
* read_data_X, *out std_logic_vector(data_width-1 downto 0)*,
  - the read in from addr_X
  - numbered by their address, starting at 0 up to conc_reads - 1
####  Write ports
* write_addr, *in std_logic_vector(addr_width-1 downto 0)*,
  - the addr to be written to
* write_data, *in std_logic_vector(data_width-1 downto 0)*,
  - triggered by write_enable
  - when triggered; the data at write in is updated to current value of this port
* write_enable, *in std_logic*
  - behavour depends on write_enable_mode:
    + 0: triggers write_data for as long as it is held high
    + 1: triggers write_data once if high on the raising edge of this clock port
    + 2: triggers write_data once on the raising edge of this port
