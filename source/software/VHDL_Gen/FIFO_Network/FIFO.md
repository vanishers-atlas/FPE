# Documentation for FIFO

## Parameters
* empty_value_mode, *integer*, [0,1,2,3]
	- 0: the fifo outputs all zeros when empty
	- 1: the fifo outputs all ones when empty
	- 2: the fifo outputs a binary number (passed in via empty_value generic) when empty
	- 3: the fifo's output is undefined when empty
* has_full_port, *boolean*,
	- controls if the FIFO has a full status port
* has_empty_port, *boolean*,dsa
	- controls if the FIFO has an empty status port
* has_almost_full_port, *boolean*,
	- controls if the FIFO has an almost full status port
* has_almost_empty_port, *boolean*,
	- controls if the FIFO has an almost empty status port
* overflow_protection, *boolean*,
	- true	: the FIFO will delay any writes when full
	 	+ if the source component doesn't want for the full status port to be low at on a raising clock edge this write will be lost
	- false	: write behaviour when full is undefined
		+ writing when the FIFO is full may lead to lost or corruption of FIFO data
* underflow_protection, *boolean*,
	- true	: the fifo will ignore update signals when empty,
	- false : the effect of the fifo receiving an update signal when empty are undefined
* use_BRAM, *boolean*
  - Determines if the FIFO is build using the native BRAMs on the chip
* width, *integer*, [0<]
	- Used iff use_BRAM = true
	- the data width of both the input and output data ports, in bits
* depth, *integer*, [0<]
	- Used iff use_BRAM = true
	- the number of data slots the is to FIFO have
	- This is only a guaranteed minimum depth, using BRAMs may have a greater deeper, all behaviours based on the FIFO's depth use this real_depth

## Generics
* almost_full_offset, *integer*, [0<,<real_depth],
	- Present iff has_almost_full_port = true
	- when the FIFO is within this many queues of being full: almost_full is set high
* almost_empty_offset, *integer*, [0<,<real_depth],
	- Present iff has_almost_empty_port = true
	- when the FIFO is within this many dequeues of being empty: almost_empty is set high
* empty_value, *integer*, [0<,<2**width]
	- Present iff empty_value_mode = 2
	- The value output by the FIFO when it is empty
* width, *integer*, [0<],
	- Present iff use_BRAM = false
	- the data width of both the input and output data ports, in bits
* depth, *integer*, [0<],
	- Present iff use_BRAM = false
	- the number of data slots the is to FIFO have

## Ports
##### General Ports
*	clock *in std_logic*,
	-	Used for sycnrising updates and writes to the fifo
##### Data ports
* write_data, *in std_logic_vector(width - 1 downto 0)*,
	- the data to be written to the FIFO
* write_enable, *in std_logic*,
	- on raising edge:
	 	+	FiFO has space: the FIFO will write the write_data to itself
		+ FIFO is full: behaviour depends on overflow_protection, see Parameter sections
* data_out, *out std_logic_vector(width)*,
	+	FiFO has data: the value at the front of the fifo
	+ FIFO is empty: value depends on empty_value_mode, see Parameter sections
* update_output , *in std_logic*,
	- on raising edge:
		+	FiFO has data: the FIFO will update data_out to the next piece of data
		+ FIFO is empty: behaviour depends on underflow_protection, see Parameter sections
##### State reporting ports
* full , *out std_logic*,
	- present iff has_full_port = true
	- Set high when the the FIFO is full and can't store anymore data
* almost_full , *out std_logic*,
	- present iff has_almost_full_port = true
	- Set high when the FIFO is within almost_Full_offset writes of being full
* empty, *out std_logic*,
	- present iff has_empty_port = true
	- Set high when the the FIFO is empty, ie has do more meaningful data to output
* almost_empty, *out std_logic*,
	- present iff has_almost_empty_port = true
	- Set high when the FIFO is within almost_empty_offset updates of being empty
