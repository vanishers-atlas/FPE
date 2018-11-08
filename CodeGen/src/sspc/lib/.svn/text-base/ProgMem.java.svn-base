package sspc.lib;

import java.util.Iterator;
import java.util.Vector;

/** Progediate Memory Configuration
 *  @author Peng Wang
 * 
 *
 */
public class ProgMem {
	public ProgMem(int width, SPUConfig conf) {
		_dataWidth = width;
		_conf = conf;
	};
	
	/**
	 * Parse the assembly. Fill the machine code into the program list.
	 * @param asm The assembly object
	 */
	public void parseAsm(Assembly asm) {
		Iterator<AsmInstr> iter = asm.getInstructions().iterator();
		while (iter.hasNext()) {
			progs.add(iter.next().instrBin);
		}
		
		actualSize = progs.size();
		if (actualSize > 0 && actualSize <= 32)
			confSize = 32;
		else if (actualSize > 32 && actualSize <= 64) {
			confSize = 64;
		} else {
			if (_dataWidth == 16)
				confSize = (int) (Math.ceil(actualSize/1024.0)*1024);
			else if (_dataWidth == 32)
				confSize = (int) (Math.ceil(actualSize/512.0)*512);
			else if (_dataWidth == 8)
				confSize = (int) (Math.ceil(actualSize/2048.0)*2048);
		}
	}
	
	/**
	 * Generate MIF data. Data formats are different for LUT memory and Block 
	 * memory. 
	 * @return
	 */
	public String generateProgInitData() {
		if (confSize == 0)
			return "";
		
		StringBuffer code = new StringBuffer(); 		
		if (confSize == 32 || confSize == 64) {
			for (int j = 0; j < _dataWidth; j++) {
				for (int i = 0; i < confSize; i++) {
					if (i < confSize - actualSize) {
						code.append("0");
					} else {
						code.append(progs.get(confSize-i-1).charAt(_dataWidth-j-1));
					}
				}
				code.append("\n");
			}
		} else if (!_conf.useBRAMForLargePM && actualSize > 64) {
			// LUT RAM built with blocks
			int blockNum = (int) Math.ceil(actualSize/64.0);
			for (int k=0; k<blockNum; k++) {
				for (int j = 0; j < _dataWidth; j++) {
					for (int i = 0; i < 64; i++) {
						if (i < 64*(k+1)-actualSize) {
							code.append("0");
						} else {
							code.append(progs.get(64*(k+1)-i-1).charAt(_dataWidth-j-1));
						}
					}
					code.append("\n");
				}
			}
		} else {
			assert confSize > 64;
			
			// Using BRAM, then the initialisation is like normal memory
			for (int j = 0; j < confSize; j++) {
				for (int i = 0; i < _dataWidth; i++) {
					if (j < actualSize) {
						code.append(progs.get(j).charAt(i));
					} else {
						code.append("0");
					}
				}
				code.append("\n");
			}
		}

		return code.toString();
	}

	/* Binary instructions */
	Vector<String> progs = new Vector<String>();
	
	/* Actual size of program memories */
	public int actualSize = 0;
	/* Nearest power of 2 of actualSize */
	public int confSize = 0;

	private int _dataWidth;
	private SPUConfig _conf;
}
