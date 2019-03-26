package sspc;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import org.w3c.dom.Document;

import sspc.hardgen.DataMemConf;
import sspc.hardgen.RFConfig;
import sspc.hardgen.SharedMemConf;
import sspc.hardgen.ProgMemConf;
import sspc.hardgen.SSPGen;
import sspc.lib.Assembly;
import sspc.lib.FIFO;
import sspc.lib.SPU;
import sspc.lib.SPUConfig.ALUTYPE;
import sspc.lib.SSP;
import sspc.lib.dsp.FFT;
import sspc.lib.dsp.MatrixMult;
import sspc.lib.dsp.MotionEst;
import sspc.lib.dsp.MotionEstH264;
import sspc.lib.dsp.SobelEdge;
import sspc.softgen.Assembler;
import sspc.softgen.FIFOSync;
import sspc.softgen.SoftwareGen;
import sspc.softgen.SoftwareGen.Mode;
import sspc.softgen.SoftwareGen.FIFOAllocScheme;

public class SSPBackend {
	// General configuration parameters
	private int fracBits = 0;
	private String graphName = new String("");
	private Document graphInMoML;
	private boolean bIntl = false;
	private int intlSize = 1;
	private FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
	private ALUTYPE coreType = ALUTYPE.REAL16B1D;

	/** Application specific configuration parameters **/
	private Mode custMode = Mode.NONE;
	private FFT _fft;
	private MatrixMult _matrixMult; 
	private MotionEst _motionEst; 
	private MotionEstH264 _motionEstH264; 
	private SobelEdge _sobelEdge;
	
	/**
	 * Top level initialisation. These parameters may be decided by compiler 
	 * later. But now they are set by hand.
	 */
	public void init(int fracBits, String graphName, boolean bInterleave, 
			int interlSize, FIFOAllocScheme bufAllocScheme, 
			ALUTYPE coreType) {
		this.fracBits = fracBits;
		this.graphName = graphName;
		this.bIntl = bInterleave;
		this.intlSize = interlSize;
		this.bufAllocScheme = bufAllocScheme;
		this.coreType = coreType;
	}
	
	/** Default initialisation.
	 * 
	 * @param fft
	 */
	public void init(int fracBits, Document graphName) {
		this.fracBits = fracBits;
		this.graphInMoML = graphName;
	}
	
	public void initFFT(FFT fft) {
		_fft = fft;
		custMode = Mode.FFT;		
	}
	
	public void initMatrixMult(MatrixMult matrixMult) {
		_matrixMult = matrixMult;
		custMode = Mode.MATRIXMULT;
	}
	
	public void initMotionEst(MotionEst motionEst) {
		_motionEst = motionEst;
		custMode = Mode.MOTIONEST;
	}
	
	public void initMotionEstH264(MotionEstH264 motionEst) {
		_motionEstH264 = motionEst;
		custMode = Mode.MOTIONESTH264;
	}
	
	public void initSobelEdge(SobelEdge sobelEdge) {
		_sobelEdge = sobelEdge;
		custMode = Mode.SOBELEDGE;
	}

	public void run() throws IOException {
		// ----------------------------------------------------------------
		// Software Synthesis Part
		// ----------------------------------------------------------------		
		SSP ssp = new SSP();
		ssp.conf.fracBits = fracBits;
		ssp.conf.init();
		
		// Generate C Code
		System.out.println("C code generation starts ...");
		double start = System.currentTimeMillis();
		
		// Document object passing is used for tool integration
		SoftwareGen sg = null;
		if (graphInMoML == null)
			sg = new SoftwareGen(ssp, new File(graphName));
		else
			sg = new SoftwareGen(ssp, graphInMoML);
		
		sg.setInterleave(bIntl, intlSize);
		sg.setBufAllocScheme(bufAllocScheme);
		
		if (custMode == Mode.FFT)
			sg.initFFT(_fft);
		else if (custMode == Mode.MATRIXMULT)
			sg.initMatrixMult(_matrixMult);
		else if (custMode == Mode.MOTIONEST)
			sg.initMotionEst(_motionEst);
		else if (custMode == Mode.MOTIONESTH264) {
			sg.initMotionEstH264(_motionEstH264);
			ssp.skipFIFOSync = true;
		}
		else if (custMode == Mode.SOBELEDGE)
			sg.initSobelEdge(_sobelEdge);
		
		sg.init(coreType);
		sg.generateCode();
		
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: C code generated!");
		
		// After LLVM compiler compiled the C codes, press enter to continue.
		System.out.println("Make sure assembly has been generated! " +
				"Press enter to continue");
		Scanner keyboard = new Scanner(System.in);
		keyboard.nextLine();
				
		// Parse assembly file generated from LLVM
		for (SPU spu : ssp.spus) {
			Assembly asm = new Assembly(spu, ssp);
			// Set pass enable/disable
			_setPassOnOff(sg, asm);
			
			asm.parseFile("in//asm//FPE"+spu.idx+".s");
//			asm.setParameters();
			asm.immToSMPass();
			asm.dmFoldingPass();
			asm.putFoldingPass();
			asm.insertDMBaseSetPass();
			asm.setFlexPortsPass();
			asm.removeUnneededNOPsPass();
			asm.fwdConvertPass();
//			asm.removeUnneededNOPsPass();
			spu.asm = asm;
		}
		
		// Make sure call this before FIFO sync
		ssp.parseCycleInfo();
		
		System.out.println("FIFO synchronization starts ...");
		start = System.currentTimeMillis();
		FIFOSync sync = new FIFOSync(ssp);
		sync.syncFIFO();
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: FIFO synchronization finished!");
		
		// RPT NOPs
		for (SPU spu : ssp.spus) {
			Assembly asm = spu.asm;
			asm.rptNOPsPass();
		}
		
		// RPT parsing
		for (SPU spu : ssp.spus) {
			Assembly asm = spu.asm;
			asm.rptParsingPass();
		}
		
		// Write out final assembly
		for (SPU spu : ssp.spus) {
			Assembly curAsm = spu.asm;
			curAsm.populateInstTypes();
			curAsm.printAsm("out//SyncedAsm//FPE" + spu.idx + "_synced.s");
		}				
		
		if (!ssp.conf.noIOCore) {
			Assembly asm = new Assembly(ssp.ioCore, ssp);
			ssp.ioCore.asm = asm;
			asm.parseFile("in//asm//IOCore.s");
			asm.rptParsingPass();
			asm.populateInstTypes();			
		}
		
		// ----------------------------------------------------------------
		// Hardware Synthesis Part
		// ----------------------------------------------------------------				
		if (!ssp.skipFIFOSync) {
			ssp.genFIFOWritesAndReadsInfo();
			
			// optional sharing FIFO
			ssp.shareFIFO();
			
			// Calculate FIFO size
			for (FIFO fifo : ssp.fifos) {
				fifo.calDepth(ssp.skipFIFOSync);
			}
		} else {
			// Set it to default value and prompts user to set manually.
			for (FIFO fifo : ssp.fifos) {
				fifo.calDepth(ssp.skipFIFOSync);
			}
			System.out.println("WARNING: Please sync communications and set FIFO sizes mannually!");
		}
		
		// Print out instruction encoding		
		ssp.printInstEncoding("out//m_word_config.vhd");
		
		// Assembling
		for (SPU spu : ssp.spus) {
			Assembler assler = new Assembler(spu.asm, spu.conf, ssp);
			assler.assemble();
			assler.printMachineCode("out//binary//FPE" + spu.idx + ".bin");
		}
		
		if (!ssp.conf.noIOCore) {
			Assembler assler = new Assembler(ssp.ioCore.asm, ssp.ioCore.conf, ssp);
			assler.assemble();
			assler.printMachineCode("out//binary//iocore.bin");
		}
		
		// Configure program memory
		ProgMemConf pmc = new ProgMemConf(ssp);
		pmc.generateMIF("out//PMInit//");
		pmc.fillInSSPConfig();
		System.out.println("Fininshed PM configuration.");
		
		// Configure rf
		RFConfig rfc = new RFConfig(ssp);
		rfc.generateMIF("out//RFInit//rf_init");
		System.out.println("Fininshed RF configuration.");
		
		// Configure shared memory
		SharedMemConf smc = new SharedMemConf(ssp);
		smc.generateMIF("out//IMMInit//imm_init");
		smc.fillInSSPConfig();
		System.out.println("Fininshed SM configuration.");
		
		// Configure data memory if constant port is used
		DataMemConf dmc = new DataMemConf(ssp);
		dmc.generateMIF();
		System.out.println("Fininshed DM configuration.");
		
		// Generate SSP top module
		SSPGen topGen = new SSPGen(ssp);
		topGen.generate();		
		System.out.println("Fininshed SSP top module generation.");
		
		// Generate System, connect spus and iocore
		if (!ssp.conf.noIOCore) {
			topGen.generateSystem();
			System.out.println("Fininshed SSP system generation.");
		}
		
		System.out.println("All finished!");
	}

	private void _setPassOnOff(SoftwareGen sg, Assembly asm) {
		if (custMode == Mode.MOTIONESTH264) {
			asm.skipPUTFoldingPass = true;
			asm.skipRPTNopsPass = true;
			asm.skipInsertDMBaseSetPass = true;
			asm.skipDMFoldingPass = true;
			asm.skipRemoveUnneededNOPsPass = true;
			asm.skipFWDConvertPass = true;
			asm.skipIMMToSMPass = true;
		}
	}
}

