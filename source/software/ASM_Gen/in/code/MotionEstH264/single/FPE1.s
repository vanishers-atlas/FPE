SETREGVALUE R29, 30000

// Wait 10868 cycles
RPT 53
NOP
NOP
  RPT 25
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
  NOP
  NOP
RPTEND

// Loop begin point, wait 19069-10868 = 8201 cycles
RPT 55
NOP
NOP
  RPT 29
  NOP
  NOP
    NOP
    NOP
    NOP
    NOP
    NOP
  RPTEND
  NOP
RPTEND
NOP
NOP
NOP

// (8*32+9)*41+3 = 10868
RPT 41
MOV R0, R29
NOP
  RPT 32
  NOP
  NOP
    GET R10, ^(0)
    GET R11, ^(0!)
    NOP
    NOP
    NOP
    SETMASKLT R0, R10
      MOV R0, R10
      MOV R1, R11
    MASKEND
  RPTEND
  
  NOP
  NOP
  NOP
  NOP
  PUT R0, ^0
  PUT R1, ^0
RPTEND