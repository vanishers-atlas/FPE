library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library unisim;
use unisim.vcomponents.all;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity iocore is
generic (
  INNERWIDTH : integer :=  8;
  
  RPT_EN       : boolean := true;
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
end iocore;

architecture structure of iocore is

type VPMOPERANDS_TYPE is array (natural range <>) of std_logic_vector(PM_DATA_WIDTH-7 downto 0);
type VRXCHWIDTH_TYPE is array (natural range <>) of std_logic_vector(RX_CH_WIDTH-1 downto 0);
type VTXCHWIDTH_TYPE is array (natural range <>) of std_logic_vector(TX_CH_WIDTH-1 downto 0);

-- Constants
constant PB2_DEPTH   : integer := 1;
constant PA0_DEPTH   : integer := 1;
constant PA1_DEPTH   : integer := 1;

signal jmp_taken_Pb2 : std_logic;

signal id_b_Pb1, id_b_Pb2 : std_logic;

signal id_rpt_Pb1, id_rpt_Pb2 : std_logic;

signal get_data_Pa3, put_data_Pa3 : VDATA_TYPE(0 downto 0);
signal pc_addr_Ps  : std_logic_vector(PM_ADDR_WIDTH-1 downto 0);

signal pm_do_Pb1  : std_logic_vector(PM_DATA_WIDTH-1 downto 0);

signal pm_operands_Pb1, pm_operands_Pb2 : std_logic_vector(PM_DATA_WIDTH-7 downto 0);

signal branch_addr_Pb2 : std_logic_vector(PM_ADDR_WIDTH-1 downto 0);

signal id_en_pc_Pb1  : std_logic;
signal id_en_spu_Pb1, id_en_spu_Pb2 : std_logic;

signal id_get_inst_Pb1, id_get_inst_Pb2, id_get_inst_Pa0 : std_logic;
signal id_txbroadcast_Pb1, id_txbroadcast_Pb2, id_txbroadcast_Pa0, id_txbroadcast_Pa1, id_txbroadcast_Pa2 : std_logic;
signal id_txmcs_Pb1, id_txmcs_Pb2, id_txmcs_Pa0, id_txmcs_Pa1, id_txmcs_Pa2 : std_logic;
signal id_txmcc_Pb1, id_txmcc_Pb2, id_txmcc_Pa0, id_txmcc_Pa1, id_txmcc_Pa2 : std_logic;
signal id_put_inst_Pb1, id_put_inst_Pb2, id_put_inst_Pa0, id_put_inst_Pa1, id_put_inst_Pa2 : std_logic_vector(0 downto 0);

signal get_ch_sel_Pb2 : std_logic_vector(RX_CH_WIDTH-1 downto 0);
signal get_ch_sel_Pa0 : VRXCHWIDTH_TYPE(0 downto 0);

signal put_ch_sel_Pb2, put_ch_sel_Pa0, put_ch_sel_Pa1 : std_logic_vector(TX_CH_WIDTH-1 downto 0);
signal put_ch_sel_Pa2 : VTXCHWIDTH_TYPE(0 downto 0);

signal mif_rd_valid : std_logic;
signal em_rb_sel_Pb2 : std_logic;
signal em_rd_wr_bs_Pb2 : std_logic_vector(30 downto 0);

signal id_em_shiftcacheline_Pb1, id_em_shiftcacheline_Pb2 : std_logic;
signal id_em_ldexmem_Pb1, id_em_ldexmem_Pb2 : std_logic;
signal id_em_ldcache_Pb1, id_em_ldcache_Pb2, id_em_ldcache_Pa0, id_em_ldcache_Pa1, id_em_ldcache_Pa2 : std_logic;
signal id_em_stexmem_Pb1, id_em_stexmem_Pb2, id_em_stexmem_Pa0, id_em_stexmem_Pa1, id_em_stexmem_Pa2 : std_logic;
signal id_em_stcache_Pb1, id_em_stcache_Pb2, id_em_stcache_Pa0, id_em_stcache_Pa1, id_em_stcache_Pa2, id_em_stcache_Pa3 : std_logic;
signal id_em_inc_rb_0_Pb1, id_em_inc_rb_0_Pb2 : std_logic;
signal id_em_inc_rb_1_Pb1, id_em_inc_rb_1_Pb2 : std_logic;
signal id_em_autoinc_rb_Pb1, id_em_autoinc_rb_Pb2 : std_logic;
signal id_em_inc_wb_0_Pb1, id_em_inc_wb_0_Pb2, id_em_inc_wb_0_Pa0, id_em_inc_wb_0_Pa1, id_em_inc_wb_0_Pa2 : std_logic;
signal id_em_autoinc_wb_Pb1, id_em_autoinc_wb_Pb2, id_em_autoinc_wb_Pa0, id_em_autoinc_wb_Pa1, id_em_autoinc_wb_Pa2 : std_logic;

signal id_rx_reset_Pb1, id_rx_reset_Pb2, id_rx_reset_Pa0 : std_logic;
signal id_rx_autoinc_Pb1, id_rx_autoinc_Pb2, id_rx_autoinc_Pa0 : std_logic;

signal id_tx_reset_Pb1, id_tx_reset_Pb2, id_tx_reset_Pa0, id_tx_reset_Pa1, id_tx_reset_Pa2 : std_logic;
signal id_tx_autoinc_Pb1, id_tx_autoinc_Pb2, id_tx_autoinc_Pa0, id_tx_autoinc_Pa1, id_tx_autoinc_Pa2 : std_logic;

begin
-----------------------------------------------------------------------
-- INSTRUCTION FETCH STAGE
-----------------------------------------------------------------------
--pc
u_pc: m_word_pc
  generic map(
    PM_ADDR_WIDTH=> PM_ADDR_WIDTH,
    PM_DATA_WIDTH=> PM_DATA_WIDTH,
    BRANCH_EN    => false,
    JMP_EN       => true,
    RPT_EN       => RPT_EN,
    RPT_LEVELS   => RPT_LEVELS,
    RPT_CNT_LEN0 => RPT_CNT_LEN0,
    RPT_CNT_LEN1 => RPT_CNT_LEN1,
    RPT_CNT_LEN2 => RPT_CNT_LEN2,
    RPT_CNT_LEN3 => RPT_CNT_LEN3,
    RPT_CNT_LEN4 => RPT_CNT_LEN4,
    RPT_BLK_LEN0 => RPT_BLK_LEN0,
    RPT_BLK_LEN1 => RPT_BLK_LEN1,
    RPT_BLK_LEN2 => RPT_BLK_LEN2,
    RPT_BLK_LEN3 => RPT_BLK_LEN3,
    RPT_BLK_LEN4 => RPT_BLK_LEN4)
  port map(
    clk        =>  clk, 
    rst        =>  rst, 
    i_en       =>  id_en_pc_Pb1,
    
    i_inst_data =>  pm_operands_Pb2,
    i_brc_taken =>  '0',
    i_brc_addr  =>  std_logic_vector(to_unsigned(0, PM_ADDR_WIDTH)),
    i_rpt_taken =>  id_rpt_Pb2,
    i_jmp_taken =>  jmp_taken_Pb2,
    i_jmp_addr  =>  branch_addr_Pb2,
    o_pc        =>  pc_addr_Ps);
    
--pm
u_pm: m_word_pm 
  generic map(PM_SIZE        => PM_SIZE,
              PM_ADDR_WIDTH  => PM_ADDR_WIDTH,
              PM_DATA_WIDTH  => PM_DATA_WIDTH,
              USE_BRAM_FOR_LARGE_PM => USE_BRAM_FOR_LARGE_PM,
              PM_INIT_FILE => PM_INIT_FILE,
              PB0_DEPTH => 1, 
              PB1_DEPTH => 1)
  port map(
    clk=>clk, 
    rst => rst,
    i_en => id_en_pc_Pb1,
    i_addr=>pc_addr_Ps,
    o_pm => pm_do_Pb1);

--id
u_id: iocore_id
  generic map(
    PM_ADDR_WIDTH => PM_ADDR_WIDTH,
    JMP_EN        => true,
    RPT_EN        => RPT_EN,
    GETCH_EN      => GETCH_EN,
    PUTCH_EN      => PUTCH_EN
    )
  port map(
    i_pm_do     => pm_do_Pb1,
    
    i_mif_rd_valid  => mif_rd_valid,
    o_en_pc         => id_en_pc_Pb1,
    o_ext_en_spu    => id_en_spu_Pb1,
    i_ext_barrier   => i_ext_barrier,

    o_id_get        => id_get_inst_Pb1,  
    o_id_put        => id_put_inst_Pb1,
    o_id_rx_autoinc => id_rx_autoinc_Pb1,
    o_id_rx_reset   => id_rx_reset_Pb1,
    o_id_tx_autoinc => id_tx_autoinc_Pb1,
    o_id_tx_reset   => id_tx_reset_Pb1,
    o_id_txbroadcast   => id_txbroadcast_Pb1,
    o_id_txmcs   => id_txmcs_Pb1,
    o_id_txmcc   => id_txmcc_Pb1,
    o_id_em_shiftcacheline => id_em_shiftcacheline_Pb1,
    o_id_em_ldexmem    => id_em_ldexmem_Pb1,
    o_id_em_ldcache    => id_em_ldcache_Pb1,
    o_id_em_stexmem    => id_em_stexmem_Pb1,
    o_id_em_stcache    => id_em_stcache_Pb1,
    o_id_em_inc_rb_0   => id_em_inc_rb_0_Pb1,
    o_id_em_inc_rb_1   => id_em_inc_rb_1_Pb1,
    o_id_em_autoinc_rb => id_em_autoinc_rb_Pb1,
    o_id_em_inc_wb_0   => id_em_inc_wb_0_Pb1,
    o_id_em_autoinc_wb => id_em_autoinc_wb_Pb1
  );

  u_exmem: m_word_exmem
  generic map(
    DATA_WIDTH         => INNERWIDTH,
    DQ_WIDTH           => 64,
    MASK_WIDTH         => MASK_WIDTH,
    BURST_LEN          => BURST_LEN,
    EM_RB_NUM          => EM_RB_NUM,
    EM_RB_INITIAL0     => EM_RB_INITIAL0,     
    EM_RB_INITIAL1     => EM_RB_INITIAL1,     
    EM_WB_INITIAL0     => EM_WB_INITIAL0,     
    EM_RB_AUTOINC_SIZE0=> EM_RB_AUTOINC_SIZE0,
    EM_RB_AUTOINC_SIZE1=> EM_RB_AUTOINC_SIZE1,
    EM_WB_AUTOINC_SIZE0=> EM_WB_AUTOINC_SIZE0,
    EM_RB_AUTOINC_EN0  => EM_RB_AUTOINC_EN0,  
    EM_RB_AUTOINC_EN1  => EM_RB_AUTOINC_EN1,  
    EM_WB_AUTOINC_EN0  => EM_WB_AUTOINC_EN0,  
    EM_RB_INC_EN0      => EM_RB_INC_EN0,      
    EM_RB_INC_EN1      => EM_RB_INC_EN1,      
    EM_WB_INC_EN0      => EM_WB_INC_EN0            
  )
  port map(
    clk                => clk,
    i_em_rd_bs         => em_rd_wr_bs_Pb2,
    i_em_wr_bs         => em_rd_wr_bs_Pb2,
    i_em_inc_rb_0      => id_em_inc_rb_0_Pb2,
    i_em_inc_rb_1      => id_em_inc_rb_1_Pb2,
    i_em_inc_wb_0      => id_em_inc_wb_0_Pa2,
    i_em_autoinc_rb    => id_em_autoinc_rb_Pb2,
    i_em_rb_sel        => em_rb_sel_Pb2,
    i_em_autoinc_wb    => id_em_autoinc_wb_Pa2,    
    o_mif_af_cmd       => o_mif_af_cmd,
    o_mif_af_addr      => o_mif_af_addr,
    o_mif_af_wren      => o_mif_af_wren,
    i_mif_af_afull     => i_mif_af_afull,
    o_mif_wdf_wren     => o_mif_wdf_wren,
    o_mif_wdf_data     => o_mif_wdf_data,
    o_mif_wdf_mask_data=> o_mif_wdf_mask_data,
    i_mif_wdf_afull    => i_mif_wdf_afull,
    i_mif_rd_data      => i_mif_rd_data,
    i_mif_rd_valid     => i_mif_rd_valid,
    o_mif_rd_valid     => mif_rd_valid,
    i_ldexmem          => id_em_ldexmem_Pb2,
    i_shiftcacheline   => id_em_shiftcacheline_Pb2,
    i_ldcache          => id_em_ldcache_Pa2,
    -- ldexmem is at Pb2, but ldcache is at Pa2. The reason is
    -- command is registered twice rather than data.
    o_core_data        => put_data_Pa3(0)(INNERWIDTH-1 downto 0),
    i_core_data        => get_data_Pa3(0)(INNERWIDTH-1 downto 0),
    i_stexmem          => id_em_stexmem_Pa2,
    i_stcache          => id_em_stcache_Pa3
    -- here stexmem is at Pa2, but stcache is at Pa3. The reason is
    -- real stexmem operation is a cycle after id_stexmem.
  );

-- 20 bits are used for em_inc
em_rd_wr_bs_Pb2 <= (30 downto 20=>pm_operands_Pb2(19)) & pm_operands_Pb2(19 downto 0);
em_rb_sel_Pb2 <= pm_operands_Pb2(0);

pm_operands_Pb1 <= pm_do_Pb1(PM_DATA_WIDTH-7 downto 0);

branch_addr_Pb2<= pm_operands_Pb2(PM_ADDR_WIDTH-1 downto 0);
get_ch_sel_Pb2 <= pm_operands_Pb2(RX_CH_WIDTH-1 downto 0);

tx_mc_off: if TX_MC_EN = false generate
  put_ch_sel_Pb2 <= pm_operands_Pb2(TX_CH_WIDTH-1 downto 0);
end generate;

o_ext_en_spu <= id_en_spu_Pb2;
-----------------------------------------------------------------------
-- PIPELINE STAGE
-----------------------------------------------------------------------
u_buf_pm_operands_Pb2:m_word_generic_reg generic map(REG_NUM=>PB2_DEPTH, REG_WIDTH=>PM_DATA_WIDTH-6) 
port map(clk=>clk, rst=>'0', i_d=>pm_operands_Pb1, o_d=>pm_operands_Pb2);

-- ID pipeline
u_buf_id_get_inst_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_get_inst_Pb1, o_d=>id_get_inst_Pb2);

u_buf_id_en_spu_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_en_spu_Pb1, o_d=>id_en_spu_Pb2);
  
u_buf_id_put_inst_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_put_inst_Pb1, o_d=>id_put_inst_Pb2);  

u_buf_id_b_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_b_Pb1, o_d=>id_b_Pb2);

u_buf_id_rpt_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_rpt_Pb1, o_d=>id_rpt_Pb2);

u_buf_id_em_ldexmem_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_ldexmem_Pb1, o_d=>id_em_ldexmem_Pb2);
  
u_buf_id_em_shiftcacheline_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_shiftcacheline_Pb1, o_d=>id_em_shiftcacheline_Pb2);

u_buf_id_em_stexmem_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stexmem_Pb1, o_d=>id_em_stexmem_Pb2);
u_buf_id_em_stexmem_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stexmem_Pb2, o_d=>id_em_stexmem_Pa0);
u_buf_id_em_stexmem_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stexmem_Pa0, o_d=>id_em_stexmem_Pa1);
u_buf_id_em_stexmem_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stexmem_Pa1, o_d=>id_em_stexmem_Pa2); 
  
u_buf_id_em_ldcache_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_ldcache_Pb1, o_d=>id_em_ldcache_Pb2);
u_buf_id_em_ldcache_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_ldcache_Pb2, o_d=>id_em_ldcache_Pa0);
u_buf_id_em_ldcache_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_ldcache_Pa0, o_d=>id_em_ldcache_Pa1);
u_buf_id_em_ldcache_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_ldcache_Pa1, o_d=>id_em_ldcache_Pa2);
  
u_buf_id_em_stcache_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stcache_Pb1, o_d=>id_em_stcache_Pb2);
u_buf_id_em_stcache_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stcache_Pb2, o_d=>id_em_stcache_Pa0);
u_buf_id_em_stcache_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stcache_Pa0, o_d=>id_em_stcache_Pa1);
u_buf_id_em_stcache_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stcache_Pa1, o_d=>id_em_stcache_Pa2);
u_buf_id_em_stcache_Pa3:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_stcache_Pa2, o_d=>id_em_stcache_Pa3);

u_buf_id_em_inc_rb_0_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_rb_0_Pb1, o_d=>id_em_inc_rb_0_Pb2);  
  
u_buf_id_em_inc_rb_1_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_rb_1_Pb1, o_d=>id_em_inc_rb_1_Pb2);  
  
u_buf_id_em_inc_wb_0_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_wb_0_Pb1, o_d=>id_em_inc_wb_0_Pb2);
u_buf_id_em_inc_wb_0_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_wb_0_Pb2, o_d=>id_em_inc_wb_0_Pa0);
u_buf_id_em_inc_wb_0_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_wb_0_Pa0, o_d=>id_em_inc_wb_0_Pa1);
u_buf_id_em_inc_wb_0_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_inc_wb_0_Pa1, o_d=>id_em_inc_wb_0_Pa2);
  
u_buf_id_em_autoinc_rb_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_autoinc_rb_Pb1, o_d=>id_em_autoinc_rb_Pb2);  
  
u_buf_id_em_autoinc_wb_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_autoinc_wb_Pb1, o_d=>id_em_autoinc_wb_Pb2);
u_buf_id_em_autoinc_wb_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_autoinc_wb_Pb2, o_d=>id_em_autoinc_wb_Pa0);
u_buf_id_em_autoinc_wb_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_autoinc_wb_Pa0, o_d=>id_em_autoinc_wb_Pa1);
u_buf_id_em_autoinc_wb_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_em_autoinc_wb_Pa1, o_d=>id_em_autoinc_wb_Pa2);

-- get
u_buf_id_get_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_get_inst_Pb2, o_d=>id_get_inst_Pa0);

u_buf_id_rx_reset_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_rx_reset_Pb1, o_d=>id_rx_reset_Pb2);
u_buf_id_rx_reset_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_rx_reset_Pb2, o_d=>id_rx_reset_Pa0);

u_buf_id_rx_autoinc_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_rx_autoinc_Pb1, o_d=>id_rx_autoinc_Pb2);
u_buf_id_rx_autoinc_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_rx_autoinc_Pb2, o_d=>id_rx_autoinc_Pa0);
  
-- put
u_buf_id_put_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_put_inst_Pb2, o_d=>id_put_inst_Pa0);
u_buf_id_put_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_put_inst_Pa0, o_d=>id_put_inst_Pa1);
put_buf_repl_gen:
for i in 0 to 0 generate  
  u_buf_id_put_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
    port map(clk=>clk, rst=>'0', i_d=>id_put_inst_Pa1, o_d=>id_put_inst_Pa2(i));
end generate;

u_buf_id_txbroadcast_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txbroadcast_Pb1, o_d=>id_txbroadcast_Pb2);  
u_buf_id_txbroadcast_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txbroadcast_Pb2, o_d=>id_txbroadcast_Pa0);
u_buf_id_txbroadcast_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txbroadcast_Pa0, o_d=>id_txbroadcast_Pa1);
u_buf_id_txbroadcast_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_txbroadcast_Pa1, o_d=>id_txbroadcast_Pa2);
  
u_buf_id_txmcs_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcs_Pb1, o_d=>id_txmcs_Pb2);  
u_buf_id_txmcs_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcs_Pb2, o_d=>id_txmcs_Pa0);
u_buf_id_txmcs_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcs_Pa0, o_d=>id_txmcs_Pa1);
u_buf_id_txmcs_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcs_Pa1, o_d=>id_txmcs_Pa2);
  
u_buf_id_txmcc_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcc_Pb1, o_d=>id_txmcc_Pb2);  
u_buf_id_txmcc_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcc_Pb2, o_d=>id_txmcc_Pa0);
u_buf_id_txmcc_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcc_Pa0, o_d=>id_txmcc_Pa1);
u_buf_id_txmcc_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_txmcc_Pa1, o_d=>id_txmcc_Pa2);
u_buf_id_tx_reset_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_reset_Pb1, o_d=>id_tx_reset_Pb2);
u_buf_id_tx_reset_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_reset_Pb2, o_d=>id_tx_reset_Pa0);
u_buf_id_tx_reset_Pa1:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_reset_Pa0, o_d=>id_tx_reset_Pa1);
u_buf_id_tx_reset_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_reset_Pa1, o_d=>id_tx_reset_Pa2);

u_buf_id_tx_autoinc_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_autoinc_Pb1, o_d=>id_tx_autoinc_Pb2);
u_buf_id_tx_autoinc_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_autoinc_Pb2, o_d=>id_tx_autoinc_Pa0);
u_buf_id_tx_autoinc_Pa1:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_autoinc_Pa0, o_d=>id_tx_autoinc_Pa1);
u_buf_id_tx_autoinc_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) 
  port map(clk=>clk, rst=>'0', i_d=>id_tx_autoinc_Pa1, o_d=>id_tx_autoinc_Pa2);

-- get_ch_sel_Pb2
get_ch_sel_buf_repl_gen: for i in 0 to 0 generate 
  u_get_ch_sel_Pa0:m_word_generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>RX_CH_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>get_ch_sel_Pb2, o_d=>get_ch_sel_Pa0(i));
end generate;

-- put_ch_sel_Pb2
u_put_ch_sel_reg_Pa0:m_word_generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>put_ch_sel_Pb2, o_d=>put_ch_sel_Pa0);
u_put_ch_sel_reg_Pa1:m_word_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>put_ch_sel_Pa0, o_d=>put_ch_sel_Pa1);
    
put_ch_sel_buf_repl_gen: for i in 0 to 0 generate 
  u_put_ch_sel_Pa1:m_word_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
  port map(clk=>clk, rst=>'0', i_d=>put_ch_sel_Pa1, o_d=>put_ch_sel_Pa2(i));
end generate;

----------------------------------------------------------------------
-- Branch control generation
-----------------------------------------------------------------------
u_branchdetect: m_word_brdetc 
generic map(PC_ADDR_WIDTH => PM_ADDR_WIDTH, BRANCH_EN => false, JMP_EN  => true)
port map(clk => clk, rst => rst, i_id_beq => '0',
         i_id_bgt => '0', i_id_blt => '0', i_id_b => id_b_Pb2,
         i_ex_zero => '0', i_ex_sign  => '0', o_jmp_taken=> jmp_taken_Pb2,
         o_branch_taken=> open);

-----------------------------------------------------------------------
-- Communication generation
-----------------------------------------------------------------------
-- Instantiate communication component
comm_gen: for i in 0 to 0 generate
  u_iocomm: m_word_iocore_commport generic map (
    INNERWIDTH  => INNERWIDTH,
    RX_CH_WIDTH => RX_CH_WIDTH,
    RX_CH_NUM   => RX_CH_NUM,
    TX_CH_WIDTH => TX_CH_WIDTH,
    TX_CH_NUM   => TX_CH_NUM,
    STATE_EN    => false,
    GETCH_EN    => GETCH_EN,
    PUTCH_EN    => PUTCH_EN,
    RX_2LEV_EN   => RX_2LEV_EN,  
    RX_CH_WIDTH0 => RX_CH_WIDTH0,
    RX_CH_WIDTH1 => RX_CH_WIDTH1,
    TX_2LEV_EN   => TX_2LEV_EN,
    TX_CH_WIDTH0 => TX_CH_WIDTH0,
    TX_CH_WIDTH1 => TX_CH_WIDTH1,
    TX_MC_EN     => TX_MC_EN,
    PA1_DEPTH   => PA1_DEPTH,
    PA1X_DEPTH  => 0)
    port map (
    clk    => clk,
    rst    => rst,
    
    i_get_ch_select  => get_ch_sel_Pa0(i),
    i_put_ch_select  => put_ch_sel_Pa2(i),
    
    -- input channel
    i_get_ch_data   => i_get_ch_data((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM),
    i_get_ch_empty  => i_get_ch_empty((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM),
    o_get_ch_read   => o_get_ch_read((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM), -- to processor core       
    i_get_inst      => id_get_inst_Pa0, --Get instruction, use as a read signal
    o_get_data      => get_data_Pa3(i)(INNERWIDTH-1 downto 0),
    o_get_ch_empty  => open,  --to processor core    
    i_rx_reset      => id_rx_reset_Pa0,
    i_rx_autoinc    => id_rx_autoinc_Pa0,
    -- output channel
    i_put_data     => put_data_Pa3(i)(INNERWIDTH-1 downto 0),
    i_put_ch_full  => open,
    i_put_inst     => id_put_inst_Pa2(i),  -- PUT instruction, used as write enable signal
    i_put_broadcast => id_txbroadcast_Pa2,
    i_tx_mcs => id_txmcs_Pa2,
    i_tx_mcc => id_txmcc_Pa2,
    o_put_ch_data  => o_put_ch_data((i+1)*TX_CH_NUM-1 downto i*TX_CH_NUM), -- to fifo
    o_put_ch_full  => open,-- To processor core
    o_put_ch_write => o_put_ch_write((i+1)*TX_CH_NUM-1 downto i*TX_CH_NUM),
    i_tx_reset      => id_tx_reset_Pa2,
    i_tx_autoinc    => id_tx_autoinc_Pa2
    );
end generate comm_gen;

end structure;