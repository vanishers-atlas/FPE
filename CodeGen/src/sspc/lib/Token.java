package sspc.lib;

import sspc.lib.SPUConfig.ALUTYPE;

public class Token {
	public Token(Port p) {
		port = p;
	}
	public Token(Port p, DATATYPE d) {
		port = p;
		dataType = d;
		tokenType = TOKENTYPE.SCALAR;
		dim0 = 1;
		dim1 = 1;
	}
	
	public Token(Port p, DATATYPE d, TOKENTYPE t, int pdim0, int pdim1) {
		port = p;
		dataType = d;
		tokenType = t;
		dim0 = pdim0;
		dim1 = pdim1;
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////

	public int getNumData(ALUTYPE ct){
		if (ct == ALUTYPE.REAL16B1D && DATATYPE.isCplx(dataType))
			// Need to get real and image separately.
			return dim0*dim1*2;
		else
			return dim0*dim1;
	}
	
	public int ridx() {
		return _ridx;
	}
	
	public void setridx(int idx) {
		_ridx=idx;
	}
	
	
    ///////////////////////////////////////////////////////////////////
    ////                         public variables                 ////
	
	/**
	 * 
	 */
	public DATATYPE dataType = DATATYPE.INT;
	
	public TOKENTYPE tokenType = TOKENTYPE.SCALAR;
	
	/** The port this token to which belongs */ 
	public Port port; 
	
	// This variable is used for conflict fifo allocation. It is the read sequence
	// in the sink PE.
	private int _ridx = -1;
	
	/**
	 *  Data type Enum  
	 */
	public enum DATATYPE {
		INT ("int"), 
		FLOAT("float"),
		DOUBLE("double"), 
		CPLXINT("complex int"), 
		CPLXFLOAT("complex float"), 
		CPLXDOUBLE("complex double");
		
		private String text;
		DATATYPE(String text) {     
			this.text = text; 
		}
		
		public static boolean isCplx(DATATYPE dt) {
			if (dt == CPLXINT || dt == CPLXFLOAT || dt == CPLXDOUBLE)
				return true;
			return false;
		}

		public static DATATYPE fromString(String text) {
			if (text != null) {
				for (DATATYPE b : DATATYPE.values()) {
					if (text.equalsIgnoreCase(b.text)) {
						return b;
					}
				}
			}
			throw new IllegalArgumentException("No constant with text " + text
					+ " found");
		}
	}
	
	/**
	 *  Token type Enum
	 */
	public enum TOKENTYPE {
		SCALAR("scalar"), VECTOR("vector"), MATRIX("matrix");
		
		private String text;
		
		TOKENTYPE(String text) {     
			this.text = text; 
		}
		public static TOKENTYPE fromString(String text) {
			if (text != null) {
				for (TOKENTYPE b : TOKENTYPE.values()) {
					if (text.equalsIgnoreCase(b.text)) {
						return b;
					}
				}
			}
			throw new IllegalArgumentException("No constant with text " + text
					+ " found");
		}
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         private variables                 ////
	/** 
	 * The dimension size if any
	 */
	public int dim0 = 1;
	public int dim1 = 1;
	

}
