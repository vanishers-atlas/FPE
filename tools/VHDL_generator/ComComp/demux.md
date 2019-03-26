# Documentation for demultiplexer

## Parameters
* number_outputs, *integer*, [0<],
  - the number of outputs
* binary_select, *boolean*,
  - if true
    + There is only 1 select port (output_select),
    + This select port's width with depends on the number of outputs
    + The value of the select port with be red as a binary number, this value will is the index of the selected output
  - if false
    + There are multiple select ports (select_X),
    + Each select port has a width of 1
    + The number of select ports depends on the number of outputs
    + When select_x is high output_x will be selected
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
* data_in, *in std_logic_vector(data_width-1 downto 0)*,
  - the input to be demultiplexed
* output_X, *out std_logic_vector(data_width-1 downto 0)*,
  - output_select == X:
    + true  : outputs data_in
    + false : outputs Z  
  - numbered by their address, starting at 0 up to number_inputs
