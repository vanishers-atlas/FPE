package sspc.lib;

import java.util.LinkedList;

import sspc.lib.Assembly.SPUInst;

public class AsmInstr {
//	public static void main(String[] args) {
//		
////		boolean test = _isDMOprd("0");
////		System.out.println("Result is " + test);
//		AsmInstr testI = new AsmInstr("SETDMSIZE", "SETDMSIZE -2500");
//		
//		System.out.println("Result is " + testI.instName.name());
//		return;
//	}
	
	public AsmInstr(String origstr) {
		instrStr = origstr;
		// Parse operands and fill in flags
		_parseInst();
	}
	
	public void print() {
		System.out.println(instrStr);
	}		
	
	/**
	 * This function change an operand name to specified one. Note it only changes the instrStr.
	 * In order to reflect the change back to all 'internal' data fields, call reparse() if needed. 
	 * @param oprdStr
	 * @param idx
	 */
	public void changeOperandTo(String oprdStr, int idx) {
		assert idx != -1;
		
		if (idx >= origOprds.size())
			throw new RuntimeException("ERROR: nonexist operand!");
		String[] fields = instrStr.trim().split("\\s+");
		String replace = fields[0]+" ";
		for (int i = 1; i < fields.length; i++) {
			// To avoid misleading string, replace uses leading characters as a guard.
			if (i-1 == idx) {
				replace += oprdStr;
				if (idx != origOprds.size()-1)
					 replace += ", ";
			}
			else {
				replace += fields[i] + " ";
			}
		}
		//System.out.println("From "+instrStr +" to "+replace);
		instrStr = replace;
	}
	
	public void changePutChNoTo(int no) {
		changeOperandTo("^"+no, 1);
		reparseInst();
	}
	
	public void removeLastOperand() {		
		String[] fields = instrStr.trim().replaceAll(",", "").split("\\s+");
		String replace = fields[0]+" ";
		for (int i = 1; i < fields.length-1; i++) {
			replace += fields[i];
			if (i < fields.length-2)
				replace += ", ";
		}
		instrStr = replace;
	}
	
	public void reparseInst() {
		_parseInst();
	}
	
	/**
	 * Convert immediate instruction to shared memory instruction.
	 * 
	 * @param instr
	 * @param idx
	 */
	public void convToSMInstr(int idx, boolean reverse) {
		// Reverse can reduce shared memory usage by reverse the operation.
		if (reverse == true) {
			if (instName.name().contains("ADD")) {
				instrStr = instrStr.replace("ADD", "SUB");
			} else if (instName.name().contains("SUB")) {
				instrStr = instrStr.replace("SUB", "ADD");
			} else {
				throw new RuntimeException("Incorrect instruction " + instrStr);
			}
			reparseInst();
		}
		smRdOprd.smSPOfs = idx;
	}
	
	/**
	 * Convert to FWD form
	 * 
	 * @param ins
	 */
	public void convertToFWD() {
		if (instName == SPUInst.PUT_FRRR) {
			instrStr = "\tPUTFWD " + instrStr.substring(instrStr.indexOf("^"));
		} else {
			// You can not simply forward absdiff. The absdiff has several versions, one of
			// which is absdifffwd and can only be that.
			instrStr = funcName+"FWD"+instrStr.substring(instrStr.indexOf(" "), instrStr.lastIndexOf(","));
		}
		reparseInst();
	}
	
	/** Fold PUT to the define instruction. The def operand will be replaced
	 *  by the chNo. Also change it to the PUT instruction form.
	 * @param chNo
	 */
	public void foldPUT(int chNo) {				
		changeOperandTo("^"+chNo, 0);
		reparseInst();
		return;
	}
	
	/**
	 * Fold store of the specified instruction to memory index mem. It actually 
	 * replaces the define with mem.
	 * 
	 * From
	 * add r0, r1, r2
	 * st &5, r0
	 * To
	 * add &5, r1, r2
	 * 
	 * @param inst 
	 * @param mem
	 */
	public void foldStore(Operand mem) {
		assert getOperand(0).isDef;
		
		// Replace the def
		changeOperandTo(mem.str, 0);
		reparseInst();
	}
	
	/**
	 * Fold load of the specified instruction to memory index mem. It actually 
	 * replaces the qualified use with mem.
	 * 
	 * From 
	 * ld r0, &5
	 * add r1, r0, r2
	 * to
	 * add r1, &5, r2 
	 * @param inst 
	 * @param mem
	 */
	public void foldLoad(Operand mem) {
		// Replace the use
		changeOperandTo(mem.str, origOprds.indexOf(oprds.get(2)));
		reparseInst();
	}

	/**
	 * Fold the use of memMove the specified instruction. It actually 
	 * replaces the 2nd operand with mem.
	 * 
	 * From
	 * mov &5, &15
	 * add r0, &5, r1
	 * To
	 * add r0, &15, r1
	 * 
	 * @param inst 
	 * @param mem
	 */
	public void foldMemMove(Operand mem) {
		changeOperandTo(mem.str, origOprds.indexOf(dmRdOprd0));
		reparseInst();
	}
	
	public Operand getOperand(int idx) {
		if (idx >= oprds.size())
			throw new RuntimeException("ERROR: nonexist operand! " + instrStr);
		return oprds.get(idx);
	}
	
	/**
	 * Return true is this instruction is move from memory to memory
	 * @return
	 */
	public boolean isMemMove() {
		if (instName != SPUInst.ADDMUL_MRMR)
			return false;
		
		if (!oprds.get(1).str.equals("ONE") || !oprds.get(3).str.equals("ZERO"))
			return false;
		
		return true;
	}
	
	/**
	 * Return true is this instruction is move from immediate memory to register.
	 * @return
	 */
	public boolean isIMToRegMove() {
		if (instName != SPUInst.ADDMUL_RRIR)
			return false;
		
		if (!oprds.get(1).str.equals("ONE") || !oprds.get(3).str.equals("ZERO"))
			return false;
		
		return true;
	}
	
	/**
	 * Return true if it is one of several forms of GET
	 * @return
	 */
	public boolean isGET() {
		if (funcName.equals("GET"))
			return true;
		
		return false;
	}
	
	/**
	 * Return true if it is one of the forms of PUT
	 * @return
	 */
	public boolean isPUT() {
		if (funcName.equals("PUT"))
			return true;
		
		return false;
	}
	
	/**
	 * Return true is this instruction is load from memory. Note this should correspond
	 * to compiler output.
	 * @return
	 */
	public boolean isLoad() {
		if (instName != SPUInst.ADDMUL_RRMR)
			return false;
		
		if (!oprds.get(1).str.equals("ONE") || !oprds.get(3).str.equals("ZERO"))
			return false;
		
		return true;
	}
	
	/**
	 * Return true is this instruction is store to memory. Note this should correspond
	 * to compiler output.
	 * Compiler: ADD mem, Rx, ZERO
	 * @return
	 */
	public boolean isStore() {
		if (instName != SPUInst.ADDMUL_MRRR)
			return false;
		
		if (!oprds.get(1).str.equals("ONE") || !oprds.get(3).str.equals("ZERO"))
			return false;

		return true;
	}
	
	public boolean isNOP() {
		return instName == SPUInst.NOP;
	}
	
	/**
	 * Return true is this instruction is an add
	 */
	public boolean isADD() {
		if (instName != SPUInst.ADDMUL_RRRR && instName != SPUInst.ADDMUL_RRIR &&
			instName != SPUInst.ADDMUL_RRMR && instName != SPUInst.ADDMUL_MRRR &&
			instName != SPUInst.ADDMUL_MRIR && instName != SPUInst.ADDMUL_MRMR)
		    return false;
		
		if (!oprds.get(1).str.equals("ONE"))
			return false;
		
		return true;
	}
	
	/**
	 * Return true is this instruction is a sub
	 */
	public boolean isSUB() {
		if (instName != SPUInst.SUBMUL_RRRR && instName != SPUInst.SUBMUL_RRIR &&
			instName != SPUInst.SUBMUL_RRMR && instName != SPUInst.SUBMUL_MRRR &&
			instName != SPUInst.SUBMUL_MRIR && instName != SPUInst.SUBMUL_MRMR)
		    return false;
		
		if (!oprds.get(1).str.equals("ONE"))
			return false;
		
		return true;
	}
		
	/**
	 * Return true if it is an mask instruction
	 * @return
	 */
	public boolean isMASK() {
		return (funcName.equals("SETMASKEQ") || funcName.equals("SETMASKGT")
				|| funcName.equals("SETMASKLT"));
	}
	
	public boolean isALUSRA1() {
		return (funcName.equals("ADDMULSRA1") || funcName.equals("SUBMULSRA1"));
	}
	
	public boolean isABSDIFF() {
		return (instrStr.contains("ABSDIFF"));
	}
	
	public boolean isBaseManipulateInst() {
		return (funcName.equals("SETDMRB_0") || funcName.equals("SETDMRB_1") || funcName.equals("SETDMRB_2") || 
				funcName.equals("SETDMRB_C0") || funcName.equals("SETDMWB_0") || funcName.equals("INCDMRB_0") || 
				funcName.equals("INCDMRB_1") || funcName.equals("INCDMRB_2") || funcName.equals("INCDMRB_C0") || 
				instName == SPUInst.INCDMRB_ALL ||
				funcName.equals("INCDMWB_0") ||
				funcName.equals("SETSMRB_0") || funcName.equals("INCSMRB_0") ||
				funcName.equals("INCSMWB_0") ||
				funcName.equals("INCEMRB_0") || funcName.equals("INCEMRB_1") || funcName.equals("INCEMWB_0"));
	}
	
	/**
	 * Return true if this instruction uses the specified register
	 */
	public boolean usesRegister(Operand reg) {
		return findRegisterUseOperandIdx(reg) != -1;
	}

	/**
	 * Return true if this instruction uses the specified register
	 */
	public boolean usesMemory(Operand mem) {
		return findMemoryUseOperandIdx(mem) != -1;
	}
	
	/**
	 * Return true if this instruction uses the specified register at the 
	 * specified operand index.
	 */
	public boolean usesRegister(Operand reg, int opIdx) {
		if (opIdx >= oprds.size())
			return false;
		
		for (int i = 0, e = oprds.size(); i != e; ++i) {
			Operand MO = oprds.get(i);
			
			if (!reg.isReg() || !MO.isUse) continue;
			
			if (reg.strEqual(MO) && opIdx == i) return true;
		}
		
		return false;		
	}
	
	/**
	 * Return true if this instruction uses the specified memory at the 
	 * specified operand index.
	 */
	public boolean usesMemory(Operand mem, int opIdx) {
		if (opIdx >= oprds.size())
			return false;
		
		for (int i = 0, e = oprds.size(); i != e; ++i) {
			Operand MO = oprds.get(i);
			
			if (!mem.isMem() || !MO.isUse) continue;
			
			if (mem.strEqual(MO) && opIdx == i) return true;
		}
		
		return false;		
	}
	
	/**
	 * Return true if this instruction defines the specified register
	 * @param reg
	 * @return
	 */
	public boolean definesRegister(Operand reg) {
		if (wrRF == true && reg.strEqual(rfWrOprd))
			return true;
		
		return false;
	}
	
	/**
	 * Return true if this instruction defines the specified memory
	 * @param mem
	 * @return
	 */
	public boolean definesMemory(Operand mem) {
		if (wrDM == true && mem.strEqual(dmWrOprd))
			return true;
		
		return false;
	}
	
	/**
	 * Returns the operand that is a use of
	 * the specific register or -1 if it is not found.
	 * 
	 * @param reg
	 * @return
	 */
	public int findRegisterUseOperandIdx(Operand reg) {		
		for (int i = 0, e = oprds.size(); i != e; ++i) {
			Operand MO = oprds.get(i);
			
			if (!MO.isUse) continue;
			
			if (reg.strEqual(MO)) return i;
		}
		
		return -1;
	}
	
	/**
	 * Returns the operand that is a use of the specific memory or -1 if it is
	 * not found.
	 * 
	 * @param mem
	 * @return
	 */
	public int findMemoryUseOperandIdx(Operand mem) {
		for (int i = 0, e = oprds.size(); i != e; ++i) {
			Operand MO = oprds.get(i);
			
			if (!MO.isUse) continue;
			
			if (mem.strEqual(MO)) return i;
		}
		
		return -1;
	}
	
	/**
	 * Create an UPDIMMBS instruction
	 * 
	 * @return
	 */
	public static AsmInstr createSETSMRB(int base) {
		AsmInstr inst = new AsmInstr("\tSETSMRB_0 " + base);
		return inst;
	}
	
	/**
	 * Create an SETDMWB instruction
	 * 
	 * @return
	 */
	public static AsmInstr createSETDMWB(int base) {
		AsmInstr inst = new AsmInstr("\tSETDMWB_0 " + base);
		return inst;
	}
	
	/**
	 * Create an SETDMRB instruction
	 * 
	 * @return
	 */
	public static AsmInstr createSETDMRB(int base) {
		AsmInstr inst = new AsmInstr("\tSETDMRB_0 " + base);
		return inst;
	}
	
	/**
	 * Create an RPT instruction with the specified block and cnt
	 * 
	 * @return
	 */
	public static AsmInstr createRPT(int block, int cnt) {
		AsmInstr inst = new AsmInstr("\tRPT " + block + ", " + cnt);
		return inst;
	}
	
	/**
	 * Create an NOP instruction
	 * 
	 * @return
	 */
	public static AsmInstr createNOP() {
		AsmInstr nop = new AsmInstr("NOP");
		return nop;
	}
	
	/**
	 * The format of input instruction is transformed so that it could be easier 
	 * to operate internally. 
	 */
	@SuppressWarnings("unchecked")
	public void formatTransform() {
		if (funcName.equals("MOV")) {
			assert origOprds.size() == 2;
			char D = origOprds.get(0).modifier;
			char C = origOprds.get(1).modifier;
			
			instName = SPUInst.valueOf("ADDMUL"+"_"+D+"R"+"R"+C);
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("ZERO", 'R'));
			oprds.add(1, new Operand("ZERO", 'R'));
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
		} else if (funcName.equals("ADD") || funcName.equals("SUB"))  {
			assert origOprds.size() == 3;
			
			char D = origOprds.get(0).modifier;
			char B = origOprds.get(1).modifier;
			char C = origOprds.get(2).modifier;
			
			instName = SPUInst.valueOf(funcName+"MUL"+"_"+D+"R"+B+C);
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("ONE", 'R'));
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
			_setUse(origOprds.get(2));
		} else if (funcName.equals("MUL"))  {
			assert origOprds.size() == 3;
			
			char D = origOprds.get(0).modifier;
			char A = origOprds.get(1).modifier;
			char B = origOprds.get(2).modifier;
			
			instName = SPUInst.valueOf("ADD"+funcName+"_"+D+A+B+'R');
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(new Operand("ZERO", 'R'));
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
			_setUse(origOprds.get(2));
		} else if (funcName.equals("ADDMUL") || funcName.equals("SUBMUL") 
				|| funcName.equals("ADDMULSRA1") || funcName.equals("SUBMULSRA1")) {
			assert origOprds.size() == 4;
			char D = origOprds.get(0).modifier;
			char A = origOprds.get(1).modifier;
			char B = origOprds.get(2).modifier;
			char C = origOprds.get(3).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+A+B+C);
			oprds = (LinkedList<Operand>) origOprds.clone();
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
			_setUse(origOprds.get(2));
			_setUse(origOprds.get(3));
		} else if (funcName.equals("ADDFWD") || funcName.equals("SUBFWD")) {
			assert origOprds.size() == 2;
			char D = origOprds.get(0).modifier;
			char B = origOprds.get(1).modifier;
			
			instName = SPUInst.valueOf(funcName.replace("FWD", "MULFWD")+"_"+D+"R"+B+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("ONE", 'R'));
			oprds.add(new Operand("X", 'X'));
			
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
		} else if (funcName.equals("ADDMULFWD") || funcName.equals("SUBMULFWD")) {
			assert origOprds.size() == 3;
			char D = origOprds.get(0).modifier;
			char A = origOprds.get(1).modifier;
			char B = origOprds.get(2).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+A+B+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(new Operand("X", 'X'));
			
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
			_setUse(origOprds.get(2));
		} else if (funcName.equals("ABSDIFFACCUM")) {
			assert (origOprds.size() == 2) || (origOprds.size() == 3);
			// two cases. first: 2 operands, that means no sink operand
			if (origOprds.size() == 3) {
				char D = origOprds.get(0).modifier;
				char B = origOprds.get(1).modifier;
				char C = origOprds.get(2).modifier;
				
				instName = SPUInst.valueOf(funcName+"_"+D+"X"+B+C);
				oprds = (LinkedList<Operand>) origOprds.clone();
				oprds.add(1, new Operand("X", 'X'));
				
				_setDef(origOprds.get(0));
				_setUse(origOprds.get(1));
				_setUse(origOprds.get(2));
			} else if (origOprds.size() == 2) {
				char B = origOprds.get(0).modifier;
				char C = origOprds.get(1).modifier;
				
				instName = SPUInst.valueOf(funcName+"_"+"X"+"X"+B+C);
				oprds = (LinkedList<Operand>) origOprds.clone();
				oprds.add(0, new Operand("X", 'X'));
				oprds.add(0, new Operand("X", 'X'));
				
				_setUse(origOprds.get(0));
				_setUse(origOprds.get(1));
			}
		} else if (funcName.equals("SETMASKEQ") || funcName.equals("SETMASKGT") || funcName.equals("SETMASKLT")) {
			assert origOprds.size() == 2;
			char B = origOprds.get(0).modifier;
			char C = origOprds.get(1).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+"X"+"R"+B+C);
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(0, new Operand("ONE", 'X'));
			oprds.add(0, new Operand("X", 'X'));
			
			_setUse(origOprds.get(0));
			_setUse(origOprds.get(1));
		} else if (funcName.equals("ABSDIFFFWD") || funcName.equals("DECONST") || funcName.equals("SQRT")) {
			assert origOprds.size() == 2;
			char D = origOprds.get(0).modifier;
			char B = origOprds.get(1).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+"X"+B+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("X", 'X'));
			oprds.add(new Operand("X", 'X'));
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
		} else if (funcName.equals("GET")) {
			assert origOprds.size() == 2;
			char D = origOprds.get(0).modifier;
			char B = 'F';
			
			instName = SPUInst.valueOf(funcName+"_"+D+"X"+B+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("X", 'X'));
			oprds.add(new Operand("X", 'X'));
			
			_setDef(origOprds.get(0));
		} else if (funcName.equals("PUT")) {
			assert origOprds.size() == 2;
			char D = 'F';
			char B = origOprds.get(0).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+"R"+B+"R");			
			oprds.add(origOprds.get(1));
			oprds.add(new Operand("ONE", 'R'));
			oprds.add(origOprds.get(0));
			oprds.add(new Operand("ZERO", 'R'));
			
			_setUse(origOprds.get(0));
		} else if (funcName.equals("ABSDIFF") || funcName.equals("SLT") || funcName.equals("SGT")) {
			assert origOprds.size() == 3;
			char D = origOprds.get(0).modifier;
			char B = origOprds.get(1).modifier;
			char C = origOprds.get(2).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+"R"+B+C);
			oprds = (LinkedList<Operand>) origOprds.clone();
			oprds.add(1, new Operand("ONE", 'R'));
			
			_setDef(origOprds.get(0));
			_setUse(origOprds.get(1));
			_setUse(origOprds.get(2));
		} else if (funcName.equals("LDSORT")) {
			assert origOprds.size() == 1;
			char B = origOprds.get(0).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+"X"+"X"+B+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			
			oprds.add(0, new Operand("X", 'X'));
			oprds.add(0, new Operand("X", 'X'));
			oprds.add(new Operand("X", 'X'));
			_setUse(origOprds.get(0));
		} else if (funcName.equals("UNLDSORT")) {
			assert origOprds.size() == 1;
			char D = origOprds.get(0).modifier;
			
			instName = SPUInst.valueOf(funcName+"_"+D+"X"+"X"+"X");
			oprds = (LinkedList<Operand>) origOprds.clone();
			
			oprds.add(0, new Operand("X", 'X'));
			oprds.add(0, new Operand("X", 'X'));
			oprds.add(new Operand("X", 'X'));
			_setDef(origOprds.get(0));
		} else if (funcName.contains("SETDM") || funcName.contains("SETEM") || funcName.contains("SETSM")
				|| funcName.contains("INCDM") || funcName.contains("INCEM") || funcName.contains("INCSM")) {
			// base address manipulation instructions
			instName = SPUInst.valueOf(funcName);
			oprds = (LinkedList<Operand>) origOprds.clone();
		} else if (funcName.equals("JMP") || funcName.equals("LDEXMEM") || funcName.equals("LDCACHE") 
				|| funcName.equals("STEXMEM") || funcName.equals("STCACHE") || funcName.equals("SETINFIFODEPTH")
				|| funcName.equals("SETOUTFIFODEPTH")
				|| funcName.equals("SETREGVALUE_ID")) {
			assert origOprds.size() == 1;
			instName = SPUInst.valueOf(funcName);
			oprds = (LinkedList<Operand>) origOprds.clone();
		} else if (funcName.equals("RPT") || funcName.equals("SETREGVALUE")) {
			assert origOprds.size() == 2;
			instName = SPUInst.valueOf(funcName);
			oprds = (LinkedList<Operand>) origOprds.clone();
		} else if (funcName.equals("ABSDIFFCLR") || funcName.equals("NOP") || funcName.equals("RPTEND")
				|| funcName.equals("MASKEND") || funcName.equals("SHIFTCACHELINE") || funcName.equals("LDCACHE_BROADCAST")
				|| funcName.equals("BARRIER") || funcName.equals("RESETRXIDX") || funcName.equals("RESETTXIDX")
				|| funcName.equals("INCRXIDXBY1") || funcName.equals("INCTXIDXBY1") || funcName.equals("SORT")) {
			assert origOprds.size() == 0;
			instName = SPUInst.valueOf(funcName);
		} else {
			throw new RuntimeException("ERROR: new instruction? " + instrStr);
		}
	}
	
	private void _setDef(Operand op) {
		defOprd = op;
		op.isDef = true;
	}
	
	private void _setUse(Operand op) {
		useOprds.add(op);
		op.isUse = true;
	}
	
	private void _parseInst() {
		rfWrOprd = null;
		dmRdOprd0 = null;
		dmRdOprd1 = null;
		dmWrOprd = null;
		smRdOprd = null;
		smWrOprd = null;
		putChOprd = null;
		defOprd = null;
		useOprds.clear();
		oprds.clear();
		origOprds.clear();
		isFWD = false;
		wrRF = false;
		rdDM0 = false;
		rdDM1 = false;
		wrDM = false;		
		rdSM = false;
		wrSM = false;
		wrFIFO = false;
		rdFIFO = false;
		String[] fields = instrStr.trim().replaceAll(",", "").split("\\s+");
		funcName = fields[0];
		for (int fldIdx = 1; fldIdx < fields.length; fldIdx++) {
			String opstr = fields[fldIdx];
			
			if (_isReg(opstr)) {
				Operand opr = new Operand(opstr, 'R');
				origOprds.add(opr);
			} else if (_isDMOprd(opstr)) {
				Operand opr = new Operand(opstr, 'M');
				opr.setDMFields();
				origOprds.add(opr);
			} else if (_isIMOprd(opstr)) {
				Operand opr = new Operand(opstr, 'I');
				opr.setSMFields();
				origOprds.add(opr);
			} else if (_isChannelNoOprd(opstr)) {
				Operand opr = new Operand(opstr, 'F');
				opr.setChFields();
				chNo = opr.chNo; // for convenience
				origOprds.add(opr);
			} else if (_isEMOprd(opstr)) {
				Operand opr = new Operand(opstr, 'E');
				opr.setEMFields();
				origOprds.add(opr);
			} else if (opstr.matches("-?\\d+")) {
				Operand opr = new Operand(opstr, 'O');
				origOprds.add(opr);
			} else {
				throw new RuntimeException("ERROR: Unrecogonised operand: "+opstr);
			}
		}
		
		// Generate instrName, oprds, and set operand property
		formatTransform();
		
		// Set instruction properties and link to convenience operand
		if (_wrRF()) {
			wrRF = true;
			rfWrOprd = _getRFWrOprd();
		} else if (_wrDM()) {
			wrDM = true;
			dmWrOprd = _getDMWrOprd();
		} else if (_wrFIFO()){
			wrFIFO = true;
			putChOprd = oprds.get(0);
		} else if (_wrSM()) {
			wrSM = true;
			smWrOprd = _getSMWrOprd();
		}
		
		if (_rdDM0()) {
			rdDM0 = true;
			dmRdOprd0 = _getDMRdOprd0();	
		} 
		
		if (_rdIM()) {
			rdSM = true;
			smRdOprd = _getIMRdOprd();
		}
		
		if (_rdDM1()) {
			rdDM1 = true;
			dmRdOprd1 = _getDMRdOprd1();	
		} 
		
		if (_rdFIFO()) {
			rdFIFO =true;
		}
		
		if (_isFWD()) {
			isFWD = true;
		}
	}
	
	/**
	 * @return
	 */
	private boolean _wrRF() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char des = oprds.charAt(0);
		if (des == 'R')
			return true;
		
		return false;
	}
	
	/**
	 * Return true if the instruction has a memory operand as use
	 * @return
	 */
	private boolean _rdDM0() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		String srcs = oprds.substring(1);
		if (srcs.contains("M"))
			return true;
		return false;
	}
	
	/**
	 * @return
	 */
	private boolean _rdDM1() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char srcA = oprds.charAt(1);
		char srcB = oprds.charAt(2);
		char srcC = oprds.charAt(3);
		
		int cnt = 0;
		if (srcA == 'M') cnt++;
		if (srcB == 'M') cnt++;
		if (srcC == 'M') cnt++;
		
		if (cnt == 3)
			throw new RuntimeException("ERROR: Three DM src operands");
		
		if (cnt != 2) 
			return false;
		else
			return true;
	}
	
	/**
	 * Return true if the define is a memory operand
	 * @return
	 */
	private boolean _wrDM() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char des = oprds.charAt(0);
		if (des == 'M')
			return true;
		
		return false;
	}
	
	private boolean _wrSM() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char des = oprds.charAt(0);
		if (des == 'I')
			return true;
		
		return false;
	}
	
	/**
	 * @return
	 */
	private boolean _wrFIFO() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char des = oprds.charAt(0);
		if (des == 'F')
			return true;
		
		return false;
	}
	
	private boolean _rdFIFO() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		char B = oprds.charAt(2);
		if (B == 'F')
			return true;
		
		return false;
	}
	
	/**
	 * @return
	 */
	private boolean _rdIM() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		if (oprds.length() != 4) return false;
		String srcs = oprds.substring(1);
		if (srcs.contains("I"))
			return true;
		return false;
	}
	
	/**
	 * Return true if it is an FWD instruction
	 * @return
	 */
	private boolean _isFWD() {
		return funcName.contains("FWD");
	}
	
	private boolean _isReg(String reg) {
		return reg.contains("R") || reg.equals("ZERO") || reg.equals("ONE");
	}
	
	/**
	 * Return true when it is a memory operand, which is the form like [ofs](sel!).
	 * It can be ofs only, or without !. E.g. [12], [12](0), [12](0!), [12](1!).
	 * 
	 * @param mem
	 * @return
	 */
	private boolean _isDMOprd(String mem) {
		return mem.contains("&");
	}
	
	/**
	 * When in read only mode, the format is #val
	 * @param im
	 * @return
	 */
	private boolean _isIMOprd(String im) {
		return im.contains("#");
	}
	
	private boolean _isEMOprd(String em) {
		return em.contains("~");
	}
	
	private boolean _isChannelNoOprd(String ch) {
		return ch.contains("^");
	}
	
	private Operand _getDMWrOprd() {
		 return oprds.get(0);
	}
	
	private Operand _getSMWrOprd() {
		return oprds.get(0);
	}
	
	/**
	 * DM read operand 0
	 * 
	 * @return
	 */
	private Operand _getDMRdOprd0() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		
		char srcA = oprds.charAt(1);
		char srcB = oprds.charAt(2);
		char srcC = oprds.charAt(3);

		if (srcA == 'M')
			return this.oprds.get(1);
		else if (srcB == 'M')
			return this.oprds.get(2);
		else if (srcC == 'M') 
			return this.oprds.get(3);
		else
			throw new RuntimeException("ERROR: No DM operand! " + instrStr);
	}
	
	private Operand _getDMRdOprd1() {		
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		
		char srcB = oprds.charAt(2);
		char srcC = oprds.charAt(3);

		if ((srcB == 'M') && (srcC != 'M'))
			return this.oprds.get(2);
		else if (srcC == 'M') 
			return this.oprds.get(3);
		else
			throw new RuntimeException("ERROR: No DM operand! " + instrStr);
	}
	
	private Operand _getRFWrOprd() {		
		return  oprds.get(0);
	}
	
	private Operand _getIMRdOprd() {
		String oprds = instName.name().substring(instName.name().indexOf("_")+1);
		
		char srcA = oprds.charAt(1);
		char srcB = oprds.charAt(2);
		char srcC = oprds.charAt(3);

		if (srcA == 'I')
			return this.oprds.get(1);
		else if (srcB == 'I')
			return this.oprds.get(2);
		else if (srcC == 'I') 
			return this.oprds.get(3);
		else
			throw new RuntimeException("ERROR: No IM operand! " + instrStr);
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         public  variables                 ////
	// Original instruction string
	public String instrStr;
	// Stores the general instruction form
	public String funcName;
	public LinkedList<Operand> origOprds = new LinkedList<Operand>(); 

	// After parsing original instruction, below fields are set and used for internal use.
	public SPUInst instName;
	public String instrBin;	

	public Operand rfWrOprd;
	public Operand dmRdOprd0;
	public Operand dmRdOprd1;
	public Operand dmWrOprd;
	public Operand smRdOprd;
	public Operand smWrOprd;
	public Operand putChOprd;
	
	public int chNo;
	
	/* Cycle before synchronisation */
	public int cycle = -1;
	
	// If it is a repeated instruction, rptLev is the level it belongs to.
	public RPTLevel rptLev;
	// If it is a RPT instruction, rptInfo is the repeat level it generates.
	public RPTLevel rptInfo;
	
	public Operand defOprd;
	public LinkedList<Operand> useOprds = new LinkedList<Operand>();
	public LinkedList<Operand> oprds = new LinkedList<Operand>(); 
	
	public boolean masked = false;
	public boolean isFWD = false;
	public boolean wrRF = false;
	public boolean rdDM0 = false;
	public boolean rdDM1 = false;
	public boolean wrDM = false;
	public boolean rdSM = false;
	public boolean wrSM = false;
	public boolean wrFIFO = false;
	public boolean rdFIFO = false;
}
