# Documentation for multiplexer

## Parameters
* number_inputs, *integer*, [0<],
  - the number of inputs
* binary_select, *boolean*,
  - if true
    + There is only 1 select port (input_select),
    + This select port's width with depends on the number of inputs
    + The value of the select port with be red as a binary number, this value will is the index of the selected input
  - if false
    + There are multiple select ports (select_X),
    + Each select port has a width of 1
    + The number of select ports depends on the number of inputs
    + When select_x is high input_x will be selected
    + If more than one select port is high at the same time the select with the lowest X with be selected

## Returned Parameters
* select_width, *integer*,
  - the width of each select port
* select_number, *integer*,
  - the number of select ports

## Generics
* data_width, *integer*, [0<],
	- the data width of both the input and output ports

## Ports
* input_select, *in std_logic_vector(ciel(lg(number_channels-1)) downto 0)*,
	-	Controls which input is mapped to the output
* input_X, *in std_logic_vector(data_width-1 downto 0)*,
  - the inputs to be multiplexed
  - numbered by their address, starting at
0 up to number_inputs
* data_out, *out std_logic_vector(data_width-1 downto 0)*,
  - outputs input_X, where X is the value of input_select
