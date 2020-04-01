--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package sFPE_typedef is
  type VDATA_TYPE is array (natural range <>) of std_logic_vector(31 downto 0);
  type VSIG_TYPE is array (natural range <>) of std_logic;

  -- Constant types for flexible ports
  constant constFLEX_R   : integer := 1;
  constant constFLEX_M   : integer := 2;
  constant constFLEX_RM  : integer := 3;
  constant constFLEX_I   : integer := 4;
  constant constFLEX_RI  : integer := 5;
  constant constFLEX_MI  : integer := 6;
  constant constFLEX_RMI : integer := 7;
  constant constFLEX_F   : integer := 8;
  constant constFLEX_RF  : integer := 9;
  constant constFLEX_MF  : integer := 10;
  constant constFLEX_RMF : integer := 11;
  constant constFLEX_IF  : integer := 12;
  constant constFLEX_RIF : integer := 13;
  constant constFLEX_MIF : integer := 14;
  constant constFLEX_RMIF: integer := 15;
end;
