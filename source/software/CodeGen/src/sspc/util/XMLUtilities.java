package sspc.util;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;

public class XMLUtilities {
	/** Instances of this class cannot be created.
     */
    private XMLUtilities() {
    }
	
	/**Output XML file.	 	 
	 * @param doc The document object. 
	 * @param filename The name of xml file.
	 * @throws TransformerException
	 * @throws IOException
	 */
	public static void writeXML(Document doc,String filename) {
	    //set up a transformer
		Document newxmldomobj = doc;
	    TransformerFactory transfac = TransformerFactory.newInstance();
	    transfac.setAttribute("indent-number", new Integer(2));//set indent value
	    try {
		    Transformer trans = transfac.newTransformer();
		    trans.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "no");
		    trans.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
		    trans.setOutputProperty(OutputKeys.INDENT, "yes");
		    trans.setOutputProperty(OutputKeys.VERSION, "1.0");
		    trans.setOutputProperty(OutputKeys.STANDALONE, "no");
		    trans.setOutputProperty(OutputKeys.METHOD, "xml");
		
		    //create string from XML tree
		    StringWriter sw = new StringWriter();
		    StreamResult result = new StreamResult(sw);
		    DOMSource source = new DOMSource(newxmldomobj);
		    trans.transform(source, result);
		    String xmlString = sw.toString();
	    	    
		    //Write the new XML files
		    PrintWriter newfid;
			newfid = new PrintWriter(new FileWriter(filename));
		    newfid.println(xmlString); 
		    newfid.close(); 
		} catch (IOException e) {
			throw new RuntimeException(e);
		} catch (TransformerException e) {
			throw new RuntimeException(e);
	    }
	    
	}
	
	/** This function is to read a *.xml file into the document object.
	 *  @param fid The XML file pointer.
	 */
	public static Document readXMLDocument(File fid) {
		if (fid == null)
			return null;
		
		try {
			// The two lines below are just for getting an instance of DocumentBuilder 
			// which we use for parsing XML data
	        // DocumentBuilderFactory Defines a factory API that enables applications 
			// to obtain a parser that produces DOM object trees from XML documents.
	        DocumentBuilderFactory xmlfactory = DocumentBuilderFactory.newInstance();
	        // newDocumentBuilder Creates a new instance of a DocumentBuilder using
	        // the currently configured parameters
	        DocumentBuilder xmlbuilder = xmlfactory.newDocumentBuilder();
	        // Here we do the actual parsing
	        // parse()Parse the content of the given file as an XML document and 
	        // return a new DOM Document object
	        Document xmldomobj = xmlbuilder.parse(fid);
	        return xmldomobj;
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}
}
