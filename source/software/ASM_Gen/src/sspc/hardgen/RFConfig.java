package sspc.hardgen;

import sspc.lib.PE;
import sspc.lib.SPU;
import sspc.lib.SSP;
import sspc.softgen.SWGenUtils;

public class RFConfig {
	public RFConfig(SSP ssp) {
		_ssp = ssp;
	}
	/**
	 * Generate MIF file for each program memory
	 */
	public void generateMIF(String outFileName) {	
		for (SPU spu : _ssp.spus) {
			for (PE pe : spu.PEs) {
				SWGenUtils.writeToFile(outFileName+pe.getName()+".mif", pe.rf.generateRFInitData());
			}
		}
	}
	
	private SSP _ssp;
}
