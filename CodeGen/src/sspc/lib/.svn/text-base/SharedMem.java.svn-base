package sspc.lib;

import java.util.Vector;

import sspc.softgen.SWGenUtils;

/** Shared Memory
 *  @author Peng Wang
 * 
 *
 */
public class SharedMem {
	public SharedMem(SPU fpe) {
		this.fpe = fpe;		
	};

	/**
	 * Return formatted shared memory initialisation data.
	 * @return
	 */
	public String generateSmInitData() {
		if (actualSize == 0) return "";
		
		int dataWidth = fpe.conf.CoreDataWidth();
		StringBuffer code = new StringBuffer(); 		
		if (confSize == 32 || confSize == 64) {
			for (int j = 0; j < dataWidth; j++) {
				for (int i = 0; i < confSize; i++) {
					if (i < confSize - actualSize) {
						code.append("0");
					} else {	
						code.append(SWGenUtils.getCertainBit(
								fixedImms.get(confSize-i-1), j));
					}
				}
				code.append("\n");
			}
		} else {
			assert confSize > 64;
			
			// Using BRAM, then the initialization is like normal memory
			for (int j = 0; j < confSize; j++) {
				for (int i = 0; i < dataWidth; i++) {
					if (j < actualSize) {
						code.append(SWGenUtils.getCertainBit(
								fixedImms.get(j), dataWidth-i-1));
					} else {
						code.append("0");
					}
				}
				code.append("\n");
			}
		}

		return code.toString();
	}

	/* Immediate data */
	public Vector<Integer> fixedImms = new Vector<Integer>();
	
	/* Actual size of shared memories */
	public int actualSize = 0;
	/* Nearest power of 2 of actualSize */
	public int confSize = 0;
	
	public SPU fpe;
}
