# Documentation for FPE.toolchain

27/05/2020, Created by Stephen Clarke,

## introduction

The FPE toolchain consists of 3 main tools:
* The config extractor, which takes an FPE assembly program and produces a config json file for a lean FPE to run the given program
* The HDL generation scripts, which takes an FPE config json and creates the HDL files for the FPE described by that config
* The assembler, which takes both an FPE assembly program and config json of an FPE capable of runnning the program and uses them to set the FPE's generics and prepare its memory files (eg program memory)

Each of these tools has its own subfolder, in addition there are a number of other subfolders:
* HDL_assembly, as both the config extractor and assembler interact with FPE assembly files to improve maintainability the reading and basic correctness checking of FPE assembly files is handled by a set of functions shared between both tools. This set of functions is stored within HDL_assembly. It is also where the documentation of the FPE assembly is stored
* tests, contains a collection of tests to aid in the retesting of the toolchain when modifications are made
* util, contains a collection of functions that are used in numerous places throughout the toolchain
