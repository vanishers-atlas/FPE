
library ieee;
use ieee.std_logic_1164.all;

entity network_baseline is
	port (
		clock : in std_logic;
		input_data : in std_logic_vector(0 downto 0);
		input_write : in std_logic;
		input_ready : out std_logic;
		output_data : out std_logic_vector(9 downto 0);
		output_read : in std_logic;
		output_ready : out std_logic
	);
end entity;

architecture arch of network_baseline is
	signal FIFO_0_data_out : std_logic_vector(0 downto 0);
	signal FIFO_0_data_read : std_logic;
	signal FIFO_0_data_read_ready : std_logic;
	signal layer_1_FPE_kickoff : std_logic;
	signal FIFO_1_data_in : std_logic_vector(0 downto 0);
	signal FIFO_1_data_write : std_logic;
	signal FIFO_1_data_write_ready : std_logic;
	signal FIFO_1_data_out : std_logic_vector(0 downto 0);
	signal FIFO_1_data_read : std_logic;
	signal FIFO_1_data_read_ready : std_logic;
	signal layer_2_FPE_kickoff : std_logic;
	signal FIFO_2_data_in : std_logic_vector(0 downto 0);
	signal FIFO_2_data_write : std_logic;
	signal FIFO_2_data_write_ready : std_logic;
	signal FIFO_2_data_out : std_logic_vector(0 downto 0);
	signal FIFO_2_data_read : std_logic;
	signal FIFO_2_data_read_ready : std_logic;
	signal layer_3_FPE_kickoff : std_logic;
	signal FIFO_3_data_in : std_logic_vector(0 downto 0);
	signal FIFO_3_data_write : std_logic;
	signal FIFO_3_data_write_ready : std_logic;
	signal FIFO_3_data_out : std_logic_vector(0 downto 0);
	signal FIFO_3_data_read : std_logic;
	signal FIFO_3_data_read_ready : std_logic;
	signal layer_4_FPE_kickoff : std_logic;
	signal FIFO_4_data_in : std_logic_vector(0 downto 0);
	signal FIFO_4_data_write : std_logic;
	signal FIFO_4_data_write_ready : std_logic;
	signal FIFO_4_data_out : std_logic_vector(0 downto 0);
	signal FIFO_4_data_read : std_logic;
	signal FIFO_4_data_read_ready : std_logic;
	signal layer_5_FPE_kickoff : std_logic;
	signal FIFO_5_data_in : std_logic_vector(0 downto 0);
	signal FIFO_5_data_write : std_logic;
	signal FIFO_5_data_write_ready : std_logic;
	signal FIFO_5_data_out : std_logic_vector(0 downto 0);
	signal FIFO_5_data_read : std_logic;
	signal FIFO_5_data_read_ready : std_logic;
	signal layer_6_FPE_kickoff : std_logic;
	signal FIFO_6_data_in : std_logic_vector(0 downto 0);
	signal FIFO_6_data_write : std_logic;
	signal FIFO_6_data_write_ready : std_logic;
	signal FIFO_6_data_out : std_logic_vector(0 downto 0);
	signal FIFO_6_data_read : std_logic;
	signal FIFO_6_data_read_ready : std_logic;
	signal layer_7_FPE_kickoff : std_logic;
	signal FIFO_7_data_in : std_logic_vector(0 downto 0);
	signal FIFO_7_data_write : std_logic;
	signal FIFO_7_data_write_ready : std_logic;
	signal FIFO_7_data_out : std_logic_vector(0 downto 0);
	signal FIFO_7_data_read : std_logic;
	signal FIFO_7_data_read_ready : std_logic;
	signal layer_8_FPE_kickoff : std_logic;
	signal FIFO_8_data_in : std_logic_vector(0 downto 0);
	signal FIFO_8_data_write : std_logic;
	signal FIFO_8_data_write_ready : std_logic;
	signal FIFO_8_data_out : std_logic_vector(0 downto 0);
	signal FIFO_8_data_read : std_logic;
	signal FIFO_8_data_read_ready : std_logic;
	signal layer_9_FPE_kickoff : std_logic;
	signal FIFO_9_data_in : std_logic_vector(0 downto 0);
	signal FIFO_9_data_write : std_logic;
	signal FIFO_9_data_write_ready : std_logic;
	signal FIFO_9_data_out : std_logic_vector(0 downto 0);
	signal FIFO_9_data_read : std_logic;
	signal FIFO_9_data_read_ready : std_logic;
	signal layer_10_FPE_kickoff : std_logic;
	signal FIFO_10_data_in : std_logic_vector(0 downto 0);
	signal FIFO_10_data_write : std_logic;
	signal FIFO_10_data_write_ready : std_logic;
	signal FIFO_10_data_out : std_logic_vector(0 downto 0);
	signal FIFO_10_data_read : std_logic;
	signal FIFO_10_data_read_ready : std_logic;
	signal layer_11_FPE_kickoff : std_logic;
	signal FIFO_11_data_in : std_logic_vector(9 downto 0);
	signal FIFO_11_data_write : std_logic;
	signal FIFO_11_data_write_ready : std_logic;
begin
	FIFO_0 : entity work.FIFO_1w_24576d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => input_data,
			data_write => input_write,
			data_write_ready => input_ready,
			data_out => FIFO_0_data_out,
			data_read => FIFO_0_data_read,
			data_read_ready => FIFO_0_data_read_ready
		);
	
	layer_1_FPE_kickoff <= FIFO_0_data_read_ready and FIFO_1_data_write_ready;
	layer_1_FPE : entity work.layer_1_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_0_data_out,
			GET_FIFO_0_red  => FIFO_0_data_read,
			PUT_FIFO_0_data  => FIFO_1_data_in,
			PUT_FIFO_0_write => FIFO_1_data_write,
			kickoff => layer_1_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_1 : entity work.FIFO_1w_65536d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_1_data_in,
			data_write => FIFO_1_data_write,
			data_write_ready => FIFO_1_data_write_ready,
			data_out => FIFO_1_data_out,
			data_read => FIFO_1_data_read,
			data_read_ready => FIFO_1_data_read_ready
		);
	
	layer_2_FPE_kickoff <= FIFO_1_data_read_ready and FIFO_2_data_write_ready;
	layer_2_FPE : entity work.layer_2_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_1_data_out,
			GET_FIFO_0_red  => FIFO_1_data_read,
			PUT_FIFO_0_data  => FIFO_2_data_in,
			PUT_FIFO_0_write => FIFO_2_data_write,
			kickoff => layer_2_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_2 : entity work.FIFO_1w_65536d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_2_data_in,
			data_write => FIFO_2_data_write,
			data_write_ready => FIFO_2_data_write_ready,
			data_out => FIFO_2_data_out,
			data_read => FIFO_2_data_read,
			data_read_ready => FIFO_2_data_read_ready
		);
	
	layer_3_FPE_kickoff <= FIFO_2_data_read_ready and FIFO_3_data_write_ready;
	layer_3_FPE : entity work.layer_3_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_2_data_out,
			GET_FIFO_0_red  => FIFO_2_data_read,
			PUT_FIFO_0_data  => FIFO_3_data_in,
			PUT_FIFO_0_write => FIFO_3_data_write,
			kickoff => layer_3_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_3 : entity work.FIFO_1w_16384d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_3_data_in,
			data_write => FIFO_3_data_write,
			data_write_ready => FIFO_3_data_write_ready,
			data_out => FIFO_3_data_out,
			data_read => FIFO_3_data_read,
			data_read_ready => FIFO_3_data_read_ready
		);
	
	layer_4_FPE_kickoff <= FIFO_3_data_read_ready and FIFO_4_data_write_ready;
	layer_4_FPE : entity work.layer_4_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_3_data_out,
			GET_FIFO_0_red  => FIFO_3_data_read,
			PUT_FIFO_0_data  => FIFO_4_data_in,
			PUT_FIFO_0_write => FIFO_4_data_write,
			kickoff => layer_4_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_4 : entity work.FIFO_1w_32768d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_4_data_in,
			data_write => FIFO_4_data_write,
			data_write_ready => FIFO_4_data_write_ready,
			data_out => FIFO_4_data_out,
			data_read => FIFO_4_data_read,
			data_read_ready => FIFO_4_data_read_ready
		);
	
	layer_5_FPE_kickoff <= FIFO_4_data_read_ready and FIFO_5_data_write_ready;
	layer_5_FPE : entity work.layer_5_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_4_data_out,
			GET_FIFO_0_red  => FIFO_4_data_read,
			PUT_FIFO_0_data  => FIFO_5_data_in,
			PUT_FIFO_0_write => FIFO_5_data_write,
			kickoff => layer_5_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_5 : entity work.FIFO_1w_32768d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_5_data_in,
			data_write => FIFO_5_data_write,
			data_write_ready => FIFO_5_data_write_ready,
			data_out => FIFO_5_data_out,
			data_read => FIFO_5_data_read,
			data_read_ready => FIFO_5_data_read_ready
		);
	
	layer_6_FPE_kickoff <= FIFO_5_data_read_ready and FIFO_6_data_write_ready;
	layer_6_FPE : entity work.layer_6_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_5_data_out,
			GET_FIFO_0_red  => FIFO_5_data_read,
			PUT_FIFO_0_data  => FIFO_6_data_in,
			PUT_FIFO_0_write => FIFO_6_data_write,
			kickoff => layer_6_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_6 : entity work.FIFO_1w_8192d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_6_data_in,
			data_write => FIFO_6_data_write,
			data_write_ready => FIFO_6_data_write_ready,
			data_out => FIFO_6_data_out,
			data_read => FIFO_6_data_read,
			data_read_ready => FIFO_6_data_read_ready
		);
	
	layer_7_FPE_kickoff <= FIFO_6_data_read_ready and FIFO_7_data_write_ready;
	layer_7_FPE : entity work.layer_7_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_6_data_out,
			GET_FIFO_0_red  => FIFO_6_data_read,
			PUT_FIFO_0_data  => FIFO_7_data_in,
			PUT_FIFO_0_write => FIFO_7_data_write,
			kickoff => layer_7_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_7 : entity work.FIFO_1w_16384d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_7_data_in,
			data_write => FIFO_7_data_write,
			data_write_ready => FIFO_7_data_write_ready,
			data_out => FIFO_7_data_out,
			data_read => FIFO_7_data_read,
			data_read_ready => FIFO_7_data_read_ready
		);
	
	layer_8_FPE_kickoff <= FIFO_7_data_read_ready and FIFO_8_data_write_ready;
	layer_8_FPE : entity work.layer_8_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_7_data_out,
			GET_FIFO_0_red  => FIFO_7_data_read,
			PUT_FIFO_0_data  => FIFO_8_data_in,
			PUT_FIFO_0_write => FIFO_8_data_write,
			kickoff => layer_8_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_8 : entity work.FIFO_1w_16384d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_8_data_in,
			data_write => FIFO_8_data_write,
			data_write_ready => FIFO_8_data_write_ready,
			data_out => FIFO_8_data_out,
			data_read => FIFO_8_data_read,
			data_read_ready => FIFO_8_data_read_ready
		);
	
	layer_9_FPE_kickoff <= FIFO_8_data_read_ready and FIFO_9_data_write_ready;
	layer_9_FPE : entity work.layer_9_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_8_data_out,
			GET_FIFO_0_red  => FIFO_8_data_read,
			PUT_FIFO_0_data  => FIFO_9_data_in,
			PUT_FIFO_0_write => FIFO_9_data_write,
			kickoff => layer_9_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_9 : entity work.FIFO_1w_4096d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_9_data_in,
			data_write => FIFO_9_data_write,
			data_write_ready => FIFO_9_data_write_ready,
			data_out => FIFO_9_data_out,
			data_read => FIFO_9_data_read,
			data_read_ready => FIFO_9_data_read_ready
		);
	
	layer_10_FPE_kickoff <= FIFO_9_data_read_ready and FIFO_10_data_write_ready;
	layer_10_FPE : entity work.layer_10_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_9_data_out,
			GET_FIFO_0_red  => FIFO_9_data_read,
			PUT_FIFO_0_data  => FIFO_10_data_in,
			PUT_FIFO_0_write => FIFO_10_data_write,
			kickoff => layer_10_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_10 : entity work.FIFO_1w_512d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_10_data_in,
			data_write => FIFO_10_data_write,
			data_write_ready => FIFO_10_data_write_ready,
			data_out => FIFO_10_data_out,
			data_read => FIFO_10_data_read,
			data_read_ready => FIFO_10_data_read_ready
		);
	
	layer_11_FPE_kickoff <= FIFO_10_data_read_ready and FIFO_11_data_write_ready;
	layer_11_FPE : entity work.layer_11_FPE_inst(arch)
		port map (	
			GET_FIFO_0_data => FIFO_10_data_out,
			GET_FIFO_0_red  => FIFO_10_data_read,
			PUT_FIFO_0_data  => FIFO_11_data_in,
			PUT_FIFO_0_write => FIFO_11_data_write,
			kickoff => layer_11_FPE_kickoff,
			clock => clock,
			running => open
		);
	
	FIFO_11 : entity work.FIFO_10w_10d(arch)
		port map (	
			clock => clock,
			clear => '0',
			full  => open,
			empty => open,
			data_in => FIFO_11_data_in,
			data_write => FIFO_11_data_write,
			data_write_ready => FIFO_11_data_write_ready,
			data_out => output_data,
			data_read => output_read,
			data_read_ready => output_ready
		);
	
end architecture;
