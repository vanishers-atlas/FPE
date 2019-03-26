# Documentation for sFPE registo file

## Parameters
* data_width, *integer*, [0<],
  - the data width of the registers
* number_reg, *integer*, [0<],
  - the number of registers in registers file
  - used to determine reg_addr_width = ceil(lg(number_reg))
* conc_reads, *integer*, [0<],
  - Determine the maximum number of the register reads that can be handled each clock cycle
  - Control how many many sets of read ports there are

## Ports
#### Read Ports
* read_data_X, *out std_logic_vector(data_width-1 downto 0)*,
  - the current value of register_X
  - numbered by their address, starting at 0 up to number_reg - 1
* read_addr_X, *in std_logic_vector(reg_addr_width-1 downto 0)*,
  - Used to select which register to read
  - numbered by their address, starting at 0 up to number_reg - 1
#### Write Ports
* write_data, *in std_logic_vector(data_width-1 downto 0)*,
  - the data to be written to the reg file
* write_addr, *in std_logic_vector(reg_addr_width-1 downto 0)*,
  -	Used to select which register to write to
* write_enable, *in std_logic*,
  - tells to unit when a write op occurs
