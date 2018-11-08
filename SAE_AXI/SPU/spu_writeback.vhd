library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
library work;
use work.ssp_pkg.all;

entity spu_writeback is
generic(
  CORE_DATA_WIDTH : integer := 32;
  ABSDIFF_EN : boolean := true;
  ALUSRA_EN  : boolean := true;
  DECONST_EN  : boolean := true  
);
port(
  i_dsp48_result: in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_dsp48sra_result: in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  i_alusra : in std_logic;  
  i_CA_absdiff : in std_logic;
  i_CA_absdiff_d : in std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  i_CA_deconst : in std_logic;   
  i_deconst_out : in std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  o_result  : out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)
);
end spu_writeback;

architecture structure of spu_writeback is
  signal absdiff :  std_logic := '0';
  signal alusra :  std_logic := '0';
  signal deconst :  std_logic := '0';
  signal result_mux  :  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
begin

ABSDIFF_GEN: if ABSDIFF_EN = true generate  
  absdiff <= i_CA_absdiff;
end generate;

ALUSRA_GEN: if ALUSRA_EN = true generate
  alusra <= i_alusra;
end generate;

DECONST_GEN: if DECONST_EN = true generate
  deconst <= i_CA_deconst;
end generate;
-----------------------------------------------------------------------
-- RESULT SELECTION & WB STAGE
-----------------------------------------------------------------------
-- Result selection
result_sel_proc:process(alusra, absdiff, i_CA_absdiff_d, 
				i_dsp48sra_result, i_dsp48_result, deconst, i_deconst_out)
begin
  if alusra = '1' then
    result_mux <= i_dsp48sra_result;
  elsif absdiff = '1' then
    result_mux <= i_CA_absdiff_d;
  elsif deconst = '1' then
    result_mux <= i_deconst_out;
  else
    result_mux <= i_dsp48_result;
  end if;
end process;

o_result <= result_mux;
end structure;
