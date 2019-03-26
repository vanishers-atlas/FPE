##  Data Types
* immediate:
  - Can only be data source
  - Access time 1 clock cycle
* Comm:
  - Can be both data source and result destination
  - Access time 1 clock cycle
* Register:
  - Can be both data source and result destination
  - Access time 1 clock cycle
* Memory:
  - Can be both data source and result destination
  - Access time 2 cycles

## Access Modes
* Direct:
  - all data sources and result destinations can be accessed directly

##  Instructiona
#### Mics Opcodes
* NOP
  - No operation
  - Used for timing
* CMP A, B
  - A and B can be any data source access
  - Set the status register to the relation between A and B

####  JUMP instructions
* JMP new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC
* JEQ new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was equal
* JNE new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was not equal
* JGT new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was greater than
* JGE new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was greater than or equal
* JLT new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was less than
* JLE new_PC
  - new_PC can only be an immediate
  - jumps the program counter to new_PC if the last CMP was less than or equal
