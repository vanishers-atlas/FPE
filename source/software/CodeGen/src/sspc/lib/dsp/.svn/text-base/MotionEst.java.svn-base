package sspc.lib.dsp;

import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import sspc.util.XMLUtilities;

public class MotionEst {
	public MotionEst(int actorNum, METype func) {
		type = func;
		_actorNum = actorNum;
		_edgeNum = actorNum*3;
	}
	
	public void graphGen(String outName) throws ParserConfigurationException {	  
		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
	
		//root elements
		_xml = docBuilder.newDocument();
		Element rootElement = _xml.createElement("constructure");
		_xml.appendChild(rootElement);
	    rootElement.setAttribute("name", "MotionEst");

	    // Append structure
	    Element structure = _xml.createElement("structure");
	    rootElement.appendChild(structure);
	    
	    // Generate task elements  
	    // Store the xml components in a list, so that we can operate on them
	    // easily.
	    for (int i=0;i<_actorNum;i++) {
	    	String str_i = new String(Integer.toString(i));
	    	
	    	Element task = _xml.createElement("entity");
	    	_bfActors.add(task);
	    	task.setAttribute("name", "T"+str_i);
	    	task.setAttribute("class", "actor.MotionEst");
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
	    for(int i=0; i<_actorNum; i++) {
	    	for (int j=0; j<2; j++) {
		    	Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "SOURCE");
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "T"+Integer.toString(i)+".i"+j);
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	    	   
	    // Generate sink links
	    for(int i=0; i<_actorNum; i++) {
	    	Element link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "T"+i+".o0");
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
	
	private void _manualMapping(Element strucEle) {		
		int spuNum;
		int avNum;
		int peNumLast;
		spuNum = (int) Math.ceil(_actorNum/32.0);
		avNum = _actorNum/spuNum;
		peNumLast = _actorNum%avNum+avNum;
		
		for (int pro = 0; pro < spuNum; pro++) {
			Element processor = _xml.createElement("processor");
	    	strucEle.appendChild(processor);
	    	processor.setAttribute("name", "SPU"+pro);
	    	
	    	int peNum = (pro == spuNum-1)? peNumLast : avNum;
	    	
			for (int i=0; i<peNum; i++) {
				Element pe = _xml.createElement("PE");
		    	processor.appendChild(pe);
		    	pe.setAttribute("name", "PE"+Integer.toString(i));
		    	pe.appendChild(_bfActors.get(pro*avNum+i));
		    }
		}
	}
	
	public enum METype {
		BASIC, BASIC_RGB, BASIC_SHARE4, DUALDM, DUALDM_CA,
		DUALDM_CA_RGB, DUALDM_CA_OVERLAPPED
	}
	public METype type;
	
	private int _actorNum;
	private int _edgeNum;
	
	/* XML object for mapping and scheduling */
	private Document _xml;
	private List<Element> _bfActors = new ArrayList<Element>();
}
