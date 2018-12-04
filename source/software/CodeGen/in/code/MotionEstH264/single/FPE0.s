// Loop length 19069

SETDMRBAUTOINCSIZE_1 2
SETDMRBINIT_1 1024
SETREGVALUE R29, 30000
SETREGVALUE R27, 32
SETREGVALUE_ID R26
SETDMSIZE 1106

// Loop begin point
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

// ((21*4+5)*4+5+5+41+41*3)*32+6 = 16966
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
  INCDMRB_C0 -240
  
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
  
  // -16-1008
  INCDMRB_0 -1024
  
  SETMASKLT &(1!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R5
    MOV &(0!), R5
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R6
    MOV &(0!), R6
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R7
    MOV &(0!), R7
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R8
    MOV &(0!), R8
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R9
    MOV &(0!), R9
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R10
    MOV &(0!), R10
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R11
    MOV &(0!), R11
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R12
    MOV &(0!), R12
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R13
    MOV &(0!), R13
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R14
    MOV &(0!), R14
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R15
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
  
  SETMASKLT &(1!), R16
    MOV &(0!), R16
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R17
    MOV &(0!), R17
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R8
    MOV &(0!), R8
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R9
    MOV &(0!), R9
    MOV &(0!), R28
  MASKEND
  
  SETMASKLT &(1!), R18
    MOV &(0!), R18
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R19
    MOV &(0!), R19
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R5
    MOV &(0!), R5
    MOV &(0!), R28
  MASKEND  
  SETMASKLT &(1!), R6
    MOV &(0!), R6
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R7
    MOV &(0!), R7
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R12
    MOV &(0!), R12
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R13
    MOV &(0!), R13
    MOV &(0!), R28
  MASKEND
  
  // b0+b1+b2+b3+b4+b5+b6+b7
  ADD R0, R20, R21
  ADD R1, R22, R23
  ADD R2, R20, R22
  ADD R3, R21, R23
  
  SETMASKLT &(1!), R20
    MOV &(0!), R20
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R21
    MOV &(0!), R21
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R22
    MOV &(0!), R22
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R23
    MOV &(0!), R23
    MOV &(0!), R28
  MASKEND
  
  // total
  ADD R4, R0, R1
  
  SETMASKLT &(1!), R0
    MOV &(0!), R0
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R1
    MOV &(0!), R1
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R2
    MOV &(0!), R2
    MOV &(0!), R28
  MASKEND
  SETMASKLT &(1!), R3
    MOV &(0!), R3
    MOV &(0!), R28
  MASKEND
  
  SETMASKLT &(1!), R4
    MOV &(0!), R4
    MOV &(0!), R28
  MASKEND
  
  ADD R28, R27, R28
  // -82 to beginning of minSAD, -16 to beginning of SAD4x4
  INCDMWB_0 -98
  INCDMRB_1 -82
RPTEND
// -32*16
INCDMRB_C0 -512
INCDMWB_0 -1008

// 4*20+6 = 86
INCDMRB_0 1024
RPT 20
PUT &(0!), ^0
PUT &(0!), ^0
NOP
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
RPTEND
INCDMRB_0 -1106