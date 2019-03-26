--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_data_mem_pkg is
	component test_data_mem is
		port (
			--Addr Ports
			read_addr_0 : in std_logic_vector(5 downto 0);
			read_addr_1 : in std_logic_vector(5 downto 0);
			
			--Read Ports
			read_data_0 : out std_logic_vector(7 downto 0);
			read_data_1 : out std_logic_vector(7 downto 0);
			
			--Write Ports
			write_enable : in std_logic;
			write_addr : in std_logic_vector(5 downto 0);
			write_data : in std_logic_vector(7 downto 0) 
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.all;
use ieee.math_real.all;
use std.textio.all;

entity test_data_mem is
	port (
		--Addr Ports
		read_addr_0 : in std_logic_vector(5 downto 0);
		read_addr_1 : in std_logic_vector(5 downto 0);
		
		--Read Ports
		read_data_0 : out std_logic_vector(7 downto 0);
		read_data_1 : out std_logic_vector(7 downto 0);
		
		--Write Ports
		write_enable : in std_logic;
		write_addr : in std_logic_vector(5 downto 0);
		write_data : in std_logic_vector(7 downto 0) 
	);
end entity;

architecture arch of test_data_mem is
	type mem_type is array (0 to 63) of std_logic_vector(7 downto 0);
	
	signal data : mem_type;
begin
	--Read Handling
	read_data_0 <= data(to_integer(unsigned(read_addr_0)));
	read_data_1 <= data(to_integer(unsigned(read_addr_1)));
	
	--Write Handling
	process (write_enable)
	begin
		if write_enable'event and write_enable = '1' then
			data(to_integer(unsigned(write_addr))) <= write_data;
		end if;
	end process;
end architecture;