library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

Library UNISIM;
use UNISIM.vcomponents.all;

entity ssp_wrap is
generic (
      CORE_WIDTH     : integer := 32;
      INPUT_WIDTH    : integer := 32;
      OUTPUT_WIDTH   : integer := 32;
      EXIN_FIFO_NUM  : integer := 2;
      EXOUT_FIFO_NUM : integer := 1;
      IOFIFODEPTH    : integer := 8);
  port (
    clk : in std_logic;
    rst : in std_logic;

    i_en_spu        : in  std_logic;
    o_barrier       : out std_logic;

    i_push_ch_data  : in  VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    i_push_ch_write : in  VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    o_push_ch_full  : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);

    o_pop_ch_data   : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
    i_pop_ch_read   : in  VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
    o_pop_ch_empty  : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0));
end ssp_wrap;

architecture Structure of ssp_wrap is

 signal barrier     : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);

  signal ch_IOCore_to_SPU0PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_write : std_logic;
  signal ch_IOCore_to_SPU0PE0_full  : std_logic;
  signal ch_IOCore_to_SPU0PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_read  : std_logic;
  signal ch_IOCore_to_SPU0PE0_empty : std_logic;
  signal ch_IOCore_to_SPU0PE0_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE0_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE0_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE0_1_empty : std_logic;
  signal ch_SPU4PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU4PE0_to_IOCore_write : std_logic;
  signal ch_SPU4PE0_to_IOCore_full  : std_logic;
  signal ch_SPU4PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU4PE0_to_IOCore_read  : std_logic;
  signal ch_SPU4PE0_to_IOCore_empty : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_1_write : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_1_full  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_1_read  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_1_empty : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_SPU2PE0_write : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_full  : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_SPU2PE0_read  : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_empty : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_SPU2PE0_1_write : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_1_full  : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_SPU2PE0_1_read  : std_logic;
  signal ch_SPU1PE0_to_SPU2PE0_1_empty : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU2PE0_to_SPU3PE0_write : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_full  : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU2PE0_to_SPU3PE0_read  : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_empty : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU2PE0_to_SPU3PE0_1_write : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_1_full  : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU2PE0_to_SPU3PE0_1_read  : std_logic;
  signal ch_SPU2PE0_to_SPU3PE0_1_empty : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU3PE0_to_SPU4PE0_write : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_full  : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU3PE0_to_SPU4PE0_read  : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_empty : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU3PE0_to_SPU4PE0_1_write : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_1_full  : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU3PE0_to_SPU4PE0_1_read  : std_logic;
  signal ch_SPU3PE0_to_SPU4PE0_1_empty : std_logic;
  -- SPU signals
  signal get_ch_data_0  : VDATA_TYPE(1 downto 0);
  signal get_ch_read_0  : VSIG_TYPE(1 downto 0);
  signal get_ch_empty_0 : VSIG_TYPE(1 downto 0);
  signal put_ch_data_0  : VDATA_TYPE(1 downto 0);
  signal put_ch_write_0 : VSIG_TYPE(1 downto 0);
  signal put_ch_full_0  : VSIG_TYPE(1 downto 0);

  signal get_ch_data_1  : VDATA_TYPE(1 downto 0);
  signal get_ch_read_1  : VSIG_TYPE(1 downto 0);
  signal get_ch_empty_1 : VSIG_TYPE(1 downto 0);
  signal put_ch_data_1  : VDATA_TYPE(1 downto 0);
  signal put_ch_write_1 : VSIG_TYPE(1 downto 0);
  signal put_ch_full_1  : VSIG_TYPE(1 downto 0);

  signal get_ch_data_2  : VDATA_TYPE(1 downto 0);
  signal get_ch_read_2  : VSIG_TYPE(1 downto 0);
  signal get_ch_empty_2 : VSIG_TYPE(1 downto 0);
  signal put_ch_data_2  : VDATA_TYPE(1 downto 0);
  signal put_ch_write_2 : VSIG_TYPE(1 downto 0);
  signal put_ch_full_2  : VSIG_TYPE(1 downto 0);

  signal get_ch_data_3  : VDATA_TYPE(1 downto 0);
  signal get_ch_read_3  : VSIG_TYPE(1 downto 0);
  signal get_ch_empty_3 : VSIG_TYPE(1 downto 0);
  signal put_ch_data_3  : VDATA_TYPE(1 downto 0);
  signal put_ch_write_3 : VSIG_TYPE(1 downto 0);
  signal put_ch_full_3  : VSIG_TYPE(1 downto 0);

  signal get_ch_data_4  : VDATA_TYPE(1 downto 0);
  signal get_ch_read_4  : VSIG_TYPE(1 downto 0);
  signal get_ch_empty_4 : VSIG_TYPE(1 downto 0);
  signal put_ch_data_4  : VDATA_TYPE(0 downto 0);
  signal put_ch_write_4 : VSIG_TYPE(0 downto 0);
  signal put_ch_full_4  : VSIG_TYPE(0 downto 0);

begin

  -- Connect signals with module ports
  o_barrier <= barrier(0);

  ch_IOCore_to_SPU0PE0_a <= i_push_ch_data(0);
  ch_IOCore_to_SPU0PE0_write  <= i_push_ch_write(0);
  o_push_ch_full(0) <= ch_IOCore_to_SPU0PE0_full;

  ch_IOCore_to_SPU0PE0_1_a <= i_push_ch_data(1);
  ch_IOCore_to_SPU0PE0_1_write  <= i_push_ch_write(1);
  o_push_ch_full(1) <= ch_IOCore_to_SPU0PE0_1_full;

  ch_SPU4PE0_to_IOCore_read  <= i_pop_ch_read(0);
  o_pop_ch_data(0) <= ch_SPU4PE0_to_IOCore_b;
  o_pop_ch_empty(0) <= ch_SPU4PE0_to_IOCore_empty;

  -- Connect FIFOs with SPUs
  -- Connect FIFO IOCore_to_SPU0PE0 with PE
  get_ch_data_0(0) <= ch_IOCore_to_SPU0PE0_b;
  get_ch_empty_0(0) <= ch_IOCore_to_SPU0PE0_empty;
  ch_IOCore_to_SPU0PE0_read <= get_ch_read_0(0);

  -- Connect FIFO IOCore_to_SPU0PE0_1 with PE
  get_ch_data_0(1) <= ch_IOCore_to_SPU0PE0_1_b;
  get_ch_empty_0(1) <= ch_IOCore_to_SPU0PE0_1_empty;
  ch_IOCore_to_SPU0PE0_1_read <= get_ch_read_0(1);

  -- Connect FIFO SPU4PE0_to_IOCore with PE
  ch_SPU4PE0_to_IOCore_a <= put_ch_data_4(0);
  ch_SPU4PE0_to_IOCore_write <= put_ch_write_4(0);
  put_ch_full_4(0) <= ch_SPU4PE0_to_IOCore_full;

  -- Connect FIFO SPU0PE0_to_SPU1PE0 with PE
  ch_SPU0PE0_to_SPU1PE0_a <= put_ch_data_0(0);
  ch_SPU0PE0_to_SPU1PE0_write <= put_ch_write_0(0);
  put_ch_full_0(0) <= ch_SPU0PE0_to_SPU1PE0_full;

  get_ch_data_1(0) <= ch_SPU0PE0_to_SPU1PE0_b;
  get_ch_empty_1(0) <= ch_SPU0PE0_to_SPU1PE0_empty;
  ch_SPU0PE0_to_SPU1PE0_read <= get_ch_read_1(0);

  -- Connect FIFO SPU0PE0_to_SPU1PE0_1 with PE
  ch_SPU0PE0_to_SPU1PE0_1_a <= put_ch_data_0(1);
  ch_SPU0PE0_to_SPU1PE0_1_write <= put_ch_write_0(1);
  put_ch_full_0(1) <= ch_SPU0PE0_to_SPU1PE0_1_full;

  get_ch_data_1(1) <= ch_SPU0PE0_to_SPU1PE0_1_b;
  get_ch_empty_1(1) <= ch_SPU0PE0_to_SPU1PE0_1_empty;
  ch_SPU0PE0_to_SPU1PE0_1_read <= get_ch_read_1(1);

  -- Connect FIFO SPU1PE0_to_SPU2PE0 with PE
  ch_SPU1PE0_to_SPU2PE0_a <= put_ch_data_1(0);
  ch_SPU1PE0_to_SPU2PE0_write <= put_ch_write_1(0);
  put_ch_full_1(0) <= ch_SPU1PE0_to_SPU2PE0_full;

  get_ch_data_2(0) <= ch_SPU1PE0_to_SPU2PE0_b;
  get_ch_empty_2(0) <= ch_SPU1PE0_to_SPU2PE0_empty;
  ch_SPU1PE0_to_SPU2PE0_read <= get_ch_read_2(0);

  -- Connect FIFO SPU1PE0_to_SPU2PE0_1 with PE
  ch_SPU1PE0_to_SPU2PE0_1_a <= put_ch_data_1(1);
  ch_SPU1PE0_to_SPU2PE0_1_write <= put_ch_write_1(1);
  put_ch_full_1(1) <= ch_SPU1PE0_to_SPU2PE0_1_full;

  get_ch_data_2(1) <= ch_SPU1PE0_to_SPU2PE0_1_b;
  get_ch_empty_2(1) <= ch_SPU1PE0_to_SPU2PE0_1_empty;
  ch_SPU1PE0_to_SPU2PE0_1_read <= get_ch_read_2(1);

  -- Connect FIFO SPU2PE0_to_SPU3PE0 with PE
  ch_SPU2PE0_to_SPU3PE0_a <= put_ch_data_2(0);
  ch_SPU2PE0_to_SPU3PE0_write <= put_ch_write_2(0);
  put_ch_full_2(0) <= ch_SPU2PE0_to_SPU3PE0_full;

  get_ch_data_3(0) <= ch_SPU2PE0_to_SPU3PE0_b;
  get_ch_empty_3(0) <= ch_SPU2PE0_to_SPU3PE0_empty;
  ch_SPU2PE0_to_SPU3PE0_read <= get_ch_read_3(0);

  -- Connect FIFO SPU2PE0_to_SPU3PE0_1 with PE
  ch_SPU2PE0_to_SPU3PE0_1_a <= put_ch_data_2(1);
  ch_SPU2PE0_to_SPU3PE0_1_write <= put_ch_write_2(1);
  put_ch_full_2(1) <= ch_SPU2PE0_to_SPU3PE0_1_full;

  get_ch_data_3(1) <= ch_SPU2PE0_to_SPU3PE0_1_b;
  get_ch_empty_3(1) <= ch_SPU2PE0_to_SPU3PE0_1_empty;
  ch_SPU2PE0_to_SPU3PE0_1_read <= get_ch_read_3(1);

  -- Connect FIFO SPU3PE0_to_SPU4PE0 with PE
  ch_SPU3PE0_to_SPU4PE0_a <= put_ch_data_3(0);
  ch_SPU3PE0_to_SPU4PE0_write <= put_ch_write_3(0);
  put_ch_full_3(0) <= ch_SPU3PE0_to_SPU4PE0_full;

  get_ch_data_4(0) <= ch_SPU3PE0_to_SPU4PE0_b;
  get_ch_empty_4(0) <= ch_SPU3PE0_to_SPU4PE0_empty;
  ch_SPU3PE0_to_SPU4PE0_read <= get_ch_read_4(0);

  -- Connect FIFO SPU3PE0_to_SPU4PE0_1 with PE
  ch_SPU3PE0_to_SPU4PE0_1_a <= put_ch_data_3(1);
  ch_SPU3PE0_to_SPU4PE0_1_write <= put_ch_write_3(1);
  put_ch_full_3(1) <= ch_SPU3PE0_to_SPU4PE0_1_full;

  get_ch_data_4(1) <= ch_SPU3PE0_to_SPU4PE0_1_b;
  get_ch_empty_4(1) <= ch_SPU3PE0_to_SPU4PE0_1_empty;
  ch_SPU3PE0_to_SPU4PE0_1_read <= get_ch_read_4(1);

  -- Instantiate PEs and clock enables
u_core_0: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 2,
  SLICE_NUM       => 4,
  CORE_DATA_WIDTH => 32,
  OPM_NUM         => 2,
  ALUM_NUM        => 3,
  FRAC_BITS       => 14,
  BSLAVE          => false,
  BMASTER         => false,
  BMASTER_NUM     => 1,
  VLEN            => 1,
  OPCODE_WIDTH    => 4,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => false,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => true,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 8,
  FLEXB_TYPE   => 4,
  FLEXC_TYPE   => 8,
  
  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> 16384,

  EBITS_A      => 0,
  EBITS_B      => 0,
  EBITS_C      => 0,
  EBITS_D      => 0,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 2,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 2,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU0PE",

  PM_SIZE       => 68,
  PM_ADDR_WIDTH => 7,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => false,
  PM_INIT_FILE => "PMInit/pm_init0.mif",

  DM_EN                 => false,
  DM_SIZE               => 32,
  DM_ADDR_WIDTH         => 5,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU0PE",
  DM_RB_M_NUM           => 0,
  DM_RB_N_NUM           => 0,
  DM_WB_NUM             => 0,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 0,
  DM_RB_N_INITIAL1      => 0,
  DM_WB_INITIAL0        => 0,
  DM_WB_INITIAL1        => 0,
  DM_RB_M_AUTOINC_SIZE0 => 1,
  DM_RB_M_AUTOINC_SIZE1 => 1,
  DM_RB_N_AUTOINC_SIZE0 => 1,
  DM_RB_N_AUTOINC_SIZE1 => 1,
  DM_WB_AUTOINC_SIZE0   => 1,
  DM_WB_AUTOINC_SIZE1   => 1,
  DM_OFFSET_EN          => false,
  DM_RB_M_SET_EN0       => false,
  DM_RB_M_SET_EN1       => false,
  DM_RB_N_SET_EN0       => false,
  DM_RB_N_SET_EN1       => false,
  DM_WB_SET_EN0         => false,
  DM_WB_SET_EN1         => false,
  DM_RB_M_AUTOINC_EN0   => false,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => false,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => false,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => false,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => false,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => false,
  DM_WB_INC_EN1         => false,

  SM_EN        => false,
  SM_SIZE       => 32,
  SM_ADDR_WIDTH    => 5,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init0.mif",
  SM_OFFSET_EN => false,
  SM_READONLY => true,
  SM_RB_SET_EN0 => false,
  SM_WB_SET_EN0 => false,
  SM_RB_INC_EN0 => false,
  SM_WB_INC_EN0 => false,
  SM_RB_AUTOINC_EN0 => false,
  SM_WB_AUTOINC_EN0 => false,
  SM_RB_AUTOINC_SIZE0 => 1,
  SM_WB_AUTOINC_SIZE0 => 1
)
port map(
  clk => clk,
  rst => rst,

  i_ext_en_spu => open,
  o_ext_barrier => open,
  i_ext_barrier => open,
  o_ext_en_spu => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_0,
  o_get_ch_read  => get_ch_read_0,
  i_get_ch_empty => get_ch_empty_0,

  -- Output channel
  o_put_ch_data  => put_ch_data_0,
  o_put_ch_write => put_ch_write_0,
  i_put_ch_full  => put_ch_full_0
);


u_core_1: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 2,
  SLICE_NUM       => 4,
  CORE_DATA_WIDTH => 32,
  OPM_NUM         => 2,
  ALUM_NUM        => 3,
  FRAC_BITS       => 14,
  BSLAVE          => false,
  BMASTER         => false,
  BMASTER_NUM     => 1,
  VLEN            => 1,
  OPCODE_WIDTH    => 4,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => false,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => true,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 10,
  FLEXB_TYPE   => 4,
  FLEXC_TYPE   => 10,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 0,
  EBITS_B      => 0,
  EBITS_C      => 0,
  EBITS_D      => 0,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 2,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 2,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU1PE",

  PM_SIZE       => 78,
  PM_ADDR_WIDTH => 7,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => false,
  PM_INIT_FILE => "PMInit/pm_init1.mif",

  DM_EN                 => true,
  DM_SIZE               => 32,
  DM_ADDR_WIDTH         => 5,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU1PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 0,
  DM_RB_N_INITIAL1      => 0,
  DM_WB_INITIAL0        => 0,
  DM_WB_INITIAL1        => 0,
  DM_RB_M_AUTOINC_SIZE0 => 1,
  DM_RB_M_AUTOINC_SIZE1 => 1,
  DM_RB_N_AUTOINC_SIZE0 => 1,
  DM_RB_N_AUTOINC_SIZE1 => 1,
  DM_WB_AUTOINC_SIZE0   => 1,
  DM_WB_AUTOINC_SIZE1   => 1,
  DM_OFFSET_EN          => true,
  DM_RB_M_SET_EN0       => false,
  DM_RB_M_SET_EN1       => false,
  DM_RB_N_SET_EN0       => false,
  DM_RB_N_SET_EN1       => false,
  DM_WB_SET_EN0         => false,
  DM_WB_SET_EN1         => false,
  DM_RB_M_AUTOINC_EN0   => false,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => false,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => false,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => false,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => false,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => false,
  DM_WB_INC_EN1         => false,

  SM_EN        => true,
  SM_SIZE       => 32,
  SM_ADDR_WIDTH    => 5,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init1.mif",
  SM_OFFSET_EN => false,
  SM_READONLY => true,
  SM_RB_SET_EN0 => false,
  SM_WB_SET_EN0 => false,
  SM_RB_INC_EN0 => false,
  SM_WB_INC_EN0 => false,
  SM_RB_AUTOINC_EN0 => false,
  SM_WB_AUTOINC_EN0 => false,
  SM_RB_AUTOINC_SIZE0 => 1,
  SM_WB_AUTOINC_SIZE0 => 1
)
port map(
  clk => clk,
  rst => rst,

  i_ext_en_spu => open,
  o_ext_barrier => open,
  i_ext_barrier => open,
  o_ext_en_spu => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_1,
  o_get_ch_read  => get_ch_read_1,
  i_get_ch_empty => get_ch_empty_1,

  -- Output channel
  o_put_ch_data  => put_ch_data_1,
  o_put_ch_write => put_ch_write_1,
  i_put_ch_full  => put_ch_full_1
);

u_core_2: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 2,
  SLICE_NUM       => 4,
  CORE_DATA_WIDTH => 32,
  OPM_NUM         => 2,
  ALUM_NUM        => 3,
  FRAC_BITS       => 14,
  BSLAVE          => false,
  BMASTER         => false,
  BMASTER_NUM     => 1,
  VLEN            => 1,
  OPCODE_WIDTH    => 4,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => false,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => true,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 10,
  FLEXB_TYPE   => 4,
  FLEXC_TYPE   => 10,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 0,
  EBITS_B      => 0,
  EBITS_C      => 0,
  EBITS_D      => 0,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 2,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 2,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU2PE",

  PM_SIZE       => 190,
  PM_ADDR_WIDTH => 8,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => false,
  PM_INIT_FILE => "PMInit/pm_init2.mif",

  DM_EN                 => true,
  DM_SIZE               => 32,
  DM_ADDR_WIDTH         => 5,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU2PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 0,
  DM_RB_N_INITIAL1      => 0,
  DM_WB_INITIAL0        => 0,
  DM_WB_INITIAL1        => 0,
  DM_RB_M_AUTOINC_SIZE0 => 1,
  DM_RB_M_AUTOINC_SIZE1 => 1,
  DM_RB_N_AUTOINC_SIZE0 => 1,
  DM_RB_N_AUTOINC_SIZE1 => 1,
  DM_WB_AUTOINC_SIZE0   => 1,
  DM_WB_AUTOINC_SIZE1   => 1,
  DM_OFFSET_EN          => true,
  DM_RB_M_SET_EN0       => false,
  DM_RB_M_SET_EN1       => false,
  DM_RB_N_SET_EN0       => false,
  DM_RB_N_SET_EN1       => false,
  DM_WB_SET_EN0         => false,
  DM_WB_SET_EN1         => false,
  DM_RB_M_AUTOINC_EN0   => false,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => false,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => false,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => false,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => false,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => false,
  DM_WB_INC_EN1         => false,

  SM_EN        => true,
  SM_SIZE       => 32,
  SM_ADDR_WIDTH    => 5,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init2.mif",
  SM_OFFSET_EN => false,
  SM_READONLY => true,
  SM_RB_SET_EN0 => false,
  SM_WB_SET_EN0 => false,
  SM_RB_INC_EN0 => false,
  SM_WB_INC_EN0 => false,
  SM_RB_AUTOINC_EN0 => false,
  SM_WB_AUTOINC_EN0 => false,
  SM_RB_AUTOINC_SIZE0 => 1,
  SM_WB_AUTOINC_SIZE0 => 1
)
port map(
  clk => clk,
  rst => rst,

  i_ext_en_spu => open,
  o_ext_barrier => open,
  i_ext_barrier => open,
  o_ext_en_spu => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_2,
  o_get_ch_read  => get_ch_read_2,
  i_get_ch_empty => get_ch_empty_2,

  -- Output channel
  o_put_ch_data  => put_ch_data_2,
  o_put_ch_write => put_ch_write_2,
  i_put_ch_full  => put_ch_full_2
);


u_core_3: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 2,
  SLICE_NUM       => 4,
  CORE_DATA_WIDTH => 32,
  OPM_NUM         => 2,
  ALUM_NUM        => 3,
  FRAC_BITS       => 14,
  BSLAVE          => false,
  BMASTER         => false,
  BMASTER_NUM     => 1,
  VLEN            => 1,
  OPCODE_WIDTH    => 4,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => false,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => true,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 10,
  FLEXB_TYPE   => 4,
  FLEXC_TYPE   => 10,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 2,
  EBITS_B      => 0,
  EBITS_C      => 2,
  EBITS_D      => 2,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 2,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 2,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU3PE",

  PM_SIZE       => 758,
  PM_ADDR_WIDTH => 10,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init3.mif",

  DM_EN                 => true,
  DM_SIZE               => 128,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => false,
  DM_INIT_FILE          => "DMInit/dm_initSPU3PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 0,
  DM_RB_N_INITIAL1      => 0,
  DM_WB_INITIAL0        => 0,
  DM_WB_INITIAL1        => 0,
  DM_RB_M_AUTOINC_SIZE0 => 1,
  DM_RB_M_AUTOINC_SIZE1 => 1,
  DM_RB_N_AUTOINC_SIZE0 => 1,
  DM_RB_N_AUTOINC_SIZE1 => 1,
  DM_WB_AUTOINC_SIZE0   => 1,
  DM_WB_AUTOINC_SIZE1   => 1,
  DM_OFFSET_EN          => true,
  DM_RB_M_SET_EN0       => false,
  DM_RB_M_SET_EN1       => false,
  DM_RB_N_SET_EN0       => false,
  DM_RB_N_SET_EN1       => false,
  DM_WB_SET_EN0         => false,
  DM_WB_SET_EN1         => false,
  DM_RB_M_AUTOINC_EN0   => false,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => false,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => false,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => false,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => false,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => false,
  DM_WB_INC_EN1         => false,

  SM_EN        => true,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init3.mif",
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
  SM_WB_SET_EN0 => false,
  SM_RB_INC_EN0 => false,
  SM_WB_INC_EN0 => false,
  SM_RB_AUTOINC_EN0 => false,
  SM_WB_AUTOINC_EN0 => false,
  SM_RB_AUTOINC_SIZE0 => 1,
  SM_WB_AUTOINC_SIZE0 => 1
)
port map(
  clk => clk,
  rst => rst,

  i_ext_en_spu => open,
  o_ext_barrier => open,
  i_ext_barrier => open,
  o_ext_en_spu => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_3,
  o_get_ch_read  => get_ch_read_3,
  i_get_ch_empty => get_ch_empty_3,

  -- Output channel
  o_put_ch_data  => put_ch_data_3,
  o_put_ch_write => put_ch_write_3,
  i_put_ch_full  => put_ch_full_3
);


u_core_4: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 2,
  SLICE_NUM       => 4,
  CORE_DATA_WIDTH => 32,
  OPM_NUM         => 2,
  ALUM_NUM        => 3,
  FRAC_BITS       => 14,
  BSLAVE          => false,
  BMASTER         => false,
  BMASTER_NUM     => 1,
  VLEN            => 1,
  OPCODE_WIDTH    => 4,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => false,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => true,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 10,
  FLEXB_TYPE   => 4,
  FLEXC_TYPE   => 10,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 4,
  EBITS_B      => 0,
  EBITS_C      => 4,
  EBITS_D      => 4,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 2,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 1,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU4PE",

  PM_SIZE       => 1949,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init4.mif",

  DM_EN                 => true,
  DM_SIZE               => 512,
  DM_ADDR_WIDTH         => 9,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU4PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 0,
  DM_RB_N_INITIAL1      => 0,
  DM_WB_INITIAL0        => 0,
  DM_WB_INITIAL1        => 0,
  DM_RB_M_AUTOINC_SIZE0 => 1,
  DM_RB_M_AUTOINC_SIZE1 => 1,
  DM_RB_N_AUTOINC_SIZE0 => 1,
  DM_RB_N_AUTOINC_SIZE1 => 1,
  DM_WB_AUTOINC_SIZE0   => 1,
  DM_WB_AUTOINC_SIZE1   => 1,
  DM_OFFSET_EN          => true,
  DM_RB_M_SET_EN0       => false,
  DM_RB_M_SET_EN1       => false,
  DM_RB_N_SET_EN0       => false,
  DM_RB_N_SET_EN1       => false,
  DM_WB_SET_EN0         => false,
  DM_WB_SET_EN1         => false,
  DM_RB_M_AUTOINC_EN0   => false,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => false,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => false,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => false,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => false,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => false,
  DM_WB_INC_EN1         => false,

  SM_EN        => true,
  SM_SIZE       => 256,
  SM_ADDR_WIDTH    => 8,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init4.mif",
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
  SM_WB_SET_EN0 => false,
  SM_RB_INC_EN0 => false,
  SM_WB_INC_EN0 => false,
  SM_RB_AUTOINC_EN0 => false,
  SM_WB_AUTOINC_EN0 => false,
  SM_RB_AUTOINC_SIZE0 => 1,
  SM_WB_AUTOINC_SIZE0 => 1
)
port map(
  clk => clk,
  rst => rst,

  i_ext_en_spu => open,
  o_ext_barrier => open,
  i_ext_barrier => open,
  o_ext_en_spu => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_4,
  o_get_ch_read  => get_ch_read_4,
  i_get_ch_empty => get_ch_empty_4,

  -- Output channel
  o_put_ch_data  => put_ch_data_4,
  o_put_ch_write => put_ch_write_4,
  i_put_ch_full  => put_ch_full_4
);


  -- Instantiate FIFOs
u_fifo_IOCore_to_SPU0PE0: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE0_a,
  write   => ch_IOCore_to_SPU0PE0_write,
  o_full  => ch_IOCore_to_SPU0PE0_full,

  o_data  => ch_IOCore_to_SPU0PE0_b,
  read    => ch_IOCore_to_SPU0PE0_read,
  o_empty => ch_IOCore_to_SPU0PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE0_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE0_1_a,
  write   => ch_IOCore_to_SPU0PE0_1_write,
  o_full  => ch_IOCore_to_SPU0PE0_1_full,

  o_data  => ch_IOCore_to_SPU0PE0_1_b,
  read    => ch_IOCore_to_SPU0PE0_1_read,
  o_empty => ch_IOCore_to_SPU0PE0_1_empty,
  clk     => clk
);

u_fifo_SPU4PE0_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU4PE0_to_IOCore_a,
  write   => ch_SPU4PE0_to_IOCore_write,
  o_full  => ch_SPU4PE0_to_IOCore_full,

  o_data  => ch_SPU4PE0_to_IOCore_b,
  read    => ch_SPU4PE0_to_IOCore_read,
  o_empty => ch_SPU4PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE0_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>12 )
port map(
  i_data  => ch_SPU0PE0_to_SPU1PE0_a,
  write   => ch_SPU0PE0_to_SPU1PE0_write,
  o_full  => ch_SPU0PE0_to_SPU1PE0_full,

  o_data  => ch_SPU0PE0_to_SPU1PE0_b,
  read    => ch_SPU0PE0_to_SPU1PE0_read,
  o_empty => ch_SPU0PE0_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE0_to_SPU1PE0_1: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>11 )
port map(
  i_data  => ch_SPU0PE0_to_SPU1PE0_1_a,
  write   => ch_SPU0PE0_to_SPU1PE0_1_write,
  o_full  => ch_SPU0PE0_to_SPU1PE0_1_full,

  o_data  => ch_SPU0PE0_to_SPU1PE0_1_b,
  read    => ch_SPU0PE0_to_SPU1PE0_1_read,
  o_empty => ch_SPU0PE0_to_SPU1PE0_1_empty,
  clk     => clk
);

u_fifo_SPU1PE0_to_SPU2PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>11 )
port map(
  i_data  => ch_SPU1PE0_to_SPU2PE0_a,
  write   => ch_SPU1PE0_to_SPU2PE0_write,
  o_full  => ch_SPU1PE0_to_SPU2PE0_full,

  o_data  => ch_SPU1PE0_to_SPU2PE0_b,
  read    => ch_SPU1PE0_to_SPU2PE0_read,
  o_empty => ch_SPU1PE0_to_SPU2PE0_empty,
  clk     => clk
);

u_fifo_SPU1PE0_to_SPU2PE0_1: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>7 )
port map(
  i_data  => ch_SPU1PE0_to_SPU2PE0_1_a,
  write   => ch_SPU1PE0_to_SPU2PE0_1_write,
  o_full  => ch_SPU1PE0_to_SPU2PE0_1_full,

  o_data  => ch_SPU1PE0_to_SPU2PE0_1_b,
  read    => ch_SPU1PE0_to_SPU2PE0_1_read,
  o_empty => ch_SPU1PE0_to_SPU2PE0_1_empty,
  clk     => clk
);

u_fifo_SPU2PE0_to_SPU3PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>63 )
port map(
  i_data  => ch_SPU2PE0_to_SPU3PE0_a,
  write   => ch_SPU2PE0_to_SPU3PE0_write,
  o_full  => ch_SPU2PE0_to_SPU3PE0_full,

  o_data  => ch_SPU2PE0_to_SPU3PE0_b,
  read    => ch_SPU2PE0_to_SPU3PE0_read,
  o_empty => ch_SPU2PE0_to_SPU3PE0_empty,
  clk     => clk
);

u_fifo_SPU2PE0_to_SPU3PE0_1: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_SPU2PE0_to_SPU3PE0_1_a,
  write   => ch_SPU2PE0_to_SPU3PE0_1_write,
  o_full  => ch_SPU2PE0_to_SPU3PE0_1_full,

  o_data  => ch_SPU2PE0_to_SPU3PE0_1_b,
  read    => ch_SPU2PE0_to_SPU3PE0_1_read,
  o_empty => ch_SPU2PE0_to_SPU3PE0_1_empty,
  clk     => clk
);

u_fifo_SPU3PE0_to_SPU4PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>197 )
port map(
  i_data  => ch_SPU3PE0_to_SPU4PE0_a,
  write   => ch_SPU3PE0_to_SPU4PE0_write,
  o_full  => ch_SPU3PE0_to_SPU4PE0_full,

  o_data  => ch_SPU3PE0_to_SPU4PE0_b,
  read    => ch_SPU3PE0_to_SPU4PE0_read,
  o_empty => ch_SPU3PE0_to_SPU4PE0_empty,
  clk     => clk
);

u_fifo_SPU3PE0_to_SPU4PE0_1: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>128 )
port map(
  i_data  => ch_SPU3PE0_to_SPU4PE0_1_a,
  write   => ch_SPU3PE0_to_SPU4PE0_1_write,
  o_full  => ch_SPU3PE0_to_SPU4PE0_1_full,

  o_data  => ch_SPU3PE0_to_SPU4PE0_1_b,
  read    => ch_SPU3PE0_to_SPU4PE0_1_read,
  o_empty => ch_SPU3PE0_to_SPU4PE0_1_empty,
  clk     => clk
);

end Structure;
