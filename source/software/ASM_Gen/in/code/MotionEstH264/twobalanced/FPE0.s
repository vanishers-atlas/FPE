// Loop length 11993
SETDMSIZE 1008

// 17*16+3 = 275
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

// 17*47+3 = 802
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

// ((20*4+4)*4+5)*32+4 = 10916
RPT 32
INCDMWB_0 -1008
NOP
  RPT 4
  NOP
  NOP
    RPT 4
    NOP
    NOP
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
      ABSDIFFACCUM &(0!), &(0!)
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
      ABSDIFFACCUM ^0, &(0!), &(0!)
      // -4*16
      INCDMRB_ALL -64
    RPTEND
    // -16+4*16
    INCDMRB_ALL 48
  RPTEND
  INCDMRB_0 -256
  // -256+16
  INCDMRB_1 -240
RPTEND
// -32*16
INCDMRB_1 -512