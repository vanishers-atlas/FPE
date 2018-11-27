# Documentation for FIFO

## Generics
* data_Width, *integer*,
	- the data width of both the input and output data ports, in bits
* required_depth, *integer*,
	- the number of data slots the is to FIFO have
	- This is only a guaranteed minimum depth, As large FIFOs may use BRAMs whic are deeper than than required_depth, all behaviours based on the FIFO's depth (FIFO_depth) use this real depth
* almost_Full_offset, *integer*,
	- when this the FIFO is within this many slot of being full almost_full is set high,  
	- must less than FIFO_depth,
	- -1 disables the almost_fuil port, pulling it to 0 all the time
* almost_empty_offset, *integer*,
	- when this the FIFO is within this many slot of being empty almost_empty is set high,  
	- must less than FIFO_depth,
	- -1 disables the almost_fuil port, pulling it to 0 all the time
* state_reporting, *boolean*,
	- if true the four state ports will be set depending on FIFO's state (see ports section),
	- if false this ports will be tired to 0
* wait_on_full, *boolean*,
	- if true the FIFO will block writes when full, if the writing component isn't following the i/o protocol (see protocol section) this may result is data being dropped.
	- false the write behaviour when full is un defined and may lead to data lost or corruption
* default_value, *integer*,
	- the default value for the FIFO output,
	- -1 means high impedance,
	- only used when default_on_empty is true or data_fall_through is false
* default_on_empty, *boolean*,
	- if true the FIFO will output default_value when it is empty,
	- if false the output when empty is undefined, may lead to juck data being read if the reading component doesn't follow the i/o protocol (see protocol section)
* data_fall_through, *boolean*,
	- if true the FIFO will present the next slot's data on the output at all times,
	- if false the FIFO will present the default_value at all times but the clock cycle after read was high

## Ports
##### General Ports
* clk, *in std_logic*,
	- the clock signal,
	- all other port's read and writes are synced to the raising edge on this signal

##### Data ports
* write_Data, *in std_logic_vector(data_Width)*,
	- the data to be written to the FIFO
* write, *in std_logic* ,
	- when high the FIFO will read and store data from write_Data port,
	- Note behavour when the fifo is full is defined by wait_on_full's value (see generic section)
* red_data, *out std_logic_vector(data_Width)*,
	- Output data of the FIFO,
	- Behavour depends on data_fall_through and Default_on_empty (see generic section)
* read, *in std_logic*,
	- when high the FIFO will update red_data at the start of the next clk cycle

##### State reporting ports
* state_full , *out std_logic*,
	- Set high when the the FIFO is full and can't store anymore data
* almost_full , *out std_logic*,
	- Set high went the FIFO has almost_Full_offset or less slots left before becoming full
	- if almost_Full_offset is 0 it will have the exact some output as state_full,
	- if almost_Full_offset = -1 then it will be tied to 0
* state_empty, *out std_logic*,
	- Set high when the the FIFO is empty, ie has do more meaningful data to output
* almost_empty, *out std_logic*,
	- Set high when the FIFO has almost_empty_offset or less slots (with data) left before being empty
	- if almost_empty_offset is 0 it will have the exact some output as state_empty,
	- if almost_empty_offset = -1 then it will be tied to 0

## I/o protocol
