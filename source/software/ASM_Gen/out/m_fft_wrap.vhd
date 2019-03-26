library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;

library work;
use work.m_word_pkg.all;
use work.m_word_config.all;

Library UNISIM;
use UNISIM.vcomponents.all;

entity m_fft_wrap is
generic (
      CORE_WIDTH     : integer := 16;
      INPUT_WIDTH    : integer := 16;
      OUTPUT_WIDTH   : integer := 16;
      EXIN_FIFO_NUM  : integer := 8;
      EXOUT_FIFO_NUM : integer := 8);
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
end m_fft_wrap;

architecture Structure of m_fft_wrap is

 signal barrier     : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);

  signal ch_IOCore_to_FPE0PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE0PE0_write : std_logic;
  signal ch_IOCore_to_FPE0PE0_full  : std_logic;
  signal ch_IOCore_to_FPE0PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE0PE0_read  : std_logic;
  signal ch_IOCore_to_FPE0PE0_empty : std_logic;
  signal ch_IOCore_to_FPE1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE1PE0_write : std_logic;
  signal ch_IOCore_to_FPE1PE0_full  : std_logic;
  signal ch_IOCore_to_FPE1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE1PE0_read  : std_logic;
  signal ch_IOCore_to_FPE1PE0_empty : std_logic;
  signal ch_IOCore_to_FPE2PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE2PE0_write : std_logic;
  signal ch_IOCore_to_FPE2PE0_full  : std_logic;
  signal ch_IOCore_to_FPE2PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE2PE0_read  : std_logic;
  signal ch_IOCore_to_FPE2PE0_empty : std_logic;
  signal ch_IOCore_to_FPE3PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE3PE0_write : std_logic;
  signal ch_IOCore_to_FPE3PE0_full  : std_logic;
  signal ch_IOCore_to_FPE3PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE3PE0_read  : std_logic;
  signal ch_IOCore_to_FPE3PE0_empty : std_logic;
  signal ch_IOCore_to_FPE4PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE4PE0_write : std_logic;
  signal ch_IOCore_to_FPE4PE0_full  : std_logic;
  signal ch_IOCore_to_FPE4PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE4PE0_read  : std_logic;
  signal ch_IOCore_to_FPE4PE0_empty : std_logic;
  signal ch_IOCore_to_FPE5PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE5PE0_write : std_logic;
  signal ch_IOCore_to_FPE5PE0_full  : std_logic;
  signal ch_IOCore_to_FPE5PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE5PE0_read  : std_logic;
  signal ch_IOCore_to_FPE5PE0_empty : std_logic;
  signal ch_IOCore_to_FPE6PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE6PE0_write : std_logic;
  signal ch_IOCore_to_FPE6PE0_full  : std_logic;
  signal ch_IOCore_to_FPE6PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE6PE0_read  : std_logic;
  signal ch_IOCore_to_FPE6PE0_empty : std_logic;
  signal ch_IOCore_to_FPE7PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE7PE0_write : std_logic;
  signal ch_IOCore_to_FPE7PE0_full  : std_logic;
  signal ch_IOCore_to_FPE7PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_IOCore_to_FPE7PE0_read  : std_logic;
  signal ch_IOCore_to_FPE7PE0_empty : std_logic;
  signal ch_FPE0PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE0PE0_to_IOCore_write : std_logic;
  signal ch_FPE0PE0_to_IOCore_full  : std_logic;
  signal ch_FPE0PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE0PE0_to_IOCore_read  : std_logic;
  signal ch_FPE0PE0_to_IOCore_empty : std_logic;
  signal ch_FPE1PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE1PE0_to_IOCore_write : std_logic;
  signal ch_FPE1PE0_to_IOCore_full  : std_logic;
  signal ch_FPE1PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE1PE0_to_IOCore_read  : std_logic;
  signal ch_FPE1PE0_to_IOCore_empty : std_logic;
  signal ch_FPE2PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE2PE0_to_IOCore_write : std_logic;
  signal ch_FPE2PE0_to_IOCore_full  : std_logic;
  signal ch_FPE2PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE2PE0_to_IOCore_read  : std_logic;
  signal ch_FPE2PE0_to_IOCore_empty : std_logic;
  signal ch_FPE3PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE3PE0_to_IOCore_write : std_logic;
  signal ch_FPE3PE0_to_IOCore_full  : std_logic;
  signal ch_FPE3PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE3PE0_to_IOCore_read  : std_logic;
  signal ch_FPE3PE0_to_IOCore_empty : std_logic;
  signal ch_FPE4PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE4PE0_to_IOCore_write : std_logic;
  signal ch_FPE4PE0_to_IOCore_full  : std_logic;
  signal ch_FPE4PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE4PE0_to_IOCore_read  : std_logic;
  signal ch_FPE4PE0_to_IOCore_empty : std_logic;
  signal ch_FPE5PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE5PE0_to_IOCore_write : std_logic;
  signal ch_FPE5PE0_to_IOCore_full  : std_logic;
  signal ch_FPE5PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE5PE0_to_IOCore_read  : std_logic;
  signal ch_FPE5PE0_to_IOCore_empty : std_logic;
  signal ch_FPE6PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE6PE0_to_IOCore_write : std_logic;
  signal ch_FPE6PE0_to_IOCore_full  : std_logic;
  signal ch_FPE6PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE6PE0_to_IOCore_read  : std_logic;
  signal ch_FPE6PE0_to_IOCore_empty : std_logic;
  signal ch_FPE7PE0_to_IOCore_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE7PE0_to_IOCore_write : std_logic;
  signal ch_FPE7PE0_to_IOCore_full  : std_logic;
  signal ch_FPE7PE0_to_IOCore_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE7PE0_to_IOCore_read  : std_logic;
  signal ch_FPE7PE0_to_IOCore_empty : std_logic;
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_write : std_logic;
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_full  : std_logic;
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_read  : std_logic;
  signal ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_empty : std_logic;
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_write : std_logic;
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_full  : std_logic;
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_read  : std_logic;
  signal ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_empty : std_logic;
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_write : std_logic;
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_full  : std_logic;
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_read  : std_logic;
  signal ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_empty : std_logic;
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_write : std_logic;
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_full  : std_logic;
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_read  : std_logic;
  signal ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_empty : std_logic;
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_write : std_logic;
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_full  : std_logic;
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_read  : std_logic;
  signal ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_empty : std_logic;
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_write : std_logic;
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_full  : std_logic;
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_read  : std_logic;
  signal ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_empty : std_logic;
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_write : std_logic;
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_full  : std_logic;
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_read  : std_logic;
  signal ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_empty : std_logic;
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_a     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_write : std_logic;
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_full  : std_logic;
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_b     : std_logic_vector(CORE_WIDTH-1 downto 0);
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_read  : std_logic;
  signal ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_empty : std_logic;
  -- SPU signals
  signal get_ch_data_0  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_0  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_0 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_0  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_0 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_0  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_1  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_1  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_1 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_1  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_1 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_1  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_2  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_2  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_2 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_2  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_2 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_2  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_3  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_3  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_3 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_3  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_3 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_3  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_4  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_4  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_4 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_4  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_4 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_4  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_5  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_5  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_5 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_5  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_5 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_5  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_6  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_6  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_6 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_6  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_6 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_6  : VSIG_TYPE(3 downto 0);

  signal get_ch_data_7  : VDATA_TYPE(3 downto 0);
  signal get_ch_read_7  : VSIG_TYPE(3 downto 0);
  signal get_ch_empty_7 : VSIG_TYPE(3 downto 0);
  signal put_ch_data_7  : VDATA_TYPE(3 downto 0);
  signal put_ch_write_7 : VSIG_TYPE(3 downto 0);
  signal put_ch_full_7  : VSIG_TYPE(3 downto 0);

begin

  -- Connect signals with module ports
  o_barrier <= barrier(0);

  ch_IOCore_to_FPE0PE0_a <= i_push_ch_data(0);
  ch_IOCore_to_FPE0PE0_write  <= i_push_ch_write(0);
  o_push_ch_full(0) <= ch_IOCore_to_FPE0PE0_full;

  ch_IOCore_to_FPE1PE0_a <= i_push_ch_data(1);
  ch_IOCore_to_FPE1PE0_write  <= i_push_ch_write(1);
  o_push_ch_full(1) <= ch_IOCore_to_FPE1PE0_full;

  ch_IOCore_to_FPE2PE0_a <= i_push_ch_data(2);
  ch_IOCore_to_FPE2PE0_write  <= i_push_ch_write(2);
  o_push_ch_full(2) <= ch_IOCore_to_FPE2PE0_full;

  ch_IOCore_to_FPE3PE0_a <= i_push_ch_data(3);
  ch_IOCore_to_FPE3PE0_write  <= i_push_ch_write(3);
  o_push_ch_full(3) <= ch_IOCore_to_FPE3PE0_full;

  ch_IOCore_to_FPE4PE0_a <= i_push_ch_data(4);
  ch_IOCore_to_FPE4PE0_write  <= i_push_ch_write(4);
  o_push_ch_full(4) <= ch_IOCore_to_FPE4PE0_full;

  ch_IOCore_to_FPE5PE0_a <= i_push_ch_data(5);
  ch_IOCore_to_FPE5PE0_write  <= i_push_ch_write(5);
  o_push_ch_full(5) <= ch_IOCore_to_FPE5PE0_full;

  ch_IOCore_to_FPE6PE0_a <= i_push_ch_data(6);
  ch_IOCore_to_FPE6PE0_write  <= i_push_ch_write(6);
  o_push_ch_full(6) <= ch_IOCore_to_FPE6PE0_full;

  ch_IOCore_to_FPE7PE0_a <= i_push_ch_data(7);
  ch_IOCore_to_FPE7PE0_write  <= i_push_ch_write(7);
  o_push_ch_full(7) <= ch_IOCore_to_FPE7PE0_full;

  ch_FPE0PE0_to_IOCore_read  <= i_pop_ch_read(0);
  o_pop_ch_data(0) <= ch_FPE0PE0_to_IOCore_b;
  o_pop_ch_empty(0) <= ch_FPE0PE0_to_IOCore_empty;

  ch_FPE1PE0_to_IOCore_read  <= i_pop_ch_read(1);
  o_pop_ch_data(1) <= ch_FPE1PE0_to_IOCore_b;
  o_pop_ch_empty(1) <= ch_FPE1PE0_to_IOCore_empty;

  ch_FPE2PE0_to_IOCore_read  <= i_pop_ch_read(2);
  o_pop_ch_data(2) <= ch_FPE2PE0_to_IOCore_b;
  o_pop_ch_empty(2) <= ch_FPE2PE0_to_IOCore_empty;

  ch_FPE3PE0_to_IOCore_read  <= i_pop_ch_read(3);
  o_pop_ch_data(3) <= ch_FPE3PE0_to_IOCore_b;
  o_pop_ch_empty(3) <= ch_FPE3PE0_to_IOCore_empty;

  ch_FPE4PE0_to_IOCore_read  <= i_pop_ch_read(4);
  o_pop_ch_data(4) <= ch_FPE4PE0_to_IOCore_b;
  o_pop_ch_empty(4) <= ch_FPE4PE0_to_IOCore_empty;

  ch_FPE5PE0_to_IOCore_read  <= i_pop_ch_read(5);
  o_pop_ch_data(5) <= ch_FPE5PE0_to_IOCore_b;
  o_pop_ch_empty(5) <= ch_FPE5PE0_to_IOCore_empty;

  ch_FPE6PE0_to_IOCore_read  <= i_pop_ch_read(6);
  o_pop_ch_data(6) <= ch_FPE6PE0_to_IOCore_b;
  o_pop_ch_empty(6) <= ch_FPE6PE0_to_IOCore_empty;

  ch_FPE7PE0_to_IOCore_read  <= i_pop_ch_read(7);
  o_pop_ch_data(7) <= ch_FPE7PE0_to_IOCore_b;
  o_pop_ch_empty(7) <= ch_FPE7PE0_to_IOCore_empty;

  -- Connect FIFOs with SPUs
  -- Connect FIFO IOCore_to_FPE0PE0 with PE
  get_ch_data_0(0) <= ch_IOCore_to_FPE0PE0_b;
  get_ch_empty_0(0) <= ch_IOCore_to_FPE0PE0_empty;
  ch_IOCore_to_FPE0PE0_read <= get_ch_read_0(0);

  -- Connect FIFO IOCore_to_FPE1PE0 with PE
  get_ch_data_1(0) <= ch_IOCore_to_FPE1PE0_b;
  get_ch_empty_1(0) <= ch_IOCore_to_FPE1PE0_empty;
  ch_IOCore_to_FPE1PE0_read <= get_ch_read_1(0);

  -- Connect FIFO IOCore_to_FPE2PE0 with PE
  get_ch_data_2(0) <= ch_IOCore_to_FPE2PE0_b;
  get_ch_empty_2(0) <= ch_IOCore_to_FPE2PE0_empty;
  ch_IOCore_to_FPE2PE0_read <= get_ch_read_2(0);

  -- Connect FIFO IOCore_to_FPE3PE0 with PE
  get_ch_data_3(0) <= ch_IOCore_to_FPE3PE0_b;
  get_ch_empty_3(0) <= ch_IOCore_to_FPE3PE0_empty;
  ch_IOCore_to_FPE3PE0_read <= get_ch_read_3(0);

  -- Connect FIFO IOCore_to_FPE4PE0 with PE
  get_ch_data_4(0) <= ch_IOCore_to_FPE4PE0_b;
  get_ch_empty_4(0) <= ch_IOCore_to_FPE4PE0_empty;
  ch_IOCore_to_FPE4PE0_read <= get_ch_read_4(0);

  -- Connect FIFO IOCore_to_FPE5PE0 with PE
  get_ch_data_5(0) <= ch_IOCore_to_FPE5PE0_b;
  get_ch_empty_5(0) <= ch_IOCore_to_FPE5PE0_empty;
  ch_IOCore_to_FPE5PE0_read <= get_ch_read_5(0);

  -- Connect FIFO IOCore_to_FPE6PE0 with PE
  get_ch_data_6(0) <= ch_IOCore_to_FPE6PE0_b;
  get_ch_empty_6(0) <= ch_IOCore_to_FPE6PE0_empty;
  ch_IOCore_to_FPE6PE0_read <= get_ch_read_6(0);

  -- Connect FIFO IOCore_to_FPE7PE0 with PE
  get_ch_data_7(0) <= ch_IOCore_to_FPE7PE0_b;
  get_ch_empty_7(0) <= ch_IOCore_to_FPE7PE0_empty;
  ch_IOCore_to_FPE7PE0_read <= get_ch_read_7(0);

  -- Connect FIFO FPE0PE0_to_IOCore with PE
  ch_FPE0PE0_to_IOCore_a <= put_ch_data_0(1);
  ch_FPE0PE0_to_IOCore_write <= put_ch_write_0(1);
  put_ch_full_0(1) <= ch_FPE0PE0_to_IOCore_full;

  -- Connect FIFO FPE1PE0_to_IOCore with PE
  ch_FPE1PE0_to_IOCore_a <= put_ch_data_1(1);
  ch_FPE1PE0_to_IOCore_write <= put_ch_write_1(1);
  put_ch_full_1(1) <= ch_FPE1PE0_to_IOCore_full;

  -- Connect FIFO FPE2PE0_to_IOCore with PE
  ch_FPE2PE0_to_IOCore_a <= put_ch_data_2(1);
  ch_FPE2PE0_to_IOCore_write <= put_ch_write_2(1);
  put_ch_full_2(1) <= ch_FPE2PE0_to_IOCore_full;

  -- Connect FIFO FPE3PE0_to_IOCore with PE
  ch_FPE3PE0_to_IOCore_a <= put_ch_data_3(1);
  ch_FPE3PE0_to_IOCore_write <= put_ch_write_3(1);
  put_ch_full_3(1) <= ch_FPE3PE0_to_IOCore_full;

  -- Connect FIFO FPE4PE0_to_IOCore with PE
  ch_FPE4PE0_to_IOCore_a <= put_ch_data_4(1);
  ch_FPE4PE0_to_IOCore_write <= put_ch_write_4(1);
  put_ch_full_4(1) <= ch_FPE4PE0_to_IOCore_full;

  -- Connect FIFO FPE5PE0_to_IOCore with PE
  ch_FPE5PE0_to_IOCore_a <= put_ch_data_5(1);
  ch_FPE5PE0_to_IOCore_write <= put_ch_write_5(1);
  put_ch_full_5(1) <= ch_FPE5PE0_to_IOCore_full;

  -- Connect FIFO FPE6PE0_to_IOCore with PE
  ch_FPE6PE0_to_IOCore_a <= put_ch_data_6(1);
  ch_FPE6PE0_to_IOCore_write <= put_ch_write_6(1);
  put_ch_full_6(1) <= ch_FPE6PE0_to_IOCore_full;

  -- Connect FIFO FPE7PE0_to_IOCore with PE
  ch_FPE7PE0_to_IOCore_a <= put_ch_data_7(1);
  ch_FPE7PE0_to_IOCore_write <= put_ch_write_7(1);
  put_ch_full_7(1) <= ch_FPE7PE0_to_IOCore_full;

  -- Connect FIFO FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0 with PE
  ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_a <= put_ch_data_0(0);
  ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_write <= put_ch_write_0(0);
  put_ch_full_0(0) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_full;

  get_ch_data_4(3) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_b;
  get_ch_empty_4(3) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_empty;
  get_ch_data_2(2) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_b;
  get_ch_empty_2(2) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_empty;
  get_ch_data_1(1) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_b;
  get_ch_empty_1(1) <= ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_empty;
  ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_read <= get_ch_read_4(3) or get_ch_read_2(2) or get_ch_read_1(1);

  -- Connect FIFO FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0 with PE
  ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_a <= put_ch_data_1(0);
  ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_write <= put_ch_write_1(0);
  put_ch_full_1(0) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_full;

  get_ch_data_5(3) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_b;
  get_ch_empty_5(3) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_empty;
  get_ch_data_3(2) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_b;
  get_ch_empty_3(2) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_empty;
  get_ch_data_0(1) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_b;
  get_ch_empty_0(1) <= ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_empty;
  ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_read <= get_ch_read_5(3) or get_ch_read_3(2) or get_ch_read_0(1);

  -- Connect FIFO FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0 with PE
  ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_a <= put_ch_data_2(0);
  ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_write <= put_ch_write_2(0);
  put_ch_full_2(0) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_full;

  get_ch_data_6(3) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_b;
  get_ch_empty_6(3) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_empty;
  get_ch_data_0(2) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_b;
  get_ch_empty_0(2) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_empty;
  get_ch_data_3(1) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_b;
  get_ch_empty_3(1) <= ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_empty;
  ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_read <= get_ch_read_6(3) or get_ch_read_0(2) or get_ch_read_3(1);

  -- Connect FIFO FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0 with PE
  ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_a <= put_ch_data_3(0);
  ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_write <= put_ch_write_3(0);
  put_ch_full_3(0) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_full;

  get_ch_data_7(3) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_b;
  get_ch_empty_7(3) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_empty;
  get_ch_data_1(2) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_b;
  get_ch_empty_1(2) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_empty;
  get_ch_data_2(1) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_b;
  get_ch_empty_2(1) <= ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_empty;
  ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_read <= get_ch_read_7(3) or get_ch_read_1(2) or get_ch_read_2(1);

  -- Connect FIFO FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0 with PE
  ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_a <= put_ch_data_4(0);
  ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_write <= put_ch_write_4(0);
  put_ch_full_4(0) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_full;

  get_ch_data_0(3) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_b;
  get_ch_empty_0(3) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_empty;
  get_ch_data_6(2) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_b;
  get_ch_empty_6(2) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_empty;
  get_ch_data_5(1) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_b;
  get_ch_empty_5(1) <= ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_empty;
  ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_read <= get_ch_read_0(3) or get_ch_read_6(2) or get_ch_read_5(1);

  -- Connect FIFO FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0 with PE
  ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_a <= put_ch_data_5(0);
  ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_write <= put_ch_write_5(0);
  put_ch_full_5(0) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_full;

  get_ch_data_1(3) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_b;
  get_ch_empty_1(3) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_empty;
  get_ch_data_7(2) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_b;
  get_ch_empty_7(2) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_empty;
  get_ch_data_4(1) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_b;
  get_ch_empty_4(1) <= ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_empty;
  ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_read <= get_ch_read_1(3) or get_ch_read_7(2) or get_ch_read_4(1);

  -- Connect FIFO FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0 with PE
  ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_a <= put_ch_data_6(0);
  ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_write <= put_ch_write_6(0);
  put_ch_full_6(0) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_full;

  get_ch_data_2(3) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_b;
  get_ch_empty_2(3) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_empty;
  get_ch_data_4(2) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_b;
  get_ch_empty_4(2) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_empty;
  get_ch_data_7(1) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_b;
  get_ch_empty_7(1) <= ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_empty;
  ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_read <= get_ch_read_2(3) or get_ch_read_4(2) or get_ch_read_7(1);

  -- Connect FIFO FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0 with PE
  ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_a <= put_ch_data_7(0);
  ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_write <= put_ch_write_7(0);
  put_ch_full_7(0) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_full;

  get_ch_data_3(3) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_b;
  get_ch_empty_3(3) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_empty;
  get_ch_data_5(2) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_b;
  get_ch_empty_5(2) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_empty;
  get_ch_data_6(1) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_b;
  get_ch_empty_6(1) <= ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_empty;
  ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_read <= get_ch_read_3(3) or get_ch_read_5(2) or get_ch_read_6(1);

  -- Instantiate PEs and clock enables
u_core_0: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE0PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init0.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE0PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init0.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_0,
  o_get_ch_read  => get_ch_read_0,
  i_get_ch_empty => get_ch_empty_0,

  -- Output channel
  o_put_ch_data  => put_ch_data_0,
  o_put_ch_write => put_ch_write_0,
  i_put_ch_full  => put_ch_full_0
);


u_core_1: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE1PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init1.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE1PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init1.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_1,
  o_get_ch_read  => get_ch_read_1,
  i_get_ch_empty => get_ch_empty_1,

  -- Output channel
  o_put_ch_data  => put_ch_data_1,
  o_put_ch_write => put_ch_write_1,
  i_put_ch_full  => put_ch_full_1
);


u_core_2: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE2PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init2.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE2PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init2.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_2,
  o_get_ch_read  => get_ch_read_2,
  i_get_ch_empty => get_ch_empty_2,

  -- Output channel
  o_put_ch_data  => put_ch_data_2,
  o_put_ch_write => put_ch_write_2,
  i_put_ch_full  => put_ch_full_2
);


u_core_3: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE3PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init3.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE3PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init3.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_3,
  o_get_ch_read  => get_ch_read_3,
  i_get_ch_empty => get_ch_empty_3,

  -- Output channel
  o_put_ch_data  => put_ch_data_3,
  o_put_ch_write => put_ch_write_3,
  i_put_ch_full  => put_ch_full_3
);


u_core_4: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE4PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init4.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE4PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init4.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_4,
  o_get_ch_read  => get_ch_read_4,
  i_get_ch_empty => get_ch_empty_4,

  -- Output channel
  o_put_ch_data  => put_ch_data_4,
  o_put_ch_write => put_ch_write_4,
  i_put_ch_full  => put_ch_full_4
);


u_core_5: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE5PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init5.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE5PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init5.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_5,
  o_get_ch_read  => get_ch_read_5,
  i_get_ch_empty => get_ch_empty_5,

  -- Output channel
  o_put_ch_data  => put_ch_data_5,
  o_put_ch_write => put_ch_write_5,
  i_put_ch_full  => put_ch_full_5
);


u_core_6: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE6PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init6.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE6PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init6.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_6,
  o_get_ch_read  => get_ch_read_6,
  i_get_ch_empty => get_ch_empty_6,

  -- Output channel
  o_put_ch_data  => put_ch_data_6,
  o_put_ch_write => put_ch_write_6,
  i_put_ch_full  => put_ch_full_6
);


u_core_7: m_word_core_v
generic map(
  DATA_WIDTH      => 16,
  DATA_TYPE       => 1,
  SLICE_NUM       => 1,
  CORE_DATA_WIDTH => 16,
  OPM_NUM         => 1,
  ALUM_NUM        => 1,
  FRAC_BITS       => 14,
  NOIOCORE        => true,

  VLEN       => 1,

  -- Control Pipeline
  MULREG_EN  => false,
  PB0_DEPTH  => 1,
  PB1_DEPTH  => 1,
  PB2_DEPTH  => 1,
  PA0_DEPTH  => 1,
  PA1_DEPTH  => 1,
  PA1X_DEPTH => 0,

  -- Control Branch
  BRANCH_EN     => false,
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

  -- Control Supported Instructions
  MASK_EN      => false,
  MASKEQ_EN    => false,
  MASKGT_EN    => false,
  MASKLT_EN    => false,
  ALUSRA1_EN   => true,
  ABSDIFF_EN   => false,
  ABSDIFF_TYPE => 1,

  FLEXA_TYPE   => 1,
  FLEXB_TYPE   => 7,
  FLEXC_TYPE   => 1,

  -- Control FIFO
  GETI_EN     => false,
  GETCH_EN    => false,
  PUTCH_EN    => false,
  RX_CH_NUM   => 4,
  RX_CH_WIDTH => 2,
  TX_CH_NUM   => 4,
  TX_CH_WIDTH => 2,

  -- Control memory
  RF_EN         => true,
  RF_ADDR_WIDTH => 5,
  RF_INIT_EN    => false,
  RF_INIT_FILE  => "RFInit/rf_initFPE7PE",

  PM_SIZE       => 1688,
  PM_ADDR_WIDTH => 11,
  PM_DATA_WIDTH => 32,
  USE_BRAM_FOR_LARGE_PM => true,
  PM_INIT_FILE => "PMInit/pm_init7.mif",

  DM_EN                 => true,
  DM_OFFSET_WIDTH       => 7,
  DM_SIZE               => 75,
  DM_ADDR_WIDTH         => 7,
  DM_DATA_WIDTH         => 16,
  DM_INIT_EN            => false,
  USE_BRAM_FOR_LARGE_DM => true,
  DM_INIT_FILE          => "DMInit/dm_initFPE7PE",
  DM_RB_B_NUM           => 1,
  DM_RB_C_NUM           => 0,
  DM_RB_B_INITIAL0      => 0,
  DM_RB_B_INITIAL1      => 0,
  DM_RB_B_INITIAL2      => 0,
  DM_RB_C_INITIAL0      => 0,
  DM_WB_INITIAL         => 0,
  DM_RB_B_AUTOINC_SIZE0 => 1,
  DM_RB_B_AUTOINC_SIZE1 => 1,
  DM_RB_B_AUTOINC_SIZE2 => 1,
  DM_RB_C_AUTOINC_SIZE0 => 1,
  DM_WB_AUTOINC_SIZE    => 1,
  DM_OFFSET_EN          => true,
  DM_DIRECT_EN          => false,
  DM_RB_B_SET_EN0       => false,
  DM_RB_B_SET_EN1       => false,
  DM_RB_B_SET_EN2       => false,
  DM_RB_C_SET_EN0       => false,
  DM_WB_SET_EN          => false,
  DM_RB_B_AUTOINC_EN0   => false,
  DM_RB_B_AUTOINC_EN1   => false,
  DM_RB_B_AUTOINC_EN2   => false,
  DM_RB_C_AUTOINC_EN0   => false,
  DM_WB_AUTOINC_EN      => false,
  DM_RB_B_INC_EN0       => false,
  DM_RB_B_INC_EN1       => false,
  DM_RB_B_INC_EN2       => false,
  DM_RB_C_INC_EN0       => false,
  DM_WB_INC_EN          => false,

  SM_EN        => true,
  SM_OFFSET_WIDTH  => 5,
  SM_SIZE       => 64,
  SM_ADDR_WIDTH    => 6,
  USE_BRAM_FOR_LARGE_SM => true,
  SM_INIT_FILE => "IMMInit/imm_init7.mif",
  SM_DIRECT_EN => false,
  SM_OFFSET_EN => true,
  SM_READONLY => true,
  SM_RB_SET_EN0 => true,
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

  i_en_spu => i_en_spu,
  o_barrier => open,

  -- Communication port signals
  i_get_ch_data  => get_ch_data_7,
  o_get_ch_read  => get_ch_read_7,
  i_get_ch_empty => get_ch_empty_7,

  -- Output channel
  o_put_ch_data  => put_ch_data_7,
  o_put_ch_write => put_ch_write_7,
  i_put_ch_full  => put_ch_full_7
);


  -- Instantiate FIFOs
u_fifo_IOCore_to_FPE0PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE0PE0_a,
  write   => ch_IOCore_to_FPE0PE0_write,
  o_full  => ch_IOCore_to_FPE0PE0_full,

  o_data  => ch_IOCore_to_FPE0PE0_b,
  read    => ch_IOCore_to_FPE0PE0_read,
  o_empty => ch_IOCore_to_FPE0PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE1PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE1PE0_a,
  write   => ch_IOCore_to_FPE1PE0_write,
  o_full  => ch_IOCore_to_FPE1PE0_full,

  o_data  => ch_IOCore_to_FPE1PE0_b,
  read    => ch_IOCore_to_FPE1PE0_read,
  o_empty => ch_IOCore_to_FPE1PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE2PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE2PE0_a,
  write   => ch_IOCore_to_FPE2PE0_write,
  o_full  => ch_IOCore_to_FPE2PE0_full,

  o_data  => ch_IOCore_to_FPE2PE0_b,
  read    => ch_IOCore_to_FPE2PE0_read,
  o_empty => ch_IOCore_to_FPE2PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE3PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE3PE0_a,
  write   => ch_IOCore_to_FPE3PE0_write,
  o_full  => ch_IOCore_to_FPE3PE0_full,

  o_data  => ch_IOCore_to_FPE3PE0_b,
  read    => ch_IOCore_to_FPE3PE0_read,
  o_empty => ch_IOCore_to_FPE3PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE4PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE4PE0_a,
  write   => ch_IOCore_to_FPE4PE0_write,
  o_full  => ch_IOCore_to_FPE4PE0_full,

  o_data  => ch_IOCore_to_FPE4PE0_b,
  read    => ch_IOCore_to_FPE4PE0_read,
  o_empty => ch_IOCore_to_FPE4PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE5PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE5PE0_a,
  write   => ch_IOCore_to_FPE5PE0_write,
  o_full  => ch_IOCore_to_FPE5PE0_full,

  o_data  => ch_IOCore_to_FPE5PE0_b,
  read    => ch_IOCore_to_FPE5PE0_read,
  o_empty => ch_IOCore_to_FPE5PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE6PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE6PE0_a,
  write   => ch_IOCore_to_FPE6PE0_write,
  o_full  => ch_IOCore_to_FPE6PE0_full,

  o_data  => ch_IOCore_to_FPE6PE0_b,
  read    => ch_IOCore_to_FPE6PE0_read,
  o_empty => ch_IOCore_to_FPE6PE0_empty,
  clk     => clk
);

u_fifo_IOCore_to_FPE7PE0: m_word_fifo
generic map( WIDTH =>INPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_IOCore_to_FPE7PE0_a,
  write   => ch_IOCore_to_FPE7PE0_write,
  o_full  => ch_IOCore_to_FPE7PE0_full,

  o_data  => ch_IOCore_to_FPE7PE0_b,
  read    => ch_IOCore_to_FPE7PE0_read,
  o_empty => ch_IOCore_to_FPE7PE0_empty,
  clk     => clk
);

u_fifo_FPE0PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE0PE0_to_IOCore_a,
  write   => ch_FPE0PE0_to_IOCore_write,
  o_full  => ch_FPE0PE0_to_IOCore_full,

  o_data  => ch_FPE0PE0_to_IOCore_b,
  read    => ch_FPE0PE0_to_IOCore_read,
  o_empty => ch_FPE0PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE1PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE1PE0_to_IOCore_a,
  write   => ch_FPE1PE0_to_IOCore_write,
  o_full  => ch_FPE1PE0_to_IOCore_full,

  o_data  => ch_FPE1PE0_to_IOCore_b,
  read    => ch_FPE1PE0_to_IOCore_read,
  o_empty => ch_FPE1PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE2PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE2PE0_to_IOCore_a,
  write   => ch_FPE2PE0_to_IOCore_write,
  o_full  => ch_FPE2PE0_to_IOCore_full,

  o_data  => ch_FPE2PE0_to_IOCore_b,
  read    => ch_FPE2PE0_to_IOCore_read,
  o_empty => ch_FPE2PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE3PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE3PE0_to_IOCore_a,
  write   => ch_FPE3PE0_to_IOCore_write,
  o_full  => ch_FPE3PE0_to_IOCore_full,

  o_data  => ch_FPE3PE0_to_IOCore_b,
  read    => ch_FPE3PE0_to_IOCore_read,
  o_empty => ch_FPE3PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE4PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE4PE0_to_IOCore_a,
  write   => ch_FPE4PE0_to_IOCore_write,
  o_full  => ch_FPE4PE0_to_IOCore_full,

  o_data  => ch_FPE4PE0_to_IOCore_b,
  read    => ch_FPE4PE0_to_IOCore_read,
  o_empty => ch_FPE4PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE5PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE5PE0_to_IOCore_a,
  write   => ch_FPE5PE0_to_IOCore_write,
  o_full  => ch_FPE5PE0_to_IOCore_full,

  o_data  => ch_FPE5PE0_to_IOCore_b,
  read    => ch_FPE5PE0_to_IOCore_read,
  o_empty => ch_FPE5PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE6PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE6PE0_to_IOCore_a,
  write   => ch_FPE6PE0_to_IOCore_write,
  o_full  => ch_FPE6PE0_to_IOCore_full,

  o_data  => ch_FPE6PE0_to_IOCore_b,
  read    => ch_FPE6PE0_to_IOCore_read,
  o_empty => ch_FPE6PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE7PE0_to_IOCore: m_word_fifo
generic map( WIDTH =>OUTPUT_WIDTH, DEPTH=>8 )
port map(
  i_data  => ch_FPE7PE0_to_IOCore_a,
  write   => ch_FPE7PE0_to_IOCore_write,
  o_full  => ch_FPE7PE0_to_IOCore_full,

  o_data  => ch_FPE7PE0_to_IOCore_b,
  read    => ch_FPE7PE0_to_IOCore_read,
  o_empty => ch_FPE7PE0_to_IOCore_empty,
  clk     => clk
);

u_fifo_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_a,
  write   => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_write,
  o_full  => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_full,

  o_data  => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_b,
  read    => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_read,
  o_empty => ch_FPE0PE0_to_FPE4PE0_FPE2PE0_FPE1PE0_empty,
  clk     => clk
);

u_fifo_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_a,
  write   => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_write,
  o_full  => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_full,

  o_data  => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_b,
  read    => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_read,
  o_empty => ch_FPE1PE0_to_FPE5PE0_FPE3PE0_FPE0PE0_empty,
  clk     => clk
);

u_fifo_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_a,
  write   => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_write,
  o_full  => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_full,

  o_data  => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_b,
  read    => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_read,
  o_empty => ch_FPE2PE0_to_FPE6PE0_FPE0PE0_FPE3PE0_empty,
  clk     => clk
);

u_fifo_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_a,
  write   => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_write,
  o_full  => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_full,

  o_data  => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_b,
  read    => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_read,
  o_empty => ch_FPE3PE0_to_FPE7PE0_FPE1PE0_FPE2PE0_empty,
  clk     => clk
);

u_fifo_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_a,
  write   => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_write,
  o_full  => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_full,

  o_data  => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_b,
  read    => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_read,
  o_empty => ch_FPE4PE0_to_FPE0PE0_FPE6PE0_FPE5PE0_empty,
  clk     => clk
);

u_fifo_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_a,
  write   => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_write,
  o_full  => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_full,

  o_data  => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_b,
  read    => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_read,
  o_empty => ch_FPE5PE0_to_FPE1PE0_FPE7PE0_FPE4PE0_empty,
  clk     => clk
);

u_fifo_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_a,
  write   => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_write,
  o_full  => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_full,

  o_data  => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_b,
  read    => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_read,
  o_empty => ch_FPE6PE0_to_FPE2PE0_FPE4PE0_FPE7PE0_empty,
  clk     => clk
);

u_fifo_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0: m_word_fifo
generic map( WIDTH =>CORE_WIDTH, DEPTH=>32 )
port map(
  i_data  => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_a,
  write   => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_write,
  o_full  => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_full,

  o_data  => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_b,
  read    => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_read,
  o_empty => ch_FPE7PE0_to_FPE3PE0_FPE5PE0_FPE6PE0_empty,
  clk     => clk
);

end Structure;
