package sspc.lib;

import java.util.Vector;

import sspc.softgen.SWGenUtils;

public class RF {
//	public static void main(String[] args) {
//		RF rf = new  RF(new SPUConfig());
//		String code = rf.generateRFInitData();
//		SWGenUtils.writeToFile("out//RFInit//rf_init0.mif", code);
//	}
	
	
	public RF(SPUConfig conf) {
		_conf = conf;
	}
	
	// The initialization must be called after SPU configuration is set for each application. 
	public void init() {
		int size = _conf.regSize;
		int datawidth = _conf.CoreDataWidth();
		assert datawidth == 16 || datawidth == 32;
		assert size == 32 || size == 64;
		for (int i=0; i<size; i++) {			
			if (i == size-1)
				rfdata.add(SWGenUtils.intToBinary(1<<_conf.sspconf.fracBits, datawidth));
			else
				rfdata.add(SWGenUtils.intToBinary(0, datawidth));
		}
	}
	
	public void setValue(int idx, int val) {
		if (idx >= _conf.regSize)
			throw new RuntimeException("Wrong SETREGVALUE(_ID)");
		rfdata.set(idx, SWGenUtils.intToBinary(val, _conf.CoreDataWidth()));
	}
	
	public String generateRFInitData() {
		int dataWidth = _conf.CoreDataWidth();
		StringBuffer code = new StringBuffer(); 
		if (_conf.regSize == 32) {
			for (int j = 0; j < dataWidth/2; j++) {
				for (int i = 0; i < _conf.regSize; i++) {
					code.append(rfdata.get(_conf.regSize-i-1).charAt(dataWidth-2*j-2));
					code.append(rfdata.get(_conf.regSize-i-1).charAt(dataWidth-2*j-1));
				}
				code.append("\n");
			}
		} else {
			for (int j = 0; j < dataWidth; j++) {
				for (int i = 0; i < _conf.regSize; i++) {
					code.append(rfdata.get(_conf.regSize-i-1).charAt(dataWidth-j-1));
				}
				code.append("\n");
			}
		}
		return code.toString();
	}
	
	public Vector<String> rfdata = new Vector<String>();
	private SPUConfig _conf;
}
