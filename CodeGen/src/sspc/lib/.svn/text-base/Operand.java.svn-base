package sspc.lib;

import sspc.softgen.SWGenUtils;

public class Operand {
	public Operand(String str, char modi) {
		this.str = str;
		this.modifier = modi;
	}
	
	public void setSMFields() {
		String sub = str.substring(str.indexOf("#") + 1);
		int bg = sub.indexOf("(");
		if (bg != -1) {
			smSPIdx = Integer.parseInt(sub.substring(bg+1,bg+2));
			smSPAutoinc = (sub.indexOf("!") != -1);
		} else {
			// Immediate value
			imVal = sub;
		}
	}
	
	/**
	 * Two formats.
	 * 1. &(d[!]) for indexed memory operation
	 * 2. &d for direct memory operation
	 */
	public void setDMFields() {
		String sub = str.substring(str.indexOf("&") + 1);
		int bg = sub.indexOf("(");
		if (bg != -1) {
			dmSPIdx = Integer.parseInt(sub.substring(bg+1,bg+2));
			dmSPAutoinc = (sub.indexOf("!") != -1);
		} else {
			dmSPOfs = Integer.parseInt(sub);
		}
	}

	public void setEMFields() {
		int bg = str.indexOf("(");
		if (bg != -1) {
			emSPIdx = Integer.parseInt(str.substring(bg+1,bg+2));
		} else {
			throw new RuntimeException("ERROR: EM operand format (sp0!).");
		}
		
		emSPAutoinc = (str.indexOf("!") != -1);
	}
	
	public void setChFields() {
		int bg = str.indexOf("(");
		if (bg != -1) {
			// Do nothing as there is only one channel pointer
			chAutoinc = (str.indexOf("!") != -1);
		} else {
			chNo = SWGenUtils.getIntOfString(str);
		}
	}
	
	public boolean strEqual(Operand ref) {
		return str.equals(ref.str);
	}
	
	public boolean isReg() {
		return modifier == 'R';
	}
	
	public boolean isMem() {
		return modifier == 'M';
	}
	
	// If the SM operand has no SPIdx setting, we can know it is an immediate
	public boolean isImm() {
		return modifier == 'I' && smSPIdx == -1;
	}
	
	public boolean isXOp() {
		return modifier == 'X';
	}
	
	public String str;
	public char modifier;
	
	public boolean isUse = false;
	public boolean isDef = false;
	
	public String imVal; // The immediate value
	public int smSPIdx = -1;
	public int smSPOfs = 0; // The location in SM
	public boolean smSPAutoinc = false;
	
	public int dmSPIdx = 0;
	public int dmSPOfs = 0;
	public boolean dmSPAutoinc = false;
	
	public int emSPIdx = 0;
	public boolean emSPAutoinc = false;
	
	public boolean chAutoinc = false;
	public int chNo = 0;
	
	public int rptEndWidth = 0;
}
