--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.ALL;

package generic_multiplexers is
  component generic_mux_2to1
    generic ( DATA_WIDTH:integer := 16 );
    port (
      i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      sel     : in std_logic;
      o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0)
    );
  end component;

  component generic_mux_3to1
    generic ( DATA_WIDTH:integer := 16 );
    port (
      i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
      sel     : in std_logic_vector(1 downto 0)
    );
  end component;

  component generic_mux_4to1 is
    generic (DATA_WIDTH:integer := 16);
    port (
      i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      i_d3    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
      o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
      sel     : in std_logic_vector(2 downto 0)
    );
  end component;
end package;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_mux_2to1 is
  generic ( DATA_WIDTH:integer := 16 );
  port (
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic;
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0)
  );
end entity;

architecture behav of generic_mux_2to1 is
begin
  o_d <= i_d0 when (sel = '0') else  i_d1;
end architecture;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_mux_3to1 is
  generic ( DATA_WIDTH:integer := 16 );
  port (
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(1 downto 0)
  );
end entity;

architecture behav of generic_mux_3to1 is
begin
  process (i_d0, i_d1, i_d2, sel) begin
    case (sel) is
      when "00" => o_d <= i_d0;
      when "01" => o_d <= i_d1;
      when "10" => o_d <= i_d2;
      when others => o_d <= i_d0;
    end case;
  end process;
end architecture;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_mux_4to1 is
  generic (DATA_WIDTH:integer := 16);
  port (
    i_d0    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d1    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d2    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    i_d3    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
    o_d     : out std_logic_vector(DATA_WIDTH-1 downto 0);
    sel     : in std_logic_vector(2 downto 0)
  );
end entity;

architecture behav of generic_mux_4to1 is
begin
  process (i_d0, i_d1, i_d2, i_d3, sel) begin
    case (sel) is
      when "000" => o_d <= i_d0;
      when "001" => o_d <= i_d1;
      when "010" => o_d <= i_d2;
      when "100" => o_d <= i_d3;
      when others => o_d <= i_d0;
    end case;
  end process;
end architecture;
