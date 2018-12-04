package sspc.hardgen;

import java.util.Arrays;

import sspc.lib.FIFO;
import sspc.lib.SPU;
import sspc.lib.SPUConfig;
import sspc.lib.PE;
import sspc.lib.SSP;
import sspc.softgen.SWGenUtils;


public class SSPGen {
	public SSPGen(SSP ssp){
		_conf = ssp.conf;
		_ssp = ssp;
	}
	
	public void generate() {
		StringBuffer code = new  StringBuffer();
		code.append(_printHead());
		
		// Print FIFO signals
		code.append(_printFIFO());		
		
		// Print SPU Signals
		code.append("  -- SPU signals\n");
		for (SPU spu : _ssp.spus) {
			code.append(_printSPUSignals(spu));
		}
		
		code.append("begin\n\n");
		code.append("  -- Connect signals with module ports\n");
		code.append("  o_barrier <= barrier(0);\n\n");
		code.append(_connectIOChannel());
		
		// Connect FIFO signals with SPU
		code.append("  -- Connect FIFOs with SPUs\n");
		code.append(_connectFIFOsWithSPUs());
		
		// Instantiate SPUs
		code.append("  -- Instantiate PEs and clock enables\n");
		code.append(_initiateSPUs());
		
		// Instantiate FIFOs
		code.append("  -- Instantiate FIFOs\n");
		code.append(_instantiateFIFOs());
		
		code.append("end Structure;\n");
		
		// Write out
		SWGenUtils.writeToFile("out//m_fft_wrap.vhd", code.toString());
	}
	
	public void generateSystem() {
		StringBuffer code = new  StringBuffer();
		code.append(_printSystemHead());
		
		// Print connection signals
		code.append("  -- Connection signals\n");
		code.append(_printConnectionSignals());
		
		code.append("begin\n\n");
		
		// Connect IOCore with SPUs
		code.append("  -- Connect IOCore with SPUs\n");
		code.append(_connectIOCoreWithSPUs());
		
		code.append("end Structure;\n");
		// Write out
		SWGenUtils.writeToFile("out//system_top.vhd", code.toString());
	}
	
	
	private String _printHead() {
		String code = 
		  "library ieee;\n"
		+ "use ieee.std_logic_1164.all;\n"
		+ "use ieee.std_logic_arith.all;\n"
		+ "\n"
		+ "library work;\n"
		+ "use work.m_word_pkg.all;\n"
		+ "use work.m_word_config.all;\n"
		+ "\n"
		+ "Library UNISIM;\n"
		+ "use UNISIM.vcomponents.all;\n"
		+ "\n"
		+ "entity m_fft_wrap is\n"
		+ "generic (\n"
		+ "      CORE_WIDTH     : integer := " + _ssp.conf.coreWidth + ";\n"
		+ "      INPUT_WIDTH    : integer := " + _ssp.conf.inputWidth + ";\n"
		+ "      OUTPUT_WIDTH   : integer := " + _ssp.conf.outputWidth + ";\n"
		+ "      EXIN_FIFO_NUM  : integer := "+_ssp.exInFifos.size()+";\n"
		+ "      EXOUT_FIFO_NUM : integer := "+_ssp.exOutFifos.size()+");\n"
		+ "  port (\n"
		+ "    clk : in std_logic;\n"
		+ "    rst : in std_logic;\n"
		+ "\n"
		+ "    i_en_spu        : in  std_logic;\n"
		+ "    o_barrier       : out std_logic;\n"
		+ "\n"
		+ "    i_push_ch_data  : in  VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);\n"
		+ "    i_push_ch_write : in  VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);\n"
		+ "    o_push_ch_full  : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);\n"
		+ "\n"
		+ "    o_pop_ch_data   : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);\n"
		+ "    i_pop_ch_read   : in  VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);\n"
		+ "    o_pop_ch_empty  : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0));\n"
		+ "end m_fft_wrap;\n"
		+ "\n"
		+ "architecture Structure of m_fft_wrap is\n"
		+ "\n"
		+ " signal barrier     : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);\n"
		+ "\n";				
		
		return code;  
					
	}
	
	private String _printFIFO() {
		StringBuffer code = new StringBuffer();			
		for (int i=0; i<_ssp.fifos.size(); i++) {
			code.append(_printFIFOSignals(_ssp.fifos.get(i).getName()));
		}
		return code.toString();
	}
	
	private String _printFIFOSignals(String ch) {
		String code = 
		  "  signal ch_" + ch + "_a     : std_logic_vector(CORE_WIDTH-1 downto 0);\n"
		+ "  signal ch_" + ch + "_write : std_logic;\n"
		+ "  signal ch_" + ch + "_full  : std_logic;\n"
		+ "  signal ch_" + ch + "_b     : std_logic_vector(CORE_WIDTH-1 downto 0);\n"
		+ "  signal ch_" + ch + "_read  : std_logic;\n"
		+ "  signal ch_" + ch + "_empty : std_logic;\n";
		return code;
	}
	
	private String _printSPUSignals(SPU spu) {
		int i = spu.idx;
		int ich1 = spu.conf.iChNo * spu.conf.simdWay - 1;
		int och1 = spu.conf.oChNo * spu.conf.simdWay - 1;
		
		String code =
		  "  signal get_ch_data_"+i+"  : VDATA_TYPE("+ich1+" downto 0);\n"
		+ "  signal get_ch_read_"+i+"  : VSIG_TYPE("+ich1+" downto 0);\n"
		+ "  signal get_ch_empty_"+i+" : VSIG_TYPE("+ich1+" downto 0);\n"
		+ "  signal put_ch_data_"+i+"  : VDATA_TYPE("+och1+" downto 0);\n"
		+ "  signal put_ch_write_"+i+" : VSIG_TYPE("+och1+" downto 0);\n"
		+ "  signal put_ch_full_"+i+"  : VSIG_TYPE("+och1+" downto 0);\n"
		+ "\n";

		
		return code;
	}
	
	private String _connectIOChannel() {
		StringBuffer code = new  StringBuffer();
	
		for (int i=0; i<_ssp.exInFifos.size(); i++) {
			FIFO curFifo = _ssp.exInFifos.get(i);
			code.append(
				"  ch_"+curFifo.getName()+"_a <= i_push_ch_data(" + i + ");\n"
			   +"  ch_"+curFifo.getName()+"_write  <= i_push_ch_write(" + i + ");\n"
			   +"  o_push_ch_full(" + i + ") <= ch_"+curFifo.getName()+"_full;\n"
			   +"\n"
			);			
		}
		
		for (int i=0; i<_ssp.exOutFifos.size(); i++) {
			FIFO curFifo = _ssp.exOutFifos.get(i);
			code.append(
				  "  ch_"+curFifo.getName()+"_read  <= i_pop_ch_read(" + i + ");\n"
				+ "  o_pop_ch_data(" + i + ") <= ch_"+curFifo.getName()+"_b;\n"
				+ "  o_pop_ch_empty(" + i + ") <= ch_"+curFifo.getName()+"_empty;\n"
				+ "\n"
			);
		}
		
		return code.toString();
	}
	
	/** connect FIFO and PE
	 *  Search through the comm_array, take each PE as a unit, connect all its FIFO
	 *  ports with the FIFO. These ports are:
	 *	get_ch_data (b), read, empty; put_ch_data (a), write, full
	 *	
	 *	The 
	 */

	private String _connectFIFOsWithSPUs() {
		StringBuffer code = new  StringBuffer();
		// The read signal must be ored.
		String[] reads = new String[_ssp.spus.size()];
		Arrays.fill(reads, "");
				
		for (FIFO f : _ssp.fifos) {			 			
			code.append("  -- Connect FIFO " + f.getName() + " with PE\n");
			
			// Connect fifo data input parts, excluding external in FIFO
			if (!f.isExInFIFO) {
				int srcSPUIdx = f.srcPE.getSPU().idx;								
				int srcPortIdx = f.getWriteIdx() + f.srcPE.idx*f.srcPE.outputFIFOs.size();
				
				code.append(
					  "  ch_" + f.getName() + "_a <= put_ch_data_" + srcSPUIdx + "(" + srcPortIdx + ");\n"
					+ "  ch_" + f.getName() + "_write <= put_ch_write_" + srcSPUIdx + "(" + srcPortIdx + ");\n"
					+ "  put_ch_full_" + srcSPUIdx + "(" + srcPortIdx + ") <= ch_" + f.getName() + "_full;\n"
					+ "\n"
				);
			}
			
			// Connect FIFO data output parts, excluding external out FIFO. 
			// Note to deal with shared FIFO case
			if (f.isExOutFIFO) continue;
			
			int i = 0;
			String read = new String();
			for (PE sinkPE : f.sinkPEs) {
				int sinkSPUIdx = sinkPE.getSPU().idx;
				int sinkPortIdx = f.getReadIdxIn(sinkPE) + sinkPE.idx*sinkPE.inputFIFOs.size();
				
				code.append(
					"  get_ch_data_" + sinkSPUIdx + "(" + sinkPortIdx + ") <= ch_" + f.getName() + "_b;\n" + 						 
					"  get_ch_empty_" + sinkSPUIdx + "(" + sinkPortIdx + ") <= ch_" + f.getName() + "_empty;\n"
				);
				
				if (i == 0) {
					read = "  ch_" + f.getName() + "_read <= get_ch_read_" + sinkSPUIdx + "(" + sinkPortIdx + ")";
				} else {
					read += " or get_ch_read_" + sinkSPUIdx + "(" + sinkPortIdx + ")";
				}
				
				i++;
			}
			code.append(read + ";\n\n");
		}
		return code.toString();
	}
	
	/**
	 * Initiate SPUs
	 * @return
	 */
	private String _initiateSPUs() {
		StringBuffer code = new  StringBuffer();
		
		for (int i=0; i<_ssp.spus.size(); i++) {
			SPUConfig fconf = _conf.SPUConfs.get(i);
			// Set threshold for choosing LUT-RAM.
			if (!fconf.useBRAMForLargePM && fconf.pmWidth > 8)
				fconf.useBRAMForLargePM = true;
			if (!fconf.useBRAMForLargeDM && fconf.dmWidth > 8)
				fconf.useBRAMForLargeDM = true;
			if (!fconf.useBRAMForLargeSM && fconf.smWidth > 8)
				fconf.useBRAMForLargeSM = true;
						
			code.append(
				"u_core_" +i + ": m_word_core_v\n" 
			  + "generic map(\n" 
			  + "  DATA_WIDTH      => " + fconf.DataWidth() + ",\n" 
			  + "  DATA_TYPE       => " + fconf.DataType() + ",\n" 
			  + "  SLICE_NUM       => " + fconf.DSP48ENum() + ",\n"
			  + "  CORE_DATA_WIDTH => " + fconf.CoreDataWidth() + ",\n"
			  + "  OPM_NUM         => " + fconf.OPMODENum() + ",\n" 
			  + "  ALUM_NUM        => " + fconf.ALUMODENum() + ",\n" 
			  + "  FRAC_BITS       => " + _conf.fracBits + ",\n"
			  + "  NOIOCORE        => " + _conf.noIOCore + ",\n"
			  + "\n"
			  + "  VLEN       => " + fconf.simdWay + ",\n"
			  + "\n"
			  + "  -- Control Pipeline\n"
			  + "  MULREG_EN  => " + fconf.mulregEn + ",\n"
			  + "  PB0_DEPTH  => " + fconf.Pb0Depth + ",\n"
			  + "  PB1_DEPTH  => " + fconf.Pb1Depth + ",\n"
			  + "  PB2_DEPTH  => " + fconf.Pb2Depth + ",\n"
			  + "  PA0_DEPTH  => " + fconf.Pa0Depth + ",\n"
			  + "  PA1_DEPTH  => " + fconf.Pa1Depth + ",\n"
			  + "  PA1X_DEPTH => " + fconf.Pa1xDepth + ",\n"
			  + "\n"
			  + "  -- Control Branch\n"
			  + "  BRANCH_EN     => " + fconf.branchEn + ",\n"
			  + "  JMP_EN        => " + fconf.jmpEn + ",\n"  
			  + "\n"
			  + "  RPT_EN       => " + fconf.rptEn + ",\n"
			  + "  RPT_USESRL   => " + fconf.rptUseSRL + ",\n"
			  + "  RPT_SPEC_1   => " + fconf.rptSpec1 + ",\n"
			  + "  RPT_LEVELS   => " + fconf.rptLevels + ",\n"
			  + "  RPT_CNT_LEN0 => " + fconf.rptCntWidth0 + ",\n"
			  + "  RPT_CNT_LEN1 => " + fconf.rptCntWidth1 + ",\n"
			  + "  RPT_CNT_LEN2 => " + fconf.rptCntWidth2 + ",\n"
			  + "  RPT_CNT_LEN3 => " + fconf.rptCntWidth3 + ",\n"
			  + "  RPT_CNT_LEN4 => " + fconf.rptCntWidth4 + ",\n"
			  + "  RPT_BLK_LEN0 => " + fconf.rptBlkWidth0 + ",\n"
			  + "  RPT_BLK_LEN1 => " + fconf.rptBlkWidth1 + ",\n"
			  + "  RPT_BLK_LEN2 => " + fconf.rptBlkWidth2 + ",\n"
			  + "  RPT_BLK_LEN3 => " + fconf.rptBlkWidth3 + ",\n"
			  + "  RPT_BLK_LEN4 => " + fconf.rptBlkWidth4 + ",\n"
			  + "\n"
			  + "  -- Control Supported Instructions\n"
			  + "  MASK_EN      => " + fconf.maskEn + ",\n"
			  + "  MASKEQ_EN    => " + fconf.maskeqEn + ",\n"
			  + "  MASKGT_EN    => " + fconf.maskgtEn + ",\n"
			  + "  MASKLT_EN    => " + fconf.maskltEn + ",\n"
			  + "  ALUSRA1_EN   => " + fconf.alusra1En + ",\n"
			  + "  ABSDIFF_EN   => " + fconf.absdiffEn + ",\n"
			  + "  ABSDIFF_TYPE => " + fconf.absdiffType + ",\n"
			  + "\n"
			  + "  FLEXA_TYPE   => " + fconf.flexAType + ",\n"
			  + "  FLEXB_TYPE   => " + fconf.flexBType + ",\n"
			  + "  FLEXC_TYPE   => " + fconf.flexCType + ",\n"
			  + "\n"
			  + "  -- Control FIFO\n"
			  + "  GETI_EN     => " + fconf.getiEn + ",\n"
			  + "  GETCH_EN    => " + fconf.getchEn + ",\n"
			  + "  PUTCH_EN    => false,\n"
			  + "  RX_CH_NUM   => " + fconf.iChNo + ",\n"
			  + "  RX_CH_WIDTH => " + fconf.iChWidth + ",\n"
			  + "  TX_CH_NUM   => " + fconf.oChNo + ",\n"
			  + "  TX_CH_WIDTH => " + fconf.oChWidth + ",\n"
			  + "\n"
			  + "  -- Control memory\n"
			  + "  RF_EN         => " + fconf.rfEn + ",\n"
			  + "  RF_ADDR_WIDTH => " + fconf.regWidth + ",\n"
			  + "  RF_INIT_EN    => " + fconf.rfInitEn + ",\n"
			  + "  RF_INIT_FILE  => \"RFInit/rf_initFPE"+i+"PE\",\n"
			  + "\n"
			  + "  PM_SIZE       => " + fconf.pmSize + ",\n"
			  + "  PM_ADDR_WIDTH => " + fconf.pmWidth + ",\n"
			  + "  PM_DATA_WIDTH => " + fconf.pmDataWidth + ",\n"
			  + "  USE_BRAM_FOR_LARGE_PM => " + fconf.useBRAMForLargePM + ",\n"
			  + "  PM_INIT_FILE => \"PMInit/pm_init"+i+".mif\",\n"
			  + "\n"
			  + "  DM_EN                 => " + fconf.dmEn + ",\n"
			  + "  DM_OFFSET_WIDTH       => " + fconf.dmOffsetWidth + ",\n"
			  + "  DM_SIZE               => " + fconf.dmSize + ",\n"
			  + "  DM_ADDR_WIDTH         => " + fconf.dmWidth + ",\n"
			  + "  DM_DATA_WIDTH         => " + fconf.dmDataWidth + ",\n"
			  + "  DM_INIT_EN            => " + fconf.dmInitEn + ",\n"
			  + "  USE_BRAM_FOR_LARGE_DM => " + fconf.useBRAMForLargeDM + ",\n"
			  + "  DM_INIT_FILE          => \"DMInit/dm_initFPE"+i+"PE\",\n"
			  + "  DM_RB_B_NUM           => " + fconf.dmRBNum0 + ",\n"
			  + "  DM_RB_C_NUM           => " + fconf.dmRBNum1 + ",\n"
			  + "  DM_RB_B_INITIAL0      => " + fconf.dmRBInitialB0 + ",\n"
			  + "  DM_RB_B_INITIAL1      => " + fconf.dmRBInitialB1 + ",\n"
			  + "  DM_RB_B_INITIAL2      => " + fconf.dmRBInitialB2 + ",\n"
			  + "  DM_RB_C_INITIAL0      => " + fconf.dmRBInitialC0 + ",\n"
			  + "  DM_WB_INITIAL         => " + fconf.dmWBInitial + ",\n"
			  + "  DM_RB_B_AUTOINC_SIZE0 => " + fconf.dmRBAutoincSizeB0 + ",\n"
			  + "  DM_RB_B_AUTOINC_SIZE1 => " + fconf.dmRBAutoincSizeB1 + ",\n"
			  + "  DM_RB_B_AUTOINC_SIZE2 => " + fconf.dmRBAutoincSizeB2 + ",\n"
			  + "  DM_RB_C_AUTOINC_SIZE0 => " + fconf.dmRBAutoincSizeC0 + ",\n"
			  + "  DM_WB_AUTOINC_SIZE    => " + fconf.dmWBAutoincSize + ",\n"
			  + "  DM_OFFSET_EN          => " + fconf.dmOffsetEn + ",\n"
			  + "  DM_DIRECT_EN          => " + fconf.dmDirectEn + ",\n"
			  + "  DM_RB_B_SET_EN0       => " + fconf.dmRBSetEnB0 + ",\n"
			  + "  DM_RB_B_SET_EN1       => " + fconf.dmRBSetEnB1 + ",\n"
			  + "  DM_RB_B_SET_EN2       => " + fconf.dmRBSetEnB2 + ",\n"
			  + "  DM_RB_C_SET_EN0       => " + fconf.dmRBSetEnC0 + ",\n"
			  + "  DM_WB_SET_EN          => " + fconf.dmWBSetEn + ",\n"
			  + "  DM_RB_B_AUTOINC_EN0   => " + fconf.dmRBAutoincEnB0 + ",\n"
			  + "  DM_RB_B_AUTOINC_EN1   => " + fconf.dmRBAutoincEnB1 + ",\n"
			  + "  DM_RB_B_AUTOINC_EN2   => " + fconf.dmRBAutoincEnB2 + ",\n"
			  + "  DM_RB_C_AUTOINC_EN0   => " + fconf.dmRBAutoincEnC0 + ",\n"
			  + "  DM_WB_AUTOINC_EN      => " + fconf.dmWBAutoincEn + ",\n"
			  + "  DM_RB_B_INC_EN0       => " + fconf.dmRBIncEnB0 + ",\n"
			  + "  DM_RB_B_INC_EN1       => " + fconf.dmRBIncEnB1 + ",\n"
			  + "  DM_RB_B_INC_EN2       => " + fconf.dmRBIncEnB2 + ",\n"
			  + "  DM_RB_C_INC_EN0       => " + fconf.dmRBIncEnC0 + ",\n"
			  + "  DM_WB_INC_EN          => " + fconf.dmWBIncEn + ",\n"
			  
			  + "\n"
			  + "  SM_EN        => " + fconf.smEn + ",\n"
			  + "  SM_OFFSET_WIDTH  => " + fconf.smOffsetWidth + ",\n"
			  + "  SM_SIZE       => " + fconf.smSize + ",\n"
			  + "  SM_ADDR_WIDTH    => " + fconf.smWidth + ",\n"
			  + "  USE_BRAM_FOR_LARGE_SM => " + fconf.useBRAMForLargeSM + ",\n"
			  + "  SM_INIT_FILE => \"IMMInit/imm_init"+i+".mif\",\n"
			  + "  SM_DIRECT_EN => "+fconf.smDirectEn+",\n"
			  + "  SM_OFFSET_EN => "+fconf.smOffsetEn+",\n"
			  + "  SM_READONLY => "+fconf.smReadonly+",\n"
			  + "  SM_RB_SET_EN0 => "+fconf.smRBSetEn0+",\n"
			  + "  SM_RB_INC_EN0 => "+fconf.smRBIncEn0+",\n"
			  + "  SM_WB_INC_EN0 => "+fconf.smWBIncEn0+",\n"
			  + "  SM_RB_AUTOINC_EN0 => "+fconf.smRBAutoincEn0+",\n"
			  + "  SM_WB_AUTOINC_EN0 => "+fconf.smWBAutoincEn0+",\n"
			  + "  SM_RB_AUTOINC_SIZE0 => "+fconf.smRBAutoincSize0+",\n"
			  + "  SM_WB_AUTOINC_SIZE0 => "+fconf.smWBAutoincSize0+"\n"			  
			  + ")\n"
			  + "port map(\n"
			  + "  clk => clk,\n"
			  + "  rst => rst,\n"
			  + "\n"
			  + "  i_en_spu => i_en_spu,\n"
			  + "  o_barrier => open,\n"
			  + "\n"
			  + "  -- Communication port signals\n"
			  + "  i_get_ch_data  => get_ch_data_" +i + ",\n"
			  + "  o_get_ch_read  => get_ch_read_" +i + ",\n"
			  + "  i_get_ch_empty => get_ch_empty_" +i + ",\n"
			  + "\n"
			  + "  -- Output channel\n"
			  + "  o_put_ch_data  => put_ch_data_" +i + ",\n"
			  + "  o_put_ch_write => put_ch_write_" +i + ",\n"
			  + "  i_put_ch_full  => put_ch_full_" +i + "\n"
			  + ");\n"
			  + "\n"
			  + "\n");
		}
		return code.toString();
	}
	
	private String _instantiateFIFOs() {
		StringBuffer code = new  StringBuffer();
		
		for (FIFO f : _ssp.fifos) {			
			code.append(_printFIFOInstatance(f, f.getName(), f.getDepth()));
		}

		return code.toString();
	}
	
	/**
	 * Help function to print an FIFO instance
	 * @param name name of the FIFO
	 * @param depth depth of the FIFO
	 * @return
	 */
	private String _printFIFOInstatance(FIFO f, String name, int depth) {
		String code = new String("");
		if (f.isExInFIFO) { 
			String insuffix = new String("");
			if( _conf.inputWidth < _conf.coreWidth)
				insuffix = "(INPUT_WIDTH-1 downto 0)";
			 code = "u_fifo_"+name+": m_word_fifo\n"
			  			+ "generic map( WIDTH =>INPUT_WIDTH, DEPTH=>" +depth+" )\n"
						+ "port map(\n"
						+ "  i_data  => ch_"+name+"_a"+insuffix+",\n"
						+ "  write   => ch_"+name+"_write,\n"
						+ "  o_full  => ch_"+name+"_full,\n"
						+ "\n"
						+ "  o_data  => ch_"+name+"_b"+insuffix+",\n"
						+ "  read    => ch_"+name+"_read,\n"
						+ "  o_empty => ch_"+name+"_empty,\n"
						+ "  clk     => clk\n"
						+ ");\n"
						+ "\n";
		} else if (f.isExOutFIFO) {
			String outsuffix = new String("");
			if (_conf.outputWidth < _conf.coreWidth)
				outsuffix = "(OUTPUT_WIDTH-1 downto 0)";
			code = "u_fifo_"+name+": m_word_fifo\n"
		  			+ "generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>" +depth+" )\n"
					+ "port map(\n"
					+ "  i_data  => ch_"+name+"_a"+outsuffix+",\n"
					+ "  write   => ch_"+name+"_write,\n"
					+ "  o_full  => ch_"+name+"_full,\n"
					+ "\n"
					+ "  o_data  => ch_"+name+"_b"+outsuffix+",\n"
					+ "  read    => ch_"+name+"_read,\n"
					+ "  o_empty => ch_"+name+"_empty,\n"
					+ "  clk     => clk\n"
					+ ");\n"
					+ "\n";
		} else {
			code = "u_fifo_"+name+": m_word_fifo\n"
		  			+ "generic map( WIDTH =>CORE_WIDTH, DEPTH=>" +depth+" )\n"
					+ "port map(\n"
					+ "  i_data  => ch_"+name+"_a,\n"
					+ "  write   => ch_"+name+"_write,\n"
					+ "  o_full  => ch_"+name+"_full,\n"
					+ "\n"
					+ "  o_data  => ch_"+name+"_b,\n"
					+ "  read    => ch_"+name+"_read,\n"
					+ "  o_empty => ch_"+name+"_empty,\n"
					+ "  clk     => clk\n"
					+ ");\n"
					+ "\n";
		}
		return code;
	}
	
	private String _printSystemHead() {
		String code = 
				  "library ieee;\n"
				+ "use ieee.std_logic_1164.all;\n"
				+ "\n"
				+ "library work;\n"
				+ "use work.m_word_pkg.all;\n"
				+ "use work.m_word_config.all;\n"
				+ "\n"
				+ "entity ssp_top is\n"
				+ "generic (\n"
				+ "  DQ_WIDTH            : integer:= 64;\n"
				+ "  MASK_WIDTH          : integer:= 8\n"
				+ ");\n"
				+ "  port (\n"
				+ "    clk : in std_logic;\n"
				+ "    rst : in std_logic;\n"
				+ "    o_mif_af_cmd   :  out std_logic_vector(2 downto 0);\n" 
				+ "    o_mif_af_addr  :  out std_logic_vector(30 downto 0);\n"
				+ "    o_mif_af_wren  :  out std_logic;\n"
				+ "    i_mif_af_afull :  in  std_logic;\n"
				+ "    o_mif_wdf_wren :  out std_logic;\n"
				+ "    o_mif_wdf_data :  out std_logic_vector(2*DQ_WIDTH-1 downto 0);\n"
				+ "    o_mif_wdf_mask_data: out std_logic_vector(2*MASK_WIDTH-1 downto 0);\n"
				+ "    i_mif_wdf_afull:  in  std_logic;\n"
				+ "    i_mif_rd_data  :  in  std_logic_vector(2*DQ_WIDTH-1 downto 0);\n"
				+ "    i_mif_rd_valid :  in  std_logic\n"
				+ "  );\n"
				+ "end ssp_top;\n"
				+ "\n"
				+ "architecture Structure of ssp_top is\n"
				+ "\n";
		return code;
	}
	
	private String _printConnectionSignals() {
		int m2sNum = _ssp.exInFifos.size();
		int s2mNum = _ssp.exOutFifos.size();
		String code =
				"  signal m2s_data   : VDATA_TYPE(" + (m2sNum-1) + " downto 0);\n" +
			    "  signal m2s_write  : VSIG_TYPE(" + (m2sNum-1) + " downto 0);\n" +
			    "  signal m2s_en_spu : std_logic;\n" +
			    "  signal s2m_data   : VDATA_TYPE(" + (s2mNum-1) + " downto 0);\n" +
			    "  signal s2m_read   : VSIG_TYPE(" + (s2mNum-1) + " downto 0);\n" +
			    "  signal s2m_barrier: std_logic;\n";
		return code;
		
	}
	
	private String _connectIOCoreWithSPUs() {
		SPUConfig ioconf = _ssp.ioCore.conf;
		String code = 
				    "u_iocore: m_word_iocore\n"
				  + "generic map(\n" 
				  + "  IO_WIDTH        => " + _ssp.conf.coreWidth + ",\n"
				  + "\n"
				  + "  -- Control Pipeline\n"
				  + "  PB0_DEPTH  => " + ioconf.Pb0Depth + ",\n"
				  + "  PB1_DEPTH  => " + ioconf.Pb1Depth + ",\n"
				  + "  PB2_DEPTH  => " + "1" + ",\n"
				  + "  PA0_DEPTH  => " + "1" + ",\n"
				  + "  PA1_DEPTH  => " + "1" + ",\n"
				  + "\n"
				  + "  -- Control Branch\n"
				  + "  JMP_EN        => " + "true" + ",\n"  
				  + "\n"
				  + "  RPT_EN       => " + ioconf.rptEn + ",\n"
				  + "  RPT_USESRL   => " + "false" + ",\n"
				  + "  RPT_SPEC_1   => " + "false"  + ",\n"
				  + "  RPT_LEVELS   => " + ioconf.rptLevels + ",\n"
				  + "  RPT_CNT_LEN0 => " + ioconf.rptCntWidth0 + ",\n"
				  + "  RPT_CNT_LEN1 => " + ioconf.rptCntWidth1 + ",\n"
				  + "  RPT_CNT_LEN2 => " + ioconf.rptCntWidth2 + ",\n"
				  + "  RPT_CNT_LEN3 => " + ioconf.rptCntWidth3 + ",\n"
				  + "  RPT_CNT_LEN4 => " + ioconf.rptCntWidth4 + ",\n"
				  + "  RPT_BLK_LEN0 => " + ioconf.rptBlkWidth0 + ",\n"
				  + "  RPT_BLK_LEN1 => " + ioconf.rptBlkWidth1 + ",\n"
				  + "  RPT_BLK_LEN2 => " + ioconf.rptBlkWidth2 + ",\n"
				  + "  RPT_BLK_LEN3 => " + ioconf.rptBlkWidth3 + ",\n"
				  + "  RPT_BLK_LEN4 => " + ioconf.rptBlkWidth4 + ",\n"
				  + "\n"
				  + "  -- Control FIFO\n"
				  + "  PG_EN       => true,\n"
				  + "  GETCH_EN    => " + "true" + ",\n"
				  + "  PUTCH_EN    => " + "true" + ",\n"
				  + "  RX_CH_NUM   => " + ioconf.iChNo + ",\n"
				  + "  RX_CH_WIDTH => " + ioconf.iChWidth + ",\n"
				  + "  TX_CH_NUM   => " + ioconf.oChNo + ",\n"
				  + "  TX_CH_WIDTH => " + ioconf.oChWidth + ",\n"
				  + "\n"
				  + "  -- Control memory\n"
				  + "  DQ_WIDTH            => " + "64" + ",\n"
				  + "  MASK_WIDTH          => " + "8" + ",\n"
				  + "  BURST_LEN           => " + ioconf.emBurstLen + ",\n"
				  + "  EM_RB_NUM           => " + ioconf.emRBNum + ",\n"
				  + "  EM_RB_INITIAL0      => " + ioconf.emRBInitial0 + ",\n"
				  + "  EM_RB_INITIAL1      => " + ioconf.emRBInitial1 + ",\n"
				  + "  EM_WB_INITIAL0      => " + ioconf.emWBInitial0 + ",\n"
				  + "  EM_RB_AUTOINC_SIZE0 => " + ioconf.emRBAutoincSize0 + ",\n"
				  + "  EM_RB_AUTOINC_SIZE1 => " + ioconf.emRBAutoincSize1 + ",\n"
				  + "  EM_WB_AUTOINC_SIZE0 => " + ioconf.emWBAutoincSize0 + ",\n"
				  + "  EM_RB_AUTOINC_EN0   => " + ioconf.emRBAutoincEn0 + ",\n"
				  + "  EM_RB_AUTOINC_EN1   => " + ioconf.emRBAutoincEn1 + ",\n"
				  + "  EM_WB_AUTOINC_EN0   => " + ioconf.emWBAutoincEn0 + ",\n"
				  + "  EM_RB_INC_EN0       => " + ioconf.emRBIncEn0 + ",\n"
				  + "  EM_RB_INC_EN1       => " + ioconf.emRBIncEn1 + ",\n"
				  + "  EM_WB_INC_EN0       => " + ioconf.emWBIncEn0 + ",\n"
				  + "\n"
				  + "  PM_SIZE       => " + ioconf.pmSize + ",\n"
				  + "  PM_ADDR_WIDTH => " + ioconf.pmWidth + ",\n"
				  + "  PM_DATA_WIDTH => " + ioconf.pmDataWidth + ",\n"
				  + "  USE_BRAM_FOR_LARGE_PM => " + ioconf.useBRAMForLargePM + ",\n"
				  + "  PM_INIT_FILE => \"PMInit/iocore.mif\"\n"
				  + ")\n"
				  + "port map(\n"
				  + "  clk => clk,\n"
				  + "  rst => rst,\n"
				  + "\n"
				  + "  -- Control\n"
				  + "  o_en_spu  => m2s_en_spu,\n"
				  + "  i_barrier => s2m_barrier,\n"
				  + "\n"
				  + "  -- Memory Interface\n"
				  + "  o_mif_af_cmd   => o_mif_af_cmd,\n"
				  + "  o_mif_af_addr  => o_mif_af_addr,\n"
				  + "  o_mif_af_wren  => o_mif_af_wren,\n"
				  + "  i_mif_af_afull => i_mif_af_afull,\n"
				  + "\n"
				  + "  o_mif_wdf_wren => o_mif_wdf_wren,\n"
				  + "  o_mif_wdf_data => o_mif_wdf_data,\n"
				  + "  o_mif_wdf_mask_data => o_mif_wdf_mask_data,\n"
				  + "  i_mif_wdf_afull=> i_mif_wdf_afull,\n"
				  + "  i_mif_rd_data  => i_mif_rd_data,\n"
				  + "  i_mif_rd_valid => i_mif_rd_valid,\n"
				  + "\n"
				  + "  -- Communication port signals\n"
				  + "  i_get_ch_data  => s2m_data,\n"
				  + "  o_get_ch_read  => s2m_read,\n"
				  + "  i_get_ch_empty => open,\n"
				  + "\n"
				  + "  -- Output channel\n"
				  + "  o_put_ch_data  => m2s_data,\n"
				  + "  o_put_ch_write => m2s_write,\n"
				  + "  i_put_ch_almostfull  => open\n"
				  + ");\n"
				  + "\n"
				  + "u_spus: m_fft_wrap\n"
				  + "generic map(\n" 
				  + "  CORE_WIDTH     => " + _ssp.conf.coreWidth + ",\n"
			 	  + "  INPUT_WIDTH    =>" + _ssp.conf.inputWidth + ",\n"
				  + "  OUTPUT_WIDTH   =>" + _ssp.conf.outputWidth + ",\n"
				  + "  EXIN_FIFO_NUM  => " + _ssp.exInFifos.size()+",\n"
				  + "  EXOUT_FIFO_NUM => " + _ssp.exOutFifos.size()+"\n"
				  +")\n"
				  + "port map(\n"
				  + "  clk => clk,\n"
				  + "  rst => rst,\n"
				  + "\n"
				  + "  -- Control\n"
				  + "  i_en_spu  => m2s_en_spu,\n"
				  + "  o_barrier => s2m_barrier,\n"
				  + "\n"
				  + "  i_push_ch_data  => m2s_data,\n"
				  + "  i_push_ch_write => m2s_write,\n"
				  + "  o_push_ch_full  => open,\n"
				  + "\n"
				  + "  o_pop_ch_data  => s2m_data,\n"
				  + "  i_pop_ch_read => s2m_read,\n"
				  + "  o_pop_ch_empty  => open\n"
				  + ");\n"
				  ;
		
		return code;
	}
	
	
	private SSPConfig _conf;
	private SSP _ssp;
}
