--**
--* Entity iocore_commport
--**

-- almostfull stall pipeline strategy is not supported now. Status signals are all tied to zeros.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity iocore_commport is
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
end iocore_commport;

architecture structure of iocore_commport is
  signal put_ch_full_Pa2 : std_logic := '0';
  signal get_ch_select   : std_logic_vector(RX_CH_WIDTH-1 downto 0) := (others=>'0');
  signal put_ch_select   : std_logic_vector(TX_CH_WIDTH-1 downto 0) := (others=>'0');
  signal mc_tx_code      : std_logic_vector(2**TX_CH_WIDTH-1 downto 0) := (others=>'0');
begin
o_get_ch_empty <= '0';
o_put_ch_full <= '0';

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

TXDIRECT_GEN: if PUTCH_EN = false generate
  put_ch_select <= i_put_ch_select;
end generate;

TXIDX_GEN: if PUTCH_EN = true and TX_MC_EN = false generate
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

TXMC_GEN: if PUTCH_EN = true and TX_MC_EN = true generate
  put_proc: process(clk)
  begin
      if clk'event and clk = '1' then
        if i_tx_mcs = '1' then
          mc_tx_code <= mc_tx_code(2**TX_CH_WIDTH-1 downto 1) & '1';
        elsif i_tx_mcc = '1' then
          mc_tx_code <= mc_tx_code(2**TX_CH_WIDTH-1 downto 1) & '0';
        elsif (i_put_broadcast = '1') then      
          mc_tx_code <= (others=>'1');
      end if;
  end process;
end generate;

---------------------------
-- Input channel
---------------------------
-- Single input channel
single_rx_gen: if (RX_CH_NUM = 1) generate
  signal get_inst_Pa1        : std_logic;
begin
  u_buf_get_Pa1: m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>i_get_inst, o_d=>get_inst_Pa1);
  u_buf_get_Pa1x: m_word_generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>get_inst_Pa1, o_d=>o_get_ch_read(0));
      
  u_get_data_reg_Pa3: m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>INNERWIDTH)
    port map(clk=>clk, rst=>rst, i_d=>i_get_ch_data(0)(INNERWIDTH-1 downto 0), o_d=>o_get_data);
    
  empty_gen: if (STATE_EN = true) generate
    u_get_empty_reg_Pa3: m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>i_get_ch_empty(0), o_d=>o_get_ch_empty);
  end generate;
  
end generate;

-- Multiple input channels
multi_rx_gen: if (RX_2LEV_EN = false and RX_CH_NUM > 1) generate
  signal get_data_muxout     : std_logic_vector(INNERWIDTH-1 downto 0);
  signal get_ch_select_Pa1   : std_logic_vector(RX_CH_WIDTH-1 downto 0);
  signal get_ch_select_Pa1x  : std_logic_vector(RX_CH_WIDTH-1 downto 0);
  signal get_ch_select_Pa2   : std_logic_vector(RX_CH_WIDTH-1 downto 0);
  signal get_ch_data_Pa2     : VDATA_TYPE(RX_CH_NUM-1 downto 0);
  signal get_inst_Pa1        : std_logic;
  signal get_inst_Pa1x       : std_logic;
  signal get_inst_Pa2        : std_logic;
  signal get_ch_read_demuxout     : VSIG_TYPE(RX_CH_NUM-1 downto 0);
begin
  -- Demux read signal
  ch_read: process (get_ch_select, i_get_inst)
  begin
    get_ch_read_demuxout <= (others=>'0');
    if i_get_inst = '1' then
      -- pragma translate_off
      if to_integer(unsigned(get_ch_select)) < RX_CH_NUM then
      -- pragma translate_on
      get_ch_read_demuxout(to_integer(unsigned(get_ch_select))) <= i_get_inst;
      -- pragma translate_off
      end if;
      -- pragma translate_on
    end if;
  end process;

  get_buf_repli_gen:
  for i in 0 to RX_CH_NUM-1 generate
    u_buf_get_Pa1: m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>get_ch_read_demuxout(i), o_d=>o_get_ch_read(i));
  end generate;
  
  -- Mux data
  u_get_inst_Pa1: m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>i_get_inst, o_d=>get_inst_Pa1);
  u_get_inst_Pa1x: m_word_generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>get_inst_Pa1, o_d=>get_inst_Pa1x);
  u_get_inst_Pa2: m_word_generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>get_inst_Pa1x, o_d=>get_inst_Pa2);
      
  u_get_ch_sel_reg_Pa1:m_word_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>RX_CH_WIDTH)
  port map(clk=>clk, rst=>open, i_d=>get_ch_select, o_d=>get_ch_select_Pa1);
  u_get_ch_sel_reg_Pa1x:m_word_generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>RX_CH_WIDTH)
  port map(clk=>clk, rst=>open, i_d=>get_ch_select_Pa1, o_d=>get_ch_select_Pa1x);
  u_get_ch_sel_reg_Pa2:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH)
  port map(clk=>clk, rst=>open, i_d=>get_ch_select_Pa1x, o_d=>get_ch_select_Pa2);
  
  get_ch_data_Pa2 <= i_get_ch_data;
  
  proc_get_data: process (get_inst_Pa2, get_ch_select_Pa2, get_ch_data_Pa2) begin
    get_data_muxout <= (others=>'X');
    if get_inst_Pa2 = '1' then
      -- pragma translate_off
      if to_integer(unsigned(get_ch_select_Pa2)) < RX_CH_NUM then
      -- pragma translate_on
      get_data_muxout <= get_ch_data_Pa2(to_integer(unsigned(get_ch_select_Pa2)))(INNERWIDTH-1 downto 0);
      -- pragma translate_off
      end if;
      -- pragma translate_on
    end if;
  end process;

  u_get_data_reg_Pa3: m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>INNERWIDTH)
    port map(clk=>clk, rst=>rst, i_d=>get_data_muxout, o_d=>o_get_data);
  
end generate;

multi_rx_2levs_gen: if (RX_2LEV_EN = true) generate
  signal get_ch_select_l0_Pa0 : std_logic_vector(RX_CH_WIDTH0-1 downto 0);
  signal get_ch_select_l0_Pa0x: std_logic_vector(RX_CH_WIDTH0-1 downto 0);
  signal get_ch_select_l0_Pa1 : std_logic_vector(RX_CH_WIDTH0-1 downto 0);
  signal get_ch_select_l0_Pa2 : std_logic_vector(RX_CH_WIDTH0-1 downto 0);
  signal get_ch_select_l0_Pa2x: std_logic_vector(RX_CH_WIDTH0-1 downto 0);
  signal get_ch_select_l1_Pa0 : std_logic_vector(RX_CH_WIDTH1-1 downto 0);
  signal get_ch_select_l1_Pa0x: std_logic_vector(RX_CH_WIDTH1-1 downto 0);
  signal get_ch_select_l1_Pa1 : std_logic_vector(RX_CH_WIDTH1-1 downto 0);
  signal get_ch_select_l1_Pa2 : std_logic_vector(RX_CH_WIDTH1-1 downto 0);
  signal get_ch_read_demuxout_l0 : std_logic_vector(2**RX_CH_WIDTH0-1 downto 0);
  signal get_ch_read_demuxout_l0_Pa0x : std_logic_vector(2**RX_CH_WIDTH0-1 downto 0);
  type READ_LEV2_TYPE is array(0 to 2**RX_CH_WIDTH0-1) of std_logic_vector(2**RX_CH_WIDTH1-1 downto 0);
  signal get_ch_read_demuxout_l1 : READ_LEV2_TYPE;
  signal get_ch_read_demuxout_l1_Pa0x : std_logic_vector(RX_CH_NUM-1 downto 0);
  
  type READDATA_LEV1_TYPE is array(0 to 2**RX_CH_WIDTH1-1) of std_logic_vector(INNERWIDTH-1 downto 0);  
  type READDATA_TYPE is array(0 to 2**RX_CH_WIDTH0-1) of READDATA_LEV1_TYPE;  
  signal get_ch_data_Pa2 : READDATA_TYPE;
  type MUXDATA_TYPE is array(0 to 2**RX_CH_WIDTH1-1) of std_logic_vector(INNERWIDTH-1 downto 0);
  signal get_data_muxout_l1 : MUXDATA_TYPE;
  signal get_data_muxout_l1_Pa2x : MUXDATA_TYPE;
  signal get_data_muxout_l0 : std_logic_vector(INNERWIDTH-1 downto 0);
begin

  -- signals generation
  get_ch_select_l0_Pa0 <= get_ch_select(RX_CH_WIDTH-1 downto RX_CH_WIDTH-RX_CH_WIDTH0);
  get_ch_select_l1_Pa0 <= get_ch_select(RX_CH_WIDTH1-1 downto 0);
  
  -- Demux read signal
  -- level 0
  ch_read_l0: process (get_ch_select_l0_Pa0, i_get_inst)
  begin
    get_ch_read_demuxout_l0 <= (others=>'X');
    get_ch_read_demuxout_l0(to_integer(unsigned(get_ch_select_l0_Pa0))) <= i_get_inst;      
  end process;
  
  -- buffering
  u_buf_get_ch_read_demuxout_l0_Pa0x:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>2**RX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_read_demuxout_l0, o_d=>get_ch_read_demuxout_l0_Pa0x);
  
  -- level 1
  demux_read_lev1_gen: for i in 0 to 2**RX_CH_WIDTH0-1 generate
    ch_read_l1: process (get_ch_read_demuxout_l0_Pa0x, get_ch_select_l1_Pa0x)
    begin
      get_ch_read_demuxout_l1(i) <= (others=>'X');
      get_ch_read_demuxout_l1(i)(to_integer(unsigned(get_ch_select_l1_Pa0x))) <= get_ch_read_demuxout_l0_Pa0x(i);      
    end process;
  end generate;
  
  -- wire connect & buffering
  read_wire_gen: for i in 0 to RX_CH_NUM-1 generate
    get_ch_read_demuxout_l1_Pa0x(i) <= get_ch_read_demuxout_l1(i/2**RX_CH_WIDTH0)(i mod 2**RX_CH_WIDTH0);
    
    u_buf_get_Pa1: m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>get_ch_read_demuxout_l1_Pa0x(i), o_d=>o_get_ch_read(i));
  end generate;
  
  -- Mux read data
  u_buf_get_ch_select_l0_Pa0x:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l0_Pa0, o_d=>get_ch_select_l0_Pa0x);
  u_buf_get_ch_select_l0_Pa1:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l0_Pa0x, o_d=>get_ch_select_l0_Pa1);
  u_buf_get_ch_select_l0_Pa2:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l0_Pa1, o_d=>get_ch_select_l0_Pa2);  
  u_buf_get_ch_select_l0_Pa2x:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l0_Pa2, o_d=>get_ch_select_l0_Pa2x);
  
  u_buf_get_ch_select_l1_Pa0x:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH1) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l1_Pa0, o_d=>get_ch_select_l1_Pa0x);   
  u_buf_get_ch_select_l1_Pa1:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH1) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l1_Pa0, o_d=>get_ch_select_l1_Pa1);
  u_buf_get_ch_select_l1_Pa2:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RX_CH_WIDTH1) 
    port map(clk=>clk, rst=>open, i_d=>get_ch_select_l1_Pa1, o_d=>get_ch_select_l1_Pa2);
  
  -- read data wire connect
  read_data_wire_gen: for i in 0 to RX_CH_NUM-1 generate
    get_ch_data_Pa2(i/2**RX_CH_WIDTH0)(i mod 2**RX_CH_WIDTH0) <= i_get_ch_data(i);
  end generate;
  
  -- read data level 1
  mux_read_data_l1: for i in 0 to 2**RX_CH_WIDTH0-1 generate
    read_data_l1_proc: process (get_ch_data_Pa2(i), get_ch_select_l1_Pa2)
    begin
      get_data_muxout_l1(i) <= get_ch_data_Pa2(i)(to_integer(unsigned(get_ch_select_l1_Pa2)));
    end process;
  end generate;
  
  -- buffering
  muxout_buf_gen: for i in 0 to 2**RX_CH_WIDTH1-1 generate
    u_get_data_muxout_Pa2x: m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>INNERWIDTH)
      port map(clk=>clk, rst=>rst, i_d=>get_data_muxout_l1(i), o_d=>get_data_muxout_l1_Pa2x(i));
  end generate;
  
  -- read data level 0
  read_data_l0_proc: process (get_data_muxout_l1_Pa2x, get_ch_select_l0_Pa2x)
  begin
    get_data_muxout_l0 <= get_data_muxout_l1_Pa2x(to_integer(unsigned(get_ch_select_l0_Pa2x)));
  end process;
  
  -- buffering
  u_get_data_Pa3: m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>INNERWIDTH)
    port map(clk=>clk, rst=>rst, i_d=>get_data_muxout_l0, o_d=>o_get_data);
end generate;
---------------------------
-- Output channel
---------------------------
-- Single output channel
single_tx_gen: if (TX_CH_NUM = 1) generate
  o_put_ch_data(0)(INNERWIDTH-1 downto 0) <= i_put_data;

  u_put_ch_write_reg_Pa3: m_word_generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>i_put_inst, o_d=>o_put_ch_write(0));
      
  full_gen: if (STATE_EN = true) generate
    put_ch_full_Pa2 <= i_put_ch_full(0);
    
    u_put_ch_full_Pa3: m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>put_ch_full_Pa2, o_d=>o_put_ch_full);
  end generate;
end generate;

-- Multiple output channels
multiple_tx_gen: if (TX_2LEV_EN = false and TX_CH_NUM > 1) generate
  
begin  
  -- Demux write signal
  MC_OFF: if (TX_MC_EN = false) generate
    signal put_ch_write_demuxout    : VSIG_TYPE(2**TX_CH_WIDTH-1 downto 0);
  begin
    ch_write: process (put_ch_select, i_put_inst)
    begin
      put_ch_write_demuxout <= (others=>'0');
      if (i_put_inst = '1') then
        put_ch_write_demuxout(to_integer(unsigned(put_ch_select))) <= i_put_inst;
      elsif (i_put_broadcast = '1') then      
        put_ch_write_demuxout <= (others=>'1');
      end if;
    end process;
    
    put_ch_write_buf_replication_gen:
    for i in 0 to TX_CH_NUM-1 generate
      u_put_ch_write_reg_Pa3: m_word_generic_reg1 generic map(REG_NUM=>1)
        port map(clk=>clk, rst=>rst, i_d=>put_ch_write_demuxout(i), o_d=>o_put_ch_write(i));
    end generate;
  end generate;
  
  MC_ON: if (TX_MC_EN = true) generate
    signal put_ch_write_demuxout : VSIG_TYPE(2**TX_CH_WIDTH-1 downto 0);
  begin
    mc_and: for i in 0 to TX_CH_NUM-1 generate
      put_ch_write_demuxout(i) <= i_put_inst and mc_tx_code(i);
    end generate;
    
    put_ch_write_buf_replication_gen:
    for i in 0 to TX_CH_NUM-1 generate
      u_put_ch_write_reg_Pa3: m_word_generic_reg1 generic map(REG_NUM=>1)
        port map(clk=>clk, rst=>rst, i_d=>put_ch_write_demuxout(i), o_d=>o_put_ch_write(i));
    end generate;
  end generate;
  
  -- Broadcast data signal
  put_data_broadcast_gen:
  for i in 0 to TX_CH_NUM-1 generate
    o_put_ch_data(i)(INNERWIDTH-1 downto 0) <= i_put_data;
  end generate;
end generate;

multi_tx_2levs_gen: if (TX_2LEV_EN = true) generate
  signal put_ch_select_l0_Pa2 : std_logic_vector(TX_CH_WIDTH0-1 downto 0);
  signal put_ch_select_l1_Pa2 : std_logic_vector(TX_CH_WIDTH1-1 downto 0);
  signal put_ch_select_l1_Pa3: std_logic_vector(TX_CH_WIDTH1-1 downto 0);
  signal put_ch_write_demuxout_l0 : std_logic_vector(2**TX_CH_WIDTH0-1 downto 0);
  signal put_ch_write_demuxout_l0_Pa3 : std_logic_vector(2**TX_CH_WIDTH0-1 downto 0);
  type WRITE_LEV2_TYPE is array(0 to 2**TX_CH_WIDTH0-1) of std_logic_vector(2**TX_CH_WIDTH1-1 downto 0);
  signal put_ch_write_demuxout_l1 : WRITE_LEV2_TYPE;
  signal put_ch_write_demuxout_l1_Pa3 : std_logic_vector(TX_CH_NUM-1 downto 0);
  
  type WRITEDATA_LEV1_TYPE is array(0 to 2**TX_CH_WIDTH1-1) of std_logic_vector(INNERWIDTH-1 downto 0);  
  type WRITEDATA_TYPE is array(0 to 2**TX_CH_WIDTH0-1) of WRITEDATA_LEV1_TYPE;  
  signal put_data_broadcast : WRITEDATA_TYPE;
  
  type WRITEDATA_LEV0_TYPE is array(0 to 2**RX_CH_WIDTH1-1) of std_logic_vector(INNERWIDTH-1 downto 0);
  signal put_data_broadcast_Pa3x : WRITEDATA_LEV0_TYPE;
begin
  -- signals generation
  put_ch_select_l0_Pa2 <= put_ch_select(TX_CH_WIDTH-1 downto TX_CH_WIDTH-TX_CH_WIDTH0);
  put_ch_select_l1_Pa2 <= put_ch_select(TX_CH_WIDTH1-1 downto 0);
  
  u_buf_put_ch_select_l1_Pa3:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>TX_CH_WIDTH1) 
    port map(clk=>clk, rst=>open, i_d=>put_ch_select_l1_Pa2, o_d=>put_ch_select_l1_Pa3);   

  -- Demux write signal
  -- level 0
  ch_write_l0: process (put_ch_select_l0_Pa2, i_put_inst)
  begin
    put_ch_write_demuxout_l0 <= (others=>'X');
    put_ch_write_demuxout_l0(to_integer(unsigned(put_ch_select_l0_Pa2))) <= i_put_inst;      
  end process;
  
  -- buffering
  u_buf_put_ch_write_demuxout_l0_Pa3:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>2**TX_CH_WIDTH0) 
    port map(clk=>clk, rst=>open, i_d=>put_ch_write_demuxout_l0, o_d=>put_ch_write_demuxout_l0_Pa3);
  
  -- level 1
  demux_write_lev1_gen: for i in 0 to 2**TX_CH_WIDTH0-1 generate
    ch_write_l1: process (put_ch_write_demuxout_l0_Pa3, put_ch_select_l1_Pa3)
    begin
      put_ch_write_demuxout_l1(i) <= (others=>'X');
      put_ch_write_demuxout_l1(i)(to_integer(unsigned(put_ch_select_l1_Pa3))) <= put_ch_write_demuxout_l0_Pa3(i);      
    end process;
  end generate;
  
  -- wire connect & buffering
  write_wire_gen: for i in 0 to TX_CH_NUM-1 generate
    put_ch_write_demuxout_l1_Pa3(i) <= put_ch_write_demuxout_l1(i/2**TX_CH_WIDTH0)(i mod 2**TX_CH_WIDTH0);
    
    u_buf_put_Pa3x: m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>put_ch_write_demuxout_l1_Pa3(i), o_d=>o_put_ch_write(i));
  end generate;
  
  -- Broadcast write data  
  -- buffering
  broadcast_buf_gen: for i in 0 to 2**TX_CH_WIDTH0-1 generate
    u_put_data_broadcast_Pa3x: m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>INNERWIDTH)
      port map(clk=>clk, rst=>rst, i_d=>i_put_data, o_d=>put_data_broadcast_Pa3x(i));
  end generate;
  
  -- buffering level 1
  broadcast_l1_gen: for i in 0 to 2**TX_CH_WIDTH0-1 generate
    broadcast_l1_inner_gen: for j in 0 to 2**TX_CH_WIDTH1-1 generate
      put_data_broadcast(i)(j) <= put_data_broadcast_Pa3x(i);
    end generate;
  end generate;
    
  -- write data wire connectc
  write_data_wire_gen: for i in 0 to TX_CH_NUM-1 generate
    o_put_ch_data(i) <= put_data_broadcast(i/2**TX_CH_WIDTH0)(i mod 2**TX_CH_WIDTH0);
  end generate;  
end generate;

end structure;