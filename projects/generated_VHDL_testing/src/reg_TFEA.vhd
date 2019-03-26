--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package reg_TFEA_pkg is
	component reg_TFEA is
		generic (
			data_width : integer := 8
		);
		port (
			reset : in std_logic;
			--Data ports
			write_enable : in std_logic;
			data_in   : in  std_logic_vector(data_width-1 downto 0);
			data_out  : out std_logic_vector(data_width-1 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

entity reg_TFEA is
	generic (
		data_width : integer := 8
	);
	port (
		reset : in std_logic;
		--Data ports
		write_enable : in std_logic;
		data_in   : in  std_logic_vector(data_width-1 downto 0);
		data_out  : out std_logic_vector(data_width-1 downto 0)
	);
end entity;

architecture arch of reg_TFEA is
	signal storedValue : std_logic_vector(data_width-1 downto 0);
begin
	assert (data_width > 0)
		report "data_width must be positive"
		severity failure;
	
	
	--Handle output of storedValue
	data_out <= storedValue;
	
	--Hanlde stored Value updating behavour
	process (write_enable, reset)
	begin
		if reset = '1' then
			storedValue <= (others => '0');
		elsif write_enable'event and write_enable = '1' then
			storedValue <= data_in;
		end if;
	end process;
end architecture;