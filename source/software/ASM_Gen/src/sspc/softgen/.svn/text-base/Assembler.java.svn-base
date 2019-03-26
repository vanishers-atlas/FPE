package sspc.softgen;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import sspc.lib.AsmInstr;
import sspc.lib.Assembly;
import sspc.lib.Assembly.SPUInst;
import sspc.lib.SPUConfig;
import sspc.lib.Operand;
import sspc.lib.SSP;

/**
 * Overview:
 * 
 * 1. To support multiple streams and autoinc, currently b25 (autoincwrite)
 * and b24 (autoincread) are assigned to autoinc use, while b23 and b22
 * are assigned for stream addressing use. Problem is when register 64 mode is
 * used, b23 and b22 will be aliased to rf_wraddr_Pb2.
 * 2. set mask bit at  b21
 * 
 * @author 40055379
 *
 */

public class Assembler {

	public Assembler (Assembly asm, SPUConfig conf, SSP ssp) {
		_asm = asm;
		_addrWidth = conf.regWidth;
		_one = conf.regSize - 1;
		_zero = conf.regSize - 2;
		_conf = conf;
		
		constRPSel1 = 2*conf.regWidth-1;
		constRPSel0 = 2*conf.regWidth-2;
		constMASKBit = conf.pmDataWidth-7;
		constAutoincWP = 2*conf.regWidth-3;
		constAutoincRP0 = 2*conf.regWidth-4;
		constAutoincRP1 = 2*conf.regWidth-5;
		
		_instTypes = new ArrayList<SPUInst>(ssp.sspInstTypes);
	};		
	
    ///////////////////////////////////////////////////////////////////
    ////                         public  methods                   ////
	
	/**
	 * Assemble the assembly
	 */
	public void assemble() {
		StringBuffer code = new  StringBuffer();
		List<AsmInstr> instrs = _asm.getInstructions();
		Iterator<AsmInstr> iter = instrs.iterator();
		while (iter.hasNext()) {
			AsmInstr I = iter.next();
			
			SPUInst opc = I.instName;
			String fstr = I.funcName;
						
			if (fstr.contains("ADD") || fstr.contains("SUB") || fstr.contains("MUL")  || fstr.equals("MOV"))
				code.append(_printADDSUBMUL(I));
			else if (opc == SPUInst.RPT)
				code.append(_printRPT(I));			
			else if (opc == SPUInst.JMP)
				code.append(_printBLTBGTBEQJMP(I));
			else if (I.isMASK())
				code.append(_printSETMASKCMP(I));
			else if (I.isGET())
				code.append(_printGET(I));
			else if (I.isPUT())
				code.append(_printPUT(I));
			else if (opc == SPUInst.PUTFWD_FRRX)
				code.append(_printPUTFWD(I));
			else if (opc == SPUInst.NOP || opc ==SPUInst.ABSDIFFCLR)
				code.append(_printNooperand(I));
			else if (I.isBaseManipulateInst())
				code.append(_printManipulateBS(I));
			else if (I.isABSDIFF())
				code.append(_printABSDIFF(I));
			else if (fstr.equals("DECONST") || fstr.equals("LDSORT") || fstr.equals("UNLDSORT"))
				code.append(_printDECONST(I));
			else if (opc == SPUInst.LDEXMEM || opc == SPUInst.STEXMEM)
				code.append(_printEXMEM(I));
			else if (opc == SPUInst.LDCACHE)
				code.append(_printLDCACHE(I));
			else if (opc == SPUInst.STCACHE)
				code.append(_printSTCACHE(I));
			else if (opc == SPUInst.BARRIER || opc == SPUInst.RESETRXIDX || opc == SPUInst.RESETTXIDX
					|| opc == SPUInst.INCRXIDXBY1 || opc == SPUInst.INCTXIDXBY1 || opc == SPUInst.SHIFTCACHELINE
					|| opc == SPUInst.LDCACHE_BROADCAST || opc == SPUInst.SORT)
				code.append(_printNooperand(I)); // printing opcode only
			/*Newly added*/
			else {
				System.out.println("ERROR: Unknow instruction is being assmbled"
						+ I.instrStr);
				System.exit(1);
			}
			
			// Add comment field
			code.append("    //");
			code.append(I.instrStr + "\n");
		}
		
		_machCode = code.toString();		
	}
	
	/**
	 * Print machine code to a file
	 * @param outFileName
	 */
	public void printMachineCode(String outFileName) {
		// Write into .bin file.
		SWGenUtils.writeToFile(outFileName, _machCode);
	}
	
	private String _printGET(AsmInstr I) {		
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		ops |= getDigits(I.getOperand(2)) << _addrWidth*1;
		ops |= getDigits(I.getOperand(3)) << _addrWidth*0;
		if (I.wrDM && I.dmWrOprd.dmSPAutoinc) {
			ops |= 1 << constAutoincWP;
		} else if (I.wrSM && I.smWrOprd.smSPAutoinc) {
			ops |= 1 << constAutoincWP;
		}
		if (I.oprds.get(2).chAutoinc) {
			ops |= 1 << constAutoincRP0;
			_conf.getchEn = true;
		}
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}

	/**
	 * PUT uses DSP48E datapath, so a special mode of DSP48E is used - 0+a*b.
	 * The rs3 is used for channel index while not to be part of the addition.
	 * @param I
	 * @return
	 */
	private String _printPUT(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		if (I.rdDM0) {
			if (I.dmRdOprd0.dmSPAutoinc)
				ops |= 1 << constAutoincRP0;

			ops |= ((I.dmRdOprd0.dmSPIdx & 2)>>1) << constRPSel1; 
			ops |= (I.dmRdOprd0.dmSPIdx & 1) << constRPSel0;
		}
		
		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		if (I.rdDM0) {
			int rdAddr = getDigits(I.dmRdOprd0);
			ops |= rdAddr/_conf.regSize << _addrWidth*4+_conf.extraWidth()/2;
			ops |= rdAddr%_conf.regSize << _addrWidth;
		} else {
			ops |= getDigits(I.getOperand(2)) << _addrWidth;
		}
		ops |= getDigits(I.getOperand(3)) << _addrWidth*0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}
	
	private String _printPUTFWD(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		ops |= getDigits(I.getOperand(2)) << _addrWidth*1;
		ops |= getDigits(I.getOperand(3)) << _addrWidth*0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}	

	private String _printManipulateBS(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		ops |= getDigits(I.getOperand(0));
		
		code.append(_setInstName(I));
		String oprdspart = SWGenUtils.intToBinary(ops, 26);
		if (oprdspart.charAt(25-constMASKBit) == '1') {
			StringBuilder strb = new StringBuilder(oprdspart);
			strb.setCharAt(25-constMASKBit, '0');
			oprdspart = strb.toString();
		}
		code.append(oprdspart);
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();		
	}
	
	private String _printNooperand(AsmInstr I) {		
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();		
	}

	private String _printSETMASKCMP(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		ops |= _one << 2*_addrWidth;
		ops |= getDigits(I.getOperand(0)) << _addrWidth;
		ops |= getDigits(I.getOperand(1));
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();	
	}	
	
	private String _printBLTBGTBEQJMP(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		ops |= getDigits(I.getOperand(0));
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();		
	}

	private String _printRPT(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		// Note the repeat counter starts from 0, so minus actual value by 1 when
		// use counter. But when using SRL AND the loop block size is 1, the rpt
		// cycle set ce<='1', and immediately check the srl output is unavailable.
		// Thus in this case, counter value must be set to actual value minus 2.
		if (I.rptInfo.insts.size() == 1 && _conf.rptUseSRL == true)
			ops |= I.rptInfo.cntNum-2;
		else
			ops |= I.rptInfo.cntNum-1;
		ops |= I.rptInfo.endLoc << 10;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();			
	}

	private String _printADDSUBMUL(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		if (I.rdDM0) {
			if (I.dmRdOprd0.dmSPAutoinc)
				ops |= 1 << constAutoincRP0;

			ops |= ((I.dmRdOprd0.dmSPIdx & 2)>>1) << constRPSel1; 
			ops |= (I.dmRdOprd0.dmSPIdx & 1) << constRPSel0;
		}
		if (I.rdDM1) {
			if (I.dmRdOprd1.dmSPAutoinc)
				ops |= 1 << constAutoincRP1;
		}
		
		if (I.wrDM && I.dmWrOprd.dmSPAutoinc) 
			ops |= 1 << constAutoincWP;
		
		int mask = I.masked? 1:0;
		ops |= mask << constMASKBit;

		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		if (I.rdDM0) {
			int rdAddr = getDigits(I.dmRdOprd0);
			ops |= rdAddr/_conf.regSize << _addrWidth*4+_conf.extraWidth()/2;
			ops |= rdAddr%_conf.regSize << _addrWidth;
		} else {
			ops |= getDigits(I.getOperand(2)) << _addrWidth;
		}
		
		ops |= getDigits(I.getOperand(3));
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}

	private String _printABSDIFF(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		if (I.rdDM0) {
			if (I.dmRdOprd0.dmSPAutoinc)
				ops |= 1 << constAutoincRP0;

			ops |= ((I.dmRdOprd0.dmSPIdx & 2)>>1) << constRPSel1; 
			ops |= (I.dmRdOprd0.dmSPIdx & 1) << constRPSel0;
		}
		if (I.rdDM1) {
			if (I.dmRdOprd1.dmSPAutoinc)
				ops |= 1 << constAutoincRP1;
		}
		
		if (I.wrDM && I.dmWrOprd.dmSPAutoinc) 
			ops |= 1 << constAutoincWP;
						
		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		ops |= getDigits(I.getOperand(2)) << _addrWidth*1;
		ops |= getDigits(I.getOperand(3)) << _addrWidth*0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();	
	}	
	
	private String _printDECONST(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		
		ops |= getDigits(I.getOperand(0)) << _addrWidth*3;
		ops |= getDigits(I.getOperand(1)) << _addrWidth*2;
		ops |= getDigits(I.getOperand(2)) << _addrWidth*1;
		ops |= getDigits(I.getOperand(3)) << _addrWidth*0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}	
	
	private String _printEXMEM(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		Operand exmem = I.oprds.get(0);
		if (I.instName == SPUInst.LDEXMEM) {
			if (exmem.emSPAutoinc)
				ops |= 1 << constAutoincRP0;
			ops |= (exmem.emSPIdx & 1) << constRPSel0;
		} else {
			if (exmem.emSPAutoinc) 
				ops |= 1 << constAutoincWP;
		}
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}
	
	// From ldcache to FIFO
	private String _printLDCACHE(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		Operand tx = I.oprds.get(0);
		if (tx.chAutoinc)
			ops |= 1 << constAutoincWP;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}
	
	// From FIFO to stcache
	private String _printSTCACHE(AsmInstr I) {
		StringBuffer code = new  StringBuffer();
		int ops = 0;
		Operand rx = I.oprds.get(0);
		if (rx.chAutoinc)
			ops |= 1 << constAutoincRP0;
		
		code.append(_setInstName(I));
		code.append(SWGenUtils.intToBinary(ops, 26));
		I.instrBin = code.toString().replaceAll("[\\D]", "");
		return code.toString();
	}
	
	public int getDigits(Operand op) {
		if (op.isMem()) {
			return op.dmSPOfs;
		} else if (op.isReg()) {
			if (op.str.equals("ZERO"))		
				return _zero;
			else if (op.str.equals("ONE"))
				return _one;
			else
				return Integer.parseInt(op.str.replaceAll("[\\D]", ""));
		} else if (op.isImm()) {
			return op.smSPOfs;
		} else if (op.isXOp()) {
			return 0;
		}
		
		// Special case like INCDMRB_0 -2500
		if (op.str.charAt(0) == '-')
			return Integer.parseInt(op.str);
		else
			return Integer.parseInt(op.str.replaceAll("[\\D]", ""));
	}
	
	/**
	 * Get the function code corresponding to the instruction name
	 * @param funcName
	 * @return
	 */
	public String getFuncCode(SPUInst inst) {		
		int idx; 
		if (inst == SPUInst.NOP)
			idx = 0;
		else {
			idx = _instTypes.indexOf(inst)+1;
			assert idx > 0;
		}
		return SWGenUtils.intToBinary(idx, 6);
	}
	
	private String _setInstName(AsmInstr I) {
		return getFuncCode(I.instName) + " ";
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         private  variables                ////
	private Assembly _asm;
	private int _addrWidth;
	private int _one;
	private int _zero;
		
	/** Store assembled machine code */
	private String _machCode;
	private SPUConfig _conf;
	private ArrayList<SPUInst> _instTypes;
	
	/** Constant variable **/
	private int constRPSel1;
	private int constRPSel0;
	private int constMASKBit;
	private int constAutoincWP;
	private int constAutoincRP0;
	private int constAutoincRP1;
	
		
}
