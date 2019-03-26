--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_delay_pkg is
	component test_delay is
		generic (
			default_value : integer := 0;
			data_width : integer := 8;
			data_depth : integer := 64
		);
		port (
			clock : in std_logic;
			reset : in std_logic;
			data_in  : in  std_logic_vector(data_width - 1 downto 0);
			data_out : out std_logic_vector(data_width - 1 downto 0) 
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.all;


entity test_delay is
	generic (
		default_value : integer := 0;
		data_width : integer := 8;
		data_depth : integer := 64
	);
	port (
		clock : in std_logic;
		reset : in std_logic;
		data_in  : in  std_logic_vector(data_width - 1 downto 0);
		data_out : out std_logic_vector(data_width - 1 downto 0) 
	);
end entity;

architecture arch of test_delay is
	type delay_data is array (data_depth - 1 downto 0) of std_logic_vector (data_width - 1 downto 0);
	signal data : delay_data;
begin
	assert (data_width > 0)
		report "data_width must be positive"
		severity failure;
	
	assert (data_depth > 0)
		report "data_depth must be positive"
		severity failure;
	
	assert (default_value > 0)
		report "default_value must be positive"
		severity failure;
	
	assert (default_value < 2 ** data_width)
		report "default_value to large to fill in data_width bits"
		severity failure;
	
	--Output Delaysd data
	data_out <= data(0);
	
	--Handle data inserting
	process(clock)
	begin
		if clock'event and clock = '1' and reset = '0' then
			data <= data(data'left - 1 downto 0) & data_in;
		end if;
	end process;
	
	--Handle reset
	process(reset)
	begin
		if reset = '1' then
			data <= (others => std_logic_vector(to_unsigned(default_value, data_width)));
		end if;
	end process;
end architecture;