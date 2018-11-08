SETPARA_ALUTYPE INT32
SETPARA_PB0_ZERO
SETPARA_DIRECTWBEN_TRUE
SETPARA_DMWBINIT_0 512
SETPARA_DMRBINIT_N0 512
SETPARA_DMSIZE 1024
SETPARA_DMTRUE2R1W_TRUE
SETPARA_INFIFODEPTH 1024
SETPARA_OUTFIFODEPTH 64

// clear sub-block result
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
RPTEND

// 16 sub-block muls -> sub-block result
RPT 16
INCDMWB_0 -1024
NOP
  BARRIERM 1
  // read Bsub:8x64
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
  RPTEND
  
  // sub-block mul
  RPT 64
  NOP
  NOP
    // row x col, 8 cols
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
    RPTEND
    // next row
    INCDMRB_M0 -512
    INCDMRB_N0 8
    INCDMWB_0 8
  RPTEND
  INCDMRB_N0 -512
  INCDMWB_0 -1024
RPTEND

// Output stages
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
RPTEND