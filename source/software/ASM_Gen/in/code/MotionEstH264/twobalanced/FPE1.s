// Set the position of first mvs
SETDMRBAUTOINCSIZE_0 2
SETREGVALUE R29, 30000
SETREGVALUE R27, 32
SETREGVALUE_ID R26
SETDMSIZE 82

// Wait 1418-local (84+4)=1330
RPT 26
NOP
NOP
NOP
  RPT 23
  NOP
  NOP
  NOP
    NOP
    NOP
  RPTEND
  NOP
RPTEND

// Loop begin point
// reset least SAD
// 84
RPT 20
MOV &(0!), R29
MOV &(0!), R26
NOP
  MOV &(0!), R29
  MOV &(0!), R26
  MOV &(0!), R29
  MOV &(0!), R26
RPTEND

// 16GET+25ADD+41*3MASK+3 = 167, *32+4
// match loop to 341, then cycle is 10916
RPT 32
INCDMWB_0 -41
MOV R28, R26
NOP
  GET R0, ^(0)
  GET R1, ^(0)
  GET R2, ^(0)
  GET R3, ^(0)
  GET R4, ^(0)
  GET R5, ^(0)
  GET R6, ^(0)
  GET R7, ^(0)
  GET R8, ^(0)
  GET R9, ^(0)
  GET R10, ^(0)
  GET R11, ^(0)
  GET R12, ^(0)
  GET R13, ^(0)
  GET R14, ^(0)
  GET R15, ^(0!)

  SETMASKLT &(0!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R5
    MOV &(0!), R5
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R6
    MOV &(0!), R6
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R7
    MOV &(0!), R7
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R8
    MOV &(0!), R8
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R9
    MOV &(0!), R9
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R10
    MOV &(0!), R10
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R11
    MOV &(0!), R11
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R12
    MOV &(0!), R12
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R13
    MOV &(0!), R13
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R14
    MOV &(0!), R14
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R15
    MOV &(0!), R15
    MOV &(0!), R28
  MASKEND

  // b0+b1, b4+b5
  ADD R16, R0, R1
  ADD R17, R4, R5
  // b0+b4, b1+b6
  ADD R18, R0, R4
  ADD R19, R1, R5
  // b2+b3, b6+b7
  ADD R0, R2, R3
  ADD R1, R6, R7
  // b2+b6, b3+b7
  ADD R4, R2, R6
  ADD R5, R3, R7
  // b8+b9, b12+b13
  ADD R2, R8, R9
  ADD R3, R12, R13
  // b8+b12, b9+b13
  ADD R6, R8, R12
  ADD R7, R9, R13
  // b10+b11, b14+b15
  ADD R8, R10, R11
  ADD R9, R14, R15
  // b10+b14, b11+b15
  ADD R12, R10, R14
  ADD R13, R11, R15
  
  // b0+b1+b4+b5
  ADD R20, R16, R17
  ADD R21, R0, R1
  ADD R22, R2, R3
  ADD R23, R8, R9
  
  SETMASKLT &(0!), R16
    MOV &(0!), R16
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R17
    MOV &(0!), R17
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R8
    MOV &(0!), R8
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R9
    MOV &(0!), R9
    MOV &(0!), R28
  MASKEND
  
  SETMASKLT &(0!), R18
    MOV &(0!), R18
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R19
    MOV &(0!), R19
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R5
    MOV &(0!), R5
    MOV &(0!), R28
  MASKEND  
  SETMASKLT &(0!), R6
    MOV &(0!), R6
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R7
    MOV &(0!), R7
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R12
    MOV &(0!), R12
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R13
    MOV &(0!), R13
    MOV &(0!), R28
  MASKEND
  
  // b0+b1+b2+b3+b4+b5+b6+b7
  ADD R0, R20, R21
  ADD R1, R22, R23
  ADD R2, R20, R22
  ADD R3, R21, R23
  
  SETMASKLT &(0!), R20
    MOV &(0!), R20
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R21
    MOV &(0!), R21
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R22
    MOV &(0!), R22
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R23
    MOV &(0!), R23
    MOV &(0!), R28
  MASKEND
  
  // total
  ADD R4, R0, R1
  
  SETMASKLT &(0!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(0!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  
  SETMASKLT &(0!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  
  // match loop 174
  RPT 17
  NOP
  NOP
  NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
  RPTEND
  
  ADD R28, R27, R28
  INCDMRB_0 -82
  INCDMWB_0 -82
RPTEND

// 8*20+6 = 166
RPT 20
PUT &(0!), ^0
INCDMRB_0 -1
NOP
  PUT &(0!), ^0
  INCDMRB_0 -1
  PUT &(0!), ^0
  INCDMRB_0 -1
  PUT &(0!), ^0
  INCDMRB_0 -1
  PUT &(0!), ^0
  INCDMRB_0 -1
RPTEND
PUT &(0!), ^0
INCDMRB_0 -83

// Match loop 11993-10916-84=993
RPT 23
NOP
NOP
NOP
  RPT 19
  NOP
  NOP
  NOP
    NOP
    NOP
  RPTEND
  NOP
RPTEND