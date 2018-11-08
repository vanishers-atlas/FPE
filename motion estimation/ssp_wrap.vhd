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
      CORE_WIDTH     : integer := 16;
      INPUT_WIDTH    : integer := 8;
      OUTPUT_WIDTH   : integer := 16;
      EXIN_FIFO_NUM  : integer := 32;
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
  signal ch_IOCore_to_SPU0PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_write : std_logic;
  signal ch_IOCore_to_SPU0PE0_full  : std_logic;
  signal ch_IOCore_to_SPU0PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE0_read  : std_logic;
  signal ch_IOCore_to_SPU0PE0_empty : std_logic;
  signal ch_IOCore_to_SPU0PE1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_write : std_logic;
  signal ch_IOCore_to_SPU0PE1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE2_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_write : std_logic;
  signal ch_IOCore_to_SPU0PE2_full  : std_logic;
  signal ch_IOCore_to_SPU0PE2_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_read  : std_logic;
  signal ch_IOCore_to_SPU0PE2_empty : std_logic;
  signal ch_IOCore_to_SPU0PE3_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_write : std_logic;
  signal ch_IOCore_to_SPU0PE3_full  : std_logic;
  signal ch_IOCore_to_SPU0PE3_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_read  : std_logic;
  signal ch_IOCore_to_SPU0PE3_empty : std_logic;
  signal ch_IOCore_to_SPU0PE4_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_write : std_logic;
  signal ch_IOCore_to_SPU0PE4_full  : std_logic;
  signal ch_IOCore_to_SPU0PE4_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_read  : std_logic;
  signal ch_IOCore_to_SPU0PE4_empty : std_logic;
  signal ch_IOCore_to_SPU0PE5_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_write : std_logic;
  signal ch_IOCore_to_SPU0PE5_full  : std_logic;
  signal ch_IOCore_to_SPU0PE5_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_read  : std_logic;
  signal ch_IOCore_to_SPU0PE5_empty : std_logic;
  signal ch_IOCore_to_SPU0PE6_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_write : std_logic;
  signal ch_IOCore_to_SPU0PE6_full  : std_logic;
  signal ch_IOCore_to_SPU0PE6_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_read  : std_logic;
  signal ch_IOCore_to_SPU0PE6_empty : std_logic;
  signal ch_IOCore_to_SPU0PE7_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_write : std_logic;
  signal ch_IOCore_to_SPU0PE7_full  : std_logic;
  signal ch_IOCore_to_SPU0PE7_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_read  : std_logic;
  signal ch_IOCore_to_SPU0PE7_empty : std_logic;
  signal ch_IOCore_to_SPU0PE8_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE8_write : std_logic;
  signal ch_IOCore_to_SPU0PE8_full  : std_logic;
  signal ch_IOCore_to_SPU0PE8_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE8_read  : std_logic;
  signal ch_IOCore_to_SPU0PE8_empty : std_logic;
  signal ch_IOCore_to_SPU0PE9_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE9_write : std_logic;
  signal ch_IOCore_to_SPU0PE9_full  : std_logic;
  signal ch_IOCore_to_SPU0PE9_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE9_read  : std_logic;
  signal ch_IOCore_to_SPU0PE9_empty : std_logic;
  signal ch_IOCore_to_SPU0PE10_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE10_write : std_logic;
  signal ch_IOCore_to_SPU0PE10_full  : std_logic;
  signal ch_IOCore_to_SPU0PE10_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE10_read  : std_logic;
  signal ch_IOCore_to_SPU0PE10_empty : std_logic;
  signal ch_IOCore_to_SPU0PE11_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE11_write : std_logic;
  signal ch_IOCore_to_SPU0PE11_full  : std_logic;
  signal ch_IOCore_to_SPU0PE11_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE11_read  : std_logic;
  signal ch_IOCore_to_SPU0PE11_empty : std_logic;
  signal ch_IOCore_to_SPU0PE12_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE12_write : std_logic;
  signal ch_IOCore_to_SPU0PE12_full  : std_logic;
  signal ch_IOCore_to_SPU0PE12_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE12_read  : std_logic;
  signal ch_IOCore_to_SPU0PE12_empty : std_logic;
  signal ch_IOCore_to_SPU0PE13_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE13_write : std_logic;
  signal ch_IOCore_to_SPU0PE13_full  : std_logic;
  signal ch_IOCore_to_SPU0PE13_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE13_read  : std_logic;
  signal ch_IOCore_to_SPU0PE13_empty : std_logic;
  signal ch_IOCore_to_SPU0PE14_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE14_write : std_logic;
  signal ch_IOCore_to_SPU0PE14_full  : std_logic;
  signal ch_IOCore_to_SPU0PE14_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE14_read  : std_logic;
  signal ch_IOCore_to_SPU0PE14_empty : std_logic;
  signal ch_IOCore_to_SPU0PE15_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE15_write : std_logic;
  signal ch_IOCore_to_SPU0PE15_full  : std_logic;
  signal ch_IOCore_to_SPU0PE15_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE15_read  : std_logic;
  signal ch_IOCore_to_SPU0PE15_empty : std_logic;
  signal ch_IOCore_to_SPU0PE16_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE16_write : std_logic;
  signal ch_IOCore_to_SPU0PE16_full  : std_logic;
  signal ch_IOCore_to_SPU0PE16_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE16_read  : std_logic;
  signal ch_IOCore_to_SPU0PE16_empty : std_logic;
  signal ch_IOCore_to_SPU0PE17_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE17_write : std_logic;
  signal ch_IOCore_to_SPU0PE17_full  : std_logic;
  signal ch_IOCore_to_SPU0PE17_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE17_read  : std_logic;
  signal ch_IOCore_to_SPU0PE17_empty : std_logic;
  signal ch_IOCore_to_SPU0PE18_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE18_write : std_logic;
  signal ch_IOCore_to_SPU0PE18_full  : std_logic;
  signal ch_IOCore_to_SPU0PE18_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE18_read  : std_logic;
  signal ch_IOCore_to_SPU0PE18_empty : std_logic;
  signal ch_IOCore_to_SPU0PE19_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE19_write : std_logic;
  signal ch_IOCore_to_SPU0PE19_full  : std_logic;
  signal ch_IOCore_to_SPU0PE19_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE19_read  : std_logic;
  signal ch_IOCore_to_SPU0PE19_empty : std_logic;
  signal ch_IOCore_to_SPU0PE20_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE20_write : std_logic;
  signal ch_IOCore_to_SPU0PE20_full  : std_logic;
  signal ch_IOCore_to_SPU0PE20_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE20_read  : std_logic;
  signal ch_IOCore_to_SPU0PE20_empty : std_logic;
  signal ch_IOCore_to_SPU0PE21_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE21_write : std_logic;
  signal ch_IOCore_to_SPU0PE21_full  : std_logic;
  signal ch_IOCore_to_SPU0PE21_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE21_read  : std_logic;
  signal ch_IOCore_to_SPU0PE21_empty : std_logic;
  signal ch_IOCore_to_SPU0PE22_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE22_write : std_logic;
  signal ch_IOCore_to_SPU0PE22_full  : std_logic;
  signal ch_IOCore_to_SPU0PE22_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE22_read  : std_logic;
  signal ch_IOCore_to_SPU0PE22_empty : std_logic;
  signal ch_IOCore_to_SPU0PE23_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE23_write : std_logic;
  signal ch_IOCore_to_SPU0PE23_full  : std_logic;
  signal ch_IOCore_to_SPU0PE23_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE23_read  : std_logic;
  signal ch_IOCore_to_SPU0PE23_empty : std_logic;
  signal ch_IOCore_to_SPU0PE24_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE24_write : std_logic;
  signal ch_IOCore_to_SPU0PE24_full  : std_logic;
  signal ch_IOCore_to_SPU0PE24_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE24_read  : std_logic;
  signal ch_IOCore_to_SPU0PE24_empty : std_logic;
  signal ch_IOCore_to_SPU0PE25_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE25_write : std_logic;
  signal ch_IOCore_to_SPU0PE25_full  : std_logic;
  signal ch_IOCore_to_SPU0PE25_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE25_read  : std_logic;
  signal ch_IOCore_to_SPU0PE25_empty : std_logic;
  signal ch_IOCore_to_SPU0PE26_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE26_write : std_logic;
  signal ch_IOCore_to_SPU0PE26_full  : std_logic;
  signal ch_IOCore_to_SPU0PE26_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE26_read  : std_logic;
  signal ch_IOCore_to_SPU0PE26_empty : std_logic;
  signal ch_IOCore_to_SPU0PE27_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE27_write : std_logic;
  signal ch_IOCore_to_SPU0PE27_full  : std_logic;
  signal ch_IOCore_to_SPU0PE27_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE27_read  : std_logic;
  signal ch_IOCore_to_SPU0PE27_empty : std_logic;
  signal ch_IOCore_to_SPU0PE28_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE28_write : std_logic;
  signal ch_IOCore_to_SPU0PE28_full  : std_logic;
  signal ch_IOCore_to_SPU0PE28_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE28_read  : std_logic;
  signal ch_IOCore_to_SPU0PE28_empty : std_logic;
  signal ch_IOCore_to_SPU0PE29_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE29_write : std_logic;
  signal ch_IOCore_to_SPU0PE29_full  : std_logic;
  signal ch_IOCore_to_SPU0PE29_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE29_read  : std_logic;
  signal ch_IOCore_to_SPU0PE29_empty : std_logic;
  signal ch_IOCore_to_SPU0PE30_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE30_write : std_logic;
  signal ch_IOCore_to_SPU0PE30_full  : std_logic;
  signal ch_IOCore_to_SPU0PE30_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE30_read  : std_logic;
  signal ch_IOCore_to_SPU0PE30_empty : std_logic;
  signal ch_IOCore_to_SPU0PE31_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE31_write : std_logic;
  signal ch_IOCore_to_SPU0PE31_full  : std_logic;
  signal ch_IOCore_to_SPU0PE31_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE31_read  : std_logic;
  signal ch_IOCore_to_SPU0PE31_empty : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE0_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE1_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE1_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE1_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE1_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE1_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE1_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE2_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE2_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE2_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE2_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE2_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE2_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE3_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE3_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE3_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE3_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE3_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE3_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE4_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE4_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE4_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE4_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE4_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE4_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE5_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE5_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE5_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE5_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE5_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE5_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE6_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE6_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE6_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE6_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE6_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE6_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE7_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE7_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE7_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE7_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE7_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE7_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE8_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE8_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE8_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE8_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE8_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE8_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE9_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE9_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE9_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE9_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE9_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE9_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE10_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE10_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE10_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE10_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE10_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE10_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE11_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE11_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE11_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE11_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE11_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE11_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE12_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE12_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE12_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE12_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE12_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE12_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE13_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE13_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE13_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE13_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE13_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE13_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE14_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE14_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE14_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE14_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE14_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE14_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE15_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE15_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE15_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE15_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE15_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE15_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE16_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE16_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE16_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE16_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE16_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE16_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE17_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE17_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE17_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE17_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE17_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE17_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE18_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE18_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE18_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE18_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE18_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE18_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE19_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE19_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE19_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE19_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE19_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE19_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE20_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE20_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE20_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE20_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE20_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE20_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE21_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE21_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE21_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE21_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE21_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE21_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE22_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE22_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE22_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE22_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE22_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE22_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE23_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE23_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE23_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE23_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE23_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE23_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE24_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE24_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE24_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE24_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE24_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE24_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE25_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE25_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE25_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE25_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE25_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE25_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE26_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE26_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE26_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE26_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE26_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE26_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE27_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE27_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE27_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE27_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE27_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE27_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE28_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE28_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE28_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE28_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE28_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE28_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE29_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE29_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE29_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE29_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE29_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE29_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE30_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE30_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE30_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE30_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE30_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE30_to_SPU1PE0_empty : std_logic;
  signal ch_SPU0PE31_to_SPU1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE31_to_SPU1PE0_write : std_logic;
  signal ch_SPU0PE31_to_SPU1PE0_full  : std_logic;
  signal ch_SPU0PE31_to_SPU1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE31_to_SPU1PE0_read  : std_logic;
  signal ch_SPU0PE31_to_SPU1PE0_empty : std_logic;
  signal ch_SPU1PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_IOCore_write : std_logic;
  signal ch_SPU1PE0_to_IOCore_full  : std_logic;
  signal ch_SPU1PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU1PE0_to_IOCore_read  : std_logic;
  signal ch_SPU1PE0_to_IOCore_empty : std_logic;
  -- SPU signals
  signal get_ch_data_0  : VDATA_TYPE(31 downto 0);
  signal get_ch_read_0  : VSIG_TYPE(31 downto 0);
  signal get_ch_empty_0 : VSIG_TYPE(31 downto 0);
  signal put_ch_data_0  : VDATA_TYPE(31 downto 0);
  signal put_ch_write_0 : VSIG_TYPE(31 downto 0);
  signal put_ch_full_0  : VSIG_TYPE(31 downto 0);

  signal get_ch_data_1  : VDATA_TYPE(31 downto 0);
  signal get_ch_read_1  : VSIG_TYPE(31 downto 0);
  signal get_ch_empty_1 : VSIG_TYPE(31 downto 0);
  signal put_ch_data_1  : VDATA_TYPE(0 downto 0);
  signal put_ch_write_1 : VSIG_TYPE(0 downto 0);
  signal put_ch_full_1  : VSIG_TYPE(0 downto 0);
  
  signal barrier_SPU1_IOCore, enspu_SPU1, enspu_IOCore_SPU0, enspu_IOCore_SPU1, enspu_SPU0_SPU1, barrier_SPU1_SPU0 : std_logic;
  signal barrier_SPU1 : std_logic_vector(1 downto 0);
  signal barrier_SPU0_IOCore : std_logic_vector(0 downto 0);
  
begin

  -- Connect signals with module ports
  o_barrier <= barrier_SPU0_IOCore(0) or barrier_SPU1_IOCore;
  enspu_IOCore_SPU0 <= i_en_spu;
  enspu_IOCore_SPU1 <= i_en_spu;
  enspu_SPU1 <= enspu_SPU0_SPU1 and enspu_IOCore_SPU1;
  barrier_SPU1_SPU0 <= barrier_SPU1(0);
  barrier_SPU1_IOCore <= barrier_SPU1(1);
  

  ch_IOCore_to_SPU0PE0_a <= i_push_ch_data(0);
  ch_IOCore_to_SPU0PE0_write  <= i_push_ch_write(0);
  o_push_ch_full(0) <= ch_IOCore_to_SPU0PE0_full;

  ch_IOCore_to_SPU0PE1_a <= i_push_ch_data(1);
  ch_IOCore_to_SPU0PE1_write  <= i_push_ch_write(1);
  o_push_ch_full(1) <= ch_IOCore_to_SPU0PE1_full;

  ch_IOCore_to_SPU0PE2_a <= i_push_ch_data(2);
  ch_IOCore_to_SPU0PE2_write  <= i_push_ch_write(2);
  o_push_ch_full(2) <= ch_IOCore_to_SPU0PE2_full;

  ch_IOCore_to_SPU0PE3_a <= i_push_ch_data(3);
  ch_IOCore_to_SPU0PE3_write  <= i_push_ch_write(3);
  o_push_ch_full(3) <= ch_IOCore_to_SPU0PE3_full;

  ch_IOCore_to_SPU0PE4_a <= i_push_ch_data(4);
  ch_IOCore_to_SPU0PE4_write  <= i_push_ch_write(4);
  o_push_ch_full(4) <= ch_IOCore_to_SPU0PE4_full;

  ch_IOCore_to_SPU0PE5_a <= i_push_ch_data(5);
  ch_IOCore_to_SPU0PE5_write  <= i_push_ch_write(5);
  o_push_ch_full(5) <= ch_IOCore_to_SPU0PE5_full;

  ch_IOCore_to_SPU0PE6_a <= i_push_ch_data(6);
  ch_IOCore_to_SPU0PE6_write  <= i_push_ch_write(6);
  o_push_ch_full(6) <= ch_IOCore_to_SPU0PE6_full;

  ch_IOCore_to_SPU0PE7_a <= i_push_ch_data(7);
  ch_IOCore_to_SPU0PE7_write  <= i_push_ch_write(7);
  o_push_ch_full(7) <= ch_IOCore_to_SPU0PE7_full;

  ch_IOCore_to_SPU0PE8_a <= i_push_ch_data(8);
  ch_IOCore_to_SPU0PE8_write  <= i_push_ch_write(8);
  o_push_ch_full(8) <= ch_IOCore_to_SPU0PE8_full;

  ch_IOCore_to_SPU0PE9_a <= i_push_ch_data(9);
  ch_IOCore_to_SPU0PE9_write  <= i_push_ch_write(9);
  o_push_ch_full(9) <= ch_IOCore_to_SPU0PE9_full;

  ch_IOCore_to_SPU0PE10_a <= i_push_ch_data(10);
  ch_IOCore_to_SPU0PE10_write  <= i_push_ch_write(10);
  o_push_ch_full(10) <= ch_IOCore_to_SPU0PE10_full;

  ch_IOCore_to_SPU0PE11_a <= i_push_ch_data(11);
  ch_IOCore_to_SPU0PE11_write  <= i_push_ch_write(11);
  o_push_ch_full(11) <= ch_IOCore_to_SPU0PE11_full;

  ch_IOCore_to_SPU0PE12_a <= i_push_ch_data(12);
  ch_IOCore_to_SPU0PE12_write  <= i_push_ch_write(12);
  o_push_ch_full(12) <= ch_IOCore_to_SPU0PE12_full;

  ch_IOCore_to_SPU0PE13_a <= i_push_ch_data(13);
  ch_IOCore_to_SPU0PE13_write  <= i_push_ch_write(13);
  o_push_ch_full(13) <= ch_IOCore_to_SPU0PE13_full;

  ch_IOCore_to_SPU0PE14_a <= i_push_ch_data(14);
  ch_IOCore_to_SPU0PE14_write  <= i_push_ch_write(14);
  o_push_ch_full(14) <= ch_IOCore_to_SPU0PE14_full;

  ch_IOCore_to_SPU0PE15_a <= i_push_ch_data(15);
  ch_IOCore_to_SPU0PE15_write  <= i_push_ch_write(15);
  o_push_ch_full(15) <= ch_IOCore_to_SPU0PE15_full;

  ch_IOCore_to_SPU0PE16_a <= i_push_ch_data(16);
  ch_IOCore_to_SPU0PE16_write  <= i_push_ch_write(16);
  o_push_ch_full(16) <= ch_IOCore_to_SPU0PE16_full;

  ch_IOCore_to_SPU0PE17_a <= i_push_ch_data(17);
  ch_IOCore_to_SPU0PE17_write  <= i_push_ch_write(17);
  o_push_ch_full(17) <= ch_IOCore_to_SPU0PE17_full;

  ch_IOCore_to_SPU0PE18_a <= i_push_ch_data(18);
  ch_IOCore_to_SPU0PE18_write  <= i_push_ch_write(18);
  o_push_ch_full(18) <= ch_IOCore_to_SPU0PE18_full;

  ch_IOCore_to_SPU0PE19_a <= i_push_ch_data(19);
  ch_IOCore_to_SPU0PE19_write  <= i_push_ch_write(19);
  o_push_ch_full(19) <= ch_IOCore_to_SPU0PE19_full;

  ch_IOCore_to_SPU0PE20_a <= i_push_ch_data(20);
  ch_IOCore_to_SPU0PE20_write  <= i_push_ch_write(20);
  o_push_ch_full(20) <= ch_IOCore_to_SPU0PE20_full;

  ch_IOCore_to_SPU0PE21_a <= i_push_ch_data(21);
  ch_IOCore_to_SPU0PE21_write  <= i_push_ch_write(21);
  o_push_ch_full(21) <= ch_IOCore_to_SPU0PE21_full;

  ch_IOCore_to_SPU0PE22_a <= i_push_ch_data(22);
  ch_IOCore_to_SPU0PE22_write  <= i_push_ch_write(22);
  o_push_ch_full(22) <= ch_IOCore_to_SPU0PE22_full;

  ch_IOCore_to_SPU0PE23_a <= i_push_ch_data(23);
  ch_IOCore_to_SPU0PE23_write  <= i_push_ch_write(23);
  o_push_ch_full(23) <= ch_IOCore_to_SPU0PE23_full;

  ch_IOCore_to_SPU0PE24_a <= i_push_ch_data(24);
  ch_IOCore_to_SPU0PE24_write  <= i_push_ch_write(24);
  o_push_ch_full(24) <= ch_IOCore_to_SPU0PE24_full;

  ch_IOCore_to_SPU0PE25_a <= i_push_ch_data(25);
  ch_IOCore_to_SPU0PE25_write  <= i_push_ch_write(25);
  o_push_ch_full(25) <= ch_IOCore_to_SPU0PE25_full;

  ch_IOCore_to_SPU0PE26_a <= i_push_ch_data(26);
  ch_IOCore_to_SPU0PE26_write  <= i_push_ch_write(26);
  o_push_ch_full(26) <= ch_IOCore_to_SPU0PE26_full;

  ch_IOCore_to_SPU0PE27_a <= i_push_ch_data(27);
  ch_IOCore_to_SPU0PE27_write  <= i_push_ch_write(27);
  o_push_ch_full(27) <= ch_IOCore_to_SPU0PE27_full;

  ch_IOCore_to_SPU0PE28_a <= i_push_ch_data(28);
  ch_IOCore_to_SPU0PE28_write  <= i_push_ch_write(28);
  o_push_ch_full(28) <= ch_IOCore_to_SPU0PE28_full;

  ch_IOCore_to_SPU0PE29_a <= i_push_ch_data(29);
  ch_IOCore_to_SPU0PE29_write  <= i_push_ch_write(29);
  o_push_ch_full(29) <= ch_IOCore_to_SPU0PE29_full;

  ch_IOCore_to_SPU0PE30_a <= i_push_ch_data(30);
  ch_IOCore_to_SPU0PE30_write  <= i_push_ch_write(30);
  o_push_ch_full(30) <= ch_IOCore_to_SPU0PE30_full;

  ch_IOCore_to_SPU0PE31_a <= i_push_ch_data(31);
  ch_IOCore_to_SPU0PE31_write  <= i_push_ch_write(31);
  o_push_ch_full(31) <= ch_IOCore_to_SPU0PE31_full;

  ch_SPU1PE0_to_IOCore_read  <= i_pop_ch_read(0);
  o_pop_ch_data(0) <= ch_SPU1PE0_to_IOCore_b;
  o_pop_ch_empty(0) <= ch_SPU1PE0_to_IOCore_empty;

  -- Connect FIFOs with SPUs
  -- Connect FIFO IOCore_to_SPU0PE0 with PE
  get_ch_data_0(0) <= ch_IOCore_to_SPU0PE0_b;
  get_ch_empty_0(0) <= ch_IOCore_to_SPU0PE0_empty;
  ch_IOCore_to_SPU0PE0_read <= get_ch_read_0(0);

  -- Connect FIFO IOCore_to_SPU0PE1 with PE
  get_ch_data_0(1) <= ch_IOCore_to_SPU0PE1_b;
  get_ch_empty_0(1) <= ch_IOCore_to_SPU0PE1_empty;
  ch_IOCore_to_SPU0PE1_read <= get_ch_read_0(1);

  -- Connect FIFO IOCore_to_SPU0PE2 with PE
  get_ch_data_0(2) <= ch_IOCore_to_SPU0PE2_b;
  get_ch_empty_0(2) <= ch_IOCore_to_SPU0PE2_empty;
  ch_IOCore_to_SPU0PE2_read <= get_ch_read_0(2);

  -- Connect FIFO IOCore_to_SPU0PE3 with PE
  get_ch_data_0(3) <= ch_IOCore_to_SPU0PE3_b;
  get_ch_empty_0(3) <= ch_IOCore_to_SPU0PE3_empty;
  ch_IOCore_to_SPU0PE3_read <= get_ch_read_0(3);

  -- Connect FIFO IOCore_to_SPU0PE4 with PE
  get_ch_data_0(4) <= ch_IOCore_to_SPU0PE4_b;
  get_ch_empty_0(4) <= ch_IOCore_to_SPU0PE4_empty;
  ch_IOCore_to_SPU0PE4_read <= get_ch_read_0(4);

  -- Connect FIFO IOCore_to_SPU0PE5 with PE
  get_ch_data_0(5) <= ch_IOCore_to_SPU0PE5_b;
  get_ch_empty_0(5) <= ch_IOCore_to_SPU0PE5_empty;
  ch_IOCore_to_SPU0PE5_read <= get_ch_read_0(5);

  -- Connect FIFO IOCore_to_SPU0PE6 with PE
  get_ch_data_0(6) <= ch_IOCore_to_SPU0PE6_b;
  get_ch_empty_0(6) <= ch_IOCore_to_SPU0PE6_empty;
  ch_IOCore_to_SPU0PE6_read <= get_ch_read_0(6);

  -- Connect FIFO IOCore_to_SPU0PE7 with PE
  get_ch_data_0(7) <= ch_IOCore_to_SPU0PE7_b;
  get_ch_empty_0(7) <= ch_IOCore_to_SPU0PE7_empty;
  ch_IOCore_to_SPU0PE7_read <= get_ch_read_0(7);

  -- Connect FIFO IOCore_to_SPU0PE8 with PE
  get_ch_data_0(8) <= ch_IOCore_to_SPU0PE8_b;
  get_ch_empty_0(8) <= ch_IOCore_to_SPU0PE8_empty;
  ch_IOCore_to_SPU0PE8_read <= get_ch_read_0(8);

  -- Connect FIFO IOCore_to_SPU0PE9 with PE
  get_ch_data_0(9) <= ch_IOCore_to_SPU0PE9_b;
  get_ch_empty_0(9) <= ch_IOCore_to_SPU0PE9_empty;
  ch_IOCore_to_SPU0PE9_read <= get_ch_read_0(9);

  -- Connect FIFO IOCore_to_SPU0PE10 with PE
  get_ch_data_0(10) <= ch_IOCore_to_SPU0PE10_b;
  get_ch_empty_0(10) <= ch_IOCore_to_SPU0PE10_empty;
  ch_IOCore_to_SPU0PE10_read <= get_ch_read_0(10);

  -- Connect FIFO IOCore_to_SPU0PE11 with PE
  get_ch_data_0(11) <= ch_IOCore_to_SPU0PE11_b;
  get_ch_empty_0(11) <= ch_IOCore_to_SPU0PE11_empty;
  ch_IOCore_to_SPU0PE11_read <= get_ch_read_0(11);

  -- Connect FIFO IOCore_to_SPU0PE12 with PE
  get_ch_data_0(12) <= ch_IOCore_to_SPU0PE12_b;
  get_ch_empty_0(12) <= ch_IOCore_to_SPU0PE12_empty;
  ch_IOCore_to_SPU0PE12_read <= get_ch_read_0(12);

  -- Connect FIFO IOCore_to_SPU0PE13 with PE
  get_ch_data_0(13) <= ch_IOCore_to_SPU0PE13_b;
  get_ch_empty_0(13) <= ch_IOCore_to_SPU0PE13_empty;
  ch_IOCore_to_SPU0PE13_read <= get_ch_read_0(13);

  -- Connect FIFO IOCore_to_SPU0PE14 with PE
  get_ch_data_0(14) <= ch_IOCore_to_SPU0PE14_b;
  get_ch_empty_0(14) <= ch_IOCore_to_SPU0PE14_empty;
  ch_IOCore_to_SPU0PE14_read <= get_ch_read_0(14);

  -- Connect FIFO IOCore_to_SPU0PE15 with PE
  get_ch_data_0(15) <= ch_IOCore_to_SPU0PE15_b;
  get_ch_empty_0(15) <= ch_IOCore_to_SPU0PE15_empty;
  ch_IOCore_to_SPU0PE15_read <= get_ch_read_0(15);

  -- Connect FIFO IOCore_to_SPU0PE16 with PE
  get_ch_data_0(16) <= ch_IOCore_to_SPU0PE16_b;
  get_ch_empty_0(16) <= ch_IOCore_to_SPU0PE16_empty;
  ch_IOCore_to_SPU0PE16_read <= get_ch_read_0(16);

  -- Connect FIFO IOCore_to_SPU0PE17 with PE
  get_ch_data_0(17) <= ch_IOCore_to_SPU0PE17_b;
  get_ch_empty_0(17) <= ch_IOCore_to_SPU0PE17_empty;
  ch_IOCore_to_SPU0PE17_read <= get_ch_read_0(17);

  -- Connect FIFO IOCore_to_SPU0PE18 with PE
  get_ch_data_0(18) <= ch_IOCore_to_SPU0PE18_b;
  get_ch_empty_0(18) <= ch_IOCore_to_SPU0PE18_empty;
  ch_IOCore_to_SPU0PE18_read <= get_ch_read_0(18);

  -- Connect FIFO IOCore_to_SPU0PE19 with PE
  get_ch_data_0(19) <= ch_IOCore_to_SPU0PE19_b;
  get_ch_empty_0(19) <= ch_IOCore_to_SPU0PE19_empty;
  ch_IOCore_to_SPU0PE19_read <= get_ch_read_0(19);

  -- Connect FIFO IOCore_to_SPU0PE20 with PE
  get_ch_data_0(20) <= ch_IOCore_to_SPU0PE20_b;
  get_ch_empty_0(20) <= ch_IOCore_to_SPU0PE20_empty;
  ch_IOCore_to_SPU0PE20_read <= get_ch_read_0(20);

  -- Connect FIFO IOCore_to_SPU0PE21 with PE
  get_ch_data_0(21) <= ch_IOCore_to_SPU0PE21_b;
  get_ch_empty_0(21) <= ch_IOCore_to_SPU0PE21_empty;
  ch_IOCore_to_SPU0PE21_read <= get_ch_read_0(21);

  -- Connect FIFO IOCore_to_SPU0PE22 with PE
  get_ch_data_0(22) <= ch_IOCore_to_SPU0PE22_b;
  get_ch_empty_0(22) <= ch_IOCore_to_SPU0PE22_empty;
  ch_IOCore_to_SPU0PE22_read <= get_ch_read_0(22);

  -- Connect FIFO IOCore_to_SPU0PE23 with PE
  get_ch_data_0(23) <= ch_IOCore_to_SPU0PE23_b;
  get_ch_empty_0(23) <= ch_IOCore_to_SPU0PE23_empty;
  ch_IOCore_to_SPU0PE23_read <= get_ch_read_0(23);

  -- Connect FIFO IOCore_to_SPU0PE24 with PE
  get_ch_data_0(24) <= ch_IOCore_to_SPU0PE24_b;
  get_ch_empty_0(24) <= ch_IOCore_to_SPU0PE24_empty;
  ch_IOCore_to_SPU0PE24_read <= get_ch_read_0(24);

  -- Connect FIFO IOCore_to_SPU0PE25 with PE
  get_ch_data_0(25) <= ch_IOCore_to_SPU0PE25_b;
  get_ch_empty_0(25) <= ch_IOCore_to_SPU0PE25_empty;
  ch_IOCore_to_SPU0PE25_read <= get_ch_read_0(25);

  -- Connect FIFO IOCore_to_SPU0PE26 with PE
  get_ch_data_0(26) <= ch_IOCore_to_SPU0PE26_b;
  get_ch_empty_0(26) <= ch_IOCore_to_SPU0PE26_empty;
  ch_IOCore_to_SPU0PE26_read <= get_ch_read_0(26);

  -- Connect FIFO IOCore_to_SPU0PE27 with PE
  get_ch_data_0(27) <= ch_IOCore_to_SPU0PE27_b;
  get_ch_empty_0(27) <= ch_IOCore_to_SPU0PE27_empty;
  ch_IOCore_to_SPU0PE27_read <= get_ch_read_0(27);

  -- Connect FIFO IOCore_to_SPU0PE28 with PE
  get_ch_data_0(28) <= ch_IOCore_to_SPU0PE28_b;
  get_ch_empty_0(28) <= ch_IOCore_to_SPU0PE28_empty;
  ch_IOCore_to_SPU0PE28_read <= get_ch_read_0(28);

  -- Connect FIFO IOCore_to_SPU0PE29 with PE
  get_ch_data_0(29) <= ch_IOCore_to_SPU0PE29_b;
  get_ch_empty_0(29) <= ch_IOCore_to_SPU0PE29_empty;
  ch_IOCore_to_SPU0PE29_read <= get_ch_read_0(29);

  -- Connect FIFO IOCore_to_SPU0PE30 with PE
  get_ch_data_0(30) <= ch_IOCore_to_SPU0PE30_b;
  get_ch_empty_0(30) <= ch_IOCore_to_SPU0PE30_empty;
  ch_IOCore_to_SPU0PE30_read <= get_ch_read_0(30);

  -- Connect FIFO IOCore_to_SPU0PE31 with PE
  get_ch_data_0(31) <= ch_IOCore_to_SPU0PE31_b;
  get_ch_empty_0(31) <= ch_IOCore_to_SPU0PE31_empty;
  ch_IOCore_to_SPU0PE31_read <= get_ch_read_0(31);

  -- Connect FIFO SPU0PE0_to_SPU1PE0 with PE
  ch_SPU0PE0_to_SPU1PE0_a <= put_ch_data_0(0);
  ch_SPU0PE0_to_SPU1PE0_write <= put_ch_write_0(0);
  put_ch_full_0(0) <= ch_SPU0PE0_to_SPU1PE0_full;

  get_ch_data_1(0) <= ch_SPU0PE0_to_SPU1PE0_b;
  get_ch_empty_1(0) <= ch_SPU0PE0_to_SPU1PE0_empty;
  ch_SPU0PE0_to_SPU1PE0_read <= get_ch_read_1(0);

  -- Connect FIFO SPU0PE1_to_SPU1PE0 with PE
  ch_SPU0PE1_to_SPU1PE0_a <= put_ch_data_0(1);
  ch_SPU0PE1_to_SPU1PE0_write <= put_ch_write_0(1);
  put_ch_full_0(1) <= ch_SPU0PE1_to_SPU1PE0_full;

  get_ch_data_1(1) <= ch_SPU0PE1_to_SPU1PE0_b;
  get_ch_empty_1(1) <= ch_SPU0PE1_to_SPU1PE0_empty;
  ch_SPU0PE1_to_SPU1PE0_read <= get_ch_read_1(1);

  -- Connect FIFO SPU0PE2_to_SPU1PE0 with PE
  ch_SPU0PE2_to_SPU1PE0_a <= put_ch_data_0(2);
  ch_SPU0PE2_to_SPU1PE0_write <= put_ch_write_0(2);
  put_ch_full_0(2) <= ch_SPU0PE2_to_SPU1PE0_full;

  get_ch_data_1(2) <= ch_SPU0PE2_to_SPU1PE0_b;
  get_ch_empty_1(2) <= ch_SPU0PE2_to_SPU1PE0_empty;
  ch_SPU0PE2_to_SPU1PE0_read <= get_ch_read_1(2);

  -- Connect FIFO SPU0PE3_to_SPU1PE0 with PE
  ch_SPU0PE3_to_SPU1PE0_a <= put_ch_data_0(3);
  ch_SPU0PE3_to_SPU1PE0_write <= put_ch_write_0(3);
  put_ch_full_0(3) <= ch_SPU0PE3_to_SPU1PE0_full;

  get_ch_data_1(3) <= ch_SPU0PE3_to_SPU1PE0_b;
  get_ch_empty_1(3) <= ch_SPU0PE3_to_SPU1PE0_empty;
  ch_SPU0PE3_to_SPU1PE0_read <= get_ch_read_1(3);

  -- Connect FIFO SPU0PE4_to_SPU1PE0 with PE
  ch_SPU0PE4_to_SPU1PE0_a <= put_ch_data_0(4);
  ch_SPU0PE4_to_SPU1PE0_write <= put_ch_write_0(4);
  put_ch_full_0(4) <= ch_SPU0PE4_to_SPU1PE0_full;

  get_ch_data_1(4) <= ch_SPU0PE4_to_SPU1PE0_b;
  get_ch_empty_1(4) <= ch_SPU0PE4_to_SPU1PE0_empty;
  ch_SPU0PE4_to_SPU1PE0_read <= get_ch_read_1(4);

  -- Connect FIFO SPU0PE5_to_SPU1PE0 with PE
  ch_SPU0PE5_to_SPU1PE0_a <= put_ch_data_0(5);
  ch_SPU0PE5_to_SPU1PE0_write <= put_ch_write_0(5);
  put_ch_full_0(5) <= ch_SPU0PE5_to_SPU1PE0_full;

  get_ch_data_1(5) <= ch_SPU0PE5_to_SPU1PE0_b;
  get_ch_empty_1(5) <= ch_SPU0PE5_to_SPU1PE0_empty;
  ch_SPU0PE5_to_SPU1PE0_read <= get_ch_read_1(5);

  -- Connect FIFO SPU0PE6_to_SPU1PE0 with PE
  ch_SPU0PE6_to_SPU1PE0_a <= put_ch_data_0(6);
  ch_SPU0PE6_to_SPU1PE0_write <= put_ch_write_0(6);
  put_ch_full_0(6) <= ch_SPU0PE6_to_SPU1PE0_full;

  get_ch_data_1(6) <= ch_SPU0PE6_to_SPU1PE0_b;
  get_ch_empty_1(6) <= ch_SPU0PE6_to_SPU1PE0_empty;
  ch_SPU0PE6_to_SPU1PE0_read <= get_ch_read_1(6);

  -- Connect FIFO SPU0PE7_to_SPU1PE0 with PE
  ch_SPU0PE7_to_SPU1PE0_a <= put_ch_data_0(7);
  ch_SPU0PE7_to_SPU1PE0_write <= put_ch_write_0(7);
  put_ch_full_0(7) <= ch_SPU0PE7_to_SPU1PE0_full;

  get_ch_data_1(7) <= ch_SPU0PE7_to_SPU1PE0_b;
  get_ch_empty_1(7) <= ch_SPU0PE7_to_SPU1PE0_empty;
  ch_SPU0PE7_to_SPU1PE0_read <= get_ch_read_1(7);

  -- Connect FIFO SPU0PE8_to_SPU1PE0 with PE
  ch_SPU0PE8_to_SPU1PE0_a <= put_ch_data_0(8);
  ch_SPU0PE8_to_SPU1PE0_write <= put_ch_write_0(8);
  put_ch_full_0(8) <= ch_SPU0PE8_to_SPU1PE0_full;

  get_ch_data_1(8) <= ch_SPU0PE8_to_SPU1PE0_b;
  get_ch_empty_1(8) <= ch_SPU0PE8_to_SPU1PE0_empty;
  ch_SPU0PE8_to_SPU1PE0_read <= get_ch_read_1(8);

  -- Connect FIFO SPU0PE9_to_SPU1PE0 with PE
  ch_SPU0PE9_to_SPU1PE0_a <= put_ch_data_0(9);
  ch_SPU0PE9_to_SPU1PE0_write <= put_ch_write_0(9);
  put_ch_full_0(9) <= ch_SPU0PE9_to_SPU1PE0_full;

  get_ch_data_1(9) <= ch_SPU0PE9_to_SPU1PE0_b;
  get_ch_empty_1(9) <= ch_SPU0PE9_to_SPU1PE0_empty;
  ch_SPU0PE9_to_SPU1PE0_read <= get_ch_read_1(9);

  -- Connect FIFO SPU0PE10_to_SPU1PE0 with PE
  ch_SPU0PE10_to_SPU1PE0_a <= put_ch_data_0(10);
  ch_SPU0PE10_to_SPU1PE0_write <= put_ch_write_0(10);
  put_ch_full_0(10) <= ch_SPU0PE10_to_SPU1PE0_full;

  get_ch_data_1(10) <= ch_SPU0PE10_to_SPU1PE0_b;
  get_ch_empty_1(10) <= ch_SPU0PE10_to_SPU1PE0_empty;
  ch_SPU0PE10_to_SPU1PE0_read <= get_ch_read_1(10);

  -- Connect FIFO SPU0PE11_to_SPU1PE0 with PE
  ch_SPU0PE11_to_SPU1PE0_a <= put_ch_data_0(11);
  ch_SPU0PE11_to_SPU1PE0_write <= put_ch_write_0(11);
  put_ch_full_0(11) <= ch_SPU0PE11_to_SPU1PE0_full;

  get_ch_data_1(11) <= ch_SPU0PE11_to_SPU1PE0_b;
  get_ch_empty_1(11) <= ch_SPU0PE11_to_SPU1PE0_empty;
  ch_SPU0PE11_to_SPU1PE0_read <= get_ch_read_1(11);

  -- Connect FIFO SPU0PE12_to_SPU1PE0 with PE
  ch_SPU0PE12_to_SPU1PE0_a <= put_ch_data_0(12);
  ch_SPU0PE12_to_SPU1PE0_write <= put_ch_write_0(12);
  put_ch_full_0(12) <= ch_SPU0PE12_to_SPU1PE0_full;

  get_ch_data_1(12) <= ch_SPU0PE12_to_SPU1PE0_b;
  get_ch_empty_1(12) <= ch_SPU0PE12_to_SPU1PE0_empty;
  ch_SPU0PE12_to_SPU1PE0_read <= get_ch_read_1(12);

  -- Connect FIFO SPU0PE13_to_SPU1PE0 with PE
  ch_SPU0PE13_to_SPU1PE0_a <= put_ch_data_0(13);
  ch_SPU0PE13_to_SPU1PE0_write <= put_ch_write_0(13);
  put_ch_full_0(13) <= ch_SPU0PE13_to_SPU1PE0_full;

  get_ch_data_1(13) <= ch_SPU0PE13_to_SPU1PE0_b;
  get_ch_empty_1(13) <= ch_SPU0PE13_to_SPU1PE0_empty;
  ch_SPU0PE13_to_SPU1PE0_read <= get_ch_read_1(13);

  -- Connect FIFO SPU0PE14_to_SPU1PE0 with PE
  ch_SPU0PE14_to_SPU1PE0_a <= put_ch_data_0(14);
  ch_SPU0PE14_to_SPU1PE0_write <= put_ch_write_0(14);
  put_ch_full_0(14) <= ch_SPU0PE14_to_SPU1PE0_full;

  get_ch_data_1(14) <= ch_SPU0PE14_to_SPU1PE0_b;
  get_ch_empty_1(14) <= ch_SPU0PE14_to_SPU1PE0_empty;
  ch_SPU0PE14_to_SPU1PE0_read <= get_ch_read_1(14);

  -- Connect FIFO SPU0PE15_to_SPU1PE0 with PE
  ch_SPU0PE15_to_SPU1PE0_a <= put_ch_data_0(15);
  ch_SPU0PE15_to_SPU1PE0_write <= put_ch_write_0(15);
  put_ch_full_0(15) <= ch_SPU0PE15_to_SPU1PE0_full;

  get_ch_data_1(15) <= ch_SPU0PE15_to_SPU1PE0_b;
  get_ch_empty_1(15) <= ch_SPU0PE15_to_SPU1PE0_empty;
  ch_SPU0PE15_to_SPU1PE0_read <= get_ch_read_1(15);

  -- Connect FIFO SPU0PE16_to_SPU1PE0 with PE
  ch_SPU0PE16_to_SPU1PE0_a <= put_ch_data_0(16);
  ch_SPU0PE16_to_SPU1PE0_write <= put_ch_write_0(16);
  put_ch_full_0(16) <= ch_SPU0PE16_to_SPU1PE0_full;

  get_ch_data_1(16) <= ch_SPU0PE16_to_SPU1PE0_b;
  get_ch_empty_1(16) <= ch_SPU0PE16_to_SPU1PE0_empty;
  ch_SPU0PE16_to_SPU1PE0_read <= get_ch_read_1(16);

  -- Connect FIFO SPU0PE17_to_SPU1PE0 with PE
  ch_SPU0PE17_to_SPU1PE0_a <= put_ch_data_0(17);
  ch_SPU0PE17_to_SPU1PE0_write <= put_ch_write_0(17);
  put_ch_full_0(17) <= ch_SPU0PE17_to_SPU1PE0_full;

  get_ch_data_1(17) <= ch_SPU0PE17_to_SPU1PE0_b;
  get_ch_empty_1(17) <= ch_SPU0PE17_to_SPU1PE0_empty;
  ch_SPU0PE17_to_SPU1PE0_read <= get_ch_read_1(17);

  -- Connect FIFO SPU0PE18_to_SPU1PE0 with PE
  ch_SPU0PE18_to_SPU1PE0_a <= put_ch_data_0(18);
  ch_SPU0PE18_to_SPU1PE0_write <= put_ch_write_0(18);
  put_ch_full_0(18) <= ch_SPU0PE18_to_SPU1PE0_full;

  get_ch_data_1(18) <= ch_SPU0PE18_to_SPU1PE0_b;
  get_ch_empty_1(18) <= ch_SPU0PE18_to_SPU1PE0_empty;
  ch_SPU0PE18_to_SPU1PE0_read <= get_ch_read_1(18);

  -- Connect FIFO SPU0PE19_to_SPU1PE0 with PE
  ch_SPU0PE19_to_SPU1PE0_a <= put_ch_data_0(19);
  ch_SPU0PE19_to_SPU1PE0_write <= put_ch_write_0(19);
  put_ch_full_0(19) <= ch_SPU0PE19_to_SPU1PE0_full;

  get_ch_data_1(19) <= ch_SPU0PE19_to_SPU1PE0_b;
  get_ch_empty_1(19) <= ch_SPU0PE19_to_SPU1PE0_empty;
  ch_SPU0PE19_to_SPU1PE0_read <= get_ch_read_1(19);

  -- Connect FIFO SPU0PE20_to_SPU1PE0 with PE
  ch_SPU0PE20_to_SPU1PE0_a <= put_ch_data_0(20);
  ch_SPU0PE20_to_SPU1PE0_write <= put_ch_write_0(20);
  put_ch_full_0(20) <= ch_SPU0PE20_to_SPU1PE0_full;

  get_ch_data_1(20) <= ch_SPU0PE20_to_SPU1PE0_b;
  get_ch_empty_1(20) <= ch_SPU0PE20_to_SPU1PE0_empty;
  ch_SPU0PE20_to_SPU1PE0_read <= get_ch_read_1(20);

  -- Connect FIFO SPU0PE21_to_SPU1PE0 with PE
  ch_SPU0PE21_to_SPU1PE0_a <= put_ch_data_0(21);
  ch_SPU0PE21_to_SPU1PE0_write <= put_ch_write_0(21);
  put_ch_full_0(21) <= ch_SPU0PE21_to_SPU1PE0_full;

  get_ch_data_1(21) <= ch_SPU0PE21_to_SPU1PE0_b;
  get_ch_empty_1(21) <= ch_SPU0PE21_to_SPU1PE0_empty;
  ch_SPU0PE21_to_SPU1PE0_read <= get_ch_read_1(21);

  -- Connect FIFO SPU0PE22_to_SPU1PE0 with PE
  ch_SPU0PE22_to_SPU1PE0_a <= put_ch_data_0(22);
  ch_SPU0PE22_to_SPU1PE0_write <= put_ch_write_0(22);
  put_ch_full_0(22) <= ch_SPU0PE22_to_SPU1PE0_full;

  get_ch_data_1(22) <= ch_SPU0PE22_to_SPU1PE0_b;
  get_ch_empty_1(22) <= ch_SPU0PE22_to_SPU1PE0_empty;
  ch_SPU0PE22_to_SPU1PE0_read <= get_ch_read_1(22);

  -- Connect FIFO SPU0PE23_to_SPU1PE0 with PE
  ch_SPU0PE23_to_SPU1PE0_a <= put_ch_data_0(23);
  ch_SPU0PE23_to_SPU1PE0_write <= put_ch_write_0(23);
  put_ch_full_0(23) <= ch_SPU0PE23_to_SPU1PE0_full;

  get_ch_data_1(23) <= ch_SPU0PE23_to_SPU1PE0_b;
  get_ch_empty_1(23) <= ch_SPU0PE23_to_SPU1PE0_empty;
  ch_SPU0PE23_to_SPU1PE0_read <= get_ch_read_1(23);

  -- Connect FIFO SPU0PE24_to_SPU1PE0 with PE
  ch_SPU0PE24_to_SPU1PE0_a <= put_ch_data_0(24);
  ch_SPU0PE24_to_SPU1PE0_write <= put_ch_write_0(24);
  put_ch_full_0(24) <= ch_SPU0PE24_to_SPU1PE0_full;

  get_ch_data_1(24) <= ch_SPU0PE24_to_SPU1PE0_b;
  get_ch_empty_1(24) <= ch_SPU0PE24_to_SPU1PE0_empty;
  ch_SPU0PE24_to_SPU1PE0_read <= get_ch_read_1(24);

  -- Connect FIFO SPU0PE25_to_SPU1PE0 with PE
  ch_SPU0PE25_to_SPU1PE0_a <= put_ch_data_0(25);
  ch_SPU0PE25_to_SPU1PE0_write <= put_ch_write_0(25);
  put_ch_full_0(25) <= ch_SPU0PE25_to_SPU1PE0_full;

  get_ch_data_1(25) <= ch_SPU0PE25_to_SPU1PE0_b;
  get_ch_empty_1(25) <= ch_SPU0PE25_to_SPU1PE0_empty;
  ch_SPU0PE25_to_SPU1PE0_read <= get_ch_read_1(25);

  -- Connect FIFO SPU0PE26_to_SPU1PE0 with PE
  ch_SPU0PE26_to_SPU1PE0_a <= put_ch_data_0(26);
  ch_SPU0PE26_to_SPU1PE0_write <= put_ch_write_0(26);
  put_ch_full_0(26) <= ch_SPU0PE26_to_SPU1PE0_full;

  get_ch_data_1(26) <= ch_SPU0PE26_to_SPU1PE0_b;
  get_ch_empty_1(26) <= ch_SPU0PE26_to_SPU1PE0_empty;
  ch_SPU0PE26_to_SPU1PE0_read <= get_ch_read_1(26);

  -- Connect FIFO SPU0PE27_to_SPU1PE0 with PE
  ch_SPU0PE27_to_SPU1PE0_a <= put_ch_data_0(27);
  ch_SPU0PE27_to_SPU1PE0_write <= put_ch_write_0(27);
  put_ch_full_0(27) <= ch_SPU0PE27_to_SPU1PE0_full;

  get_ch_data_1(27) <= ch_SPU0PE27_to_SPU1PE0_b;
  get_ch_empty_1(27) <= ch_SPU0PE27_to_SPU1PE0_empty;
  ch_SPU0PE27_to_SPU1PE0_read <= get_ch_read_1(27);

  -- Connect FIFO SPU0PE28_to_SPU1PE0 with PE
  ch_SPU0PE28_to_SPU1PE0_a <= put_ch_data_0(28);
  ch_SPU0PE28_to_SPU1PE0_write <= put_ch_write_0(28);
  put_ch_full_0(28) <= ch_SPU0PE28_to_SPU1PE0_full;

  get_ch_data_1(28) <= ch_SPU0PE28_to_SPU1PE0_b;
  get_ch_empty_1(28) <= ch_SPU0PE28_to_SPU1PE0_empty;
  ch_SPU0PE28_to_SPU1PE0_read <= get_ch_read_1(28);

  -- Connect FIFO SPU0PE29_to_SPU1PE0 with PE
  ch_SPU0PE29_to_SPU1PE0_a <= put_ch_data_0(29);
  ch_SPU0PE29_to_SPU1PE0_write <= put_ch_write_0(29);
  put_ch_full_0(29) <= ch_SPU0PE29_to_SPU1PE0_full;

  get_ch_data_1(29) <= ch_SPU0PE29_to_SPU1PE0_b;
  get_ch_empty_1(29) <= ch_SPU0PE29_to_SPU1PE0_empty;
  ch_SPU0PE29_to_SPU1PE0_read <= get_ch_read_1(29);

  -- Connect FIFO SPU0PE30_to_SPU1PE0 with PE
  ch_SPU0PE30_to_SPU1PE0_a <= put_ch_data_0(30);
  ch_SPU0PE30_to_SPU1PE0_write <= put_ch_write_0(30);
  put_ch_full_0(30) <= ch_SPU0PE30_to_SPU1PE0_full;

  get_ch_data_1(30) <= ch_SPU0PE30_to_SPU1PE0_b;
  get_ch_empty_1(30) <= ch_SPU0PE30_to_SPU1PE0_empty;
  ch_SPU0PE30_to_SPU1PE0_read <= get_ch_read_1(30);

  -- Connect FIFO SPU0PE31_to_SPU1PE0 with PE
  ch_SPU0PE31_to_SPU1PE0_a <= put_ch_data_0(31);
  ch_SPU0PE31_to_SPU1PE0_write <= put_ch_write_0(31);
  put_ch_full_0(31) <= ch_SPU0PE31_to_SPU1PE0_full;

  get_ch_data_1(31) <= ch_SPU0PE31_to_SPU1PE0_b;
  get_ch_empty_1(31) <= ch_SPU0PE31_to_SPU1PE0_empty;
  ch_SPU0PE31_to_SPU1PE0_read <= get_ch_read_1(31);

  -- Connect FIFO SPU1PE0_to_IOCore with PE
  ch_SPU1PE0_to_IOCore_a <= put_ch_data_1(0);
  ch_SPU1PE0_to_IOCore_write <= put_ch_write_1(0);
  put_ch_full_1(0) <= ch_SPU1PE0_to_IOCore_full;

  -- Instantiate PEs and clock enables
u_core_0: spu_core
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 0,
  BSLAVE          => true,
  BMASTER         => true,
  BMASTER_NUM     => 1,
  VLEN            => 32,
  OPCODE_WIDTH    => 6,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 0,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => true,
  RPT_SPEC_1   => false,
  RPT_LEVELS   => 2,
  RPT_CNT_LEN0 => 6,
  RPT_CNT_LEN1 => 4,
  RPT_CNT_LEN2 => 1,
  RPT_CNT_LEN3 => 1,
  RPT_CNT_LEN4 => 1,
  RPT_BLK_LEN0 => 3,
  RPT_BLK_LEN1 => 4,
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
  ALUSRA_EN    => false,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => true,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 0,
  FLEXB_TYPE   => 2,
  FLEXC_TYPE   => 10,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 0,
  EBITS_B      => 0,
  EBITS_C      => 0,
  EBITS_D      => 0,

  DSP48E_EN    => false,
  
  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 1,
  RX_CH_WIDTH => 1,
  TX_CH_NUM   => 1,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => false,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initSPU0PE",

  PM_SIZE       => 64,
  PM_ADDR_WIDTH => 6,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init0.mif",

  DM_EN                 => true,
  DM_SIZE               => 1008,
  DM_ADDR_WIDTH         => 10,
  DM_DATA_WIDTH         => 8,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU0PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => false,
  DM_RB_M_INITIAL0      => 0,
  DM_RB_M_INITIAL1      => 0,
  DM_RB_N_INITIAL0      => 256,
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
  DM_RB_M_AUTOINC_EN0   => true,
  DM_RB_M_AUTOINC_EN1   => false,
  DM_RB_N_AUTOINC_EN0   => true,
  DM_RB_N_AUTOINC_EN1   => false,
  DM_WB_AUTOINC_EN0     => true,
  DM_WB_AUTOINC_EN1     => false,
  DM_RB_M_INC_EN0       => true,
  DM_RB_M_INC_EN1       => false,
  DM_RB_N_INC_EN0       => true,
  DM_RB_N_INC_EN1       => false,
  DM_WB_INC_EN0         => true,
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
  o_ext_barrier => barrier_SPU0_IOCore,
  i_ext_barrier => barrier_SPU1_SPU0,
  o_ext_en_spu => enspu_SPU0_SPU1,

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
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 0,
  BSLAVE          => false,
  BMASTER         => true,
  BMASTER_NUM     => 2,
  VLEN            => 1,
  OPCODE_WIDTH    => 6,

  -- Control Pipeline
  MULREG_EN  => true,
  PB0_DEPTH  => 0,
  PB1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
  JMP_EN        => true,

  RPT_EN       => true,
  RPT_SPEC_1   => false,
  RPT_LEVELS   => 2,
  RPT_CNT_LEN0 => 5,
  RPT_CNT_LEN1 => 5,
  RPT_CNT_LEN2 => 1,
  RPT_CNT_LEN3 => 1,
  RPT_CNT_LEN4 => 1,
  RPT_BLK_LEN0 => 4,
  RPT_BLK_LEN1 => 3,
  RPT_BLK_LEN2 => 1,
  RPT_BLK_LEN3 => 1,
  RPT_BLK_LEN4 => 1,

  -- Control Supported Instructions
  MASK_EN      => true,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  MASKGE_EN    => true,
  MASKLE_EN    => false,
  MASKNE_EN    => false,
  ALUSRA_EN    => false,
  ALUSRA_VAL   => 1,
  ABSDIFF_EN   => false,
  ABSDIFF_WITHACCUM => true,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 1,
  FLEXC_TYPE   => 9,

  DIRECT_WB_EN => true,
  FLEXB_IMM_VAL=> -1,

  EBITS_A      => 0,
  EBITS_B      => 0,
  EBITS_C      => 0,
  EBITS_D      => 0,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => true,
  PUTCH_EN    => false,
  RX_CH_NUM   => 32,
  RX_CH_WIDTH => 5,
  TX_CH_NUM   => 1,
  TX_CH_WIDTH => 1,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => true,
  RF_INIT_FILE  => "RFInit/rf_initSPU1PE",

  PM_SIZE       => 32,
  PM_ADDR_WIDTH => 5,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init1.mif",

  DM_EN                 => false,
  DM_SIZE               => 32,
  DM_ADDR_WIDTH         => 5,
  DM_DATA_WIDTH         => 8,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU1PE",
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

  i_ext_en_spu => enspu_SPU1,
  o_ext_barrier => barrier_SPU1,
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


  -- Instantiate FIFOs
u_fifo_IOCore_to_SPU0PE0: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE0_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE0_write,
  o_full  => ch_IOCore_to_SPU0PE0_full,

  o_data  => ch_IOCore_to_SPU0PE0_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE0_read,
  o_empty => ch_IOCore_to_SPU0PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE1_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE1_write,
  o_full  => ch_IOCore_to_SPU0PE1_full,

  o_data  => ch_IOCore_to_SPU0PE1_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE1_read,
  o_empty => ch_IOCore_to_SPU0PE1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE2: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE2_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE2_write,
  o_full  => ch_IOCore_to_SPU0PE2_full,

  o_data  => ch_IOCore_to_SPU0PE2_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE2_read,
  o_empty => ch_IOCore_to_SPU0PE2_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE3: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE3_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE3_write,
  o_full  => ch_IOCore_to_SPU0PE3_full,

  o_data  => ch_IOCore_to_SPU0PE3_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE3_read,
  o_empty => ch_IOCore_to_SPU0PE3_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE4: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE4_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE4_write,
  o_full  => ch_IOCore_to_SPU0PE4_full,

  o_data  => ch_IOCore_to_SPU0PE4_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE4_read,
  o_empty => ch_IOCore_to_SPU0PE4_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE5: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE5_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE5_write,
  o_full  => ch_IOCore_to_SPU0PE5_full,

  o_data  => ch_IOCore_to_SPU0PE5_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE5_read,
  o_empty => ch_IOCore_to_SPU0PE5_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE6: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE6_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE6_write,
  o_full  => ch_IOCore_to_SPU0PE6_full,

  o_data  => ch_IOCore_to_SPU0PE6_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE6_read,
  o_empty => ch_IOCore_to_SPU0PE6_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE7: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE7_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE7_write,
  o_full  => ch_IOCore_to_SPU0PE7_full,

  o_data  => ch_IOCore_to_SPU0PE7_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE7_read,
  o_empty => ch_IOCore_to_SPU0PE7_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE8: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE8_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE8_write,
  o_full  => ch_IOCore_to_SPU0PE8_full,

  o_data  => ch_IOCore_to_SPU0PE8_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE8_read,
  o_empty => ch_IOCore_to_SPU0PE8_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE9: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE9_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE9_write,
  o_full  => ch_IOCore_to_SPU0PE9_full,

  o_data  => ch_IOCore_to_SPU0PE9_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE9_read,
  o_empty => ch_IOCore_to_SPU0PE9_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE10: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE10_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE10_write,
  o_full  => ch_IOCore_to_SPU0PE10_full,

  o_data  => ch_IOCore_to_SPU0PE10_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE10_read,
  o_empty => ch_IOCore_to_SPU0PE10_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE11: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE11_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE11_write,
  o_full  => ch_IOCore_to_SPU0PE11_full,

  o_data  => ch_IOCore_to_SPU0PE11_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE11_read,
  o_empty => ch_IOCore_to_SPU0PE11_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE12: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE12_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE12_write,
  o_full  => ch_IOCore_to_SPU0PE12_full,

  o_data  => ch_IOCore_to_SPU0PE12_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE12_read,
  o_empty => ch_IOCore_to_SPU0PE12_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE13: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE13_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE13_write,
  o_full  => ch_IOCore_to_SPU0PE13_full,

  o_data  => ch_IOCore_to_SPU0PE13_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE13_read,
  o_empty => ch_IOCore_to_SPU0PE13_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE14: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE14_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE14_write,
  o_full  => ch_IOCore_to_SPU0PE14_full,

  o_data  => ch_IOCore_to_SPU0PE14_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE14_read,
  o_empty => ch_IOCore_to_SPU0PE14_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE15: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE15_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE15_write,
  o_full  => ch_IOCore_to_SPU0PE15_full,

  o_data  => ch_IOCore_to_SPU0PE15_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE15_read,
  o_empty => ch_IOCore_to_SPU0PE15_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE16: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE16_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE16_write,
  o_full  => ch_IOCore_to_SPU0PE16_full,

  o_data  => ch_IOCore_to_SPU0PE16_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE16_read,
  o_empty => ch_IOCore_to_SPU0PE16_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE17: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE17_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE17_write,
  o_full  => ch_IOCore_to_SPU0PE17_full,

  o_data  => ch_IOCore_to_SPU0PE17_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE17_read,
  o_empty => ch_IOCore_to_SPU0PE17_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE18: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE18_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE18_write,
  o_full  => ch_IOCore_to_SPU0PE18_full,

  o_data  => ch_IOCore_to_SPU0PE18_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE18_read,
  o_empty => ch_IOCore_to_SPU0PE18_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE19: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE19_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE19_write,
  o_full  => ch_IOCore_to_SPU0PE19_full,

  o_data  => ch_IOCore_to_SPU0PE19_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE19_read,
  o_empty => ch_IOCore_to_SPU0PE19_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE20: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE20_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE20_write,
  o_full  => ch_IOCore_to_SPU0PE20_full,

  o_data  => ch_IOCore_to_SPU0PE20_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE20_read,
  o_empty => ch_IOCore_to_SPU0PE20_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE21: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE21_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE21_write,
  o_full  => ch_IOCore_to_SPU0PE21_full,

  o_data  => ch_IOCore_to_SPU0PE21_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE21_read,
  o_empty => ch_IOCore_to_SPU0PE21_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE22: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE22_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE22_write,
  o_full  => ch_IOCore_to_SPU0PE22_full,

  o_data  => ch_IOCore_to_SPU0PE22_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE22_read,
  o_empty => ch_IOCore_to_SPU0PE22_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE23: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE23_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE23_write,
  o_full  => ch_IOCore_to_SPU0PE23_full,

  o_data  => ch_IOCore_to_SPU0PE23_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE23_read,
  o_empty => ch_IOCore_to_SPU0PE23_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE24: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE24_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE24_write,
  o_full  => ch_IOCore_to_SPU0PE24_full,

  o_data  => ch_IOCore_to_SPU0PE24_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE24_read,
  o_empty => ch_IOCore_to_SPU0PE24_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE25: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE25_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE25_write,
  o_full  => ch_IOCore_to_SPU0PE25_full,

  o_data  => ch_IOCore_to_SPU0PE25_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE25_read,
  o_empty => ch_IOCore_to_SPU0PE25_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE26: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE26_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE26_write,
  o_full  => ch_IOCore_to_SPU0PE26_full,

  o_data  => ch_IOCore_to_SPU0PE26_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE26_read,
  o_empty => ch_IOCore_to_SPU0PE26_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE27: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE27_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE27_write,
  o_full  => ch_IOCore_to_SPU0PE27_full,

  o_data  => ch_IOCore_to_SPU0PE27_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE27_read,
  o_empty => ch_IOCore_to_SPU0PE27_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE28: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE28_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE28_write,
  o_full  => ch_IOCore_to_SPU0PE28_full,

  o_data  => ch_IOCore_to_SPU0PE28_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE28_read,
  o_empty => ch_IOCore_to_SPU0PE28_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE29: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE29_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE29_write,
  o_full  => ch_IOCore_to_SPU0PE29_full,

  o_data  => ch_IOCore_to_SPU0PE29_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE29_read,
  o_empty => ch_IOCore_to_SPU0PE29_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE30: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE30_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE30_write,
  o_full  => ch_IOCore_to_SPU0PE30_full,

  o_data  => ch_IOCore_to_SPU0PE30_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE30_read,
  o_empty => ch_IOCore_to_SPU0PE30_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE31: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>1024 )
port map(
  i_data  => ch_IOCore_to_SPU0PE31_a(INPUT_WIDTH-1 downto 0),
  write   => ch_IOCore_to_SPU0PE31_write,
  o_full  => ch_IOCore_to_SPU0PE31_full,

  o_data  => ch_IOCore_to_SPU0PE31_b(INPUT_WIDTH-1 downto 0),
  read    => ch_IOCore_to_SPU0PE31_read,
  o_empty => ch_IOCore_to_SPU0PE31_empty,
  clk     => clk
);

u_fifo_SPU0PE0_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE0_to_SPU1PE0_a,
  write   => ch_SPU0PE0_to_SPU1PE0_write,
  o_full  => ch_SPU0PE0_to_SPU1PE0_full,

  o_data  => ch_SPU0PE0_to_SPU1PE0_b,
  read    => ch_SPU0PE0_to_SPU1PE0_read,
  o_empty => ch_SPU0PE0_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE1_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE1_to_SPU1PE0_a,
  write   => ch_SPU0PE1_to_SPU1PE0_write,
  o_full  => ch_SPU0PE1_to_SPU1PE0_full,

  o_data  => ch_SPU0PE1_to_SPU1PE0_b,
  read    => ch_SPU0PE1_to_SPU1PE0_read,
  o_empty => ch_SPU0PE1_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE2_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE2_to_SPU1PE0_a,
  write   => ch_SPU0PE2_to_SPU1PE0_write,
  o_full  => ch_SPU0PE2_to_SPU1PE0_full,

  o_data  => ch_SPU0PE2_to_SPU1PE0_b,
  read    => ch_SPU0PE2_to_SPU1PE0_read,
  o_empty => ch_SPU0PE2_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE3_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE3_to_SPU1PE0_a,
  write   => ch_SPU0PE3_to_SPU1PE0_write,
  o_full  => ch_SPU0PE3_to_SPU1PE0_full,

  o_data  => ch_SPU0PE3_to_SPU1PE0_b,
  read    => ch_SPU0PE3_to_SPU1PE0_read,
  o_empty => ch_SPU0PE3_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE4_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE4_to_SPU1PE0_a,
  write   => ch_SPU0PE4_to_SPU1PE0_write,
  o_full  => ch_SPU0PE4_to_SPU1PE0_full,

  o_data  => ch_SPU0PE4_to_SPU1PE0_b,
  read    => ch_SPU0PE4_to_SPU1PE0_read,
  o_empty => ch_SPU0PE4_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE5_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE5_to_SPU1PE0_a,
  write   => ch_SPU0PE5_to_SPU1PE0_write,
  o_full  => ch_SPU0PE5_to_SPU1PE0_full,

  o_data  => ch_SPU0PE5_to_SPU1PE0_b,
  read    => ch_SPU0PE5_to_SPU1PE0_read,
  o_empty => ch_SPU0PE5_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE6_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE6_to_SPU1PE0_a,
  write   => ch_SPU0PE6_to_SPU1PE0_write,
  o_full  => ch_SPU0PE6_to_SPU1PE0_full,

  o_data  => ch_SPU0PE6_to_SPU1PE0_b,
  read    => ch_SPU0PE6_to_SPU1PE0_read,
  o_empty => ch_SPU0PE6_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE7_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE7_to_SPU1PE0_a,
  write   => ch_SPU0PE7_to_SPU1PE0_write,
  o_full  => ch_SPU0PE7_to_SPU1PE0_full,

  o_data  => ch_SPU0PE7_to_SPU1PE0_b,
  read    => ch_SPU0PE7_to_SPU1PE0_read,
  o_empty => ch_SPU0PE7_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE8_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE8_to_SPU1PE0_a,
  write   => ch_SPU0PE8_to_SPU1PE0_write,
  o_full  => ch_SPU0PE8_to_SPU1PE0_full,

  o_data  => ch_SPU0PE8_to_SPU1PE0_b,
  read    => ch_SPU0PE8_to_SPU1PE0_read,
  o_empty => ch_SPU0PE8_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE9_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE9_to_SPU1PE0_a,
  write   => ch_SPU0PE9_to_SPU1PE0_write,
  o_full  => ch_SPU0PE9_to_SPU1PE0_full,

  o_data  => ch_SPU0PE9_to_SPU1PE0_b,
  read    => ch_SPU0PE9_to_SPU1PE0_read,
  o_empty => ch_SPU0PE9_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE10_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE10_to_SPU1PE0_a,
  write   => ch_SPU0PE10_to_SPU1PE0_write,
  o_full  => ch_SPU0PE10_to_SPU1PE0_full,

  o_data  => ch_SPU0PE10_to_SPU1PE0_b,
  read    => ch_SPU0PE10_to_SPU1PE0_read,
  o_empty => ch_SPU0PE10_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE11_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE11_to_SPU1PE0_a,
  write   => ch_SPU0PE11_to_SPU1PE0_write,
  o_full  => ch_SPU0PE11_to_SPU1PE0_full,

  o_data  => ch_SPU0PE11_to_SPU1PE0_b,
  read    => ch_SPU0PE11_to_SPU1PE0_read,
  o_empty => ch_SPU0PE11_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE12_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE12_to_SPU1PE0_a,
  write   => ch_SPU0PE12_to_SPU1PE0_write,
  o_full  => ch_SPU0PE12_to_SPU1PE0_full,

  o_data  => ch_SPU0PE12_to_SPU1PE0_b,
  read    => ch_SPU0PE12_to_SPU1PE0_read,
  o_empty => ch_SPU0PE12_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE13_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE13_to_SPU1PE0_a,
  write   => ch_SPU0PE13_to_SPU1PE0_write,
  o_full  => ch_SPU0PE13_to_SPU1PE0_full,

  o_data  => ch_SPU0PE13_to_SPU1PE0_b,
  read    => ch_SPU0PE13_to_SPU1PE0_read,
  o_empty => ch_SPU0PE13_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE14_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE14_to_SPU1PE0_a,
  write   => ch_SPU0PE14_to_SPU1PE0_write,
  o_full  => ch_SPU0PE14_to_SPU1PE0_full,

  o_data  => ch_SPU0PE14_to_SPU1PE0_b,
  read    => ch_SPU0PE14_to_SPU1PE0_read,
  o_empty => ch_SPU0PE14_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE15_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE15_to_SPU1PE0_a,
  write   => ch_SPU0PE15_to_SPU1PE0_write,
  o_full  => ch_SPU0PE15_to_SPU1PE0_full,

  o_data  => ch_SPU0PE15_to_SPU1PE0_b,
  read    => ch_SPU0PE15_to_SPU1PE0_read,
  o_empty => ch_SPU0PE15_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE16_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE16_to_SPU1PE0_a,
  write   => ch_SPU0PE16_to_SPU1PE0_write,
  o_full  => ch_SPU0PE16_to_SPU1PE0_full,

  o_data  => ch_SPU0PE16_to_SPU1PE0_b,
  read    => ch_SPU0PE16_to_SPU1PE0_read,
  o_empty => ch_SPU0PE16_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE17_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE17_to_SPU1PE0_a,
  write   => ch_SPU0PE17_to_SPU1PE0_write,
  o_full  => ch_SPU0PE17_to_SPU1PE0_full,

  o_data  => ch_SPU0PE17_to_SPU1PE0_b,
  read    => ch_SPU0PE17_to_SPU1PE0_read,
  o_empty => ch_SPU0PE17_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE18_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE18_to_SPU1PE0_a,
  write   => ch_SPU0PE18_to_SPU1PE0_write,
  o_full  => ch_SPU0PE18_to_SPU1PE0_full,

  o_data  => ch_SPU0PE18_to_SPU1PE0_b,
  read    => ch_SPU0PE18_to_SPU1PE0_read,
  o_empty => ch_SPU0PE18_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE19_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE19_to_SPU1PE0_a,
  write   => ch_SPU0PE19_to_SPU1PE0_write,
  o_full  => ch_SPU0PE19_to_SPU1PE0_full,

  o_data  => ch_SPU0PE19_to_SPU1PE0_b,
  read    => ch_SPU0PE19_to_SPU1PE0_read,
  o_empty => ch_SPU0PE19_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE20_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE20_to_SPU1PE0_a,
  write   => ch_SPU0PE20_to_SPU1PE0_write,
  o_full  => ch_SPU0PE20_to_SPU1PE0_full,

  o_data  => ch_SPU0PE20_to_SPU1PE0_b,
  read    => ch_SPU0PE20_to_SPU1PE0_read,
  o_empty => ch_SPU0PE20_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE21_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE21_to_SPU1PE0_a,
  write   => ch_SPU0PE21_to_SPU1PE0_write,
  o_full  => ch_SPU0PE21_to_SPU1PE0_full,

  o_data  => ch_SPU0PE21_to_SPU1PE0_b,
  read    => ch_SPU0PE21_to_SPU1PE0_read,
  o_empty => ch_SPU0PE21_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE22_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE22_to_SPU1PE0_a,
  write   => ch_SPU0PE22_to_SPU1PE0_write,
  o_full  => ch_SPU0PE22_to_SPU1PE0_full,

  o_data  => ch_SPU0PE22_to_SPU1PE0_b,
  read    => ch_SPU0PE22_to_SPU1PE0_read,
  o_empty => ch_SPU0PE22_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE23_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE23_to_SPU1PE0_a,
  write   => ch_SPU0PE23_to_SPU1PE0_write,
  o_full  => ch_SPU0PE23_to_SPU1PE0_full,

  o_data  => ch_SPU0PE23_to_SPU1PE0_b,
  read    => ch_SPU0PE23_to_SPU1PE0_read,
  o_empty => ch_SPU0PE23_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE24_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE24_to_SPU1PE0_a,
  write   => ch_SPU0PE24_to_SPU1PE0_write,
  o_full  => ch_SPU0PE24_to_SPU1PE0_full,

  o_data  => ch_SPU0PE24_to_SPU1PE0_b,
  read    => ch_SPU0PE24_to_SPU1PE0_read,
  o_empty => ch_SPU0PE24_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE25_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE25_to_SPU1PE0_a,
  write   => ch_SPU0PE25_to_SPU1PE0_write,
  o_full  => ch_SPU0PE25_to_SPU1PE0_full,

  o_data  => ch_SPU0PE25_to_SPU1PE0_b,
  read    => ch_SPU0PE25_to_SPU1PE0_read,
  o_empty => ch_SPU0PE25_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE26_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE26_to_SPU1PE0_a,
  write   => ch_SPU0PE26_to_SPU1PE0_write,
  o_full  => ch_SPU0PE26_to_SPU1PE0_full,

  o_data  => ch_SPU0PE26_to_SPU1PE0_b,
  read    => ch_SPU0PE26_to_SPU1PE0_read,
  o_empty => ch_SPU0PE26_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE27_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE27_to_SPU1PE0_a,
  write   => ch_SPU0PE27_to_SPU1PE0_write,
  o_full  => ch_SPU0PE27_to_SPU1PE0_full,

  o_data  => ch_SPU0PE27_to_SPU1PE0_b,
  read    => ch_SPU0PE27_to_SPU1PE0_read,
  o_empty => ch_SPU0PE27_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE28_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE28_to_SPU1PE0_a,
  write   => ch_SPU0PE28_to_SPU1PE0_write,
  o_full  => ch_SPU0PE28_to_SPU1PE0_full,

  o_data  => ch_SPU0PE28_to_SPU1PE0_b,
  read    => ch_SPU0PE28_to_SPU1PE0_read,
  o_empty => ch_SPU0PE28_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE29_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE29_to_SPU1PE0_a,
  write   => ch_SPU0PE29_to_SPU1PE0_write,
  o_full  => ch_SPU0PE29_to_SPU1PE0_full,

  o_data  => ch_SPU0PE29_to_SPU1PE0_b,
  read    => ch_SPU0PE29_to_SPU1PE0_read,
  o_empty => ch_SPU0PE29_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE30_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE30_to_SPU1PE0_a,
  write   => ch_SPU0PE30_to_SPU1PE0_write,
  o_full  => ch_SPU0PE30_to_SPU1PE0_full,

  o_data  => ch_SPU0PE30_to_SPU1PE0_b,
  read    => ch_SPU0PE30_to_SPU1PE0_read,
  o_empty => ch_SPU0PE30_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU0PE31_to_SPU1PE0: fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>1 )
port map(
  i_data  => ch_SPU0PE31_to_SPU1PE0_a,
  write   => ch_SPU0PE31_to_SPU1PE0_write,
  o_full  => ch_SPU0PE31_to_SPU1PE0_full,

  o_data  => ch_SPU0PE31_to_SPU1PE0_b,
  read    => ch_SPU0PE31_to_SPU1PE0_read,
  o_empty => ch_SPU0PE31_to_SPU1PE0_empty,
  clk     => clk
);

u_fifo_SPU1PE0_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>2 )
port map(
  i_data  => ch_SPU1PE0_to_IOCore_a,
  write   => ch_SPU1PE0_to_IOCore_write,
  o_full  => ch_SPU1PE0_to_IOCore_full,

  o_data  => ch_SPU1PE0_to_IOCore_b,
  read    => ch_SPU1PE0_to_IOCore_read,
  o_empty => ch_SPU1PE0_to_IOCore_empty,
  clk     => clk
);

end Structure;
