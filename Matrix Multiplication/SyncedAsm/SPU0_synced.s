RPT 64
NOP
NOP
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
  CLR &(0!)
RPT 16
INCDMWB_0 -1024
NOP
  BARRIERM 1
  RPT 64
  NOP
  NOP
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
    GET &(0!), ^0
  RPT 64
  NOP
  NOP
    RPT 64
    NOP
    NOP
      ADDMUL &0(0), &(0!), ^p0, &0(0)
      ADDMUL &1(0), &(0!), ^p0, &1(0)
      ADDMUL &2(0), &(0!), ^p0, &2(0)
      ADDMUL &3(0), &(0!), ^p0, &3(0)
      ADDMUL &4(0), &(0!), ^p0, &4(0)
      ADDMUL &5(0), &(0!), ^p0, &5(0)
      ADDMUL &6(0), &(0!), ^p0, &6(0)
      ADDMUL &7(0), &(0!), ^0, &7(0)
    INCDMRB_M0 -512
    INCDMRB_N0 8
    INCDMWB_0 8
  INCDMRB_N0 -512
  INCDMWB_0 -1024
RPT 64
NOP
NOP  
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  PUT &(0!), ^0
  BARRIERM 1
