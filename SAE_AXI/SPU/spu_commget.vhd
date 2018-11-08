--**
--* Entity spu_commport
--**
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity spu_commget is
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
end spu_commget;

architecture structure of spu_commget is
  signal get_ch_select   : std_logic_vector(RX_CH_WIDTH-1 downto 0) := (others=>'0');
  signal get_data : std_logic_vector(DATA_WIDTH-1 downto 0);
begin

o_get_ch_empty <= '0';

RXDIRECT_GEN: if GETCH_EN = false generate
  get_ch_select <= i_get_ch_select;
end generate;

RXIDX_GEN: if GETCH_EN = true generate
  get_proc: process(clk)
  begin
    if clk'event and clk = '1' then
      if i_rx_reset = '1' then
        get_ch_select <= std_logic_vector(to_unsigned(0, RX_CH_WIDTH));
      elsif i_rx_autoinc = '1' then
        get_ch_select <= std_logic_vector(unsigned(get_ch_select) + 1);
      end if;
    end if;
  end process;
end generate;

assert (OUT_DATA_WIDTH <= DATA_WIDTH)
  report "OUT_DATA_WIDTH > DATA_WIDTH not supported"
severity failure;

---------------------------
-- Input channel
---------------------------
-- Single input channel
single_rx_gen: if (RX_CH_NUM = 1) generate
begin  
  u_buf_get_Pb3: spu_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>i_get_inst, o_d=>o_get_ch_read(0));
      
  u_get_data_reg_Pa1: spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>i_get_ch_data(0), o_d=>get_data);
  
  o_get_data <= get_data(OUT_DATA_WIDTH-1 downto 0);
    
  empty_gen: if (STATE_EN = true) generate
    u_get_empty_reg_Pa1: spu_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>i_get_ch_empty(0), o_d=>o_get_ch_empty);
  end generate;
  
end generate;

-- Multiple input channels
multi_rx_gen: if (RX_CH_NUM > 1) generate
  signal get_data_muxout     : std_logic_vector(DATA_WIDTH-1 downto 0);
  signal get_ch_select_Pb3   : std_logic_vector(RX_CH_WIDTH-1 downto 0);
  signal get_ch_select_Pa0   : std_logic_vector(RX_CH_WIDTH-1 downto 0);
  signal get_ch_data_Pa0     : VDATA_TYPE(2**RX_CH_WIDTH-1 downto 0);
  signal get_ch_read_demuxout: VSIG_TYPE(2**RX_CH_WIDTH-1 downto 0);
begin
  -- This i_get_inst is at the stage Pb2. So the following buffers the demux for
  -- read signal (between Pb2 and Pb3).
  -- 1a. Demux read signal
  ch_read: process (get_ch_select, i_get_inst)
  begin
    get_ch_read_demuxout <= (others=>'0');
    get_ch_read_demuxout(to_integer(unsigned(get_ch_select))) <= i_get_inst;
  end process;

  -- 1b. Wiring & buffering
  get_buf_gen: for i in 0 to RX_CH_NUM-1 generate
    u_buf_get_Pb3: spu_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>get_ch_read_demuxout(i), o_d=>o_get_ch_read(i));
  end generate;
  
  -- 2. Mux data
  -- 2a. signal 'select' pipeline
  u_get_ch_sel_reg_Pa1:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>get_ch_select, o_d=>get_ch_select_Pb3);
  u_get_ch_sel_reg_Pa2:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>get_ch_select_Pb3, o_d=>get_ch_select_Pa0);
  
  -- 2b. Wiring
  get_data_wiring_gen: for i in 0 to RX_CH_NUM-1 generate
    get_ch_data_Pa0(i) <= i_get_ch_data(i);
  end generate;

  proc_get_data: process (get_ch_select_Pa0, get_ch_data_Pa0) begin
    get_data_muxout <= get_ch_data_Pa0(to_integer(unsigned(get_ch_select_Pa0))); 
  end process;

  -- 2c. data pipeline & asymmetric width
  u_get_data_reg_Pa1: spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>get_data_muxout, o_d=>get_data);
  o_get_data <= get_data(OUT_DATA_WIDTH-1 downto 0);

end generate;
end structure;
