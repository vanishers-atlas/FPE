package tools;

import java.io.File;
import java.io.IOException;

import sspc.hardgen.SharedMemConf;
import sspc.hardgen.ProgMemConf;
import sspc.lib.Assembly;
import sspc.lib.SPU;
import sspc.lib.SPUConfig;
import sspc.lib.SSP;
import sspc.softgen.Assembler;
import sspc.softgen.SWGenUtils;

public class RunAssembler {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		SSP ssp = new SSP();
		ssp.conf.init();
		ssp.conf.fracBits = 8;
		
		
		SWGenUtils.emptyDirectory("C://_Design_//PhD//Testcases//Assembler//out");
		
		SPU fpe = new SPU(ssp, "TestPE0");
		fpe.conf = new SPUConfig(ssp.conf);
		ssp.spus.add(fpe);
		ssp.conf.SPUConfs.add(fpe.conf);
		
		File dir = new File("C://_Design_//PhD//Testcases//Assembler");
		for (File child : dir.listFiles()) {
			String fname = child.getName();
			if (fname.contains(".s")) {
				Assembly asm = new Assembly(fpe, ssp);
				asm.parseFile("C://_Design_//PhD//Testcases//Assembler//"+fname);
				fpe.asm = asm;
				Assembler assler = new Assembler(fpe.asm, fpe.conf, ssp);
				assler.assemble();
				assler.printMachineCode("C://_Design_//PhD//Testcases//Assembler//out//" + fname.replace(".s", ".bin"));
			}
		}
		
		// Configure program memory
		ProgMemConf pmc = new ProgMemConf(ssp);
		pmc.generateMIF("C://_Design_//PhD//Testcases//Assembler//out//pm_init");
		pmc.fillInSSPConfig();
		System.out.println("Fininshed program memory configuration.");
		
		// Configure shared memory
		SharedMemConf imc = new SharedMemConf(ssp);
		imc.generateMIF("C://_Design_//PhD//Testcases//Assembler//out//imm_init");
		imc.fillInSSPConfig();
		System.out.println("Fininshed shared memory configuration.");
	}

}
