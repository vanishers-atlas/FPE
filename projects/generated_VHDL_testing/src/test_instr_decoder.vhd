--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package test_instr_decoder_pkg is
	component test_instr_decoder is
		port (
			--Data Address Ports
			a_addr : out std_logic_vector(5 downto 0);
			c_addr : out std_logic_vector(5 downto 0);
			
			--Comm get update Ports
			c_update : out std_logic;
			
			--a Select Ports
			a_sel_REG : out std_logic;
			a_sel_MEM : out std_logic;
			a_sel_GET : out std_logic;
			
			--c Select Ports
			c_sel_REG : out std_logic;
			c_sel_IMM : out std_logic;
			c_sel_MEM : out std_logic;
			c_sel_GET : out std_logic;
			
			--ALU Control Ports
			control_op_mode : out std_logic_vector(6 downto 0);
			
			--Write Back Ports
			res_addr : out std_logic_vector(5 downto 0);
			res_sel_REG : out std_logic;
			res_sel_PUT : out std_logic;
			res_sel_MEM : out std_logic;
			
			--Status Registor Update Port
			status_update : out std_logic;
			
			--Jump Ports
			jmp : out std_logic;
			jeq : out std_logic;
			
			--Input instruction Port
			instr : in std_logic_vector(21 downto 0)
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;

entity test_instr_decoder is
	port (
		--Data Address Ports
		a_addr : out std_logic_vector(5 downto 0);
		c_addr : out std_logic_vector(5 downto 0);
		
		--Comm get update Ports
		c_update : out std_logic;
		
		--a Select Ports
		a_sel_REG : out std_logic;
		a_sel_MEM : out std_logic;
		a_sel_GET : out std_logic;
		
		--c Select Ports
		c_sel_REG : out std_logic;
		c_sel_IMM : out std_logic;
		c_sel_MEM : out std_logic;
		c_sel_GET : out std_logic;
		
		--ALU Control Ports
		control_op_mode : out std_logic_vector(6 downto 0);
		
		--Write Back Ports
		res_addr : out std_logic_vector(5 downto 0);
		res_sel_REG : out std_logic;
		res_sel_PUT : out std_logic;
		res_sel_MEM : out std_logic;
		
		--Status Registor Update Port
		status_update : out std_logic;
		
		--Jump Ports
		jmp : out std_logic;
		jeq : out std_logic;
		
		--Input instruction Port
		instr : in std_logic_vector(21 downto 0)
	);
end entity;

architecture arch of test_instr_decoder is
	--Extracted op_code Signal
	signal op_code : std_logic_vector(3 downto 0);
begin
	-- Extract op_code and addrs from instr
	op_code <= instr(21 downto 18);
	res_addr <= instr(17 downto 12);
	a_addr <= instr(11 downto 6);
	c_addr <= instr(5 downto 0);
	
	--Handle Data Access decoding
	process(op_code)
		variable int_op_code : integer := to_integer(unsigned(op_code));
	begin
		--Generate Comm Get update signals
		c_update <= '1' when int_op_code = 141
			or int_op_code = 142
			or int_op_code = 143
			or int_op_code = 204
			or int_op_code = 304
		else '0';
		
		--Generate a select signals
		a_sel_REG <= '1' when int_op_code = 410
		else '0';
		a_sel_MEM <= '1' when int_op_code = 420
		else '0';
		a_sel_GET <= '1' when int_op_code = 430
		else '0';
		
		--Generate c select signals
		c_sel_REG <= '1' when int_op_code = 111
			or int_op_code = 112
			or int_op_code = 113
			or int_op_code = 201
			or int_op_code = 301
		else '0';
		c_sel_IMM <= '1' when int_op_code = 101
			or int_op_code = 102
			or int_op_code = 103
			or int_op_code = 200
			or int_op_code = 300
			or int_op_code = 410
			or int_op_code = 420
			or int_op_code = 430
		else '0';
		c_sel_MEM <= '1' when int_op_code = 121
			or int_op_code = 122
			or int_op_code = 123
			or int_op_code = 202
			or int_op_code = 302
		else '0';
		c_sel_GET <= '1' when int_op_code = 131
			or int_op_code = 132
			or int_op_code = 133
			or int_op_code = 141
			or int_op_code = 142
			or int_op_code = 143
			or int_op_code = 203
			or int_op_code = 204
			or int_op_code = 303
			or int_op_code = 304
		else '0';
		
		--Generate op_mode signal
		control_op_mode <= std_logic_vector(to_unsigned(51, 7)) when int_op_code = 410
			or int_op_code = 420
			or int_op_code = 430
		else std_logic_vector(to_unsigned(48, 7));
		
		--Generate Result destination select signals
		res_sel_REG <= '1' when int_op_code = 101
			or int_op_code = 111
			or int_op_code = 111
			or int_op_code = 112
			or int_op_code = 113
			or int_op_code = 121
			or int_op_code = 131
			or int_op_code = 141
			or int_op_code = 201
			or int_op_code = 301
			or int_op_code = 410
		else '0';
		res_sel_PUT <= '1' when int_op_code = 103
			or int_op_code = 113
			or int_op_code = 123
			or int_op_code = 133
			or int_op_code = 143
		else '0';
		res_sel_MEM <= '1' when int_op_code = 102
			or int_op_code = 112
			or int_op_code = 121
			or int_op_code = 122
			or int_op_code = 122
			or int_op_code = 123
			or int_op_code = 132
			or int_op_code = 142
			or int_op_code = 202
			or int_op_code = 302
			or int_op_code = 420
		else '0';
		
		--Generate Status Registor Update signal
		status_update <= '1' when int_op_code = 410
			or int_op_code = 410
			or int_op_code = 420
			or int_op_code = 420
			or int_op_code = 430
			or int_op_code = 430
		else '0';
		
		--Generate Jump signals
		jmp <= '1' when int_op_code = 200
			or int_op_code = 201
			or int_op_code = 202
			or int_op_code = 203
			or int_op_code = 204
		else '0';
		jeq <= '1' when int_op_code = 300
			or int_op_code = 301
			or int_op_code = 302
			or int_op_code = 303
			or int_op_code = 304
		else '0';
	end process;
end architecture;