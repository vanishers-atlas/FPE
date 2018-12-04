package sspc.softgen;

import java.io.IOException;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import sspc.lib.AsmInstr;
import sspc.lib.Assembly;
import sspc.lib.FIFO;
import sspc.lib.FIFOInstr;
import sspc.lib.RptedInst;
import sspc.lib.SPU;
import sspc.lib.PE;
import sspc.lib.SSP;
import sspc.lib.Transition;
import sspc.softgen.SoftwareGen.Mode;

public class FIFOSync {
	public FIFOSync(SSP ssp) {
		this.ssp = ssp;
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	
	/**
	 * Execute synchronisation. Note synchronisation should operate on all
	 * PEs instead of only PE0 in a FPE. This is necessary and refer to FFT 
	 * SIMD for examples.
	 * 
	 * During the synchronisation continues, the FIFO reads and writes are
	 * recorded, which are later used for calculating FIFO size.
	 * @param asms
	 * @throws IOException
	 */
	public void syncFIFO() {
		if (ssp.skipFIFOSync)
			return;
		
		_init();		
		
		// Synchronise according to sequence recorded during code generation.
		List<Transition> syncSeq = ssp.trans;
		Iterator<Transition> iterSeq = syncSeq.iterator();
		while (iterSeq.hasNext()) {
			Transition curSync = iterSeq.next();
			SPU sinkFPE = curSync.getSinkFPE();
			Assembly sinkFPEAsm = sinkFPE.asm;
			
			// Find the read channel NO to match against latter in assembly.
			int readIdx = curSync.fifo.getReadIdxIn(curSync.getSinkPE());
			
			int cnt = curSync.sinkPort.token.getNumData(sinkFPE.conf.coreType);
			// The number of instructions to be synchronised each time equal to
			// the number of data in a token. When the sink FPE is SIMD, each 
			// GET should be synchronised for every PE to find the maximum NOPs
			// to be inserted.
			for (int i = 0; i < cnt; i++) {
				int maxInsertedNops = 0;
				List<FIFOInstr> gets = sinkFPEAsm.copyOfGetInstrs;
				Iterator<FIFOInstr> iterGET = gets.iterator();
				
				if (!iterGET.hasNext()) {
					throw new RuntimeException("Mismatch in synchronization!");
				}
				
				FIFOInstr get = iterGET.next();
				assert !(get.asmInstr instanceof RptedInst) : "ERROR: Do not support repeated GET";
				iterGET.remove();
				int GETChNo = get.getChannelNo();
				
				if (readIdx != GETChNo) {
					throw new RuntimeException("Mismatch in synchronization!");				
				}
				
				for (PE sinkPE : sinkFPE.PEs) {
					// Find corresponding put instruction
					Assembly srcPEAsm = sinkPE.getInputFIFO(GETChNo).srcPE.asm;
					
					List<FIFOInstr> puts = srcPEAsm.getPutInstrs();
					
					Iterator<FIFOInstr> iterPUT = puts.iterator();
					
					// Get the corresponding write channel number in the PUT.
					int PUTChNo = sinkPE.getWriteChNo(GETChNo);

					// It is normal that a matched PUT is not at the beginning
					// of current PUT list (it is not a conflict, as they are in
					// different FIFOs). See below example
					// ------           ------
					// | A0 | 0-------  | B0 |
					// ------ 1\     /  ------
					//          \   /
					//           \ /    
					//            \
					//           / \
					//          /   \
					// ------ 2/     \  ------
					// | A1 | 3-------  | B1 |
					// ------           ------
					// PUT list is 0, 1, 2, 3. But for B0 GET from port 1, the
					// corresponding PUT is 2, which at that time is not at the
					// beginning of PUT list (after 1).
					//
					// So search the PUT list to find the matched PUT.
					boolean found = false;
					FIFOInstr put = new FIFOInstr();
					assert !(put.asmInstr instanceof RptedInst) : "ERROR: Do not support repeated PUT";
					while (iterPUT.hasNext()) {
						put = iterPUT.next();
						
						if (put.getChannelNo() != PUTChNo)  continue;
						
						// Found a matched PUT
						found = true;
						iterPUT.remove();
						break;
					}
					
					if (!found) {
						throw new RuntimeException(
								"Mismatch in synchronization! PUT was not found!");
					}
								
					// Start synchronisation
					int putCycle = put.getCycleAfterSync();
					int getCycle = sinkFPE.inc + get.asmInstr.cycle;

					// PUT also uses DSP48E datapath, so PUT is delayed by one
					// cycle compared to before. So GET must be at least two
					// cycles after PUT.
					if (getCycle - putCycle < 3) {
						int insertedNops = putCycle - getCycle + 3;
						if (maxInsertedNops < insertedNops)
							maxInsertedNops = insertedNops;
					}
					
				} // Finished PE by PE synchronisation
				
				// Set increments for this synchronisation
				sinkFPE.inc += maxInsertedNops;
				if (get.isLeadingGET) {
					// Leading GETs only increases pipeline overhead rather
					// than the loop body.
					sinkFPEAsm.loopBeginSynced = sinkFPE.inc + sinkFPEAsm.loopBegin;
					sinkFPEAsm.pipelineNOPs = sinkFPE.inc;
					sinkFPEAsm.leadingGETs.add(get);
				}
				
				_calCycleAfterSync(sinkFPE, get);
				
				get.setInsertedNops(maxInsertedNops);
				
				if (maxInsertedNops > 0)
					sinkFPEAsm.addSyncedInstr(get);
			} // Finished one transaction synchronisation
		}
		
		// Update cycle information after synchronisation for leading GETs. As
		// all NOPs are shifted outside loop body, the previously synchronised
		// GETs will be altered by later synchronisation, thus the cycle information
		// must be updated after all leading GETs are synchronised.
		for (SPU spu : ssp.spus) {
			for (FIFOInstr ai : spu.asm.leadingGETs) {
				ai.cycleAfterSync = ai.asmInstr.cycle + spu.asm.pipelineNOPs;
			}
		}
		
		// Calculate loop length
		int loopLength = 0;
		for (SPU spu : ssp.spus) {
			Assembly curAsm = spu.asm;
			int length = curAsm.loopLen + spu.inc - curAsm.pipelineNOPs;
			curAsm.loopLenSynced = length;
			if (loopLength < length)
				loopLength = length;			
			int cnt = spu.inc - curAsm.pipelineNOPs;
			if (cnt > 0)
				System.out.println(spu.name + ": Inserted NOPs to loop are: " +  cnt);
		}
				
		// Print information
		System.out.println("Loop length is: " + loopLength);				
		
		// Insert NOPs to assembly
		for (SPU spu : ssp.spus) {
			Assembly curAsm = spu.asm;
			List<FIFOInstr> syncedGETs = curAsm.getSyncedInstrs();

			Iterator<FIFOInstr> iterGET = syncedGETs.iterator();
			while (iterGET.hasNext()) {
				FIFOInstr curGET = iterGET.next();
				int nops = curGET.getInsertedNops();
				if (curGET.isLeadingGET) {
					// The leading GETs will insert NOPs outside loop body
					curAsm.insertNOP(0, nops);
				} else {
					curAsm.insertNOP(curAsm.asmInstrs.indexOf(curGET.asmInstr), nops);
				}
			}
			
			// Print information
			if (syncedGETs.size() > 0)
				System.out.println(
					spu.name + ": Synchronized " + syncedGETs.size() + " GETs!");
		}
		
		// Synchronise loop length and add JUMP instruction
		for (SPU spu : ssp.spus) {
			Assembly curAsm = spu.asm;
			if (loopLength >  curAsm.loopLenSynced) {
				int nops = loopLength - curAsm.loopLenSynced;
				
				// Try to cancel loop NOPs with startup NOPs
				if (curAsm.pipelineNOPs >= nops) {
					curAsm.loopBeginSynced = curAsm.pipelineNOPs-nops;
				} else {
					int cnt = nops - curAsm.pipelineNOPs;
					AsmInstr nop = new AsmInstr("NOP");
					for (int j = 0; j < cnt; j++)
						curAsm.addInstruction(nop);
					curAsm.loopBeginSynced = 0;
				}
				
				curAsm.loopLenSynced = loopLength;
			}
			AsmInstr jump = new AsmInstr("JMP " + curAsm.loopBeginSynced);
			curAsm.addInstruction(jump);
			spu.conf.jmpEn = true;
		}
		
		if (ssp.sg.mode == Mode.FFT) {
			if (true) {
				int latencyCycle = ssp.spus.get(ssp.spus.size()-1).asm.loopBeginSynced+loopLength;
				System.out.println("Latency cycle is: " + latencyCycle);
				ssp.latency = latencyCycle;
			}
		}
	}
	
	/**
	 * Calculate the cycle after a GET is synchronised. Besides the GET, the
	 * cycles for following PUTs before next GET are also calculated.
	 * @param spu The sink FPE
	 * @param get The just synchronised GET
	 */
	private void _calCycleAfterSync(SPU spu, FIFOInstr get) {
		get.setCycleAfterSync(spu.inc + get.asmInstr.cycle);
		
		List<FIFOInstr> fifoInstrs = spu.asm.fifoInstrs;
		
		// Remove the leading PUTs
		Iterator<FIFOInstr> it = fifoInstrs.iterator();
		while(it.hasNext()) {
			FIFOInstr fI = it.next();
			it.remove();
			if (fI.isGET) {
				break;
			}
		}
		
		// Find the PUT between two GETs
		List<FIFOInstr> puts = new LinkedList<FIFOInstr>();
		while (it.hasNext()) {
			FIFOInstr fI = it.next();
			if (!fI.isGET) {
				it.remove();
				puts.add(fI);
			} else {
				break;
			}
		}
		
		// Update the cycles of PUTs 
		for (FIFOInstr put : puts) {
			put.setCycleAfterSync(spu.inc + put.asmInstr.cycle);
		}
	}
	
	/**
	 * The first function to call before synchronisation starts. Firstly, parse
	 * the assembly and fill in FIFO instructions. Secondly, make a copy of GETs
	 * for synchronisation.
	 */
	private void _init() {
		_parseAsms();
		
		// Clone the assembly for PE by PE synchronisation
		for (SPU spu : ssp.spus) {
			Assembly asm = spu.asm;
			for (PE pe : spu.PEs) {
				try {
					pe.asm = (Assembly)asm.clone();
				} catch (CloneNotSupportedException e) {
					throw new RuntimeException("Can not clone?");
				}
			}
		}
					
		for (SPU spu : ssp.spus) {
			spu.asm.copyOfGetInstrs = new LinkedList<FIFOInstr>(spu.asm.getInstrs);
		}
	}
	
	/**
	 * Parse the FIFO instructions from assemblies.
	 */
	private void _parseAsms() {
		for (SPU spu : ssp.spus) {
			Assembly asm = spu.asm;
			// Helper variable to indicate a inter-PE PUT instruction has been  encountered.
			boolean interPEPUTEncountered = false;
			for (AsmInstr inst : asm.getInstructions()) {
				interPEPUTEncountered = _fillInFIFOInstrs(inst, asm, spu, interPEPUTEncountered);
			}						
		}
	}
	
	/**
	 * When an instruction is FIFO instruction, and it is not an external input
	 * output FIFO instruction, then fill it into the FIFO instructions list.
	 * @param instr The input assembly instruction.
	 */
	private boolean _fillInFIFOInstrs(AsmInstr instr, 
			Assembly asm, SPU spu, boolean interPEPUTEncountered) {
		if (!instr.rdFIFO && !instr.wrFIFO) {
			return interPEPUTEncountered;
		}
	    	
    	int chNo = instr.chNo;
    	
    	if (instr.rdFIFO) {
    		if (!spu.getPE(0).getInputFIFO(chNo).isExInFIFO) {
    			FIFOInstr fInstr = new FIFOInstr(instr, chNo, true);
    			if (!interPEPUTEncountered) fInstr.isLeadingGET = true;
    			asm.getInstrs.add(fInstr);
    			asm.fifoInstrs.add(fInstr);
    			return interPEPUTEncountered;
    		}
    	} else {
    		FIFO f = spu.getPE(0).getOutputFIFO(chNo);
    		f.putInsts.add(instr);
    		if (!f.isExOutFIFO) {
    			interPEPUTEncountered = true;
    			FIFOInstr fInstr = new FIFOInstr(instr, chNo, false);
    			asm.putInstrs.add(fInstr);
    			asm.fifoInstrs.add(fInstr);
    			return interPEPUTEncountered;
    		}
    		  		    		
    	}
    	return interPEPUTEncountered;
	}
	///////////////////////////////////////////////////////////////////
	////                         public variables                  ////
	
	private SSP ssp;
	
}

