library ieee;
use ieee.std_logic_1164.all;

package ssp_typedef is
type VDATA_TYPE is array (natural range <>) of std_logic_vector(31 downto 0);
  type VSIG_TYPE is array (natural range <>) of std_logic;
type VSDATA_TYPE is array (natural range <>) of std_logic_vector(63 downto 0);
end;
