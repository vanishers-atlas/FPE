--**
--* Entity spu_commport
--**
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity spu_commput is
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
end spu_commput;

architecture structure of spu_commput is
  signal put_ch_select : std_logic_vector(TX_CH_WIDTH-1 downto 0) := (others=>'0');
begin

o_put_ch_full <= '0';

TXDIRECT_GEN: if PUTCH_EN = false generate
  put_ch_select <= i_put_ch_select;
end generate;

TXIDX_GEN: if PUTCH_EN = true generate
  put_proc: process(clk)
  begin
    if clk'event and clk = '1' then
      if i_tx_reset = '1' then
        put_ch_select <= std_logic_vector(to_unsigned(0, TX_CH_WIDTH));
      elsif i_tx_autoinc = '1' then
        put_ch_select <= std_logic_vector(unsigned(put_ch_select) + 1);
      end if;
    end if;
  end process;
end generate;

---------------------------
-- Output channel
---------------------------
-- Single output channel
single_tx_gen: if (TX_CH_NUM = 1) generate
  o_put_ch_data(0) <= i_put_data;

  u_put_ch_write_reg_Pa3: spu_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>i_put_inst, o_d=>o_put_ch_write(0));
      
  full_gen: if (STATE_EN = true) generate
    o_put_ch_full <= i_put_ch_full(0);
  end generate;
end generate;

-- Multiple output channels
multiple_tx_gen: if (TX_CH_NUM > 1) generate
  signal put_ch_write_demuxout    : VSIG_TYPE(2**TX_CH_WIDTH-1 downto 0);
begin  
  -- Demux write signal
  ch_write: process (put_ch_select, i_put_inst)
  begin
    put_ch_write_demuxout <= (others=>'0');
    put_ch_write_demuxout(to_integer(unsigned(put_ch_select))) <= i_put_inst;
  end process;
  
  -- Wiring & buffering
  -- To improve frequency, the write pipeline register is shifted after the 
  -- demux. Read is dealt with in the same way. Then the FIFO datapath is 
  -- seperated by pipleine registers, so FIFO placement is free to be the 
  -- best point for all connected SPEs.
  put_ch_write_buf_replication_gen: for i in 0 to TX_CH_NUM-1 generate
    u_put_ch_write_reg_Pa3: spu_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>put_ch_write_demuxout(i), o_d=>o_put_ch_write(i));
  end generate;
  
  -- Broadcast data signal
  put_data_broadcast_gen: for i in 0 to TX_CH_NUM-1 generate
    o_put_ch_data(i) <= i_put_data;
  end generate;
end generate;
end structure;