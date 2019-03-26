--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_comm_put_pkg is
	component test_comm_put is
		port (
			--FIFO Data Ports
			FIFO_0 : out std_logic_vector(7 downto 0);
			FIFO_1 : out std_logic_vector(7 downto 0);
			FIFO_2 : out std_logic_vector(7 downto 0);
			FIFO_3 : out std_logic_vector(7 downto 0);
			
			--FIFO Update Ports
			update_FIFO_0 : out std_logic;
			update_FIFO_1 : out std_logic;
			update_FIFO_2 : out std_logic;
			update_FIFO_3 : out std_logic;
			
			--sFPE Ports
			data    : in std_logic_vector(7 downto 0);
			address : in std_logic_vector(1 downto 0);
			enable  : in std_logic;
			
			clock : in std_logic
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.demux_4_pkg.ALL;

entity test_comm_put is
	port (
		--FIFO Data Ports
		FIFO_0 : out std_logic_vector(7 downto 0);
		FIFO_1 : out std_logic_vector(7 downto 0);
		FIFO_2 : out std_logic_vector(7 downto 0);
		FIFO_3 : out std_logic_vector(7 downto 0);
		
		--FIFO Update Ports
		update_FIFO_0 : out std_logic;
		update_FIFO_1 : out std_logic;
		update_FIFO_2 : out std_logic;
		update_FIFO_3 : out std_logic;
		
		--sFPE Ports
		data    : in std_logic_vector(7 downto 0);
		address : in std_logic_vector(1 downto 0);
		enable  : in std_logic;
		
		clock : in std_logic
	);
end entity;

architecture arch of test_comm_put is
	--Update signal
	signal update : std_logic;
begin
	--Generate update signal
	update <= '1' when enable = '1' and clock = '0' else '0';
	
	--Demux Update
	update_demux : demux_4
		generic map (data_width => 1)
		port map (
			output_0(0) => update_FIFO_0,
			output_1(0) => update_FIFO_1,
			output_2(0) => update_FIFO_2,
			output_3(0) => update_FIFO_3,
			data_in(0)  => update,
			output_select => address
		);
	
	--Demux Data
	data_demux : demux_4
		generic map (data_width => 8)
		port map (
			output_0 => FIFO_0,
			output_1 => FIFO_1,
			output_2 => FIFO_2,
			output_3 => FIFO_3,
			data_in  => data,
			output_select => address
		);
end architecture;