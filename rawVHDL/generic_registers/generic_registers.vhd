--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.ALL;

package generic_registers is
  component generic_reg
    generic(
      REG_NUM  : integer := 2;
      REG_WIDTH : integer := 16
    );
    port(
      clk      : in std_logic;
      rst      : in std_logic := '0';
      i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
      o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
    );
  end component;

  component generic_reg_with_en is
    generic(
      REG_NUM  : integer := 2;
      REG_WIDTH : integer := 16
    );
    port(
      clk      : in std_logic;
      rst      : in std_logic := '0';
      i_en     : in std_logic;
      i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
      o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
    );
  end component;

  component generic_reg1
    generic(REG_NUM  : integer := 2);
    port(
      clk      : in std_logic;
      rst      : in std_logic := '0';
      i_d      : in std_logic;
      o_d      : out std_logic := '0'
    );
  end component;

  component generic_reg1_with_en is
    generic( REG_NUM  : integer := 2 );
    port(
      clk      : in std_logic;
      rst      : in std_logic := '0';
      i_en     : in std_logic;
      i_d      : in std_logic;
      o_d      : out std_logic := '0'
    );
  end component;
end package;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_reg is
  generic(
    REG_NUM  : integer := 2;
    REG_WIDTH : integer := 16
  );
  port(
    clk      : in std_logic;
    rst      : in std_logic := '0';
    i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
    o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
  );
end generic_reg;

architecture behav of generic_reg is
begin
  --Act as a wire
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  --A raising edge single reg
  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        o_d <= i_d;
      end if;
    end process P1;
  end generate GR1;

  --Act as a FIFO
  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic_vector(REG_WIDTH - 1 downto 0);
    signal t_reg_in : type_in_reg := (others=>(others=>'0'));
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then
        t_reg_in(REG_NUM - 1) <= i_d;
        t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
      end if;
    end process P1;
  end generate GR2;
end architecture;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_reg_with_en is
  generic(
    REG_NUM  : integer := 2;
    REG_WIDTH : integer := 16
  );
  port(
    clk      : in std_logic;
    rst      : in std_logic := '0';
    i_en     : in std_logic;
    i_d      : in std_logic_vector(REG_WIDTH-1 downto 0);
    o_d      : out std_logic_vector(REG_WIDTH-1 downto 0) := (others=>'0')
  );
end generic_reg_with_en;

architecture behav of generic_reg_with_en is
begin
  --Act as a wire
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  --A raising edge single reg
  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          o_d <= i_d;
        end if;
      end if;
    end process P1;
  end generate GR1;

  --Act as a FIFO
  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic_vector(REG_WIDTH - 1 downto 0);
    signal t_reg_in : type_in_reg := (others=>(others=>'0'));
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          t_reg_in(REG_NUM - 1) <= i_d;
          t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
        end if;
      end if;
    end process P1;
  end generate GR2;
end architecture;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_reg1 is
generic(
  REG_NUM  : integer := 2
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_d      : in std_logic;
  o_d      : out std_logic := '0'
);
end generic_reg1;

architecture behav of generic_reg1 is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        o_d <= i_d;
      end if;
    end process P1;
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic;
    signal t_reg_in : type_in_reg := (others=>'0');
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then
        t_reg_in(REG_NUM - 1) <= i_d;
        t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
      end if;
    end process P1;
  end generate GR2;
end architecture;

----------------------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.ALL;

entity generic_reg1_with_en is
generic(
  REG_NUM  : integer := 2
);
port(
  clk      : in std_logic;
  rst      : in std_logic := '0';
  i_en     : in std_logic;
  i_d      : in std_logic;
  o_d      : out std_logic := '0'
);
end generic_reg1_with_en;

architecture behav of generic_reg1_with_en is
begin
  GR0: if REG_NUM = 0 generate
    o_d <= i_d;
  end generate GR0;

  GR1: if REG_NUM = 1 generate
    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          o_d <= i_d;
        end if;
      end if;
    end process P1;
  end generate GR1;

  GR2: if REG_NUM > 1 generate
    type type_in_reg is array (0 to REG_NUM - 1) of std_logic;
    signal t_reg_in : type_in_reg := (others=>'0');
  begin
    o_d <= t_reg_in(0);

    P1: process (clk) is
    begin
      if rising_edge(clk) then
        if (i_en = '1') then
          t_reg_in(REG_NUM - 1) <= i_d;
          t_reg_in(0 to REG_NUM - 2) <= t_reg_in(1 to REG_NUM -1);
        end if;
      end if;
    end process P1;
  end generate GR2;
end architecture;
