package sspc.lib.dsp;

import java.lang.Math;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.*;

import org.w3c.dom.*;

import sspc.math.Complex;
import sspc.util.*;

public class FFT {

	public FFT(int size, int parNum) {
		pointSize = size;
		_stages = (int) (Math.log(pointSize)/Math.log(2));
		_FPENum = parNum;
		_actorPerStage = size/2;
		_actorPerPEPerStage = _actorPerStage/parNum;
		_ws = new Complex[size/2];
		initW();
	}
	
	// Constructor for SIMD FFT
	// Note the argument stageSpan. SIMD spanning multiple stages is constrained
	// by the maximum possible number of sharing stages, which is 
	// log2(actorPerPEPerStage) + 1. E.g. 1024-point FFT in 16 way SIMDs, maximum
	// sharing stages are 6.
	public FFT(int size, int stageSpan, int wayNum) {
		pointSize = size;
		_stages = (int) (Math.log(pointSize)/Math.log(2));
		_ws = new Complex[size/2];
		
		simdWayNum = wayNum;
		
		_actorPerStage = size/2;
		_actorPerPEPerStage = _actorPerStage/simdWayNum;
		_maxShare = (int) (Math.log(_actorPerPEPerStage)/Math.log(2)) + 1;
		
		// stageSpan must be able to divided by maxShare without reminder
		if (stageSpan > _maxShare || _maxShare%stageSpan != 0)
				throw new RuntimeException("Wrong argument for SIMD FFT!");
		_SIMDNum = _maxShare/stageSpan + _stages - _maxShare;
		_stageSpan = stageSpan;		
		bSIMD = true;
		initW();
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         public methods                    ////
	public void init(FFTType fftFireType, boolean bShareCoesWhenPossible) {
		type = fftFireType;
		this.bShareCoesWhenPossible = bShareCoesWhenPossible;
		
		int B = pointSize / 2;
		// The point is the butterfly actor index which is the actor starts to
		// set their parameter as private.
		coeSharePoint = (int) ((Math.log(B/simdWayNum) / Math.log(2)+1)*B);
	}
	
	/** Construct the FFT graph in MoML format.
     */
	public void fftGraphGen(String outName) throws ParserConfigurationException {
	    int nodeNum = pointSize/2*_stages;
	    int edgeNum = (nodeNum+pointSize/2)*2;
	  
		DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
	
		//root elements
		_xml = docBuilder.newDocument();
		Element rootElement = _xml.createElement("constructure");
		_xml.appendChild(rootElement);
	    rootElement.setAttribute("name", "FFT");

	    // Append structure
	    Element structure = _xml.createElement("structure");
	    rootElement.appendChild(structure);
	    
	    // Generate task elements  
	    // Store the xml components in a list, so that we can operate on them
	    // easily.
	    for (int i=0;i<nodeNum;i++) {
	    	String str_i = new String(Integer.toString(i));
	    	
	    	Element task = _xml.createElement("entity");
	    	_bfActors.add(task);
	    	task.setAttribute("name", "T"+str_i);
	    	task.setAttribute("class", "actor.Butterfly");
	    }
	
	    // coefficient
	    int idx =0;
	    for(int i=0;i< _stages;i++)
	    {
	    	int l=( 1<<i );
	    	for(int j=0;j < pointSize;j+= (l<<1) )
	    	{
	    		for(int k=0;k<l;k++)
	    		{
	    		    Element property = _xml.createElement("property");
	    		    _bfActors.get(idx++).appendChild(property); 
	    		    property.setAttribute("name", "W");
	    		    float real = (float) _ws[pointSize*k/2/l].re;
	    		    float imag = (float) _ws[pointSize*k/2/l].im;
	    		    String v = new Complex(real, imag).toString();
	    		    property.setAttribute("value", v);
	    		    /* FIXME: Add the fixed-point and complex support */
	    		}
	    	}
	    }
	    
	    // Generate manual mapping	    
	    _fftManualMapping(structure);
		
	    
	    // Generate relation
	    int relIndex = 0;
	    for(int i=0; i<edgeNum; i++) {
	    	Element relation = _xml.createElement("relation");
	    	structure.appendChild(relation);
	    	relation.setAttribute("name", "r" + Integer.toString(relIndex++));
	    }

	    // Generate links.
	    // Generate source links
	    relIndex = 0;
	    for(int i=0; i<pointSize/2; i++) {
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
	    for(int i=1;i< _stages;i++)
	    {
	    	int l=( 1<<i );
	    	for(int j=0;j < pointSize;j+= (l<<1) )
	    	{
	    		for(int k=0;k<(l>>1);k++)
	    		{
	    			int source_index = (i-1)*pointSize/2+(j>>1)+k;
	    			int sink_index = i*pointSize/2+(j>>1)+k;
	    			
	    			// pair 0
	    			Element link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(source_index)+".o0");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex));
	    			
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(sink_index)+".i0");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	          	    
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(source_index+(l>>1))+".o0");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex));
	    			
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(sink_index)+".i1");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex++));	    				         	        
	    			
	    			// pair 1
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(source_index)+".o1");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex));
	    			
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(sink_index+(l>>1))+".i0");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	          	    
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(source_index+(l>>1))+".o1");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex));
	    			
	    			link = _xml.createElement("link");
	    			structure.appendChild(link);
	    			link.setAttribute("port", "T"+Integer.toString(sink_index+(l>>1))+".i1");
	    			link.setAttribute("relation", "r" + Integer.toString(relIndex++));
	    		}
	    	}
    	}
	    	    
	    // Generate sink links
	    for(int i=0; i<pointSize/2; i++) {
	    	for (int j=0; j<2; j++) {
		    	Element link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "T"+Integer.toString(pointSize/2*(_stages-1)+i)+".o"+Integer.toString(j));
				link.setAttribute("relation", "r" + Integer.toString(relIndex));
	      
				link = _xml.createElement("link");
				structure.appendChild(link);
				link.setAttribute("port", "SINK");
				link.setAttribute("relation", "r" + Integer.toString(relIndex++));	      
	    	}
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
	 */
	private void _fftManualMapping(Element strucEle) {
		if (bSIMD) {
			for (int idxSIMD=0; idxSIMD<_SIMDNum; idxSIMD++) {
				Element processor = _xml.createElement("processor");
		    	strucEle.appendChild(processor);
		    	processor.setAttribute("name", "FPE"+Integer.toString(idxSIMD));
		    	
		    	// Attach PE
		    	for (int idxWay=0; idxWay<simdWayNum; idxWay++) {
			    	Element pe = _xml.createElement("PE");
			    	processor.appendChild(pe);
			    	pe.setAttribute("name", "PE"+Integer.toString(idxWay));
			    	
			    	int singleStageSIMDIdx = _maxShare/_stageSpan;
			    	if (idxSIMD >= singleStageSIMDIdx) {
			    		// after max can be shared stage, there is one SIMD per stage
			    		int curStage = (idxSIMD-singleStageSIMDIdx) + _maxShare;
			    		for (int idxActor=0; idxActor<_actorPerPEPerStage; idxActor++) {  		
					    	pe.appendChild(_bfActors.get(curStage*_actorPerStage +
					    			idxWay*_actorPerPEPerStage + idxActor));
			    		}
			    	} else {
				    	for (int idxSpan=0; idxSpan<_stageSpan; idxSpan++) {
				    		for (int idxActor=0; idxActor<_actorPerPEPerStage; idxActor++) {  		
						    	pe.appendChild(_bfActors.get(idxSIMD*_stageSpan*_actorPerStage + 
						    			idxSpan*_actorPerStage + idxWay*_actorPerPEPerStage + idxActor));
				    		}
				    	}
			    	}
		    	}
			}
		} else {
			for (int i=0; i<_FPENum; i++) {
		    	Element processor = _xml.createElement("processor");
		    	strucEle.appendChild(processor);
		    	processor.setAttribute("name", "FPE"+Integer.toString(i));
		    	
	    		Element pe = _xml.createElement("PE");
		    	processor.appendChild(pe);
		    	pe.setAttribute("name", "PE"+Integer.toString(0));
		    	
		    	for (int k=0; k<_stages; k++) {
		    		for (int j=0; j<_actorPerPEPerStage; j++) {  		
				    	pe.appendChild(
				    			_bfActors.get(i*_actorPerPEPerStage+j+k*_actorPerStage));
		    		}
		    	}
		    }
		}
	}
	
	
    /** Generate the rotation factor array.
     *  
     *  
     */
	public void initW()
	{
		int i;
		double re, im;
		for(i=0;i<pointSize/2;i++)
		{
			re=Math.cos(2*Math.PI/pointSize*i);
			im=-1*Math.sin(2*Math.PI/pointSize*i);
			im = (im == 0)? 0 : im;
			_ws[i] = new Complex(re, im);			
		}
	}
	
    ///////////////////////////////////////////////////////////////////
    ////                         private variables                 ////
	
	// MIMD specific
	private int _FPENum;
	
	// SIMD specific
	private int _SIMDNum;
	private int _maxShare;
	private int _stageSpan;
	
	
	private Complex[] _ws;
	
	// Help variable
	public int _stages;
	public int _actorPerStage;
	public int _actorPerPEPerStage;	
	
	/* XML object for mapping and scheduling */
	private Document _xml;
	private List<Element> _bfActors = new ArrayList<Element>();
	
	/** Application specific fields **/
	public int pointSize;
	public int simdWayNum = 1;
	public FFTType type;
	public boolean bShareCoesWhenPossible;
	public boolean bSIMD = false;
	public int coeSharePoint;
	
	public enum FFTType {
		REAL_FULLC, REAL_PARTIALCUSTOM, REAL_CUSTOM_MIMD, REAL_CUSTOM_SIMD, 
		CPLX_CUSTOM_MIMD, CPLX_CUSTOM_SIMD, 
		
		/** Interleaved **/
		IL2_REAL_MIMD, IL2_REAL_SIMD, IL4_CPLX_MIMD, IL4_CPLX_SIMD 
	}
}







