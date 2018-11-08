// Loop Length 15037

SETDMSIZE 1024

// 17*16+4 = 276
RPT 16
NOP
NOP
NOP
  RPT 12
  GET &(0!), ^0
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  RPTEND
  GET &(0!), ^0
RPTEND

// 17*47+4 = 803
RPT 47
NOP
NOP
NOP
  RPT 12
  GET &(0!), ^0
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  RPTEND
  GET &(0!), ^0
RPTEND

// ((21*4+5)*4+6+74)*32+6 = 13958
RPT 32
NOP
NOP
NOP
  RPT 4
  NOP
  NOP
  NOP
    RPT 4
    NOP
    NOP
    NOP
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      // make a hole for memory writting
      NOP
      ABSDIFFACCUM &(0!), &(0!)
      // -4+16
      INCDMRB_ALL 12
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      INCDMRB_ALL 12
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      INCDMRB_ALL 12
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!), &(0!)
      // -4*16
      INCDMRB_ALL -64
    RPTEND
    // -16+4*16
    INCDMRB_ALL 48
  RPTEND
  // -256+16
  INCDMRB_1 -240
  INCDMWB_0 -16
  
  // +47*16
  INCDMRB_0 752
  
  MOV R0, &(0!)
  MOV R1, &(0!)
  MOV R2, &(0!)
  MOV R3, &(0!)
  MOV R4, &(0!)
  MOV R5, &(0!)
  MOV R6, &(0!)
  MOV R7, &(0!)
  MOV R8, &(0!)
  MOV R9, &(0!)
  MOV R10, &(0!)
  MOV R11, &(0!)
  MOV R12, &(0!)
  MOV R13, &(0!)
  MOV R14, &(0!)
  MOV R15, &(0!)
  
  PUT R0, ^0
  PUT R1, ^0
  PUT R2, ^0
  PUT R3, ^0
  PUT R4, ^0
  PUT R5, ^0
  PUT R6, ^0
  PUT R7, ^0
  PUT R8, ^0
  PUT R9, ^0
  PUT R10, ^0
  PUT R11, ^0
  PUT R12, ^0
  PUT R13, ^0
  PUT R14, ^0
  PUT R15, ^0
  
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
  
  PUT R16, ^0
  PUT R0, ^0
  PUT R17, ^0
  PUT R1, ^0
  PUT R2, ^0
  PUT R8, ^0
  PUT R3, ^0
  // b0+b1+b2+b3+b4+b5+b6+b7
  ADD R0, R20, R21
  ADD R1, R22, R23
  ADD R2, R20, R22
  ADD R3, R21, R23
  PUT R9, ^0
  PUT R18, ^0
  PUT R19, ^0
  PUT R4, ^0
  PUT R5, ^0
  PUT R6, ^0
  PUT R7, ^0
  PUT R12, ^0
  PUT R13, ^0
  
  // total
  ADD R4, R0, R1
  
  PUT R20, ^0
  PUT R21, ^0
  PUT R22, ^0
  PUT R23, ^0
  
  PUT R0, ^0
  PUT R1, ^0  
  PUT R2, ^0
  PUT R3, ^0
  PUT R4, ^0
  
  // -(1008+16)
  INCDMRB_0 -1024
RPTEND
// -32*16
INCDMRB_1 -512
INCDMWB_0 -1008