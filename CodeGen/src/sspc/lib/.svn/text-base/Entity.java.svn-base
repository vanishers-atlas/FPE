package sspc.lib;

import java.io.File;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;


import sspc.lib.Token.DATATYPE;
import sspc.lib.Token.TOKENTYPE;
import sspc.softgen.SWGenUtils;
import sspc.util.XMLUtilities;

/** 
 An Entity is a vertex in a generalized graph. It is an aggregation
 of ports. The ports can be linked to relations. The
 relations thus represent connections between ports, and hence,
 connections between entities. To add a port to an entity, simply
 set its container to the entity.  To remove it, set its container
 to null, or to some other entity.

 @author Peng Wang
 */
public class Entity implements Comparable<Entity>{
	// Test entry
//	public static void main(String[] args) {
//		Entity ent = new Entity("ent1", "myname");
//		System.out.println(ent.getClassName());		
//	}
	
	public Entity(String name, String actorclass) {
		_name = name;
		this.actorClass = actorclass;
		if (name.equals("SOURCE") || name.equals("SINK")) 
			idx = -1;
		else if (actorclass.contains("MotionEstH264"))
			idx = -1;
		else 
			idx = SWGenUtils.getDigits(name);
    }
	
	/** Get the name. If no name has been given, or null has been given,
     *  then return an empty string, "".
     *  @return The name of the object.
     *  @see #setName(String)
     */
    public String getName() {
        return _name;
    }
	

    /** List all the input ports.
     *  @return A list of input Port objects.
     */
    public List<Port> inputPortList() {
        return _inputPortList;
    }
    
    /** List all the output ports.
     *  @return A list of output Port objects.
     */
    public List<Port> outputPortList() {
        return _outputPortList;
    }
    
    /** List all the input ports.
     *  @return A list of input Port objects.
     */
    public List<Port> getPorts() {
        return _portList;
    }
    
	public void addInputPort(Port port) {
		if (_inputPortList == null) {
			_inputPortList = new LinkedList<Port>();
        }
		_inputPortList.add(port);
		_portList.add(port);
	}
	
	public void addOutputPort(Port port) {
		if (_outputPortList == null) {
			_outputPortList = new LinkedList<Port>();
        }
		_outputPortList.add(port);
		_portList.add(port);
	}
	
	public void addParameter(Parameter para) {
		_parameterList.add(para);
	}
	
	public Parameter getParameter(String name) {
		// Do a linear search
        Iterator<Parameter> iterator = _parameterList.iterator();

        while (iterator.hasNext()) {
            Parameter obj = iterator.next();

            if (name.equals(obj.getName())) {
                return obj;
            }
        }
        
        return null;
	}
	
	/** List all the input ports.
     *  @return A list of input Port objects.
     */
    public List<Parameter> parameterList() {
        return _parameterList;
    }
	
	public void setOwnedPE(PE pe) {
		_ownedPE = pe;
	}
	
	public PE getOwnedPE() {
		return _ownedPE;
	}
	
	/** Return the port contained by this entity that has the specified name.
     *  If there is no such port, return null.
     *  @param name The name of the desired port.
     *  @return A port with the given name, or null if none exists.
     */
    public Port getPort(String name) {
    	// Do a linear search
        Iterator<Port> iterator = _portList.iterator();

        while (iterator.hasNext()) {
            Port obj = iterator.next();

            if (name.equals(obj.getName())) {
                return obj;
            }
        }
        
        return null;
    }
    
    public boolean isInPE0() {
    	boolean b = (_ownedPE.idx == 0)? true:false;
    	return b;
    }
    
    /**
     * Return true if all inputs are inner for the owner PE.
     * @return
     */
    public boolean areInputsInner() {
    	for (Port in : _inputPortList) {
    		PE srcPE = in.getConnectedPortList().get(0).getPE();
    		if (!srcPE.equals(_ownedPE)) {
				return false;
			}				
    	}
    	return true;
    }
    
    /**
     * Return true if all outputs are inner for the owner PE.
     * @return
     */
    public boolean areOutputsInner() {
    	for (Port out : _outputPortList) {
    		PE sinkPE = out.getConnectedPortList().get(0).getPE();
    		if (!sinkPE.equals(_ownedPE)) {
				return false;
			}
    	}
    	return true;
    }
    
    /**
     * Return input connected entities. Return a set which has no same elements.
     * @return
     */
    public LinkedList<Entity> getInputEntities() {
    	LinkedList<Entity> ents = new LinkedList<Entity>();
    	for (Port in : _inputPortList) {
    		Entity ent = in.getConnectedPort(0).getContainer();
    		if (!ents.contains(ent)) {
    			ents.add(ent);
    		}
    	}
    	return ents;
    }
    
    /**
     * To sort entities by its idx.
     * @param arg0
     * @return
     */
	@Override
	public int compareTo(Entity ent) {
		return idx - ent.idx;
	}
	
	public void parseActor(String actorclass) {
		File dir = new File(actorclass.replaceAll("\\.", "//") + ".xml");
		Document moml = XMLUtilities.readXMLDocument(dir);
		
		// Parse ports
		NodeList portList = moml.getElementsByTagName("port");
		for (int i = 0; i < portList.getLength(); i++) {
			Element ePort = (Element) portList.item(i);
			Port port = new Port(this, ePort.getAttribute("name"));
			NodeList propertyList = ePort.getElementsByTagName("property");
			String mathtype = new String("");
			
			for (int j = 0; j < propertyList.getLength(); j++) {
				Element eProperty = (Element) propertyList.item(j);
								
				if (eProperty.getAttribute("name").equals("direction") && eProperty.getAttribute("value").equals("in")) {
					// Set input port
					port.setInput(true);
					addInputPort(port);					
				} else if (eProperty.getAttribute("name").equals("direction") && eProperty.getAttribute("value").equals("out")) {
					// Set output port
					port.setOutput(true);
					addOutputPort(port);
					// FIXME: Yun misuses datatype and mathtype
				} else if (eProperty.getAttribute("name").equals("mathtype")) {					
					// Mathtype is merged with datatype
					if (eProperty.getAttribute("value").equals("complex"))
						mathtype = "complex ";
				} else if (eProperty.getAttribute("name").equals("datatype")) {
					port.token.dataType = DATATYPE.fromString(mathtype + eProperty.getAttribute("value"));
				} else if (eProperty.getAttribute("name").equals("tokentype")) {
					// Set tokentype
					if (eProperty.getAttribute("value").equals("scalar"))
						continue;
					else if (eProperty.getAttribute("value").equals("vector")) {
						port.token.tokenType = TOKENTYPE.VECTOR;
						Element eDim0 = (Element) eProperty.getElementsByTagName("property").item(0);
						port.token.dim0 = Integer.parseInt(eDim0.getAttribute("value"));
					}
					else if (eProperty.getAttribute("value").equals("matrix")) {
						port.token.tokenType = TOKENTYPE.MATRIX;
						Element eDim0 = (Element) eProperty.getElementsByTagName("property").item(0);
						port.token.dim0 = Integer.parseInt(eDim0.getAttribute("value"));
						Element eDim1 = (Element) eProperty.getElementsByTagName("property").item(1);
						port.token.dim1 = Integer.parseInt(eDim1.getAttribute("value"));
					}
				}
			}
		}
		
		// Parse parameters
		NodeList paraList = moml.getElementsByTagName("para");
		for (int i = 0; i < paraList.getLength(); i++) {
			Element ePara = (Element) paraList.item(i);
			String name = ePara.getAttribute("name");
			NodeList propertyList = ePara.getElementsByTagName("property");
			String mathtype = new String("");
			DATATYPE dt = DATATYPE.INT;
			
			for (int j = 0; j < propertyList.getLength(); j++) {
				Element eProperty = (Element) propertyList.item(j);
								
				if (eProperty.getAttribute("name").equals("mathtype")) {					
					// Mathtype is merged with datatype
					if (eProperty.getAttribute("value").equals("complex"))
						mathtype = "complex ";
				} else if (eProperty.getAttribute("name").equals("datatype")) {				
					dt = DATATYPE.fromString(mathtype + eProperty.getAttribute("value"));
				}
			}
			this.addParameter(new Parameter(this, name, dt));			
		}
	}
    
	public String getClassName() {
		String className = actorClass.substring(actorClass.lastIndexOf(".")+1);
		return className;
	}
    ///////////////////////////////////////////////////////////////////
    ////                         public  variables                ////  
    /** Entity index in the graph */
    public int idx;
    
    ///////////////////////////////////////////////////////////////////
    ////                         private  variables                ////

    /** A list of ports owned by this Entity. */
    private List<Port> _inputPortList;
    private List<Port> _outputPortList;
    private List<Port> _portList = new LinkedList<Port>();
    
    /** A list of parameters owned by this Entity.
     *  Note, the list can be null.
     */
    private List<Parameter> _parameterList = new LinkedList<Parameter>();
    
    /** The processor which contains this entity */
    private PE _ownedPE;
    
    private String _name;
    public String actorClass;
}
