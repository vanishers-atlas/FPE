library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.ssp_typedef.all;
use work.ssp_instencoding.all;
use work.ssp_pkg.all;

entity iocore_id is
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
end iocore_id;

architecture structure of iocore_id is

  -- Help functions
  signal  opc : std_logic_vector(5 downto 0);
  
  signal id_get : std_logic := '0';
  signal id_put : std_logic := '0';
  signal id_rx_autoinc : std_logic := '0';
  signal id_rx_reset : std_logic := '0';
  signal id_tx_autoinc : std_logic := '0';
  signal id_tx_reset : std_logic := '0';
  signal id_b : std_logic := '0';
  signal id_rpt : std_logic := '0';
  signal id_em_ldexmem    : std_logic;
  signal id_em_ldcache    : std_logic;
  signal id_em_stexmem    : std_logic;
  signal id_em_stcache    : std_logic;
  
  signal cnter : std_logic_vector(1 downto 0) := "00";
  type state_type is (s_nml, s_wait);
  signal state: state_type;
  
  signal  id_barrier : std_logic := '0';
begin

opc <= i_pm_do(31 downto 26);

-- branch inst
o_id_b <= id_b;
o_id_rpt <= id_rpt;

jmp_gen:
if JMP_EN = true generate  
  id_b <= '1' when (opc = IO_JMP) else '0';
end generate;

rpt_gen:
if RPT_EN = true generate  
  id_rpt <= '1' when (opc = IO_RPT) else '0';
end generate;

--put/get inst
o_id_put  <=  id_put;
o_id_get  <=  id_get;

id_put    <= '1' when (opc = IO_LDCACHE) else '0';
id_get    <= '1' when (opc = IO_STCACHE) else '0';

-- getch
o_id_rx_autoinc <= id_rx_autoinc;
o_id_rx_reset   <= id_rx_reset;
id_getch_gen: if GETCH_EN = true generate
  id_rx_autoinc <= '1' when (id_get = '1' and i_pm_do(1) = '1') or (opc = IO_INCRXIDXBY1) else '0';
  id_rx_reset <= '1' when (opc = IO_RESETRXIDX) else '0';
end generate;

-- putch
o_id_tx_autoinc <= id_tx_autoinc;
o_id_tx_reset   <= id_tx_reset;
id_putch_gen: if PUTCH_EN = true generate
  id_tx_autoinc <= '1' when (id_put = '1' and i_pm_do(16) = '1') or (opc = IO_INCTXIDXBY1) else '0';
  id_tx_reset <= '1' when (opc = IO_RESETTXIDX) else '0';
end generate;

o_id_em_ldexmem <= id_em_ldexmem;
o_id_em_ldcache <= id_em_ldcache;
o_id_em_stexmem <= id_em_stexmem;
o_id_em_stcache <= id_em_stcache;

o_id_txbroadcast <= '1' when (opc = IO_LDCACHE_BROADCAST) else '0';
o_id_txmcs <= '1' when (opc = IO_LDCACHEMC_S) else '0';
o_id_txmcc <= '1' when (opc = IO_LDCACHEMC_C) else '0';
o_id_em_shiftcacheline <= '1' when (opc = IO_SHIFTCACHELINE) else '0';
id_em_ldexmem <= '1' when (opc = IO_LDEXMEM) else '0';
id_em_ldcache <= '1' when opc = IO_LDCACHE or opc = IO_LDCACHE_BROADCAST or
  opc = IO_LDCACHEMC or opc = IO_LDCACHEMC_S or opc = IO_LDCACHEMC_C else '0';
id_em_stexmem <= '1' when (opc = IO_STEXMEM) else '0';
id_em_stcache <= '1' when (opc = IO_STCACHE) else '0';

o_id_em_inc_rb_0 <= '1'   when (opc = IO_INCEMRB_0) else '0';
o_id_em_inc_rb_1 <= '1'   when (opc = IO_INCEMRB_1) else '0';
o_id_em_inc_wb_0  <= '1'  when (opc = IO_INCEMWB_0)    else '0';
o_id_em_autoinc_rb <= '1' when id_em_ldexmem = '1' and i_pm_do(1) = '1' else '0';
o_id_em_autoinc_wb <= '1' when id_em_stexmem = '1' and i_pm_do(2) = '1' else '0';

-- en_pc
o_en_pc <= '0' when (opc = IO_LDEXMEM and i_mif_rd_valid = '0') or 
           ((opc = IO_BARRIERS) and i_ext_barrier = '0') else '1';

-- en_spu
-- every time both reaches barrier point, it needs to wait several cycles to recover spu (to
-- deassert i_ext_barrier). IOCore keeps running after it checks barrier point, so if we do not
-- have a state of 'wait', o_ext_en_spu will be wrongly asserted agian.
process (clk) begin
  if (clk'event and clk = '1') then
    case state is
        when s_nml =>
          if (opc = IO_BARRIERS and i_ext_barrier = '1') then
            state <= s_wait;
          end if;
        when s_wait =>
          if (cnter = "11") then
            state <= s_nml;
          end if;
          cnter <= std_logic_vector(unsigned(cnter)+1);
    end case;
  end if;
end process;

o_ext_en_spu <= '0' when (state = s_nml and opc /= IO_BARRIERS and i_ext_barrier = '1') else '1';

end structure;