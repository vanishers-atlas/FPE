# Test 000

## Test Summary

A basic test to check the toonchain can generate an FPE process that can output lateral values

## Compounts Tested
* Control Components
* Immedate/lateral Memory
* Comm Put
* ALU

## Instructions Tested
* MOV#IMM[]#ALU#PUT[]

## Datapaths Tested
* ID:fetch -> IMM:addr
* IMM:data -> ALU:in
* ID:store -> PUT:addr
* ALU:in   -> PUT:data
