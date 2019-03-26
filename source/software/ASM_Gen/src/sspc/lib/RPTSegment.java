package sspc.lib;

import java.util.LinkedList;

public class RPTSegment {
	public RPTLevel getLevel(int idx) {
		return levels.get(idx);
	}
	
	/**
	 * Parse the cycle information of the RPT segment. The cycle information is
	 * composed of two parts: offset and repeat interval. Offset represents the
	 * beginning cycle of this instruction, and repeat interval means how often
	 * it is repeated.
	 */
	public void parseCycle() {
		assert (!insts.isEmpty());
		
		RPTLevel curLev = levels.get(0);
		int cntOfs = -1;
		for (AsmInstr inst : insts) {
			RptedInst I = (RptedInst) inst;
			// Once curLev is decreased, compute the length of last level
			// and add it to offset.
			if (I.rptLev.levl < curLev.levl) {
				cntOfs += 1 +  (curLev.cntNum - 1) * curLev.computeLength(0);
			} else {
				cntOfs ++;				
			}
			I.offset = cntOfs;
			curLev = I.rptLev;
			
			if (insts.getLast() == inst) {
				// The last instruction must be in level 0, as the RPT controller is designed
				// to be not allowed to back multiple levels.
				assert inst.rptLev.levl == 0;
				I.rptLev.length = cntOfs+1;
				length = (cntOfs+1) * I.rptLev.cntNum;
			}
		}
		
		// Add repeat interval info
		for (AsmInstr inst : insts) {
			RptedInst I = (RptedInst) inst;

			I.rptInterval.add(I.rptLev.length);
			RPTLevel levIt = I.rptLev;
			for (int i = 0; i < I.rptLev.levl; i++) {
				levIt = levIt.predLevel;
				I.rptInterval.add(levIt.length);				
			}
		}
	}
	
	public LinkedList<RPTLevel> levels = new LinkedList<RPTLevel>();
	public LinkedList<AsmInstr> insts = new LinkedList<AsmInstr>();
	
	// Record the beginning cycle of this segment in the entire assembly.
	public int baseCycle;
	
	// The whole length of this segment, which is length(lev0) * cnt(lev0)
	public int length;
	// The number of levels in this segment. Note it is not levels.size() as
	// there may be parallel levels.
	public int levlNum = 1;
}
