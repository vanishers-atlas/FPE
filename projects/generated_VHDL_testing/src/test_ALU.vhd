--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

library UNISIM;
use UNISIM.vcomponents.all;

package test_ALU_pkg is
	component test_ALU is
		port (
			--Data input data ports
			a : in std_logic_vector(14 downto 0);
			c : in std_logic_vector(23 downto 0);
			
			--Data output port
			res : out std_logic_vector(24 downto 0);
			status_equal : out std_logic;
			
			--Control ports
			control_op_mode : in std_logic_vector(6 downto 0);
			
			clock : in std_logic;
			reset : in std_logic
		);
	end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in implanentation
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
Library UNISIM;
use UNISIM.vcomponents.all;

entity test_ALU is
	port (
		--Data input data ports
		a : in std_logic_vector(14 downto 0);
		c : in std_logic_vector(23 downto 0);
		
		--Data output port
		res : out std_logic_vector(24 downto 0);
		status_equal : out std_logic;
		
		--Control ports
		control_op_mode : in std_logic_vector(6 downto 0);
		
		clock : in std_logic;
		reset : in std_logic
	);
end entity;

architecture arch of test_ALU is
	signal res_data : std_logic_vector(23 downto 0);
begin
	--DSP Slice
	DSP48E1_inst : DSP48E1
		generic map (
			--Don't buffer output to give 2 clock cycle pipeline through DSP slice
			PREG => 0,
			
			--Setup pattern to check of zero result
			USE_PATTERN_DETECT => "PATDET",
			
			--Disable preadder and multipler
			USE_MULT => "NONE"
		)
		port map (
			clk => clock,
			
			--Set up Data Inputs ports
			A => (14 downto 0 => a, others => '0'),
			CEA1 => clock,
			CEA2 => clock,
			RSTA => reset,
			B => (others => '1'),
			CEB1 => '0',
			CEB2 => '0',
			RSTB => '0',
			D => (others => '1'),
			CED  => '0',
			RSTD => '0',
			C => (23 downto 0 => c, others => '0'),
			CEC  => clock,
			RSTC => reset,
			
			--Set up Result Output ports
			P(23 downto 0) => res_data,
			P(47 downto 24) => open,
			CEP  => '0',
			RSTP => '0',
			
			--Set up Control ports
			INMODE => (others => '1'),
			CEINMODE  => '0',
			RSTINMODE => '0',
			ALUMODE => std_logic_vector(to_unsigned(3, 4)),
			CEALUMODE  => clock,
			RSTALUMODE => reset,
			CARRYIN => '0',
			CECARRYIN => clock,
			RSTALLCARRYIN => reset,
			CARRYINSEL => std_logic_vector(to_unsigned(0, 4)),
			OPMODE => control_op_mode,
			CECTRL  => clock,
			RSTCTRL => reset,
			PATTERNDETECT  => status_equal,
			PATTERNBDETECT => open,
			
			--Disable Preadder and multiple ports
			CEM  => '0',
			CEAD => '0',
			RSTM => '0',
			MULTSIGNIN  => '1',
			MULTSIGNOUT => open,
			
			--carryout, underflow, and underflow ports
			CARRYOUT   => open,
			OVERFLOW   => open,
			UNDERFLOW  => open,
			ACIN  => (others => '1'),
			BCIN  => (others => '1'),
			PCIN  => (others => '1'),
			CARRYCASCIN => '1',
			ACOUT  => open,
			BCOUT  => open,
			PCOUT  => open,
			CARRYCASCOUT  => open
		);
		
		--Connect DSP to res port
		res <= res_data;
	end architecture;