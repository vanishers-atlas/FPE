package sspc.hardgen;

import java.util.Vector;

import sspc.lib.FIFOConfig;
import sspc.lib.SPUConfig;

public class SSPConfig {
	public Vector<String> commArray = new Vector<String>();
	public Vector<SPUConfig> SPUConfs = new Vector<SPUConfig>();
	public Vector<FIFOConfig> FIFOConfs = new Vector<FIFOConfig>();
	
	// The width of core data width. If it is complex core, then coreWidth is dataWidth*2.
	public int coreWidth   = 16;
	// This is the width for input data (FIFO data). It is often less than 
	// dataWidth, like memory data is 8bit, but core data is 16bit.	
	public int inputWidth   = 16;
	public int outputWidth   = 16;
	
	public boolean noIOCore = true;
	
	public int dataWidth = 16;
	public int fracBits = 14;
	
	public double Min;
	public double Max;
	public double Precision;
	
	/**
	 * Initialise helper variables
	 */
	public void init() {
		Min = -1*Math.pow(2, dataWidth-fracBits-1);
		Max = Math.pow(2, dataWidth-fracBits-1);
		Precision = Math.pow(2, -1*fracBits);
	}
}
