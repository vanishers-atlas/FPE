-- Filename: ssp_pkg.vhd
-- Author: Xuezheng Chu
-- Description: constant, component package
-- Called by: severy entity
-- Revision History: 20-11-09
-- Revision 1.0

--///////////////////////////////////////////////////////////////////
--////                         Package                           ////
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library work;
use work.ssp_typedef.all;

package ssp_pkg is

-- Constant types for flexible ports         
constant constFLEX_R   : integer := 1;
constant constFLEX_M   : integer := 2;
constant constFLEX_RM  : integer := 3;
constant constFLEX_I   : integer := 4;
constant constFLEX_RI  : integer := 5;
constant constFLEX_MI  : integer := 6;
constant constFLEX_RMI : integer := 7;
constant constFLEX_F   : integer := 8;
constant constFLEX_RF  : integer := 9;
constant constFLEX_MF  : integer := 10;
constant constFLEX_RMF : integer := 11;
constant constFLEX_IF  : integer := 12;
constant constFLEX_RIF : integer := 13;
constant constFLEX_MIF : integer := 14;
constant constFLEX_RMIF: integer := 15;

function log_2 (x : positive) return natural;
function vectorize(s: std_logic) return std_logic_vector;
	
component axis_ssp_ip_v2_0_S00_AXIS is
	generic (
		-- Users to add parameters here

		-- User parameters ends
		-- Do not modify the parameters beyond this line

		-- AXI4Stream sink: Data Width
		C_S_AXIS_TDATA_WIDTH	: integer	:= 64;
		NUMBER_OF_INPUT_WORDS	: integer	:= 1024
	);
	port (
		-- Users to add ports here

		-- User ports ends
		-- Do not modify the ports beyond this line

		-- AXI4Stream sink: Clock
		S_AXIS_ACLK	: in std_logic;
		-- AXI4Stream sink: Reset
		S_AXIS_ARESETN	: in std_logic;
		-- Ready to accept data in
		S_AXIS_TREADY	: out std_logic;
		-- Data in
		S_AXIS_TDATA	: in std_logic_vector(C_S_AXIS_TDATA_WIDTH-1 downto 0);
		-- Byte qualifier
		-- S_AXIS_TSTRB	: in std_logic_vector((C_S_AXIS_TDATA_WIDTH/8)-1 downto 0);
		-- Indicates boundary of last packet
		S_AXIS_TLAST	: in std_logic;
		-- Data is in valid
		S_AXIS_TVALID	: in std_logic;
		
		-- to ssp
		SSP_DATA_OUT : out std_logic_vector(C_S_AXIS_TDATA_WIDTH-1 downto 0);
		SSP_AXIS_TREADY	: in std_logic;
		SSP_AXIS_TVALID	: out std_logic;
		SSP_AXIS_TLAST : out std_logic;
		SSP_FIFO_IN_EMPTY : in std_logic;
		SSP_FIFO_IN_FULL : in std_logic;
		SSP_DATA_WREN : out std_logic;
		SSP_write_pointer : out std_logic_vector(11 downto 0);
		M_AXIS_IDLE : in std_logic
	);
end component;

component axis_ssp_ip_v2_0_M00_AXIS is
	generic (
		-- Users to add parameters here

		-- User parameters ends
		-- Do not modify the parameters beyond this line

		-- Width of S_AXIS address bus. The slave accepts the read and write addresses of width C_M_AXIS_TDATA_WIDTH.
		C_M_AXIS_TDATA_WIDTH	: integer	:= 32;
		-- Start count is the numeber of clock cycles the master will wait before initiating/issuing any transaction.
		C_M_START_COUNT	: integer	:= 32;
		NUMBER_OF_OUTPUT_WORDS : integer	:= 1024
	);
	port (
		-- Users to add ports here

		-- User ports ends
		-- Do not modify the ports beyond this line

		-- Global ports
		M_AXIS_ACLK	: in std_logic;
		-- 
		M_AXIS_ARESETN	: in std_logic;
		-- Master Stream Ports. TVALID indicates that the master is driving a valid transfer, A transfer takes place when both TVALID and TREADY are asserted. 
		M_AXIS_TVALID	: out std_logic;
		-- TDATA is the primary payload that is used to provide the data that is passing across the interface from the master.
		M_AXIS_TDATA	: out std_logic_vector(C_M_AXIS_TDATA_WIDTH-1 downto 0);
		-- TSTRB is the byte qualifier that indicates whether the content of the associated byte of TDATA is processed as a data byte or a position byte.
		--M_AXIS_TSTRB	: out std_logic_vector((C_M_AXIS_TDATA_WIDTH/8)-1 downto 0);
		-- TLAST indicates the boundary of a packet.
		M_AXIS_TLAST	: out std_logic;
		-- TREADY indicates that the slave can accept a transfer in the current cycle.
		M_AXIS_TREADY	: in std_logic;
	
		-- to ssp
		SSP_DATA_IN : in std_logic_vector(C_M_AXIS_TDATA_WIDTH-1 downto 0);
		SSP_AXIS_TREADY	: out std_logic;
		SSP_AXIS_TVALID	: in std_logic;
		SSP_AXIS_TLAST : in std_logic;
		SSP_FIFO_IN_EMPTY : in std_logic;
		SSP_FIFO_IN_FULL : in std_logic;
		SSP_DATA_RDEN : out std_logic;
		SSP_read_pointer : out std_logic_vector(11 downto 0);
		M_AXIS_IDLE : out std_logic
	);
end component;

--**
--* Component ssp_wrap
--**
COMPONENT ssp_axi_fft_stage_1st is 
    generic(
        DATA_WIDTH  :  integer  :=  32;
        SDATA_WIDTH  :  integer  :=  64;
		EXIN_FIFO_NUM : integer := 2;
		EXOUT_FIFO_NUM : integer := 2;
		DEXOUT_FIFO_NUM : integer := 1;
		NUMBER_OF_INPUT_WORDS  : integer := 256; 
		NUMBER_OF_OUTPUT_WORDS : integer := 256;
		NUMBER_OF_DOUTPUT_WORDS : integer := 1;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
    );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK	: in	std_logic:= '0'; 
		ARESETN	: in	std_logic:= '0'; 
		S_AXIS_TREADY	: out	std_logic:= '0';
		S_AXIS_TDATA	: in	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		S_AXIS_TLAST	: in	std_logic:= '0'; 
		S_AXIS_TVALID	: in	std_logic:= '0';
		M_AXIS_TVALID	: out	std_logic:= '0';
		M_AXIS_TDATA	: out	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST	: out	std_logic:= '0';
		M_AXIS_TREADY	: in	std_logic:= '0';
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
		IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		IN_DATA_LAST   : out std_logic := '0';
		OUT_DATA_LAST  : out std_logic := '0';
		OUT_DDATA_LAST  : out std_logic := '0';
		-- debug		
		M_AXIS_TVALID_1	: out	std_logic:= '0';
		M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST_1	: out	std_logic:= '0';
		M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
END COMPONENT;

COMPONENT ssp_axi_fft_stage_2nd is 
    generic(
        DATA_WIDTH  :  integer  :=  32;
        SDATA_WIDTH  :  integer  :=  64;
		EXIN_FIFO_NUM : integer := 2;
		EXOUT_FIFO_NUM : integer := 2;
		DEXOUT_FIFO_NUM : integer := 1;
		NUMBER_OF_INPUT_WORDS  : integer := 256; 
		NUMBER_OF_OUTPUT_WORDS : integer := 256;
		NUMBER_OF_DOUTPUT_WORDS : integer := 1;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
    );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK	: in	std_logic:= '0'; 
		ARESETN	: in	std_logic:= '0'; 
		S_AXIS_TREADY	: out	std_logic:= '0';
		S_AXIS_TDATA	: in	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		S_AXIS_TLAST	: in	std_logic:= '0'; 
		S_AXIS_TVALID	: in	std_logic:= '0';
		M_AXIS_TVALID	: out	std_logic:= '0';
		M_AXIS_TDATA	: out	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST	: out	std_logic:= '0';
		M_AXIS_TREADY	: in	std_logic:= '0';
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
		IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		IN_DATA_LAST   : out std_logic := '0';
		OUT_DATA_LAST  : out std_logic := '0';
		OUT_DDATA_LAST  : out std_logic := '0';
		-- debug		
		M_AXIS_TVALID_1	: out	std_logic:= '0';
		M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST_1	: out	std_logic:= '0';
		M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
END COMPONENT;

COMPONENT ssp_axi_fft_stage_3rd is 
    generic(
        DATA_WIDTH  :  integer  :=  32;
        SDATA_WIDTH  :  integer  :=  64;
		EXIN_FIFO_NUM : integer := 2;
		EXOUT_FIFO_NUM : integer := 2;
		DEXOUT_FIFO_NUM : integer := 1;
		NUMBER_OF_INPUT_WORDS  : integer := 256; 
		NUMBER_OF_OUTPUT_WORDS : integer := 256;
		NUMBER_OF_DOUTPUT_WORDS : integer := 1;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
    );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK	: in	std_logic:= '0'; 
		ARESETN	: in	std_logic:= '0'; 
		S_AXIS_TREADY	: out	std_logic:= '0';
		S_AXIS_TDATA	: in	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		S_AXIS_TLAST	: in	std_logic:= '0'; 
		S_AXIS_TVALID	: in	std_logic:= '0';
		M_AXIS_TVALID	: out	std_logic:= '0';
		M_AXIS_TDATA	: out	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST	: out	std_logic:= '0';
		M_AXIS_TREADY	: in	std_logic:= '0';
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
		IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		IN_DATA_LAST   : out std_logic := '0';
		OUT_DATA_LAST  : out std_logic := '0';
		OUT_DDATA_LAST  : out std_logic := '0';
		-- debug		
		M_AXIS_TVALID_1	: out	std_logic:= '0';
		M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST_1	: out	std_logic:= '0';
		M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
END COMPONENT;

COMPONENT ssp_axi_fft_stage_4th is 
    generic(
        DATA_WIDTH  :  integer  :=  32;
        SDATA_WIDTH  :  integer  :=  64;
		EXIN_FIFO_NUM : integer := 2;
		EXOUT_FIFO_NUM : integer := 2;
		DEXOUT_FIFO_NUM : integer := 1;
		NUMBER_OF_INPUT_WORDS  : integer := 256; 
		NUMBER_OF_OUTPUT_WORDS : integer := 256;
		NUMBER_OF_DOUTPUT_WORDS : integer := 1;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
    );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK	: in	std_logic:= '0'; 
		ARESETN	: in	std_logic:= '0'; 
		S_AXIS_TREADY	: out	std_logic:= '0';
		S_AXIS_TDATA	: in	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		S_AXIS_TLAST	: in	std_logic:= '0'; 
		S_AXIS_TVALID	: in	std_logic:= '0';
		M_AXIS_TVALID	: out	std_logic:= '0';
		M_AXIS_TDATA	: out	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST	: out	std_logic:= '0';
		M_AXIS_TREADY	: in	std_logic:= '0';
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
		IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		IN_DATA_LAST   : out std_logic := '0';
		OUT_DATA_LAST  : out std_logic := '0';
		OUT_DDATA_LAST  : out std_logic := '0';
		-- debug		
		M_AXIS_TVALID_1	: out	std_logic:= '0';
		M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST_1	: out	std_logic:= '0';
		M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
END COMPONENT;

COMPONENT ssp_axi_fft_stage_5th is 
    generic(
        DATA_WIDTH  :  integer  :=  32;
        SDATA_WIDTH  :  integer  :=  64;
		EXIN_FIFO_NUM : integer := 2;
		EXOUT_FIFO_NUM : integer := 2;
		DEXOUT_FIFO_NUM : integer := 1;
		NUMBER_OF_INPUT_WORDS  : integer := 256; 
		NUMBER_OF_OUTPUT_WORDS : integer := 256;
		NUMBER_OF_DOUTPUT_WORDS : integer := 1;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
    );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK	: in	std_logic:= '0'; 
		ARESETN	: in	std_logic:= '0'; 
		S_AXIS_TREADY	: out	std_logic:= '0';
		S_AXIS_TDATA	: in	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		S_AXIS_TLAST	: in	std_logic:= '0'; 
		S_AXIS_TVALID	: in	std_logic:= '0';
		M_AXIS_TVALID	: out	std_logic:= '0';
		M_AXIS_TDATA	: out	std_logic_vector(SDATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST	: out	std_logic:= '0';
		M_AXIS_TREADY	: in	std_logic:= '0';
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
		IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
		IN_DATA_LAST   : out std_logic := '0';
		OUT_DATA_LAST  : out std_logic := '0';
		OUT_DDATA_LAST  : out std_logic := '0';
		-- debug		
		M_AXIS_TVALID_1	: out	std_logic:= '0';
		M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
		M_AXIS_TLAST_1	: out	std_logic:= '0';
		M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
END COMPONENT;
    
component ssp_axi_fft_stage_final is 
		 generic(
			  DATA_WIDTH  :  integer  :=  32;
			  SDATA_WIDTH  :  integer  :=  64;
			  EXIN_FIFO_NUM : integer := 2;
			  EXOUT_FIFO_NUM : integer := 1;
		DEXOUT_FIFO_NUM : integer := 1;
			  NUMBER_OF_INPUT_WORDS  : integer := 1024; 
			  NUMBER_OF_OUTPUT_WORDS : integer := 2048;
			  NUMBER_OF_DOUTPUT_WORDS : integer := 1;
			RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
			PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
			DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
			SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
		 );
	port  
	( 
		-- DO NOT EDIT BELOW THIS LINE --------------------- 
		-- Bus protocol ports, do not add or delete.  
		ACLK    : in    std_logic; 
		ARESETN    : in    std_logic; 
		S_AXIS_TREADY    : out    std_logic;
		S_AXIS_TDATA    : in    std_logic_vector(SDATA_WIDTH-1 downto 0);
		S_AXIS_TLAST    : in    std_logic;
		S_AXIS_TVALID    : in    std_logic;
		M_AXIS_TVALID    : out    std_logic;
		M_AXIS_TDATA    : out    std_logic_vector(DATA_WIDTH-1 downto 0);
		M_AXIS_TLAST    : out    std_logic;
		M_AXIS_TREADY    : in    std_logic;
		-- DO NOT EDIT ABOVE THIS LINE --------------------- 
			-- indicator
			IN_DATA_COUNT  : out std_logic_vector(15 downto 0) := (others=>'0');
			OUT_DATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
			OUT_DDATA_COUNT : out std_logic_vector(15 downto 0) := (others=>'0');
			IN_DATA_LAST   : out std_logic := '0';
			OUT_DATA_LAST  : out std_logic := '0';
			OUT_DDATA_LAST  : out std_logic := '0';
			-- debug		
			M_AXIS_TVALID_1	: out	std_logic:= '0';
			M_AXIS_TDATA_1	: out	std_logic_vector(DATA_WIDTH-1 downto 0) := (others=>'0'); 
			M_AXIS_TLAST_1	: out	std_logic:= '0';
			M_AXIS_TREADY_1	: in	std_logic:= '0'
	); 
end component;

--**
--* Component ssp_wrap
--**
COMPONENT ssp_cache_core_wrap_stage_1st
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug port	
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);		
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0')
	);
END COMPONENT;

COMPONENT ssp_cache_core_wrap_stage_2nd
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
	);
END COMPONENT;

COMPONENT ssp_cache_core_wrap_stage_3rd
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
	);
END COMPONENT;

COMPONENT ssp_cache_core_wrap_stage_4th
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
	);
END COMPONENT;

COMPONENT ssp_cache_core_wrap_stage_5th
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
	);
END COMPONENT;

COMPONENT ssp_cache_core_wrap_stage_final
	generic ( 
		CORE_WIDTH : integer := 16;
		INPUT_WIDTH : integer := 16;
		OUTPUT_WIDTH : integer := 16;
		EXIN_FIFO_NUM : integer := 1;
		EXOUT_FIFO_NUM : integer := 1;
		INPUT_WORDS : integer := 1;
		OUTPUT_WORDS : integer := 1;
		DOUTPUT_WORDS : integer := 1;
		IOFIFODEPTH : integer := 1024;
		RF_INIT_FILE         : string := "RFInit/rf_initSPU0PE.mif";
		PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
		DM_INIT_FILE         : string := "DMInit/dm_initSPU0PE";
		SM_INIT_FILE         : string := "IMMInit/imm_init0.mif"
	);
	port(
		clk : in std_logic;
		rst : in std_logic;
		i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
		o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
		-- debug
		o_ddata_last : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		i_dpop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		o_dpop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
		dtlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
	);
END COMPONENT;

--**
--* Component data_in
--**
component data_in
  generic(
    ARRAY_NUM    : integer := 2;
    RF_IO_WIDTH  : integer := 16
    );
  port (     
  clk         : in    std_logic;
  o_rst       : out   std_logic;
  i_pm_finish : in    std_logic;
  
  --program memory config
  o_data      : out   VDATA_TYPE(ARRAY_NUM-1 downto 0);
  o_data_wen  : out   VSIG_TYPE(ARRAY_NUM-1 downto 0));  
end component;

--**
--* Component s2p_fifoin
--**
component s2p_fifoin
generic(DATA_WIDTH    : integer := 16;
        CH_NUM    : integer := 128);
port(clk, rst : in std_logic;

i_push_ch_data  : in  std_logic_vector(DATA_WIDTH-1 downto 0);
i_push_ch_write : in  std_logic; 

o_push_ch_write : out VSIG_TYPE(CH_NUM-1 downto 0); 
o_push_ch_data : out VDATA_TYPE(CH_NUM-1 downto 0));
end component;

--**
--* Component s2p_fifoin
--**
component s2p_fiforead
generic(DATA_WIDTH    : integer := 16;
        CH_NUM    : integer := 128);
port(clk, rst : in std_logic;

i_pop_ch_read  : in std_logic;

o_pop_ch_read  : out VSIG_TYPE(CH_NUM-1 downto 0));
end component;

--**
--* Component p2s_fifoout
--**
component p2s_fifoout
generic(DATA_WIDTH    : integer := 16;
        CH_NUM    : integer := 128);
port(clk, rst : in std_logic;
i_pop_ch_read     : in std_logic;
i_pop_ch_data  : in VDATA_TYPE(CH_NUM-1 downto 0);
o_pop_ch_data  : out std_logic_vector(DATA_WIDTH-1 downto 0));
end component;


--**
--* Component spu_core
--**
component spu_core
generic(
  DATA_WIDTH           : integer:= 16;  -- Data element width, e.g. real (and image) data width
  DATA_TYPE            : integer:= 1;
  SLICE_NUM            : integer:= 1;
  CORE_DATA_WIDTH      : integer:= 16; -- CPU data width, e.g. real (or real+image) width
  OPM_NUM              : integer:= 1;
  ALUM_NUM             : integer:= 1;
  FRAC_BITS            : integer:= 0;
  BSLAVE               : boolean:= false;
  BMASTER              : boolean:= false;
  BMASTER_NUM          : integer:= 1;
  VLEN                 : integer:= 1;

  OPCODE_WIDTH         : integer:= 6;
  
  -- Control Pipeline
  MULREG_EN            : boolean:= true;
  PB0_DEPTH            : integer:= 1;
  PB1_DEPTH            : integer:= 1;
  PB2_DEPTH            : integer:= 2;
  PA0_DEPTH            : integer:= 1;
  PA1_DEPTH            : integer:= 1;
  PA1X_DEPTH           : integer:= 0;
  
  -- Control Branch
  BRANCH_EN            : boolean:= false;
  JMP_EN               : boolean:= true;  
  
  RPT_EN               : boolean:= false;
  RPT_SPEC_1           : boolean:= false;
  RPT_LEVELS           : integer:= 4;
  RPT_CNT_LEN0         : integer:= 5;
  RPT_CNT_LEN1         : integer:= 5;
  RPT_CNT_LEN2         : integer:= 5;
  RPT_CNT_LEN3         : integer:= 5;
  RPT_CNT_LEN4         : integer:= 1;
  RPT_BLK_LEN0         : integer:= 5;
  RPT_BLK_LEN1         : integer:= 5;
  RPT_BLK_LEN2         : integer:= 5;
  RPT_BLK_LEN3         : integer:= 5;
  RPT_BLK_LEN4         : integer:= 1;
  
  -- Control Supported Instructions
  MASK_EN              : boolean:= false;
  MASKEQ_EN            : boolean:= false;
  MASKGT_EN            : boolean:= false;
  MASKLT_EN            : boolean:= false;
  MASKGE_EN            : boolean:= false;
  MASKLE_EN            : boolean:= false;
  MASKNE_EN            : boolean:= false;
  ALUSRA_EN            : boolean:= false;
  ALUSRA_VAL           : integer:= 1;
  ABSDIFF_EN           : boolean:= false;
  ABSDIFF_WITHACCUM    : boolean:= true;
  DECONST_EN			  : boolean:= true;
  DEBUG_EN				  : boolean:= true;
  
  -- Control Flexible Ports
  FLEXA_TYPE           : integer:= 1;
  FLEXB_TYPE           : integer:= 1;
  FLEXC_TYPE           : integer:= 1;  
  
  -- Special Case
  FLEXB_IMM_VAL        : integer:= -1;
  DIRECT_WB_EN         : boolean:= false;
  SHARE_GET_DATA       : boolean:= false;
  
  -- Control Extensible Bits
  EBITS_A              : integer:= 0;
  EBITS_B              : integer:= 0;
  EBITS_C              : integer:= 0;
  EBITS_D              : integer:= 0;
  
  DSP48E_EN            : boolean:= true;
  
  -- Control FIFO
  GETI_EN              : boolean:= false;
  GETCH_EN             : boolean:= false;
  PUTCH_EN             : boolean:= false;
  RX_CH_NUM            : integer:= 4;
  RX_CH_WIDTH          : integer:= 2;
  TX_CH_NUM            : integer:= 4;
  TX_CH_WIDTH          : integer:= 2;
  DTX_CH_NUM            : integer:= 1;
  DTX_CH_WIDTH          : integer:= 1;
  
  -- Control memory
  RF_EN                : boolean:= true;
  RF_ADDR_WIDTH        : integer:= 5;
  RF_INIT_EN           : boolean:= false;
  RF_INIT_FILE         : string := "RFInit/rf_initFPE0PE.mif";
  
  PM_SIZE              : integer:= 32;
  PM_ADDR_WIDTH        : integer:= 5;
  PM_DATA_WIDTH        : integer:= 32;
  USE_BRAM_FOR_LARGE_PM: boolean:= true;
  PM_INIT_FILE         : string := "PMInit/pm_init0.mif";
  
  DM_EN                : boolean:= false;
  DM_SIZE              : integer:= 32;
  DM_ADDR_WIDTH        : integer:= 5;
  DM_DATA_WIDTH        : integer:= 16;
  DM_INIT_EN           : boolean:= false;
  USE_BRAM_FOR_LARGE_DM: boolean:= true;
  DM_INIT_FILE         : string := "DMInit/dm_initFPE0PE";
  DM_RB_M_NUM          : integer:= 2;
  DM_RB_N_NUM          : integer:= 2;
  DM_WB_NUM            : integer:= 2;
  DM_TRUE_2R1W         : boolean:= true;
  DM_RB_M_INITIAL0     : integer:= 0;
  DM_RB_M_INITIAL1     : integer:= 0;
  DM_RB_N_INITIAL0     : integer:= 0;
  DM_RB_N_INITIAL1     : integer:= 0;
  DM_WB_INITIAL0       : integer:= 0;  
  DM_WB_INITIAL1       : integer:= 0;  
  DM_RB_M_AUTOINC_SIZE0: integer:= 1;
  DM_RB_M_AUTOINC_SIZE1: integer:= 1;
  DM_RB_N_AUTOINC_SIZE0: integer:= 1;
  DM_RB_N_AUTOINC_SIZE1: integer:= 1;
  DM_WB_AUTOINC_SIZE0  : integer:= 1;
  DM_WB_AUTOINC_SIZE1  : integer:= 1;
  DM_OFFSET_EN         : boolean:= false;
  DM_RB_M_SET_EN0      : boolean:= false;
  DM_RB_M_SET_EN1      : boolean:= false;
  DM_RB_N_SET_EN0      : boolean:= false;
  DM_RB_N_SET_EN1      : boolean:= false;
  DM_WB_SET_EN0        : boolean:= false;
  DM_WB_SET_EN1        : boolean:= false;
  DM_RB_M_AUTOINC_EN0  : boolean:= false; 
  DM_RB_M_AUTOINC_EN1  : boolean:= false;
  DM_RB_N_AUTOINC_EN0  : boolean:= false;
  DM_RB_N_AUTOINC_EN1  : boolean:= false;
  DM_WB_AUTOINC_EN0    : boolean:= false;
  DM_WB_AUTOINC_EN1    : boolean:= false;
  DM_RB_M_INC_EN0      : boolean:= false;
  DM_RB_M_INC_EN1      : boolean:= false;
  DM_RB_N_INC_EN0      : boolean:= false;
  DM_RB_N_INC_EN1      : boolean:= false;
  DM_WB_INC_EN0        : boolean:= false;
  DM_WB_INC_EN1        : boolean:= false;
  
  SM_EN                : boolean:= false;
  SM_SIZE              : integer:= 32;
  SM_ADDR_WIDTH        : integer:= 5;
  USE_BRAM_FOR_LARGE_SM: boolean:= true;
  SM_INIT_FILE         : string := "IMMInit/imm_init0.mif";
  SM_OFFSET_EN         : boolean:= false;
  SM_READONLY          : boolean:= true;
  SM_RB_SET_EN0        : boolean:= false;
  SM_WB_SET_EN0        : boolean:= false;
  SM_RB_AUTOINC_SIZE0  : integer:= 1;
  SM_WB_AUTOINC_SIZE0  : integer:= 1;
  SM_RB_AUTOINC_EN0    : boolean:= false;
  SM_WB_AUTOINC_EN0    : boolean:= false;
  SM_RB_INC_EN0        : boolean:= false;
  SM_WB_INC_EN0        : boolean:= false
);
port(
  clk     : in std_logic;
  rst     : in std_logic;

  -- Control
  i_ext_en_spu   : in  std_logic  := '1';
  o_ext_barrier  : out std_logic_vector(BMASTER_NUM-1 downto 0);
  i_ext_barrier  : in  std_logic := '0';
  o_ext_en_spu   : out std_logic := '1';
  o_put_last     : out std_logic := '0';
  
  -- Communication port signals
  i_get_ch_data  :  in VDATA_TYPE(RX_CH_NUM*VLEN-1 downto 0);
  i_get_ch_empty :  in VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0) := (others=>'0');  -- vector channel empty
  o_get_ch_read  :  out VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0);    -- vector channel read
  -- Output channel
  o_put_ch_data  :  out VDATA_TYPE(TX_CH_NUM*VLEN-1 downto 0);
  i_put_ch_full  :  in VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0):= (others=>'0');
  o_put_ch_write  : out VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0);  
  -- Debug communication port signals
  o_dput_ch_data  :  out VDATA_TYPE(DTX_CH_NUM*VLEN-1 downto 0);
  i_dput_ch_full  :  in VSIG_TYPE(DTX_CH_NUM*VLEN-1 downto 0):= (others=>'0');
  o_dput_ch_write  : out VSIG_TYPE(DTX_CH_NUM*VLEN-1 downto 0)
);
end component;

component iocore is
generic (
  INNERWIDTH : integer :=  8;
  
  RPT_EN       : boolean := true;
  RPT_SPEC_1   : boolean := false;
  RPT_LEVELS   : integer := 3;
  RPT_CNT_LEN0 : integer := 6;
  RPT_CNT_LEN1 : integer := 5;
  RPT_CNT_LEN2 : integer := 2;
  RPT_CNT_LEN3 : integer := 1;
  RPT_CNT_LEN4 : integer := 1;
  RPT_BLK_LEN0 : integer := 5;
  RPT_BLK_LEN1 : integer := 5;
  RPT_BLK_LEN2 : integer := 5;
  RPT_BLK_LEN3 : integer := 1;
  RPT_BLK_LEN4 : integer := 1;

  -- Control FIFO
  GETCH_EN    : boolean := true;
  PUTCH_EN    : boolean := true;
  RX_CH_NUM   : integer := 8;
  RX_CH_WIDTH : integer := 3;
  TX_CH_NUM   : integer := 8;
  TX_CH_WIDTH : integer := 3;
  RX_2LEV_EN  : boolean := false;
  RX_CH_WIDTH0: integer := 2;
  RX_CH_WIDTH1: integer := 2;  
  TX_2LEV_EN  : boolean := false;
  TX_CH_WIDTH0: integer := 2;
  TX_CH_WIDTH1: integer := 2;
  TX_MC_EN    : boolean := false;
  
  -- Control memory
  DQ_WIDTH            : integer:= 64;
  MASK_WIDTH          : integer:= 8;
  BURST_LEN           : integer:= 2;
  EM_RB_NUM           : integer:= 2;
  EM_RB_INITIAL0      : integer:= 10000;
  EM_RB_INITIAL1      : integer:= 20000;
  EM_WB_INITIAL0      : integer:= 30000;
  EM_RB_AUTOINC_SIZE0 : integer:= 16;
  EM_RB_AUTOINC_SIZE1 : integer:= 16;
  EM_WB_AUTOINC_SIZE0 : integer:= 16;
  EM_RB_AUTOINC_EN0   : boolean:= true;    
  EM_RB_AUTOINC_EN1   : boolean:= true;
  EM_WB_AUTOINC_EN0   : boolean:= true;
  EM_RB_INC_EN0       : boolean:= true;
  EM_RB_INC_EN1       : boolean:= true;
  EM_WB_INC_EN0       : boolean:= true;
  
  PM_SIZE      : integer := 64;
  PM_ADDR_WIDTH: integer := 6;
  PM_DATA_WIDTH: integer := 32;
  USE_BRAM_FOR_LARGE_PM: boolean := false;
  PM_INIT_FILE: string := "PMInit/iocore.mif"
);
port (
  clk     : in std_logic;
  rst     : in std_logic;

  -- Control
  o_ext_en_spu  : out std_logic;
  i_ext_barrier : in  std_logic := '0';

  -- Memory Interface
  o_mif_af_cmd   :  out std_logic_vector(2 downto 0);
  o_mif_af_addr  :  out std_logic_vector(30 downto 0);
  o_mif_af_wren  :  out std_logic;
  i_mif_af_afull :  in  std_logic;

  o_mif_wdf_wren :  out std_logic;
  o_mif_wdf_data :  out std_logic_vector(2*DQ_WIDTH-1 downto 0);
  o_mif_wdf_mask_data: out std_logic_vector(2*MASK_WIDTH-1 downto 0);
  i_mif_wdf_afull:  in  std_logic;

  i_mif_rd_data  :  in  std_logic_vector(2*DQ_WIDTH-1 downto 0);
  i_mif_rd_valid :  in  std_logic;

  -- Communication port signals
  i_get_ch_data  :  in VDATA_TYPE(RX_CH_NUM-1 downto 0);
  i_get_ch_empty :  in VSIG_TYPE(RX_CH_NUM-1 downto 0) := (others=>'0');  -- vector channel empty
  o_get_ch_read  :  out VSIG_TYPE(RX_CH_NUM-1 downto 0);    -- vector channel read
  -- Output channel
  o_put_ch_data  :  out VDATA_TYPE(TX_CH_NUM-1 downto 0);
  i_put_ch_almostfull :   in VSIG_TYPE(TX_CH_NUM-1 downto 0) := (others=>'0');
  o_put_ch_write :  out VSIG_TYPE(TX_CH_NUM-1 downto 0)
);
end component;

component iocore_id is
generic(
  PM_ADDR_WIDTH  : integer  := 6;
  JMP_EN         : boolean := true;
  RPT_EN         : boolean := true;
  GETCH_EN       : boolean := false;
  PUTCH_EN       : boolean := false
);
port(
  i_pm_do        : in std_logic_vector(31 downto 0);

  -- Control signals
  i_mif_rd_valid     : in  std_logic := '1';
  o_en_pc            : out std_logic;
  o_ext_en_spu       : out std_logic;
  i_ext_barrier      : in  std_logic := '0'; -- from external master spu
  
  -- component signals
  o_id_get           : out std_logic;
  o_id_put           : out std_logic;
  o_id_rx_autoinc    : out std_logic;
  o_id_rx_reset      : out std_logic;
  o_id_tx_autoinc    : out std_logic;
  o_id_tx_reset      : out std_logic;
  o_id_txbroadcast   : out std_logic;
  o_id_txmcs   : out std_logic;
  o_id_txmcc   : out std_logic;
  o_id_em_shiftcacheline: out std_logic;
  o_id_em_ldexmem    : out std_logic;
  o_id_em_ldcache    : out std_logic;
  o_id_em_stexmem    : out std_logic;
  o_id_em_stcache    : out std_logic;
  o_id_em_inc_rb_0   : out std_logic;
  o_id_em_inc_rb_1   : out std_logic;
  o_id_em_autoinc_rb : out std_logic;
  o_id_em_inc_wb_0   : out std_logic;
  o_id_em_autoinc_wb : out std_logic
);
end component;

--**
--* Component spu_pc
--**
component spu_pc
    generic (
    OPCODE_WIDTH  : integer := 6;
    PM_ADDR_WIDTH : integer := 11;
    PM_DATA_WIDTH : integer := 32;
    BRANCH_EN     : boolean := false;
    JMP_EN        : boolean := false;
    RPT_EN        : boolean := false;
    RPT_SPEC_1    : boolean := false;
    RPT_LEVELS    : integer := 4;
    RPT_CNT_LEN0  : integer := 5;
    RPT_CNT_LEN1  : integer := 5;
    RPT_CNT_LEN2  : integer := 4;
    RPT_CNT_LEN3  : integer := 4;
    RPT_CNT_LEN4  : integer := 4;
    RPT_BLK_LEN0  : integer := 5;
    RPT_BLK_LEN1  : integer := 3;
    RPT_BLK_LEN2  : integer := 3;
    RPT_BLK_LEN3  : integer := 2;
    RPT_BLK_LEN4  : integer := 3
  );
  port (
    clk           :  in std_logic;
    rst           :  in std_logic;
    i_en          :  in std_logic := '1';
    
    i_inst_data   :  in std_logic_vector(PM_DATA_WIDTH-OPCODE_WIDTH-1 downto 0);
    i_brc_taken   :  in std_logic;
    i_brc_addr    :  in std_logic_vector(PM_ADDR_WIDTH-1 downto 0);
  
    i_rpt_taken   :  in std_logic;
    
    i_jmp_taken   :  in std_logic;
    i_jmp_addr    :  in std_logic_vector(PM_ADDR_WIDTH-1 downto 0);
    o_pc          :  out std_logic_vector(PM_ADDR_WIDTH-1 downto 0)
  );
end component;

--**
--* Component spu_pm
--**               
component spu_pm
  generic (
    PM_SIZE        : integer := 100;
    PM_ADDR_WIDTH  : integer := 7;
    PM_DATA_WIDTH  : integer := 32;
    USE_BRAM_FOR_LARGE_PM   : boolean := false;
    PM_INIT_FILE: string := "PMInit/pm_init0.mif";
    PB0_DEPTH   : integer  := 1;
    PB1_DEPTH   : integer  := 1
  );
  port (
    clk    :  in std_logic;
    rst    :  in std_logic;
    i_en   :  in std_logic := '1';
    
    i_addr  :  in std_logic_vector (PM_ADDR_WIDTH-1 downto 0);
    o_pm  :  out std_logic_vector (PM_DATA_WIDTH-1 downto 0)
  );
end component;

--**
--* Component spu_id
--**                          
component spu_id is
generic(
  DATA_WIDTH       : integer:= 16;
  DATA_TYPE        : integer:= 1;
  SLICE_NUM        : integer:= 1;
  RF_ADDR_WIDTH    : integer:= 5;
  OPCODE_WIDTH     : integer:= 6;
  PM_ADDR_WIDTH    : integer:= 6;
  OPM_NUM          : integer:= 1;
  ALUM_NUM         : integer:= 1;
  FLEXA_TYPE       : integer:= 1;
  FLEXB_TYPE       : integer:= 1;
  FLEXC_TYPE       : integer:= 1;  
  BSLAVE           : boolean:= false;
  BMASTER          : boolean:= false;
  BMASTER_NUM     : integer:= 1;
  BRANCH_EN        : boolean:= false;
  JMP_EN           : boolean:= false;
  RPT_EN           : boolean:= false;
  RF_EN            : boolean:= false;
  DM_EN            : boolean:= false;
  DM_TWO_RD_PORTS  : boolean:= false;
  SM_EN            : boolean:= false;
  GETCH_EN         : boolean:= false;
  PUTCH_EN         : boolean:= false;
  MASKEQ_EN        : boolean:= false;
  MASKGT_EN        : boolean:= false;
  MASKLT_EN        : boolean:= false;
  MASKGE_EN        : boolean:= false;
  MASKLE_EN        : boolean:= false;
  MASKNE_EN        : boolean:= false;
  ALUSRA_EN        : boolean:= false;
  ABSDIFF_EN       : boolean:= false;
  ABSDIFF_WITHACCUM: boolean:= false;
  DEBUG_EN			 : boolean:= false
);
port(
  clk                   : in std_logic;
  i_pm_do               : in std_logic_vector(31 downto 0);
  o_id_opmode           : out std_logic_vector(7*OPM_NUM-1 downto 0);
  o_id_alumode          : out std_logic_vector(4*ALUM_NUM-1 downto 0);
  -- Control signals
  i_ext_barrier         : in  std_logic:= '0'; -- from external master spu
  o_en_pc               : out std_logic;
  o_ext_en_spu          : out std_logic;
  o_ext_id_barrier      : out std_logic_vector(BMASTER_NUM-1 downto 0);
  i_ext_en_spu          : in  std_logic:= '1'; -- from external slave spu
  o_put_last     : out std_logic := '0';
  
  -- component signals
  o_id_get_or_peak0: out std_logic:= '0';
  o_id_get_or_peak1: out std_logic:= '0';
  o_id_get0        : out std_logic:= '0';
  o_id_get1        : out std_logic:= '0';
  o_id_fifowrite        : out std_logic:= '0';
  o_id_rx_autoinc       : out std_logic:= '0';
  o_id_rx_reset         : out std_logic:= '0';
  o_id_tx_autoinc       : out std_logic:= '0';
  o_id_tx_reset         : out std_logic:= '0';
                                       
  o_id_rddm0            : out std_logic:= '0';
  o_id_rddm1            : out std_logic:= '0';
  o_id_wrdm             : out std_logic:= '0';
  o_id_dm_set_rb_m0     : out std_logic:= '0';
  o_id_dm_set_rb_m1     : out std_logic:= '0';
  o_id_dm_set_rb_n0     : out std_logic:= '0';
  o_id_dm_set_rb_n1     : out std_logic:= '0';
  o_id_dm_inc_rb_m0     : out std_logic:= '0';
  o_id_dm_inc_rb_m1     : out std_logic:= '0';
  o_id_dm_inc_rb_n0     : out std_logic:= '0';
  o_id_dm_inc_rb_n1     : out std_logic:= '0';
  o_id_dm_autoinc_rb_m  : out std_logic:= '0';
  o_id_dm_autoinc_rb_n  : out std_logic:= '0';
  o_id_dm_set_wb_0      : out std_logic:= '0';
  o_id_dm_set_wb_1      : out std_logic:= '0';
  o_id_dm_inc_wb_0      : out std_logic:= '0';
  o_id_dm_inc_wb_1      : out std_logic:= '0';
  o_id_dm_autoinc_wb    : out std_logic:= '0';
                                      
  o_id_sm_set_rb_0      : out std_logic:= '0';
  o_id_sm_inc_rb_0      : out std_logic:= '0';
  o_id_sm_set_wb_0      : out std_logic:= '0';
  o_id_sm_inc_wb_0      : out std_logic:= '0';
  o_id_sm_autoinc_rb    : out std_logic:= '0';
  o_id_sm_autoinc_wb    : out std_logic:= '0';
  o_id_sm_wen           : out std_logic:= '0';
  o_id_rdsm             : out std_logic:= '0';
                                      
  o_id_rf_wen           : out std_logic:= '0';
  
  o_id_b                : out std_logic:= '0';
  o_id_rpt              : out std_logic:= '0';
  o_id_beq              : out std_logic:= '0';
  o_id_bgt              : out std_logic:= '0';
  o_id_blt              : out std_logic:= '0';
  o_id_bge              : out std_logic:= '0';
  o_id_ble              : out std_logic:= '0';
  o_id_bne              : out std_logic:= '0';
                                       
  o_id_setmaskeq        : out std_logic:= '0';
  o_id_setmaskgt        : out std_logic:= '0';
  o_id_setmasklt        : out std_logic:= '0';
  o_id_setmaskge        : out std_logic:= '0';
  o_id_setmaskle        : out std_logic:= '0';
  o_id_setmaskne        : out std_logic:= '0';
                                       
  o_id_alusra           : out std_logic:= '0';
  o_id_CA_absdiff       : out std_logic:= '0';
  o_id_CA_absdiff_clr   : out std_logic:= '0';
  o_id_deconst       	: out std_logic:= '0';
  o_id_debug       		: out std_logic:= '0';
  o_id_tx_dautoinc       : out std_logic:= '0';
  o_id_tx_dreset         : out std_logic:= '0'
);
end component;                   
                                          
--**
--* Component spu_sm
--**
component spu_sm
generic(
  SM_OFFSET_WIDTH     : integer  := 5;
  SM_SIZE             : integer  := 32;
  SM_ADDR_WIDTH       : integer  := 5;
  SM_DATA_WIDTH       : integer  := 16;
  USE_BRAM_FOR_LARGE_SM : boolean := true;
  SM_INIT_FILE        : string   := "IMMInit/imm_init0.mif";
  PA0_DEPTH           : integer  := 1;
  PA1_DEPTH           : integer  := 1;
  
  SM_OFFSET_EN        : boolean  := false;
  
  SM_READONLY         : boolean  := true;
  SM_RB_SET_EN0       : boolean  := false;
  SM_WB_SET_EN0       : boolean  := false;
  
  SM_RB_AUTOINC_SIZE0 : integer  := 1;
  SM_WB_AUTOINC_SIZE0 : integer  := 1;
  
  SM_RB_AUTOINC_EN0   : boolean  := true;
  SM_WB_AUTOINC_EN0   : boolean  := true;
  
  SM_RB_INC_EN0       : boolean  := true;
  SM_WB_INC_EN0       : boolean  := true
);
port(
  clk      : in std_logic;
  rst      : in std_logic;

  i_sm_rd_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
  i_sm_wr_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
  i_sm_set_rb_0    : in std_logic;
  i_sm_set_wb_0    : in std_logic;
  i_sm_inc_rb_0    : in std_logic;
  i_sm_inc_wb_0    : in std_logic;
  i_sm_autoinc_rb  : in std_logic;
  i_sm_autoinc_wb  : in std_logic;

  i_sm_wen         : in std_logic;
  i_sm_rd_ofs      : in std_logic_vector(SM_OFFSET_WIDTH-1 downto 0);
  i_sm_din         : in std_logic_vector(SM_DATA_WIDTH-1 downto 0);
  o_sm_dout        : out std_logic_vector (SM_DATA_WIDTH-1 downto 0)
);
end component;

component spu_sau is
  generic (
    DM_OFFSET_WIDTH      : integer:= 5;
    DM_ADDR_WIDTH        : integer:= 10;
    DM_DATA_WIDTH        : integer:= 16;
    DM_WB_NUM            : integer:= 1;
    DM_RB_M_NUM          : integer:= 1;
    DM_RB_N_NUM          : integer:= 1;
    
    -- The initial value of base
    DM_RB_M_INITIAL0      : integer:= 0;
    DM_RB_M_INITIAL1      : integer:= 0;
    DM_RB_N_INITIAL0      : integer:= 0;
    DM_RB_N_INITIAL1      : integer:= 0;
    DM_WB_INITIAL0        : integer:= 0;
    DM_WB_INITIAL1        : integer:= 0;
    
    DM_RB_M_AUTOINC_SIZE0 : integer:= 1;
    DM_RB_M_AUTOINC_SIZE1 : integer:= 1;
    DM_RB_N_AUTOINC_SIZE0 : integer:= 1;
    DM_RB_N_AUTOINC_SIZE1 : integer:= 1;
    DM_WB_AUTOINC_SIZE0   : integer:= 1;
    DM_WB_AUTOINC_SIZE1   : integer:= 1;
    
    DM_OFFSET_EN          : boolean:= false;
    DM_RB_M_SET_EN0       : boolean:= false;
    DM_RB_M_SET_EN1       : boolean:= false;
    DM_RB_N_SET_EN0       : boolean:= false;
    DM_RB_N_SET_EN1       : boolean:= false;
    DM_WB_SET_EN0         : boolean:= false;
    DM_WB_SET_EN1         : boolean:= false;
    DM_RB_M_AUTOINC_EN0   : boolean:= false;    
    DM_RB_M_AUTOINC_EN1   : boolean:= false;
    DM_RB_N_AUTOINC_EN0   : boolean:= false;
    DM_RB_N_AUTOINC_EN1   : boolean:= false;
    DM_WB_AUTOINC_EN0     : boolean:= false;
    DM_WB_AUTOINC_EN1     : boolean:= false;
    DM_RB_M_INC_EN0       : boolean:= false;
    DM_RB_M_INC_EN1       : boolean:= false;
    DM_RB_N_INC_EN0       : boolean:= false;
    DM_RB_N_INC_EN1       : boolean:= false;
    DM_WB_INC_EN0         : boolean:= false;
    DM_WB_INC_EN1         : boolean:= false
  );
  port (
    clk    :  in std_logic;
    
    i_dm_rd_ofs_m     :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0);
    i_dm_rd_ofs_n     :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0);
    i_dm_rd_bs        :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    i_dm_set_rb_m0    :  in std_logic;
    i_dm_set_rb_m1    :  in std_logic;
    i_dm_set_rb_n0    :  in std_logic;
    i_dm_set_rb_n1    :  in std_logic;
    i_dm_inc_rb_m0    :  in std_logic;
    i_dm_inc_rb_m1    :  in std_logic;
    i_dm_inc_rb_n0    :  in std_logic;
    i_dm_inc_rb_n1    :  in std_logic;
    i_dm_autoinc_rb_m :  in std_logic;
    i_dm_autoinc_rb_n :  in std_logic;
    i_dm_rb_sel_m     :  in std_logic;
    i_dm_rb_sel_n     :  in std_logic;
    
    i_dm_wr_ofs       :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0);
    i_dm_wr_bs        :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    i_dm_set_wb_0      :  in std_logic;
    i_dm_set_wb_1      :  in std_logic;
    i_dm_inc_wb_0      :  in std_logic;
    i_dm_inc_wb_1      :  in std_logic;
    i_dm_autoinc_wb   :  in std_logic;
    i_dm_wb_sel       :  in std_logic;
    
    o_dm_rd_addr_0    :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    o_dm_rd_addr_1    :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    o_dm_wr_addr      :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0)
  );
end component;

--**
--* Component spu_dm
--**            
component spu_dm
  generic (
    DM_OFFSET_WIDTH      : integer:= 5;
    DM_SIZE              : integer:= 64;
    DM_ADDR_WIDTH        : integer:= 6;
    DM_DATA_WIDTH        : integer:= 16;
    DM_INIT_EN           : boolean:= false;
    USE_BRAM_FOR_LARGE_DM: boolean:= true;
    DM_INIT_FILE         : string := "mem.dat";
    DM_TWO_RD_PORTS      : boolean:= false;
    DM_TRUE_2R1W         : boolean:= false;
    
    PA0_DEPTH            : integer:= 1;
    PA1_DEPTH            : integer:= 1
  );
  port (
    clk                  :  in std_logic;
    rst                  :  in std_logic;
    
    i_dm_rd_addr_0       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);    
    i_dm_rd_addr_1       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);    
    i_dm_wr_addr         :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);

    i_dm_wen             :  in std_logic;
    i_dm_din             :  in std_logic_vector (DM_DATA_WIDTH-1 downto 0);
    
    o_dm_dout0           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0);
    o_dm_dout1           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0)
  );

end component;   

--**
--* Component spu_rf
--**            
component spu_rf
  generic (
    RF_ADDR_WIDTH  : integer := 5;
    RF_DATA_WIDTH  : integer := 16;
    FRAC_BITS      : integer := 8;
    RF_INIT_EN   : boolean := false;
    RF_INIT_FILE : string := "RFInit/rf_init0.mif";
    PA0_DEPTH  : integer  := 1;
    PA1_DEPTH  : integer  := 1
  );
  port (
    clk: in std_logic;
    rst: in std_logic;
    
    i_rdaddr_a : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_rdaddr_b : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_rdaddr_c : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    o_rddata_a : out std_logic_vector (RF_DATA_WIDTH-1 downto 0);
    o_rddata_b : out std_logic_vector (RF_DATA_WIDTH-1 downto 0) ;
    o_rddata_c : out std_logic_vector (RF_DATA_WIDTH-1 downto 0);

    i_wraddr_d : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_wrdata_d : in std_logic_vector (RF_DATA_WIDTH-1 downto 0);
    i_wen     : in std_logic
  );
end component;                         
                                  
--**
--* Component spu_ex
--**                      
component spu_ex
generic(
  DATA_WIDTH : integer := 32; -- Real or Imag width
  CORE_DATA_WIDTH : integer := 32; -- Real + Imag width
  DATA_TYPE  : integer := 1;
  SLICE_NUM  : integer := 4;
  OPM_NUM    : integer   := 1;
  ALUM_NUM   : integer   := 1;
  MULREG_EN  : boolean  := false;
  FRAC_BITS  : integer := 0;
  MASK_EN    : boolean := false;
  ALUSRA_VAL : integer := 1;
  BRANCH_EN  : boolean := false
);
port (
  clk, rst   : in  std_logic;
  i_opmode   : in  std_logic_vector(7*OPM_NUM-1 downto 0);
  i_alumode  : in  std_logic_vector(4*ALUM_NUM-1 downto 0);
  i_src_a    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_src_b    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_src_c    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  o_sign : out std_logic;
  o_zero : out std_logic;
  o_dsp48_result: out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  o_dsp48sra_result: out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)
);
end component;

--**
--* Component spu_brdetc
--**
component spu_brdetc
  generic (
  PC_ADDR_WIDTH : integer :=  6;
  BRANCH_EN     : boolean  := false;
  JMP_EN        : boolean  := false
  );
  port (
    i_id_beq    :   in std_logic;
    i_id_bgt    :   in std_logic;
    i_id_blt    :   in std_logic;
		i_id_bge		:   in std_logic;
		i_id_ble		:   in std_logic;
		i_id_bne		:   in std_logic;

    i_ex_zero   :   in std_logic;
    i_ex_sign   :   in std_logic;    
    o_branch_taken  :   out std_logic;
    
    i_id_b      :  in std_logic;
    o_jmp_taken :   out std_logic
  );
end component;

  --**
  --* Component spu_commget
  --**
  component spu_commget_en is
  generic(
    DATA_WIDTH    : integer:= 16;
    OUT_DATA_WIDTH: integer:= 16; -- for asymmetric width
    
    RX_CH_WIDTH   : integer:= 1;
    RX_CH_NUM     : integer:= 1;
    GETCH_EN      : boolean:= false;
    
    -- Enable FIFO status signals (empty, full)
    STATE_EN      : boolean:= false
  );
  port(
    clk, rst       : in std_logic;
    i_ext_en_spu   : in  std_logic;
    i_get_ch_select: in std_logic_vector(RX_CH_WIDTH-1 downto 0) := (others=>'0');
    
    -- input channel
    i_get_ch_data  : in VDATA_TYPE(RX_CH_NUM-1 downto 0);
    i_get_ch_empty : in VSIG_TYPE(RX_CH_NUM-1 downto 0);
    i_get_inst     : in std_logic; --Get instruction, use as a read signal
    i_rx_autoinc   : in std_logic:= '0';
    i_rx_reset     : in std_logic := '0';
                   
    o_get_data     : out std_logic_vector(OUT_DATA_WIDTH-1 downto 0); -- to processor core
    o_get_ch_empty : out std_logic;  --to processor core
    o_get_ch_read  : out VSIG_TYPE(RX_CH_NUM-1 downto 0) -- to processor core
  );
  end component;
  
  component spu_commput_en is
  generic(
    DATA_WIDTH     : integer:= 16;
    
    TX_CH_WIDTH    : integer:= 1;
    TX_CH_NUM      : integer:= 2;
    PUTCH_EN       : boolean:= false;
    
    -- Enable FIFO status signals (empty, full)
    STATE_EN       : boolean:= false
  );
  port(
    clk, rst       : in std_logic;
    i_ext_en_spu   : in  std_logic;
    i_put_ch_select: in std_logic_vector(TX_CH_WIDTH-1 downto 0);
  
    i_tx_autoinc   : in std_logic:= '0';
    i_tx_reset     : in std_logic := '0';
    
    -- output channel
    i_put_data     : in std_logic_vector(DATA_WIDTH-1 downto 0); -- From processor core
    i_put_ch_full  : in VSIG_TYPE(TX_CH_NUM-1 downto 0);
    i_put_inst     : in std_logic;  -- PUT instruction, used as write enable signal
    
    o_put_ch_data  : out VDATA_TYPE(TX_CH_NUM-1 downto 0); -- to fifo
    o_put_ch_full  : out std_logic;-- To processor core
    o_put_ch_write : out VSIG_TYPE(TX_CH_NUM-1 downto 0)
  );
  end component;

--**
--* Component spu_commget
--**
component spu_commget is
generic(
  DATA_WIDTH    : integer:= 16;
  OUT_DATA_WIDTH: integer:= 16; -- for asymmetric width
  
  RX_CH_WIDTH   : integer:= 1;
  RX_CH_NUM     : integer:= 1;
  GETCH_EN      : boolean:= false;
  
  -- Enable FIFO status signals (empty, full)
  STATE_EN      : boolean:= false
);
port(
  clk, rst       : in std_logic;
  i_get_ch_select: in std_logic_vector(RX_CH_WIDTH-1 downto 0) := (others=>'0');
  
  -- input channel
  i_get_ch_data  : in VDATA_TYPE(RX_CH_NUM-1 downto 0);
  i_get_ch_empty : in VSIG_TYPE(RX_CH_NUM-1 downto 0);
  i_get_inst     : in std_logic; --Get instruction, use as a read signal
  i_rx_autoinc   : in std_logic:= '0';
  i_rx_reset     : in std_logic := '0';
                 
  o_get_data     : out std_logic_vector(OUT_DATA_WIDTH-1 downto 0); -- to processor core
  o_get_ch_empty : out std_logic;  --to processor core
  o_get_ch_read  : out VSIG_TYPE(RX_CH_NUM-1 downto 0) -- to processor core
);
end component;

component spu_commput is
generic(
  DATA_WIDTH     : integer:= 16;
  
  TX_CH_WIDTH    : integer:= 1;
  TX_CH_NUM      : integer:= 2;
  PUTCH_EN       : boolean:= false;
  
  -- Enable FIFO status signals (empty, full)
  STATE_EN       : boolean:= false
);
port(
  clk, rst       : in std_logic;
  i_put_ch_select: in std_logic_vector(TX_CH_WIDTH-1 downto 0);

  i_tx_autoinc   : in std_logic:= '0';
  i_tx_reset     : in std_logic := '0';
  
  -- output channel
  i_put_data     : in std_logic_vector(DATA_WIDTH-1 downto 0); -- From processor core
  i_put_ch_full  : in VSIG_TYPE(TX_CH_NUM-1 downto 0);
  i_put_inst     : in std_logic;  -- PUT instruction, used as write enable signal
  
  o_put_ch_data  : out VDATA_TYPE(TX_CH_NUM-1 downto 0); -- to fifo
  o_put_ch_full  : out std_logic;-- To processor core
  o_put_ch_write : out VSIG_TYPE(TX_CH_NUM-1 downto 0)
);
end component;

component spu_writeback is
generic(
  CORE_DATA_WIDTH : integer := 32;
  ABSDIFF_EN : boolean := true;
  ALUSRA_EN  : boolean := true;
  DECONST_EN  : boolean := true
);
port(
  i_dsp48_result: in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_dsp48sra_result: in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  i_alusra : in std_logic;  
  i_CA_absdiff : in std_logic;
  i_CA_absdiff_d : in std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  i_CA_deconst : in std_logic;   
  i_deconst_out : in std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  o_result  : out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)
);
end component;

--**
--* Component iocore_commport
--**
component iocore_commport is
generic(
  INNERWIDTH  : integer := 16;
  
  RX_CH_WIDTH : integer := 4;
  RX_CH_NUM   : integer := 16;
  
  TX_CH_WIDTH : integer := 4;
  TX_CH_NUM   : integer := 16;
  
  -- Enable FIFO status signals (empty, full)
  STATE_EN    : boolean := false;
  
  -- Indexed channel access
  GETCH_EN   : boolean := false;
  PUTCH_EN   : boolean := false;
  
  -- Multiple level support
  RX_2LEV_EN  : boolean := true;
  RX_CH_WIDTH0: integer := 2;
  RX_CH_WIDTH1: integer := 2;
  
  TX_2LEV_EN  : boolean := true;
  TX_CH_WIDTH0: integer := 2;
  TX_CH_WIDTH1: integer := 2;
  
  TX_MC_EN    : boolean := false;
  
  PA1_DEPTH   : integer  := 1;
  PA1X_DEPTH  : integer  := 0
);
port(
  clk, rst    : in std_logic;
  i_get_ch_select  : in std_logic_vector(RX_CH_WIDTH-1 downto 0);
  i_put_ch_select  : in std_logic_vector(TX_CH_WIDTH-1 downto 0);
  
  -- input channel
  i_get_ch_data  : in VDATA_TYPE(RX_CH_NUM-1 downto 0);
  i_get_ch_empty  : in VSIG_TYPE(RX_CH_NUM-1 downto 0);
  i_get_inst  : in std_logic; --Get instruction, use as a read signal

  o_get_data  : out std_logic_vector(INNERWIDTH-1 downto 0); -- to processor core
  o_get_ch_empty  : out std_logic;  --to processor core
  o_get_ch_read  : out VSIG_TYPE(RX_CH_NUM-1 downto 0); -- to processor core

  i_rx_reset   : in std_logic := '0';
  i_rx_autoinc : in std_logic := '0';
  
  -- output channel
  i_put_data  : in std_logic_vector(INNERWIDTH-1 downto 0); -- From processor core
  i_put_ch_full  : in VSIG_TYPE(TX_CH_NUM-1 downto 0);
  i_put_inst  : in std_logic;  -- PUT instruction, used as write enable signal
  i_put_broadcast : in std_logic := '0';
  i_tx_mcs : in std_logic := '0';
  i_tx_mcc : in std_logic := '0';
  
  o_put_ch_data  : out VDATA_TYPE(TX_CH_NUM-1 downto 0); -- to fifo
  o_put_ch_full  : out std_logic;-- To processor core
  o_put_ch_write  : out VSIG_TYPE(TX_CH_NUM-1 downto 0);
  
  i_tx_reset   : in std_logic := '0';
  i_tx_autoinc : in std_logic := '0'
);
end component;

component iocore_exm is
generic(
  DATA_WIDTH  : integer  := 16;
  DQ_WIDTH    : integer  := 64;
  MASK_WIDTH  : integer  := 8;
  BURST_LEN   : integer  := 2;
  
  EM_RB_NUM      : integer:= 2;  
  EM_RB_INITIAL0 : integer:= 10000;
  EM_RB_INITIAL1 : integer:= 20000;
  EM_WB_INITIAL0 : integer:= 30000;
  
  EM_RB_AUTOINC_SIZE0 : integer:= 16;
  EM_RB_AUTOINC_SIZE1 : integer:= 16;
  EM_WB_AUTOINC_SIZE0 : integer:= 16;
  
  EM_RB_AUTOINC_EN0   : boolean:= true;    
  EM_RB_AUTOINC_EN1   : boolean:= true;
  EM_WB_AUTOINC_EN0   : boolean:= true;
  
  EM_RB_INC_EN0       : boolean:= true;
  EM_RB_INC_EN1       : boolean:= true;
  EM_WB_INC_EN0       : boolean:= true
);
port(
  clk            : in  std_logic;
  
  i_em_rd_bs       :  in std_logic_vector (30 downto 0);
  i_em_wr_bs       :  in std_logic_vector (30 downto 0);
  i_em_inc_rb_0    :  in std_logic;
  i_em_inc_rb_1    :  in std_logic;
  i_em_inc_wb_0    :  in std_logic;
  i_em_autoinc_rb  :  in std_logic;
  i_em_rb_sel      :  in std_logic;
  i_em_autoinc_wb  :  in std_logic;
    
  o_mif_af_cmd   : out std_logic_vector(2 downto 0);
  o_mif_af_addr  : out std_logic_vector(30 downto 0);
  o_mif_af_wren  : out std_logic := '0';
  i_mif_af_afull : in  std_logic;

  o_mif_wdf_wren : out std_logic;
  o_mif_wdf_data : out std_logic_vector(2*DQ_WIDTH-1 downto 0);
  o_mif_wdf_mask_data: out std_logic_vector(2*MASK_WIDTH-1 downto 0);
  i_mif_wdf_afull: in  std_logic;

  i_mif_rd_data  : in  std_logic_vector(2*DQ_WIDTH-1 downto 0);
  i_mif_rd_valid : in  std_logic;
  o_mif_rd_valid : out std_logic;
  
  i_shiftcacheline: in std_logic := '0';
  i_ldexmem      : in  std_logic;
  i_ldcache      : in  std_logic;
  o_core_data    : out std_logic_vector(DATA_WIDTH-1 downto 0);
  i_core_data    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
  i_stexmem      : in  std_logic;
  i_stcache      : in  std_logic
);
end component;

--**
--* Component fifo
--**
component fifo
  generic ( 
    WIDTH    : integer := 16;
    DEPTH    : integer := 8;
    STATE_EN : boolean := false);
  port( 
    clk          : in     std_logic;
    i_data       : in     std_logic_vector (WIDTH -1 downto 0);
    o_data       : out    std_logic_vector (WIDTH -1 downto 0);
    write        : in     std_logic;
    read         : in     std_logic;
    o_full       : out    std_logic;
    o_almostfull : out    std_logic;
    o_empty      : out    std_logic
  );
end component;

--**
--* Component spu_mux_2to1
--**                      
component spu_mux_2to1                   
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic;
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0)                 
  );                                   
end component;                            

--**
--* Component spu_mux3to1
--** 
component spu_mux_3to1 is                     
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(1 downto 0)
  );                                    
end component;

-- spu_mux_4to1
component spu_mux_4to1 is                     
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d3    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(2 downto 0)
  );                                    
end component;       

--**
--* Component spu_generic_reg
--**
component spu_generic_reg 
generic(REG_NUM  : integer := 2;
    REG_WIDTH : integer := 16);
port(
clk      : in std_logic;
rst      : in std_logic := '0';
i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0'));
end component;

component spu_generic_reg_with_en is
generic(
  REG_NUM  : integer := 2;
  REG_WIDTH : integer := 16
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_en     : in std_logic;
  i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
  o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
);
end component;

--**
--* Component spu_generic_reg1
--**
component spu_generic_reg1
generic(REG_NUM  : integer := 2);
port(
clk      : in std_logic;
rst      : in std_logic := '0';
i_d      : in std_logic;
o_d      : out std_logic := '0');
end component;

component spu_generic_reg1_with_en is
generic(
  REG_NUM  : integer := 2
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_en     : in std_logic;
  i_d      : in std_logic;
  o_d      : out std_logic := '0'
);
end component;
                 
component spu_shift_counter
generic (
  DEPTH_WIDTH : integer := 4
);
port(
  CLK  : in std_logic;
  DATA : in std_logic;
  CE   : in std_logic;
  A    : in std_logic_vector(DEPTH_WIDTH-1 downto 0);
  Q    : out std_logic
);
end component;

component spu_absdiffaccum is
generic (
  DATA_WIDTH : integer := 8;
  IN_DATA_WIDTH : integer := 8;
  ABSDIFF_WITHACCUM: boolean := true
);
port(
  clk  : in std_logic;
  i_d0 : in std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  i_d1 : in std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  i_en : in std_logic;
  i_clr : in std_logic;
  o_d  : out std_logic_vector(DATA_WIDTH-1 downto 0)
);
end component;

component ssp_deconst is
generic(WIDTH : integer := 16); -- set to how wide fifo is to be
port( 
    i_data    : in     std_logic_vector (WIDTH -1 downto 0);
    o_data		: out    std_logic_vector (WIDTH -1 downto 0);
    clk       : in     std_logic;
	 rst				: in	   std_logic);
end component ;

component conv_std_logic_vector_to_signed is
generic(WIDTH : integer := 16);
PORT( 
a : in std_logic_vector(WIDTH-1 downto 0); 
b : out signed(WIDTH-1 downto 0) 
); 
end component; 

component m_SQRD_ZF_22_wrap is
generic (
CORE_WIDTH : integer := 16;
INPUT_WIDTH : integer := 16;
OUTPUT_WIDTH : integer := 16;
EXIN_FIFO_NUM : integer := 1;
EXOUT_FIFO_NUM : integer := 3
);
port (
clk : in std_logic;
rst : in std_logic;
i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0)
);
end component;
end ssp_pkg;
--///////////////////////////////////////////////////////////////////
--////                         package body                      ////
package body ssp_pkg is

  function log_2 (x : positive) return natural is
  begin
  if x <= 1 then
    return 0;
  else
    return log_2 (x / 2) + 1;
  end if;
  end function log_2;
  
  function vectorize (s: std_logic) return std_logic_vector is
  variable v: std_logic_vector(0 downto 0);
  begin
    v(0) := s;
  return v;
  end; 
   
end package body ssp_pkg;

--///////////////////////////////////////////////////////////////////
--////                         Entities                          //// 
                                         
--**
--* Entity spu_mux2to1
--**                             
library ieee;                             
use ieee.std_logic_1164.ALL;              
library unisim;                           
use unisim.vcomponents.all;               
entity spu_mux_2to1 is                     
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic;
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0)                 
  );                                    
end spu_mux_2to1;                          
                                          
architecture structure of spu_mux_2to1 is  
begin                                     
  o_d <= i_d0 when (sel = '0') else  i_d1;
end structure;

--**
--* Entity spu_mux3to1
--**                             
library ieee;                             
use ieee.std_logic_1164.ALL;                        
entity spu_mux_3to1 is                     
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(1 downto 0)
  );                                    
end spu_mux_3to1;                          
                                          
architecture structure of spu_mux_3to1 is  
begin                                     
  process (i_d0, i_d1, i_d2, sel) begin
    case (sel) is
      when "00" => o_d <= i_d0;
      when "01" => o_d <= i_d1;
      when "10" => o_d <= i_d2;
      when others => o_d <= i_d0;
    end case;
  end process;
end structure;

-- Entity spu_mux4to1             
library ieee;                             
use ieee.std_logic_1164.ALL;                        
entity spu_mux_4to1 is                     
  generic (                               
    DATA_WIDTH:integer := 16
  );                                      
  port (                                
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d3    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(2 downto 0)
  );                                    
end spu_mux_4to1;                          
                                          
architecture structure of spu_mux_4to1 is  
begin                                     
  process (i_d0, i_d1, i_d2, i_d3, sel) begin
    case (sel) is
      when "000" => o_d <= i_d0;
      when "001" => o_d <= i_d1;
      when "010" => o_d <= i_d2;
      when "100" => o_d <= i_d3;
      when others => o_d <= i_d0;
    end case;
  end process;
end structure;

--**
--* Entity spu_generic_reg
--**
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity spu_generic_reg is
generic(
  REG_NUM  : integer := 2;
  REG_WIDTH : integer := 16
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
  o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
);
end spu_generic_reg;

architecture behav of spu_generic_reg is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        o_d <= i_d;
      end if;
    end process P1;      
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic_vector(REG_WIDTH - 1 downto 0);
    signal t_reg_in : type_in_reg := (others=>(others=>'0'));
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then      
        t_reg_in(REG_NUM - 1) <= i_d;
        t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
      end if;
    end process P1;  
  end generate GR2;  
end architecture;

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity spu_generic_reg_with_en is
generic(
  REG_NUM  : integer := 2;
  REG_WIDTH : integer := 16
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_en     : in std_logic;
  i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
  o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
);
end spu_generic_reg_with_en;

architecture behav of spu_generic_reg_with_en is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          o_d <= i_d;
        end if;
      end if;
    end process P1;      
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic_vector(REG_WIDTH - 1 downto 0);
    signal t_reg_in : type_in_reg := (others=>(others=>'0'));
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then        
          t_reg_in(REG_NUM - 1) <= i_d;
          t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
        end if;
      end if;
    end process P1;  
  end generate GR2;  
end architecture;


--**
--* Entity spu_generic_reg1
--**
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity spu_generic_reg1 is
generic(
  REG_NUM  : integer := 2
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_d      : in std_logic;
  o_d      : out std_logic := '0'
);
end spu_generic_reg1;

architecture behav of spu_generic_reg1 is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        o_d <= i_d;
      end if;
    end process P1;
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic;
    signal t_reg_in : type_in_reg := (others=>'0');
  begin
    o_d <= t_reg_in(0);
    
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        t_reg_in(REG_NUM - 1) <= i_d;
        t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
      end if;         
    end process P1;
  end generate GR2;  
end architecture;

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity spu_generic_reg1_with_en is
generic(
  REG_NUM  : integer := 2
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_en     : in std_logic;
  i_d      : in std_logic;
  o_d      : out std_logic := '0'
);
end spu_generic_reg1_with_en;

architecture behav of spu_generic_reg1_with_en is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          o_d <= i_d;
        end if;
      end if;
    end process P1;
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic;
    signal t_reg_in : type_in_reg := (others=>'0');
  begin
    o_d <= t_reg_in(0);
    
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          t_reg_in(REG_NUM - 1) <= i_d;
          t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
        end if;
      end if;         
    end process P1;
  end generate GR2;  
end architecture;

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
entity spu_shift_counter is
generic (
  DEPTH_WIDTH : integer := 4
);
port(
  CLK  : in std_logic;
  DATA : in std_logic;
  CE   : in std_logic;
  A    : in std_logic_vector(DEPTH_WIDTH-1 downto 0);
  Q    : out std_logic
);

  attribute shreg_extract : string;
  attribute shreg_extract of spu_shift_counter : entity is "yes";
  
end spu_shift_counter;

architecture rtl of spu_shift_counter is
  constant DEPTH : integer := 2**DEPTH_WIDTH;
  type SRL_ARRAY is array (0 to DEPTH-1) of std_logic;
  signal SRL_SIG : SRL_ARRAY := (others=>'0');
begin
  PROC_SRL : process (CLK)
  begin
    if (CLK'event and CLK = '1') then
      if (CE = '1') then
        SRL_SIG <= DATA & SRL_SIG(0 to DEPTH-2);
      end if;
    end if;
  end process;
  Q <= SRL_SIG(conv_integer(A));
end rtl;

library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.ssp_pkg.all;

entity spu_absdiffaccum is
generic (
  DATA_WIDTH : integer := 8;
  IN_DATA_WIDTH : integer := 8;
  ABSDIFF_WITHACCUM: boolean := true
);
port(
  clk  : in std_logic;
  i_d0 : in std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  i_d1 : in std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  i_en : in std_logic;
  i_clr : in std_logic;
  o_d  : out std_logic_vector(DATA_WIDTH-1 downto 0)
);
end spu_absdiffaccum;

architecture rtl of spu_absdiffaccum is
  signal en : std_logic := '0';
  signal clr : std_logic := '0';
  signal d0 : std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  signal d1 : std_logic_vector(IN_DATA_WIDTH-1 downto 0);
  signal absdiff_wire, absdiff_reg : signed(IN_DATA_WIDTH-1 downto 0);
  signal accum : signed(DATA_WIDTH-1 downto 0) := (others=>'0');
begin
  u_d0_reg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>IN_DATA_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>i_d0, o_d=>d0);
  u_d1_reg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>IN_DATA_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>i_d1, o_d=>d1);
  
  en <= i_en;
  clr <= i_clr;
  
  absdiff_wire <= signed(d0)-signed(d1);
  
  ACCUM_GEN: if ABSDIFF_WITHACCUM = true generate
    process (clk)
    begin
      if (clk'event and clk = '1') then
        absdiff_reg <= absdiff_wire;
        if (clr = '1') then
          accum <= (others=>'0');
        elsif en = '1' then
          accum <= accum + abs(absdiff_reg);
        end if;
      end if;
    end process;
    o_d <= std_logic_vector(accum);  
  end generate;
  
  NOACCUM_GEN: if ABSDIFF_WITHACCUM = false generate
    process (clk)
    begin
      if (clk'event and clk = '1') then
        absdiff_reg <= absdiff_wire;
      end if;
    end process;
    o_d <= std_logic_vector(absdiff_reg);  
  end generate;
end rtl;


library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_arith.all; 

entity conv_std_logic_vector_to_signed is
generic(WIDTH : integer := 16);
PORT( 
a : in std_logic_vector(WIDTH-1 downto 0); 
b : out signed(WIDTH-1 downto 0) 
); 
end conv_std_logic_vector_to_signed; 

architecture struct of conv_std_logic_vector_to_signed is 
begin 
label1: for i in 0 to b'LENGTH-1 generate 
b(i) <= a(i); 
end generate label1; 
END struct;