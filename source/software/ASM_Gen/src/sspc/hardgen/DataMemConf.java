package sspc.hardgen;

import java.util.Map;

import sspc.lib.SPU;
import sspc.lib.SPUConfig;
import sspc.lib.PE;
import sspc.lib.SSP;
import sspc.lib.SPUConfig.ALUTYPE;
import sspc.softgen.SWGenUtils;

public class DataMemConf {
	public DataMemConf(SSP ssp) {
		this.ssp = ssp;
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	
	public void generateMIF() {
		for (SPU fpe : ssp.spus) {		
			if (!fpe.conf.dmEn) continue;			
			
			for (PE pe : fpe.PEs) {								
				Map<Integer, Double> map = pe.memParaMap;
				
				if (map.isEmpty()) {
					SWGenUtils.writeToFile("out//DMInit//dm_init"+pe.getName()+".mif", "");
					continue;
				}
				
				fpe.conf.dmInitEn = true;
				String code = _genInitData(fpe.conf, map);
				// Write out
				SWGenUtils.writeToFile("out//DMInit//dm_init"+pe.getName()+".mif", code);
			}
		}
	}
	
	///////////////////////////////////////////////////////////////////
	////                         private methods                   ////
	
	/**
	 * Return formatted data memory initialisation data.
	 * When using LUT for memory, initialisation has the format as: 
	 * bit0(datan, datan-1, ..., data0)
	 * bit1(datan, datan-1, ..., data0)
	 * ...
	 * bitN(datan, datan-1, ..., data0)
	 * 
	 * When using BRAM for memory, initialisation has the format as:
	 * data0(bitN, bitN-1, ..., bit0)
	 * data1(bitN, bitN-1, ..., bit0)
	 * ...
	 * datan(bitN, bitN-1, ..., bit0)
	 * @return
	 */
	private String _genInitData(SPUConfig conf, Map<Integer, Double> map) {
		StringBuffer code = new StringBuffer(); 		
		if (conf.dmSize <= 64) {
			int rowWidth = SWGenUtils.getNearestPowerOf2(conf.dmSize);
			for (int j = 0; j < conf.CoreDataWidth(); j++) {
				for (int i = 0; i < rowWidth; i++) {
					if (map.containsKey(rowWidth-i-1)) {
						double val = map.get(rowWidth-i-1);
						int fixval;
						if (conf.coreType == ALUTYPE.REAL16B1D || conf.coreType == ALUTYPE.REAL32B4D)
							fixval = SWGenUtils.float2fix(val, conf.CoreDataWidth(), ssp.conf.fracBits);
						else if (conf.coreType == ALUTYPE.CPLX16B4D)
							// When use complex datapath, the constant has already
							// been converted to fixed-point and packed.
							fixval = (int)val;
						else 
							throw new RuntimeException("ERROR: Unrecognized type.");
						code.append(SWGenUtils.getCertainBit(fixval, j));
					} else {
						code.append("0");
					}
				}
				code.append("\n");
			}
		} else {
			// Using BRAM, then the initialisation is like normal memory
			int confSize = conf.dmSize;

			if (confSize > 64) {
				if (conf.CoreDataWidth() == 16)
					confSize = (int) (Math.ceil(conf.dmSize/1024.0)*1024);
				else if (conf.CoreDataWidth() == 32)
					confSize = (int) (Math.ceil(conf.dmSize/512.0)*512);
			}
			
			for (int j = 0; j < confSize; j++) {
				double val = map.containsKey(j)? map.get(j) : 0;
				int fixval = SWGenUtils.float2fix(val, conf.CoreDataWidth(), ssp.conf.fracBits);
				for (int i = 0; i < conf.CoreDataWidth(); i++) {					
					code.append(SWGenUtils.getCertainBit(fixval, conf.CoreDataWidth()-i-1));
				}
				code.append("\n");
			}
		}

		return code.toString();
	}
	
	///////////////////////////////////////////////////////////////////
	////                         private variables                 ////
	
	private SSP ssp;
}
