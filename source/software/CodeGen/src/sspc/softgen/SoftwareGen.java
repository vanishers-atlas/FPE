package sspc.softgen;

import java.io.*;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import sspc.util.*;
import sspc.lib.*;
import sspc.lib.SPUConfig.ALUTYPE;
import sspc.lib.Token.DATATYPE;
import sspc.lib.Token.TOKENTYPE;
import sspc.lib.dsp.FFT;
import sspc.lib.dsp.FFT.FFTType;
import sspc.lib.dsp.MatrixMult;
import sspc.lib.dsp.MatrixMult.MMType;
import sspc.lib.dsp.MotionEst;
import sspc.lib.dsp.MotionEst.METype;
import sspc.lib.dsp.MotionEstH264;
import sspc.lib.dsp.MotionEstH264.MEH264Type;
import sspc.lib.dsp.SobelEdge;
import sspc.lib.dsp.SobelEdge.SEType;


/**
 * This class implements the software generator functions. It scans the port
 * list of each entity of the mapping and scheduling output, and assembles
 * pieces of code into C source code for every processor.
 * 
 * @author Peng Wang
 * 
 */
public class SoftwareGen {
	// Test entry
//	public static void main(String[] args) {
//		String symbol;
//		if (true)
//			symbol = "&";
//		else
//			symbol = "";
//		String out = symbol + "T0" + "_" + "port0";
//		System.out.println(out);
//	}
	
	public SoftwareGen(SSP ssp, File graphMoml) {
		this.ssp = ssp;
		ssp.sg = this;
		_momlDoc = XMLUtilities.readXMLDocument(graphMoml);
		_trans = ssp.trans;
	}
	
	public SoftwareGen(SSP ssp, Document graphMoml) {
		this.ssp = ssp;
		ssp.sg = this;
		_momlDoc = graphMoml;
		_trans = ssp.trans;
	}

	/**
	 * Call this before general init()
	 */
	public void initFFT(FFT afft) {
		ssp.conf.dataWidth = 16;
		fft = afft;
		if (fft.type == FFTType.IL4_CPLX_MIMD || fft.type == FFTType.IL4_CPLX_SIMD) {
			ssp.conf.coreWidth = 32;
			ssp.conf.inputWidth = 32;
			ssp.conf.outputWidth = 32;
		}
		mode = Mode.FFT;
		_manualIntl = _bIntl;
		if (fft.type == FFTType.IL4_CPLX_MIMD || fft.type == FFTType.IL2_REAL_MIMD)
			ssp.skipShareFIFO = false;
	}
	
	public void initMatrixMult(MatrixMult mm) {
		if (mm.type == MMType.M1024B32W32) {
			ssp.conf.coreWidth = 32;
			ssp.conf.inputWidth = 32;
			ssp.conf.outputWidth = 32;
			ssp.conf.dataWidth = 32;
			ssp.conf.noIOCore = false;
		} else if (mm.type == MMType.test) {
			ssp.conf.coreWidth = 32;
			ssp.conf.inputWidth = 32;
			ssp.conf.outputWidth = 32;
			ssp.conf.dataWidth = 32;
		}
		_manualCode = true;
		this.matrixMult = mm;
		mode = Mode.MATRIXMULT;
	}
	
	public void initMotionEst(MotionEst me) {
		ssp.conf.coreWidth = 16;
		ssp.conf.inputWidth = 8;
		ssp.conf.outputWidth = 16;
		ssp.conf.dataWidth = 16;
		if (me.type == METype.DUALDM_CA_OVERLAPPED) {
			ssp.conf.noIOCore = false;
		}
		_manualCode = true;
		this.motionEst = me;
		mode = Mode.MOTIONEST;
	}
	
	public void initMotionEstH264(MotionEstH264 me) {
		ssp.conf.coreWidth = 16;
		ssp.conf.inputWidth = 8;
		ssp.conf.outputWidth = 16;
		ssp.conf.dataWidth = 16;
		ssp.conf.noIOCore = true;
		
		_manualCode = false;
		this.motionEstH264 = me;
		mode = Mode.MOTIONESTH264;
	}
	
	public void initSobelEdge(SobelEdge se) {
		ssp.conf.coreWidth = 16;
		ssp.conf.inputWidth = 8;
		ssp.conf.outputWidth = 16;
		ssp.conf.dataWidth = 16;
		_manualCode = true;
		this.sobelEdge = se;
		mode = Mode.SOBELEDGE;
	}
	/**
	 * This is the second init function to call before the code generation process 
	 * unless application special setup needed. It does:
	 * 1. set spu core type
	 * 2. parses MoML files; 
	 * 3. build a global schedule sequence; 
	 * 4. assign FIFOs;
	 * 5. build codegen units
	 * 
	 */
	public void init(ALUTYPE ct) {
		parseMoML(_momlDoc);
		parseMapSched(_momlDoc);
		
		// NOTE spus are constructed only when mapping was parsed
		for (SPU spu : ssp.spus) {
			spu.conf.coreType = ct;
			if (mode == Mode.MATRIXMULT) {
				spu.conf.Pb0Depth = 0;
				spu.conf.dmDataWidth = spu.conf.CoreDataWidth();
			} else if (mode == Mode.MOTIONEST) {
				spu.conf.Pb0Depth = 0;
				spu.conf.dmDataWidth = 8;
				if (motionEst.type == METype.DUALDM_CA || motionEst.type == METype.DUALDM_CA_OVERLAPPED ||
				    motionEst.type == METype.DUALDM_CA_RGB) {
					spu.conf.absdiffType = 2; // absdiffaccum component
					spu.conf.mulregEn = true;
				}
			} else if (mode == Mode.MOTIONESTH264) {				
				spu.conf.dmDataWidth = 8;
				spu.conf.absdiffType = 2;
				if (motionEstH264.type == MEH264Type.SINGLE) {
					if (spu.idx == 0) {
						spu.conf.mulregEn = true;
					} else if (spu.idx == 1) {
						spu.conf.Pb0Depth = 0;
					}
				} else if (motionEstH264.type == MEH264Type.TWO) {
					if (spu.idx == 0) {
						spu.conf.mulregEn = true;
					} else if (spu.idx == 2) {
						spu.conf.Pb0Depth = 0;
					}
				} else if (motionEstH264.type == MEH264Type.TWOBALANCED) {
					if (spu.idx == 0) {
						spu.conf.mulregEn = true;
						spu.conf.Pb0Depth = 0;
					} else if (spu.idx == 2) {
						spu.conf.Pb0Depth = 0;
					}
				}
			} else if (mode == Mode.SOBELEDGE) {
				spu.conf.Pb0Depth = 0;
				spu.conf.dmDataWidth = 8;
				if (sobelEdge.type == SEType.BASIC){
					spu.conf.Pb1Depth = 0;
					spu.conf.absdiffType = 0; // absdifffwd
				} else {
					spu.conf.absdiffType = 1; // absdiff
				}
			}
			
			// RF can initialize here as it knows fracBits and coreDataWidth
			for (PE pe : spu.PEs) {
				pe.rf = new RF(spu.conf);
				pe.rf.init();
			}
		}
		
		
		// Deal with IOCore configuration
		if (!ssp.conf.noIOCore) {
			SPUConfig ioconf = ssp.ioCore.conf;
			ioconf.Pb0Depth = 0;
			if (mode == Mode.MATRIXMULT) {
				ioconf.emBurstLen = 4;
			}
		}
		
		buildGlobalSchedSeq();
		assignFIFOs();
					
		buildCGUnits();
	}

	
	/**
	 * Set whether to interleave actors during SWGen.
	 * @param bInterleave
	 * @param ilSize The interleave size
	 */
	public void setInterleave(boolean bInterleave, int ilSize) {
		_bIntl = bInterleave;
		_ilSize = ilSize;
	}
	
	/**
	 * Set buffer allocation scheme. The default one minimises the number of 
	 * FIFOs by allocating only one FIFO between two PEs; shared buffer allocation
	 * sharing output FIFOs of a certain PE, typically used in MIMD FFT; 
	 * conflict-free buffer allocation tries to allocate FIFOs without causing 
	 * read conflicts with as less as possible FIFOs.
	 * 
	 * @param scheme 0 is default; 1 is shared; 2 is conflict-free
	 */
	public void setBufAllocScheme(FIFOAllocScheme scheme) {
		bufAllocScheme = scheme;
	}
	
	public void generateCode() throws IOException {
		_generateCode();
	}

	/**
	 * Get parsed MoML
	 * 
	 */
	public Document getParsedMoML() {
		return _momlDoc;
	}

	/**
	 * Parse the MoML file and fill in entities and ports. The MoML file is like
	 * the application model. The parsing scans the entities and generate entity
	 * objects. Then the parsing scans the relations and links and generate the
	 * connectedPortList for every port in each entity.
	 * 
	 * @param moml
	 */
	public void parseMoML(Document moml) {
		// Generate entities from MoML.
		NodeList entityList = moml.getElementsByTagName("entity");
		for (int i = 0; i < entityList.getLength(); i++) {
			Element entity = (Element) entityList.item(i);

			// Create entity.
			String entityClass = entity.getAttribute("class");
			String entityName = entity.getAttribute("name");
			Entity e = _createEntity(entityClass, entityName);

			// Build global schedule.
			// FIXME: Need to interface with Yun. Currently, only deal with
			// FFT's case. Simply set the global schedule complying with the
			// appearance of entities in MoML.
			_globalSched.add(e);

			// Set parameters.
			Element property = (Element) entity.getElementsByTagName("property").item(0);
			if (property != null) {
				String propertyName = property.getAttribute("name");
				String propertyValue = property.getAttribute("value");
	
				Parameter para = e.getParameter(propertyName);
				para.setValue(propertyValue);
				if (mode == Mode.FFT && fft.bSIMD && fft.bShareCoesWhenPossible) {
					if (i-1 >= fft.coeSharePoint)	
						para.setAsPort();
				}
			}

			_hashedEntityList.put(entityName, e);
		}

		// -- Parse links.
		_createIOCore();
		
		// Parse the interface
		_parseInterface(moml);

		// FIXME: It is assumed one link is the source and next link is the sink
		NodeList linkList = moml.getElementsByTagName("link");
		for (int i = 0; i < linkList.getLength(); i += 2) {
			Element link = (Element) linkList.item(i);
			String attrPort = link.getAttribute("port");

			Element link1 = (Element) linkList.item(i + 1);
			String attrPort1 = link1.getAttribute("port");

			if (SOURCEs.contains(attrPort)) {
				String[] subnames = SWGenUtils.splitName(attrPort1);
				Entity curEntity = _hashedEntityList.get(subnames[0]);
				Port curPort = curEntity.getPort(subnames[1]);

				curPort.addConnectedPort(_exSrcPort);
				_exSrcPort.addConnectedPort(curPort);
			} else {
				String[] subnames = SWGenUtils.splitName(attrPort);
				Entity curEntity = _hashedEntityList.get(subnames[0]);
				Port curPort = curEntity.getPort(subnames[1]);

				if (SINKs.contains(attrPort1)) {
					curPort.addConnectedPort(_exSinkPort);
					_exSinkPort.addConnectedPort(curPort);
				} else {
					String[] subnames1 = SWGenUtils.splitName(attrPort1);
					Entity curEntity1 = _hashedEntityList.get(subnames1[0]);
					Port curPort1 = curEntity1.getPort(subnames1[1]);

					curPort.addConnectedPort(curPort1);
					curPort1.addConnectedPort(curPort);
				}
			}
		}
	}
	
	/**
	 * Parse the Map&Schedule file and generate the lists. In order to
	 * accelerate the look-up speed for code generation, the map and schedule
	 * result is stored in data structures.
	 * 
	 * @param moml
	 */
	public void parseMapSched(Document moml) {
		NodeList spuList = moml.getElementsByTagName("processor");
		for (int i = 0; i < spuList.getLength(); i++) {
			Element ele_spu = (Element) spuList.item(i);
			String attrProcessorName = ele_spu.getAttribute("name");
			// Create a Processor object
			SPU spu = new SPU(ssp, attrProcessorName);

			NodeList peList = ele_spu.getElementsByTagName("PE");
			for (int j = 0; j < peList.getLength(); j++) {
				Element peEle = (Element) peList.item(j);
				// Create a PE object
				PE pe = new PE(j, spu);

				NodeList entityList = peEle.getElementsByTagName("entity");
				for (int k = 0; k < entityList.getLength(); k++) {
					Element entity = (Element) entityList.item(k);
					String attrEntityName = entity.getAttribute("name");
					Entity ent = _hashedEntityList.get(attrEntityName);
					ent.setOwnedPE(pe);

					pe.addEntity(ent);
				}

				spu.PEs.add(pe);
			}
			ssp.spus.add(spu);
		}
	}

	/**
	 * Build the global schedule from input MoMLs.
	 */
	public void buildGlobalSchedSeq() {
		// FIXME: This function needs to interface with Yun's IPC procedure.
		
		if (mode == Mode.FFT)
			Collections.sort(_globalSched);
	}

	/**
	 * Assign FIFOs to links. This pass happens after parse MoML and build
	 * global schedule sequence.
	 */
	public void assignFIFOs() {
		if (bufAllocScheme == FIFOAllocScheme.BASELINE) {
			_assignFIFODefault();
		} else if (bufAllocScheme == FIFOAllocScheme.SHARED) {
			_assignFIFOShared();
		} else if (bufAllocScheme == FIFOAllocScheme.CONFLICTFREE) {
//			_assignFIFOforSIMDFFT();
			_assignFIFOConflictFree();
		}
	}

	/**
	 * This is a complex function. To derive a conflict free FIFO allocation, the first
	 * step is to get the order of read write sequence between two PEs; then apply the
	 * LIS, each port is then connected to a FIFO.
	 */
	private void _assignFIFOConflictFree() {
		// ssp.fifos, pe outputfifos, inputfifos
		
		// First assign fifo like default fifo allocation, but only consider inter-PE.
		for (Entity curEnt : _globalSched) {
			PE srcPE = curEnt.getOwnedPE();

			for (Port output : curEnt.outputPortList()) {
				Port connectedPort = output.getConnectedPortList().get(0);
				PE sinkPE = connectedPort.getContainer().getOwnedPE();

				if (sinkPE.equals(srcPE)) continue;

				if (sinkPE.isIOPE()) continue;
				
				// To see if the sinkPE already connected
				if (!sinkPE.hasInputFIFOFrom(srcPE)) {
					// Create a new FIFO and connect it to PEs
					FIFO fifo = new FIFO(srcPE, sinkPE);
					fifo.inPorts.add(output);
					output.connectedFIFO = fifo;
					fifo.outPorts.add(connectedPort);
					connectedPort.connectedFIFO = fifo;
					
					_interPEFIFOs.add(fifo);
					
					srcPE.addOutputFifo(fifo);
					sinkPE.addInputFifo(fifo);
				} else {
					// Just connect the port with the FIFO
					FIFO fifo = sinkPE.getInputFIFOFrom(srcPE);
					output.connectedFIFO = fifo;
					connectedPort.connectedFIFO = fifo;
				}
			}
		}
		
		// Second model fifo read and write sequence
		for (Entity curEnt : _globalSched) {
			PE srcPE = curEnt.getOwnedPE();
			_genFIFOWriteSequence(srcPE, curEnt);
		}
		for (Entity curEnt : _globalSched) {
			PE sinkPE = curEnt.getOwnedPE();
			_genFIFOReadSequence(sinkPE, curEnt);
		}
		
		// Third reset all PE FIFOs for previous modeling purpose
		for (SPU spu:ssp.spus) {
			for (PE pe:spu.PEs) {
				pe.outputFIFOs.clear();
				pe.inputFIFOs.clear();
			}
		}
		
		// Four use LIS algorithm
		_addExInFIFOs();
		_addExOutFIFOs();
		
		for (FIFO f:_interPEFIFOs) {
			// each fifo represents a test target
			int n=0;
			while (!f.readSeq.isEmpty()) {
				Vector<Token> lis = new Vector<Token>();  
				find_lis(f.readSeq, lis);
				_allocAConfreeFifo(lis, n);
				n++;
				f.readSeq.removeAll(lis);
			}
		}
	}
	
	private void _allocAConfreeFifo(Vector<Token> tseq, int n) {
		PE srcPE = tseq.get(0).port.getContainer().getOwnedPE();
		PE sinkPE = tseq.get(0).port.getConnectedPort(0).getContainer().getOwnedPE();
		FIFO fifo = new FIFO(srcPE, sinkPE);
		fifo.localIdx = n;
		srcPE.addOutputFifo(fifo);
		sinkPE.addInputFifo(fifo);
		for (Token t:tseq) {
			Port srcPort = t.port;
			Port sinkPort = t.port.getConnectedPort(0);
			fifo.inPorts.add(srcPort);
			srcPort.connectedFIFO = fifo;
			fifo.outPorts.add(sinkPort);
			sinkPort.connectedFIFO = fifo;
			ssp.fifos.add(fifo);
		}
	}
	
	public void find_lis(Vector<Token> a, Vector<Token> out) {
		Vector<Integer> p = new Vector<Integer>();
		for (int i = 0; i < a.size(); i++) {
			p.add(0);
		}
		Vector<Integer> b = new Vector<Integer>();
		int u, v;
		 
		if (a.isEmpty()) return;
		
		b.add(0);
		for (int i = 1; i < a.size(); i++) {
			if (a.get(b.lastElement()).ridx() < a.get(i).ridx()) 
			{
				p.set(i, b.lastElement());
				b.add(i);
				continue;
			}
			
			for (u = 0, v = b.size()-1; u < v;) 
			{
				int c = (u + v) / 2;
				if (a.get(b.get(c)).ridx() < a.get(i).ridx()) 
					u=c+1; 
				else 
					v=c;
			}
			
			if (a.get(i).ridx() < a.get(b.get(u)).ridx()) 
			{
				if (u > 0) p.set(i, b.get(u-1));;
				b.set(u, i);
			}
		}
		
		for (u = b.size(), v = b.lastElement(); u>0; v = p.get(v)) {
			u--;
			b.set(u, v);
		}
		
		for (u=0; u<b.size(); u++) {
			out.add(a.get(b.get(u)));
		}
	}
	
	private void _genFIFOWriteSequence(PE pe, Entity ent) {
		List<Port> outputs = ent.outputPortList();
		Iterator<Port> iterator = outputs.iterator();

		while (iterator.hasNext()) {
			Port srcPort = iterator.next();
			List<Port> connectedPorts = srcPort.getConnectedPortList();
			Port sinkPort = connectedPorts.get(0);

			Entity sinkEnt = sinkPort.getContainer();
			PE sinkPE = sinkEnt.getOwnedPE();

			if (sinkPE.equals(pe) || sinkPE.isIOPE())	continue;

			FIFO fifo = srcPort.connectedFIFO;

			fifo.put(srcPort.token);
		}
		
	}
	
	private void _genFIFOReadSequence(PE pe, Entity ent) {
		for (Port sinkPort : ent.inputPortList()) {
			List<Port> connectedPorts = sinkPort.getConnectedPortList();
			
			if (connectedPorts.isEmpty()) {
				System.out.println("WARNING: Actor "+ent.getName()+" has an unconnected port: " + sinkPort.getName());
				continue;
			}
			
			// Get the only connected port.
			Port srcPort = connectedPorts.get(0);

			Entity srcEnt = srcPort.getContainer();
			PE srcPE = srcEnt.getOwnedPE();
			
			// If the entity of the connected port is in the same FPE, generate simple variable assignment.
			if (srcPE.equals(pe) || srcPE.isIOPE()) continue;


			// Code may have been generated when a FIFO access congestion happened.
			FIFO fifo = sinkPort.connectedFIFO;
			int dIndex = fifo.idxOf(srcPort.token);
			// Data must be in FIFO now.
			assert dIndex != -1;
			fifo.readSeq.add(srcPort.token);
			srcPort.token.setridx(dIndex);
		}
	}
	
	/**
	 * Build the codeGen Units. When interleaving is required, up to ilSize 
	 * number of actors are packed into one CGUnit. CGUnit is the basic unit
	 * for code generation. The input communications are generated first for
	 * all actors inside a CGUnit, then computation code and output communication
	 * code are generated.
	 */
	public void buildCGUnits() {
		for (Entity curEnt : _globalSched) {
			if (!_bIntl) {
				// When interleave is disabled, every curEnt is a CGUnit
				LinkedList<Entity> CGUnit = new LinkedList<Entity>();
				CGUnit.add(curEnt);
				_CGUnits.add(CGUnit);
				continue;
			}
			
			// <><> this is disabled currently. all are interleaved when possible.
			// The scheme employed here is it is only interleaved when it is beneficial.
			// Only the actor both have GETs and PUTs are considered as needed
			// to interleave.
//			if (!curEnt.areInputsInner() && !curEnt.areOutputsInner()) {
				_createCGUnit(curEnt, false);
//			} else {
//				_createCGUnit(curEnt, true);
//			}
		}
	}
	
	/**
	 * Help function to create the communication string.
	 * 
	 * The communication is represented in the form of 'src_dst', and stored in
	 * a communication array.
	 * 
	 * @param src The digit part of the source FPE (e.g. 7 for FPE7)
	 * @param dst The digit part of the destination FPE (e.g. 7 for FPE7)
	 * @return
	 */
	public static final String getCommString(String src, String dst) {
		String dSrc = src.equals("SOURCE") ? "in" : src.replaceAll("[\\D]", "");
		String dDst = dst.equals("SINK") ? "out" : dst.replaceAll("[\\D]", "");
		return dSrc + "_" + dDst;
	}

	public static final String getCommString(String src, int dst) {
		String dSrc = src.equals("SOURCE") ? "in" : src.replaceAll("[\\D]", "");
		String dDst = "" + dst;
		return dSrc + "_" + dDst;
	}

	public static final String getCommString(int src, String dst) {
		String dSrc = "" + src;
		String dDst = dst.equals("SINK") ? "out" : dst.replaceAll("[\\D]", "");
		return dSrc + "_" + dDst;
	}

	private static final String _generateGETInstr(String name, int no) {
		String asm = "GET_FIFO(" + name + ", " + no + ");\n";
		return asm;
	}

	private static final String _generatePUTInstr(String name, int no) {
		String asm = "PUT_FIFO(" + name + ", " + no + ");\n";
		return asm;
	}
	
	private void _parseInterface(Document moml) {
		NodeList portList = moml.getElementsByTagName("port");
		for (int i = 0; i < portList.getLength(); i++) {
			Element ele_port = (Element) portList.item(i);
			String attrPortName = ele_port.getAttribute("name");

			if (_portIsInput(ele_port))
				SOURCEs.add(attrPortName);
			else
				SINKs.add(attrPortName);
		}
	}
	
	private boolean _portIsInput(Element ePort) {
		NodeList propertyList = ePort.getElementsByTagName("property");
		for (int j = 0; j < propertyList.getLength(); j++) {
			Element eProperty = (Element) propertyList.item(j);
			if (eProperty.getAttribute("name").equals("direction") && eProperty.getAttribute("value").equals("in")) {
				return true;					
			}
		}
		return false;				
	}
		
	/**
	 * Create CGUnit for specified PE with specified entity. When inner is set
	 * and the CGUnit is empty, then the entity its own is a CGUnit.
	 * 
	 * A complicated case is theoretically it can be packed, but before packing
	 * completes, another packing has been done. That pack cannot issue until the 
	 * previous pack is finished. This could become very complicated if it waits
	 * for that one to complete (just think the same thing occurs during waiting).
	 * So in order to solve it easily, when another pack is ready to issue,
	 * complete previous pack even it has not got enough number.
	 * 
	 * @param pe
	 * @param ent
	 * @param inner The entity is not directly connected to the outside, ie it does
	 *        not has GETs and PUTs
	 */
	@SuppressWarnings("unchecked")
	private void _createCGUnit(Entity ent, boolean inner) {
		PE pe = ent.getOwnedPE();
		pe.entityCounter ++;
		
		if (_packIssued) {
			_nextIssuePack = pe.CGUnit;
			_packIssued = false;
		}
		
		if (pe.CGUnit.isEmpty() && inner == true) {
			// When an inner actor is the first element in a CGUnit, then its own
			// is a CGUnit.
			LinkedList<Entity> unit = new LinkedList<Entity>();
			unit.add(ent);
			_issueCGUnit(unit);			
		} else {
			// Otherwise, test the dependency.
			if (_verifyDependency(pe.CGUnit, ent)) {
				// If satisfied, the entity is added to a CGUnit. When a CGUnit
				// is ready to issue (contains enough elements), populate it
				// into the CGUnits.
				pe.CGUnit.add(ent);
				if (pe.CGUnit.size() == _ilSize || pe.getEntities().size() == pe.entityCounter) {
					_issueCGUnit((LinkedList<Entity>) pe.CGUnit.clone());
					pe.CGUnit.clear();
				} else {
					// Look-ahead to finish a CGUnit creation. If it is delayed
					// until the ent creates a dependency failure, the CGUnit
					// may not be inserted into CGUnits at the right position.
					// E.g. The second last CGUnit and the last CGUnit maybe 
					// inserted one after another, but there are other CGUnits
					// in other PE should be between them (FFT's case).
					if (!_verifyDependency(pe.CGUnit, pe.next(ent))) {
						_issueCGUnit((LinkedList<Entity>) pe.CGUnit.clone());
						pe.CGUnit.clear();
					}
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	private void _issueCGUnit(LinkedList<Entity> unit) {
		// Check if this is the right next issue, if not, first issue the 
		// unfinished nextIssue
		if (!unit.equals(_nextIssuePack)) {
			_CGUnits.add((LinkedList<Entity>) _nextIssuePack.clone());
			_nextIssuePack.clear();
		}
		_CGUnits.add(unit);
		_packIssued = true;
	}
	
	/**
	 * Verify the dependency when creating a CGUnit. The entities inside a CGUnit
	 * must not have predecessors whose index in the globalSched is after anyone
	 * in the CGUnit. But only compare the index with the first entity in the
	 * CGUnit is enough, as it has the smallest index.
	 *   [APre]->[A]->
     *   [BPre]->[B]->
     *            | (cannot interleave)
     *            +-->[CPred*]->[C]->
     *   * CPred may be just B
	 * @param CGUnit
	 * @param ent
	 * @return
	 */
	private boolean _verifyDependency(LinkedList<Entity> CGUnit, Entity ent) {
		if (CGUnit.isEmpty())
			return true;
		
		Entity first = CGUnit.get(0);
		
		for (Entity pred : ent.getInputEntities()) {
			if (_globalSched.indexOf(first) <= _globalSched.indexOf(pred))
				return false;
		}
		
		return true;
	}
	
	/**
	 * Default: automatically assign FIFO according to the principle that there
	 * is at most one FIFO exists between two PEs. This may cause congestion to
	 * access FIFO data by different actors.
	 */
	private void _assignFIFODefault() {
		// First assign input FIFOs
		_addExInFIFOs();

		for (Entity curEnt : _globalSched) {
			PE srcPE = curEnt.getOwnedPE();

			for (Port output : curEnt.outputPortList()) {
				Port connectedPort = output.getConnectedPortList().get(0);

				PE sinkPE = connectedPort.getContainer().getOwnedPE();

				// If the entity of the connected port is in the same FPE,
				// do nothing
				if (sinkPE.equals(srcPE))
					continue;

				// To see if the sinkPE already connected
				if (!sinkPE.hasInputFIFOFrom(srcPE)) {
					// Create a new FIFO and connect it to PEs
					FIFO fifo = new FIFO(srcPE, sinkPE);
					fifo.inPorts.add(output);
					output.connectedFIFO = fifo;
					fifo.outPorts.add(connectedPort);
					connectedPort.connectedFIFO = fifo;

					ssp.fifos.add(fifo);

					// Add exOutFIFOs
					if (sinkPE.isIOPE()) {
						ssp.exOutFifos.add(fifo);
						fifo.isExOutFIFO = true;
					}

					srcPE.addOutputFifo(fifo);
					sinkPE.addInputFifo(fifo);
				} else {
					// Just connect the port with the FIFO
					FIFO fifo = sinkPE.getInputFIFOFrom(srcPE);
					output.connectedFIFO = fifo;
					connectedPort.connectedFIFO = fifo;
				}
			}
		}
	}

	private void _assignFIFOShared() {
		if (mode == Mode.NONE) {
			throw new RuntimeException("ERROR");
		} else if (mode == Mode.FFT) {
			// First assign input FIFOs
			_addExInFIFOs();
			for (SPU spu : ssp.spus) {
				for (PE srcPE : spu.PEs) {
					boolean sharedFIFOCreated = false;
					for (Entity curEnt : srcPE.getEntities()) {
						for (int i = 0; i < curEnt.outputPortList().size(); i++) {
							Port output = curEnt.outputPortList().get(i);
							Port connectedPort = output.getConnectedPort(0);
							
							PE sinkPE = connectedPort.getPE();
	
							// If the entity of the connected port is in the same
							// FPE, do nothing
							if (srcPE.equals(sinkPE)) continue;
							
							if (sinkPE.isIOPE()) {
								// All ports connected to external output are shared
								// as default FIFO allocation
								if (!sinkPE.hasInputFIFOFrom(srcPE)) {
									_connectNewFIFO(srcPE, sinkPE, output, connectedPort);
								} else {
									FIFO fifo = sinkPE.getInputFIFOFrom(srcPE);
									output.connectedFIFO = fifo;
									connectedPort.connectedFIFO = fifo;
								}
							} else {
								// Create once, and shared all inter-PE ports in
								// one FIFO.
								if (!sharedFIFOCreated) {
									_connectNewFIFO(srcPE, sinkPE, output, connectedPort);							
									sharedFIFOCreated = true;
								} else {
									FIFO fifo = srcPE.getOutputFIFO(0);
	
									output.connectedFIFO = fifo;
									connectedPort.connectedFIFO = fifo;
									
									fifo.inPorts.add(output);
									fifo.outPorts.add(connectedPort);
									
									if (!fifo.sinkPEs.contains(sinkPE)) {									
										fifo.sinkPEs.add(sinkPE);								
										sinkPE.addInputFifo(fifo);
									}																
								}
							}
						}
					}
				}
			}
		}
	}
	
	/**
	 * FIFO read congestion free assignment. Stage 0 assigns port 0 to fifo0,
	 * and port 1 to fifo1; last stage assigns both ports to fifo0; other stages
	 * assign port 0 to fifo0, port 1 to fifo1 for upper actors, and assign port
	 * 0 to fifo2, port 1 to fifo3 for lower actors.
	 */
//	private void _assignFIFOforSIMDFFT() {
//		int stages = (int) (Math.log(fft.pointSize) / Math.log(2));
//		int bfsPerStage = fft.pointSize / 2;
//		int bfsPerPEPerStage = bfsPerStage / fft.simdWayNum;
//
//		if (mode == Mode.NONE) {
//			throw new RuntimeException("ERROR");
//		} else if (mode == Mode.FFT) {
//			// First assign input FIFOs
//			_addExInFIFOs();
//			for (SPU spu : ssp.spus) {
//				for (PE srcPE : spu.PEs) {
//					for (Entity curEnt : srcPE.getEntities()) {
//						// Helper variables
//						int curStage = curEnt.idx / bfsPerStage;
//	
//						// Half of a sub-FFT
//						int lowerBF = (int) Math.pow(2, curStage);
//	
//						// Number of channels this PE will have
//						boolean hasOneCh = false;
//						boolean hasTwoCh = false;
//						boolean hasFourCh = false;
//						if (curStage == 0) {
//							hasTwoCh = true;
//						} else if (curStage == stages - 1) {
//							hasOneCh = true;
//						} else if (bfsPerPEPerStage <= lowerBF) {
//							hasTwoCh = true;
//						} else {
//							hasFourCh = true;
//						}
//	
//						for (int i = 0; i < curEnt.outputPortList().size(); i++) {
//							Port output = curEnt.outputPortList().get(i);
//							Port connectedPort = output.getConnectedPort(0);
//	
//							PE sinkPE = connectedPort.getPE();
//	
//							// If the entity of the connected port is in the same
//							// PE, do nothing
//							if (srcPE.equals(sinkPE))
//								continue;
//	
//							if (hasOneCh) {
//								if (srcPE.outputFIFOs.size() == 0) {
//									_connectNewFIFO(srcPE, sinkPE, output,
//											connectedPort);
//								} else {
//									FIFO fifo = srcPE.getOutputFIFO(0);
//									output.connectedFIFO = fifo;
//									connectedPort.connectedFIFO = fifo;
//								}
//							} else if (hasTwoCh) {
//								// Port0 is connected to fifo0, port1 to fifo1;
//								if (srcPE.outputFIFOs.size() == 0) {
//									_connectNewFIFO(srcPE, sinkPE, output,
//											connectedPort);
//								} else if (srcPE.outputFIFOs.size() == 1) {
//									FIFO f = _connectNewFIFO(srcPE, sinkPE, output,
//											connectedPort);
//									// Local index is not necessarily 1, it must
//									// be calculated here.
//									f.localIdx = sinkPE.numOfInputFIFOsFrom(srcPE);
//								} else {
//									FIFO fifo = srcPE.getOutputFIFO(i);
//									output.connectedFIFO = fifo;
//									connectedPort.connectedFIFO = fifo;
//								}
//							} else if (hasFourCh) {
//								// Manually create more FIFOs than the minimum number
//								// decided by the PE-to-PE links to solve the FIFO
//								// read access conflict. Except the first stage which
//								// requires only two FIFOs to solve conflict, other
//								// stages require four FIFOs to solve all conflicts.
//								// This is shown as
//								// ------           ------
//								// | A0 | 0-------  | B0 |
//								// ------ 1\     /  ------
//								//          \   /
//								// ------    \ /    ------
//								// | A1 | 0-------  | B1 |
//								// ------ 1\ / \ /  ------
//								//   ..     /   /     ..
//								// ------ 2/ \ / \  ------
//								// | A2 | 3---/---  | B2 |
//								// ------    / \    ------
//								//          /   \
//								// ------ 2/     \  ------
//								// | A3 | 3-------  | B3 |
//								// ------           ------
//	
//	
//								// Belongs to the Up half of a sub-FFT
//								boolean isUp = (curEnt.idx % bfsPerStage % (lowerBF * 2)) < lowerBF;
//								// Is the first sub-FFT in a PE
//								boolean isFirstUPLOW = (curEnt.idx % bfsPerStage % bfsPerPEPerStage) < lowerBF * 2;
//	
//								// Up part: port0-fifo0, port1-fifo1;
//								// Low part: port0-fifo2, port1-fifo3;
//								if (isFirstUPLOW) {
//									if (isUp) {
//										if (srcPE.outputFIFOs.size() == 0) {
//											_connectNewFIFO(srcPE, sinkPE, output,
//													connectedPort);
//										} else if (srcPE.outputFIFOs.size() == 1) {
//											FIFO f = _connectNewFIFO(srcPE, sinkPE,
//													output, connectedPort);
//											f.localIdx = 1;
//										} else {
//											FIFO fifo = srcPE.getOutputFIFO(i);
//											output.connectedFIFO = fifo;
//											connectedPort.connectedFIFO = fifo;
//										}
//									} else {
//										if (srcPE.outputFIFOs.size() == 2) {
//											FIFO f = _connectNewFIFO(srcPE, sinkPE,
//													output, connectedPort);
//											f.localIdx = 2;
//										} else if (srcPE.outputFIFOs.size() == 3) {
//											FIFO f = _connectNewFIFO(srcPE, sinkPE,
//													output, connectedPort);
//											f.localIdx = 3;
//										} else {
//											FIFO fifo = srcPE.getOutputFIFO(2 + i);
//											output.connectedFIFO = fifo;
//											connectedPort.connectedFIFO = fifo;
//										}
//									}
//								} else {
//									int base = (isUp) ? 0 : 2;
//									FIFO fifo = srcPE.getOutputFIFO(base + i);
//									output.connectedFIFO = fifo;
//									connectedPort.connectedFIFO = fifo;
//								}
//							}
//						}
//					}
//				}
//			}
//		}
//	}

	/**
	 * Connect a new FIFO to srcPE, sinkPE, srcPort and sinkPort
	 * 
	 * @param srcPE
	 * @param sinkPE
	 * @param output
	 * @param input
	 */
	private FIFO _connectNewFIFO(PE srcPE, PE sinkPE, Port output, Port input) {
		// Create a new FIFO and connect it to PEs
		FIFO fifo = new FIFO(srcPE, sinkPE);

		fifo.inPorts.add(output);
		fifo.outPorts.add(input);

		output.connectedFIFO = fifo;
		input.connectedFIFO = fifo;

		ssp.fifos.add(fifo);

		// Add exOutFIFOs
		if (sinkPE.isIOPE()) {
			ssp.exOutFifos.add(fifo);
			fifo.isExOutFIFO = true;
		}

		srcPE.addOutputFifo(fifo);
		sinkPE.addInputFifo(fifo);

		return fifo;
	}

	/**
	 * First fire external FPEs. This fills the external input FIFOs, and sets
	 * the index of external input FIFO always to 0.
	 */
	private void _addExInFIFOs() {
		List<Port> ports = _exSrcPort.getConnectedPortList();
		PE exSrcPE = _ioCore.PEs.get(0);

		for (Port connectedPort : ports) {
			Entity sinkEnt = connectedPort.getContainer();
			PE sinkPE = sinkEnt.getOwnedPE();

			// To see if the sinkPE already connected
			if (!sinkPE.hasInputFIFOFrom(exSrcPE)) {
				// Create a new FIFO. Fill in inPorts and outPorts of FIFO;
				// add connectedFIFO to ports.
				FIFO fifo = new FIFO(exSrcPE, sinkPE);
				fifo.inPorts.add(_exSrcPort);
				fifo.outPorts.add(connectedPort);
				connectedPort.connectedFIFO = fifo;

				ssp.fifos.add(fifo);
				ssp.exInFifos.add(fifo);
				
				fifo.isExInFIFO = true;

				exSrcPE.addOutputFifo(fifo);
				sinkPE.addInputFifo(fifo);
			} else {
				// Just connect the port with the FIFO
				FIFO fifo = sinkPE.getInputFIFOFrom(exSrcPE);
				connectedPort.connectedFIFO = fifo;
			}
		}
	}
	
	private void _addExOutFIFOs() {
		List<Port> ports = _exSinkPort.getConnectedPortList();
		PE exSinkPE = _ioCore.PEs.get(0);

		for (Port connectedPort : ports) {
			Entity srcEnt = connectedPort.getContainer();
			PE srcPE = srcEnt.getOwnedPE();

			// To see if the srcPE already connected
			if (!exSinkPE.hasInputFIFOFrom(srcPE)) {
				// Create a new FIFO. Fill in inPorts and outPorts of FIFO;
				// add connectedFIFO to ports.
				FIFO fifo = new FIFO(srcPE, exSinkPE);
				fifo.inPorts.add(connectedPort);
				fifo.outPorts.add(_exSinkPort);
				connectedPort.connectedFIFO = fifo;

				ssp.fifos.add(fifo);
				ssp.exOutFifos.add(fifo);
				
				fifo.isExOutFIFO = true;

				exSinkPE.addInputFifo(fifo);
				srcPE.addOutputFifo(fifo);
			} else {
				// Just connect the port with the FIFO
				FIFO fifo = exSinkPE.getInputFIFOFrom(srcPE);
				connectedPort.connectedFIFO = fifo;
			}
		}
	}

	private Entity _createEntity(String actorClass, String entityName) {
		Entity e = new Entity(entityName, actorClass);
		
		e.parseActor(actorClass);

		return e;
	}	
	
	/**
	 * Get the data type of a given port.
	 * 
	 * @param p
	 * @return
	 */
	private String _getDataType(DATATYPE dt, ALUTYPE ct) {
		if (ct == ALUTYPE.CPLX16B4D) {
			if (dt == DATATYPE.CPLXFLOAT)
				return "int";
			else
				throw new RuntimeException("ERROR: Unsupported data types! " + dt);
		} else {
			if (dt == DATATYPE.CPLXFLOAT)
				return "Complex";
			else if (dt == DATATYPE.INT)
				return "int";
			else if (dt == DATATYPE.FLOAT)
				return "float";
			else 
				throw new RuntimeException("ERROR: Unsupported data types! " + dt);
		}
	}
	
	// /////////////////////////////////////////////////////////////////
	// // private methods ////

	/**
	 * Generate code and append it to the given string buffer.
	 * 
	 * @param code The given string buffer.
	 * @throws IOException
	 */
	private void _generateCode() throws IOException {
		// Generate C code for every SPU. Start from generating body code. As
		// body codes should be generated simultaneously for all SPUs according
		// to the global schedule, so body code is separated from generating
		// remaining code.
		for (LinkedList<Entity> CGUnit : _CGUnits) {
			PE curPE = CGUnit.get(0).getOwnedPE();	
			String code = new String();
			if (CGUnit.size() > 1) {
				CGUnit.get(0).getOwnedPE().cCode += 
					"\n// Interleaving " + CGUnit.size() +" actors\n";
				System.out.println("\nInterleaving " + CGUnit.size());
			}
			
			// Input communication portion
			for (Entity curEnt : CGUnit) {
				curPE.cCode += _generateInputsCommCode(curPE, curEnt);		
			}
			
			// Computation call portion
			if (!_manualIntl) {
				for (Entity curEnt : CGUnit) {
					code = "";				
					code += _genCompCode(curEnt);
					curPE.cCode += code;
				}
			} else {
				curPE.cCode += _genCompCodeMerged(CGUnit);
			}
			
			// Output communication portion
			for (Entity curEnt : CGUnit) {
				curPE.cCode += _generateOutputsCommCode(curPE, curEnt);
			}
			
			// Fire function definition portion
			if (_manualCode) continue;
			
			if (!_manualIntl) {
				for (Entity curEnt : CGUnit) {
					curPE.fireFuncCode += _genFireFuncCode(curEnt, curPE.getSPU().conf.coreType);
				}
			} else {
				curPE.fireFuncCode += _genFireFuncCodeMerged(CGUnit, curPE.getSPU().conf.coreType);
			}			
		}
		
		for (SPU spu : ssp.spus) {			
			ALUTYPE ct = spu.conf.coreType;
			for (PE pe : spu.PEs) {
				// Generate code.
				StringBuffer code = new StringBuffer();
				if (_manualCode) {
					code.append(_genManualCode(spu.idx));
					// Output assembly directly
					if (pe.idx == 0)
						SWGenUtils.writeToFile("in//asm//FPE" + spu.idx + ".s", code.toString());					
				} else {
					List<Entity> entities = pe.getEntities();
	
					String variableDeclarationCode = new String();
					String variableInitializationCode = new String();
					for (Entity curEnt : entities) {
						variableDeclarationCode += _generateVariableDeclaration(curEnt, ct);
	
						variableInitializationCode += _generateVariableInitialization(curEnt, ct);					
					}
	
					// The appending phase					
					code.append("#include \"header.h\"\n\n");
					
					code.append("\n// **** Fire function declaration **** //\n");
					code.append(pe.fireFuncCode);
					
					code.append("\n// **** Main function **** //\n");
					code.append("void " + pe.getName() + "() {\n");
					code.append("\n  // **** Variable declaration **** //\n");
					code.append(variableDeclarationCode);
					code.append("\n  // **** Parameter initialisation **** //\n");
					code.append(variableInitializationCode);
					code.append("\n  // **** Code body **** //\n");
					code.append(pe.cCode);
					code.append("}\n");
				}

				pe.cCode = code.toString();

				// When FPE is SIMD, although the generated C code is different
				// in operating entity, but the compiled assembly should be the
				// same, otherwise, it cannot be an SIMD. Here we believe the
				// SIMD mapping is right, and only output C code for PE0 .
				if (pe.idx == 0)
					SWGenUtils.writeToFile("out//C//FPE" + spu.idx + ".c", pe.cCode);
			}
		}
		
		if (!ssp.conf.noIOCore)
			SWGenUtils.writeToFile("in//asm//IOCore.s", _genIOCoreCode());

		// Configure FIFO number, FIFO width, number of SIMD ways
		for (SPU spu : ssp.spus) {
			SPUConfig conf = spu.conf;
			conf.iChNo = spu.getPE(0).inputFIFOs.size();
			conf.iChWidth = SWGenUtils.getAddressWidth(conf.iChNo);

			conf.oChNo = spu.getPE(0).outputFIFOs.size();
			conf.oChWidth = SWGenUtils.getAddressWidth(conf.oChNo);

			conf.simdWay = spu.PEs.size();

			ssp.conf.SPUConfs.add(conf);
		}
		
		if (!ssp.conf.noIOCore) {
			SPUConfig conf = ssp.ioCore.conf;
			PE iope = ssp.ioCore.getPE(0);
			conf.iChNo = iope.inputFIFOs.size();
			conf.iChWidth = SWGenUtils.getAddressWidth(conf.iChNo);

			conf.oChNo = iope.outputFIFOs.size();
			conf.oChWidth = SWGenUtils.getAddressWidth(conf.oChNo);
		}
	}

	/**
	 * Generate The fire function code. Each actor's firing code is in a
	 * function with the same name as that of the actor.
	 * 
	 * @return The fire function code.
	 * @throws IOException 
	 */
	private String _genFireFuncCode(Entity e, ALUTYPE ct) throws IOException {
		String code = new String("");
		
		if (mode == Mode.FFT) {
			throw new RuntimeException("Unsupported fireFunc type!");
		} else {
			// The definition code is for actor class rather than actor instance.
			LinkedList<String> gened = e.getOwnedPE().getSPU().generatedActorClass;
			if (gened.contains(e.actorClass))
				return code;
			
			gened.add(e.actorClass);
			code = _readActorFireFuncFile("fireFunctions/"+e.getClassName()+".c");
		}
		return code;
	}
	
	private String _readActorFireFuncFile(String filename) throws IOException {
		FileInputStream fstream = new FileInputStream(filename);
		DataInputStream in = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String strLine;
		StringBuffer code = new StringBuffer();

		// Read File Line By Line
		while ((strLine = br.readLine()) != null) {
			code.append(strLine+"\n");
		}
		return code.toString();
	}

	/**
	 * Hand interleaved version fire function of FFT butterfly actors.
	 * @param CGUnit
	 * @param ct
	 * @return
	 * @throws IOException 
	 */
	private String _genFireFuncCodeMerged(LinkedList<Entity> CGUnit, ALUTYPE ct) throws IOException {
		String code = new String("");		
		LinkedList<String> gened = CGUnit.getFirst().getOwnedPE().getSPU().generatedActorClass;
		String filename = fft.type.toString();
		
		if (mode == Mode.FFT) {
			switch (fft.type) {			
			case IL4_CPLX_MIMD:
			case IL2_REAL_MIMD:
				if (gened.contains(filename))
					return code;
				gened.add(filename);				
				code = _readCodefromFile("in//code//FFT//actor//"+filename);
			break;
			case IL4_CPLX_SIMD:
				// complex, SIMD, fully customisation, interleaving 4
				if (fft.bShareCoesWhenPossible  && CGUnit.getFirst().idx < fft.coeSharePoint) {
					filename = filename+"_sharecoe";
				}
				if (gened.contains(filename))
					return code;
				gened.add(filename);
				code = _readCodefromFile("in//code//FFT//actor//"+filename);
				
			break;
			default: 
				throw new RuntimeException("Unsupported fireFunc type!");
			}
		}
		return code;
	}
	
	/**
	 * Generate entire code manually. This could achieve better performance.
	 * @throws IOException 
	 */
	private String _genManualCode(int i) throws IOException {
		String code = new String("");
		if (mode == Mode.MATRIXMULT) {
			String filename = matrixMult.type.toString();
			if (!ssp.conf.noIOCore)
				filename = "WithIOCore//" + filename;
			code = _readCodefromFile("in//code//MatrixMult//"+filename);			
		} else if (mode == Mode.MOTIONEST) {
			String filename = motionEst.type.toString();
			if (!ssp.conf.noIOCore)
				filename = "WithIOCore//" + filename;
			code = _readCodefromFile("in//code//MotionEst//"+filename);
		} else if (mode == Mode.MOTIONESTH264) {
			String filename = motionEstH264.type.toString();
			code = _readCodefromFile("in//code//MotionEstH264//"+filename+"//FPE"+i+".s");
		} else if (mode == Mode.SOBELEDGE) {
			String filename = sobelEdge.type.toString();
			if (!ssp.conf.noIOCore)
				filename = "WithIOCore//" + filename;
			code = _readCodefromFile("in//code//SobelEdge//"+filename);
		}
		return code;
	}
	
	private String _readCodefromFile(String codeFile) throws IOException {
		FileInputStream fstream = new FileInputStream(codeFile);
		DataInputStream in = new DataInputStream(fstream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String strLine;
		String code = new String("");
		
		// Read File Line By Line
		while ((strLine = br.readLine()) != null) {
			code += strLine+"\n";
		}
		return code;
	}
	
	private String _genIOCoreCode() throws IOException {
		String code = new String("");
		
		if (mode == Mode.MATRIXMULT) {
			String filename = matrixMult.type.toString()+"_io";
			code = _readCodefromFile("in//code//MatrixMult//"+filename);			
		} else if (mode == Mode.MOTIONEST) {
			String filename = motionEst.type.toString()+"_io";
			code = _readCodefromFile("in//code//MotionEst//"+filename);
		} else if (mode == Mode.SOBELEDGE) {
			String filename = sobelEdge.type.toString()+"_io";
			code = _readCodefromFile("in//code//SobelEdge//"+filename);
		}
		
		return code;
		
	}
	
	/**
	 * Generate variable declarations for inputs and outputs and parameters.
	 * Append the declarations to the given string buffer.
	 * 
	 * @return code The generated code.
	 */
	private String _generateVariableDeclaration(Entity ent, ALUTYPE ct) {
		StringBuffer code = new StringBuffer();

		// Declare ports.
		List<Port> ports = ent.getPorts();
		Iterator<Port> iterPort = ports.iterator();
		while (iterPort.hasNext()) {
			Port curPort = iterPort.next();
			String name = ent.getName() + "_" + curPort.getName();
			if (curPort.token.tokenType != TOKENTYPE.SCALAR) {
				name += "["+curPort.token.dim0+"]";
			}
			code.append("\t" + _getDataType(curPort.token.dataType, ct) + " " + name + ";\n");
		}

		// Declare parameters.
		for (Parameter para : ent.parameterList()) {			
			code.append("\t" + _getDataType(para.dataType, ct) + " " + para.getFullName() + ";\n");			
		}

		code.append("\n");
		return code.toString();
	}

	private String _genConstPortInlineAsm(String name) {
		String asm = "asm volatile (\"GET_CONST_PORT %0, ^0\\n\\t\":\"=m\"("
				+ name + ")::);\n";
		return asm;
	}

	/**
	 * Generate variable initialisation for the referenced parameters.
	 * 
	 * @return code The generated code.
	 */
	private String _generateVariableInitialization(Entity ent, ALUTYPE ct) {
		StringBuffer code = new StringBuffer();

		for (Parameter para : ent.parameterList()) {
			if (DATATYPE.isCplx(para.dataType)) {
				double re = _fitInRange(para.getReal());
				double im = _fitInRange(para.getImag());

				if (ct == ALUTYPE.REAL16B1D) {
					if (para.asPort()) {
						// Optimisation after C compiling will remove GET_CONT_PORT instructions.
						code.append(_genConstPortInlineAsm(para.getFullName()+ ".real"));
						code.append(_genConstPortInlineAsm(para.getFullName()+ ".imag"));
						// Fill in constant port parameters list
						ent.getOwnedPE().cpParas.add(re);
						ent.getOwnedPE().cpParas.add(im);
					} else {
						code.append(para.getFullName() + ".real = " + re + ";\n");
						code.append(para.getFullName() + ".imag = " + im + ";\n");
					}
				} else {
					// Complex datapath needs complex data to be packed as Imag|Real.
					int packed = (SWGenUtils.float2fix(im, ssp.conf.dataWidth, 
							ssp.conf.fracBits) << ssp.conf.dataWidth) + 
							SWGenUtils.float2fix(re, ssp.conf.dataWidth, ssp.conf.fracBits);
					if (para.asPort()) {
						code.append(_genConstPortInlineAsm(para.getFullName()));
						ent.getOwnedPE().cpParas.add((double) packed);
					} else {
						code.append(para.getFullName() + " = " + packed + ";\n");
					}					
				}
			} else {
				throw new RuntimeException("Only complex type is supported now\n");
			}
		}
		return code.toString();
	}

	/**
	 * Generate the communication code for inputs of the given entity.
	 *  
	 */
	private String _generateInputsCommCode(PE pe, Entity ent) {
		ALUTYPE ct = pe.getSPU().conf.coreType;
		
		System.out.println("Generate code for " + ent.getName());
		StringBuffer code = new StringBuffer("\n");

		for (Port input : ent.inputPortList()) {
			List<Port> connectedPorts = input.getConnectedPortList();
			
			if (connectedPorts.isEmpty()) {
				System.out.println("WARNING: Actor "+ent.getName()+" has an unconnected port: " + input.getName());
				continue;
			}
			
			// Get the only connected port.
			Port connectedPort = connectedPorts.get(0);

			Entity srcEnt = connectedPort.getContainer();
			PE srcPE = srcEnt.getOwnedPE();
			
			// If the entity of the connected port is in the same FPE, generate simple variable assignment.
			if (srcPE.equals(pe)) {
				String in = ent.getName() + "_" + input.getName();
				String out = srcEnt.getName() + "_" + connectedPort.getName();
				
				if (input.token.tokenType == TOKENTYPE.SCALAR)
					code.append("\t" + in + " = " + out + ";\n");
				else {
					String index = "";
					for (int i = 0; i < input.token.dim0; i++) {
						index = "["+i+"]";
						code.append("\t" + in+index + " = " + out+index + ";\n");
					}
				}
				input.codeGenerated = true;
				continue;
			}

			FIFO fifo = input.connectedFIFO;
			int chNo = fifo.getReadIdxIn(pe);

			// Put always happens before a corresponding get. So the link should
			// have been connected.
			assert chNo != -1;

			// Code may have been generated when a FIFO access congestion
			// happened.
			if (input.codeGenerated)
				continue;

			// Print information of where the FIFO data come from
			//code.append("\t" + "// Get from " + srcPE.getName() + "\n");

			if (srcPE.isIOPE()) {
				// When it is external input, the data is assumed to be always
				// available. Current scheme enforces external input FIFO is always at
				// index 0.
				assert chNo == 0;
				code.append(_generateGETforPort(input, chNo, ct));
			} else {
				// The data might be not available directly as it is in an 'FIFO'.
				// When FIFO read congestion happens, the data which won't be immediately
				// consumed still have to be read out from FIFO and cached in registers,
				// so that to get the needed data. This is why we need to model 
				// the FIFO access to get the congestion information.
				int dIndex = fifo.idxOf(connectedPort.token);
				// Data must be in FIFO now.
				assert dIndex != -1;

				for (int i = 0; i <= dIndex; i++) {
					Token t = fifo.get();
					Port srcPort = t.port;
					Port sinkPort = srcPort.getConnectedPortList().get(0);
					code.append(_generateGETforPort(sinkPort, chNo, ct));
					// Only insert transition occurs with PE0. _trans records
					// the GET sequence considering the congestion behavior.
					if (pe.idx == 0)
						_trans.add(new Transition(srcPort, sinkPort, fifo));
				}
			}
		}

		return code.toString();
	}

	/**
	 * Generate code for outputs of given entity.
	 * 
	 * It also fills in the commArray in the communication sequence. This is
	 * important, as the commArray used in the HarwareGnerator must comply with
	 * the GET/PUT channel index.
	 * 
	 * @param e
	 * @return
	 */
	private String _generateOutputsCommCode(PE pe, Entity ent) {
		ALUTYPE ct = pe.getSPU().conf.coreType;
		
		List<Port> outputs = ent.outputPortList();
		Iterator<Port> iterator = outputs.iterator();

		StringBuffer code = new StringBuffer();

		while (iterator.hasNext()) {
			Port output = iterator.next();

			// FIXME: How to deal with broadcast output port? Assume only one
			// connected port currently.
			List<Port> connectedPorts = output.getConnectedPortList();
			Port connectedPort = connectedPorts.get(0);

			Entity sinkEnt = connectedPort.getContainer();
			PE sinkPE = sinkEnt.getOwnedPE();

			// If the entity of the connected port is in the same FPE,
			// do nothing, as input communications has generate the
			// value assignments.
			if (sinkPE.equals(pe)) {
				continue;
			}

			FIFO fifo = output.connectedFIFO;
			int chNo = fifo.getWriteIdx();

			fifo.put(output.token);

			// Generate PUT instructions
			String portName = ent.getName() + "_" + output.getName();
			String index = "";  
			
			// If the port type is complex, the real part and image part are
			// got separately.
			if (ct == ALUTYPE.REAL16B1D && DATATYPE.isCplx(output.token.dataType)) {
				for (int i = 0; i < output.token.getNumData(ct)/2; i++) {
					if (output.token.tokenType != TOKENTYPE.SCALAR)
						index = "["+i+"]";
					code.append("\t" + _generatePUTInstr(portName+index + ".real", chNo));
					code.append("\t" + _generatePUTInstr(portName+index + ".imag", chNo));
				}
			} else {
				for (int i = 0; i < output.token.getNumData(ct); i++) {
					if (output.token.tokenType != TOKENTYPE.SCALAR)
						index = "["+i+"]";
					code.append("\t" + _generatePUTInstr(portName+index, chNo));
				}
			}
		}
		
		return code.toString();
	}
	
	/**
	 * Generate code for calling the computation function of a given entity.
	 * 
	 * @param e
	 * @return
	 */
	private String _genCompCode(Entity e) {
		StringBuffer code = new StringBuffer();
		code.append("\t" + e.getClassName() + "(");

		// Generate input arguments.
		List<Port> iports = e.inputPortList();
		Iterator<Port> iterIn = iports.iterator();

		while (iterIn.hasNext()) {
			Port iport = iterIn.next();
			String in = e.getName() + "_" + iport.getName();
			code.append(in + ", ");
		}

		// Generate output arguments.
		List<Port> oports = e.outputPortList();
		Iterator<Port> iterOut = oports.iterator();

		while (iterOut.hasNext()) {
			Port oport = iterOut.next();
			String symbol;
			// For vector or matrix token, we use array in C, so just pass the name 
			// of the array. For scalar, use dereference.
			if (oport.token.tokenType == TOKENTYPE.SCALAR)
				symbol = "&";
			else
				symbol = "";
			String out = symbol + e.getName() + "_" + oport.getName();
			code.append(out + ", ");
		}

		// Generate parameter arguments.
		List<Parameter> parameters = e.parameterList();
		Iterator<Parameter> iterPara = parameters.iterator();

		while (iterPara.hasNext()) {
			Parameter parameter = iterPara.next();
			String strPara = e.getName() + "_" + parameter.getName();
			code.append(strPara + ", ");
		}

		// Replace trailing ','. 
		String result = code.substring(0, code.lastIndexOf(", "));

		return result + ");\n";
	}

	/**
	 * An bundled version of _generateComputationCode. This is to support
	 * hand crafted interleaving to walk around the problem caused by LLVM
	 * register allocator and preRA Scheduler.
	 * @param CGUnit
	 * @return 
	 */
	private String _genCompCodeMerged(LinkedList<Entity> CGUnit) {
		StringBuffer code = new StringBuffer();
		if (mode != Mode.FFT)
			throw new RuntimeException("ERROR: manual interleaved only for FFT");
			
		if (fft.bShareCoesWhenPossible && CGUnit.getFirst().idx < fft.coeSharePoint)
			code.append("\t"+"butterfly_sharecoe(");
		else
			code.append("\t"+"butterfly(");
		
		// Generate input arguments.
		for (Entity e : CGUnit) {
			List<Port> iports = e.inputPortList();
			Iterator<Port> iterIn = iports.iterator();
	
			while (iterIn.hasNext()) {
				Port iport = iterIn.next();
				String in = e.getName() + "_" + iport.getName();
				code.append(in + ", ");
			}		
		}
		for (Entity e : CGUnit) {
			// Generate output arguments.
			List<Port> oports = e.outputPortList();
			Iterator<Port> iterOut = oports.iterator();

			while (iterOut.hasNext()) {
				Port oport = iterOut.next();
				String out = "&" + e.getName() + "_" + oport.getName();
				code.append(out + ", ");
			}
		}
		for (Entity e : CGUnit) {
			// Generate parameter arguments.
			List<Parameter> parameters = e.parameterList();
			Iterator<Parameter> iterPara = parameters.iterator();

			while (iterPara.hasNext()) {
				Parameter parameter = iterPara.next();
				String strPara = e.getName() + "_" + parameter.getName();
				code.append(strPara + ", ");
			}
		}
		String result = code.substring(0, code.lastIndexOf(", "));

		return result + ");\n";
	}
	
	/**
	 * Create SPUs for external source and sink.
	 */
	private void _createIOCore() {
		_ioCore = new SPU(ssp, "IOCore");
		_ioCore.isIOCore = true;
		ssp.ioCore = _ioCore;
		PE ioPE = new PE(0, _ioCore);
		_ioCore.PEs.add(ioPE);
		
		Entity exSrcEnt = new Entity("SOURCE", "SOURCE");
		ioPE.addEntity(exSrcEnt);
		exSrcEnt.setOwnedPE(ioPE);
		_exSrcPort = new Port(exSrcEnt, "SOURCE", true, false);
		if (mode == Mode.FFT)
			_exSrcPort.token = new Token(_exSrcPort, DATATYPE.CPLXINT);
		else
			_exSrcPort.token = new Token(_exSrcPort, DATATYPE.INT);
		exSrcEnt.addOutputPort(_exSrcPort);

		Entity exSinkEnt = new Entity("SINK", "SINK");
		ioPE.addEntity(exSinkEnt);
		exSinkEnt.setOwnedPE(ioPE);
		_exSinkPort = new Port(exSinkEnt, "SINK", false, true);
		if (mode == Mode.FFT)
			_exSinkPort.token = new Token(_exSinkPort, DATATYPE.CPLXINT);
		else
			_exSinkPort.token = new Token(_exSinkPort, DATATYPE.INT);
		exSinkEnt.addInputPort(_exSinkPort);

	}

	/**
	 * Generate GET instructions for an input port.
	 * 
	 * @param p The port
	 * @param chNo The FIFO number from which the GET gets data
	 * @return Generated code
	 */
	private String _generateGETforPort(Port p, int chNo, ALUTYPE ct) {
		StringBuffer code = new StringBuffer();

		String portName = p.getContainer().getName() + "_" + p.getName();
		String index = "";

		// If the port type is complex, the real part and imag part are
		// got separately.
		if (ct == ALUTYPE.REAL16B1D && DATATYPE.isCplx(p.token.dataType)) {
			for (int i = 0; i < p.token.getNumData(ct)/2; i++) {
				if (p.token.tokenType != TOKENTYPE.SCALAR)
					index = "["+i+"]";
				code.append("\t"+_generateGETInstr(portName+index + ".real", chNo));
				code.append("\t"+_generateGETInstr(portName+index + ".imag", chNo));
			}
		} else {
			for (int i = 0; i < p.token.getNumData(ct); i++) {
				if (p.token.tokenType != TOKENTYPE.SCALAR)
					index = "["+i+"]";
				code.append("\t"+_generateGETInstr(portName+index, chNo));
			}
		}

		p.codeGenerated = true;

		return code.toString();
	}

	/**
	 * To check if the float will fit in the fixed-point datapath. If it is too
	 * small, set it to zero; if it is too big, throw an error; otherwise, do
	 * not change.
	 * 
	 * @param d
	 * @return
	 */
	private float _fitInRange(float d) {
		float ret;

		if (d >= ssp.conf.Max || d < ssp.conf.Min) {
			throw new RuntimeException("The data is too big to fit in");
		} else if (Math.abs(d) < ssp.conf.Precision) {
			ret = 0;
		} else {
			ret = d;
		}

		return ret;
	}

	// /////////////////////////////////////////////////////////////////
	// // public variables ////
	/** SSP instance */
	public SSP ssp;
	
	public enum Mode {
		FFT, MATRIXMULT, MOTIONEST, SOBELEDGE, NONE, MOTIONESTH264
	}
	public Mode mode = Mode.NONE;
	
	public enum FIFOAllocScheme {
		BASELINE, CONFLICTFREE, SHARED
	}	
	public FIFOAllocScheme bufAllocScheme;
	
	
	public FFT fft;
	public MatrixMult matrixMult;	
	public MotionEst motionEst;	
	public MotionEstH264 motionEstH264;	
	public SobelEdge sobelEdge;
	

	// /////////////////////////////////////////////////////////////////
	// // private variables ////
	/** Store transition records. It is used for FIFO synchronisation. */
	private List<Transition> _trans;
	
	private LinkedList<String> SOURCEs = new LinkedList<String>();
	private LinkedList<String> SINKs = new LinkedList<String>();
	
	private List<FIFO> _interPEFIFOs = new LinkedList<FIFO>();
	
	// -----------------------------------
	// Flags
	// -----------------------------------
	// When switched on, the interleaved actors are merged by hand 
	private boolean _manualIntl = false;
	private boolean _manualCode = false;
	
	
	private Document _momlDoc;

	/** A HashMap linking Entity names in MoML to Entity object */
	private Map<String, Entity> _hashedEntityList = new HashMap<String, Entity>();

	/** Store global schedule sequence */
	private List<Entity> _globalSched = new LinkedList<Entity>();
	
	/** Store CodeGen Units */
	private List<LinkedList<Entity>> _CGUnits = new LinkedList<LinkedList<Entity>>();

	/** ExSource, ExSink */
	private SPU _ioCore;
	private Port _exSrcPort, _exSinkPort;
	
	/** Enable actor interleaving in SWGen */
	private boolean _bIntl = false;
	private int _ilSize = 4;
	
	/** Support CGUnits generation */
	private boolean _packIssued = true;
	private LinkedList<Entity> _nextIssuePack;		
}
