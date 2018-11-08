library ieee;
use ieee.std_logic_1164.ALL;
use ieee.std_logic_arith.all;
library work;
use work.ssp_pkg.all;

entity ca_deconst is
generic(WIDTH : integer := 16); -- set to how wide fifo is to be
port( 
    i_data    : in     std_logic_vector (WIDTH -1 downto 0);
    o_data		: out    std_logic_vector (WIDTH -1 downto 0);
    clk       : in     std_logic;
	 rst				: in	   std_logic);
end ca_deconst ;

architecture behaviour of ca_deconst is

constant a1 : std_logic_vector(15 downto 0) := "0000000001010001"; -- 0.3162
constant a2 : std_logic_vector(15 downto 0) := "1111111110101111"; -- -0.3162
constant a3 : std_logic_vector(15 downto 0) := "0000000011110011"; -- 0.9487
constant a4 : std_logic_vector(15 downto 0) := "1111111100001101"; -- -0.9487
constant a5 : signed(15 downto 0) := "0000000010100010"; -- 0.6324
constant a6 : signed(15 downto 0) := "1111111101011110"; -- -0.6324
constant zero : signed(15 downto 0):="0000000000000000";

signal sgn_data : signed(15 downto 0);
signal dout : std_logic_vector(15 downto 0);
signal flag : std_logic_vector(1 downto 0);

begin
u_conv1:conv_std_logic_vector_to_signed generic map(WIDTH=>WIDTH) 
			port map(a=>i_data, b=>sgn_data);

flag_proc: process(clk, rst)
	begin
		if rst = '1' then
			flag <= (others => '0');
		elsif clk'event and clk = '1' then
			if (sgn_data >= a5) then			
				flag <= "00";
			elsif (sgn_data < a5) and (sgn_data >= zero) then
				flag <= "01";
			elsif (sgn_data < zero) and (sgn_data >= a6)  then
				flag <= "10" ;
			else
				flag <= "11";      
         end if;
		end if;
end process;

data_reg: process(clk, rst)
	begin
		if rst = '1' then
			dout <= (others => '0');
		elsif clk'event and clk = '1' then
		  case flag is
				when "00" => dout <= a3;
				when "01" => dout <= a1;
				when "10" => dout <= a2;
				when others => dout <= a4;
			end case;
		end if;
end process;
				 
o_data <= dout;
		
end behaviour;