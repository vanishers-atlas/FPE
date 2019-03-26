package sspc.lib;

import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Vector;

public class FIFO {
	public FIFO(PE src, PE sink) {
		srcPE = src;
		sinkPEs.add(sink);				
	}
	
	public FIFO() {
		
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	public void put(Token t) {
		_store.add(t);		
	}
	
	public Token get() {
		return _store.remove(0);
	}
	
	/**
	 * Inquiry whether a token is in FIFO
	 * @param t
	 * @return
	 */
	public boolean contains(Token t) {
		return _store.contains(t);
	}
	
	/**
	 * Return the index of the enquired token. Return -1 when the token is not
	 * found.
	 * @param t
	 * @return
	 */
	public int idxOf(Token t) {
		return _store.indexOf(t);
	}
	
	/**
	 * Get the first token without remove it from FIFO 
	 * @return
	 */
	public Token peek() {
		return _store.get(0);
	}
	
	/**
	 * Get the number of tokens
	 * @return
	 */
	public int numOfTokens() {
		return _store.size();
	}
	
	/**
	 * Calculate the minimum size of FIFO from reads and writes.
	 * 
	 * Current FIFO synchronisation can promise the reads and writes are in
	 * order, no sorting is required.
	 */
	public void calDepth(boolean skip) {
		if (isExInFIFO) {
			// If there is no iocore, the depth of external FIFOs are just set as 8 now. 
			_depth = (_depth==0)? 8 : _depth;
			return;
		}
		
		if (isExOutFIFO) {
			_depth = (_depth==0)? 8 : _depth;
			return;
		}
		
		if (skip) {
			_depth = (_depth==0)? 32: _depth;
			return;
		}
		
		if (reads.isEmpty() || writes.isEmpty())
			throw new RuntimeException("Reads and writes are empty");
		
		if (reads.size() != writes.size())
			throw new RuntimeException("Reads and writes sizes are different");
		
		int size = 0;
		int maxSize = 0;
		
		// This is to fix bug when sharing buffer. The order needs to be sorted.
		Collections.sort(reads);
		Collections.sort(writes);
		
		// The last read must happen after last write, so here iterating reads.
		for (int read : reads) {
			size --;
			if (!writes.isEmpty()) {
				Iterator<Integer> it = writes.iterator();
				
				// Find all writes before or on read
				while(it.hasNext()) {
					int write = it.next();
				
					if (write > read) {
						break;
					} else {
						it.remove();
						size ++;
						if (write < read) {
							maxSize = (size+1 > maxSize)? size+1 : maxSize;
						}
					}
				}
			}
		}
		assert size == 0;
		
		_depth = maxSize;
	}
	
	/**
	 * Retrieve the maximum space required
	 */
	public int getDepth() {
		if (_depth == 0) {
			throw new RuntimeException("Depth has not been calculated, first call calDepth()");
		}
		return _depth;
	}
	
	public void setExInFIFODepth(int depth) {
		if (!isExInFIFO) {
			throw new RuntimeException("Not a External Input FIFO!");
		} else {
			_depth = depth;
		}
	}
	
	public void setExOutFIFODepth(int depth) {
		if (!isExOutFIFO) {
			throw new RuntimeException("Not a External Output FIFO!");
		} else {
			_depth = depth;
		}
	}
	/** 
	 * Print FIFO name with the following convention. 
	 * FPExPEx__FPEy0PEy0_FPEy1PEy1_FPEy2PEy2(_IDXz)
	 * where x is source PE; y0,y1,y2 are sink PEs; z is index when there are
	 * more than one FIFOs between two PEs. 
	 * @return
	 */
	public String getName() {
		// TODO: Finish it!
		String name = new String();
		name = srcPE.getName()+"_to";
		for (PE sinkPE : sinkPEs) {
			name += "_" + sinkPE.getName();
		}
		if (localIdx > 0) {
			name += "_" + localIdx;
		}
		return name;
	}
	
	/**
	 * Get read index in the specified PE. Return -1 when no such FIFO exists
	 * in specified PE.
	 * @param sinkPE
	 * @return
	 */
	public int getReadIdxIn(PE sinkPE) {
		int i = sinkPE.inputFIFOs.indexOf(this);
		if (i == -1)
			throw new RuntimeException ("Can not get the index of the FIFO in inputFIFOs of the specified PE");
		return i;
	}
	
	/**
	 * Get read index in the srcPE. Return -1 when no such FIFO exists
	 * in PE.
	 * @return
	 */
	public int getWriteIdx() {
		int idx = srcPE.outputFIFOs.indexOf(this);
		if (idx == -1)
			throw new RuntimeException(
					"Found inconsistency: this FIFO does not exist in srcPE!");
		return idx;
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         public variables                  ////
	
	/** The connected PEs */
	public PE srcPE;
	
	/** A FIFO can be connected to multi-sinkPEs, then it is a shared FIFO */
	public LinkedList<PE> sinkPEs = new LinkedList<PE>();
	
	// This is used for sharing FIFO. If FIFOs are shared, the PUT instructions
	// will change the write channel No.
	public LinkedList<AsmInstr> putInsts = new LinkedList<AsmInstr>();
	
	/** Connected input actor ports. */
	public LinkedList<Port> inPorts = new LinkedList<Port>();
	
	/** Connected output actor ports. */
	public LinkedList<Port> outPorts = new LinkedList<Port>();		
	
	/** The global index of this FIFO in entire SSP */
	public int globalIdx;
	
	/** The local index to indicate the index in FIFOs between two PEs. Usually
	 *  it is 0, and it is 1 or above when there are more FIFOs between the
	 *  same two PEs.
	 */
	public int localIdx = 0;
	
	/** List to record FIFO reads and writes. In the list, the cycle the read
	 * or write occurs is recorded. 
	 */
	public List<Integer> reads = new LinkedList<Integer>();
	public List<Integer> writes = new LinkedList<Integer>();
	
	/** Flag whether it is an external input FIFO*/
	public boolean isExInFIFO = false;
	
	/** Flag whether it is an external output FIFO */
	public boolean isExOutFIFO = false;
    ///////////////////////////////////////////////////////////////////
    ////                         private variables                 ////
	
	private List<Token> _store = new LinkedList<Token>();
	
	// For conflict free FIFO allocation. Store the read sequence.
	public Vector<Token> readSeq = new Vector<Token>();
	
	/** The maximum FIFO space needed in an iteration */
	private int _depth = 0;
}
