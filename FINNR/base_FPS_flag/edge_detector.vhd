
library ieee;
use ieee.std_logic_1164.all;

entity edge_detector is
	port (
		clock : in std_logic;
		probe : in std_logic;
		found_rising_edge  : out std_logic;
		found_falling_edge : out std_logic
	);
end entity;

architecture arch of edge_detector is
	signal curr_sample : std_logic;
	signal last_sample : std_logic;
begin
	process (clock)
	begin
		if rising_edge(clock) then
			last_sample <= curr_sample;
			curr_sample <= probe;
		end if;
	end process;

	found_rising_edge <= not last_sample and curr_sample;
	found_falling_edge <= last_sample and not curr_sample;
end architecture;
