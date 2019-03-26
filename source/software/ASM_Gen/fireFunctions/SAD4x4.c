static inline void SAD4x4(int cur[16][16], int ref[16][16], int out[16]){
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
}
