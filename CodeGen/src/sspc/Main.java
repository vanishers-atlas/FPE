package sspc;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;

import sspc.lib.SPUConfig.ALUTYPE;
import sspc.lib.dsp.*;
import sspc.lib.dsp.FFT.FFTType;
import sspc.lib.dsp.MatrixMult.MMType;
import sspc.lib.dsp.MotionEst.METype;
import sspc.lib.dsp.MotionEstH264.MEH264Type;
import sspc.lib.dsp.SobelEdge.SEType;
import sspc.softgen.*;
import sspc.softgen.SoftwareGen.FIFOAllocScheme;
import sspc.util.XMLUtilities;

public class Main {
	public static void main(String[] args) throws Exception  {
//		runFFT();
//		runMatrixMult();
//		runMotionEst();
//		runSobelEdge();
		runMotionEstH264();
//		File name = new File("P12_18/primitivefiles/FSD_44_16QAM_peng_part12.xml");
//		Document graphName = XMLUtilities.readXMLDocument(name);
//		
//		// Empty directories
//		SWGenUtils.emptyDirectory("out//C");
//		SWGenUtils.emptyDirectory("out//DMInit");
//		SWGenUtils.emptyDirectory("out//PMInit");
//		SWGenUtils.emptyDirectory("out//IMMInit");
//		SWGenUtils.emptyDirectory("out//RFInit");
//		SWGenUtils.emptyDirectory("out//SyncedAsm");
//		SWGenUtils.emptyDirectory("out//binary");
//		
//		SSPBackend backend = new SSPBackend();
//		backend.init(0, graphName);
//		backend.run();
		
	}
	
	public static void runSobelEdge() throws ParserConfigurationException, IOException {
		boolean bInterleave = false;
		ALUTYPE coreType = ALUTYPE.REAL16B1D;
		int fracBits = 0;
		int interlSize = 1;
		// actor number decides the number of PEs
		int actorNum = 3;
		SEType func = SEType.INTL3;
		String graphName = "SobelEdge.xml";
		FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
		
		System.out.println("Sobel Edge Detection graph generation starts ...");
		long start = System.currentTimeMillis();
		SobelEdge sobelEdge = new SobelEdge(actorNum, func);
		sobelEdge.graphGen(graphName);
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: Sobel Edge Detection graph generated!");
		
		// Empty directories
		SWGenUtils.emptyDirectory("out//C");
		SWGenUtils.emptyDirectory("out//DMInit");
		SWGenUtils.emptyDirectory("out//PMInit");
		SWGenUtils.emptyDirectory("out//IMMInit");
		SWGenUtils.emptyDirectory("out//RFInit");
		SWGenUtils.emptyDirectory("out//SyncedAsm");
		SWGenUtils.emptyDirectory("out//binary");

		SSPBackend backend = new SSPBackend();
		backend.initSobelEdge(sobelEdge);
		backend.init(fracBits, graphName, bInterleave, interlSize, bufAllocScheme, coreType);
		backend.run();
	}
	
	public static void runMotionEst() throws ParserConfigurationException, IOException {
		boolean bInterleave = false;
		ALUTYPE coreType = ALUTYPE.REAL16B1D;
		int fracBits = 0;
		int interlSize = 1;
		// actor number decides the number of PEs
		int actorNum = 1;
		METype func = METype.DUALDM_CA;
		String graphName = "MotionEst.xml";
		FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
		
		System.out.println("Motion Estimation graph generation starts ...");
		long start = System.currentTimeMillis();
		MotionEst motionEst = new MotionEst(actorNum, func);
		motionEst.graphGen(graphName);
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: Motion Estimation graph generated!");
		
		// Empty directories
		SWGenUtils.emptyDirectory("out//C");
		SWGenUtils.emptyDirectory("out//DMInit");
		SWGenUtils.emptyDirectory("out//PMInit");
		SWGenUtils.emptyDirectory("out//IMMInit");
		SWGenUtils.emptyDirectory("out//SyncedAsm");
		SWGenUtils.emptyDirectory("out//binary");

		SSPBackend backend = new SSPBackend();
		backend.initMotionEst(motionEst);
		backend.init(fracBits, graphName, bInterleave, interlSize, bufAllocScheme, coreType);
		backend.run();
	}
	
	public static void runMotionEstH264() throws ParserConfigurationException, IOException {
		boolean bInterleave = false;
		ALUTYPE coreType = ALUTYPE.REAL16B1D;
		int fracBits = 0;
		int interlSize = 1;
		MEH264Type func = MEH264Type.TWOBALANCED;
		String graphName = "MotionEstH264.xml";
		FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
		
		System.out.println("H.264 Motion Estimation graph generation starts ...");
		long start = System.currentTimeMillis();
		MotionEstH264 motionEst = new MotionEstH264(func);
		motionEst.graphGen(graphName);
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: Motion Estimation graph generated!");
		
		// Empty directories
		SWGenUtils.emptyDirectory("out//C");
		SWGenUtils.emptyDirectory("out//DMInit");
		SWGenUtils.emptyDirectory("out//PMInit");
		SWGenUtils.emptyDirectory("out//IMMInit");
		SWGenUtils.emptyDirectory("out//SyncedAsm");
		SWGenUtils.emptyDirectory("out//binary");

		SSPBackend backend = new SSPBackend();
		backend.initMotionEstH264(motionEst);
		backend.init(fracBits, graphName, bInterleave, interlSize, bufAllocScheme, coreType);
		backend.run();
	}
	
	public static void runMatrixMult() throws ParserConfigurationException, IOException {
		boolean bInterleave = false;
		ALUTYPE coreType;
		int fracBits = 0;
		int interlSize = 1;
		
		int peNum = 1;
		int blkNum = 32;
		MMType func = MMType.test;
		
		if (func == MMType.M1024B32W32 || func == MMType.test)
			coreType = ALUTYPE.REAL32B4D;
		else
			coreType = ALUTYPE.REAL16B1D;
		
		String graphName = "MatrixMult.xml";
		FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
		
		System.out.println("Matrix Multiplication graph generation starts ...");
		long start = System.currentTimeMillis();
		MatrixMult matrixMult = new MatrixMult(peNum, blkNum, func);
		matrixMult.graphGen(graphName);
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: Matrix Multiplication graph generated!");
		
		// Empty directories
		SWGenUtils.emptyDirectory("out//C");
		SWGenUtils.emptyDirectory("out//DMInit");
		SWGenUtils.emptyDirectory("out//PMInit");
		SWGenUtils.emptyDirectory("out//IMMInit");
		SWGenUtils.emptyDirectory("out//SyncedAsm");
		SWGenUtils.emptyDirectory("out//binary");

		SSPBackend backend = new SSPBackend();
		backend.initMatrixMult(matrixMult);
		backend.init(fracBits, graphName, bInterleave, interlSize, bufAllocScheme, coreType);
		backend.run();
	}
	
	
	public static void runFFT() throws ParserConfigurationException, IOException {
		/* FFT case study */
		boolean bInterleave = false;
		ALUTYPE coreType;
		int fracBits = 14;
		int interlSize = 5;
		String graphName = "FFT.xml";
		FIFOAllocScheme bufAllocScheme = FIFOAllocScheme.BASELINE;
		
		int FFTSize = 256;
		int FPENUM = 1;
		int STAGESPAN = 1;
		int WAYNUM = 1;		
		FFTType fftFireType;
		boolean bFFTSIMD = false;
		boolean bFFTShareCoesWhenPossible = false;
		
		// Real Datapath
		//   MIMD
		FPENUM = 8;
		bufAllocScheme = FIFOAllocScheme.BASELINE;
		bInterleave = true;
		coreType = ALUTYPE.REAL16B1D;
		fftFireType = FFTType.IL2_REAL_MIMD;
		interlSize = 2;
//		
//		//   SIMD
//		STAGESPAN = 1;
//		WAYNUM = 2;
//		bSIMD = true;
//		bufAllocScheme = FIFOAllocScheme.CONFLICTFREE;
//		bShareCoesWhenPossible = true;
//		bInterleave = true;
//		coreType = CORETYPE.REAL16B1D;
//		fftFireType = FFTFirefunctionType.IL2_REAL_SIMD;
//		interlSize = 2;
//		
//		// Complex Datapath
//		//   MIMD
//		FPENUM = 4;
//		bufAllocScheme = FIFOAllocScheme.BASELINE;
//		bInterleave = true;
//		coreType = ALUTYPE.CPLX16B4D;
//		fftFireType = FFTType.IL4_CPLX_MIMD;
//		interlSize = 4;
		
//		//   SIMD
//		STAGESPAN = 1;
//		WAYNUM = 2;
//		bFFTSIMD = true;
//		bFFTShareCoesWhenPossible = true;
//		bufAllocScheme = FIFOAllocScheme.CONFLICTFREE;
//		bInterleave = true;
//		coreType = ALUTYPE.CPLX16B4D;
//		fftFireType = FFTType.IL4_CPLX_SIMD;
//		interlSize = 4;
		
		
		System.out.println("FFT graph generation starts ...");
		long start = System.currentTimeMillis();
		FFT fft = (bFFTSIMD)? new FFT(FFTSize, STAGESPAN, WAYNUM) : new FFT(FFTSize, FPENUM);
		fft.init(fftFireType, bFFTShareCoesWhenPossible);
		fft.fftGraphGen(graphName);
		System.out.println((System.currentTimeMillis()-start)/1000F 
				+ "s: FFT graph generated!");
		
		// Empty directories
		SWGenUtils.emptyDirectory("out//C");
		SWGenUtils.emptyDirectory("out//DMInit");
		SWGenUtils.emptyDirectory("out//PMInit");
		SWGenUtils.emptyDirectory("out//IMMInit");
		SWGenUtils.emptyDirectory("out//SyncedAsm");
		SWGenUtils.emptyDirectory("out//binary");

		SSPBackend backend = new SSPBackend();
		backend.initFFT(fft);
		backend.init(fracBits, graphName, bInterleave, interlSize, bufAllocScheme, coreType);
		backend.run();
	}
}