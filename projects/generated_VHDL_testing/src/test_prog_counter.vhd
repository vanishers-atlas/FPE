--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_prog_counter_pkg is
	component test_prog_counter is
		port (
			--Jump Ports
			jump_occured : out std_logic;
			jump_addr : in std_logic_vector(7 downto 0);
			jmp : in std_logic;
			jeq : in std_logic;
			--status Ports
			status_equal : in std_logic;
			
			--General Ports
			clock: in std_logic;
			reset: in std_logic;
			value : out std_logic_vector(7 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.reg_TFEA_pkg.ALL;
use ieee.numeric_std.ALL;

entity test_prog_counter is
	port (
		--Jump Ports
		jump_occured : out std_logic;
		jump_addr : in std_logic_vector(7 downto 0);
		jmp : in std_logic;
		jeq : in std_logic;
		--status Ports
		status_equal : in std_logic;
		
		--General Ports
		clock: in std_logic;
		reset: in std_logic;
		value : out std_logic_vector(7 downto 0)
	);
end entity;

architecture arch of test_prog_counter is
	
	--Register Signals
	signal notClock: std_logic;
	signal next_PC : std_logic_vector(7 downto 0);
	signal curr_PC : std_logic_vector(7 downto 0);
	
	signal  internal_jump : std_logic;
begin
	
	--Generate not clock signal
	notClock <= not clock;
	
	--Store PC's Value
	PC : reg_TFEA
		generic map (data_width => 8)
		port map (
			reset => reset,
			write_enable => notClock,
			data_in   => next_PC,
			data_out  => curr_PC
		);
	
	--Connect Vvlue port to registor output
	value <= curr_PC;
	
	--Connent jump_occured port to internal_jump
	jump_occured <= internal_jump;
	
	--Generate internal_jump signal
	jump_occured <= '1' when 
		   jmp = '1'
		or (jeq = '1' and status_equal = '1')
	else '0';
	
	--Generate next_PC
	process(curr_PC, internal_jump)
		variable PC_inc : integer := to_integer(unsigned(curr_PC));
	begin
		if internal_jump = '1' then
			next_PC <= jump_addr;
		else
			PC_inc := PC_inc + 1;
			if PC_inc = 16 then
				PC_inc := 0;
			end if;
			next_PC <= std_logic_vector(to_unsigned(PC_inc, 7));
		end if;
	end process;
end architecture;