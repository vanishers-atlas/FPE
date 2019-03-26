# Documentation sFPE_PC

## Parameters
* PC_wrap_value, *integer*, [0<]
  - Used for looping the PC at the end of the program
* PC_width, *integer*, [ceil(lg(PC_max + 1))<=]
  - The width of the data ports
* jumps_enabled, *array of strings*,
  - Controls what jump circuitry is synthesized

##  Ports
*	clock, *in std_logic*,
  - The clock port
  - Unless some other event happens (jump or repeat) the Pc increment once every clock cycle
* reset, *in std_logic*,
  - Reset signal
  - Force the PC to 0
* value : *out std_logic_vector(PM_addr_width - 1 downto 0)*,
  - the currect value of PC

####  Jump ports
* jump_addr, *in std_logic_vector(PM_addr_width downto 0)*,
  - present iff JMP_enabled or JEQ_enabled or JGT_enabled or JLT_enabled = true
  - the value the PC is to be set to if a jump occurs
* equal_flag, *in std_logic;*,
  - present iff JEQ_enabled or JGT_enabled or JLT_enabled = true
  - The zero status flag, is '1' when the numbers are equal
* negative_flag, *in std_logic*,
  - present iff JGT_enabled or JLT_enabled = true
  - The sign status flag, is '1' when the result is negative (ie A < B)
* JMP, *in std_logic*,
  - present iff JMP_enabled
  - if high the PC will be set to branch_addr
* JEQ, *in std_logic*,
  - present iff JEQ_enabled
  - if read high the PC will be set to new_addr if equal_flag is high
* JGT, *in std_logic*,
  - present iff JGT_enabled
  - if read high the PC will be set to new_addr if negative_flag and equal_flag are both low
* JLT, *in sd_logic*,
  - present iff JLT_enabled
  - if read high the PC will be set to new_addr if negative_flag is high and equal_flag is low

##Timing
####  Clock
* Falling edge:
  - value updates
