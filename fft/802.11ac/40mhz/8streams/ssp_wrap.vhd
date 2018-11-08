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
      EXIN_FIFO_NUM  : integer := 16;
      EXOUT_FIFO_NUM : integer := 8;
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
  signal ch_IOCore_to_SPU0PE1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_write : std_logic;
  signal ch_IOCore_to_SPU0PE1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE1_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE1_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE1_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE1_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE1_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE2_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_write : std_logic;
  signal ch_IOCore_to_SPU0PE2_full  : std_logic;
  signal ch_IOCore_to_SPU0PE2_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_read  : std_logic;
  signal ch_IOCore_to_SPU0PE2_empty : std_logic;
  signal ch_IOCore_to_SPU0PE2_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE2_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE2_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE2_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE2_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE3_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_write : std_logic;
  signal ch_IOCore_to_SPU0PE3_full  : std_logic;
  signal ch_IOCore_to_SPU0PE3_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_read  : std_logic;
  signal ch_IOCore_to_SPU0PE3_empty : std_logic;
  signal ch_IOCore_to_SPU0PE3_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE3_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE3_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE3_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE3_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE4_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_write : std_logic;
  signal ch_IOCore_to_SPU0PE4_full  : std_logic;
  signal ch_IOCore_to_SPU0PE4_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_read  : std_logic;
  signal ch_IOCore_to_SPU0PE4_empty : std_logic;
  signal ch_IOCore_to_SPU0PE4_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE4_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE4_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE4_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE4_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE5_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_write : std_logic;
  signal ch_IOCore_to_SPU0PE5_full  : std_logic;
  signal ch_IOCore_to_SPU0PE5_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_read  : std_logic;
  signal ch_IOCore_to_SPU0PE5_empty : std_logic;
  signal ch_IOCore_to_SPU0PE5_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE5_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE5_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE5_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE5_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE6_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_write : std_logic;
  signal ch_IOCore_to_SPU0PE6_full  : std_logic;
  signal ch_IOCore_to_SPU0PE6_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_read  : std_logic;
  signal ch_IOCore_to_SPU0PE6_empty : std_logic;
  signal ch_IOCore_to_SPU0PE6_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE6_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE6_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE6_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE6_1_empty : std_logic;
  signal ch_IOCore_to_SPU0PE7_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_write : std_logic;
  signal ch_IOCore_to_SPU0PE7_full  : std_logic;
  signal ch_IOCore_to_SPU0PE7_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_read  : std_logic;
  signal ch_IOCore_to_SPU0PE7_empty : std_logic;
  signal ch_IOCore_to_SPU0PE7_1_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_1_write : std_logic;
  signal ch_IOCore_to_SPU0PE7_1_full  : std_logic;
  signal ch_IOCore_to_SPU0PE7_1_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_SPU0PE7_1_read  : std_logic;
  signal ch_IOCore_to_SPU0PE7_1_empty : std_logic;
  signal ch_SPU0PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_IOCore_write : std_logic;
  signal ch_SPU0PE0_to_IOCore_full  : std_logic;
  signal ch_SPU0PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE0_to_IOCore_read  : std_logic;
  signal ch_SPU0PE0_to_IOCore_empty : std_logic;
  signal ch_SPU0PE1_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE1_to_IOCore_write : std_logic;
  signal ch_SPU0PE1_to_IOCore_full  : std_logic;
  signal ch_SPU0PE1_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE1_to_IOCore_read  : std_logic;
  signal ch_SPU0PE1_to_IOCore_empty : std_logic;
  signal ch_SPU0PE2_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE2_to_IOCore_write : std_logic;
  signal ch_SPU0PE2_to_IOCore_full  : std_logic;
  signal ch_SPU0PE2_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE2_to_IOCore_read  : std_logic;
  signal ch_SPU0PE2_to_IOCore_empty : std_logic;
  signal ch_SPU0PE3_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE3_to_IOCore_write : std_logic;
  signal ch_SPU0PE3_to_IOCore_full  : std_logic;
  signal ch_SPU0PE3_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE3_to_IOCore_read  : std_logic;
  signal ch_SPU0PE3_to_IOCore_empty : std_logic;
  signal ch_SPU0PE4_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE4_to_IOCore_write : std_logic;
  signal ch_SPU0PE4_to_IOCore_full  : std_logic;
  signal ch_SPU0PE4_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE4_to_IOCore_read  : std_logic;
  signal ch_SPU0PE4_to_IOCore_empty : std_logic;
  signal ch_SPU0PE5_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE5_to_IOCore_write : std_logic;
  signal ch_SPU0PE5_to_IOCore_full  : std_logic;
  signal ch_SPU0PE5_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE5_to_IOCore_read  : std_logic;
  signal ch_SPU0PE5_to_IOCore_empty : std_logic;
  signal ch_SPU0PE6_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE6_to_IOCore_write : std_logic;
  signal ch_SPU0PE6_to_IOCore_full  : std_logic;
  signal ch_SPU0PE6_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE6_to_IOCore_read  : std_logic;
  signal ch_SPU0PE6_to_IOCore_empty : std_logic;
  signal ch_SPU0PE7_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE7_to_IOCore_write : std_logic;
  signal ch_SPU0PE7_to_IOCore_full  : std_logic;
  signal ch_SPU0PE7_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_SPU0PE7_to_IOCore_read  : std_logic;
  signal ch_SPU0PE7_to_IOCore_empty : std_logic;
  -- SPU signals
  signal get_ch_data_0  : VDATA_TYPE(15 downto 0);
  signal get_ch_read_0  : VSIG_TYPE(15 downto 0);
  signal get_ch_empty_0 : VSIG_TYPE(15 downto 0);
  signal put_ch_data_0  : VDATA_TYPE(7 downto 0);
  signal put_ch_write_0 : VSIG_TYPE(7 downto 0);
  signal put_ch_full_0  : VSIG_TYPE(7 downto 0);

begin

  -- Connect signals with module ports
  o_barrier <= barrier(0);

  ch_IOCore_to_SPU0PE0_a <= i_push_ch_data(0);
  ch_IOCore_to_SPU0PE0_write  <= i_push_ch_write(0);
  o_push_ch_full(0) <= ch_IOCore_to_SPU0PE0_full;

  ch_IOCore_to_SPU0PE0_1_a <= i_push_ch_data(1);
  ch_IOCore_to_SPU0PE0_1_write  <= i_push_ch_write(1);
  o_push_ch_full(1) <= ch_IOCore_to_SPU0PE0_1_full;

  ch_IOCore_to_SPU0PE1_a <= i_push_ch_data(2);
  ch_IOCore_to_SPU0PE1_write  <= i_push_ch_write(2);
  o_push_ch_full(2) <= ch_IOCore_to_SPU0PE1_full;

  ch_IOCore_to_SPU0PE1_1_a <= i_push_ch_data(3);
  ch_IOCore_to_SPU0PE1_1_write  <= i_push_ch_write(3);
  o_push_ch_full(3) <= ch_IOCore_to_SPU0PE1_1_full;

  ch_IOCore_to_SPU0PE2_a <= i_push_ch_data(4);
  ch_IOCore_to_SPU0PE2_write  <= i_push_ch_write(4);
  o_push_ch_full(4) <= ch_IOCore_to_SPU0PE2_full;

  ch_IOCore_to_SPU0PE2_1_a <= i_push_ch_data(5);
  ch_IOCore_to_SPU0PE2_1_write  <= i_push_ch_write(5);
  o_push_ch_full(5) <= ch_IOCore_to_SPU0PE2_1_full;

  ch_IOCore_to_SPU0PE3_a <= i_push_ch_data(6);
  ch_IOCore_to_SPU0PE3_write  <= i_push_ch_write(6);
  o_push_ch_full(6) <= ch_IOCore_to_SPU0PE3_full;

  ch_IOCore_to_SPU0PE3_1_a <= i_push_ch_data(7);
  ch_IOCore_to_SPU0PE3_1_write  <= i_push_ch_write(7);
  o_push_ch_full(7) <= ch_IOCore_to_SPU0PE3_1_full;

  ch_IOCore_to_SPU0PE4_a <= i_push_ch_data(8);
  ch_IOCore_to_SPU0PE4_write  <= i_push_ch_write(8);
  o_push_ch_full(8) <= ch_IOCore_to_SPU0PE4_full;

  ch_IOCore_to_SPU0PE4_1_a <= i_push_ch_data(9);
  ch_IOCore_to_SPU0PE4_1_write  <= i_push_ch_write(9);
  o_push_ch_full(9) <= ch_IOCore_to_SPU0PE4_1_full;

  ch_IOCore_to_SPU0PE5_a <= i_push_ch_data(10);
  ch_IOCore_to_SPU0PE5_write  <= i_push_ch_write(10);
  o_push_ch_full(10) <= ch_IOCore_to_SPU0PE5_full;

  ch_IOCore_to_SPU0PE5_1_a <= i_push_ch_data(11);
  ch_IOCore_to_SPU0PE5_1_write  <= i_push_ch_write(11);
  o_push_ch_full(11) <= ch_IOCore_to_SPU0PE5_1_full;

  ch_IOCore_to_SPU0PE6_a <= i_push_ch_data(12);
  ch_IOCore_to_SPU0PE6_write  <= i_push_ch_write(12);
  o_push_ch_full(12) <= ch_IOCore_to_SPU0PE6_full;

  ch_IOCore_to_SPU0PE6_1_a <= i_push_ch_data(13);
  ch_IOCore_to_SPU0PE6_1_write  <= i_push_ch_write(13);
  o_push_ch_full(13) <= ch_IOCore_to_SPU0PE6_1_full;

  ch_IOCore_to_SPU0PE7_a <= i_push_ch_data(14);
  ch_IOCore_to_SPU0PE7_write  <= i_push_ch_write(14);
  o_push_ch_full(14) <= ch_IOCore_to_SPU0PE7_full;

  ch_IOCore_to_SPU0PE7_1_a <= i_push_ch_data(15);
  ch_IOCore_to_SPU0PE7_1_write  <= i_push_ch_write(15);
  o_push_ch_full(15) <= ch_IOCore_to_SPU0PE7_1_full;

  ch_SPU0PE0_to_IOCore_read  <= i_pop_ch_read(0);
  o_pop_ch_data(0) <= ch_SPU0PE0_to_IOCore_b;
  o_pop_ch_empty(0) <= ch_SPU0PE0_to_IOCore_empty;

  ch_SPU0PE1_to_IOCore_read  <= i_pop_ch_read(1);
  o_pop_ch_data(1) <= ch_SPU0PE1_to_IOCore_b;
  o_pop_ch_empty(1) <= ch_SPU0PE1_to_IOCore_empty;

  ch_SPU0PE2_to_IOCore_read  <= i_pop_ch_read(2);
  o_pop_ch_data(2) <= ch_SPU0PE2_to_IOCore_b;
  o_pop_ch_empty(2) <= ch_SPU0PE2_to_IOCore_empty;

  ch_SPU0PE3_to_IOCore_read  <= i_pop_ch_read(3);
  o_pop_ch_data(3) <= ch_SPU0PE3_to_IOCore_b;
  o_pop_ch_empty(3) <= ch_SPU0PE3_to_IOCore_empty;

  ch_SPU0PE4_to_IOCore_read  <= i_pop_ch_read(4);
  o_pop_ch_data(4) <= ch_SPU0PE4_to_IOCore_b;
  o_pop_ch_empty(4) <= ch_SPU0PE4_to_IOCore_empty;

  ch_SPU0PE5_to_IOCore_read  <= i_pop_ch_read(5);
  o_pop_ch_data(5) <= ch_SPU0PE5_to_IOCore_b;
  o_pop_ch_empty(5) <= ch_SPU0PE5_to_IOCore_empty;

  ch_SPU0PE6_to_IOCore_read  <= i_pop_ch_read(6);
  o_pop_ch_data(6) <= ch_SPU0PE6_to_IOCore_b;
  o_pop_ch_empty(6) <= ch_SPU0PE6_to_IOCore_empty;

  ch_SPU0PE7_to_IOCore_read  <= i_pop_ch_read(7);
  o_pop_ch_data(7) <= ch_SPU0PE7_to_IOCore_b;
  o_pop_ch_empty(7) <= ch_SPU0PE7_to_IOCore_empty;

  -- Connect FIFOs with SPUs
  -- Connect FIFO IOCore_to_SPU0PE0 with PE
  get_ch_data_0(0) <= ch_IOCore_to_SPU0PE0_b;
  get_ch_empty_0(0) <= ch_IOCore_to_SPU0PE0_empty;
  ch_IOCore_to_SPU0PE0_read <= get_ch_read_0(0);

  -- Connect FIFO IOCore_to_SPU0PE0_1 with PE
  get_ch_data_0(1) <= ch_IOCore_to_SPU0PE0_1_b;
  get_ch_empty_0(1) <= ch_IOCore_to_SPU0PE0_1_empty;
  ch_IOCore_to_SPU0PE0_1_read <= get_ch_read_0(1);

  -- Connect FIFO IOCore_to_SPU0PE1 with PE
  get_ch_data_0(2) <= ch_IOCore_to_SPU0PE1_b;
  get_ch_empty_0(2) <= ch_IOCore_to_SPU0PE1_empty;
  ch_IOCore_to_SPU0PE1_read <= get_ch_read_0(2);

  -- Connect FIFO IOCore_to_SPU0PE1_1 with PE
  get_ch_data_0(3) <= ch_IOCore_to_SPU0PE1_1_b;
  get_ch_empty_0(3) <= ch_IOCore_to_SPU0PE1_1_empty;
  ch_IOCore_to_SPU0PE1_1_read <= get_ch_read_0(3);

  -- Connect FIFO IOCore_to_SPU0PE2 with PE
  get_ch_data_0(4) <= ch_IOCore_to_SPU0PE2_b;
  get_ch_empty_0(4) <= ch_IOCore_to_SPU0PE2_empty;
  ch_IOCore_to_SPU0PE2_read <= get_ch_read_0(4);

  -- Connect FIFO IOCore_to_SPU0PE2_1 with PE
  get_ch_data_0(5) <= ch_IOCore_to_SPU0PE2_1_b;
  get_ch_empty_0(5) <= ch_IOCore_to_SPU0PE2_1_empty;
  ch_IOCore_to_SPU0PE2_1_read <= get_ch_read_0(5);

  -- Connect FIFO IOCore_to_SPU0PE3 with PE
  get_ch_data_0(6) <= ch_IOCore_to_SPU0PE3_b;
  get_ch_empty_0(6) <= ch_IOCore_to_SPU0PE3_empty;
  ch_IOCore_to_SPU0PE3_read <= get_ch_read_0(6);

  -- Connect FIFO IOCore_to_SPU0PE3_1 with PE
  get_ch_data_0(7) <= ch_IOCore_to_SPU0PE3_1_b;
  get_ch_empty_0(7) <= ch_IOCore_to_SPU0PE3_1_empty;
  ch_IOCore_to_SPU0PE3_1_read <= get_ch_read_0(7);

  -- Connect FIFO IOCore_to_SPU0PE4 with PE
  get_ch_data_0(8) <= ch_IOCore_to_SPU0PE4_b;
  get_ch_empty_0(8) <= ch_IOCore_to_SPU0PE4_empty;
  ch_IOCore_to_SPU0PE4_read <= get_ch_read_0(8);

  -- Connect FIFO IOCore_to_SPU0PE4_1 with PE
  get_ch_data_0(9) <= ch_IOCore_to_SPU0PE4_1_b;
  get_ch_empty_0(9) <= ch_IOCore_to_SPU0PE4_1_empty;
  ch_IOCore_to_SPU0PE4_1_read <= get_ch_read_0(9);

  -- Connect FIFO IOCore_to_SPU0PE5 with PE
  get_ch_data_0(10) <= ch_IOCore_to_SPU0PE5_b;
  get_ch_empty_0(10) <= ch_IOCore_to_SPU0PE5_empty;
  ch_IOCore_to_SPU0PE5_read <= get_ch_read_0(10);

  -- Connect FIFO IOCore_to_SPU0PE5_1 with PE
  get_ch_data_0(11) <= ch_IOCore_to_SPU0PE5_1_b;
  get_ch_empty_0(11) <= ch_IOCore_to_SPU0PE5_1_empty;
  ch_IOCore_to_SPU0PE5_1_read <= get_ch_read_0(11);

  -- Connect FIFO IOCore_to_SPU0PE6 with PE
  get_ch_data_0(12) <= ch_IOCore_to_SPU0PE6_b;
  get_ch_empty_0(12) <= ch_IOCore_to_SPU0PE6_empty;
  ch_IOCore_to_SPU0PE6_read <= get_ch_read_0(12);

  -- Connect FIFO IOCore_to_SPU0PE6_1 with PE
  get_ch_data_0(13) <= ch_IOCore_to_SPU0PE6_1_b;
  get_ch_empty_0(13) <= ch_IOCore_to_SPU0PE6_1_empty;
  ch_IOCore_to_SPU0PE6_1_read <= get_ch_read_0(13);

  -- Connect FIFO IOCore_to_SPU0PE7 with PE
  get_ch_data_0(14) <= ch_IOCore_to_SPU0PE7_b;
  get_ch_empty_0(14) <= ch_IOCore_to_SPU0PE7_empty;
  ch_IOCore_to_SPU0PE7_read <= get_ch_read_0(14);

  -- Connect FIFO IOCore_to_SPU0PE7_1 with PE
  get_ch_data_0(15) <= ch_IOCore_to_SPU0PE7_1_b;
  get_ch_empty_0(15) <= ch_IOCore_to_SPU0PE7_1_empty;
  ch_IOCore_to_SPU0PE7_1_read <= get_ch_read_0(15);

  -- Connect FIFO SPU0PE0_to_IOCore with PE
  ch_SPU0PE0_to_IOCore_a <= put_ch_data_0(0);
  ch_SPU0PE0_to_IOCore_write <= put_ch_write_0(0);
  put_ch_full_0(0) <= ch_SPU0PE0_to_IOCore_full;

  -- Connect FIFO SPU0PE1_to_IOCore with PE
  ch_SPU0PE1_to_IOCore_a <= put_ch_data_0(1);
  ch_SPU0PE1_to_IOCore_write <= put_ch_write_0(1);
  put_ch_full_0(1) <= ch_SPU0PE1_to_IOCore_full;

  -- Connect FIFO SPU0PE2_to_IOCore with PE
  ch_SPU0PE2_to_IOCore_a <= put_ch_data_0(2);
  ch_SPU0PE2_to_IOCore_write <= put_ch_write_0(2);
  put_ch_full_0(2) <= ch_SPU0PE2_to_IOCore_full;

  -- Connect FIFO SPU0PE3_to_IOCore with PE
  ch_SPU0PE3_to_IOCore_a <= put_ch_data_0(3);
  ch_SPU0PE3_to_IOCore_write <= put_ch_write_0(3);
  put_ch_full_0(3) <= ch_SPU0PE3_to_IOCore_full;

  -- Connect FIFO SPU0PE4_to_IOCore with PE
  ch_SPU0PE4_to_IOCore_a <= put_ch_data_0(4);
  ch_SPU0PE4_to_IOCore_write <= put_ch_write_0(4);
  put_ch_full_0(4) <= ch_SPU0PE4_to_IOCore_full;

  -- Connect FIFO SPU0PE5_to_IOCore with PE
  ch_SPU0PE5_to_IOCore_a <= put_ch_data_0(5);
  ch_SPU0PE5_to_IOCore_write <= put_ch_write_0(5);
  put_ch_full_0(5) <= ch_SPU0PE5_to_IOCore_full;

  -- Connect FIFO SPU0PE6_to_IOCore with PE
  ch_SPU0PE6_to_IOCore_a <= put_ch_data_0(6);
  ch_SPU0PE6_to_IOCore_write <= put_ch_write_0(6);
  put_ch_full_0(6) <= ch_SPU0PE6_to_IOCore_full;

  -- Connect FIFO SPU0PE7_to_IOCore with PE
  ch_SPU0PE7_to_IOCore_a <= put_ch_data_0(7);
  ch_SPU0PE7_to_IOCore_write <= put_ch_write_0(7);
  put_ch_full_0(7) <= ch_SPU0PE7_to_IOCore_full;

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
  VLEN            => 8,
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
  EBITS_B      => 1,
  EBITS_C      => 2,
  EBITS_D      => 2,

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
  RF_INIT_FILE  => "RFInit/rf_initSPU0PE",

  PM_SIZE       => 902,
  PM_ADDR_WIDTH => 10,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init0.mif",

  DM_EN                 => true,
  DM_SIZE               => 128,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 32,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initSPU0PE",
  DM_RB_M_NUM           => 1,
  DM_RB_N_NUM           => 1,
  DM_WB_NUM             => 1,
  DM_TRUE_2R1W          => true,
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
  SM_INIT_FILE => "IMMInit/imm_init0.mif",
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
  i_get_ch_data  => get_ch_data_0,
  o_get_ch_read  => get_ch_read_0,
  i_get_ch_empty => get_ch_empty_0,

  -- Output channel
  o_put_ch_data  => put_ch_data_0,
  o_put_ch_write => put_ch_write_0,
  i_put_ch_full  => put_ch_full_0
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

u_fifo_IOCore_to_SPU0PE1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE1_a,
  write   => ch_IOCore_to_SPU0PE1_write,
  o_full  => ch_IOCore_to_SPU0PE1_full,

  o_data  => ch_IOCore_to_SPU0PE1_b,
  read    => ch_IOCore_to_SPU0PE1_read,
  o_empty => ch_IOCore_to_SPU0PE1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE1_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE1_1_a,
  write   => ch_IOCore_to_SPU0PE1_1_write,
  o_full  => ch_IOCore_to_SPU0PE1_1_full,

  o_data  => ch_IOCore_to_SPU0PE1_1_b,
  read    => ch_IOCore_to_SPU0PE1_1_read,
  o_empty => ch_IOCore_to_SPU0PE1_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE2: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE2_a,
  write   => ch_IOCore_to_SPU0PE2_write,
  o_full  => ch_IOCore_to_SPU0PE2_full,

  o_data  => ch_IOCore_to_SPU0PE2_b,
  read    => ch_IOCore_to_SPU0PE2_read,
  o_empty => ch_IOCore_to_SPU0PE2_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE2_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE2_1_a,
  write   => ch_IOCore_to_SPU0PE2_1_write,
  o_full  => ch_IOCore_to_SPU0PE2_1_full,

  o_data  => ch_IOCore_to_SPU0PE2_1_b,
  read    => ch_IOCore_to_SPU0PE2_1_read,
  o_empty => ch_IOCore_to_SPU0PE2_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE3: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE3_a,
  write   => ch_IOCore_to_SPU0PE3_write,
  o_full  => ch_IOCore_to_SPU0PE3_full,

  o_data  => ch_IOCore_to_SPU0PE3_b,
  read    => ch_IOCore_to_SPU0PE3_read,
  o_empty => ch_IOCore_to_SPU0PE3_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE3_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE3_1_a,
  write   => ch_IOCore_to_SPU0PE3_1_write,
  o_full  => ch_IOCore_to_SPU0PE3_1_full,

  o_data  => ch_IOCore_to_SPU0PE3_1_b,
  read    => ch_IOCore_to_SPU0PE3_1_read,
  o_empty => ch_IOCore_to_SPU0PE3_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE4: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE4_a,
  write   => ch_IOCore_to_SPU0PE4_write,
  o_full  => ch_IOCore_to_SPU0PE4_full,

  o_data  => ch_IOCore_to_SPU0PE4_b,
  read    => ch_IOCore_to_SPU0PE4_read,
  o_empty => ch_IOCore_to_SPU0PE4_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE4_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE4_1_a,
  write   => ch_IOCore_to_SPU0PE4_1_write,
  o_full  => ch_IOCore_to_SPU0PE4_1_full,

  o_data  => ch_IOCore_to_SPU0PE4_1_b,
  read    => ch_IOCore_to_SPU0PE4_1_read,
  o_empty => ch_IOCore_to_SPU0PE4_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE5: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE5_a,
  write   => ch_IOCore_to_SPU0PE5_write,
  o_full  => ch_IOCore_to_SPU0PE5_full,

  o_data  => ch_IOCore_to_SPU0PE5_b,
  read    => ch_IOCore_to_SPU0PE5_read,
  o_empty => ch_IOCore_to_SPU0PE5_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE5_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE5_1_a,
  write   => ch_IOCore_to_SPU0PE5_1_write,
  o_full  => ch_IOCore_to_SPU0PE5_1_full,

  o_data  => ch_IOCore_to_SPU0PE5_1_b,
  read    => ch_IOCore_to_SPU0PE5_1_read,
  o_empty => ch_IOCore_to_SPU0PE5_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE6: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE6_a,
  write   => ch_IOCore_to_SPU0PE6_write,
  o_full  => ch_IOCore_to_SPU0PE6_full,

  o_data  => ch_IOCore_to_SPU0PE6_b,
  read    => ch_IOCore_to_SPU0PE6_read,
  o_empty => ch_IOCore_to_SPU0PE6_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE6_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE6_1_a,
  write   => ch_IOCore_to_SPU0PE6_1_write,
  o_full  => ch_IOCore_to_SPU0PE6_1_full,

  o_data  => ch_IOCore_to_SPU0PE6_1_b,
  read    => ch_IOCore_to_SPU0PE6_1_read,
  o_empty => ch_IOCore_to_SPU0PE6_1_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE7: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE7_a,
  write   => ch_IOCore_to_SPU0PE7_write,
  o_full  => ch_IOCore_to_SPU0PE7_full,

  o_data  => ch_IOCore_to_SPU0PE7_b,
  read    => ch_IOCore_to_SPU0PE7_read,
  o_empty => ch_IOCore_to_SPU0PE7_empty,
  clk     => clk
);

u_fifo_IOCore_to_SPU0PE7_1: fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_IOCore_to_SPU0PE7_1_a,
  write   => ch_IOCore_to_SPU0PE7_1_write,
  o_full  => ch_IOCore_to_SPU0PE7_1_full,

  o_data  => ch_IOCore_to_SPU0PE7_1_b,
  read    => ch_IOCore_to_SPU0PE7_1_read,
  o_empty => ch_IOCore_to_SPU0PE7_1_empty,
  clk     => clk
);

u_fifo_SPU0PE0_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE0_to_IOCore_a,
  write   => ch_SPU0PE0_to_IOCore_write,
  o_full  => ch_SPU0PE0_to_IOCore_full,

  o_data  => ch_SPU0PE0_to_IOCore_b,
  read    => ch_SPU0PE0_to_IOCore_read,
  o_empty => ch_SPU0PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE1_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE1_to_IOCore_a,
  write   => ch_SPU0PE1_to_IOCore_write,
  o_full  => ch_SPU0PE1_to_IOCore_full,

  o_data  => ch_SPU0PE1_to_IOCore_b,
  read    => ch_SPU0PE1_to_IOCore_read,
  o_empty => ch_SPU0PE1_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE2_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE2_to_IOCore_a,
  write   => ch_SPU0PE2_to_IOCore_write,
  o_full  => ch_SPU0PE2_to_IOCore_full,

  o_data  => ch_SPU0PE2_to_IOCore_b,
  read    => ch_SPU0PE2_to_IOCore_read,
  o_empty => ch_SPU0PE2_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE3_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE3_to_IOCore_a,
  write   => ch_SPU0PE3_to_IOCore_write,
  o_full  => ch_SPU0PE3_to_IOCore_full,

  o_data  => ch_SPU0PE3_to_IOCore_b,
  read    => ch_SPU0PE3_to_IOCore_read,
  o_empty => ch_SPU0PE3_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE4_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE4_to_IOCore_a,
  write   => ch_SPU0PE4_to_IOCore_write,
  o_full  => ch_SPU0PE4_to_IOCore_full,

  o_data  => ch_SPU0PE4_to_IOCore_b,
  read    => ch_SPU0PE4_to_IOCore_read,
  o_empty => ch_SPU0PE4_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE5_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE5_to_IOCore_a,
  write   => ch_SPU0PE5_to_IOCore_write,
  o_full  => ch_SPU0PE5_to_IOCore_full,

  o_data  => ch_SPU0PE5_to_IOCore_b,
  read    => ch_SPU0PE5_to_IOCore_read,
  o_empty => ch_SPU0PE5_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE6_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE6_to_IOCore_a,
  write   => ch_SPU0PE6_to_IOCore_write,
  o_full  => ch_SPU0PE6_to_IOCore_full,

  o_data  => ch_SPU0PE6_to_IOCore_b,
  read    => ch_SPU0PE6_to_IOCore_read,
  o_empty => ch_SPU0PE6_to_IOCore_empty,
  clk     => clk
);

u_fifo_SPU0PE7_to_IOCore: fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>IOFIFODEPTH )
port map(
  i_data  => ch_SPU0PE7_to_IOCore_a,
  write   => ch_SPU0PE7_to_IOCore_write,
  o_full  => ch_SPU0PE7_to_IOCore_full,

  o_data  => ch_SPU0PE7_to_IOCore_b,
  read    => ch_SPU0PE7_to_IOCore_read,
  o_empty => ch_SPU0PE7_to_IOCore_empty,
  clk     => clk
);

end Structure;
