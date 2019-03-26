# Documentation for sFPE delay

## Parameters
* has_data_enable, *boolean*,
  - controls if the delay had an data_enable port
* has_reset, *boolean*,
  - controls if the delay had an reset port

## Generics
* default_value, *integer*, [0<,<2**width]
	- Present iff has_data_enable or has_reset = ttue
	- the default value inserted into the delay if data isn't given
* width, *integer*, [0<],
	- the data width of both the input and output data ports, in bits
* depth, *integer*, [0<],
	- how many cycle cycles the delay lasts

## Ports
*	clock *in std_logic*,
	-	Used for timing
*	reset *in std_logic*,
	- present iff has_reset = true
	-	when high wipe the hold delay back to default_value
* data_in, *in std_logic_vector(width - 1 downto 0)*,
	- the data to be written to the delay
  - has_data_enable = false, the value on the port is added to the delay on the raising edge of the clock cycle
* data_out, *out std_logic_vector(width)*,
  +	the delayed data passed in depth clock cycles ago
* data_enable, *in std_logic*,
	- present iff has_data_enable = true
  - if high on raise clock edge: value on data_in to inserted into the delay
  - if low  on raise clock edge: default_value is inserted into the delay
