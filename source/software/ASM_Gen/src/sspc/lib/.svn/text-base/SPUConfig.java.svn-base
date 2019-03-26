package sspc.lib;

import sspc.hardgen.SSPConfig;

public class SPUConfig {
	public SPUConfig(SSPConfig topconf) {
		sspconf = topconf;
	}
	
	public ALUTYPE coreType = ALUTYPE.REAL16B1D;
	
	public SSPConfig sspconf;
	
	/** SMID way number */
	public int simdWay = 1;
	
	/** Control Pipeline **/
	public boolean mulregEn = false;
	public int Pb0Depth = 1;
	public int Pb1Depth = 1;
	public int Pb2Depth = 1;
	public int Pa0Depth = 1;
	public int Pa1Depth = 1;
	public int Pa1xDepth = 0;
	
	/** Control Branch **/
	public boolean branchEn = false;
	public boolean jmpEn = false;

	public boolean rptEn = false;
	public boolean rptUseSRL = false;
	public int rptLevels = 0;
	public boolean rptSpec1 = false;
	public int rptCntWidth0 = 1;
	public int rptCntWidth1 = 1;
	public int rptCntWidth2 = 1;
	public int rptCntWidth3 = 1;
	public int rptCntWidth4 = 1;
	public int rptBlkWidth0 = 1;
	public int rptBlkWidth1 = 1;
	public int rptBlkWidth2 = 1;
	public int rptBlkWidth3 = 1;
	public int rptBlkWidth4 = 1;
	
	/** Control Supported Instructions */
	public boolean maskEn = false;
	public boolean maskeqEn = false;
	public boolean maskgtEn = false;
	public boolean maskltEn = false;
	
	public boolean alusra1En = false;
	
	public boolean absdiffEn = false;
	public int absdiffType = 1; // Default dsp48(|a-b|)
	
	/** Control Flexible Ports **/
	public int flexAType = 0; // I|M|R
	public int flexBType = 0;
	public int flexCType = 0;
	
	/** Control FIFO **/
	public boolean getiEn = false;
	public boolean getchEn = false;
	public boolean putchEn = false;
	public int iChNo = 1;
	public int iChWidth = 1;
	public int oChNo = 1;
	public int oChWidth = 1;
	
	// Used for IOCore
	public boolean iCh2LevEn = false;
	public int iChWidth0 = 1;
	public int iChWidth1 = 1;
	public boolean oCh2LevEn = false;
	public int oChWidth0 = 1;
	public int oChWidth1 = 1;
	
	public boolean bypassPUTEn = true;
	
	/** Control memory **/
	public boolean rfEn = true;
	public int regSize = 32;
	public int regWidth = 5;
	public boolean rfInitEn = false;
	
	public int pmDataWidth = 32;
	public int pmSize = 1024;
	public int pmWidth = 10;
	public boolean useBRAMForLargePM = true;
	
	public boolean smEn = false;
	public int smSize = 32;
	public int smOffsetWidth = 5;
	public int smWidth = 5;
	public boolean useBRAMForLargeSM = true;
	public boolean smReadonly = true;
	public boolean smDirectEn = true;
	public boolean smOffsetEn = false;
	public boolean smRBSetEn0 = false;
	public int smRBAutoincSize0 = 1;
	public int smWBAutoincSize0 = 1;
	public boolean smRBAutoincEn0 = false;
	public boolean smWBAutoincEn0 = false;
	public boolean smRBIncEn0 = false;
	public boolean smWBIncEn0 = false;
	
	/** Data memory stuff */
	public boolean dmEn = false;	
	public int dmOffsetWidth = 5;
	public int dmSize = 32;
	public int dmWidth = 5;
	public int dmDataWidth = 16;
	public boolean dmInitEn = false;
	public boolean useBRAMForLargeDM = true;
	public int dmRBNum0 = 0;
	public int dmRBNum1 = 0;
	public boolean useTrue2R1W = false;
	public int dmRBInitialB0 = 0;
	public int dmRBInitialB1 = 0;
	public int dmRBInitialB2 = 0;
	public int dmRBInitialC0 = 0;
	public int dmWBInitial = 0;
	public int dmRBAutoincSizeB0 = 1;
	public int dmRBAutoincSizeB1 = 1;
	public int dmRBAutoincSizeB2 = 1;
	public int dmRBAutoincSizeC0 = 1;
	public int dmWBAutoincSize = 1;
	public boolean dmDirectEn = true;
	public boolean dmOffsetEn = false;
	public boolean dmRBSetEnB0 = false;
	public boolean dmRBSetEnB1 = false;
	public boolean dmRBSetEnB2 = false;
	public boolean dmRBSetEnC0 = false;
	public boolean dmWBSetEn = false;
	public boolean dmRBAutoincEnB0 = false;
	public boolean dmRBAutoincEnB1 = false;
	public boolean dmRBAutoincEnB2 = false;
	public boolean dmRBAutoincEnC0 = false;
	public boolean dmWBAutoincEn = false;
	public boolean dmRBIncEnB0 = false;
	public boolean dmRBIncEnB1 = false;
	public boolean dmRBIncEnB2 = false;
	public boolean dmRBIncEnC0 = false;
	public boolean dmWBIncEn = false;
	
	/** External Memory **/
	public int emBurstLen = 2;
    public int emRBNum = 2;
    public int emRBInitial0 = 10000;
    public int emRBInitial1 = 20000;
    public int emWBInitial0 = 30000;
    public int emRBAutoincSize0 = 16;
    public int emRBAutoincSize1 = 16;
    public int emWBAutoincSize0 = 16;
    public boolean emRBAutoincEn0 = true;
    public boolean emRBAutoincEn1 = true;
    public boolean emWBAutoincEn0 = true;
    public boolean emRBIncEn0 = true;
    public boolean emRBIncEn1 = true;
    public boolean emWBIncEn0 = true;
	
	public enum ALUTYPE {
		REAL16B1D, CPLX16B4D, REAL32B4D
	}
	
	public int DataWidth() {
		switch (coreType) {		
		case REAL16B1D:
			return 16;
		case CPLX16B4D:
			return 16;
		case REAL32B4D:
			return 32;
		default: 
			return 16;
		}
	}
	
	/**
	 * Real is 1; Complex is 2
	 * @return
	 */
	public int DataType() {
		switch (coreType) {		
		case REAL16B1D:
		case REAL32B4D:
			return 1;
		case CPLX16B4D:
			return 2;
		default: 
			return 1;
		}
	}
	
	public int DSP48ENum() {
		switch (coreType) {		
		case REAL16B1D:
			return 1;
		case CPLX16B4D:
		case REAL32B4D:
			return 4;
		default: 
			return 1;
		}
	}
	
	public int CoreDataWidth() {
		switch (coreType) {		
		case REAL16B1D:
			return 16;
		case CPLX16B4D:
		case REAL32B4D:
			return 32;
		default: 
			return 16;
		}
	}
	
	/**
	 * The number of distinct OPMODEs for DSP48E
	 * @return
	 */
	public int OPMODENum() {
		switch (coreType) {		
		case REAL16B1D:
		case REAL32B4D:
			return 1;
		case CPLX16B4D:
			return 2;
		default: 
			return 1;
		}
	}
	
	/**
	 * The number of distinct ALUMODEs for DSP48E
	 * @return
	 */
	public int ALUMODENum() {
		switch (coreType) {		
		case REAL16B1D:
		case REAL32B4D:
			return 1;
		case CPLX16B4D:
			return 3;
		default: 
			return 1;
		}
	}
	
	/**
	 * Maximum possible offset width for SM and DM
	 * @return
	 */
	public int maxOffsetWidth() {
		if (regWidth == 5) 
			return 8;
		else
			return 6;
	}
	
	/**
	 * Extra width between opcode and 4*regWidth 
	 * @return
	 */
	public int extraWidth() {
		if (regWidth == 5)
			return 6;
		else
			return 2;
					
	}
	
	public int RPTOverhead() {
		int oh = 0;
		oh = Pb0Depth + Pb1Depth + Pb2Depth;
		return oh;
	}
	
	/////////////////////////////////////////////////////////////////////
	// Methods
	public void setRFSize(int size) {
		regSize = size;
		regWidth = (int) (Math.log(size)/Math.log(2));
	}
}
