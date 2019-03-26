--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package demux_4_pkg is
	component demux_4 is
		generic (
			data_width : integer := 8
		);
		port (
			output_0 : out std_logic_vector(data_width - 1 downto 0);
			output_1 : out std_logic_vector(data_width - 1 downto 0);
			output_2 : out std_logic_vector(data_width - 1 downto 0);
			output_3 : out std_logic_vector(data_width - 1 downto 0);
			output_select : in std_logic_vector(1 downto 0);
			data_in : in std_logic_vector(data_width - 1 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

entity demux_4 is
	generic (
		data_width : integer := 8
	);
	port (
		output_0 : out std_logic_vector(data_width - 1 downto 0);
		output_1 : out std_logic_vector(data_width - 1 downto 0);
		output_2 : out std_logic_vector(data_width - 1 downto 0);
		output_3 : out std_logic_vector(data_width - 1 downto 0);
		output_select : in std_logic_vector(1 downto 0);
		data_in : in std_logic_vector(data_width - 1 downto 0)
	);
end entity;

architecture arch of demux_4 is
begin
	assert (data_width > 0)
		report "data_width must be positive"
		severity failure;
	
	process (output_select, data_in)
	begin
		--Clear all ports
		output_0 <= (others => 'Z');
		output_1 <= (others => 'Z');
		output_2 <= (others => 'Z');
		output_3 <= (others => 'Z');
		--Demux data_in
		case output_select is
			when "00" =>
				output_0 <= data_in;
			when "01" =>
				output_1 <= data_in;
			when "10" =>
				output_2 <= data_in;
			when others =>
				output_3 <= data_in;
		end case;
	end process;
end architecture;