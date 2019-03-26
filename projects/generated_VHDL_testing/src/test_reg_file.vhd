--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_reg_file_pkg is
	component test_reg_file is
		port (
			--Read Data Ports
			read_data_0 : out std_logic_vector(7 downto 0);
			read_data_1 : out std_logic_vector(7 downto 0);
			
			--Read Address Ports
			read_addr_0 : in  std_logic_vector(1 downto 0);
			read_addr_1 : in  std_logic_vector(1 downto 0);
			
			--Write Ports
			write_data : in std_logic_vector(7 downto 0);
			write_addr : in std_logic_vector(1 downto 0);
			write_enable : in std_logic
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.reg_FFEA_pkg.ALL;
use work.mux_4_pkg.ALL;
use work.demux_4_pkg.ALL;

entity test_reg_file is
	port (
		--Read Data Ports
		read_data_0 : out std_logic_vector(7 downto 0);
		read_data_1 : out std_logic_vector(7 downto 0);
		
		--Read Address Ports
		read_addr_0 : in  std_logic_vector(1 downto 0);
		read_addr_1 : in  std_logic_vector(1 downto 0);
		
		--Write Ports
		write_data : in std_logic_vector(7 downto 0);
		write_addr : in std_logic_vector(1 downto 0);
		write_enable : in std_logic
	);
end entity;

architecture arch of test_reg_file is
	--Register Output Signals
	signal reg_0_out : std_logic_vector(7 downto 0);
	signal reg_1_out : std_logic_vector(7 downto 0);
	signal reg_2_out : std_logic_vector(7 downto 0);
	signal reg_3_out : std_logic_vector(7 downto 0);
	
	--Register Write Signals
	signal reg_0_write : std_logic;
	signal reg_1_write : std_logic;
	signal reg_2_write : std_logic;
	signal reg_3_write : std_logic;
begin
	--Registers
	reg_0 : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => reg_0_write,
			data_in   => write_data,
			data_out  => reg_0_out
		);
	
	reg_1 : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => reg_1_write,
			data_in   => write_data,
			data_out  => reg_1_out
		);
	
	reg_2 : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => reg_2_write,
			data_in   => write_data,
			data_out  => reg_2_out
		);
	
	reg_3 : reg_FFEA
		generic map (data_width => 8)
		port map (
			write_enable => reg_3_write,
			data_in   => write_data,
			data_out  => reg_3_out
		);
	
	--Read Muxes
	Read_0_mux : mux_4
		generic map (data_width => 8)
		port map (
			input_0 => reg_0_out,
			input_1 => reg_1_out,
			input_2 => reg_2_out,
			input_3 => reg_3_out,
			input_select => read_addr_0,
			data_out  => read_data_0
		);
	
	Read_1_mux : mux_4
		generic map (data_width => 8)
		port map (
			input_0 => reg_0_out,
			input_1 => reg_1_out,
			input_2 => reg_2_out,
			input_3 => reg_3_out,
			input_select => read_addr_1,
			data_out  => read_data_1
		);
	
	-- Write enable demux
	write_demux : demux_4
		generic map (data_width => 1)
		port map (
			output_0(0) => reg_0_write,
			output_1(0) => reg_1_write,
			output_2(0) => reg_2_write,
			output_3(0) => reg_3_write,
			output_select => write_addr,
			data_in(0)  => write_enable
		);
end architecture;