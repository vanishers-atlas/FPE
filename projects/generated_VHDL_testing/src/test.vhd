--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_pkg is
	component test is
		port (
			--Comm Get Data Ports
			CG_channel_0 : in std_logic_vector(7 downto 0);
			CG_channel_1 : in std_logic_vector(7 downto 0);
			CG_channel_2 : in std_logic_vector(7 downto 0);
			CG_channel_3 : in std_logic_vector(7 downto 0);
			
			--Comm Get Update Ports
			CG_channel_update_0 : out std_logic;
			CG_channel_update_1 : out std_logic;
			CG_channel_update_2 : out std_logic;
			CG_channel_update_3 : out std_logic;
			
			--Comm Put Data Ports
			CP_channel_0 : out std_logic_vector(8 downto 0);
			CP_channel_1 : out std_logic_vector(8 downto 0);
			CP_channel_2 : out std_logic_vector(8 downto 0);
			CP_channel_3 : out std_logic_vector(8 downto 0);
			
			--Comm Put Write Ports
			CP_channel_write_0 : out std_logic;
			CP_channel_write_1 : out std_logic;
			CP_channel_write_2 : out std_logic;
			CP_channel_write_3 : out std_logic;
			
			--General Ports
			clock : in std_logic;
			reset : in std_logic
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.test_delay_pkg.ALL;
use work.test_comm_get_pkg.ALL;
use work.test_IMM_pkg.ALL;
use work.test_reg_file_pkg.ALL;
use work.test_data_mem_pkg.ALL;
use work.test_comm_put_pkg.ALL;
use work.test_instr_decoder_pkg.ALL;
use work.test_prog_mem_pkg.ALL;
use work.test_prog_counter_pkg.ALL;
use work.test_status_reg_pkg.ALL;
use work.priority_mux_3_pkg.ALL;
use work.priority_mux_4_pkg.ALL;
use work.test_ALU_pkg.ALL;

entity test is
	port (
		--Comm Get Data Ports
		CG_channel_0 : in std_logic_vector(7 downto 0);
		CG_channel_1 : in std_logic_vector(7 downto 0);
		CG_channel_2 : in std_logic_vector(7 downto 0);
		CG_channel_3 : in std_logic_vector(7 downto 0);
		
		--Comm Get Update Ports
		CG_channel_update_0 : out std_logic;
		CG_channel_update_1 : out std_logic;
		CG_channel_update_2 : out std_logic;
		CG_channel_update_3 : out std_logic;
		
		--Comm Put Data Ports
		CP_channel_0 : out std_logic_vector(8 downto 0);
		CP_channel_1 : out std_logic_vector(8 downto 0);
		CP_channel_2 : out std_logic_vector(8 downto 0);
		CP_channel_3 : out std_logic_vector(8 downto 0);
		
		--Comm Put Write Ports
		CP_channel_write_0 : out std_logic;
		CP_channel_write_1 : out std_logic;
		CP_channel_write_2 : out std_logic;
		CP_channel_write_3 : out std_logic;
		
		--General Ports
		clock : in std_logic;
		reset : in std_logic
	);
end entity;

architecture arch of test is
	--Comm Get -> Data Select signals
	signal a_GET_buff_in  : std_logic_vector(7 downto 0);
	signal c_GET_buff_in  : std_logic_vector(7 downto 0);
	signal a_GET_buff_out : std_logic_vector(14 downto 0);
	signal c_GET_buff_out : std_logic_vector(23 downto 0);
	
	--Imm Mem -> Data Select signals
	signal c_IMM_buff_in  : std_logic_vector(7 downto 0);
	signal c_IMM_buff_out : std_logic_vector(23 downto 0);
	
	--Reg File -> Data Select signals
	signal a_REG_buff_in  : std_logic_vector(7 downto 0);
	signal c_REG_buff_in  : std_logic_vector(7 downto 0);
	signal a_REG_buff_out : std_logic_vector(14 downto 0);
	signal c_REG_buff_out : std_logic_vector(23 downto 0);
	
	--Data Mem -> Data Select signals
	signal a_MEM_buff_in  : std_logic_vector(7 downto 0);
	signal c_MEM_buff_in  : std_logic_vector(7 downto 0);
	signal a_MEM_buff_out : std_logic_vector(14 downto 0);
	signal c_MEM_buff_out : std_logic_vector(23 downto 0);
	
	--Instr Decoder -> Data Memories Addr signals
	signal a_addr_buff_in  : std_logic_vector(5 downto 0);
	signal c_addr_buff_in  : std_logic_vector(5 downto 0);
	signal a_addr_buff_out : std_logic_vector(5 downto 0);
	signal c_addr_buff_out : std_logic_vector(5 downto 0);
	
	--Instr Decoder ->  GET update signals
	signal GET_update_buff_c_in  : std_logic;
	signal GET_update_buff_c_out : std_logic;
	
	--Instr Decoder -> a Data Select signals
	signal a_sel_buff_REG_in  : std_logic;
	signal a_sel_buff_MEM_in  : std_logic;
	signal a_sel_buff_GET_in  : std_logic;
	signal a_sel_buff_REG_out : std_logic;
	signal a_sel_buff_MEM_out : std_logic;
	signal a_sel_buff_GET_out : std_logic;
	
	--Instr Decoder -> c Data Select signals
	signal c_sel_buff_REG_in  : std_logic;
	signal c_sel_buff_IMM_in  : std_logic;
	signal c_sel_buff_MEM_in  : std_logic;
	signal c_sel_buff_GET_in  : std_logic;
	signal c_sel_buff_REG_out : std_logic;
	signal c_sel_buff_IMM_out : std_logic;
	signal c_sel_buff_MEM_out : std_logic;
	signal c_sel_buff_GET_out : std_logic;
	
	--Instr Decoder -> ALU control signals
	signal control_op_mode_buff_in  : std_logic_vector(6 downto 0);
	signal control_op_mode_buff_out : std_logic_vector(6 downto 0);
	
	--Instr Decoder -> Data Write Back signals
	signal res_addr_buff_in  : std_logic_vector(6 downto 0);
	signal res_addr_buff_mid : std_logic_vector(6 downto 0);
	signal res_addr_buff_out : std_logic_vector(6 downto 0);
	signal res_sel_buff_REG_in  : std_logic;
	signal res_sel_buff_PUT_in  : std_logic;
	signal res_sel_buff_MEM_in  : std_logic;
	signal res_sel_buff_REG_mid : std_logic;
	signal res_sel_buff_PUT_mid : std_logic;
	signal res_sel_buff_MEM_mid : std_logic;
	signal res_sel_buff_REG_out : std_logic;
	signal res_sel_buff_PUT_out : std_logic;
	signal res_sel_buff_MEM_out : std_logic;
	
	--Instr Decoder -> Status Register signals
	signal status_update_buff_in  : std_logic;
	signal status_update_buff_mid : std_logic;
	signal status_update_buff_out : std_logic;
	
	--Instr Decoder -> Program Counter signals
	signal jump_buff_jmp_in  : std_logic;
	signal jump_buff_jeq_in  : std_logic;
	signal jump_buff_jmp_out : std_logic;
	signal jump_buff_jeq_out : std_logic;
	
	--Program Memory  -> Instr Decoder signals
	signal instr_buff_in  : std_logic_vector(21 downto 0);
	signal instr_buff_out : std_logic_vector(21 downto 0);
	
	--Jump occured signals
	signal jumped_buff_in  : std_logic;
	signal jumped_buff_out : std_logic;
	signal jump_or_reset : std_logic;
	
	--Program Counter -> Program Memory signals
	signal PC_buff_in  : std_logic_vector(7 downto 0);
	signal PC_buff_out : std_logic_vector(7 downto 0);
	
	--Status Register Signals
	signal status_reg_equal_in  : std_logic;
	signal status_reg_equal_out : std_logic;
	
	--Data Select -> ALU Signals
	signal a_selected_buff_in : std_logic_vector(14 downto 0);
	signal c_selected_buff_in : std_logic_vector(23 downto 0);
	signal a_selected_buff_out : std_logic_vector(14 downto 0);
	signal c_selected_buff_out : std_logic_vector(23 downto 0);
	
	--ALU -> Data Write Back signals
	signal result_buff_in  : std_logic_vector(24 downto 0);
	signal result_buff_out : std_logic_vector(24 downto 0);
begin
	--###########################################################
	--##                        Comm Get                       ##
	--###########################################################
	
	comm_get: test_comm_get
		port map (
			--FIFO Ports
			FIFO_0 => CG_channel_0,
			FIFO_1 => CG_channel_1,
			FIFO_2 => CG_channel_2,
			FIFO_3 => CG_channel_3,
			update_FIFO_0 => CG_channel_update_0,
			update_FIFO_1 => CG_channel_update_1,
			update_FIFO_2 => CG_channel_update_2,
			update_FIFO_3 => CG_channel_update_3,
			
			--sFPE Ports
			address_0 => c_addr_buff_out(1 downto 0),
			address_1 => a_addr_buff_out(1 downto 0),
			data_0(7 downto 0) => c_GET_buff_in,
			data_1(7 downto 0) => a_GET_buff_in,
			update_0 => GET_update_buff_c_out,
			
			clock => clock
		);
	
	a_GET_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => a_GET_buff_in,
			data_out => a_GET_buff_out
		);
	--Pad buffer output
	a_GET_buff_out <= (14 downto 8 => '0');
	
	c_GET_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => c_GET_buff_in,
			data_out => c_GET_buff_out
		);
	--Pad buffer output
	c_GET_buff_out <= (23 downto 8 => '0');
	
	--###########################################################
	--##                         Imm ROM                       ##
	--###########################################################
	
	IMM_ROM: test_IMM
		port map (
			addr_0 => c_addr_buff_out(4 downto 0),
			data_0(7 downto 0) => c_IMM_buff_in
		);
	
	c_IMM_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => c_IMM_buff_in,
			data_out => c_IMM_buff_out
		);
	--Pad buffer output
	c_IMM_buff_out <= (23 downto 8 => '0');
	
	--###########################################################
	--##                        Reg File                       ##
	--###########################################################
	
	--Reg File
	Reg_File: test_reg_file
		port map (
			read_addr_0 => a_addr_buff_out(1 downto 0),
			read_addr_1 => c_addr_buff_out(1 downto 0),
			read_data_0(7 downto 0) => a_REG_buff_in,
			read_data_1(7 downto 0) => c_REG_buff_in,
			write_addr => res_addr_buff_out(1 downto 0),
			write_data => result_buff_out(7 downto 0),
			write_enable => res_sel_buff_REG_out
		);
	
	a_REG_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => a_REG_buff_in,
			data_out => a_REG_buff_out
		);
	--Pad buffer output
	a_REG_buff_out <= (14 downto 8 => '0');
	
	c_REG_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => c_REG_buff_in,
			data_out => c_REG_buff_out
		);
	--Pad buffer output
	c_REG_buff_out <= (23 downto 8 => '0');
	
	--###########################################################
	--##                        Data Mem                       ##
	--###########################################################
	
	Data_Mem: test_data_mem
		port map (
			read_addr_0 => a_addr_buff_out(5 downto 0),
			read_addr_1 => c_addr_buff_out(5 downto 0),
			read_data_0(7 downto 0) => a_MEM_buff_in,
			read_data_1(7 downto 0) => c_MEM_buff_in,
			write_addr => res_addr_buff_out(1 downto 0),
			write_data => result_buff_out(7 downto 0),
			write_enable => res_sel_buff_MEM_out
		);
	
	a_MEM_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => a_MEM_buff_in,
			data_out => a_MEM_buff_out
		);
	--Pad buffer output
	a_REG_buff_out <= (14 downto 8 => '0');
	
	c_MEM_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 8,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => c_MEM_buff_in,
			data_out => c_MEM_buff_out
		);
	--Pad buffer output
	c_REG_buff_out <= (23 downto 8 => '0');
	
	--###########################################################
	--##                        Comm Put                       ##
	--###########################################################
	
	comm_put: test_comm_put
		port map (
			--FIFO Ports
			FIFO_0 => CP_channel_0,
			FIFO_1 => CP_channel_1,
			FIFO_2 => CP_channel_2,
			FIFO_3 => CP_channel_3,
			
			--sFPE Ports
			address => res_addr_buff_out(1 downto 0),
			enable => res_sel_buff_PUT_out,
			data => result_buff_out(7 downto 0),
			
			clock => clock
		);
	--###########################################################
	--##                       Instr Decode                    ##
	--###########################################################
	
	--Instruction Decoder
	ID: test_instr_decoder
		port map (
			--Connect data addr ports to buffers
			a_addr => a_addr_buff_in,
			c_addr => c_addr_buff_in,
			
			--Connect Comm Get update ports to buffer
			c_update => GET_update_buff_c_in,
			
			--Connect a Data Sel ports to buffers
			a_sel_REG => a_sel_buff_REG_in,
			a_sel_MEM => a_sel_buff_MEM_in,
			a_sel_GET => a_sel_buff_GET_in,
			
			--Connect c Data Sel ports to buffers
			c_sel_REG => c_sel_buff_REG_in,
			c_sel_IMM => c_sel_buff_IMM_in,
			c_sel_MEM => c_sel_buff_MEM_in,
			c_sel_GET => c_sel_buff_GET_in,
			
			--Connect ALU Control Ports to buffers
			control_op_mode => control_op_mode_buff_in,
			
			---Connect Write Back Ports to buffers
			res_addr => res_addr_buff_in,
			res_sel_REG => res_sel_buff_REG_in,
			res_sel_PUT => res_sel_buff_PUT_in,
			res_sel_MEM => res_sel_buff_MEM_in,
			
			--Connect status update port to buffer
			status_update => status_update_buff_in,
			
			--Connect jump ports to buffer
			jmp => jump_buff_jmp_in,
			jeq => jump_buff_jeq_in,
			
			--Connect instr ports to buffer
			instr => instr_buff_out
		);
	
	--Instr Decoder -> Data Memories Addr buffers
	a_addr_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 6,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => jump_or_reset,
			data_in  => a_addr_buff_in,
			data_out => a_addr_buff_out
		);
	c_addr_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 6,
			data_depth => 1
		)
		port map(
			clock => clock,
			reset => jump_or_reset,
			data_in  => c_addr_buff_in,
			data_out => c_addr_buff_out
		);
	
	--Instr Decoder -> GET update buffer
	GET_update_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 1,
			data_depth => 1
		)
		port map(
			data_in(0) => GET_update_buff_c_in,
			data_out(0)  => GET_update_buff_c_out,
			clock => clock,
			reset => jump_or_reset
		);
	
	--Instr Decoder -> a Data Select buffer
	a_sel_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 3,
			data_depth => 2
		)
		port map(
			data_in(0) => a_sel_buff_REG_in,
			data_in(1) => a_sel_buff_MEM_in,
			data_in(2) => a_sel_buff_GET_in,
			data_out(0) => a_sel_buff_REG_out,
			data_out(1) => a_sel_buff_MEM_out,
			data_out(2) => a_sel_buff_GET_out,
			clock => clock,
			reset => jump_or_reset
		);
	
	--Instr Decoder -> c Data Select buffer
	c_sel_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 4,
			data_depth => 2
		)
		port map(
			data_in(0) => c_sel_buff_REG_in,
			data_in(1) => c_sel_buff_IMM_in,
			data_in(2) => c_sel_buff_MEM_in,
			data_in(3) => c_sel_buff_GET_in,
			data_out(0) => c_sel_buff_REG_out,
			data_out(1) => c_sel_buff_IMM_out,
			data_out(2) => c_sel_buff_MEM_out,
			data_out(3) => c_sel_buff_GET_out,
			clock => clock,
			reset => jump_or_reset
		);
	
	--Instr Decoder -> ALU control op_mode Buffer
	control_op_mode_buff : test_delay
		generic map (
			default_value => 0,
			data_width => 7,
			data_depth => 3
		)
		port map(
			clock => clock,
			reset => jump_or_reset,
			data_in  => control_op_mode_buff_in,
			data_out => control_op_mode_buff_out
		);
	
	--Instr Decoder -> Data Write Back buffers
	res_addr_buff_first : test_delay
		generic map (
			default_value => 0,
			data_width => 6,
			data_depth => 3
		)
		port map(
			clock => clock,
			reset => jump_or_reset,
			data_in  => res_addr_buff_in,
			data_out => res_addr_buff_mid
		);
	res_addr_buff_last : test_delay
		generic map (
			default_value => 0,
			data_width => 6,
			data_depth => 3
		)
		port map(
			clock => clock,
			reset => reset,
			data_in  => res_addr_buff_mid,
			data_out => res_addr_buff_out
		);
	
	res_select_buff_first : test_delay
		generic map (
			default_value => 0,
			data_width => 3,
			data_depth => 3
		)
		port map(
			data_in(0) => res_sel_buff_REG_in,
			data_in(1) => res_sel_buff_PUT_in,
			data_in(2) => res_sel_buff_MEM_in,
			data_out(0) => res_sel_buff_REG_mid,
			data_out(1) => res_sel_buff_PUT_mid,
			data_out(2) => res_sel_buff_MEM_mid,
			clock => clock,
			reset => jump_or_reset
		);
	res_select_buff_last : test_delay
		generic map (
			default_value => 0,
			data_width => 3,
			data_depth => 3
		)
		port map(
			data_in(0) => res_sel_buff_REG_mid,
			data_in(1) => res_sel_buff_PUT_mid,
			data_in(2) => res_sel_buff_MEM_mid,
			data_out(0) => res_sel_buff_REG_out,
			data_out(1) => res_sel_buff_PUT_out,
			data_out(2) => res_sel_buff_MEM_out,
			clock => clock,
			reset => reset
		);
		
		--Instr Decoder -> Status Register buffers
		status_update_buff_first : test_delay
			generic map (
				default_value => 0,
				data_width => 1,
				data_depth => 3
			)
			port map(
				clock => clock,
				reset => jump_or_reset,
				data_in(0)  => status_update_buff_in,
				data_out(0) => status_update_buff_mid
			);
		status_update_buff_last : test_delay
			generic map (
				default_value => 0,
				data_width => 1,
				data_depth => 3
			)
			port map(
				clock => clock,
				reset => reset,
				data_in(0)  => status_update_buff_mid,
				data_out(0) => status_update_buff_out
			);
		
		--Instr Decoder -> Program Counter buffers
		jump_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 2,
				data_depth => 3
			)
			port map(
				data_in(0) => jump_buff_jmp_in,
				data_in(1) => jump_buff_jeq_in,
				data_out(0) => jump_buff_jmp_out,
				data_out(1) => jump_buff_jeq_out,
				clock => clock,
				reset => jump_or_reset
			);
		
		--###########################################################
		--##                    Program Memory                     ##
		--###########################################################
		
		--Program Memory 
		PM: test_prog_mem
			port map (
				addr_0 => PC_buff_out,
				data_0 => instr_buff_in
			);
		
		--Program Memory -> Instr Decoder buffer
		instr_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 22,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in  => instr_buff_in,
				data_out => instr_buff_out
			);
		
		--###########################################################
		--##                   Program Counter                     ##
		--###########################################################
		
		--Program Counter 
		PC: test_prog_counter
			port map (
				--jump ports
				jump_occured => jumped_buff_in,
				jump_addr => c_selected_buff_out,
				jmp => jump_buff_jmp_out,
				jeq => jump_buff_jeq_out,
				
				--status ports
				status_equal => status_reg_equal_out,
				
				--General Ports
				clock => clock,
				reset => reset,
				value => PC_buff_in
			);
		
		--Jump occured buffer
		jumped_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 1,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in(0)  => jumped_buff_in,
				data_out(0) => jumped_buff_out
			);
		
		--Generate jump_or_reset signal
		jump_or_reset <= jumped_buff_out or reset;
		
		--Program Counter -> Program Memory buffer
		PC_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 8,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in  => PC_buff_in,
				data_out => PC_buff_out
			);
		
		--###########################################################
		--##                    Status Register                    ##
		--###########################################################
		
		--status register
		SR: test_status_reg
			generic map (data_width => 1)
			port map (
				data_in(0) => status_reg_equal_in,
				data_out(0) => status_reg_equal_out,
				write_enable => status_update_buff_out
			);
		
		--###########################################################
		--##                      Data select                      ##
		--###########################################################
		-- a data select
		a_data_mux : priority_mux_3
			generic map (data_width => 15)
			port map (
				input_0 => a_REG_buff_out,
				input_1 => a_MEM_buff_out,
				input_2 => a_GET_buff_out,
				select_0 => a_sel_buff_REG_out,
				select_1 => a_sel_buff_MEM_out,
				select_2 => a_sel_buff_GET_out,
				data_out => a_selected_buff_in
			);
		
		-- a data select buff
		a_selected_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 15,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in  => a_selected_buff_in,
				data_out => a_selected_buff_out
			);
		-- c data select
		c_data_mux : priority_mux_4
			generic map (data_width => 24)
			port map (
				input_0 => c_REG_buff_out,
				input_1 => c_IMM_buff_out,
				input_2 => c_MEM_buff_out,
				input_3 => c_GET_buff_out,
				select_0 => c_sel_buff_REG_out,
				select_1 => c_sel_buff_IMM_out,
				select_2 => c_sel_buff_MEM_out,
				select_3 => c_sel_buff_GET_out,
				data_out => c_selected_buff_in
			);
		
		-- c data select buff
		c_selected_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 24,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in  => c_selected_buff_in,
				data_out => c_selected_buff_out
			);
		
		--###########################################################
		--##                           ALU                          ##
		--###########################################################
		ALU: test_ALU
			port map (
				--Connect up data ports
				a => a_selected_buff_out(14 downto 0),
				c => c_selected_buff_out(23 downto 0),
				
				--Data output ports
				res => result_buff_in,
				status_equal => status_reg_equal_in,
				
				--Control ports
				control_op_mode => control_op_mode_buff_out,
				
				clock => clock,
				reset => reset
			);
		
		--ALU -> Data Write Back buffer
		result_buff : test_delay
			generic map (
				default_value => 0,
				data_width => 24,
				data_depth => 1
			)
			port map(
				clock => clock,
				reset => reset,
				data_in  => result_buff_in,
				data_out => result_buff_out
			);
	end architecture;