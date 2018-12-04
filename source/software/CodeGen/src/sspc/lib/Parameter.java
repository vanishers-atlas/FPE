package sspc.lib;

import sspc.lib.Token.DATATYPE;

public class Parameter {
	
	public Parameter(Entity e, String name, DATATYPE type) {
		_ent = e;
		_name = name;
		dataType = type;
	}
	
	/**
	 * Get the name of this parameter, like W in butterfly.
	 * @return
	 */
	public String getName() {
		return _name;
	}
	
	/**
	 * Get full name of this parameter, including both entity name and parameter
	 * name.
	 * @return
	 */
	public String getFullName() {
		return _ent.getName() + "_" + _name;
	}
	
	public String getValue() {
		return _value;
	}
	
	public void setName(String name) {
		_name = name;
	}
		
	public void setValue(String value) {
		_value = value;
	}
	
	/**When _type is complex, the function returns the real part of the 
	 * complex data.
	 * @return
	 */
	public float getReal() {
		String strReal = _value.substring(0, _value.indexOf(" "));
		return new Float(strReal);
	}
	
	/**When _type is complex, the function returns the imaginary part of the 
	 * complex data.
	 * @return
	 */
	public float getImag() {
		String strImag = _value.substring(_value.indexOf(" "), _value.lastIndexOf("i"))
				.replaceAll(" ", "");
		return new Float(strImag);
	}
	
	/** 
	 * Set this parameter as a constant port.
	 */
	public void setAsPort() {
		_bAsPort = true;
	}
	
	/**
	 * Should this parameter be used as a constant port.
	 * @return
	 */
	public boolean asPort() {
		return _bAsPort;
	}
	
	///////////////////////////////////////////////////////////////////
	////						private variables				   ////
	
	/** The owner entity*/
	private Entity _ent;
	
	private String _name;
	
	public DATATYPE dataType;
	
	private String _value;
	
	/**In order to facilitate SIMD processing, parameter may be passed into FPE
	 * through Constant Port. Practically, this constant port is virtual. After
	 * compilation, the memory locations for parameters are fixed, so these 
	 * locations can be initialised in VHDL avoid adding a real FIFO.  
	 */
	private boolean _bAsPort = false;

}
