# Documentation sFPE Instruction Decoder

## Parameters
* op_code_width, *integer*, [0<]
  - The width of instr op code
* addr_widths, *dict of integer*,
  - There should be one width for each addr in the instr Set
  - Each width must be greater then 0

## Returned Parameters
* instr_width, *integer*, [0<]
  - The width of the instr port
* ALU_opcode_width, *integer*, [0<]
  - The width of the instr port
* data_select, *dict of booleans*,
  - 1 for each of the memory addr pair
  - if true there is a select port for that memory addr pair
* jump, *dict*,
  - A dict of booleans,
  - 1 for each of the jump signal
  - if true there is a port for that jump signal
* update, *dict*,
  - A dict of booleans,
  - 1 for each input addresses
  - if true there is a port updating that address' target channel channel
* status_reg, *boolean*,
  - If true there is a port for updating a status registor

##  Ports
#### Data Select Ports
* A_sel_COM, *out std_logic*,
  - Controls wether A data is from comm get
* A_sel_IMM, *out std_logic*,
  - Controls wether A data is from IMM
* A_sel_RAM, *out std_logic*,
  - Controls wether A data is from RAM
* A_sel_REG, *out std_logic*,
  - Controls wether A data is from reg file
* b_sel_COM, *out std_logic*,
  - Controls wether B data is from comm get
* B_sel_IMM, *out std_logic*,
  - Controls wether B data is from IMM
* B_sel_RAM, *out std_logic*,
  - Controls wether B data is from RAM
* B_sel_REG, *out std_logic*,
  - Controls wether B data is from reg file
* C_sel_COM, *out std_logic*,
  - Controls wether C data is from comm get
* C_sel_IMM, *out std_logic*,
  - Controls wether C data is from IMM
* C_sel_RAM, *out std_logic*,
  - Controls wether C data is from RAM
* C_sel_REG, *out std_logic*,
  - Controls wether C data is from reg file
* R_sel_COM, *out std_logic*,
  - Controls wether comm put writes result data
* R_sel_RAM, *out std_logic*,
  - Controls wether RAM stores result data
* R_sel_REG, *out std_logic*,
  - Controls wether reg file stores result data

####  Jump ports
* JMP, *out std_logic*,
  - signal program to jump unconditionally
* JEQ, *out std_logic*,
  - signal program to jump if status_reg is equal
* JGT, *out std_logic*,
  - signal program to jump if status_reg is greater than
* JLT, *out sd_logic*,
  - signal program to jump if status_reg is less than

#### Comm Update Ports
* A_update, *out std_logic*,
  - signal to comm get to update the A addr channel
* B_update, *out std_logic*,
  - signal to comm get to update the B addr channel
* C_update, *out std_logic*,
  - signal to comm get to update the C addr channel

#### Status Register Ports
* status_update, *out std_logic*,
  - signal to status registor to update its value

#### Addr Ports
* A_addr, *out std_logic_vector(A_addr_width - 1 downto 0)*,
  - The address of the A data source
* B_addr, *out std_logic_vector(B_addr_width - 1 downto 0)*,
  - The address of the B data source
* C_addr, *out std_logic_vector(C_addr_width - 1 downto 0)*,
  - The address of the C data source
* R_addr, *out std_logic_vector(R_addr_width - 1 downto 0)*,
  - The address of the result destination

#### ALU Op Code ports
* ALU_op_code, *out std_logic_vector(ALU_op_width - 1 downto 0)*,
  - The opcode for the ALU

#### Instruction Port
* instr, *in std_logic_vector(A_addr_width - 1 downto 0)*,
  - The input instruction to be decoded
