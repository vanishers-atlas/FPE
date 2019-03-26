# Documentation for sFPE comm_get

## Parameters
* sFPE_data_width, *integer*, [0<],
  - the data width of the output to the sFPE core
* FIFO_data_width, *integer*, [0<],
  - the data width of the input FIFOs
* alignment_ref, *boolean*,
  - only used if sFPE_data_width != FIFO_data_width
  - if true, uses the least significant bit of both widths as the alignment reference point
  - if false, uses the most significant bit of both widths as the alignment reference point
* alignment_offset, *integer*, [0<,<=|sFPE_data_width - FIFO_data_width|],
  - only used if sFPE_data_width != FIFO_data_width
  - Controls the offset between the alignment reference point of the two widths
* number_FIFO, *integer*, [0<],
  - the number of input FIFOs
  - used to determine FIFO_addr_width = ceil(lg(number_FIFO))
* conc_reads, *integer*, [0<],
  - Controls how many address_X and data_X ports there are
* conc_updates, *integer*, [0<, <=conc_reads],
  - Controls how many update_X ports there are

## Returned Parameters
* addr_width, *integer*,
    - the address width required to access all channels of the comm

## Ports
#### General ports
* clock, *in std_logic*,
  - used for internal timing events
#### Fifo Ports
* FIFO_X, *in std_logic_vector(FIFO_data_width-1 downto 0)*,
  - the input FIFOs
  - numbered by their address, starting at 0 up to number_inputs
* update_FIFO_X, *out std_logic*,
  - updates FIFO_X that it's been red and needs to update its output FIFOs
  - numbered by their address, starting at 0 up to number_inputs - 1
#### sFPE Ports
* address_X, *in std_logic_vector(FIFO_addr_width-1 downto 0)*,
  -	Selects the FIFO ypou be red from
  - labelled from 0 to conc_reads - 1
* data_X, *out std_logic_vector(sFPE_data_width-1 downto 0)*,
  - the data read from the FIFO pointed to be address_X
  - labelled from 0 to conc_reads - 1
* update_X, *in std_logic*,
  - tells to comm unit to update the FIFO pointed to be address_X
  - labelled from 0 to conc_updates - 1

##Timing
####  Clock
* Raising edge:
  - fifo data buffered
  - fifo update signal goes low
* Falling edge:
  - fifo update signal goes high
