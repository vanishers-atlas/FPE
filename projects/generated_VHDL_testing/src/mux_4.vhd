--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package mux_4_pkg is
	component mux_4 is
		generic (
			data_width : integer := 8
		);
		port (
			input_0 : in std_logic_vector(data_width - 1 downto 0);
			input_1 : in std_logic_vector(data_width - 1 downto 0);
			input_2 : in std_logic_vector(data_width - 1 downto 0);
			input_3 : in std_logic_vector(data_width - 1 downto 0);
			input_select : in std_logic_vector(1 downto 0);
			data_out : out std_logic_vector(data_width - 1 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

entity mux_4 is
	generic (
		data_width : integer := 8
	);
	port (
		input_0 : in std_logic_vector(data_width - 1 downto 0);
		input_1 : in std_logic_vector(data_width - 1 downto 0);
		input_2 : in std_logic_vector(data_width - 1 downto 0);
		input_3 : in std_logic_vector(data_width - 1 downto 0);
		input_select : in std_logic_vector(1 downto 0);
		data_out : out std_logic_vector(data_width - 1 downto 0)
	);
end entity;

architecture arch of mux_4 is
begin
	assert (data_width > 0)
		report "data_width must be positive"
		severity failure;
	
	
	process (input_select, input_0, input_1, input_2, input_3)
	begin
		--Mux data_out
		case input_select is
			when "00" =>
				data_out <= input_0;
			when "01" =>
				data_out <= input_1;
			when "10" =>
				data_out <= input_2;
			when others =>
				data_out <= input_3;
		end case;
	end process;
end architecture;