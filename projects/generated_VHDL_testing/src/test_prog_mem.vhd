--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_prog_mem_pkg is
	component test_prog_mem is
		port (
			--Addr Ports
			addr_0 : in std_logic_vector(4 downto 0);
			
			--Read Ports
			data_0 : out std_logic_vector(21 downto 0)
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

entity test_prog_mem is
	port (
		--Addr Ports
		addr_0 : in std_logic_vector(4 downto 0);
		
		--Read Ports
		data_0 : out std_logic_vector(21 downto 0)
	);
end entity;

architecture arch of test_prog_mem is
	type mem_type is array (0 to 31) of std_logic_vector (21 downto 0);
	
	impure function init_mem(mif_filename : in string) return mem_type is
		file mif_file : text open read_mode is mif_filename;
		variable mif_line : line;
		variable temp_bv  : bit_vector(21 downto 0);
		variable temp_mem : mem_type;
	begin
		for index in mem_type'range loop
			if ENDFILE(mif_file) then
				exit;
			else
				readline(mif_file, mif_line);
				read(mif_line, temp_bv);
				temp_mem(index) := to_stdlogicvector(temp_bv);
			end if;
		end loop;
		return temp_mem;
	end function;
	
	signal data : mem_type  := init_mem("IMM_values.mif");
begin
	--Read Handling
	data_0 <= data(to_integer(unsigned(addr_0)));
end architecture;