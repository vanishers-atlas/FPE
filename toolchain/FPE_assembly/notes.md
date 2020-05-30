# Documentation for the FPE assembly language

28/05/2020, Created by Stephen Clarke,

# Language Features

## Whitespace

The FPE assembly language is white space independent.

## Comments
The FPE assembly language currently supports 2 types of comments
* Single line comments, started by double backslashes (\\\\) and ended by a new line,
* Multi line comments, started by  double backslashes followed by an asterisk (\\\\\*) and ended by the reverse (\*\\\\)

## Instructions, Operations, and Statements

There are 2 mains types of instructions within the FPE assembly language
* Operations, instructions that map to instructions in the program memory, most operations also map to pieces/features of hardware in the generated FPE
* Statements, instructions that don't map to instructions in the program memory, statements may still map to pieces/features of hardware in the generated FPE

## Scopes

Scopes are started by an opening curly bracket({) and ended by a closing curly bracket(}) with instructions in between. They can be used anywhere within the program, and are even required to define the area of effect of some instructions eg the ZOL instruction.

Currently a scope not required by an instruction has no meaning, and the program is treated as if the brackets aren't there ie the scope is ignored, but not the instructions within it.

Every FPE assembly program is required to be bounded by a scope

## Identifers

Anywhere within an FPE assembly program where the programmer is required to enter a name for something an Identifer is used. Identifers can be any string of letters, numbers, and underscores (\_) with the caveat that the first character cannot be a number

## Numbers

Anywhere within an FPE assembly program where the programmer is required to enter a numeric value any of the follow bases may be used
 + Decimal, written as a string of any numbers between 0 and 9
 + Binary, written as a string of numbers between 0 and 1, prefixed with "0b" or "0B"
 + Octal, written as a string of numbers between 0 to 7, prefixed with "0o" or "0O"
 + Hexadecimal, written as a string of numbers between 0 and 9 and letters between a and f in either case, prefixed with "0x" or "0X"


## Constants, and Expressions

To make FPE assembly programs easier to read there are of constants and expressions.

Constants are a way to assigned a name to a numeric value, once a constant is defined it can't be redefined but can be used anywhere a numeric value is required.

Expressions are a way to derive a numeric value from other numeric values. Expressions can be used anywhere a numeric value is required. Expressions are evaluated by the toolchain at synthesis time. The following operations are supported
* Addition, _numeric_ **+** _numeric_
* Subtraction, _numeric_ **-** _numeric_
* Multiplication, _numeric_ **\*** _numeric_
* Integer Division, _numeric_ **/** _numeric_
* Remainder after Integer Division,_numeric_ **%** _numeric_

Expression operations follow an order of precedences, operations of the same precedences are evaluated left to right. Below are is the order of precedence in decreasing order
1. Rounds brackets
2. Multiplication, Integer Division, and Remainder after Integer Division
3. Addition, and Subtraction

# Programming Guide

## Natually SIMD

The FPE is designed to support Single Instruction Multiple Data (SIMD) programs. This is achieved by having multiple lanes within the FPE, these lanes are lockstepped together, each preforming the exact same operations on their own data. The number of lanes an FPE has is controlled within the parameter file, by setting the *lanes* field within the *SIMD* field. The number of lanes can be any natural number.

Single Instruction Single Data (SISD) is handled as a special case of SIMD, were there is only 1 lane.

## The FPE pipeline

An FPE's pipeline depends on the instructions it supports, however to make programming an FPE simpler their pipelines are broken into stages, with only the exact number of clock cycles per stage varying from FPE to FPE, but not the order of these stages. This then means an instructions can specify which stage their effects occur within, instead of after a number of clockcycles.

The pipeline stages, the range of their lengths, and purpose are
1.  PC update, always 1 cycle, gives the program count and xero overhead manager/trackers time to determine the next PC value
2.  Instruction Fetch, always 1 cycle, a cycle to use the PC value to lookup the next instruction in program memory
3. Instruction Decode, alway 1 cycle, a cycle to decode the fetched instruction into control signals, and address values for the rest of the pipeline
4. Data Fetch, alway 1 cycle, used to access data source memories to fetch the data for the exe stage
5. Exe, 1 to 2 cycles, used to perform operations on the fetch data to generate the results data to be stored
6. Data Store, used to write the result data to the data destination memories

## Block Access Managers

To enhance the usefulness of repeated instructions (eg ones within a ZOLs), the FPE assembly language has the idea of Block Access Managers (BAM). They are used when the address of a memory access is to change in a way known at synthesis time. Eg to increment a known amount every time the instruction is run. Anywhere an address is required a BAM access may be used instead.

BAM addresses are the sum of 2 parts:
* The base, a generic within the BAM hardware which set the lowest value a BAM's address can take
* The offset, the value of a counter within the BAM hardware that can be updated during a BAM access.

#### Sytnax
**BAM** **[** _select_ **]** **<** _mods_ **>**

_select_ is a numeric value used to differentiate between multiple BAMs

#### Mods
* **FORWARD**, If present the BAM's offset will be incremented after the address read. Mutually exclusive with **BACKWARD**
* **BACKWARD**, If present the BAM's offset will be decremented after the address read. Mutually exclusive with **FORWARD**

#### Parameters
* *addr_max*, the max value the BAM's address should take, used to determine the BAM's address width. Note there is no checking for this value so it may be exceeded if the value is not 1 less than a power of 2 ie if it is not a Mersenne prime.
* *offset_max*, the max value the BAM's offset should take, used to determine the BAM's offset width. Note there is no checking for this value so it may be exceeded if the value is not 1 less than and a power of 2 ie if it is not a Mersenne prime.

#### Generics
* *base*, the base part of the the BAM's address
* *increment*, the amount the BAM's offset is to be incremented(decremented) if a **FORWARD**(**BACKWARD**) modifier is present in a BAM access


## Data Memories, and Memory Accesses

Within an FPE assembly program, operations have their data fetched, and stored, by memory accesses. The syntax of a memory access, and if it can be used as a fetch/store depends on the data memory being accessed. This section lists the available data memories, their syntax and usability as fetch and store accesses.

An FPE assembly program can use any combinations of the data memories. If a data memory is not accessed within an FPE assembly program it won't be included within the generated FPE.

Some memory accesses support modifiers (mods), if more that one modifier is being applied to an access, the mods should be included in a comma separated list.


### Immediate Memory

The immediate memory (IMM) is how an FPE stores immediate values used with the program. It is handled purely by the toolchain, and can only be used as a fetch access.

#### Sytnax
_numeric_value_

#### Parameters
No generics required

#### Generics
No generics required


### Comm Get

The comm get (GET) is how an FPE reads data from outside itself. It can only be used as a fetch access.

#### Sytnax
**GET** **[** _address_ **]** **<** _mods_ **>**

#### Mods
* **ADV**, If present the comm get will raise the red signal related to the addressed port, telling the input FIFO to advance to the next piece of data by the next clock rising edge. Should only be used when the program is finished with the current piece of data

#### Parameters
* Depth, the number of channels the comm get has. The channel read by an access is controlled by the address given, channels are addressed from 0. Each channel has its own port into the FPE and can be advanced independently from other channels.
* data_width, the number of bits each channel has

#### Generics
No generics requires


### Comm Put

Comm put (PUT) is how an FPE writes data outside of itself. It can only be used as a store access.

#### Sytnax
**PUT** **[** _address_ **]**

#### Parameters
* Depth, the number of channels the comm put has. The channel written by an access is controlled by the address given, channels are addressed from 0. Each channel has its own port out of the FPE.
* data_width, the number of bits each channel has

#### Generics
No generics required


### Register File

The Register File (REG) is a group of registers within the FPE. It can be used as both fetch and store accesses.

#### Sytnax
**REG** **[** _address_ **]**

#### Parameters
* Depth, the number of registers the register file has. The register read/written by an access is controlled by the address given, registers are addressed from 0.
* data_width, the number of bits each register has.

#### Generics
No generics required


### RAM

Can be used as both fetch and store accesses.

#### Sytnax
**RAM** **[** _address_ **]**

#### Parameters
* Depth, the number of locations the RAM has. The locations read/written by an access is controlled by the address given, locations are addressed from 0.
* data_width, the number of bits each location has.

#### Generics
No generics required


### ROM

Can be only used as a fetch access.

#### Sytnax
**ROM** **[** _address_ **]**

#### Parameters
* Depth, the number of locations the ROM has. The locations read/written by an access is controlled by the address given, locations are addressed from 0.
* data_width, the number of bits each location has.

#### Generics
No generics required

## Statements
Below is a list of the statements currently within the FPE assembly language; their function, their syntax, and any hardware they map to.

### Jump Labels

Jump labels are used to define positions within the program for jump operations to set the the program counter to.

#### Syntax
*jump_label* **:**

*jump_label*, an identifier, must be unique from *jump_label* used within other jump label statements

#### Hardware
No direct hardware mapping

### Constant Declaration

Define an identifier for and numeric value

#### Syntax
**DEF** *constant_name* *value* **;**

*constant_name*, an identifier, must be unique from *constant_name* used within other  constant declaration statements
value, a numeric value

#### Hardware
No direct hardware mapping

### Zero Overhead Loop (ZOL) Statements

#### Function
Zero overhead loops (ZOLs) are used to repeat a group of instructions a number of times, this number must be knows at synthesis time. At runtime the instructions are repeated with no overhead cycles, it is as if the instructions are just repeated one after another within the program memory.

#### Syntax
**ZOL** **(** *times* **)** *scope*

*times*, a numeric value
*scope*, a scope containing all the instructions to be repeated by the ZOL

#### Hardware
Each ZOL statement directly maps to a ZOL tracker unit in hardware. All the ZOL tracker units within an FPE are collected together into a ZOL handler unit. Both these hardware units are handled by the toolchain and don't require any input parameters or generics from the programmer.

#### Note

ZOLs can be nested, but if so they can't share the same end point, or put another way, there must be at least 1 instruction between the end of the each nested ZOLs' scopes

## Operations

As many operations share the same hardware impacts as each other, operations will be grouped by the hardware impacts they have. Note impacts such as adding decoding logic are not considered here.

### Hardwareless (Voids) Operations

Hardwareless (void) Operations are operation with no hardware impacts.

#### No Operation (NOP)

The no operation (NOP) operation, has no effect on any data, it is solely used for introducing a 1 cycle stall into the pipeline

##### Syntax
**NOP** **;**

### Program Counter Operations

Program counter operations affect the program counter. Their impacts are controlled by the toolchain, and their use does not require anymore information from the programmer.

#### Jumps
Jumps use a jump label to set the program count to a position within the program.

##### Syntax
*mnemonic* **(** *jump_label* **)** **;**

##### Mnemonics
Supported jumps and their mnemonics are below
* **JMP**, an unconditional jump
* **JLT**, jump if the first operand of the last comparison operation was less than the second operand.

##### Timings
* The program counter value is over written within exe stage of the pipeline.

### Block Access Manager Operations

Block Access Manager (BAM) Operations control and change the state of BAM units within the FPE.

#### Reset

The BAM Reset Operation resets the addressed BAM's offset to zero, it is advised that it be run before any BAM accesses are used so the BAM's offset (and therefore address) are in a known state.

##### Syntax
**RESET** **BAM** **[** _select_ **]** **;**

##### Timings
* The BAM's offset is updated in the exe stage of the pipeline.

#### Seek

The BAM Seek Operation is used to change a BAM's offset outset a BAM access. It has the benefit that it fetches its increment value, this means it is not bound to steps of the BAM's generic increment value and can instead be any numeric value from memory, even ones derived from input to the FPE.

##### Syntax
**SEEK** **BAM** **[** _select_ **]** **(** *memory_fetch* **)** **<** _mods_ **>** **;**

##### Mods
* **FORWARD**, denotes the seek is forward, causes the fetched value to be added to the BAM's offset. Mutually exclusive with **BACKWARD**
* **BACKWARD**, denotes the seek is backward, causes the fetched value to be subtracted from the BAM's offset. Mutually exclusive with **FORWARD**

##### Timings
* The increment value is read within the data fetch stage of the pipeline.
* The BAM's offset is updated in the exe stage of the pipeline.

### ALU Operations

ALU Operations require the inclusion of an ALU in the FPE. When the ALU is included in the FPE it's data_width must be set to a natural number in the parameter file.

ALU operations can access a special memory location called the accumulator (ACC), which is always set to the result of the last ALU operation. To do this the memory access is replaced with keyword **ACC**. Eg CMP (ACC, 1) compares the accumulator with the immediate value 1. Note even if the accumulator isn't used in place of a memory store the accumulator is still set to the result, replacing the memory_store with the **ACC** keyword,  just eliminates the store to another data memory.

#### 1 Fetch 1 Store ALU Operations

##### Syntax
*mnemonic* **(** *memory_fetch* **,** *memory_store* **)** **;**

##### Mnemonics
Supported 1 Fetch 1 Store ALU Operations and their mnemonics are below
* **MOV**, stores the fetched data to the memory specified within the store access
* **NOT**, stores the bitwise negation of the fetched data to the memory specified within the store access

##### Timings
* The fetch data is read in the data fetch stage of the pipeline
* The accumulator is set in the exe stage of the pipeline.
* The result is written in the data store stage of the pipeline

#### 2 Fetch 0 Store ALU Operations

##### Syntax
*mnemonic* **(** *memory_fetch* **,** *memory_fetch* **)** **;**

##### Mnemonics
Supported 2 Fetch 0 Store ALU Operations and their mnemonics are below
* **CMP**, compares the fetched values and sets the program counter's status register accordingly

##### Timings
* The fetch data is read in the data fetch stage of the pipeline
* The accumulator is set in the exe stage of the pipeline.
* For **CMP** the program counter is updated in the data store stage of the pipeline

#### 2 Fetch 1 Store ALU Operations

##### Syntax
*mnemonic* **(** *memory_fetch* **,** *memory_fetch* **,** *memory_store* **)** **;**

##### Mnemonics
Supported 2 Fetch 1 Store ALU Operations and their mnemonics are below
* **ADD**, stores the sum of the fetched data in the memory specified by the store access
* **AND**, stores the bitwise and of the fetched data in the memory specified by the store access
* **OR** , stores the bitwise or of the fetched data in the memory specified by the store access
* **XOR**, stores the bitwise exclusive or of the fetched data in the memory specified by the store access

##### Timings
* The fetch data is read in the data fetch stage of the pipeline
* The accumulator is set in the exe stage of the pipeline.
* The result is written in the data store stage of the pipeline
