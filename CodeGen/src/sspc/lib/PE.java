package sspc.lib;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Vector;

public class PE {
	public PE(int idx, SPU container) {
		this.idx = idx;
		_spu = container;
	}

	public String getName() {
		if (_spu.idx == -1)
			return _spu.name;
		return "FPE" + _spu.idx + "PE" + idx;
	}

	/**
	 * Get the FPE this PE resides in.
	 * 
	 * @return
	 */
	public SPU getSPU() {
		return _spu;
	}

	public List<Entity> getEntities() {
		return _entities;
	}

	public void addEntity(Entity entity) {
		if (_entities == null) {
			_entities = new LinkedList<Entity>();
		}
		_entities.add(entity);
	}

	/**
	 * Add a new output FIFO
	 * 
	 * @param fifo
	 */
	public void addOutputFifo(FIFO fifo) {
		outputFIFOs.add(fifo);
	}

	/**
	 * Add a new input FIFO
	 * 
	 * @param fifo
	 */
	public void addInputFifo(FIFO fifo) {
		inputFIFOs.add(fifo);
	}

	/**
	 * Get the specified input FIFO
	 * 
	 * @param idx
	 * @return
	 */
	public FIFO getInputFIFO(int idx) {
		return inputFIFOs.get(idx);
	}

	/**
	 * Get the specified output FIFO
	 * 
	 * @param idx
	 * @return
	 */
	public FIFO getOutputFIFO(int idx) {
		return outputFIFOs.get(idx);
	}

	/**
	 * Inquiry if input FIFO connection between current PE and the source PE
	 * exists.
	 * 
	 * @srcPE The source PE
	 */
	public boolean hasInputFIFOFrom(PE srcPE) {
		boolean has = false;
		for (FIFO f : inputFIFOs) {
			if (srcPE.equals(f.srcPE)) {
				has = true;
				break;
			}
		}
		return has;
	}

	/**
	 * Return the number of FIFOs between current PE and the source PE. 
	 * 
	 * @srcPE The source PE
	 */
	public int numOfInputFIFOsFrom(PE srcPE) {
		int cnt = 0;
		for (FIFO f : inputFIFOs) {
			if (srcPE.equals(f.srcPE)) {
				cnt++;				
			}
		}
		return cnt;
	}

	/**
	 * Get the FIFO connected with the specified PE. Only return the first FIFO
	 * found.
	 * 
	 * @param srcPE
	 * @return
	 */
	public FIFO getInputFIFOFrom(PE srcPE) {
		FIFO inFIFO = null;
		for (FIFO f : inputFIFOs) {
			if (srcPE.equals(f.srcPE)) {
				inFIFO = f;
				break;
			}
		}
		return inFIFO;
	}
	
	/**
	 * Get the FIFO connected with the specified PE. Return the nth (starting
	 * from 0) FIFO found.
	 * 
	 * @param srcPE
	 * @param n
	 *            The
	 * @return
	 */
	public FIFO getInputFIFOFrom(PE srcPE, int n) {
		FIFO inFIFO = null;
		int cnt = 0;
		for (FIFO f : inputFIFOs) {
			if (srcPE.equals(f.srcPE)) {
				if (cnt == n) {
					inFIFO = f;
					break;
				}
				cnt++;
			}
		}
		return inFIFO;
	}

	/**
	 * Get the channel number in the source PE side corresponding to sink
	 * channel number.
	 * 
	 * @param sinkChNo
	 * @return
	 */
	public int getWriteChNo(int readChNo) {
		FIFO f = inputFIFOs.get(readChNo);
		return f.srcPE.outputFIFOs.indexOf(f);
	}

	/**
	 * Return the next entity after the specified entity in the entity list.
	 * @param ent
	 * @return
	 */
	public Entity next(Entity ent) {
		return _entities.get(_entities.indexOf(ent)+1);
	}
	
	/**
	 * Return true is this PE is actually SOURCE
	 * 
	 * @return
	 */
	public boolean isIOPE() {
		return _spu.isIOCore;
	}

	///////////////////////////////////////////////////////////////////
	//                       public variables                        //

	/** Input FIFOs */
	public Vector<FIFO> inputFIFOs = new Vector<FIFO>();
	
	/** Output FIFOs */
	public Vector<FIFO> outputFIFOs = new Vector<FIFO>();	

	/** C code */
	public String cCode = new String();
	
	/** Fire function code */
	public String fireFuncCode = new String("");
	
	/**
	 * CodeGen unit. Because the CGUnit creation is not done in continuous way,
	 * but created in the process of iterating globalSched, so this variable is
	 * used for such purpose.
	 */
	public LinkedList<Entity> CGUnit = new LinkedList<Entity>();
	/**
	 * Used during buildCGUnits() to count how many actors have been processed.
	 */
	public int entityCounter = 0;

	/** Assembly */
	public Assembly asm;

	/** List of parameters which are constant port type */
	public List<Double> cpParas = new LinkedList<Double>();
	public RF rf;
	/** The <memory, parameter> map */
	public Map<Integer, Double> memParaMap = new HashMap<Integer, Double>();

	/** The index of the PE inside an FPE */
	public int idx;

	///////////////////////////////////////////////////////////////////
	//                       private variables                       //

	private List<Entity> _entities = new LinkedList<Entity>();

	private SPU _spu;
}
