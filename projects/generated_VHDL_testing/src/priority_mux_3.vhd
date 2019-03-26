--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package priority_mux_3_pkg is
	component priority_mux_3 is
		generic (
			data_width : integer := 8
		);
		port (
			input_0 : in std_logic_vector(data_width - 1 downto 0);
			input_1 : in std_logic_vector(data_width - 1 downto 0);
			input_2 : in std_logic_vector(data_width - 1 downto 0);
			select_0 : in std_logic;
			select_1 : in std_logic;
			select_2 : in std_logic;
			data_out : out std_logic_vector(data_width - 1 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

entity priority_mux_3 is
	generic (
		data_width : integer := 8
	);
	port (
		input_0 : in std_logic_vector(data_width - 1 downto 0);
		input_1 : in std_logic_vector(data_width - 1 downto 0);
		input_2 : in std_logic_vector(data_width - 1 downto 0);
		select_0 : in std_logic;
		select_1 : in std_logic;
		select_2 : in std_logic;
		data_out : out std_logic_vector(data_width - 1 downto 0)
	);
end entity;

architecture arch of priority_mux_3 is
begin
	assert (data_width > 0)
		report "data_width must be positive"
		severity failure;
	
	
	process (input_0, select_0, input_1, select_1, input_2, select_2)
	begin
		--Mux data_out
		if select_0 = '1' then
			data_out <= input_0;
		elsif select_1 = '1' then
			data_out <= input_1;
		elsif select_2 = '1' then
			data_out <= input_2;
		end if;
	end process;
end architecture;