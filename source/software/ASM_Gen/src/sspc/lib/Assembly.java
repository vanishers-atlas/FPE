package sspc.lib;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import sspc.lib.SPUConfig.ALUTYPE;
import sspc.lib.dsp.FFT.FFTType;
import sspc.softgen.SWGenUtils;
import sspc.softgen.SoftwareGen.Mode;
import sspc.softgen.SoftwareGen.FIFOAllocScheme;

public class Assembly implements Cloneable {
	public Assembly(SPU spu, SSP ssp) {
		_spu = spu;
		_ssp = ssp;
		if (_spu.conf.coreType == ALUTYPE.REAL16B1D) {
			PDEPTH = 4;
		} else if (_spu.conf.coreType == ALUTYPE.REAL32B4D) {
			PDEPTH = 7;
		} else if (_spu.conf.coreType == ALUTYPE.CPLX16B4D) {
			PDEPTH = 5;
		} else {
			throw new RuntimeException("ERROR: Unrecognized type.");
		}
	}

	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////

	/**
	 * Insert an instruction to certain location in the assembly.
	 * 
	 * @param idx
	 * @param inst
	 */
	public void insertInstruction(int idx, AsmInstr inst) {
		asmInstrs.add(idx, inst);
	}

	/**
	 * Append an instruction to the end of the assembly.
	 * 
	 * @param inst
	 */
	public void addInstruction(AsmInstr inst) {
		asmInstrs.add(inst);
	}

	/**
	 * Return the assembly
	 * 
	 * @return
	 */
	public List<AsmInstr> getInstructions() {
		return asmInstrs;
	}

	/**
	 * Insert cnt number of NOPs to certain position in assembly
	 * 
	 * @param idx
	 *            The location index where insertion starts
	 * @param cnt
	 *            The number of NOPs to be inserted
	 */
	public void insertNOP(int idx, int cnt) {
		for (int i = 0; i < cnt; i++) {
			insertInstruction(idx, AsmInstr.createNOP());
		}
	}

	/**
	 * Add get to the get instruction list.
	 * 
	 * @param inst
	 */
	public void addGetInstr(FIFOInstr inst) {
		getInstrs.add(inst);
	}

	/**
	 * Get an GET instruction from specified location
	 * 
	 * @param idx
	 * @return
	 */
	public FIFOInstr getGetInstr(int idx) {
		return getInstrs.get(idx);
	}

	/**
	 * Add put to the put instruction list.
	 * 
	 * @param inst
	 */
	public void addPutInstr(FIFOInstr inst) {
		putInstrs.add(inst);
	}

	public List<FIFOInstr> getPutInstrs() {
		return putInstrs;
	}

	/**
	 * Add synchronised instructions to the syncedInstrs.
	 * 
	 * @param inst
	 */
	public void addSyncedInstr(FIFOInstr inst) {
		syncedInstrs.add(inst);
	}

	public List<FIFOInstr> getSyncedInstrs() {
		return syncedInstrs;
	}

	/**
	 * Parse assembly file. Set the loop beginning; configure data memory; save
	 * constant port parameters; fill in AsmInstruction fields; detect and fill
	 * in FIFO instruction list
	 * 
	 * @param asmFile
	 * @throws IOException
	 */
	public void parseFile(String asmFile) throws IOException {
		FileInputStream fstream = new FileInputStream(asmFile);
		DataInputStream in = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String strLine;

		// Count GET_CONST_PORT instructions
		int cntGETCP = 0;
		

		// Read File Line By Line
		while ((strLine = br.readLine()) != null) {
			String instrName = getAsmInstrName(strLine);

			if (!_validInstr(instrName)) {
				if (instrName.equals("GET_CONST_PORT")) {
					// Found constant port instructions. Fill in the (mem, para) map.
					int memAddr = _getMemAddr(strLine);
					for (PE pe : _spu.PEs) {
						try {
							Double paraValue = pe.cpParas.get(cntGETCP);
							pe.memParaMap.put(memAddr, paraValue);
						} catch (IndexOutOfBoundsException e) {
							throw new RuntimeException(
									"Cannot find paramter to match GET_CONST_PORT instruction ");
						}
					}
					cntGETCP++;
				} else {
					if (strLine.matches(".*\\w+") && !strLine.contains("//"))
						System.out.println("INFO: skip "+strLine);
				}
				continue;
			}
			
			AsmInstr inst = _fitNewInstr(strLine);
			// When parsed a mark instruction, continue
			if (inst == null) continue;

			asmInstrs.add(inst);
		}
		
		// Sanity check
		if (_maskOn)
			throw new RuntimeException("ERROR: Haven't seen MASKEND.");
		else if (_rptOn)
			throw new RuntimeException("ERROR: Haven't seen RPTEND.");
		// Close the input stream
		in.close();
	}

	/**
	 * Write assembly file instruction by instruction.
	 * 
	 * @param fileName
	 * @throws IOException
	 */
	public void printAsm(String fileName) throws IOException {
		Iterator<AsmInstr> iterInstr = asmInstrs.iterator();
		StringBuffer code = new StringBuffer();
		while (iterInstr.hasNext()) {
			AsmInstr inst = iterInstr.next();
			code.append(inst.instrStr + "\n");
		}

		// Write asm to a file
		SWGenUtils.writeToFile(fileName, code.toString());

	}

	/**
	 * Get instruction name from the string line.
	 * 
	 * @param line
	 * @return
	 */
	public static String getAsmInstrName(String line) {
		Pattern pat = Pattern.compile("^[\\s]*(\\w+)");
		Matcher m = pat.matcher(line);
		return m.find() ? m.group(1) : "NOTFOUND";
	}

	/**
	 * The clone is intended to service FIFO sharing. The assembly returned from
	 * LLVM is cloned for every PE so that a PE by PE synchronisation can be
	 * done. This uses the clone() method of java.lang.Object, which makes a
	 * field-by-field copy. It then clones the PUT instruction list.
	 * 
	 * The assembly and synchronised instruction list is not cloned, as they
	 * will not be changed during PE by PE synchronisation. Also not cloned is
	 * GET instruction list, as they change only once for PE by PE
	 * synchronisation.
	 */
	public Object clone() throws CloneNotSupportedException {
		Assembly newObj = (Assembly) super.clone();

		// Clone GET and PUT instruction list
		newObj.getInstrs = new LinkedList<FIFOInstr>(getInstrs);
		newObj.putInstrs = new LinkedList<FIFOInstr>(putInstrs);

		return newObj;
	}
	
	public void cycleInRPTSegs() {
		for (RPTSegment seg : _rptSegs) {
			seg.parseCycle();
		}
	}
	
	/**
	 * Post compiling, set configuration parameters according to compiled result.
	 * E.g. RF Size
	 */
	public void setParameters() {
		if (_ssp.sg.mode == Mode.FFT) {
			// Set RF size for SIMD FFT when default FIFO allocation is used.
			// Statistic results from compiled results for 1024 SIMD FFT.
			// Complex
			// SPU5 16 DM; SPU6 61 DM; SPU7 132, DM; SPU8 265
			// Real
			// SPU3  3; SPU4 20; SPU5 64; SPU6 134; SPU7 262; SPU8 518
			//
			// So it is worth when complex C10V8, set SPU6; and real C10V16,
			// set SPU4 and SPU5.
			if (_ssp.sg.fft.pointSize == 1024) {
				if (_ssp.sg.fft.type == FFTType.IL4_CPLX_SIMD &&
						_ssp.sg.bufAllocScheme == FIFOAllocScheme.BASELINE && _ssp.sg.fft.simdWayNum == 16 && (_spu.idx == 6 || _spu.idx == 5))
					// C10V8, Baseline, set SPU6, SPU5
					_spu.conf.setRFSize(64);
				else if (_ssp.sg.fft.type == FFTType.IL2_REAL_SIMD &&
						_ssp.sg.bufAllocScheme == FIFOAllocScheme.BASELINE && _ssp.sg.fft.simdWayNum == 16 && (_spu.idx == 3 || _spu.idx == 4 || _spu.idx == 5))
					// R10V16, Baseline, set SPU3 SPU4 SPU5
					_spu.conf.setRFSize(64);
				else if (_ssp.sg.fft.type == FFTType.IL4_CPLX_MIMD && (_ssp.spus.size() == 16 || _ssp.spus.size() == 32))
					// C16V1, C32V1
					_spu.conf.setRFSize(64);
			} else if (_ssp.sg.fft.pointSize == 256) {
				if (_ssp.sg.fft.type == FFTType.IL4_CPLX_MIMD && (_ssp.spus.size() == 4 || _ssp.spus.size() == 8))
					// C4V1, C8V1
					_spu.conf.setRFSize(64);
				else if (_ssp.sg.fft.type == FFTType.IL4_CPLX_SIMD &&
						 _ssp.sg.bufAllocScheme == FIFOAllocScheme.BASELINE && 
						 _ssp.sg.fft.simdWayNum == 1 && (_spu.idx == 5 || _spu.idx == 6 || _spu.idx == 7))
					// R8V1, Baseline, set SPU5 SPU6 SPU7
					_spu.conf.setRFSize(64);
				else if (_ssp.sg.fft.type == FFTType.IL4_CPLX_SIMD &&
						 _ssp.sg.bufAllocScheme == FIFOAllocScheme.BASELINE && 
						 _ssp.sg.fft.simdWayNum == 2 && (_spu.idx == 5 || _spu.idx == 6))
					// R8V1, Baseline, set SPU5 SPU6
					_spu.conf.setRFSize(64);
			}
		}
	}
	
	/**
	 * Memory folding pass to support memory-register architecture.
	 * 
	 * For store folding
	 * Produce__Use
	 *        |_Store can not fold
	 * Produce__Store can fold
	 * 
	 * For load folding
	 * Load-Use and use is 2nd operand or can be swapped to second operand can fold
	 * otherwise, can not fold 
	 */
	public void dmFoldingPass() {
		if (_spu.conf.dmEn == false) {
			return;
		}
		
		if (skipDMFoldingPass == true) {
			System.out.println("INFO: DM folding pass is skipped by request.");
			return;
		}
		
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			
			boolean canFold = true;
			
			if (I.isStore()) {
				// Note this corresponds to formatTransform()
				Operand regToStore = I.oprds.get(2);
				// Create a copy of iterator
				ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.previousIndex());
				AsmInstr defI = null;
				
				// Loop backwards until find the define. When find another use,
				// it cannot fold
				while (itTmp.hasPrevious()) {
					AsmInstr P = itTmp.previous();
					
					if (P.definesRegister(regToStore)) {
						defI = P;
						break;
					}
					
					if (P.usesRegister(regToStore)) {
						canFold = false;
						break;
					}
				}
				
				if (!canFold) continue;
				
				// Loop forward until find a kill. When find another use, it 
				// cannot fold
				itTmp = asmInstrs.listIterator(it.nextIndex());
				while (itTmp.hasNext()) {
					AsmInstr N = itTmp.next();					
					
					if (N.usesRegister(regToStore)) {
						canFold = false;
						break;
					}
					
					if (N.definesRegister(regToStore)) 
						break;
				}
				
				if (!canFold) continue;
				
				// Fold the store				
				it.previous();
				// Replace store with an NOP, because it may cause hazard if 
				// we simply delete it. Let the clean-redundant-NOPs pass to
				// clean it up.
				it.remove();
				it.add(AsmInstr.createNOP());
				
				assert defI != null;
				
				defI.foldStore(I.dmWrOprd);
			} else if (I.isLoad()) {
				Operand regLoadTo = I.getOperand(0);
				Vector<AsmInstr> loadUseIs = new Vector<AsmInstr>();
				boolean memKilled = false;
				
				Operand mem = I.getOperand(2);
				
				// Loop forward, stop until find regLoadTo is killed or to the
				// end. When find use of regLoadTo, it cannot fold when it is
				// not the only second operand; when the mem has been killed,
				// it cannot fold when there are more uses of regLoadTo.
				// 
				ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.nextIndex());
				while (itTmp.hasNext()) {
					AsmInstr N = itTmp.next();
										
					if (N.usesRegister(regLoadTo)) {
						// If memory has been killed, and there are still uses
						// of register, we can not fold it.
						if (memKilled 
						 || (N.findRegisterUseOperandIdx(regLoadTo) != 2 
						     && N.instName != SPUInst.PUT_FRRR)
						 || N.usesRegister(regLoadTo, 3)){
							canFold = false;
							break;
						}
						
						// PUT is always foldable.
						loadUseIs.add(N);						
					}
					
					// If find the register been killed, it means there is no 
					// more use of this register, so searching finishes.
					if (N.definesRegister(regLoadTo)) 
						break;
					
					if (N.definesMemory(mem))
						memKilled = true;
				}
				
				if (!canFold) continue;
				
				// Fold the load
				it.previous();
				// Replace store with an NOP, because it may cause hazard if 
				// we simply delete it. Let the clean-redundant-NOPs pass to
				// clean it up.
				it.remove();
				it.add(AsmInstr.createNOP());
				
				assert !loadUseIs.isEmpty();
				
				for (AsmInstr loadUse : loadUseIs) {
					loadUse.foldLoad(mem);
				}
			}
		}
		
		// Memory move folding is separated from above as new memory move might
	    // be created after above.
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			boolean canFold = true;
		
			if (I.isMemMove()) {
				// This part is to solve a LLVM deficiency that inline assembly 
				// with '=m' constraint is passed into an inline function which
				// has inline assembly with 'm' constraint to use that argument
				// but failed to regard them as the same memory operand, resulting
				// an memory move from the '=m' to 'm'.
				Operand memMoveTo = I.getOperand(0);
				Vector<AsmInstr> moveUseIs = new Vector<AsmInstr>();
				boolean memKilled = false;
				
				Operand mem = I.getOperand(2);
				
				// Loop forward, stop until find memMoveTo is killed or to the
				// end. When find use of memMoveTo, it cannot fold when it is
				// not the only second operand; when the mem has been killed,
				// it cannot fold when there are more uses of memMoveTo.
				ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.nextIndex());
				while (itTmp.hasNext()) {
					AsmInstr N = itTmp.next();
										
					if (N.usesMemory(memMoveTo)) {
						// If memory has been killed, and there are still uses
						// of memMoveTo, we can not fold it.
						if (memKilled 
						 || (N.findMemoryUseOperandIdx(memMoveTo) != 2 
						     && N.instName != SPUInst.PUT_FRMR)
						     || N.usesMemory(memMoveTo, 3)){
							canFold = false;
							break;
						}
						
						// PUTM is always foldable.
						moveUseIs.add(N);
					}
					
					// If find the register been killed, it means there is no 
					// more use of this register, so searching finishes.
					if (N.definesMemory(memMoveTo)) 
						break;
					
					if (N.definesMemory(mem))
						memKilled = true;
				}
				
				if (!canFold) continue;
				
				// Fold the load
				it.previous();
				// Replace store with an NOP, because it may cause hazard if 
				// we simply delete it. Let the clean-redundant-NOPs pass to
				// clean it up.
				it.remove();
				it.add(AsmInstr.createNOP());
				
				assert !moveUseIs.isEmpty();
				
				for (AsmInstr moveUse : moveUseIs) {
					moveUse.foldMemMove(mem);
				}
			}
		}
		
		_computeDMSize();
	}
	
	public void putFoldingPass() {
		if (skipPUTFoldingPass) {
			System.out.println("INFO: putFoldingPass is skipped by request.");
			return;
		}
		
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			
			boolean canFold = true;
			AsmInstr defI = null;
			
			if (!I.isPUT()) continue;
			
			if (!I.rdDM0) {
				// First case is PUT. Try to fold the REG.
				Operand regToPut = I.oprds.get(0);
				assert regToPut.isReg();
				
				// Create a copy of iterator
				ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.previousIndex());				
				
				// Look backwards until find the define. When find another use, or it sees another PUT
				// it cannot fold
				while (itTmp.hasPrevious()) {
					AsmInstr P = itTmp.previous();
					if (P.isPUT() || P.isGET() || P.instName == SPUInst.UNLDSORT_RXXX) {
						canFold = false;
						break;
					}
					
					if (P.definesRegister(regToPut)) {
						defI = P;
						break;
					}
					
					if (P.usesRegister(regToPut)) {
						canFold = false;
						break;
					}
				}
				
				if (!canFold) continue;
				
				// Loop forward until find a kill. When find another use, it 
				// cannot fold
				itTmp = asmInstrs.listIterator(it.nextIndex());
				while (itTmp.hasNext()) {
					AsmInstr N = itTmp.next();					
					
					if (N.usesRegister(regToPut)) {
						canFold = false;
						break;
					}
					
					if (N.definesRegister(regToPut)) 
						break;
				}
				
				if (!canFold) continue;								
			} else {
				// The other case is PUTM. Try to fold MEM.
				Operand memToPut = I.oprds.get(0);
				// Create a copy of iterator
				ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.previousIndex());
				
				// Loop backwards until find the define. When find another use, or it sees another PUT
				// it cannot fold
				while (itTmp.hasPrevious()) {
					AsmInstr P = itTmp.previous();
					if (P.isPUT() || P.isGET()) {
						canFold = false;
						break;
					}
					
					if (P.definesMemory(memToPut)) {
						defI = P;
						break;
					}
					
					if (P.usesMemory(memToPut)) {
						canFold = false;
						break;
					}
				}
				
				if (!canFold) continue;
				
				// Loop forward until find a kill. When find another use, it 
				// cannot fold
				itTmp = asmInstrs.listIterator(it.nextIndex());
				while (itTmp.hasNext()) {
					AsmInstr N = itTmp.next();					
					
					if (N.usesMemory(memToPut)) {
						canFold = false;
						break;
					}
					
					if (N.definesMemory(memToPut)) 
						break;
				}
				
				if (!canFold) continue;		
			}
			
			// Fold the PUT				
			it.previous();
			// Replace store with an NOP, because it may cause hazard if 
			// we simply delete it. Let the clean-redundant-NOPs pass to
			// clean it up.
			it.remove();
			it.add(AsmInstr.createNOP());
			foldedPUTNum ++;
			
			assert defI != null;
			
			defI.foldPUT(I.chNo);
			
		}
	}
	
	public void immToSMPass() {
		if (skipIMMToSMPass) return;
		
		// Record old SM base pointer
		int SMbase = 0;
		
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			if (I.rdSM) {			
				SMbase = _fillInSM(it, I, _spu.sm, SMbase);
			}
		}
	}
	
	/**
	 * Flexible ports can be set only after memory folding pass finished.
	 */
	public void setFlexPortsPass() {
		SPUConfig cf = _spu.conf;
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			
			// Without this line, 'SORT' may be chosen as a mistake
			if (I.instName.name().indexOf("_") == -1) continue;
			
			String oprds = I.instName.name().substring(I.instName.name().indexOf("_")+1);
			if (oprds.length() != 4) continue;
			
			char srcA = oprds.charAt(1);
			char srcB = oprds.charAt(2);
			char srcC = oprds.charAt(3);			
			
			cf.flexAType = cf.flexAType | getFlexCoding(srcA);
			cf.flexBType = cf.flexBType | getFlexCoding(srcB);
			cf.flexCType = cf.flexCType | getFlexCoding(srcC);
		}
		int RA, RB, RC;
		RA = cf.flexAType & 1;
		RB = cf.flexBType & 1;
		RC = cf.flexCType & 1;
		if ((RA | RB | RC) == 0)
			cf.rfEn = false;
	}
	
	private int getFlexCoding(char m) {
		if (m == 'R') return 1;
		if (m == 'M') return 2; 
		if (m == 'I') return 4;
		return 0;
	}
	
	public void insertDMBaseSetPass() {
		if (skipInsertDMBaseSetPass) {
			System.out.println("INFO: insert DM base pass is skipped by request.");
			return;
		}
		
		int dmSize = _spu.conf.dmSize;
		int blockSize = (int) Math.pow(2, _spu.conf.dmOffsetWidth);
		
		if (dmSize <= blockSize) return;
		
		// Record DM read and write base pointer
		int dmRdBase = 0;
		int dmWrBase = 0;
		
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			
			if (I.wrDM) {
				Operand def = I.dmWrOprd;
				int memAddr = def.dmSPOfs;
				int newBase = memAddr / blockSize;
				
				if (newBase != dmWrBase) {
					// FWD instruction can not emit SETBS
					assert !I.isFWD;
					
					dmWrBase = newBase;
					// Emit UPDDMWRBASE
					_spu.conf.dmWBSetEn = true;
					it.previous();
					AsmInstr setdmwb = AsmInstr.createSETDMWB(newBase);
					it.add(setdmwb);
					it.next();
				}
				
				// replace memory index
				if (memAddr >= blockSize) {
					I.changeOperandTo("&" + memAddr%blockSize, 0);
					I.reparseInst();
				}
			}
			
			if (I.rdDM0) {						
				int memAddr = I.dmRdOprd0.dmSPOfs;
				int newBase = memAddr / blockSize;
				
				if (newBase != dmRdBase) {
					// FWD instruction can not emit UPDBASE
					assert !I.isFWD;
					_spu.conf.dmDirectEn = false;
					
					dmRdBase = newBase;
					// Emit UPDDMRDBASE
					_spu.conf.dmRBSetEnB0 = true;
					it.previous();
					AsmInstr setdmrb = AsmInstr.createSETDMRB(newBase);
					it.add(setdmrb);
					it.next();
				}
				
				// replace memory index
				if (memAddr >= blockSize) {
					I.changeOperandTo("&" + memAddr%blockSize, I.origOprds.indexOf(I.dmRdOprd0));
					I.reparseInst();
				}
			}
		}		
	}
	
	public void removeUnneededNOPsPass() {
		if (skipRemoveUnneededNOPsPass) {
			System.out.println("INFO: removeUnneededNOPsPass is skipped by request.");
			return;
		}
		
		int sta = 0;
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			if (I.instName != SPUInst.NOP)
				continue;

			int idxI = it.previousIndex();
			
			if (_isNOPUnneeded(idxI)) {
				// The NOP is unneeded, delete it
				it.previous();
				it.remove();
				sta++;
			}
		}
		System.out.println("No of unneeded NOPs removed is " + sta);
	}
	
	/**
	 * The pass to make forward instruction conversion.
	 */
	public void fwdConvertPass() {
		if (skipFWDConvertPass) {
			System.out.println("INFO: fwdConvertPass is skipped by request.");
			return;
		}
		
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			// I is the forward use, and T is the forward def. The search goes backwards.
			AsmInstr I = it.next();
			int idxI = it.previousIndex();
			
			if (!_FWDUseInsts.contains(I.instName)) continue;
			
			int idxT = it.previousIndex() - PDEPTH - 1;
			if (idxT < 0) continue;
			
			AsmInstr T = asmInstrs.get(idxT);
			if (!_canBeFwdPair(T, I)) {
				// Deal with a corner case. When I is ADD, switch operands and try again.
				if (I.instName == SPUInst.ADDMUL_RRRR && I.isADD()) {
					String addoprd = I.origOprds.get(1).str;
					I.changeOperandTo(I.origOprds.get(2).str, 1);
					I.changeOperandTo(addoprd, 2);
					I.reparseInst();
					if (!_canBeFwdPair(T, I))
						continue;
				}
				else 
					continue;
			}
			
			// Create a copy of iterator
			ListIterator<AsmInstr> itTmp = asmInstrs.listIterator(it.previousIndex());
			
			// Find the pattern
			int idx = 0;
			int numOthers = 0;
			int idxOther = 0, idxOther1 = 0;
			AsmInstr otherI = null, otherI1 = null;
			boolean mayConvert = false;
			
			for (; itTmp.hasPrevious() && idx < PDEPTH; idx++) {
				AsmInstr pre = itTmp.previous();
				
				if (pre.instName != SPUInst.NOP) {
					// When it crosses another PUT, or an FWD instruction, 
					// it can not be converted. When it crosses base update
					// instructions, check T to see will it cause a conflict.
					if (pre.instName.name().contains("FWD")) break;
					
					if (pre.instName == SPUInst.SETSMRB_0 && T.rdSM) 
						break;
					
					if (pre.instName == SPUInst.SETDMWB_0 && T.wrDM)
						break;
					
					if ((pre.instName == SPUInst.SETDMRB_0 && T.rdDM0 && T.dmRdOprd0.dmSPIdx == 0)
					 || (pre.instName == SPUInst.SETDMRB_1 && T.rdDM0 && T.dmRdOprd0.dmSPIdx == 1)
					 || (pre.instName == SPUInst.SETDMRB_2 && T.rdDM0 && T.dmRdOprd0.dmSPIdx == 2))
						break;						

					if (I.instName == SPUInst.PUT_FRRR && pre.instName == SPUInst.PUT_FRRR) break;
					
					numOthers++;
					if (numOthers > 2) break;

					if (numOthers == 1) {
						idxOther = itTmp.nextIndex();
						otherI = pre;
					} else {
						// Caution: as it searches backwards, so the right sequence will be idxOther1, idxOther
						idxOther1 = itTmp.nextIndex();
						otherI1 = pre;
					}
				}
				
				// Set canConvert when it successfully goes to the last
				// instruction.
				if (idx == PDEPTH - 1)
					mayConvert = true;
			}
			
			if (!mayConvert) continue;
			
			// When redefine happens, skip
			String fwdDef = _getFwdDefOperand(T);
			
			int cost1 = 0;
			int cost2 = 0;
			
			// CASE 1: All are NOPs
			// Check fields: for clarity PDEPTH = 5
			// I vs T-1, T-2, T-3, T-4
			// I+1 vs T-1, T-2, T-3
			// I+2 vs T-1, T-2
			// I+3 vs T-1
			// T vs I+1, I+2, I+3, I+4
			if (numOthers == 0) {
				// cost1 is NOPs inserted before T, caused by hazards between [I ... I+PDEPTH-1] and instructions
				// before T.
				int hIdx =  _checkCostBackwardWithMask(idxI, idxT-1, PDEPTH-1, fwdDef);
				cost1 = (hIdx == -1) ? 0 : PDEPTH - 1 - hIdx;
				
				for (int i = 0; i < PDEPTH - 1; i++) {
					hIdx = _checkCostBackwardWithMask(idxI + 1 + i, idxT-1, 
							PDEPTH - 2 - i, fwdDef);
					int tmp = (hIdx == -1) ? 0 : PDEPTH - hIdx - 2 - i;
					cost1 = Math.max(tmp, cost1);
				}
				
				// cost2 is NOPs inserted after I, caused by hazards between T and instructions
				// after I.
				hIdx =  _checkCostForward(idxT, idxI + 1, PDEPTH - 1);
				cost2 = (hIdx == -1) ? 0 : PDEPTH - 1 - hIdx;
				
				int cost = cost1 + cost2;
				if (cost > PDEPTH) continue;				
			} else if (numOthers == 1) {
				// CASE 2: One 'other' instruction
				// 'other' will be inserted after I
				// Check fields: for clarity PDEPTH = 5
				// I vs T-1, T-2, T-3, T-4
				// I+1 vs T-1, T-2
				// I+2 vs T-1
				// Other vs T-1, T-2, T-3
				// T vs I+1, I+2, I+3
				// Other vs I+1, I+2, I+3, I+4, I+5
				
				if (_hasHazard(I, otherI)) continue;
				
				// cost1 is NOPs inserted before T
				int hIdx = _checkCostBackwardWithMask(idxI, idxT - 1, PDEPTH - 1, fwdDef);
				cost1 = (hIdx == -1) ? 0 : PDEPTH - hIdx - 1;
				
				hIdx =  _checkCostBackwardWithMask(idxOther, idxT - 1, PDEPTH-2, fwdDef);
				int tmp = (hIdx == -1) ? 0 : PDEPTH - hIdx - 1;
				cost1 = Math.max(tmp, cost1);
				
				for (int i = 0; i < PDEPTH-3; i++) {
					hIdx = _checkCostBackwardWithMask(idxI + 1 + i, idxT - 1, 
							PDEPTH-3-i, fwdDef);
					tmp = (hIdx == -1) ? 0 : PDEPTH - 3 - i - hIdx;
					cost1 = Math.max(tmp, cost1);
				}				
				
				// cost2 is NOPs inserted after Other
				hIdx =  _checkCostForward(idxT, idxI + 1, PDEPTH - 2);
				cost2 = (hIdx == -1) ? 0 : PDEPTH - 2 - hIdx;
				
				hIdx =  _checkCostForward(idxOther, idxI + 1, PDEPTH);
				tmp = (hIdx == -1) ? 0 : PDEPTH - hIdx;
				cost2 = Math.max(tmp, cost2);
				
				int cost = cost1 + cost2;
				if (cost > PDEPTH - 1) {
					// Deal with a special case:
					// MULI R12, R15, #1
					// MULI R11, R13, #1
					// NOP
					// NOP
					// NOP
					// PUT R12, ^2
					// PUT R11, ^2
					//
					// or
					//
					// MULI  R14, R10, #3
					// MULI  R10, R10, #4
					// NOP
					// NOP
					// NOP
					// ADDMULI  R14, R15, #4, R14
					// ADDMULI  R10, R15, #5, R10
					AsmInstr nextInst = asmInstrs.get(idxI + 1);
					if (!_FWDUseInsts.contains(nextInst.instName) || !_canBeFwdPair(otherI, nextInst))
						continue;
				}							
			} else if (numOthers == 2) {
				// CASE 3: Two 'other' instruction
				// 'other' will be inserted after I
				// Check fields: for clarity PDEPTH = 5
				// I vs T-1, T-2, T-3, T-4
				// I+1 vs T-1
				// Other1 vs T-1, T-2, T-3
				// Other0 vs T-1, T-2
				// T vs I+1, I+2
				// Other1 vs I+1, I+2, I+3, I+4
				// Other0 vs I+1, I+2, I+3, I+4, I+5
				
				if (_hasHazard(I, otherI) || _hasHazard(I, otherI1)) continue;
				
				// cost1 is NOPs inserted before T
				int hIdx =  _checkCostBackwardWithMask(idxI, idxT-1, PDEPTH-1, fwdDef);
				cost1 = (hIdx == -1) ? 0 : PDEPTH - 1 - hIdx;
				
				hIdx =  _checkCostBackwardWithMask(idxOther1, idxT - 1, PDEPTH-2, fwdDef);
				int tmp = (hIdx == -1) ? 0 : PDEPTH - 2 - hIdx;
				cost1 = Math.max(tmp, cost1);
				
				hIdx =  _checkCostBackwardWithMask(idxOther, idxT - 1, PDEPTH-3, fwdDef);
				tmp = (hIdx == -1) ? 0 : PDEPTH - 3 - hIdx;
				cost1 = Math.max(tmp, cost1);
				
				for (int i = 0; i < PDEPTH-4; i++) {
					hIdx = _checkCostBackwardWithMask(idxI + 1 + i, idxT - 1, 
							PDEPTH-4-i, fwdDef);
					tmp = (hIdx == -1) ? 0 : PDEPTH - 4 - i - hIdx;
					cost1 = Math.max(tmp, cost1);
				}				
				
				// cost2 is NOPs inserted after Other
				hIdx =  _checkCostForward(idxT, idxI + 1, PDEPTH - 3);
				cost2 = (hIdx == -1) ? 0 : PDEPTH - 3 - hIdx;
				
				hIdx =  _checkCostForward(idxOther1, idxI + 1, PDEPTH-1);
				tmp = (hIdx == -1) ? 0 : PDEPTH - 1 - hIdx;
				cost2 = Math.max(tmp, cost2);
				
				hIdx =  _checkCostForward(idxOther, idxI + 1, PDEPTH);
				tmp = (hIdx == -1) ? 0 : PDEPTH - hIdx;
				cost2 = Math.max(tmp, cost2);
				
				int cost = cost1 + cost2;

				if (cost > PDEPTH - 2) continue;
			}
			
			// FWD instructions can be forwarded, but we need special care
			// about the NOP inserted before T
			boolean fwdFwd = false;
			if (cost1 > 0 && T.instName.name().contains("FWD")) {
				AsmInstr preT = asmInstrs.get(asmInstrs.indexOf(T) - 1);
				if (preT.instName.name().contains("FWD")) {
					// Cannot support fwd-fwd-fwd yet
					continue;
				} else {
					fwdFwd = true;
				}
			}
			
			// Convert to FWD, and delete NOPs
			AsmInstr cv = it.previous();
			cv.convertToFWD();
			for (int i = 0; i < PDEPTH; i++) {
				it.previous();
				it.remove();
			}
			// Previous to T (pointer between T-1 and T)
			it.previous();
			
			if (fwdFwd)
				it.previous();
			
			// Add NOPs before T if there are hazards
			for (int i = 0; i < cost1; i++) {
				it.add(AsmInstr.createNOP());
			}
			
			// Next to the FWD (pointer between I and I+1)
			it.next();
			it.next();
			
			if (fwdFwd)
				it.next();
			
			// 'other's are inserted after FWD
			if (numOthers == 1) {
				it.add(otherI);
			} else if (numOthers == 2) {
				it.add(otherI1);
				it.add(otherI);
			}
			
			// Add NOPs after I if there are hazards
			for (int i = 0; i < cost2; i++) {
				it.add(AsmInstr.createNOP());
			}		
			
			_postConvClean(it, T);
		}
	}
	
		
	/**
	 * This pass may be called after FIFOSync to convert NOPs into repeat form.
	 * NOP
	 * NOP
	 * NOP
	 * NOP
	 * NOP
	 * convert to ->>
	 * RPT 4
	 * NOP
	 */
	public void rptNOPsPass() {
		if (skipRPTNopsPass) {
			System.out.println("INFO: rptNOPsPass is skipped by request.");
			return;
		}
		
		boolean rptNOP = false;
		int rptCnt = 0;
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			if (!it.next().isNOP()) continue;
				
			int cntNOPs = 1;
			AsmInstr N = null;
			while (it.hasNext()) {
				N = it.next();
				if (N.isNOP()) 
					cntNOPs++;
				else
					break;
			}
			
			// Replace when it exceeds the threshold. The threshold is
			// 1. the size must beyond 64, and
			// 2. gain is positive, and
			// 3. if rpt is already on, or
			// 4. when replace, it reduces below 64 or
			// 5. when replace, it reduces at lease one 512 block
			int gain = cntNOPs - 5;
			if (asmInstrs.size() > 64
			 && gain > 0
			 && (_spu.conf.rptEn == true 
			  || (asmInstrs.size() - gain <= 64) 
			  || (asmInstrs.size()/512 > (asmInstrs.size()- gain)/512)
			    )
			   )
			{
				rptNOP = true;
				rptCnt = (cntNOPs - 1 > rptCnt)? cntNOPs-1 : rptCnt;
				if (!N.isNOP())
					it.previous();
				
				// Delete all NOPs and insert RPT and NOP
				for (int i = 0; i < cntNOPs; i++) {
					it.previous();
					it.remove();
				}
				
				// When the RPT cnt exceeds 128, the RPT logic may become the
				// frequency bottleneck. So we divide large RPT into small
				// 128 chunks.
				int CHUNKSIZE = 128;
				int CHUNKWIDTH = 7;
				
				int chunks = cntNOPs/CHUNKSIZE;
				int rem = cntNOPs%CHUNKSIZE - _spu.conf.RPTOverhead();
				
				for (int i = 0; i < chunks; i++) {
					_curRPTSeg = new RPTSegment();
					_rptSegs.add(_curRPTSeg);
					
					RPTLevel lev0 = new RPTLevel(_curRPTSeg, 0);
					_curRPTSeg.levels.add(lev0);
					
					lev0.cntNum = CHUNKSIZE;
					
					AsmInstr inst = AsmInstr.createRPT(1, CHUNKSIZE);					
					it.add(inst);
					
					// This is the RPT instruction.
					inst.rptInfo = lev0;
					
					// This is the delay slot
					for (int j = 0; j < _spu.conf.RPTOverhead(); j++) {
						inst = AsmInstr.createNOP();
						it.add(inst); 
					}
					inst = AsmInstr.createNOP();
					lev0.addInst(inst);
					it.add(inst);
					
					_spu.conf.rptCntWidth0 = CHUNKWIDTH;
				}

				if (rem < 1) {
					for (int j = 0; j < rem; j++)
						it.add(AsmInstr.createNOP());
				} else {
					_curRPTSeg = new RPTSegment();
					_rptSegs.add(_curRPTSeg);
					
					RPTLevel lev0 = new RPTLevel(_curRPTSeg, 0);
					_curRPTSeg.levels.add(lev0);
					
					lev0.cntNum = rem;
					
					AsmInstr inst = AsmInstr.createRPT(1, rem);
					it.add(inst);
					
					inst.rptInfo = lev0;
					
					// This is the delay slot
					for (int j = 0; j < _spu.conf.RPTOverhead(); j++) {
						inst = AsmInstr.createNOP();
						it.add(inst);
					}
					inst = AsmInstr.createNOP();					
					lev0.addInst(inst);
					it.add(inst);
					
					_spu.conf.rptCntWidth0 = Math.max(_spu.conf.rptCntWidth0, SWGenUtils.getAddressWidth(rem));
				}
			}			
		}
		
		// Set RPT part in SPU configuration
		if (rptNOP) {
			if (!_spu.conf.rptEn) {
				_spu.conf.rptEn = true;
				_spu.conf.rptSpec1 = true;
				_spu.conf.rptLevels = 1;				
			}
		}
	}
	
	/**
	 * This pass parses the RPT structures and configure corresponding fields.
	 * The most important task is to figure out what the rpt_end is.
	 */
	public void rptParsingPass() {
		if (!_spu.conf.rptEn || _spu.conf.rptSpec1) return;
		
		SPUConfig cf = _spu.conf;
		
		for (RPTSegment seg : _rptSegs) {
			cf.rptLevels = Math.max(cf.rptLevels, seg.levlNum);
			
			for (RPTLevel lev : seg.levels) {
				if (lev.levl == 0) {
					cf.rptCntWidth0 = Math.max(cf.rptCntWidth0, SWGenUtils.getAddressWidth(lev.cntNum));
					int endBits = _findRPTLevEnd(lev);
					cf.rptBlkWidth0 = Math.max(cf.rptBlkWidth0, endBits);
				} else if (lev.levl == 1) {
					cf.rptCntWidth1 = Math.max(cf.rptCntWidth1, SWGenUtils.getAddressWidth(lev.cntNum));
					int endBits = _findRPTLevEnd(lev);
					cf.rptBlkWidth1 = Math.max(cf.rptBlkWidth1, endBits);
				} else if (lev.levl == 2) {
					cf.rptCntWidth2 = Math.max(cf.rptCntWidth2, SWGenUtils.getAddressWidth(lev.cntNum));
					int endBits = _findRPTLevEnd(lev);
					cf.rptBlkWidth2 = Math.max(cf.rptBlkWidth2, endBits);
				} else if (lev.levl == 3) {
					cf.rptCntWidth3 = Math.max(cf.rptCntWidth3, SWGenUtils.getAddressWidth(lev.cntNum));
					int endBits = _findRPTLevEnd(lev);
					cf.rptBlkWidth3 = Math.max(cf.rptBlkWidth3, endBits);
				} else if (lev.levl == 4) {
					cf.rptCntWidth4 = Math.max(cf.rptCntWidth4, SWGenUtils.getAddressWidth(lev.cntNum));
					int endBits = _findRPTLevEnd(lev);
					cf.rptBlkWidth4 = Math.max(cf.rptBlkWidth4, endBits);
				}
			}
		}
		
		// After all segments are parsed, the end width info is known. Only now we can set the endLoc
		// value.
		for (RPTSegment seg : _rptSegs) {			
			for (RPTLevel lev : seg.levels) {
				if (lev.levl == 0) {
					AsmInstr endI = lev.insts.getLast();
					String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
					lev.endLoc = Integer.parseInt(endIBits.substring(9 - cf.rptBlkWidth0), 2);
				} else if (lev.levl == 1) {
					AsmInstr endI = lev.insts.getLast();
					String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
					lev.endLoc = Integer.parseInt(endIBits.substring(9 - cf.rptBlkWidth1), 2);
				} else if (lev.levl == 2) {
					AsmInstr endI = lev.insts.getLast();
					String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
					lev.endLoc = Integer.parseInt(endIBits.substring(9 - cf.rptBlkWidth2), 2);
				} else if (lev.levl == 3) {
					AsmInstr endI = lev.insts.getLast();
					String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
					lev.endLoc = Integer.parseInt(endIBits.substring(9 - cf.rptBlkWidth3), 2);
				} else if (lev.levl == 4) {
					AsmInstr endI = lev.insts.getLast();
					String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
					lev.endLoc = Integer.parseInt(endIBits.substring(9 - cf.rptBlkWidth4), 2);
				}
			}
		}		
		
		// TODO: Check if rptSpec1 should be set here 
	}
	
	public void populateInstTypes() {
		for (AsmInstr I : asmInstrs) {
			instTypes.add(I.instName);
		}
	}
	///////////////////////////////////////////////////////////////////////////
	//                          private methods                              //

	private AsmInstr _fitNewInstr(String line) {		
		SPUConfig cf = _spu.conf;
		
		AsmInstr inst;
		if (_rptOn)
			inst = new RptedInst(line);
		else
			inst = new AsmInstr( line);
		
		if (inst.instName == SPUInst.JMP) {
			cf.jmpEn = true;
		} else if (inst.instName == SPUInst.RPT) {
			cf.rptEn = true;
		} else if (inst.isMASK()) {
			cf.maskEn = true;
			if (inst.funcName.equals("SETMASKEQ"))
				cf.maskeqEn = true;
			else if (inst.funcName.equals("SETMASKGT"))
				cf.maskgtEn = true;
			else if (inst.funcName.equals("SETMASKLT"))
				cf.maskltEn = true;
			_maskOn = true;
		} else if (inst.instName == SPUInst.MASKEND) {
			_maskOn = false;
			inst = null;
		} else if (inst.isALUSRA1()) {
			cf.alusra1En = true;
		} else if (inst.isABSDIFF()) {
			cf.absdiffEn = true;
			if (cf.absdiffType == 1 || cf.absdiffType == 0)
				cf.Pa1xDepth = 1;
		} else if (inst.instName == SPUInst.RPT) {
			cf.rptEn = true;
		} else if (inst.instName == SPUInst.GET_IXFX) {
			cf.getiEn = true;
		} 
		// DM set, inc, init, autoincsize, size
		else if (inst.instName == SPUInst.SETDMRB_0) {			
			cf.dmRBSetEnB0 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.SETDMRB_1) {
			cf.dmRBSetEnB1 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.SETDMRB_2) {
			cf.dmRBSetEnB2 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.SETDMRB_C0) {
			cf.dmRBSetEnC0 = true;
			_spu.conf.dmDirectEn = false;
		}else if (inst.instName == SPUInst.SETDMWB_0) {
			cf.dmWBSetEn = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.INCDMRB_0) {
			cf.dmRBIncEnB0 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.INCDMRB_1) {
			cf.dmRBIncEnB1 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.INCDMRB_2) {
			cf.dmRBIncEnB2 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.INCDMRB_C0) {
			cf.dmRBIncEnC0 = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.INCDMWB_0) {
			cf.dmWBIncEn = true;
			_spu.conf.dmDirectEn = false;
		} else if (inst.instName == SPUInst.SETDMRBINIT_0) {
			cf.dmRBInitialB0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBINIT_1) {
			cf.dmRBInitialB1 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBINIT_2) {
			cf.dmRBInitialB2 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBINIT_C0) {
			cf.dmRBInitialC0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMWBINIT_0) {
			cf.dmWBInitial = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBAUTOINCSIZE_0) {
			cf.dmRBAutoincSizeB0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBAUTOINCSIZE_1) {
			cf.dmRBAutoincSizeB1 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBAUTOINCSIZE_2) {
			cf.dmRBAutoincSizeB2 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMRBAUTOINCSIZE_C0) {
			cf.dmRBAutoincSizeC0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMWBAUTOINCSIZE_0) {
			cf.dmWBAutoincSize = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETDMSIZE) {
			// When manual setting DMSize happens, the programmers take care about memory
			// use, and compiler will not optimise on memory, so disable DMFolding pass.
			cf.dmSize = Integer.parseInt(inst.getOperand(0).str);
			setDMParamters();
			skipDMFoldingPass = true;
			inst = null;
		} 
		// SM set, inc, autoincsize, size
		else if (inst.instName == SPUInst.SETSMRB_0) {			
			cf.smRBSetEn0 = true;
			_spu.conf.smDirectEn = false;
		} else if (inst.instName == SPUInst.INCSMRB_0) {
			cf.smRBIncEn0 = true;
			_spu.conf.smDirectEn = false;
		} else if (inst.instName == SPUInst.INCSMWB_0) {
			cf.smWBIncEn0 = true;
			_spu.conf.smDirectEn = false;
		} else if (inst.instName == SPUInst.SETSMRBAUTOINCSIZE_0) {
			cf.smRBAutoincSize0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETSMWBAUTOINCSIZE_0) {
			cf.smWBAutoincSize0 = Integer.parseInt(inst.getOperand(0).str);
			inst = null;
		} else if (inst.instName == SPUInst.SETSMSIZE) {			
			cf.smSize = Integer.parseInt(inst.getOperand(0).str);
			throw new RuntimeException("ERROR: Haven't finished SETSMSIZE!");
		} 
		else if (inst.instName == SPUInst.SETREGVALUE) {
			for (PE pe:_spu.PEs)
				pe.rf.setValue(SWGenUtils.getDigits(inst.getOperand(0).str), Integer.parseInt(inst.getOperand(1).str));
			cf.rfInitEn = true;
			inst = null;
		} else if (inst.instName == SPUInst.SETREGVALUE_ID) {
			for (PE pe:_spu.PEs)
				pe.rf.setValue(SWGenUtils.getDigits(inst.getOperand(0).str), pe.idx);
			cf.rfInitEn = true;
			inst = null;
		} 
		// EM inc, init, autoincsize
		else if (_spu.isIOCore) {
			if (inst.instName == SPUInst.INCEMRB_0) {
				cf.emRBIncEn0 = true;
			} else if (inst.instName == SPUInst.INCEMRB_1) {
				cf.emRBIncEn1 = true;
			} else if (inst.instName == SPUInst.INCEMWB_0) {
				cf.emWBIncEn0 = true;
			} else if (inst.instName == SPUInst.SETEMRBINIT_0) {
				cf.emRBInitial0 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETEMRBINIT_1) {
				cf.emRBInitial1 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETEMWBINIT_0) {
				cf.emWBInitial0 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETEMRBAUTOINCSIZE_0) {
				cf.emRBAutoincSize0 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETEMRBAUTOINCSIZE_1) {
				cf.emRBAutoincSize1 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETEMWBAUTOINCSIZE_0) {
				cf.emWBAutoincSize0 = Integer.parseInt(inst.getOperand(0).str);
				inst = null;
			} else if (inst.instName == SPUInst.SETINFIFODEPTH) {
				PE ioPE = _spu.PEs.get(0);
				for (FIFO ofifo : ioPE.outputFIFOs) {
					ofifo.setExInFIFODepth(Integer.parseInt(inst.getOperand(0).str));
				}
				inst = null;
			} else if (inst.instName == SPUInst.SETOUTFIFODEPTH) {
				PE ioPE = _spu.PEs.get(0);
				for (FIFO ififo : ioPE.inputFIFOs) {
					ififo.setExOutFIFODepth(Integer.parseInt(inst.getOperand(0).str));
				}
				inst = null;
			}
		}
		
		// Instruction equal to null is used as compiler directives.
		if (inst == null) return inst;
		
		if (inst.rdDM0) {
			cf.dmEn = true;
			cf.dmRBNum0 = Math.max(inst.dmRdOprd0.dmSPIdx+1, cf.dmRBNum0);
			if (!cf.dmRBAutoincEnB0 && inst.dmRdOprd0.dmSPIdx == 0) {
				cf.dmRBAutoincEnB0 = inst.dmRdOprd0.dmSPAutoinc;
				_spu.conf.dmDirectEn = false;
			} else if (!cf.dmRBAutoincEnB1 && inst.dmRdOprd0.dmSPIdx == 1) {
				cf.dmRBAutoincEnB1 = inst.dmRdOprd0.dmSPAutoinc;
				_spu.conf.dmDirectEn = false;
			} else if (!cf.dmRBAutoincEnB2 && inst.dmRdOprd0.dmSPIdx == 2) {
				cf.dmRBAutoincEnB2 = inst.dmRdOprd0.dmSPAutoinc;
				_spu.conf.dmDirectEn = false;
			}
			
			if (!cf.dmOffsetEn) {
				cf.dmOffsetEn = (inst.dmRdOprd0.dmSPOfs != 0);
				if (cf.dmOffsetEn && (cf.dmRBNum0 > 1 || cf.dmRBIncEnB0 || cf.dmRBAutoincEnB0)) 
					throw new RuntimeException("DM offset is only supported when" +"in most basic mode");
			}
		}
		
		if (inst.rdDM1) {
			cf.dmEn = true;
			cf.dmRBNum1 = Math.max(inst.dmRdOprd1.dmSPIdx+1, cf.dmRBNum1);
			// Only support one pointer for DM port1.
			assert inst.dmRdOprd1.dmSPIdx == 0;
			if (!cf.dmRBAutoincEnC0 && inst.dmRdOprd1.dmSPIdx == 0) {
				cf.dmRBAutoincEnC0 = inst.dmRdOprd1.dmSPAutoinc;
				_spu.conf.dmDirectEn = false;
			}
		}
		
		if (inst.wrDM) {
			cf.dmEn = true;
			if (!cf.dmWBAutoincEn) {
				cf.dmWBAutoincEn = inst.dmWrOprd.dmSPAutoinc;
			}
		}
		
		if (inst.wrSM) {
			cf.smEn = true;
			if (!cf.smWBAutoincEn0)
				cf.smWBAutoincEn0 = inst.smWrOprd.smSPAutoinc;
		}
		
		if (inst.rdSM) {
			cf.smEn = true;
			if (!cf.smRBAutoincEn0)
				cf.smRBAutoincEn0 = inst.smRdOprd.smSPAutoinc;
		}
		
		
		if (inst.instName == SPUInst.LDEXMEM) {
			cf.emRBNum = Math.max(inst.oprds.get(0).emSPIdx+1, cf.emRBNum);
		} else if (inst.instName == SPUInst.STEXMEM) {
			// EMWB number is always 1 now
		}
		
		if (_maskOn) {
			inst.masked = true;
		}
		
		// RPT segment parse
		if (!_rptOn && inst.instName == SPUInst.RPT) {
			_cntRPTLev = 0;
			
			_curRPTSeg = new RPTSegment();
			_rptSegs.add(_curRPTSeg);
			
			RPTLevel lev0 = new RPTLevel(_curRPTSeg, 0);
			_curRPTSeg.levels.add(lev0);
			lev0.cntNum = Integer.parseInt(inst.getOperand(0).str);
			inst.rptInfo = lev0;
			
			if (_spu.conf.RPTOverhead() > 0)
				_rptOverheadStage = true;
		} else if (_rptOverheadStage) {
			_cntRPTOverhead ++;
			if (_cntRPTOverhead == _spu.conf.RPTOverhead()) {
				_cntRPTOverhead = 0;
				_rptOverheadStage = false;
				_rptOn = true;
			}
			
			if (_cntRPTLev > 0) {
				_curRPTSeg.levels.getLast().predLevel.addInst(inst);	
			}
		} else if (_rptOn && inst.instName == SPUInst.RPT) {
			// See another RPT
			_cntRPTLev ++;
			assert _cntRPTLev <= 5;
			
			// Set total level depth
			_curRPTSeg.levlNum = Math.max(_cntRPTLev+1, _curRPTSeg.levlNum);
			
			RPTLevel lev = new RPTLevel(_curRPTSeg, _cntRPTLev);
			_curRPTSeg.levels.add(lev);
			lev.cntNum = Integer.parseInt(inst.getOperand(0).str);
			inst.rptInfo = lev;
			
			// Get immediate predecessor, RPT creates a new level, but itself belongs to a lower level.
			// The way to get the immediate successor: search from last level until we find a level
			// which has lower level index.
			RPTLevel predecessorLev = null;
			ListIterator<RPTLevel> it = _curRPTSeg.levels.listIterator(_curRPTSeg.levels.size());
			while (it.hasPrevious()) {
				RPTLevel preLev = it.previous();
				if (preLev.levl >= lev.levl)
					continue;
				else {
					predecessorLev = preLev;
					break;
				}
			}
			predecessorLev.addInst(inst);
			inst.rptLev.addSuccLev(lev);
			
			if (_spu.conf.RPTOverhead() > 0)
				_rptOverheadStage = true;
		} else if (_rptOn) {
			if (inst.instName == SPUInst.RPTEND) {
				if (_cntRPTLev == 0) {
					_rptOn = false;
					return null;
				}
				_cntRPTLev --;
				return null;
			} else {
				// Retrieve the right repeat level with index of _cntRPTLev
				RPTLevel lev = null;
				ListIterator<RPTLevel> it = _curRPTSeg.levels.listIterator(_curRPTSeg.levels.size());
				while (it.hasPrevious()) {
					RPTLevel preLev = it.previous();
					if (preLev.levl == _cntRPTLev) {
						lev = preLev;
						break;
					}						
				}
				lev.addInst(inst);
			}
		}
		
		return inst;
	}
		
	
	/**
	 * Return true if this NOP is unneeded. Note the case where NOP is 
	 * in a repeat block.
	 * @param idxNOP The index of the NOP
	 * @return
	 */
	private boolean _isNOPUnneeded(int idxNOP) {
		if (asmInstrs.get(idxNOP) instanceof RptedInst)
			return false;
		
		// The possible range is DEPTH instructions before NOP and DEPTH
		// instructions after NOP. Check b(D) with a(1), b(D-1) with a(2)
		// and so on, total DEPTH checks.
		boolean hazard = false;
		for (int i = 0; i < PDEPTH; i++) {
			if (_hasHazard(idxNOP - PDEPTH + i, idxNOP + i + 1)) {
				hazard = true;
				break;
			}
		}
		return !hazard;
	}
	
	/** 
	 * Recompute DM size by searching DM offset index.
	 * TODO: this is not valid when there is autoincrement.
	 */
	private void _computeDMSize() {		
		SPUConfig conf = _spu.conf;
		if (!conf.dmEn) 
			return;
		
		// Recompute starts ...			
		conf.dmSize = 0;
								
		for (ListIterator<AsmInstr> it = asmInstrs.listIterator(); it.hasNext();) {
			AsmInstr I = it.next();
			
			if (I.wrDM) {
				Operand def = I.dmWrOprd;
				int memAddr = def.dmSPOfs;	
				conf.dmSize = (memAddr > conf.dmSize)? memAddr : conf.dmSize;				
			}
			
			if (I.rdDM0) {
				Operand mem = I.dmRdOprd0;
				int memAddr = mem.dmSPOfs;
				conf.dmSize = (memAddr > conf.dmSize)? memAddr : conf.dmSize;
			}
		}
		// Above is address, the size is largest address + 1
		conf.dmSize ++;
		
		setDMParamters();
	}
	
	public void setDMParamters() {
		SPUConfig cf = _spu.conf;
		
		// Recompute dmWidth, dmOffsetWidth
		cf.dmWidth = SWGenUtils.getAddressWidth(cf.dmSize);
		
		if (cf.dmWidth <= cf.regWidth) {
			if (cf.dmSize <= 32)
				cf.dmSize = 32;
			else
				cf.dmSize = 64;
			cf.dmOffsetWidth = cf.dmWidth;
		} else {
			// the offset width is constrained to be maximum 8 bits
			// for RF=32, and 6 bits for RF=64
			if (cf.regWidth == 5 && cf.dmWidth > 8) {
				cf.dmOffsetWidth = 8;
			} else if (cf.regWidth == 6 && cf.dmWidth > 6) {
				cf.dmOffsetWidth = 6;
			} else {
				cf.dmOffsetWidth = cf.dmWidth;
			}
		}
	}
	
	/**
	 * Clean up unneeded NOPs due to advance of I instruction and falling of
	 * Other instructions. Check the PDEPTH instructions after I and before T,
	 * and remove unneeded NOPs.
	 * 
	 * Iterate backward is not easy. Firstly, the iterator must iterate to T, 
	 * which means the correct number of calling previous() must be known. So 
	 * T instruction provides such information.
	 * 
	 * @param it Iterator pointing before I + 1
	 * @param T Instruction T, used to get the index.
	 */
	private void _postConvClean(ListIterator<AsmInstr> it, AsmInstr T) {
		// At the beginning, iterator is between I + 1 and new inserted NOPs if
		// any.
		
		// Record the move of iterator to recover it after cleansing
		int steps = 0;
		
		int idxCur = it.previousIndex();
		int idxT   = asmInstrs.indexOf(T);
		int back = idxCur - idxT + 1;
		
		for (int i = 0; i < back; i++) {
			it.previous();
		}
		// Now it is between T-1 and T
		
		// Loop backward to check NOPs
		for (int i=0; it.hasPrevious() && i < PDEPTH; i++) {
			AsmInstr ins = it.previous();
			steps ++;
			
			if (ins.instName == SPUInst.NOP) {
				if (_isNOPUnneeded(it.nextIndex())) {					
					it.remove();
					steps --;
				}
			}
		}
		
		// Recover iterator
		for (int i = 0; i < steps + back; i++) {
			it.next();
		}			
		
		steps = 0;
		
		for (int i=0; it.hasNext() && i < PDEPTH; i++) {
			AsmInstr ins = it.next();
			steps ++;
			
			if (ins.instName == SPUInst.NOP) {
				if (_isNOPUnneeded(it.previousIndex())) {
					it.previous();
					it.remove();
					steps --;
				}				
			}
		}
		
		// Recover iterator
		for (int i = 0; i < steps; i++) {
			it.previous();
		}
	}
	
	/**
	 * Return true when this line is a valid instruction.
	 * 
	 * @param inst
	 * @return
	 */
	private boolean _validInstr(String inst) {		
		return SPUInstGeneralSet.contains(inst);
	}

	/**
	 * When an immediate instruction is encountered, translate it into shared
	 * memory instruction.
	 * 
	 * @param instr
	 * @param im The shared memory to operate on
	 * @param base The current base pointer of shared memory
	 * @return The new base pointer of shared memory
	 */
	private int _fillInSM(ListIterator<AsmInstr> it, AsmInstr instr, SharedMem im, int base) {		
		SPUConfig conf = _spu.conf;		

		float imm = new Float(instr.smRdOprd.imVal);
		int fiximm;
		if (conf.coreType == ALUTYPE.REAL16B1D) 
			fiximm = SWGenUtils.float2fix(imm, conf.CoreDataWidth(), _ssp.conf.fracBits);
		else {
			// For complex datapath, float data has already been converted to
			// fixed-point and real and imag parts are packed.
			assert (int)imm == imm;
			fiximm = (int)imm;
		}
		
		// The index of immediate in IM
		int idx;
		boolean toReverse = false;
		if (im.fixedImms.contains(fiximm)) {
			idx = im.fixedImms.indexOf(fiximm);
		} else {
			Integer invfiximm = SWGenUtils.float2fix(-1 * imm,
					conf.CoreDataWidth(), _ssp.conf.fracBits);
			if (im.fixedImms.contains(invfiximm)) {
				idx = im.fixedImms.indexOf(invfiximm);
				toReverse = true;
			} else {
				idx = im.fixedImms.size();
				im.fixedImms.add(fiximm);
				
				// Update immOffsetWidth
				// Here is a difficulty, when both DM and SM need extra addressing bits,
				// how to allocate the resources. Currently, SM can only use its REGWIDTH
				// bits, no extra addressing bits.
				int width = SWGenUtils.getAddressWidth(im.fixedImms.size());
				if (width > conf.smOffsetWidth && 
						conf.smOffsetWidth < conf.regWidth) {
					conf.smOffsetWidth = width;
				}
			}
		}

		// Update base pointer
		int offsetableSize = (int) Math.pow(2, conf.smOffsetWidth);
		int newBase = idx / offsetableSize;
		if (newBase != base) {
			conf.smDirectEn = false;
			conf.smRBSetEn0 = true;
			// NOTE: this may cause bug, but for Read-only SM, this normally means it needs
			// to update base address.
			conf.smOffsetEn = true;
			AsmInstr setsmrb = AsmInstr.createSETSMRB(newBase);
			it.previous();
			it.add(setsmrb);
			it.next();
		}

		instr.convToSMInstr(idx % offsetableSize, toReverse);

		return newBase;
	}

	/**
	 * Get the memory address from the GET_CONST_PORT instruction string.
	 * 
	 * @param line The instruction string
	 * @return
	 */
	private int _getMemAddr(String line) {
		return Integer.parseInt(line.substring(line.indexOf("&") + 1,
				line.indexOf(",")));
	}

	/**
	 * Return true if src can be forwarded
	 * 
	 * @param src The def instruction
	 * @param sink The use instruction
	 * @return
	 */
	private boolean _canBeFwdPair(AsmInstr src, AsmInstr sink) {
		if (!_FWDDefInsts.contains(src.instName) || !_FWDUseInsts.contains(sink.instName))
			return false;
		
		// Note a special case, PUTFWD and PUTFWDM, find the right define.
		String def;
		String use;
		
		def = _getFwdDefOperand(src);
		
		use = _getFwdUseOperand(sink);
		
		if (!def.equals(use))
			return false;
				
		if (sink.instName != SPUInst.PUT_FRRR && sink.instName != SPUInst.PUT_FRMR) {
			if (_spu.conf.coreType == ALUTYPE.CPLX16B4D) {
				// For complex 4 slice, only PUT,ADD and SUB can be forwarded.
				if (!sink.isADD() && !sink.isSUB())
					return false;
			}
			
			// When the forward use also appears as part of the 'mul', it can not
			// be forwarded. E.g. ADDMUL R2, ONE, R1, R1
			String use1, use2;
			use1 = sink.getOperand(1).str;
			use2 = sink.getOperand(2).str;
			if (use1.equals(use) || use2.equals(use))
				return false;
		}

		return true;
	}

	/**
	 * Get the forward use operand, i.e. the register to be forwarded.
	 * @param useI
	 * @return
	 */
	private String _getFwdUseOperand(AsmInstr useI) {
		String use;
		if (useI.instName == SPUInst.PUT_FRRR || useI.instName == SPUInst.PUT_FRMR) {
			use = useI.getOperand(0).str;
		} else if (useI.instrStr.contains("ABSDIFF")) {
			use = useI.getOperand(2).str;
		} else {
			use = useI.getOperand(3).str;
		}
		return use;
	}
	
	/**
	 * Get the forward def operand, i.e. the register to be forwarded.
	 * @param useI
	 * @return
	 */
	private String _getFwdDefOperand(AsmInstr defI) {
		String def;
		if (defI.instName == SPUInst.PUTFWD_FRRX) {
			def = asmInstrs.get(asmInstrs.indexOf(defI)-1).getOperand(0).str;
		} else {
			def = defI.getOperand(0).str;
		}
		return def;
	}
	
	/**
	 * Check backward to find hazard and record the index if found.
	 * 
	 * @param idxT The index of the target instruction to check
	 * @param idxS The start index of the instruction to check against
	 * @param cnt The number of instructions to check against
	 * @return The index of hazard instruction. Return -1 if there is no hazard.
	 */
//	private int _checkCostBackward(int idxT, int idxS, int cnt) {
//		if (idxT < 0 || idxT >= asmInstrs.size() || idxS < 0
//				|| idxS >= asmInstrs.size())
//			return -1;
//
//		// Note iterS is at index idxS+1, so that iterator.previous() can
//		// retrieve the instruction S.
//		ListIterator<AsmInstr> iterS = asmInstrs.listIterator(idxS + 1);
//		AsmInstr T = asmInstrs.get(idxT);
//
//		for (int idx = 0; iterS.hasPrevious() && idx < cnt; idx++) {
//			AsmInstr S = iterS.previous();
//			if (_hasHazard(S, T)) {
//				return idx;
//			}
//		}
//
//		return -1;
//	}

	/**
	 * Check backward to find hazard and record the index if found. It includes a mask
	 * to exclude checking a certain use. This is useful, for example, in forward conversion,
	 * the to-be-forwarded register should not be checked again against instructions before 
	 * forward def instruction.
	 * 
	 * 1. add R0, R1, R2
	 * 2. subfwd Rx, R2
	 * 3. add R0, R2, R3 -- forward define
	 * 4. addmul Rx, R2, R3, R0 -- forward use
	 * 
	 * Here, R0 should not be checked against (1)(2), so R0 is set as a mask.
	 * 
	 * @param idxT The index of the target instruction to check
	 * @param idxS The start index of the instruction to check against
	 * @param cnt The number of instructions to check against
	 * @param fwdDef The mask operand should not be checked
	 * @return The index of hazard instruction. Return -1 if there is no hazard.
	 */
	private int _checkCostBackwardWithMask(int idxT, int idxS, int cnt, String fwdDef) {
		if (idxT < 0 || idxT >= asmInstrs.size() || idxS < 0
				|| idxS >= asmInstrs.size())
			return -1;

		// Note iterS is at index idxS+1, so that iterator.previous() can
		// retrieve the instruction S.
		ListIterator<AsmInstr> iterS = asmInstrs.listIterator(idxS + 1);
		AsmInstr T = asmInstrs.get(idxT);

		for (int idx = 0; iterS.hasPrevious() && idx < cnt; idx++) {
			AsmInstr S = iterS.previous();
						
			if (!_neverProduceHazards.contains(S.instName) && S.getOperand(0).equals(fwdDef)) 
				continue;
			
			if (_hasHazard(S, T)) {
				return idx;
			}
		}

		return -1;
	}
	
	/**
	 * Check forward to find hazard and record the index if found.
	 * 
	 * @param idxT The index of the target instruction to check
	 * @param idxS The start index of the instruction to check against
	 * @param cnt The number of instructions to check against
	 * @return The index of hazard instruction. Return -1 if there is no hazard.
	 */
	private int _checkCostForward(int idxT, int idxS, int cnt) {
		if (idxT < 0 || idxT >= asmInstrs.size() || idxS < 0
				|| idxS >= asmInstrs.size())
			return -1;

		ListIterator<AsmInstr> iterS = asmInstrs.listIterator(idxS);
		AsmInstr T = asmInstrs.get(idxT);

		for (int idx = 0; iterS.hasNext() && idx < cnt; idx++) {
			AsmInstr S = iterS.next();
			if (_hasHazard(T, S)) {
				return idx;
			}
		}

		return -1;
	}
	
	/**
	 * Check if an instruction will cause hazard when it is inserted after the
	 * check-against instruction.
	 * 
	 * @param sink The instruction to check
	 * @param src The instruction to check against
	 * @return
	 */
	private boolean _hasHazard(AsmInstr src, AsmInstr sink) {
		if (_neverProduceHazards.contains(src.instName))
			return false;
		if (_neverHaveHazards.contains(sink.instName))
			return false;				
		// When there is no define operand, of course no hazard.
		if (src.defOprd == null)
			return false;
		
		// Check every use with the def
		String def = src.defOprd.str;
		for (Operand use : sink.useOprds) {
			if (def.equals(use.str))
				return true;
		}
		return false;
	}

	/**
	 * The index version of hazard check. It firstly uses index to fetch
	 * instruction and then call the instruction version.
	 * 
	 * @param idxUse
	 * @param idxDef
	 * @return
	 */
	private boolean _hasHazard(int idxDef, int idxUse) {
		if (idxUse < 0 || idxUse >= asmInstrs.size() || idxDef < 0
				|| idxDef >= asmInstrs.size())
			return false;
		AsmInstr use = asmInstrs.get(idxUse);
		AsmInstr def = asmInstrs.get(idxDef);

		return _hasHazard(def, use);
	}
	
	/**
	 * Find the RPT end width and value for the specified level.
	 * @param lev
	 * @return
	 */
	private int _findRPTLevEnd(RPTLevel lev) {
		int difIdx = 0;
		LinkedList<AsmInstr> work = lev.insts;
		
		AsmInstr endI = work.getLast();
		String endIBits = SWGenUtils.intToBinary(asmInstrs.indexOf(endI), 10);
		
		for (AsmInstr I : lev.insts) {
			if (I == endI) break;
			
			String bits = SWGenUtils.intToBinary(asmInstrs.indexOf(I), 10);
			for (int i = 0; i < bits.length(); i++) {
				if (bits.charAt(9-i) != endIBits.charAt(9-i)) {
					difIdx = Math.max(difIdx, i);
					break;
				}
			}
		}		
		return difIdx+1;
	}
	
	///////////////////////////////////////////////////////////////////
	////                  public variables                         ////

	public boolean skipPUTFoldingPass = false;
	public boolean skipRPTNopsPass = false;
	public boolean skipDMFoldingPass = false;
	public boolean skipInsertDMBaseSetPass = false;
	public boolean skipRemoveUnneededNOPsPass = false;
	public boolean skipFWDConvertPass = false;
	public boolean skipIMMToSMPass = false;
	
	// Temporary variables
	public int foldedPUTNum = 0;
	
	/* Loop start cycle and length before synchronization */
	public int loopBegin = 0;
	public int loopLen = 0;

	/* Loop start cycle and length after synchronization */
	public int loopBeginSynced = 0;
	public int loopLenSynced = 0;

	/* The nops inserted outside loop body as the pipeline overhead */
	public int pipelineNOPs = 0;

	/** List of FIFO instructions */
	public List<FIFOInstr> fifoInstrs = new LinkedList<FIFOInstr>();

	/** List of leading GETs */
	public List<FIFOInstr> leadingGETs = new LinkedList<FIFOInstr>();

	public LinkedList<AsmInstr> asmInstrs = new LinkedList<AsmInstr>();

	/** List of inter-PE GET instructions */
	public List<FIFOInstr> getInstrs = new LinkedList<FIFOInstr>();

	/**
	 * Copy of GET instructions for synchronisation use. The list can be changed
	 * during synchronisation and will be emptied at the end of synchronisation.
	 */
	public List<FIFOInstr> copyOfGetInstrs;

	/** List of inter-PE PUT instructions */
	public List<FIFOInstr> putInstrs = new LinkedList<FIFOInstr>();

	/** List of synchronised (need to insert NOPs) inter-PE GET instructions */
	public List<FIFOInstr> syncedInstrs = new LinkedList<FIFOInstr>();

	/**
	 * The instructions to parse. This set neglects the subtypes to indicate operands type. 
	 * @author 40055379
	 *
	 */
	public List<String> SPUInstGeneralSet = Arrays.asList(
	    "ADD", "SUB", "MUL", "ADDMUL", "SUBMUL", "ADDMULFWD", "SUBMULFWD",
		"ADDMULSRA1", "SUBMULSRA1", "ABSDIFF", "ABSDIFFACCUM",
		"ABSDIFFCLR", "ABSDIFFFWD", "NOP", "GET", "PUT", "PUTFWD",
		
		"JMP", "RPT", "CMP", "RPTEND", "MASKEND", "SETMASKEQ", "SETMASKGT", "SETMASKLT",
		
		"SETSMRB_0", "INCSMRB_0", "INCSMWB_0", "SETSMRBAUTOINCSIZE_0", "SETSMWBAUTOINCSIZE_0", "SETSMSIZE",
		
		"SETDMRB_0", "SETDMRB_1", "SETDMRB_2", "SETDMRB_C0", "SETDMWB_0", "SETDMSIZE",
		"INCDMRB_0", "INCDMRB_1", "INCDMRB_2", "INCDMRB_C0", "INCDMWB_0",
		"SETDMRBINIT_0", "SETDMRBINIT_1", "SETDMRBINIT_2", "SETDMRBINIT_C0", "SETDMWBINIT_0",
		"SETDMRBAUTOINCSIZE_0", "SETDMRBAUTOINCSIZE_1", "SETDMRBAUTOINCSIZE_2", "SETDMRBAUTOINCSIZE_C0", "SETDMWBAUTOINCSIZE_0",
		
		"SHIFTCACHELINE", "LDCACHE_BROADCAST", "LDEXMEM", "LDCACHE", "STEXMEM", "STCACHE", "INCEMRB_0", "INCEMRB_1", "INCEMWB_0", "BARRIER",
		"SETEMRBINIT_0", "SETEMRBINIT_1", "SETEMWBINIT_0",		
		"SETEMRBAUTOINCSIZE_0", "SETEMRBAUTOINCSIZE_1", "SETEMWBAUTOINCSIZE_0",
		
		"RESETRXIDX", "RESETTXIDX", "INCRXIDXBY1", "INCTXIDXBY1",
		"SETINFIFODEPTH", "SETOUTFIFODEPTH", "SETREGVALUE",
		
		/*Newly added*/
		"INCDMRB_ALL", "MOV", "SETREGVALUE_ID",
		
		/* Have not implemented yet*/
		"DECONST", "SLT", "SGT", "LDSORT", "SORT", "UNLDSORT", "DIV", "SQRT"
	);
	
	/**
	 * All SPU instructions, including both native and artificial ones.
	 * 
	 */
	public enum SPUInst {
		ADDMUL_RRRR, ADDMUL_RRIR, ADDMUL_RRMR, ADDMUL_MRRR, ADDMUL_MRIR, ADDMUL_MRMR, 
		ADDMUL_FRRR, ADDMUL_FRIR, ADDMUL_FRMR, ADDMUL_RRMM, ADDMUL_MIMR, 

		SUBMUL_RRRR, SUBMUL_RRIR, SUBMUL_RRMR, SUBMUL_MRRR, SUBMUL_MRIR, SUBMUL_MRMR, 
		SUBMUL_FRRR, SUBMUL_FRIR, SUBMUL_FRMR, 

		ADDMULFWD_RRRX, ADDMULFWD_RRIX, ADDMULFWD_RRMX, ADDMULFWD_MRRX, ADDMULFWD_MRIX, 
		ADDMULFWD_MRMX, ADDMULFWD_FRRX, ADDMULFWD_FRIX, ADDMULFWD_FRMX, ADDMULFWD_MIMX,

		SUBMULFWD_RRRX, SUBMULFWD_RRIX, SUBMULFWD_RRMX, SUBMULFWD_MRRX, SUBMULFWD_MRIX, 
		SUBMULFWD_MMRX, SUBMULFWD_FRRX, SUBMULFWD_FRIX, SUBMULFWD_FRMX, SUBMULFWD_MIMX,

		ADDMULSRA1_RRRR, ADDMULSRA1_RRIR, ADDMULSRA1_RRMR, ADDMULSRA1_MRRR, ADDMULSRA1_MRIR, 
		ADDMULSRA1_MRMR, ADDMULSRA1_FRRR, ADDMULSRA1_FRIR, ADDMULSRA1_FRMR, 
		
		SUBMULSRA1_RRRR, SUBMULSRA1_RRIR, SUBMULSRA1_RRMR, SUBMULSRA1_MRRR, SUBMULSRA1_MRIR, 
		SUBMULSRA1_MRMR, SUBMULSRA1_FRRR, SUBMULSRA1_FRIR, SUBMULSRA1_FRMR, 
		
	    ABSDIFF_RRRR, ABSDIFF_RRIR, ABSDIFF_RRMR, ABSDIFF_MRRR, ABSDIFF_MRIR, ABSDIFF_MRMR, 
		ABSDIFF_FRRR, ABSDIFF_FRIR, ABSDIFF_FRMR, ABSDIFF_RRMM, ABSDIFFFWD_RRRX, ABSDIFFACCUM_RXRR, 
		ABSDIFFACCUM_RXMM, ABSDIFFCLR,
		
		NOP, GET_RXFX, PUT_FRRR, PUTFWD_FRRX, GET_MXFX, GET_IXFX, PUT_FRMR,
		RPT, RPTEND, CMP_XXRR, CMP_XXMR, JMP,
		SETMASKEQ_XRRR, SETMASKGT_XRRR, SETMASKLT_XRRR, MASKEND, 
		
		SETSMRB_0, INCSMRB_0, INCSMWB_0, SETSMRBAUTOINCSIZE_0,SETSMWBAUTOINCSIZE_0, SETSMSIZE,
		
		SETDMRB_0, SETDMRB_1, SETDMRB_2, SETDMRB_C0, SETDMWB_0, SETDMSIZE,
		INCDMRB_0, INCDMRB_1, INCDMRB_2, INCDMRB_C0, INCDMWB_0, 
		SETDMRBINIT_0, SETDMRBINIT_1, SETDMRBINIT_2, SETDMRBINIT_C0, SETDMWBINIT_0,		
		SETDMRBAUTOINCSIZE_0, SETDMRBAUTOINCSIZE_1, SETDMRBAUTOINCSIZE_2, SETDMRBAUTOINCSIZE_C0, SETDMWBAUTOINCSIZE_0,
		
		SHIFTCACHELINE, LDCACHE_BROADCAST, LDEXMEM, LDCACHE, STEXMEM, STCACHE, INCEMRB_0, INCEMRB_1, INCEMWB_0, BARRIER,
		SETEMRBINIT_0, SETEMRBINIT_1, SETEMWBINIT_0,		
		SETEMRBAUTOINCSIZE_0, SETEMRBAUTOINCSIZE_1, SETEMWBAUTOINCSIZE_0,
		
		RESETRXIDX, RESETTXIDX, INCRXIDXBY1, INCTXIDXBY1,
		SETINFIFODEPTH, SETOUTFIFODEPTH, SETREGVALUE,
		
		/*Newly added*/
		INCDMRB_ALL, ABSDIFFACCUM_XXMM, ABSDIFFACCUM_MXMM, ABSDIFFACCUM_FXMM, SETREGVALUE_ID, SETMASKLT_XRMR,
		
		/* Have not implemented yet*/
		DECONST_RXRX, DECONST_MXRX, DECONST_RXMX,
		SLT_RRRR, SLT_RRIR, SGT_RRRR, SGT_RRIR, LDSORT_XXRX, SORT, UNLDSORT_RXXX, DIV_RXRR, SQRT_RXRR;
		
		public static boolean contains(String str) { 			 
		    for (SPUInst c : SPUInst.values()) { 
		        if (c.name().equals(str)) { 
		            return true; 
		        } 
		    } 		 
		    return false; 
		} 
	}

	/** Store detected instructions **/
	public EnumSet<SPUInst> instTypes = EnumSet.noneOf(SPUInst.class);
	
	//////////////////////////////////////////////////////////////////
	//                          private variables                   //

	/**
	 *  Instructions that can be forwarded. These instructions all go through
	 *  DSP48E datapath and writes the P register.
	 */
	private static final List<SPUInst> _FWDDefInsts = Arrays.asList(
		SPUInst.ADDMUL_RRRR, SPUInst.SUBMUL_RRRR, SPUInst.ADDMULFWD_RRRX,  SPUInst.SUBMULFWD_RRRX,
		SPUInst.ADDMUL_RRIR, SPUInst.SUBMUL_RRIR, SPUInst.ADDMULFWD_RRIX, SPUInst.SUBMULFWD_RRIX, 
		SPUInst.ADDMUL_RRMR, SPUInst.SUBMUL_RRMR, SPUInst.ADDMULFWD_RRMX, SPUInst.SUBMULFWD_RRMX,
		SPUInst.ABSDIFF_RRRR, SPUInst.ABSDIFF_RRIR, SPUInst.ABSDIFF_RRMR, SPUInst.ABSDIFFFWD_RRRX
	);
	
	/**
	 * Forward use instructions. These instructions could be converted to 
	 * forward instruction form.
	 */
	private static final List<SPUInst> _FWDUseInsts = Arrays.asList(
		SPUInst.ADDMUL_RRRR, SPUInst.SUBMUL_RRRR, 
		SPUInst.ADDMUL_RRIR, SPUInst.SUBMUL_RRIR,
		SPUInst.ADDMUL_RRMR, SPUInst.SUBMUL_RRMR,
		SPUInst.ADDMUL_MRRR, SPUInst.SUBMUL_MRRR,
		SPUInst.ADDMUL_MRIR, SPUInst.SUBMUL_MRIR,
		SPUInst.ADDMUL_MRMR, SPUInst.SUBMUL_MRMR,
		SPUInst.ADDMUL_FRRR, SPUInst.SUBMUL_FRRR, 
		SPUInst.ADDMUL_FRIR, SPUInst.SUBMUL_FRIR,
		SPUInst.ADDMUL_FRMR, SPUInst.SUBMUL_FRMR,
		SPUInst.PUT_FRRR
	);

	// Instructions that never produce hazards. Note this is not a complete list.
	private static final List<SPUInst> _neverProduceHazards = Arrays.asList(
			SPUInst.SETSMRB_0, 
			SPUInst.SETDMWB_0, SPUInst.SETDMRB_0, SPUInst.SETDMRB_1, SPUInst.SETDMRB_2,
			SPUInst.RPT, SPUInst.JMP, SPUInst.NOP,
			SPUInst.PUT_FRRR,
			SPUInst.PUT_FRMR, SPUInst.PUTFWD_FRRX, 
			SPUInst.ADDMUL_FRRR, SPUInst.SUBMUL_FRRR, SPUInst.ADDMULFWD_FRRX, SPUInst.SUBMULFWD_FRRX,
			SPUInst.ADDMUL_FRIR, SPUInst.SUBMUL_FRIR, SPUInst.ADDMULFWD_FRIX, SPUInst.SUBMULFWD_FRIX,
			SPUInst.ADDMUL_FRMR, SPUInst.SUBMUL_FRMR, SPUInst.ADDMULFWD_FRMX, SPUInst.SUBMULFWD_FRMX,
			SPUInst.ABSDIFF_FRRR, SPUInst.ABSDIFF_FRIR, SPUInst.ABSDIFF_FRMR,
			SPUInst.ADDMULSRA1_FRRR, SPUInst.SUBMULSRA1_FRRR, SPUInst.ADDMULSRA1_FRMR, SPUInst.SUBMULSRA1_FRMR, 
			SPUInst.ADDMULSRA1_FRIR, SPUInst.SUBMULSRA1_FRIR,
			SPUInst.LDSORT_XXRX, SPUInst.SORT
			);

	// Instructions that never have hazards.
	private static final List<SPUInst> _neverHaveHazards = Arrays.asList(
			SPUInst.SETSMRB_0, 
			SPUInst.SETDMWB_0, SPUInst.SETDMRB_0, SPUInst.SETDMRB_1, SPUInst.SETDMRB_2,
			
			SPUInst.RPT, SPUInst.JMP, SPUInst.NOP, SPUInst.GET_RXFX,
			SPUInst.GET_MXFX, SPUInst.PUTFWD_FRRX,
			SPUInst.UNLDSORT_RXXX, SPUInst.SORT
			);
	
	private SPU _spu;
	private SSP _ssp;

	// ------------------------------------
	// Help variables, used temporally
	// ------------------------------------
	// For RPT parsing
	private LinkedList<RPTSegment> _rptSegs = new LinkedList<RPTSegment>();
	private boolean _rptOn = false;
	private boolean _rptOverheadStage = false;
	private RPTSegment _curRPTSeg;
	private int _cntRPTOverhead = 0;
	private int _cntRPTLev = 0;
	// For parsing conditional execution
	private boolean _maskOn = false;
	
	
	// Pipeline depth
	private int PDEPTH = 4;
}
