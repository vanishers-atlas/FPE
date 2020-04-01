# Documentation for FPE_assembly

07/02/2020 needs updating/rewrite following assembly tidy up
Created 21/01/2020 by Stephen Clarke,
07/02/2020

## Preample

This folder sevres 2 propuses:
1. The act as a python 3 package to reduce repeatation of common code related to handling the FPE assemble language. However at the moment this is limited to loading FPE assemble (.fpea) files and returning their ANTLR trees.
2. The contains files related the the (re)generation of FPE assembly grammars.

At the moment only a single FPE grammar can be active at any one time. The active grammar is stored in the _grammar_ subfloder (or the symbolically linked to it), Documentation for any FPE grammar should be found within their sub folder.

Documentation for the generation tools choyuld be found in the _generation_ subfubfolder.

The remainer of the file will document the FPE_assembly package

## FPE_assembly package

### Functions

#### load_file

##### parameters

1. filename _string_, the path to the file to be loaded. This file doesn't require any particular extention, however I recommend using **.fpea** to help demark FPE assembly files.

##### Returns

If the root of an ANTLR tree repesentation of the loaded FPE assembly file

##### Throws

- FileNotFoundError, if _filename_ can't be loaded.

##### Details

This function takes a filename (_filename_), and trys to load it as a FPE assembly file using the currently active grammar. If the input doesn't prefectly fit into the currently active grammar, ANTLR will print messages containing the line and colume of the mismatched input, but wouldn't throw an error. I've been unable to find a way to have the script recieve and handle this error (possible future work)
