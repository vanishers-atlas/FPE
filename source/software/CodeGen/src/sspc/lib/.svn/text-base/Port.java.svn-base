package sspc.lib;

import java.util.LinkedList;
import java.util.List;


public class Port {
	
	public Port(Entity container, String name, boolean isInput, 
            boolean isOutput) {
        _container = container;
        _name = name;
        setInput(isInput);
        setOutput(isOutput);
	}
	
	public Port(Entity container, String name) {
        _container = container;
        _name = name;
	}
	///////////////////////////////////////////////////////////////////
	////                         public methods                    ////
	
	public Entity getContainer() {
        return _container;
    }
	
	/**
	 * Get the FPE containing this port. This function can only be called 
	 * after mapping MoML has been parsed.
	 * @return
	 */
	public SPU getFPE() {
		return _container.getOwnedPE().getSPU();
	}
	
	/**
	 * Get the PE containing this port. This function can only be called 
	 * after mapping MoML has been parsed.
	 * @return
	 */
	public PE getPE() {
		return _container.getOwnedPE();
	}
	
	public String getName() {
        return _name;
    }	
	
	public String getFullName() {
		String fullName = _name;
		fullName = getContainer().getName() + "." + fullName;
		return fullName;
	}
	
	public void setInput(boolean isInput) {
        _isInput = isInput;
    }
	
	public void setOutput(boolean isOutput) {
        _isOutput = isOutput;
    }
	
	public boolean isInput() {
        return _isInput;
    }
	
	public boolean isOutput() {
        return _isOutput;
	}
	
	public List<Port> getConnectedPortList() {
		return _connectedPortlist;
	}
	
	/**
	 * Get specified port
	 * @param i
	 * @return
	 */
	public Port getConnectedPort(int i) {
		return _connectedPortlist.get(i);
	}
	
	public void addConnectedPort(Port port) {
		_connectedPortlist.add(port);
	}
	
	///////////////////////////////////////////////////////////////////
	////                         public variables                  ////
	public Token token = new Token(this);
	
	/**
	 * Flag to indicate input communication code has already generated for this
	 * port. When there was a congestion in accessing FIFO, it means for example
	 * in order to fire actor a, the token for actor b has to be read out from
	 * FIFO first. So when this happened, the input code may have been
	 * generated as a side effect of previous actor code generation.
	 */
	public boolean codeGenerated = false;
	
	/** The connected FIFO of this port. Only one FIFO can be connected. */
	public FIFO connectedFIFO;
	
	///////////////////////////////////////////////////////////////////
	////                         private variables                 ////
	private boolean _isInput;
	private boolean _isOutput;
	
	/* The instance name of the entity class this port belongs to. */
	private Entity _container;
	
	/* This is the name of the port. */
	private String _name;		
	
	/* The connected port list */
	private List<Port> _connectedPortlist = new LinkedList<Port>();
	
}
