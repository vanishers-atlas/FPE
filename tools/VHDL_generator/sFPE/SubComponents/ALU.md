# Documentation for sFPE ALU

## Parameters
* data_width, *integer*, [0<],
  - the data width of the data input and output ports
* CMP_equal_enabled, *boolean*,
  - Controls if unconditional jump circuitry is synthesize
* CMP_sign_enabled, *boolean*,
  - Controls if conditional, equals, jump circuitry is synthesized

## Ports
#### General ports
* clock, *in std_logic*,
  - used for internal timing events
* read_addr_X, *in std_logic_vector(reg_addr_width-1 downto 0)*,
  - Used to select which register to read
  - numbered by their address, starting at 0 up to number_registers - 1
* write_enable, *in std_logic*,
  - tells to unit when a write op occurs
