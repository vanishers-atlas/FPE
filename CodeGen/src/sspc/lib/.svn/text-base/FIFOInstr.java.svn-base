package sspc.lib;

public class FIFOInstr {
	public FIFOInstr() {}
	
	public FIFOInstr(AsmInstr ai, int chNo, boolean isget) {
		asmInstr = ai;
		channelNo = chNo;
		isGET = isget;
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	
	public void setCycleAfterSync(int cycle) {
		cycleAfterSync = cycle;
	}
	
	public int getChannelNo() {
		return channelNo;
	}
	
	public void setInsertedNops(int num) {
		insertedNops = num;
	}
	
	public int getInsertedNops() {
		return insertedNops;
	}
		
	public int getCycleAfterSync() {
		if (cycleAfterSync == -1)
			return asmInstr.cycle;

		return cycleAfterSync;
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                        public variable                   ////
	/** Indicate this instruction is GET or PUT */
	public boolean isGET;
	
	/** If this is a GET, indicate weather it is a leading GET. Leading GETs 
	 *  are GET those are before the first inter-PE PUT instruction. The 
	 *  synchronisation of leading GETs only incur startup overheads, i.e. the
	 *  inserted NOPs are only inserted outside the loop body.
	 */
	public boolean isLeadingGET = false;
	
	// The corresponding assembly instruction
	public AsmInstr asmInstr;
	
	/* Cycle after synchronisation */
	public int cycleAfterSync = -1;
	
	/* The local channel index */
	public int channelNo = 0; 
	
	public int insertedNops;
	
}
