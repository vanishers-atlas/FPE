# Documentation sFPE_branch

##  Generics
* PC_ADDR_WIDTH, *integer*,
  - The data width of the program addresses
* BRANCH_EN, *boolean*,
  - Controls if the branch circuitry is created
  - True to creatue
  - False to skip
* JMP_EN, *boolean*.
  - Controls if the jump circuitry is created
  - True to creatue
  - False to skip

##  Ports
##### Decoded Instruction Ports
* i_id_beq, *in std_logic*,
  - Is '1' when the current Instruction is branch if equal
* i_id_bgt, *in std_logic*,
  - Is '1' when the current Instruction is branch if greater than
* i_id_blt, *in sd_logic*,
  - Is '1' when the current Instruction is branch if less than
* i_id_bge, *in std_logic*,
  - Is '1' when the current Instruction is branch if greater than or equal
* i_id_ble, *in std_logic*,
  - Is '1' when the current Instruction is branch if less than or equal
* i_id_bne, *in std_logic*,
  - Is '1' when the current Instruction is branch if not equal
* i_id_b, *in std_logic*,
  - Is '1' when the current Instruction is an unconditional branch

##### State input Ports
* i_ex_zero, *in std_logic;*,
  - The zero flag from the ALU, is '1' when the numbers are equal
* i_ex_sign, *in std_logic*,
  - The sign flag from the ALU, is '1' when the result is negative (ie A < B)

##### Result Ports
* o_branch_taken, *out std_logic*,
  - Is set to '1' when a branch is taken
* o_jmp_taken, *out std_logic*,
  - Is set to '1' when a branch is taken
