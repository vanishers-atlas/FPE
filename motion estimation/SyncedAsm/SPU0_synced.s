BARRIERM 0
RPT 16
NOP
NOP
  RPT 13
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  GET &(0!), ^0
RPT 47
NOP
NOP
  RPT 13
  GET &(0!), ^0
  GET &(0!), ^0
    GET &(0!), ^0
  GET &(0!), ^0
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
  INCDMRB_M0 -256
  INCDMRB_N0 -240
  PUTCA ^0
  BARRIERS
INCDMRB_N0 -512
