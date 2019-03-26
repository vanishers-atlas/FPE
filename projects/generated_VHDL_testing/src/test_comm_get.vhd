--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_comm_get_pkg is
	component test_comm_get is
		port (
			--FIFO Data Ports
			FIFO_0 : in std_logic_vector(7 downto 0);
			FIFO_1 : in std_logic_vector(7 downto 0);
			FIFO_2 : in std_logic_vector(7 downto 0);
			FIFO_3 : in std_logic_vector(7 downto 0);
			
			--FIFO Update Ports
			update_FIFO_0 : out std_logic;
			update_FIFO_1 : out std_logic;
			update_FIFO_2 : out std_logic;
			update_FIFO_3 : out std_logic;
			
			--Read Address Ports
			address_0 : in  std_logic_vector(1 downto 0);
			address_1 : in  std_logic_vector(1 downto 0);
			
			--Read Data Ports
			data_0  : out std_logic_vector(7 downto 0);
			data_1  : out std_logic_vector(7 downto 0);
			
			--Read Update Ports
			update_0 : in std_logic;
			
			clock : in std_logic
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.reg_FFEA_pkg.ALL;
use work.demux_4_pkg.ALL;
use work.mux_4_pkg.ALL;

entity test_comm_get is
	port (
		--FIFO Data Ports
		FIFO_0 : in std_logic_vector(7 downto 0);
		FIFO_1 : in std_logic_vector(7 downto 0);
		FIFO_2 : in std_logic_vector(7 downto 0);
		FIFO_3 : in std_logic_vector(7 downto 0);
		
		--FIFO Update Ports
		update_FIFO_0 : out std_logic;
		update_FIFO_1 : out std_logic;
		update_FIFO_2 : out std_logic;
		update_FIFO_3 : out std_logic;
		
		--Read Address Ports
		address_0 : in  std_logic_vector(1 downto 0);
		address_1 : in  std_logic_vector(1 downto 0);
		
		--Read Data Ports
		data_0  : out std_logic_vector(7 downto 0);
		data_1  : out std_logic_vector(7 downto 0);
		
		--Read Update Ports
		update_0 : in std_logic;
		
		clock : in std_logic
	);
end entity;

architecture arch of test_comm_get is
	--FIFO buffer signals
	signal FIFO_0_buff_out : std_logic_vector(7 downto 0);
	signal FIFO_1_buff_out : std_logic_vector(7 downto 0);
	signal FIFO_2_buff_out : std_logic_vector(7 downto 0);
	signal FIFO_3_buff_out : std_logic_vector(7 downto 0);
	
	--FIFO Update signals
	signal update_FIFO_0_0 : std_logic;
	signal update_FIFO_1_0 : std_logic;
	signal update_FIFO_2_0 : std_logic;
	signal update_FIFO_3_0 : std_logic;
begin
	--Buffer FIFO ports
	FIFO_0_buff : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => clock,
			data_in   => FIFO_0,
			data_out  => FIFO_0_buff_out
		);
	FIFO_1_buff : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => clock,
			data_in   => FIFO_1,
			data_out  => FIFO_1_buff_out
		);
	FIFO_2_buff : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => clock,
			data_in   => FIFO_2,
			data_out  => FIFO_2_buff_out
		);
	FIFO_3_buff : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => clock,
			data_in   => FIFO_3,
			data_out  => FIFO_3_buff_out
		);
	
	--Generate update_FIFO signals
	update_FIFO_0 <= update_FIFO_0_0;
	update_FIFO_1 <= update_FIFO_1_0;
	update_FIFO_2 <= update_FIFO_2_0;
	update_FIFO_3 <= update_FIFO_3_0;
	
	--Demux fifo update
	update_demux_0 : demux_4
		generic map (data_width => 1)
		port map (
			output_0(0) => update_FIFO_0_0,
			output_1(0) => update_FIFO_1_0,
			output_2(0) => update_FIFO_2_0,
			output_3(0) => update_FIFO_3_0,
			output_select => address_0,
			data_in(0)  => update_FIFO_0
		);
	
	--Read Muxes
	read_mux_0 : mux_4
		generic map (data_width => 8)
		port map (
			input_0 => FIFO_0_buff_out,
			input_1 => FIFO_1_buff_out,
			input_2 => FIFO_2_buff_out,
			input_3 => FIFO_3_buff_out,
			input_select => address_0,
			data_out  => data_0
		);
	read_mux_1 : mux_4
		generic map (data_width => 8)
		port map (
			input_0 => FIFO_0_buff_out,
			input_1 => FIFO_1_buff_out,
			input_2 => FIFO_2_buff_out,
			input_3 => FIFO_3_buff_out,
			input_select => address_1,
			data_out  => data_1
		);
end architecture;