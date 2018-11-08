library ieee;
use ieee.std_logic_1164.all;

library work;
use work.m_word_pkg.all;
use work.m_word_config.all;

entity ssp_top is
generic (
  DQ_WIDTH            : integer:= 64;
  MASK_WIDTH          : integer:= 8
);
  port (
    clk : in std_logic;
    rst : in std_logic;
    o_mif_af_cmd   :  out std_logic_vector(2 downto 0);
    o_mif_af_addr  :  out std_logic_vector(30 downto 0);
    o_mif_af_wren  :  out std_logic;
    i_mif_af_afull :  in  std_logic;
    o_mif_wdf_wren :  out std_logic;
    o_mif_wdf_data :  out std_logic_vector(2*DQ_WIDTH-1 downto 0);
    o_mif_wdf_mask_data: out std_logic_vector(2*MASK_WIDTH-1 downto 0);
    i_mif_wdf_afull:  in  std_logic;
    i_mif_rd_data  :  in  std_logic_vector(2*DQ_WIDTH-1 downto 0);
    i_mif_rd_valid :  in  std_logic
  );
end ssp_top;

architecture Structure of ssp_top is

  -- Connection signals
  signal m2s_data   : VDATA_TYPE(31 downto 0);
  signal m2s_write  : VSIG_TYPE(31 downto 0);
  signal m2s_en_spu : std_logic;
  signal s2m_data   : VDATA_TYPE(0 downto 0);
  signal s2m_read   : VSIG_TYPE(0 downto 0);
  signal s2m_barrier: std_logic;
begin

  -- Connect IOCore with SPUs
u_iocore: m_word_iocore
generic map(
  IO_WIDTH        => 16,

  -- Control Pipeline
  PB0_DEPTH  => 0,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,

  -- Control Branch
  JMP_EN        => true,

  RPT_EN       => false,
  RPT_USESRL   => false,
  RPT_SPEC_1   => false,
  RPT_LEVELS   => 0,
  RPT_CNT_LEN0 => 1,
  RPT_CNT_LEN1 => 1,
  RPT_CNT_LEN2 => 1,
  RPT_CNT_LEN3 => 1,
  RPT_CNT_LEN4 => 1,
  RPT_BLK_LEN0 => 1,
  RPT_BLK_LEN1 => 1,
  RPT_BLK_LEN2 => 1,
  RPT_BLK_LEN3 => 1,
  RPT_BLK_LEN4 => 1,

  -- Control FIFO
  PG_EN       => true,
  GETCH_EN    => true,
  PUTCH_EN    => true,
  RX_CH_NUM   => 1,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 32,
  TX_CH_WIDTH => 5,

  -- Control memory
  DQ_WIDTH            => 64,
  MASK_WIDTH          => 8,
  BURST_LEN           => 2,
  EM_RB_NUM           => 2,
  EM_RB_INITIAL0      => 10000,
  EM_RB_INITIAL1      => 20000,
  EM_WB_INITIAL0      => 30000,
  EM_RB_AUTOINC_SIZE0 => 16,
  EM_RB_AUTOINC_SIZE1 => 16,
  EM_WB_AUTOINC_SIZE0 => 16,
  EM_RB_AUTOINC_EN0   => true,
  EM_RB_AUTOINC_EN1   => true,
  EM_WB_AUTOINC_EN0   => true,
  EM_RB_INC_EN0       => true,
  EM_RB_INC_EN1       => true,
  EM_WB_INC_EN0       => true,

  PM_SIZE       => 0,
  PM_ADDR_WIDTH => -2147483648,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/iocore.mif"
)
port map(
  clk => clk,
  rst => rst,

  -- Control
  o_en_spu  => m2s_en_spu,
  i_barrier => s2m_barrier,

  -- Memory Interface
  o_mif_af_cmd   => o_mif_af_cmd,
  o_mif_af_addr  => o_mif_af_addr,
  o_mif_af_wren  => o_mif_af_wren,
  i_mif_af_afull => i_mif_af_afull,

  o_mif_wdf_wren => o_mif_wdf_wren,
  o_mif_wdf_data => o_mif_wdf_data,
  o_mif_wdf_mask_data => o_mif_wdf_mask_data,
  i_mif_wdf_afull=> i_mif_wdf_afull,
  i_mif_rd_data  => i_mif_rd_data,
  i_mif_rd_valid => i_mif_rd_valid,

  -- Communication port signals
  i_get_ch_data  => s2m_data,
  o_get_ch_read  => s2m_read,
  i_get_ch_empty => open,

  -- Output channel
  o_put_ch_data  => m2s_data,
  o_put_ch_write => m2s_write,
  i_put_ch_almostfull  => open
);

u_spus: m_fft_wrap
generic map(
  CORE_WIDTH     => 16,
  INPUT_WIDTH    : integer := 8;
  OUTPUT_WIDTH   : integer := 16;
  EXIN_FIFO_NUM  => 32,
  EXOUT_FIFO_NUM => 1
)
port map(
  clk => clk,
  rst => rst,

  -- Control
  i_en_spu  => m2s_en_spu,
  o_barrier => s2m_barrier,

  i_push_ch_data  => m2s_data,
  i_push_ch_write => m2s_write,
  o_push_ch_full  => open,

  o_pop_ch_data  => s2m_data,
  i_pop_ch_read => s2m_read,
  o_pop_ch_empty  => open
);
end Structure;
