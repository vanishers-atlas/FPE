# Documentation for FPE_assembly\\generation

Created 21/01/2020 by Stephen Clarke,

## Preample

This file documents FPE_assembly\\generation, within this folder there are a number of files related to the generation and expandation of FPE assembly grammars.
The main file is _generation_FPE_grammar.py_, a python 3 script used to (re)generation FPE grammars.
It is hardcoded to read data from _FPE_grammar.json_; and use _antlr-4.7.2-complete.jar_ to generate an FPE grammar and the ANTLR files requires to process it within python 3 scripts.
These files will output in FPE_assembly\\grammar)

## Common FPE grammar feactures

Regardless of the input given to _generation_FPE_grammar.py_ there are some features that will be in the generated FPE grammar.

#### Scopes

Scopes are present in every FPE grammar, as an FPE assembly program should be writen within a scope body for the toolchain to process it currently.
Along with scopes comes the idea of statements, that is controlled rules which can be within a scope.

#### Labels

Due to how different they syntac is from the rules conbtrol by the input json file label are always present in FPE assembly grammars.
As these labels don't become instructions in the assembled code this doesn't incur any cost on the resulting hardware

#### Timing construsts

As the pipeljne of any FPE instance isn't knew until after it is run throught the pipeline (config generater, and HDL generation scipts), explisite timing (eg insertion of NOPs) is impractable, instead all FPE grammars use a set of 3 timing construsts: before mods, after mods, and delay statements.
This constructs are present in all FPE grammars

#### Comments

Every FPE grammar supports 2 types of comment, rest of line (\\\\), and multiline (\\\\* ... *\\\\)

#### Whitespace Insensitive

Every FPE grammar skips over all Whitespace, only used it to denote breaks between tokens.

#### Case Insensitive keywords

All FPE grammars are case insensitive for keywords, the other case sensitive part of the common feactures are labels

## Controlled Rules

Many of the rules present in an FPE grammar are controlled by the input given to _generation_FPE_grammar.py_. this sectain detailled this rules and how their are controlled using _FPE_grammar.json_

### Rule Types

All the controlled rules haver a rule type, this type determines the possible syntax of the rule's instruction, along with where an FPE assembly program the rule's instructions can appear.
Within _FPE_grammar.json_ and rule's type is determed by which second level (first key) it is contained within.
There are currently three types of rules.

#### Wrapper Rules

Wrappers rules are statements that end what, ie wrap, a new scope.

Wrapper rules support _mnemonics_, _component_select_, _address_, _operands_, _mods_, and _timing_mods_ rule fields/markers (see Rule Fields/Markers section for details)

An example for an instruction that uses a wrapper rule type, is the ZOL (Zero Overhead Loop).
At uses the wrapped scope to determine exaxtly which instruction are contained by within the loop body

#### Operation Rules

Operation rules are statements there have no speacal syntax (only rule fields).

Operation rules support _mnemonics_, _component_select_, _address_, _operands_, _mods_, and _timing_mods_ rule fields/markers (see Rule Fields/Markers section for details)

An example of an rule that uses the operation type is MOV.
it only rewuires a mnemonic and  2 operands, and doesn't need any special syntax so it can be a operation type rule

#### Access Rules

Access rules are used to access data within the FPE's memories.
Their are not statements, (thus can't just be within a scope), however they can be accessed within the _address_, and _operands_ rule fields, via the two data types they define: _src_ and _dst_

Access rules support _mnemonics_, _component_select_, _address_, _operands_, _mods_,  _timing_mods_, _is_src_, and _is_dst_ rule fields/markers (see Rule Fields/Markers section for details)

An example of an access rule is the ROM access, used to get data from the FPE's internal ROM

### Rule name

Within the grammar each rule must have an unique name, this is achieved by have each rule within the same type having a unique name, then concatinf the rule type this rule name.
Within _FPE_grammar.json_ and rule's name is determed by which third level (second key) it is contained within.


### Rule Fields/Markers

Rules use a combination of rule fields, to set their syntax, and rule markers, to set how they interacter with the rest of the grammat.
Rule fields are checking in a set order, and if present each add a set syntaxe to the overall rule.

#### Data types within FPE grammars

A number of rule fields require data types, there are 2 that are always present in an FPE grammar:
- _NUMBER_, a number token straight from the parser.
Current three different number formats are accepted by FPE grammars
  - Binary, a block of *0*, and *1*; prefixed with *0b*
  - Hexadecimal, a block of *0-9*, *A-F*, and *a-f*;  prefixed with *0x*
  - Decimal, a block token straight from the pa of *0-9*, optionally prefixes with a *+* or *-*
- _STRING_, a string token straight from the parser.
A parser STRING tokens are defined a block of letters, numbers, and/or underscores. where the the first character is not a number

In addition to the straight token data types there are 2 rule marker define data types: _src_, and _dst_, with will be in almost every FPE grammar.
These types are used to get data from/put data into the different memories within an FPE.

##### Note on handling immedate/literal values

The _scr_ data type can handle immedate/literal data value, via an automatical included access call _imm_access_.
The means that both _NUMBER_, and _src_ can be used to pass an immedate/literal value to a rule, however I recommend only one be used in a rule field; this both keeps the grammar unsmbigous, and means that only one of the types needs for each loctation by the toolchain.

**Use _NUMBER_ if**
1. The immedate/lateral value needs to be known at synthasous time
2. date/lateral values are used by this rule

**Use _src_ if**
1. Other src accesses are already being used

#### Rule fields

All rule fields are explained here.
the order here, matches the order in which they are tested for in _generation_FPE_grammar.py_.

#####  _Mnemonics_

This rule field is used to list all acceptable mnemonics for a rule.
Its propuse is reduce the number of nearly identical rules, by combining rules which differ only by their mnemonics.
For example: _AND_, and _ADD_ operations both take 3 operands: 2 _scr_ (who's order doesn't matter), followed a _dst_; support FPE timing mods, don't have custum mods; in fact only differance is what the ALU does to the inputs to get the output.
This makes them good candadates for merging into a single rule to reduce repeated code in the toolchain to handle 2 nearly identical rules.

###### Syntax Added to Rule
A case insensitive keyword token

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
An list under the key "_mnemonics_" within a rule's dictionary.
This list should contain all mnemonics accepted by the rule. Case insensitive is handled by the grammar so one string for each mnemonic is enough.

##### _Component Select_

This rule field is used to list all valid compount select data types.
Component selects are required when more than one component of each type can be contained within an FPE, eg multiple BAM units.
Multiple compounts may be used to efficently handle different data widths within the same compount type, or to split an address space where different regions have different pipeline characteristics.
These latter reason can be hidden from programmer how the component select, and address rule fields add the same syntax to a rule and are processed beside each other.

###### Syntax Added to Rule
One of the listed data types in square brackets

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
An list under the key "_comp_select_" within a rule's dictionary.
This list should contain all data types accepted by the rule.

##### _Address_

This rule field is used to list all valid compount select data types.
Within rules, addresses are used to pass address values. Eg which channel to read/write in a comm access, or where is a RAM to store some data

###### Syntax Added to Rule
One of the listed data types in square brackets

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
An list under the key "_address_" within a rule's dictionary.
This list should contain all data types accepted by the rule.

##### _Operands_

This rule field is used to both determine the number of operands a rule takes, and also to list all valid data types for each operand.
Within rules, operands are used to pass data values. Eg input value to be added, and the resulting value

###### Syntax Added to Rule
A comma seperated list of the rule's operands, enclosed by round brackets

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
A list of lists under the key "_operands_" within a rule's dictionary.
Within the root list there should be a list for each operand the rule has.
Each of these child lists should contain all data types accepted by the rule for that operand.


#####  _Mods_

This rule field is used to add custion modifiers to a rule.
Within rules, modifiers are used to pass extra information to the toolchain, this extra information by be used to create more efficent HDL, and/or slightly change the effects of the instrction.

###### Syntax Added to Rule
An opotional comma seperated list of the rule's modifiers, enclosed by angle brackets

Note if timing mods are in use both timing and custom mods will share the some list

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
A list of dictionary under the key "_mods_" within a rule's dictionary.
There should 1 dictionary for each poosible modifier inside the root list.
The child dictionaries, must contain a field called _flag_, which define the keyword of the modifier, then if a value is nexted for the modifier its type should be in a fields valued _value_

#####  _Timing mods_

This rule field is used to control if timing modifiers are used by a rule.
Timing mods are used, along with delay statements, to ensure data dependancities are resaolved correctly with FPS assembly programs.
This system is used is because an FPE's pipeline isn't set until synthasous time, therefore the more common system of leaving it to a programmer to inserts NOPs to resolve data dependancities because very complex.

###### Syntax Added to Rule
An opotional comma seperated list of the rule's modifiers, enclosed by angle brackets

Note if custom mods are in use both timing and custom mods will share the some list

###### Supported by rule types
Wrappers, Operations, and Accesses

###### Encoding in _FPE_grammar.json_
To enable timing mods the "_timing_mods_" field of a rule's dictionary must be set to _true_.
if this field is set to any other value or obtained timing mods won;t be enables for the rule.

#### Rule markers

##### _Is src_

This rule marker marks an access as a _src_, meaning it will be part of the _src_ data type.

###### Supported by rule types
Accesses

###### Encoding in _FPE_grammar.json_
To enable timing mods the "_Is_src_" field of a rule's dictionary must be set to _true_.
if this field is set to any other value or obtained timing mods won;t be enables for the rule.

##### _Is dst_

This rule marker marks an access as a _dst_, meaning it will be part of the _dst_ data type.

###### Supported by rule types
Accesses

###### Encoding in _FPE_grammar.json_
To enable timing mods the "_Is_dst_" field of a rule's dictionary must be set to _true_.
if this field is set to any other value or obtained timing mods won;t be enables for the rule.
