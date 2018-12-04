package sspc.hardgen;

import java.util.Vector;

import sspc.lib.SPU;
import sspc.lib.SPUConfig;
import sspc.lib.ProgMem;
import sspc.lib.SSP;
import sspc.softgen.SWGenUtils;

/** Progediate Memory Configuration
 *  @author Peng Wang
 * 
 *
 */
public class ProgMemConf {
	public ProgMemConf(SSP ssp) {
		_SPUNum = ssp.spus.size();
		_ssp = ssp;
	}

	/**
	 * Generate MIF file for each program memory
	 */
	public void generateMIF(String outFileName) {
		_parseProgMems();
	
		for (int i=0; i<_SPUNum; i++) {
			ProgMem curPM = progMems.get(i);
			
			// Write out
			SWGenUtils.writeToFile(outFileName+"pm_init"+i+".mif", 
					curPM.generateProgInitData());
		}
		
		if (!_ssp.conf.noIOCore) {
			ProgMem iocorePM = progMems.lastElement();
			SWGenUtils.writeToFile(outFileName+"iocore.mif", iocorePM.generateProgInitData());
		}
	}

	public void fillInSSPConfig() {
		for (int i=0; i<progMems.size(); i++) {		
			ProgMem curPM = progMems.get(i);
			SPUConfig conf;
			if (_ssp.conf.noIOCore) {
				conf = _ssp.conf.SPUConfs.get(i);
			} else {
				if (i != progMems.size()-1)
					conf = _ssp.conf.SPUConfs.get(i);
				else
					conf = _ssp.ioCore.conf;
			}
			
			if (curPM.confSize <= 64)
				conf.pmSize = curPM.confSize;
			else
				conf.pmSize = curPM.actualSize;
			conf.pmWidth = SWGenUtils.getAddressWidth(conf.pmSize);
		}
	}

	/**
	 * Parse program memory from FPE assembly.
	 */
	private void _parseProgMems() {
		for (SPU spu : _ssp.spus) {
			ProgMem pm = new ProgMem(spu.conf.pmDataWidth, spu.conf);
			pm.parseAsm(spu.asm);
			progMems.add(pm);
		}
		
		if (!_ssp.conf.noIOCore) {
			ProgMem pm = new ProgMem(_ssp.ioCore.conf.pmDataWidth, _ssp.ioCore.conf);
			pm.parseAsm(_ssp.ioCore.asm);
			progMems.add(pm);
		}
	}

	private int _SPUNum;
	public Vector<ProgMem> progMems = new Vector<ProgMem>();
	private SSP _ssp;
}
