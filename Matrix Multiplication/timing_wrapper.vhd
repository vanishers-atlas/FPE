----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:13:10 10/24/2011 
-- Design Name: 
-- Module Name:    timing_wrapper - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------

--**
--* Entity timing_wrapper
--**
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity timing_wrapper is 
generic (      
      CORE_WIDTH     : integer := 32;
      INPUT_WIDTH    : integer := 32;
      OUTPUT_WIDTH   : integer := 32;
      EXIN_FIFO_NUM  : integer := 8;
      EXOUT_FIFO_NUM : integer := 8);
  port (
    clk : in std_logic;

    i_push_ch_data  : in  std_logic_vector(CORE_WIDTH-1 downto 0);
    i_push_ch_write : in  std_logic; 

    o_pop_ch_data   : out std_logic_vector(CORE_WIDTH-1 downto 0);
    i_pop_ch_read   : in  std_logic);
end timing_wrapper;

architecture Behavioral of timing_wrapper is
	signal push_ch_data : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal push_ch_write : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	
	signal pop_ch_data : VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
	signal pop_ch_read : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
  
  signal rst : std_logic;
  
begin
  rst <= '0';
  
  u_s2p_conv:s2p_fifoin generic map
    (DATA_WIDTH => CORE_WIDTH, CH_NUM => EXIN_FIFO_NUM)
	port map(clk => clk, rst => rst,
	i_push_ch_data => i_push_ch_data,
	i_push_ch_write => i_push_ch_write,
	o_push_ch_write => push_ch_write,
	o_push_ch_data => push_ch_data);
  
  u_s2p_conv1:s2p_fiforead generic map
    (DATA_WIDTH => CORE_WIDTH, CH_NUM => EXOUT_FIFO_NUM)
	port map(clk => clk, rst => rst,
	i_pop_ch_read => i_pop_ch_read,
	o_pop_ch_read => pop_ch_read);
  
  u_p2s_conv:p2s_fifoout generic map
    (DATA_WIDTH => CORE_WIDTH, CH_NUM => EXOUT_FIFO_NUM)
	port map(clk => clk, rst => rst,
  i_pop_ch_read => i_pop_ch_read,
	i_pop_ch_data => pop_ch_data,
  o_pop_ch_data => o_pop_ch_data);


  u_core: ssp_wrap
  generic map (
    CORE_WIDTH => CORE_WIDTH,
    INPUT_WIDTH => INPUT_WIDTH,
    OUTPUT_WIDTH => OUTPUT_WIDTH,
    EXIN_FIFO_NUM  => EXIN_FIFO_NUM,
    EXOUT_FIFO_NUM => EXOUT_FIFO_NUM
  )
  port map(
  clk => clk,
  rst => rst,

  i_push_ch_data => push_ch_data,
  i_push_ch_write=> push_ch_write,
  o_push_ch_full => open,

  o_pop_ch_data  => pop_ch_data,
  i_pop_ch_read  => pop_ch_read, 
  o_pop_ch_empty => open);
    
end Behavioral;

--**
--* Entity s2p_fifoin
--**   
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity s2p_fifoin is
generic(DATA_WIDTH    : integer := 16;
        CH_NUM		: integer := 128);
port(clk, rst : in std_logic;

-- convert one to CH_NUM reads
i_push_ch_data  : in  std_logic_vector(DATA_WIDTH-1 downto 0);
i_push_ch_write : in  std_logic; 


o_push_ch_write : out VSIG_TYPE(CH_NUM-1 downto 0); 
o_push_ch_data : out VDATA_TYPE(CH_NUM-1 downto 0));
end s2p_fifoin;

architecture beh of s2p_fifoin is

signal ch_write_shift_reg : VSIG_TYPE(CH_NUM-1 downto 0);
signal push_ch_data_reg : VDATA_TYPE(CH_NUM-1 downto 0);

begin

o_push_ch_write <= ch_write_shift_reg;
o_push_ch_data <= push_ch_data_reg;

write_buffer_replication_gen:
  for i in 0 to CH_NUM-1 generate		
    u_buf_write:spu_generic_reg1 generic map(REG_NUM=>1) 
    port map(clk=>clk, rst=>open, i_d=>i_push_ch_write, o_d=>ch_write_shift_reg(i));
end generate;

s2p_proc:process(clk, rst)
 begin
	if rst = '1' then
	  push_ch_data_reg <= (others => (others=>'0'));
	elsif (clk'event and clk = '1') then
	  push_ch_data_reg(CH_NUM-1 downto 1) <= push_ch_data_reg(CH_NUM-2 downto 0);  		   
	  push_ch_data_reg(0) <= i_push_ch_data;	 
	end if;
end process;

end beh;

--**
--* Entity s2p_fifoin
--**   
library ieee;
use ieee.std_logic_1164.ALL;

library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity s2p_fiforead is
generic(DATA_WIDTH    : integer := 16;
        CH_NUM		: integer := 128);
port(clk, rst : in std_logic;

-- convert one to CH_NUM reads
i_pop_ch_read  : in std_logic;

o_pop_ch_read  : out VSIG_TYPE(CH_NUM-1 downto 0)
);
end s2p_fiforead;

architecture beh of s2p_fiforead is

signal ch_read_shift_reg : VSIG_TYPE(CH_NUM-1 downto 0);

begin

o_pop_ch_read  <= ch_read_shift_reg;

read_buffer_replication_gen:
  for i in 0 to CH_NUM-1 generate		
    u_buf_read:spu_generic_reg1 generic map(REG_NUM=>1) 
    port map(clk=>clk, rst=>open, i_d=>i_pop_ch_read, o_d=>ch_read_shift_reg(i));
end generate;

end beh;
--**
--* Entity p2s_fifoout
--** 
library ieee;
use ieee.std_logic_1164.ALL;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity p2s_fifoout is
generic(DATA_WIDTH    : integer := 32;
        CH_NUM		: integer := 1);
port(clk, rst : in std_logic;
i_pop_ch_read     : in std_logic;
i_pop_ch_data  : in VDATA_TYPE(CH_NUM-1 downto 0);
o_pop_ch_data  : out std_logic_vector(DATA_WIDTH-1 downto 0));
end p2s_fifoout;

architecture beh of p2s_fifoout is
--             d0          d1            dn-1
--             |           |             |   
--          /| |        /| |          /| |     
--out .-.  | |-'  .-.  | |-'  .-.    | |-'   
--  --| |--| |----| |--| |----| | ...| |--'0'
--  0 '-'   \|   1'-'   \|   2'-'     \|     
  signal pop_ch_data_reg : VDATA_TYPE(CH_NUM-1 downto 0);
  signal mux_out : VDATA_TYPE(CH_NUM-1 downto 0);
  signal pop_ch_read_buf1 : std_logic;
  signal pop_ch_read_buf2 : VSIG_TYPE(CH_NUM-1 downto 0);
  constant ALL_ZERO : std_logic_vector(DATA_WIDTH-1 downto 0) := (others =>'0');
begin

u_buf_read:spu_generic_reg1 generic map(REG_NUM=>1) 
    port map(clk=>clk, rst=>rst, i_d=>i_pop_ch_read, o_d=>pop_ch_read_buf1);
    
read_buffer_replication_gen:
  for i in 0 to CH_NUM-1 generate		
    u_buf_read:spu_generic_reg1 generic map(REG_NUM=>1) 
    port map(clk=>clk, rst=>open, i_d=>pop_ch_read_buf1, o_d=>pop_ch_read_buf2(i));
end generate;

mux_gen:
for i in 0 to CH_NUM-2 generate	
  u_p2s_mux:spu_mux_2to1 generic map(DATA_WIDTH=>DATA_WIDTH)
      port map(i_d0=>i_pop_ch_data(i), i_d1=>pop_ch_data_reg(i+1), sel=>pop_ch_read_buf2(i), o_d=>mux_out(i));
end generate;
u_p2s_mux_last:spu_mux_2to1 generic map(DATA_WIDTH=>DATA_WIDTH)
    port map(i_d0=>i_pop_ch_data(CH_NUM-1), i_d1=>ALL_ZERO, sel=>pop_ch_read_buf2(CH_NUM-1), o_d=>mux_out(CH_NUM-1));

p2s_proc:process(clk, rst)
 begin
	if rst = '1' then
	  pop_ch_data_reg <= (others => (others=>'0'));
	elsif (clk'event and clk = '1') then
    pop_ch_data_reg <= mux_out;   
	end if;
end process;

o_pop_ch_data <= pop_ch_data_reg(0);
end beh;