package sspc.lib;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Vector;

import sspc.hardgen.SSPConfig;
import sspc.lib.Assembly.SPUInst;
import sspc.softgen.SWGenUtils;
import sspc.softgen.SoftwareGen;

public class SSP {
	public SSP() {};
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	
	/**
	 * Return total PE numbers in this SSP instance.
	 * @return
	 */
	public int getNumPEs() {
		int sum = 0;
		for (SPU spu : spus) {
			sum += spu.PEs.size();
		}
		return sum;
	}
	
	/**
	 * Return the number of FPEs in this SSP instance.
	 * @return
	 */
	public int numSPUs() {
		return spus.size();
	}
	
	/**
	 * Get the specified FPE
	 * @param idx
	 * @return
	 */
	public SPU getSPU(int idx) {
		return spus.get(idx);
	}
	
	/**
	 * Fill in reads and writes of all inter-PE FIFOs.
	 */
	public void genFIFOWritesAndReadsInfo() {
		for (SPU spu : spus) {
			Assembly asm = spu.asm;
			// Fill in writes
			for (FIFOInstr put : asm.putInstrs) {
				for (PE pe : spu.PEs) {
					FIFO f = pe.getOutputFIFO(put.channelNo);
					// Note +2 is because PUT is pa4, get is pa2 for the pipeline
					// at the output of FIFO
					f.writes.add(put.getCycleAfterSync()+2);
				}
			}
			
			// Fill in reads
			for (FIFOInstr get : asm.getInstrs) {
				for (PE pe : spu.PEs) {
					FIFO f = pe.getInputFIFO(get.channelNo);
					f.reads.add(get.cycleAfterSync);
				}
			}
		}
	}
	
	/**
	 * After the FIFO information has been got, try to share some FIFOs.
	 */
	@SuppressWarnings("unchecked")
	public void shareFIFO() {
		if(skipShareFIFO) return;
		
		for (SPU spu : spus) {
			// NOTE: Only work for SISD SPU
			if (spu.PEs.size() > 1) continue;
			
			PE pe = spu.PEs.get(0);
			
			// tFIFOs are the working list of candidate FIFOs
			Vector<FIFO> tFIFOs = new Vector<FIFO> ();
			// exFIFO used to insert the output FIFO at the end of tFIFOs 
			FIFO exFIFO = null;
			for (FIFO f:pe.outputFIFOs) {
				if (f.isExOutFIFO)
					exFIFO = f;
				else
					tFIFOs.add(f);
			}
			// First: get the share matrix, it is the matrix of which each element
			// represents weather the row-col can be shared. For example:
			//   A B C
			// A 1 0 1  
			// B 0 1 0 
			// C 1 0 1
			// Which means AC can share. The data structure can be a list of list. A
			// column is a list.
			
			// 'size' is the number of candidate FIFOs
			int size = tFIFOs.size();
			if (size < 2) return;
			if (size > 7) {
				System.out.println("WARNING: FIFO sharing do not support sharing more than 7");
				return;
			}
			
			LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
			for (int i=0; i<size; i++) {
				shareMat.add(new LinkedList<Integer>());
			}
			
			for (int i=0; i<size; i++) {
				for (int j=0; j<size; j++) {
					LinkedList<Integer> col = shareMat.get(j);
					if (i==j) {
						col.add(1);
						continue;
					} else if (i>j) {
						col.add(shareMat.get(i).get(j));
						continue;
					}
					
					int testResult = testShare(tFIFOs.get(i), tFIFOs.get(j));
					col.add(testResult);
				}
			}
			
			// Second: find the largest area possible with all '1's in share matrix. The area is
			// composed by selected rows and columns. For example delete B row/column.
			//   A C
			// A 1 1  
			// C 1 1
			LinkedList<LinkedList<Integer>> origMat = shareMat;
			LinkedList<Integer> oriResult = new LinkedList<Integer>();			
			for (int i=0; i<shareMat.size(); i++) {
				oriResult.add(i);
			}
			LinkedList<Integer> result = new LinkedList<Integer>();
			boolean find = false;
			int level = 0;
			
			if (level == 0) {
				level++;
				result = (LinkedList<Integer>) oriResult.clone();
				if (!containsZero(shareMat)) {
					// once it satisfies the condition, current 'result' contains the largest set.
					// Just stop after that.
					find = true;				
				}
			} else if (level==1 && find==false && level<size) {
				level++;
				// Below means already searched all sub-matrices, but still find noting sharable.
				if (level == size)
					return;
				find = level1ShareTest(origMat, oriResult, result);
			} else if (level==2 && find==false && level<size) {
				level++;
				if (level == size)
					return;
				find = level2ShareTest(origMat, oriResult, result);
			} else if (level==3 && find==false && level<size) {
				level++;
				if (level == size)
					return;
				find = level3ShareTest(origMat, oriResult, result);
			} else if (level==4 && find==false && level<size) {
				level++;
				if (level == size)
					return;
				find = level4ShareTest(origMat, oriResult, result);
			}  else if (level==5 && find==false && level<size) {
				level++;
				if (level == size)
					return;
				find = level5ShareTest(origMat, oriResult, result);
			} else if (level==6 && find==false && level<size) {
				level++;
				return;
			}
			
			// 'result' records the FIFOs (the indexes) to be shared. 
			System.out.println("INFO: Shared "+result.size() + " FIFOs in "+spu.name);
			FIFO newf = new FIFO();
			newf.srcPE = pe;
			tFIFOs.add(newf);
			fifos.add(newf);
			
			for (int i=result.size()-1; i>=0; i--) {
				//BUG here.
				FIFO f = tFIFOs.get(i);
				tFIFOs.remove(f);
				
				// 'newf' will merge fields of all shared FIFOs, including 'putInsts',
				// 'writes' and 'reads'.
				newf.putInsts.addAll(f.putInsts);
				newf.writes.addAll(f.writes);
				newf.reads.addAll(f.reads);
				// 'fifos' will remove this shared FIFO
				fifos.remove(f);
				
				// 'newf' should add the sinkPE of the merged FIFO to its sinkPEs list.
				// NOTE: we assume before sharing, all FIFOs only has one sinkPE.
				PE f_sinkpe = f.sinkPEs.get(0);
				newf.sinkPEs.add(f_sinkpe);
				
				// Corresponding sink PE should notice the input FIFO has changed.
				// Change 'f' to 'newf'.
				f_sinkpe.inputFIFOs.set(f.getReadIdxIn(f_sinkpe), newf); // reflect to sinkpe
			}
			
			// Add the external output FIFO to the end of the list.
			if (exFIFO != null) {
				tFIFOs.add(exFIFO);
			}
			pe.outputFIFOs = tFIFOs;
			
			// After sharing, the FIFO indexes will change in the srcPE. So here it
			// updates all the indexes of the PUT instructions issued from the srcPE.
			for (FIFO f:tFIFOs) {
				int chNo = tFIFOs.indexOf(f);
				for (AsmInstr inst:f.putInsts) {
					inst.changePutChNoTo(chNo);
				}
			}
		}
	}
	
	// Test is done by deleting one row, test, if not satisfied, reset and delete another row,
	// until all rows are tested. The 'result' will store information of which rows are deleted. 
	@SuppressWarnings("unchecked")
	private boolean level1ShareTest(LinkedList<LinkedList<Integer>> origMat, LinkedList<Integer> oriResult,
			LinkedList<Integer> result) {
		boolean find = false;
		LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
		
		for (int i=0; i<origMat.size(); i++) {
			shareMat = cloneMat(origMat);
			result = (LinkedList<Integer>) oriResult.clone();
			deleteRowCol(shareMat, i);
			result.remove(i);
			if (!containsZero(shareMat)) {
				find = true;
				return find;
			}
		}
		return find;
	}
	
	@SuppressWarnings("unchecked")
	private boolean level2ShareTest(LinkedList<LinkedList<Integer>> origMat, LinkedList<Integer> oriResult,
			LinkedList<Integer> result) {
		boolean find = false;
		LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
		
		for (int i=0; i<origMat.size(); i++) {
			LinkedList<LinkedList<Integer>> backupMat1 = cloneMat(origMat);
			deleteRowCol(backupMat1, i);
			
			LinkedList<Integer> backupRes1 = (LinkedList<Integer>) oriResult.clone();
			backupRes1.remove(i);
			
			for (int j=0; j<backupMat1.size()-1; j++) {
				shareMat = cloneMat(backupMat1);
				result = (LinkedList<Integer>) backupRes1.clone();
				
				deleteRowCol(shareMat, j);
				result.remove(j);
				
				if (!containsZero(shareMat)) {
					find = true;
					return find;
				}
			}
		}
		return find;
	}
	
	@SuppressWarnings("unchecked")
	private boolean level3ShareTest(LinkedList<LinkedList<Integer>> origMat, LinkedList<Integer> oriResult,
			LinkedList<Integer> result) {
		boolean find = false;
		LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
		
		for (int i=0; i<origMat.size(); i++) {
			LinkedList<LinkedList<Integer>> backupMat1 = cloneMat(origMat);
			deleteRowCol(backupMat1, i);
			
			LinkedList<Integer> backupRes1 = (LinkedList<Integer>) oriResult.clone();
			backupRes1.remove(i);
			
			for (int j=0; j<backupMat1.size()-1; j++) {
				LinkedList<LinkedList<Integer>> backupMat2 = cloneMat(backupMat1);
				deleteRowCol(backupMat2, j);
				
				LinkedList<Integer> backupRes2 = (LinkedList<Integer>) backupRes1.clone();
				backupRes2.remove(j);
				
				for (int k=0; k<backupMat2.size()-1; k++) {
					shareMat = cloneMat(backupMat2);
					result = (LinkedList<Integer>) backupRes2.clone();
					
					deleteRowCol(shareMat, k);
					result.remove(k);
					
					if (!containsZero(shareMat)) {
						find = true;
						return find;
					}
				}
			}
		}
		
		return find;
	}
	

	@SuppressWarnings("unchecked")
	private boolean level4ShareTest(LinkedList<LinkedList<Integer>> origMat, LinkedList<Integer> oriResult,
			LinkedList<Integer> result) {
		boolean find = false;
		LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
		
		for (int i=0; i<origMat.size(); i++) {
			LinkedList<LinkedList<Integer>> backupMat1 = cloneMat(origMat);
			deleteRowCol(backupMat1, i);
			
			LinkedList<Integer> backupRes1 = (LinkedList<Integer>) oriResult.clone();
			backupRes1.remove(i);
			
			for (int j=0; j<backupMat1.size()-1; j++) {
				LinkedList<LinkedList<Integer>> backupMat2 = cloneMat(backupMat1);
				deleteRowCol(backupMat2, j);
				
				LinkedList<Integer> backupRes2 = (LinkedList<Integer>) backupRes1.clone();
				backupRes2.remove(j);
				
				for (int k=0; k<backupMat2.size()-1; k++) {
					LinkedList<LinkedList<Integer>> backupMat3 = cloneMat(backupMat2);
					deleteRowCol(backupMat3, k);
					
					LinkedList<Integer> backupRes3 = (LinkedList<Integer>) backupRes2.clone();
					backupRes3.remove(k);
					
					for (int l=0; l<backupMat3.size()-1; l++) {
						shareMat = cloneMat(backupMat3);
						result = (LinkedList<Integer>) backupRes3.clone();
						
						deleteRowCol(shareMat, l);
						result.remove(l);
						
						if (!containsZero(shareMat)) {
							find = true;
							return find;
						}
					}
				}
			}
		}
		
		return find;
	}
	

	@SuppressWarnings("unchecked")
	private boolean level5ShareTest(LinkedList<LinkedList<Integer>> origMat, LinkedList<Integer> oriResult,
			LinkedList<Integer> result) {
		boolean find = false;
		LinkedList<LinkedList<Integer>> shareMat = new LinkedList<LinkedList<Integer>>();
		
		for (int i=0; i<origMat.size(); i++) {
			LinkedList<LinkedList<Integer>> backupMat1 = cloneMat(origMat);
			deleteRowCol(backupMat1, i);
			
			LinkedList<Integer> backupRes1 = (LinkedList<Integer>) oriResult.clone();
			backupRes1.remove(i);
			
			for (int l0=0; l0<backupMat1.size()-1; l0++) {
				LinkedList<LinkedList<Integer>> backupMat2 = cloneMat(backupMat1);
				deleteRowCol(backupMat2, l0);
				
				LinkedList<Integer> backupRes2 = (LinkedList<Integer>) backupRes1.clone();
				backupRes2.remove(l0);
				
				for (int l1=0; l1<backupMat2.size()-1; l1++) {
					LinkedList<LinkedList<Integer>> backupMat3 = cloneMat(backupMat2);
					deleteRowCol(backupMat3, l1);
					
					LinkedList<Integer> backupRes3 = (LinkedList<Integer>) backupRes2.clone();
					backupRes3.remove(l1);
					
					for (int l2=0; l2<backupMat3.size()-1; l2++) {
						LinkedList<LinkedList<Integer>> backupMat4 = cloneMat(backupMat3);
						deleteRowCol(backupMat4, l2);
						
						LinkedList<Integer> backupRes4 = (LinkedList<Integer>) backupRes3.clone();
						backupRes4.remove(l2);
						
						for (int l3=0; l3<backupMat3.size()-1; l3++) {
							shareMat = cloneMat(backupMat3);
							result = (LinkedList<Integer>) backupRes3.clone();
							
							deleteRowCol(shareMat, l3);
							result.remove(l3);
							
							if (!containsZero(shareMat)) {
								find = true;
								return find;
							}
						}
					}
				}
			}
		}
		
		return find;
	}
	
	private void deleteRowCol(LinkedList<LinkedList<Integer>> x, int idx) {
		x.remove(idx);
		for (int i=0; i<x.size(); i++)
			x.get(i).remove(idx);
	}
	
	private LinkedList<LinkedList<Integer>> cloneMat(LinkedList<LinkedList<Integer>> x) {
		LinkedList<LinkedList<Integer>> res = new LinkedList<LinkedList<Integer>>();
		for (int i=0; i<x.size(); i++) {
			@SuppressWarnings("unchecked")
			LinkedList<Integer> col = (LinkedList<Integer>) x.get(i).clone();
			res.add(col);
		}
		return res;
	}
	
	private boolean containsZero(LinkedList<LinkedList<Integer>> m) {
		for (LinkedList<Integer> x:m) {
			if (x.contains(0))
				return true;
		}
		return false;
	}
	/**
	 * Test two FIFOs to see if they can be shared
	 * @param a
	 * @param b
	 * @return
	 */
	private int testShare(FIFO a, FIFO b) {
		Vector<OrderedFIFOAccess> writes = new Vector<OrderedFIFOAccess>();
		Vector<OrderedFIFOAccess> reads = new Vector<OrderedFIFOAccess>();
		for (int i=0; i<a.writes.size(); i++) {
			writes.add(new OrderedFIFOAccess(a.writes.get(i), a));
		}
		for (int i=0; i<b.writes.size(); i++) {
			writes.add(new OrderedFIFOAccess(b.writes.get(i), b));
		}
		Collections.sort(writes);
		for (int i=0; i<a.reads.size(); i++) {
			reads.add(new OrderedFIFOAccess(a.reads.get(i), a));
		}
		for (int i=0; i<b.reads.size(); i++) {
			reads.add(new OrderedFIFOAccess(b.reads.get(i), b));
		}
		Collections.sort(reads);
		
		assert writes.size() == reads.size();
		
		int preRead=-1;
		for (int i=0; i<writes.size(); i++) {
			OrderedFIFOAccess curRead =  reads.get(i);
			if (writes.get(i).fifo != curRead.fifo) {
				return 0;
			}
			if (preRead ==curRead.ord) {
				// Possibly read from two FIFOs occur at the same time.
				return 0;
			}
			preRead = curRead.ord;
		}
		return 1;
	}
	
	/**
	 * Only the cycle information of FIFO access instructions are needed. A complicate case 
	 * is the PUT or GET inside a repeat segment. 
	 */
	public void parseCycleInfo() {
		for (SPU spu : spus) {
			Assembly asm = spu.asm;
			asm.cycleInRPTSegs();
			int cyc = 0;
			for (AsmInstr I : asm.asmInstrs) {
				if (I instanceof RptedInst) {
					if (I.rptLev.insts.indexOf(I) == 0 && I.rptLev.levl == 0) {
						// If this is the first instruction inside a repeat segment, set the 
						// base cycle information for this segment.
						I.rptLev.container.baseCycle = cyc;
						cyc += I.rptLev.container.length;
					}
					I.cycle = ((RptedInst) I).offset + I.rptLev.container.baseCycle;
				} else {
					I.cycle = cyc;
					cyc ++;
				}
			}
			
			AsmInstr last = asm.asmInstrs.getLast();
			if (last instanceof RptedInst) {
				// Because JUMP is added after FIFO synchronisation, so the last instruction may 
				// be a repeated instruction, whose cycle does not consider the outermost loop.
				asm.loopLen = last.cycle + 1 + (last.rptLev.container.length-last.rptLev.length);
			} else {
				asm.loopLen = last.cycle;		
			}			
		}
	}
	
	public void printInstEncoding(String file) {
		
		for (SPU spu : spus) {
			Assembly asm = spu.asm;
			sspInstTypes.addAll(asm.instTypes);
		}
		if (!conf.noIOCore) {
			sspInstTypes.addAll(ioCore.asm.instTypes);
		}
		
		sspInstTypes.remove(SPUInst.NOP);
		EnumSet<SPUInst> notUsedInstTypes = EnumSet.complementOf(sspInstTypes);
		notUsedInstTypes.remove(SPUInst.NOP);
		ArrayList<SPUInst> tmpList = new ArrayList<SPUInst>(sspInstTypes);
		
		StringBuffer code = new StringBuffer();
		
		code.append("library ieee;\r\n" + 
		"use ieee.std_logic_1164.all;\r\n" + 
		"use ieee.numeric_std.all;\r\n" + 
		"\r\n" + 
		"package m_word_config is\r\n" + 
		"\r\n" + 
		"---------------------------------------------------------\r\n" + 
		"-- Type definition\r\n" + 
		"--------------------------------------------------------- \r\n" + 
		"  type VDATA_TYPE is array (natural range <>) of std_logic_vector(" + (conf.coreWidth-1) + " downto 0);\r\n" + 
		"  type VSIG_TYPE is array (natural range <>) of std_logic;\r\n" + 
		"  \r\n" + 
		"---------------------------------------------------------\r\n" + 
		"-- Instruction Encoding\r\n" + 
		"---------------------------------------------------------\r\n"
		);
		
		code.append(_encodingLine("NOP", 0));
		
		for (SPUInst inst : tmpList) {			
			code.append(_encodingLine(inst.name(), tmpList.indexOf(inst)+1));
		}
		
		for (SPUInst inst : notUsedInstTypes) {
			code.append(_encodingLine(inst.name(), 63));
		}
		
		code.append("end;");
		
		SWGenUtils.writeToFile(file, code.toString());
	}
	
	
//	/**
//	 * Fix some configuration parameters after all optimisation done. The list of configurations are:
//	 * 1. DM address width and offset width
//	 * 2. 
//	 */
//	public void finaliseConfig() {
//		for (SPU spu : spus) {
//						
//			
//		}
//	}
	
	private String _encodingLine(String name, int value) {
		return "  constant " + name + " : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(" + value + ", 6));\r\n";
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public variables                  ////
	/** The code generation agent of SSP **/
	public SoftwareGen sg;
	
	/** All instructions used in this application**/
	public EnumSet<SPUInst> sspInstTypes = EnumSet.noneOf(SPUInst.class);
	
	/** The list of contained SPUs */
	public List<SPU> spus = new LinkedList<SPU>();
	
	public SPU ioCore;
	
	/** External input and output FIFOs */
	public List<FIFO> exInFifos =  new LinkedList<FIFO>();
	public List<FIFO> exOutFifos =  new LinkedList<FIFO>();
	
	/** FIFO list in SSP */
	public List<FIFO> fifos = new LinkedList<FIFO>();
	
	/** SSP configuration */
	public SSPConfig conf = new SSPConfig();
	
	/** Store transition records. It is used for FIFO synchronisation. */
	public List<Transition> trans = new LinkedList<Transition>();
	
	/** The latency of the synthesised SSP **/
	public int latency;
	
	public boolean skipFIFOSync = false;
	public boolean skipShareFIFO = true;
	///////////////////////////////////////////////////////////////////
	////                         private variables                 ////
}
