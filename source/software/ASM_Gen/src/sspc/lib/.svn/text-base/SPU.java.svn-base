package sspc.lib;

import java.util.LinkedList;
import java.util.List;

import sspc.softgen.SWGenUtils;

public class SPU {
	public SPU(SSP ssp, String name) {
		this.name = name;
		
		// Currently assume idx is got from name
		if (name.equals("IOCore")) 
			idx = -1;
		else 
			idx = SWGenUtils.getDigits(name);
		
		this.ssp = ssp;
		sm = new SharedMem(this);
		
		conf  = new SPUConfig(ssp.conf);
    }
	
    ///////////////////////////////////////////////////////////////////
    ////                         public  methods                   ////
	
	/**
	 * Return true is this FPE is actually SOURCE 
	 * @return
	 */
	public boolean isExtIn() {
		return name.equals("SOURCE");
	}
	
	/**
	 * Return true is this FPE is actually SINK 
	 * @return
	 */
	public boolean isExtOut() {
		return name.equals("SINK");
	}
	
	/**
	 * Get the specified PE
	 * @param idx
	 * @return
	 */
	public PE getPE(int idx) {
		return PEs.get(idx);
	}
    ///////////////////////////////////////////////////////////////////
    ////                         public  variables                ////
    
    public List<PE> PEs = new LinkedList<PE>();
    
	public String name;
	
	/** Processor index */
	public int idx;
	
	/** The assembly */
	public Assembly asm;
	
	/** The shared memory */
	public SharedMem sm;
		
	/** FPE configuration */
	public SPUConfig conf;
	
	/** The help variables for FIFO synchronisation */
	// The increments of lines when NOPs are inserted */
	public int inc = 0;
	
	public boolean isIOCore = false;
	
	public SSP ssp;
	
	// Used for fire function definition generation phase. The encountered actor classes
	// are stored in this temporary variable.
	public LinkedList<String> generatedActorClass = new LinkedList<String>();
}
