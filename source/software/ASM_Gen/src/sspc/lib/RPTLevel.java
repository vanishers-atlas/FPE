package sspc.lib;

import java.util.LinkedList;

public class RPTLevel {
	public RPTLevel(RPTSegment container, int levl) {
		this.container = container;
		this.levl = levl;
	}
	
	public void addInst(AsmInstr I) {
		insts.add(I);
		container.insts.add(I);
		I.rptLev = this;
	}
	
	/**
	 * When a nested loop occurs, establish the predecessor and successor
	 * relationship.
	 * @param lev
	 */
	public void addSuccLev(RPTLevel lev) {
		succLevels.add(lev);
		lev.predLevel = this;
	}
	
	/**
	 * Use recursion to get the length of this level. Results is cached in length;
	 * cnt must be 0 for the first call;
	 * @return
	 */
	public int computeLength(int cnt) {			
		for (RPTLevel succ : succLevels) {
			cnt += succ.cntNum * succ.computeLength(cnt);			
		}
		cnt += insts.size();
		length = cnt;
		return cnt;
	}
	
	public AsmInstr rptInst;
	public int levl;
	public int cntNum;
	public int endLoc;
	
	public LinkedList<AsmInstr> insts = new LinkedList<AsmInstr>();
	
	public RPTSegment container;
	public RPTLevel predLevel;
	public LinkedList<RPTLevel> succLevels = new LinkedList<RPTLevel>();
	// Length equals instructions + all sub rpts.
	public int length;
	public int offset;
}
