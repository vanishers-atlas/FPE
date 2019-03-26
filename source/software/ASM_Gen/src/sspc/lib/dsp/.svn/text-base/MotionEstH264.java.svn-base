package sspc.lib.dsp;

import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import sspc.util.XMLUtilities;

public class MotionEstH264 {
	public MotionEstH264(MEH264Type func) {
		type = func;
	}
	
	public void graphGen(String outName) throws ParserConfigurationException {	  
		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
	
		//root elements
		_xml = docBuilder.newDocument();
		Element rootElement = _xml.createElement("constructure");
		_xml.appendChild(rootElement);
	    rootElement.setAttribute("name", "MotionEstH264");

	    // Append structure
	    Element structure = _xml.createElement("structure");
	    rootElement.appendChild(structure);
	    
	    // Generate task elements ...
	    // 1st: 32*32 SAD4x4, denotes as A0_0 ...
	    for (int i=0;i<32;i++) {
	    	for (int j=0;j<32;j++) {
		    	String str_i = new String(i+"_"+j);
		    	
		    	Element task = _xml.createElement("entity");
		    	_actors.add(task);
		    	task.setAttribute("name", "A"+str_i);
		    	task.setAttribute("class", "actor.MotionEstH264.SAD4x4");
	    	}	    		   
	    }
	    // 2nd: 32x32 SADcombine, denotes as B0_0
	    for (int i=0;i<32;i++) {
	    	for (int j=0;j<32;j++) {
		    	String str_i = new String(i+"_"+j);
		    	
		    	Element task = _xml.createElement("entity");
		    	_actors.add(task);
		    	task.setAttribute("name", "B"+str_i);
		    	task.setAttribute("class", "actor.MotionEstH264.SADcombine");
	    	}
	    }
	    // 3rd: 32 localMin, denotes as C0 ...
	    for (int i=0;i<32;i++) {
	    	String str_i = new String(i+"");
	    	
	    	Element task = _xml.createElement("entity");
	    	_actors.add(task);
	    	task.setAttribute("name", "C"+str_i);
	    	task.setAttribute("class", "actor.MotionEstH264.localMin");
	    }
	    // 4th: 1 globalMin, denotes as D
	    {	    	
	    	Element task = _xml.createElement("entity");
	    	_actors.add(task);
	    	task.setAttribute("name", "D");
	    	task.setAttribute("class", "actor.MotionEstH264.globalMin");
	    }
	    
	    
	    // Generate manual mapping	    
	    _manualMapping(structure);
			    
	    // Generate links...
	    // 1st: source->SAD4x4
	    int relIndex = 0;
	    for(int i=0; i<32; i++) {
	    	for (int j=0;j<32;j++) {
		    	Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "SOURCE");
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "A"+i+"_"+j+".cur_in");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
				
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "SOURCE");
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "A"+i+"_"+j+".ref_in");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	    // 2nd: SAD4x4->SADcombine
	    for(int i=0; i<32; i++) {
	    	for (int j=0;j<32;j++) {	      
	    		Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "A"+i+"_"+j+".sad4x4_out");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
				
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "B"+i+"_"+j+".sad4x4_in");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	    // 3rd: SADcombine->localMin
	    for(int i=0; i<32; i++) {
	    	for (int j=0;j<32;j++) {	      
	    		Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "B"+i+"_"+j+".sad_out");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
				
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "C"+i+".sad_in"+j);
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    	}
	    }
	    // 4th: localMin->globalMin
	    for (int j=0;j<32;j++) {	      
    		Element link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "C"+j+".localminsad_out");
			link.setAttribute("relation", "r" + Integer.toString(relIndex++));
			
			link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "D"+".sad_in"+j);
			link.setAttribute("relation", "r" + Integer.toString(relIndex++));
    	}
	    	   
	    // 5th: globalMin->sink
	    {
	    	Element link = _xml.createElement("link");
			structure.appendChild(link);
			link.setAttribute("port", "D"+".globalminsad_out");
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
	 * Three types of mapping.
	 * @param strucEle
	 */
	private void _manualMapping(Element strucEle) {
		switch(type) {
		case SINGLE:
			_mappingSingle(strucEle); break;
		case TWO:
			_mappingTwo(strucEle); break;
		case TWOBALANCED:
			_mappingTwoBalanced(strucEle); break;
		}
	}
	
	private void _mappingSingle(Element strucEle) {
		// A,B,C->SPU0		
		Element processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU0");
    	
    	for (int i=0; i<32; i++) {
    		Element pe = _xml.createElement("PE");
	    	processor.appendChild(pe);
	    	pe.setAttribute("name", "PE"+Integer.toString(i));
	    	// A
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(i*32+j));
	    	// B
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(1024+i*32+j));
	    	// C
	    	pe.appendChild(_actors.get(2048+i));
    	}		
    	processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU1");
	    	
		Element pe = _xml.createElement("PE");
    	processor.appendChild(pe);
    	pe.setAttribute("name", "PE0");
    	// D
    	pe.appendChild(_actors.get(2080));	    	
	}
	
	private void _mappingTwo(Element strucEle) {
		// A,B->SPU0 C->SPU1	
		Element processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU0");
    	
    	for (int i=0; i<32; i++) {
    		Element pe = _xml.createElement("PE");
	    	processor.appendChild(pe);
	    	pe.setAttribute("name", "PE"+Integer.toString(i));
	    	// A
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(i*32+j));
	    	// B
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(1024+i*32+j));
    	}		
    	processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU1");
	    
    	for (int i=0; i<32; i++) {
    		Element pe = _xml.createElement("PE");
	    	processor.appendChild(pe);
	    	pe.setAttribute("name", "PE"+Integer.toString(i));

	    	// C
	    	pe.appendChild(_actors.get(2048+i));
    	}
    	
    	processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU2");
    	
		Element pe = _xml.createElement("PE");
    	processor.appendChild(pe);
    	pe.setAttribute("name", "PE0");
    	// D
    	pe.appendChild(_actors.get(2080));
	}
	
	private void _mappingTwoBalanced(Element strucEle) {
		// A->SPU0 B,C->SPU1	
		Element processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU0");
    	
    	for (int i=0; i<32; i++) {
    		Element pe = _xml.createElement("PE");
	    	processor.appendChild(pe);
	    	pe.setAttribute("name", "PE"+Integer.toString(i));
	    	// A
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(i*32+j));
    	}		
    	processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU1");
	    
    	for (int i=0; i<32; i++) {
    		Element pe = _xml.createElement("PE");
	    	processor.appendChild(pe);
	    	pe.setAttribute("name", "PE"+Integer.toString(i));

	    	// B
	    	for (int j=0; j<32; j++)
	    		pe.appendChild(_actors.get(1024+i*32+j));
	    	// C
	    	pe.appendChild(_actors.get(2048+i));
    	}
    	
    	processor = _xml.createElement("processor");
    	strucEle.appendChild(processor);
    	processor.setAttribute("name", "SPU2");
    	
		Element pe = _xml.createElement("PE");
    	processor.appendChild(pe);
    	pe.setAttribute("name", "PE0");
    	// D
    	pe.appendChild(_actors.get(2080));
	}
	
	public enum MEH264Type {
		SINGLE /* SAD and localMin are in a single core */, TWO /* SAD and localMin are in seperate core */,
		TWOBALANCED /* SAD4x4 is in one core, SADcombine and localMin are in the other core*/
	}
	public MEH264Type type;	
	
	/* XML object for mapping and scheduling */
	private Document _xml;
	private List<Element> _actors = new ArrayList<Element>();
}
