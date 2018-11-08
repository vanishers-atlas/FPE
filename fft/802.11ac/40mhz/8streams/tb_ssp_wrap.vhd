library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity tb_ssp_wrap is
end tb_ssp_wrap;

architecture structure of tb_ssp_wrap is
  constant CORE_WIDTH     : integer := 32;
  constant INPUT_WIDTH    : integer := 32;
  constant OUTPUT_WIDTH   : integer := 32;
  constant EXIN_FIFO_NUM  : integer := 16;
  constant EXOUT_FIFO_NUM : integer := 8;
  
	signal rst : std_logic := '1';
	signal clk : std_logic := '1';
	signal push_ch_data : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal push_ch_full : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal push_ch_write : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	
	signal pop_ch_data : VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
	signal pop_ch_read : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others => '0');
	signal pop_ch_empty : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
	
	constant CLK_PERIOD : TIME := 10 ns;
begin
  
  u_ssp: ssp_wrap
		generic map (		  
		  CORE_WIDTH     => CORE_WIDTH,
		  INPUT_WIDTH    => INPUT_WIDTH,
		  OUTPUT_WIDTH   => OUTPUT_WIDTH,
      EXIN_FIFO_NUM  => EXIN_FIFO_NUM,
      EXOUT_FIFO_NUM => EXOUT_FIFO_NUM,
      IOFIFODEPTH    => 1024
    )
		port map(
		clk => clk,
		rst => rst,
    
    i_en_spu => '1',
    o_barrier => open,

		i_push_ch_data => push_ch_data,
		i_push_ch_write=> push_ch_write,
		o_push_ch_full => push_ch_full,

		o_pop_ch_data  => pop_ch_data,
		i_pop_ch_read  => pop_ch_read, 
		o_pop_ch_empty => pop_ch_empty
    );

	u_data_in: data_in
		generic map(
    ARRAY_NUM   => EXIN_FIFO_NUM,
		RF_IO_WIDTH => CORE_WIDTH
    )
		port map(
    clk         => clk, 
		o_rst       => rst,
		i_pm_finish => '1',
		o_data      => push_ch_data,
		o_data_wen	=> push_ch_write
    );
  
	clk_gen_proc: process
	begin		
		loop		  
		  wait for CLK_PERIOD/2;
		  clk <= '1';
		  wait for CLK_PERIOD/2;
		  clk <= '0';
		end loop;
	end process;

end structure;

