SETPARA_DMSIZE 1008
SETPARA_DMRBINIT_N0 256
SETPARA_PB0_ZERO
SETPARA_DIRECTWBEN_TRUE
SETPARA_DMDATAWIDTH 8
SETPARA_DSP48EN_FALSE
SETPARA_INFIFODEPTH 1024
SETPARA_OUTFIFODEPTH 1

BARRIERM 1
RPT 16
NOP
NOP
  RPT 13
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  RPTEND
  GET &(0!), ^0
RPTEND

RPT 47
NOP
NOP
  RPT 13
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  RPTEND
  GET &(0!), ^0
RPTEND

RPT 32
INCDMWB_0 -1008
NOP
  RPT 16 
  ABSDIFFCLR
  NOP
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
    ABSDIFFACCUM &(0!), &(0!)
  RPTEND    
  INCDMRB_M0 -256
  // -16*16+16
  INCDMRB_N0 -240
  PUTCA ^0
  BARRIERS
RPTEND
// -32*16
INCDMRB_N0 -512