package tools;

import java.io.File;
import java.io.IOException;

import sspc.lib.Assembly;
import sspc.lib.SPU;
import sspc.lib.SPUConfig;
import sspc.lib.SSP;
public class PostCompilingProcessing {
	public static void main(String[] args) throws IOException {
		SSP ssp = new SSP();
		ssp.conf.init();
		
		SPU fpe = new SPU(ssp, "TestPE0");
		fpe.conf = new SPUConfig(ssp.conf);
				
//		for (int i=3; i<4; i++) {
//			Assembly asm = new Assembly(fpe, ssp);
//			asm.parseFile("C://Users//40055379//Desktop//test//asm//APED_enum"+i+"_OrderOptimised.s");
//			asm.removeUnneededNOPsPass();
//			asm.putfwdConvertPass();
//			asm.printAsm("C://Users//40055379//Desktop//test//out//APED_enum"+i+"_OrderOptimised.s");
//		}
//		Assembly asm = new Assembly(fpe, ssp);
//		asm.parseFile("C://Users//40055379//Desktop//test//test.s");
//		asm.removeUnneededNOPsPass();
//		asm.putfwdConvertPass();
//		asm.printAsm("C://Users//40055379//Desktop//test//test_out.s");
		File dir = new File("C://Users//40055379//Desktop//test");
		_compile(ssp, fpe, dir);
	}
	
	public PostCompilingProcessing() {}
	
	private static void _compile(SSP ssp, SPU fpe, File fl) throws IOException {		
		for (File child : fl.listFiles()) {
			if (child.isFile()) {
				String fname = child.getName();
				if (fname.contains(".s")) {
					Assembly asm = new Assembly(fpe, ssp);
					asm.parseFile(child.getAbsolutePath());
//					asm.dmFoldingPass();
	//				asm.putFoldingPass();
//					asm.insertDMBaseSetPass();
//					asm.removeUnneededNOPsPass();
//					asm.fwdConvertPass();
					File out = new File(child.getAbsolutePath().replace(".s", "_parsed.s"));
					asm.printAsm(out.getAbsolutePath());
				}
			}  else if (child.isDirectory()) {
				_compile(ssp, fpe, child);
			}			
		}
	}
}
