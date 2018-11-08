library ieee;
use ieee.std_logic_1164.ALL;
use ieee.std_logic_arith.all;
library work;
use work.ssp_pkg.all;

entity ssp_deconst is
generic(
	 WIDTH : integer := 16;-- set to how wide fifo is to be
	 MODULATION : string := "16QAM"); 
port( 
    i_data    : in     std_logic_vector (WIDTH -1 downto 0);
    o_data		: out    std_logic_vector (WIDTH -1 downto 0);
    clk       : in     std_logic;
	 rst				: in	   std_logic);
end ssp_deconst ;

architecture behaviour of ssp_deconst is

constant a1 : std_logic_vector(15 downto 0) := "0000000001010001"; -- 0.3162
constant a2 : std_logic_vector(15 downto 0) := "1111111110101111"; -- -0.3162
constant a3 : std_logic_vector(15 downto 0) := "0000000011110011"; -- 0.9487
constant a4 : std_logic_vector(15 downto 0) := "1111111100001101"; -- -0.9487
constant a5 : signed(15 downto 0) := "0000000010100010"; -- 0.6324
constant a6 : signed(15 downto 0) := "1111111101011110"; -- -0.6324

constant a7 : std_logic_vector(15 downto 0) := "0000000010110101"; -- 0.7071
constant a8 : std_logic_vector(15 downto 0) := "1111111101001010"; -- -0.7071
constant zero : signed(15 downto 0):="0000000000000000";
                         
constant a9 : std_logic_vector(15 downto 0) := "1111111011101011"; -- -1.0801
constant a10 : std_logic_vector(15 downto 0) := "1111111100111010"; -- -0.7715
constant a11 : std_logic_vector(15 downto 0) := "1111111110001001"; -- -0.4629
constant a12 : std_logic_vector(15 downto 0) := "1111111111011000"; -- -0.1543
constant a13 : std_logic_vector(15 downto 0) := "0000000000100111"; -- 0.1543
constant a14 : std_logic_vector(15 downto 0) := "0000000001110110"; -- 0.4629
constant a15 : std_logic_vector(15 downto 0) := "0000000011000101"; -- 0.7715
constant a16 : std_logic_vector(15 downto 0) := "0000000100010100"; -- 1.0801
constant a17 : signed(15 downto 0) := "0000000010100010"; -- 0.3086
constant a18 : signed(15 downto 0) := "1111111101011110"; -- -0.3086
constant a19 : signed(15 downto 0) := "0000000010100010"; -- 0.6172
constant a20 : signed(15 downto 0) := "1111111101011110"; -- -0.6172
constant a21 : signed(15 downto 0) := "0000000010100010"; -- 0.9258
constant a22 : signed(15 downto 0) := "1111111101011110"; -- -0.9258

signal sgn_data : signed(15 downto 0);
signal dout : std_logic_vector(15 downto 0);
signal flag_4qam : std_logic_vector(0 downto 0);
signal flag_16qam : std_logic_vector(1 downto 0);
signal flag_64qam : std_logic_vector(2 downto 0);

begin
u_conv1:conv_std_logic_vector_to_signed generic map(WIDTH=>WIDTH) 
			port map(a=>i_data, b=>sgn_data);
			
Gen4QAM: if MODULATION = "4QAM" generate
	flag_proc: process(clk, rst)
		begin
			if rst = '1' then
				flag_4qam <= (others => '0');
			elsif clk'event and clk = '1' then
				if (sgn_data >= zero) then			
					flag_4qam <= "1";
				else
					flag_4qam <= "0";      
				end if;
			end if;
	end process;

	data_reg: process(clk, rst)
		begin
			if rst = '1' then
				dout <= (others => '0');
			elsif clk'event and clk = '1' then
			  case flag_4qam is
					when "0" => dout <= a8;
					when "1" => dout <= a7;
					when others   => null;
				end case;
			end if;
	end process;
end generate;

Gen16QAM: if MODULATION = "16QAM" generate
	flag_proc: process(clk, rst)
		begin
			if rst = '1' then
				flag_16qam <= (others => '0');
			elsif clk'event and clk = '1' then
				if (sgn_data >= a5) then			
					flag_16qam <= "00";
				elsif (sgn_data < a5) and (sgn_data >= zero) then
					flag_16qam <= "01";
				elsif (sgn_data < zero) and (sgn_data >= a6)  then
					flag_16qam <= "10" ;
				else
					flag_16qam <= "11";      
				end if;
			end if;
	end process;

	data_reg: process(clk, rst)
		begin
			if rst = '1' then
				dout <= (others => '0');
			elsif clk'event and clk = '1' then
			  case flag_16qam is
					when "00" => dout <= a3;
					when "01" => dout <= a1;
					when "10" => dout <= a2;
					when "11" => dout <= a4;
					when others   => null;
				end case;
			end if;
	end process;
end generate;
			
Gen64QAM: if MODULATION = "64QAM" generate
	flag_proc: process(clk, rst)
		begin
			if rst = '1' then
				flag_64qam <= (others => '0');
			elsif clk'event and clk = '1' then
				if (sgn_data >= a21) then			
					flag_64qam <= "000";
				elsif (sgn_data < a21) and (sgn_data >= a19) then
					flag_64qam <= "001";
				elsif (sgn_data < a19) and (sgn_data >= a17)  then
					flag_64qam <= "010" ;
				elsif (sgn_data < a17) and (sgn_data >= zero)  then
					flag_64qam <= "011" ;
				elsif (sgn_data < zero) and (sgn_data >= a18) then
					flag_64qam <= "100";
				elsif (sgn_data < a18) and (sgn_data >= a20)  then
					flag_64qam <= "101" ;
				elsif (sgn_data < a20) and (sgn_data >= a22)  then
					flag_64qam <= "110" ;
				else
					flag_64qam <= "111";      
				end if;
			end if;
	end process;

	data_reg: process(clk, rst)
		begin
			if rst = '1' then
				dout <= (others => '0');
			elsif clk'event and clk = '1' then
			  case flag_64qam is
					when "000" => dout <= a16;
					when "001" => dout <= a15;
					when "010" => dout <= a14;
					when "011" => dout <= a13;
					when "100" => dout <= a12;
					when "101" => dout <= a11;
					when "110" => dout <= a10;
					when "111" => dout <= a9;
					when others   => null;
				end case;
			end if;
	end process;
end generate;

    -- Register output
    u_data_reg_Pa0: spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dout, o_d=>o_data);
				 
--o_data <= dout;
		
end behaviour;
