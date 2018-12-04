package sspc.hardgen;

import sspc.lib.SPU;
import sspc.lib.SharedMem;
import sspc.lib.SSP;
import sspc.softgen.SWGenUtils;
import sspc.softgen.SoftwareGen.Mode;

/** Shared Memory Configuration
 *  @author Peng Wang
 * 
 *
 */
public class SharedMemConf {
//	public static void main(String[] args) 
//			throws NumberFormatException, IOException {
//		SSPConfig conf = new SSPConfig();
//		ImmMemConfig imc = new ImmMemConfig(128, 16);
//		imc.generateMIF();
//		imc.fillInSSPConfig(conf);
//	}

	public SharedMemConf(SSP ssp) {
		_ssp = ssp;
	}

	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	/**
	 * Initialise IM in each FPE
	 */
	public void init() {
		for (SPU spu : _ssp.spus) {
			SharedMem curIM = spu.sm;
			curIM.actualSize = curIM.fixedImms.size();			
			if (curIM.actualSize > 0 && curIM.actualSize <= 32)
				curIM.confSize = 32;
			else if (curIM.actualSize > 32 && curIM.actualSize <= 64) {
				curIM.confSize = 64;
			} else {
				if (spu.conf.CoreDataWidth() == 16)
					curIM.confSize = (int) (Math.ceil(curIM.actualSize/1024.0)*1024);
				else if (spu.conf.CoreDataWidth() == 32)
					curIM.confSize = (int) (Math.ceil(curIM.actualSize/512.0)*512);
			}
		}
	}
	
	/** 
	 * Generate MIF file
	 */
	public void generateMIF(String outFileName) {
		init();
		
		for (SPU fpe : _ssp.spus) {
			SharedMem curIM = fpe.sm;			
			// Write out
			SWGenUtils.writeToFile(outFileName+fpe.idx+".mif", curIM.generateSmInitData());
		}
	}
	
	/**
	 * Fill in shared memory fields of SSPConfig
	 * @param conf
	 */
	public void fillInSSPConfig() {
		for (SPU fpe : _ssp.spus) {	
			SharedMem curIM = fpe.sm;
			if (curIM.confSize > 0) {
				fpe.conf.smEn = true;
				if (curIM.confSize <= 64)
					fpe.conf.smSize = curIM.confSize;
				else
					fpe.conf.smSize = curIM.actualSize;
				fpe.conf.smWidth = SWGenUtils.getAddressWidth(fpe.conf.smSize);
				
				// Compute smOffsetWidth
				if (fpe.conf.smWidth > fpe.conf.regWidth) {
					if (fpe.conf.regWidth == 5 && fpe.conf.smWidth > 8) {
						fpe.conf.smOffsetWidth = 8;
					} else if (fpe.conf.regWidth == 6 && fpe.conf.smWidth > 6) {
						fpe.conf.smOffsetWidth = 6;
					}
				} else {
					fpe.conf.smOffsetWidth = fpe.conf.smWidth;
				}
			}
		}
		// TODO: Delete this when #0, #1 to ZERO and ONE is possible.
		if (_ssp.sg.mode == Mode.FFT) {
			if (_ssp.sg.fft.bSIMD)
				_ssp.getSPU(0).conf.smEn = false;
		}
	}
	
	///////////////////////////////////////////////////////////////////
	////                         private methods                   ////
	
	
	///////////////////////////////////////////////////////////////////
	////                         public variables                  ////

	///////////////////////////////////////////////////////////////////
	////                         private variables                   ////
	private SSP _ssp;
}
