package sspc.lib.dsp;

import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import sspc.util.XMLUtilities;

public class MatrixMult {
	public MatrixMult(int penum, int blknum, MMType func) {
		// it could be 32x32 blocks, but only 16 PEs
		peNum = penum;
		actorNumInEachPE = blknum;
		totalActorNum = penum*actorNumInEachPE;
		
		type = func;
		_edgeNum = totalActorNum*3;
	}
	
	/** Construct the graph in MoML format.
	 *  Block number equals PE number.
     */
	public void graphGen(String outName) throws ParserConfigurationException {	  
		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
	
		//root elements
		_xml = docBuilder.newDocument();
		Element rootElement = _xml.createElement("constructure");
		_xml.appendChild(rootElement);
	    rootElement.setAttribute("name", "MatrixMult");

	    // Append structure
	    Element structure = _xml.createElement("structure");
	    rootElement.appendChild(structure);
	    
	    // Generate task elements  
	    // Store the xml components in a list, so that we can operate on them
	    // easily.
	    for (int i=0;i<totalActorNum;i++) {
	    	String str_i = new String(Integer.toString(i));
	    	
	    	Element task = _xml.createElement("entity");
	    	_bfActors.add(task);
	    	task.setAttribute("name", "T"+str_i);
	    	task.setAttribute("class", "actor.MatMult");
	    }	    		   
	    
	    // Generate manual mapping	    
	    _manualMapping(structure);
			    
	    // Generate relation
	    int relIndex = 0;
	    for(int i=0; i<_edgeNum; i++) {
	    	Element relation = _xml.createElement("relation");
	    	structure.appendChild(relation);
	    	relation.setAttribute("name", "r" + Integer.toString(relIndex++));
	    }
	    
	    // Generate links.
	    // Generate source links
	    relIndex = 0;
	    for(int i=0; i<totalActorNum; i++) {
	    	for (int j=0; j<2; j++) {
		    	Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "SOURCE");
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "T"+Integer.toString(i)+".i"+Integer.toString(j));
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	    
	    // Generate inter-task links
	    for(int i=0; i<peNum; i++) {
	    	for (int j=0; j<actorNumInEachPE-1; j++) {
	    		Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "T"+Integer.toString(actorNumInEachPE*i + j)+".o0");
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "T"+Integer.toString(actorNumInEachPE*i + j + 1)+".i2");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	   
	    // Generate sink links
	    for(int i=0; i<peNum; i++) {
	    	Element link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "T"+Integer.toString(actorNumInEachPE*(i+1)-1)+".o0");
			link.setAttribute("relation", "r" + Integer.toString(relIndex));
      
			link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "SINK");
			link.setAttribute("relation", "r" + Integer.toString(relIndex++));	      
	    }
	    
	    // Append interface
	    Element inf = _xml.createElement("interface");
	    rootElement.appendChild(inf);
	    
	    // Add SOURCE and SINK
	    Element source = _xml.createElement("port");
	    inf.appendChild(source);
		source.setAttribute("name", "SOURCE");
		Element prop0 = _xml.createElement("property");
		source.appendChild(prop0);
		prop0.setAttribute("name", "direction");
		prop0.setAttribute("value", "in");
				
		Element sink = _xml.createElement("port");
	    inf.appendChild(sink);
		sink.setAttribute("name", "SINK");
		Element prop1 = _xml.createElement("property");
		sink.appendChild(prop1);
		prop1.setAttribute("name", "direction");
		prop1.setAttribute("value", "out");
		
	    // Output xml file.
	    XMLUtilities.writeXML(_xml, outName); 
	}
	

	
	/**
	 * Create a manual mapping&scheduling output and store in xml format.
	 * When the SIMD way is too wide, split it into copies.
	 */
	private void _manualMapping(Element strucEle) {
		if (peNum > 32) {
			assert peNum == 64;
			int num = peNum/2;
			
			for (int pro = 0; pro < 2; pro++) {
				Element processor = _xml.createElement("processor");
		    	strucEle.appendChild(processor);
		    	processor.setAttribute("name", "SPU"+pro);
				for (int i=0; i<num; i++) {
					Element pe = _xml.createElement("PE");
			    	processor.appendChild(pe);
			    	pe.setAttribute("name", "PE"+Integer.toString(i));
		
			    	for (int j=0; j<actorNumInEachPE; j++)
			    		pe.appendChild(_bfActors.get(pro*num*actorNumInEachPE + actorNumInEachPE*i + j));
			    }
			}
		} else {
			Element processor = _xml.createElement("processor");
	    	strucEle.appendChild(processor);
	    	processor.setAttribute("name", "SPU0");
			for (int i=0; i<peNum; i++) {
				Element pe = _xml.createElement("PE");
		    	processor.appendChild(pe);
		    	pe.setAttribute("name", "PE"+Integer.toString(i));
	
		    	for (int j=0; j<actorNumInEachPE; j++)
		    		pe.appendChild(_bfActors.get(actorNumInEachPE*i + j));
		    }
		}
	}
	
	public int peNum;
	private int totalActorNum;
	private int actorNumInEachPE;
	
	private int _edgeNum;
	
	/* XML object for mapping and scheduling */
	private Document _xml;
	private List<Element> _bfActors = new ArrayList<Element>();
	
	// Matrix multiplication types. M1024 means 1024x1024, B32 means block 32x32, W32 means width is 32 bits.
	public enum MMType {
		M128B2W16, M128B4W16, M128B8W16 , M1024B32W32, test
	}
	public MMType type;
}
