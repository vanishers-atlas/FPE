library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package iocore_instencoding is
  constant IO_NOP : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(0, 6));  
  constant IO_BARRIERS : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(1, 6));
  constant IO_JMP : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(2, 6));
  constant IO_RPT : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(3, 6));
  constant IO_INCRXIDXBY1 : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(4, 6));
  constant IO_RESETRXIDX : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(5, 6));
  constant IO_INCTXIDXBY1 : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(6, 6));
  constant IO_RESETTXIDX : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(7, 6));
  constant IO_LDCACHE    : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(8, 6));
  constant IO_STCACHE    : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(9, 6));
  constant IO_LDCACHE_BROADCAST : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(10, 6));
  constant IO_LDCACHEMC_S : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(11, 6));
  constant IO_LDCACHEMC_C : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(12, 6));
  constant IO_SHIFTCACHELINE : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(13, 6));
  constant IO_INCEMRB_0 : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(14, 6));
  constant IO_INCEMRB_1 : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(15, 6));
  constant IO_INCEMWB_0 : std_logic_vector(5 downto 0) := std_logic_vector(to_unsigned(16, 6));
end;