package sspc.lib;

public class Transition {
	public Transition(Port s, Port si, FIFO f) {
		srcPort = s;
		sinkPort = si;
		fifo = f;
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
		
	/**
	 * Get sink FPE. 
	 * @return
	 */
	public SPU getSinkFPE() {
		// Note that fifo may connect to multi-sinkPEs, so here we use sinkPort
		// to get the sinkFPE.
		return sinkPort.getFPE();
	}
	
	/**
	 * Get sink PE. 
	 * @return
	 */
	public PE getSinkPE() {
		// Note that fifo may connect to multi-sinkPEs, so here we use sinkPort
		// to get the sinkPE.
		return sinkPort.getPE();
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public variables                  ////
	
	/** Source port of this transition */
	public Port srcPort;
	
	/** Sink port of this transition */
	public Port sinkPort;
	
	/** The associated FIFO in which this transition occurs */
	public FIFO fifo;
}
