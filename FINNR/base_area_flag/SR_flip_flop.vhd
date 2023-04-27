
library ieee;
use ieee.std_logic_1164.all;

entity SR_flip_flop is
	generic (
		start_set : boolean := false;
		start_reset : boolean := false
	);
	port (
		clock : in std_logic;
		S : in std_logic;
		R : in std_logic;
		Q : out std_logic;
		Q_bar : out std_logic
	);
end entity;

architecture arch of SR_flip_flop is
	pure function compute_starting_state return std_logic is
	begin
		if start_set = True and start_reset = False then
			return '1';
		elsif start_set = False and start_reset = True then
			return '0';
		elsif start_set = True and start_reset = True then
			return 'X';
		else --if start_set = False and start_reset = False then
			return 'U';
		end if;
	end function;

    signal state : std_logic := compute_starting_state;
begin
	process (clock)
	begin
		if rising_edge(clock) then
			if    S = '1' and R = '0' then
				state <= '1';
			elsif S = '0' and R = '1' then
				state <= '0';
			elsif S = '1' and R = '1' then
				state <= 'X';
			end if;
		end if;
	end process;

	Q <= state;
	Q_bar <= not state;
end architecture;
