// loop length 15037

// Set the position of first mvs
SETDMRBAUTOINCSIZE_0 2
SETREGVALUE R29, 30000
SETREGVALUE R27, 32
SETREGVALUE_ID R26
SETDMSIZE 82

// latency 1508 cycles, -88 local = 1420
RPT 24
NOP
NOP
NOP
  RPT 27
  NOP
  NOP
  NOP
    NOP
    NOP
  RPTEND
  NOP
RPTEND


// Loop begin point
// From here useful cycles 14046
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

// 41GET+41*3MASK+3 = 167, match to 431*32+4 = 13796
RPT 32
INCDMWB_0 -41
MOV R28, R26
NOP
  // To keep the fifo depth to be 41 in this level low, match length to FPE0  
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
  
  GET R16, ^0
  GET R0, ^0
  GET R17, ^0
  GET R1, ^0
  GET R2, ^0
  GET R8, ^0
  GET R3, ^0
  GET R9, ^0
  GET R18, ^0
  GET R19, ^0
  GET R4, ^0
  GET R5, ^0
  GET R6, ^0
  GET R7, ^0
  GET R12, ^0
  GET R13, ^0
  
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
  
  GET R20, ^0
  GET R21, ^0
  GET R22, ^0
  GET R23, ^0
  
  GET R0, ^0
  GET R1, ^0  
  GET R2, ^0
  GET R3, ^0
  GET R4, ^0
  
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
  
  // match loop 431 - 167 = 264
  RPT 52
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

// Match loop 15037-14046=991
RPT 21
NOP
NOP
NOP
  RPT 14
  NOP
  NOP
  NOP
    NOP
    NOP
    NOP
  RPTEND
  NOP
RPTEND