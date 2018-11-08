----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05.07.2017 12:11:41
-- Design Name: 
-- Module Name: ssp_cache_core_wrap_stage_1st - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library ieee;  
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.numeric_std.all;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;
library unisim;
use unisim.vcomponents.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ssp_cache_core_wrap_stage_1st is
		generic ( 
			CORE_WIDTH : integer := 32;
			INPUT_WIDTH : integer := 32;
			OUTPUT_WIDTH : integer := 32;
			EXIN_FIFO_NUM : integer := 2;
			EXOUT_FIFO_NUM : integer := 1;
            DEXOUT_FIFO_NUM : integer := 1;
			INPUT_WORDS : integer := 1024;
			OUTPUT_WORDS : integer := 2048;
			DOUTPUT_WORDS : integer := 1;
			IOFIFODEPTH : integer := 1024
		);
		port(
			clk : in std_logic := '0';
			rst : in std_logic := '0';
			i_data_last : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_data_last: out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			i_push_ch_data : in VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
			i_push_ch_write : in VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_push_ch_read : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_push_ch_empty : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_push_ch_full : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_push_ch_en : out VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
			o_pop_ch_data : out VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
			o_pop_ch_write : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			i_pop_ch_read : in VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			o_pop_ch_empty : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			o_pop_ch_full : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			o_pop_ch_en : out VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			tlast_asserted : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			-- debug port	
			o_ddata_last : out VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0);		
			o_dpop_ch_data : out VDATA_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
			o_dpop_ch_write : out VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			i_dpop_ch_read : in VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			o_dpop_ch_empty : out VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			o_dpop_ch_en : out VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			dtlast_asserted : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
			-- for debug signal 
			spu_en_1: out std_logic;
            spu_en_2: out std_logic;
            spu_en_3: out std_logic;
            spu_en_4: out std_logic;
            spu_en_5: out std_logic;
            spu_en_6: out std_logic;
            fifo_end_1: out std_logic;
            fifo_end_2: out std_logic;
            fifo_end_3: out std_logic;
            fifo_end_4: out std_logic;
            fifo_end_5: out std_logic;
            fifo_end_6: out std_logic
		);
end ssp_cache_core_wrap_stage_1st;

architecture Behavioral of ssp_cache_core_wrap_stage_1st is

  -- Component Declaration
	COMPONENT ssp_fifo_cache
		generic ( 
			WIDTH    : integer := 16;  -- the data width of sync fifo
			DEPTH    : integer := 1024;  -- the size of sync fifo
			OUT_REG_NUM  : integer := 1;
			STATE_EN : boolean := true
		);

		port(
			clk          : in     std_logic;  -- clock signal 
			rst          : in     std_logic;  -- reset signal 
			i_data       : in     std_logic_vector (WIDTH -1 downto 0);  -- input data
			o_data       : out    std_logic_vector (WIDTH -1 downto 0);  -- output data
			i_write      : in     std_logic;  -- write fifo request signal 
			i_read       : in     std_logic;  -- read fifo request signal 
			o_full       : out    std_logic; -- fifo is full signal
			o_almostfull : out    std_logic; -- fifo is almost full signal 
			o_empty      : out    std_logic; -- fifo can take data signal 

			-- additive signal
			i_data_end_s   : in     std_logic; -- end of input data signal 
			i_data_end_e   : in     std_logic; -- end of input data signal 
			o_pc_en      : out    std_logic -- output enable signal
		);
	END COMPONENT;    
	
        
    signal ch_SOURCE_to_PE_1_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_SOURCE_to_PE_1_1_write : std_logic;
    signal ch_SOURCE_to_PE_1_1_full : std_logic;
    signal ch_SOURCE_to_PE_1_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_SOURCE_to_PE_1_1_read : std_logic;
    signal ch_SOURCE_to_PE_1_1_empty : std_logic;
    signal ch_SOURCE_to_PE_1_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_SOURCE_to_PE_1_1_write_1 : std_logic;
    signal ch_SOURCE_to_PE_1_1_full_1 : std_logic;
    signal ch_SOURCE_to_PE_1_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_SOURCE_to_PE_1_1_read_1 : std_logic;
    signal ch_SOURCE_to_PE_1_1_empty_1 : std_logic;
    
    signal ch_PE_1_1_to_PE_2_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_1_1_to_PE_2_1_write : std_logic;
    signal ch_PE_1_1_to_PE_2_1_full : std_logic;
    signal ch_PE_1_1_to_PE_2_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_1_1_to_PE_2_1_read : std_logic;
    signal ch_PE_1_1_to_PE_2_1_empty : std_logic;
    signal ch_PE_1_1_to_PE_2_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_1_1_to_PE_2_1_write_1 : std_logic;
    signal ch_PE_1_1_to_PE_2_1_full_1 : std_logic;
    signal ch_PE_1_1_to_PE_2_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_1_1_to_PE_2_1_read_1 : std_logic;
    signal ch_PE_1_1_to_PE_2_1_empty_1 : std_logic;
    
    signal ch_PE_2_1_to_PE_3_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_2_1_to_PE_3_1_write : std_logic;
    signal ch_PE_2_1_to_PE_3_1_full : std_logic;
    signal ch_PE_2_1_to_PE_3_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_2_1_to_PE_3_1_read : std_logic;
    signal ch_PE_2_1_to_PE_3_1_empty : std_logic;
    signal ch_PE_2_1_to_PE_3_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_2_1_to_PE_3_1_write_1 : std_logic;
    signal ch_PE_2_1_to_PE_3_1_full_1 : std_logic;
    signal ch_PE_2_1_to_PE_3_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_2_1_to_PE_3_1_read_1 : std_logic;
    signal ch_PE_2_1_to_PE_3_1_empty_1 : std_logic;
    
    signal ch_PE_3_1_to_PE_4_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_3_1_to_PE_4_1_write : std_logic;
    signal ch_PE_3_1_to_PE_4_1_full : std_logic;
    signal ch_PE_3_1_to_PE_4_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_3_1_to_PE_4_1_read : std_logic;
    signal ch_PE_3_1_to_PE_4_1_empty : std_logic;
    signal ch_PE_3_1_to_PE_4_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_3_1_to_PE_4_1_write_1 : std_logic;
    signal ch_PE_3_1_to_PE_4_1_full_1 : std_logic;
    signal ch_PE_3_1_to_PE_4_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_3_1_to_PE_4_1_read_1 : std_logic;
    signal ch_PE_3_1_to_PE_4_1_empty_1 : std_logic;
    
    signal ch_PE_4_1_to_PE_5_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_4_1_to_PE_5_1_write : std_logic;
    signal ch_PE_4_1_to_PE_5_1_full : std_logic;
    signal ch_PE_4_1_to_PE_5_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_4_1_to_PE_5_1_read : std_logic;
    signal ch_PE_4_1_to_PE_5_1_empty : std_logic;
    signal ch_PE_4_1_to_PE_5_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_4_1_to_PE_5_1_write_1 : std_logic;
    signal ch_PE_4_1_to_PE_5_1_full_1 : std_logic;
    signal ch_PE_4_1_to_PE_5_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_4_1_to_PE_5_1_read_1 : std_logic;
    signal ch_PE_4_1_to_PE_5_1_empty_1 : std_logic;
    
    signal ch_PE_5_1_to_PE_6_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_5_1_to_PE_6_1_write : std_logic;
    signal ch_PE_5_1_to_PE_6_1_full : std_logic;
    signal ch_PE_5_1_to_PE_6_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_5_1_to_PE_6_1_read : std_logic;
    signal ch_PE_5_1_to_PE_6_1_empty : std_logic;
    signal ch_PE_5_1_to_PE_6_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_5_1_to_PE_6_1_write_1 : std_logic;
    signal ch_PE_5_1_to_PE_6_1_full_1 : std_logic;
    signal ch_PE_5_1_to_PE_6_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_5_1_to_PE_6_1_read_1 : std_logic;
    signal ch_PE_5_1_to_PE_6_1_empty_1 : std_logic;
        
    signal ch_PE_6_1_to_PE_7_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_6_1_to_PE_7_1_write : std_logic;
    signal ch_PE_6_1_to_PE_7_1_full : std_logic;
    signal ch_PE_6_1_to_PE_7_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_6_1_to_PE_7_1_read : std_logic;
    signal ch_PE_6_1_to_PE_7_1_empty : std_logic;
    signal ch_PE_6_1_to_PE_7_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_6_1_to_PE_7_1_write_1 : std_logic;
    signal ch_PE_6_1_to_PE_7_1_full_1 : std_logic;
    signal ch_PE_6_1_to_PE_7_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_6_1_to_PE_7_1_read_1 : std_logic;
    signal ch_PE_6_1_to_PE_7_1_empty_1 : std_logic;
        
    signal ch_PE_7_1_to_PE_8_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_7_1_to_PE_8_1_write : std_logic;
    signal ch_PE_7_1_to_PE_8_1_full : std_logic;
    signal ch_PE_7_1_to_PE_8_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_7_1_to_PE_8_1_read : std_logic;
    signal ch_PE_7_1_to_PE_8_1_empty : std_logic;
    signal ch_PE_7_1_to_PE_8_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_7_1_to_PE_8_1_write_1 : std_logic;
    signal ch_PE_7_1_to_PE_8_1_full_1 : std_logic;
    signal ch_PE_7_1_to_PE_8_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_7_1_to_PE_8_1_read_1 : std_logic;
    signal ch_PE_7_1_to_PE_8_1_empty_1 : std_logic;
        
    signal ch_PE_8_1_to_PE_9_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_8_1_to_PE_9_1_write : std_logic;
    signal ch_PE_8_1_to_PE_9_1_full : std_logic;
    signal ch_PE_8_1_to_PE_9_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_8_1_to_PE_9_1_read : std_logic;
    signal ch_PE_8_1_to_PE_9_1_empty : std_logic;
    signal ch_PE_8_1_to_PE_9_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_8_1_to_PE_9_1_write_1 : std_logic;
    signal ch_PE_8_1_to_PE_9_1_full_1 : std_logic;
    signal ch_PE_8_1_to_PE_9_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_8_1_to_PE_9_1_read_1 : std_logic;
    signal ch_PE_8_1_to_PE_9_1_empty_1 : std_logic;
            
    signal ch_PE_9_1_to_PE_10_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_9_1_to_PE_10_1_write : std_logic;
    signal ch_PE_9_1_to_PE_10_1_full : std_logic;
    signal ch_PE_9_1_to_PE_10_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_9_1_to_PE_10_1_read : std_logic;
    signal ch_PE_9_1_to_PE_10_1_empty : std_logic;
    signal ch_PE_9_1_to_PE_10_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_9_1_to_PE_10_1_write_1 : std_logic;
    signal ch_PE_9_1_to_PE_10_1_full_1 : std_logic;
    signal ch_PE_9_1_to_PE_10_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_9_1_to_PE_10_1_read_1 : std_logic;
    signal ch_PE_9_1_to_PE_10_1_empty_1 : std_logic;
        
    signal ch_PE_10_1_to_PE_11_1_a : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_10_1_to_PE_11_1_write : std_logic;
    signal ch_PE_10_1_to_PE_11_1_full : std_logic;
    signal ch_PE_10_1_to_PE_11_1_b : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_10_1_to_PE_11_1_read : std_logic;
    signal ch_PE_10_1_to_PE_11_1_empty : std_logic;
    signal ch_PE_10_1_to_PE_11_1_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_10_1_to_PE_11_1_write_1 : std_logic;
    signal ch_PE_10_1_to_PE_11_1_full_1 : std_logic;
    signal ch_PE_10_1_to_PE_11_1_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_10_1_to_PE_11_1_read_1 : std_logic;
    signal ch_PE_10_1_to_PE_11_1_empty_1 : std_logic;

	signal ch_PE_11_1_to_SINK_a : std_logic_vector(CORE_WIDTH-1 downto 0);
	signal ch_PE_11_1_to_SINK_write : std_logic;
	signal ch_PE_11_1_to_SINK_full : std_logic;
	signal ch_PE_11_1_to_SINK_b : std_logic_vector(CORE_WIDTH-1 downto 0);
	signal ch_PE_11_1_to_SINK_read : std_logic;
	signal ch_PE_11_1_to_SINK_empty : std_logic;    
    signal ch_PE_11_1_to_SINK_a_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_11_1_to_SINK_write_1 : std_logic;
    signal ch_PE_11_1_to_SINK_full_1 : std_logic;
    signal ch_PE_11_1_to_SINK_b_1 : std_logic_vector(CORE_WIDTH-1 downto 0);
    signal ch_PE_11_1_to_SINK_read_1 : std_logic;
    signal ch_PE_11_1_to_SINK_empty_1 : std_logic;
        
	signal get_ch_data_1 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_1 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_1 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_1 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_1 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_1 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_1 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_1 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_1 : VSIG_TYPE(1-1 downto 0);
			
	signal get_ch_data_2 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_2 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_2 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_2 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_2 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_2 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_2 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_2 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_2 : VSIG_TYPE(1-1 downto 0);
			
	signal get_ch_data_3 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_3 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_3 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_3 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_3 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_3 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_3 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_3 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_3 : VSIG_TYPE(1-1 downto 0);
			
	signal get_ch_data_4 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_4 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_4 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_4 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_4 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_4 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_4 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_4 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_4 : VSIG_TYPE(1-1 downto 0);
			
	signal get_ch_data_5 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_5 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_5 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_5 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_5 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_5 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_5 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_5 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_5 : VSIG_TYPE(1-1 downto 0);
			
	signal get_ch_data_6 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_read_6 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal get_ch_empty_6 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_data_6 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_write_6 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal put_ch_full_6 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
	signal dput_ch_data_6 : VDATA_TYPE(1-1 downto 0);
	signal dput_ch_write_6 : VSIG_TYPE(1-1 downto 0);
	signal dput_ch_full_6 : VSIG_TYPE(1-1 downto 0);
                
    signal get_ch_data_7 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_read_7 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_empty_7 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_data_7 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_write_7 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_full_7 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal dput_ch_data_7 : VDATA_TYPE(1-1 downto 0);
    signal dput_ch_write_7 : VSIG_TYPE(1-1 downto 0);
    signal dput_ch_full_7 : VSIG_TYPE(1-1 downto 0);
                
    signal get_ch_data_8 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_read_8 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_empty_8 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_data_8 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_write_8 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_full_8 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal dput_ch_data_8 : VDATA_TYPE(1-1 downto 0);
    signal dput_ch_write_8 : VSIG_TYPE(1-1 downto 0);
    signal dput_ch_full_8 : VSIG_TYPE(1-1 downto 0);
                
    signal get_ch_data_9 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_read_9 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_empty_9 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_data_9 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_write_9 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_full_9 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal dput_ch_data_9 : VDATA_TYPE(1-1 downto 0);
    signal dput_ch_write_9 : VSIG_TYPE(1-1 downto 0);
    signal dput_ch_full_9 : VSIG_TYPE(1-1 downto 0);
                
    signal get_ch_data_10 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_read_10 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_empty_10 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_data_10 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_write_10 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_full_10 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal dput_ch_data_10 : VDATA_TYPE(1-1 downto 0);
    signal dput_ch_write_10 : VSIG_TYPE(1-1 downto 0);
    signal dput_ch_full_10 : VSIG_TYPE(1-1 downto 0);
                
    signal get_ch_data_11 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_read_11 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal get_ch_empty_11 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0);
    signal put_ch_data_11 : VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0);
    signal put_ch_write_11 : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
    signal put_ch_full_11 : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0);
    signal dput_ch_data_11 : VDATA_TYPE(1-1 downto 0);
    signal dput_ch_write_11 : VSIG_TYPE(1-1 downto 0);
    signal dput_ch_full_11 : VSIG_TYPE(1-1 downto 0);
	
	signal FIFO_1_in_end : std_logic;
	signal FIFO_2_in_end : std_logic;
	signal FIFO_3_in_end : std_logic;
	signal FIFO_4_in_end : std_logic;
	signal FIFO_5_in_end : std_logic;
	signal FIFO_6_in_end : std_logic;
	signal FIFO_7_in_end : std_logic;
    signal FIFO_8_in_end : std_logic;
    signal FIFO_9_in_end : std_logic;
    signal FIFO_10_in_end : std_logic;
    signal FIFO_11_in_end : std_logic;
    signal FIFO_12_in_end : std_logic;
	
	signal PE_1_1_end : std_logic;
	signal PE_2_1_end : std_logic;
	signal PE_3_1_end : std_logic;
	signal PE_4_1_end : std_logic;
	signal PE_5_1_end : std_logic;
	signal PE_6_1_end : std_logic;
    signal PE_7_1_end : std_logic;
    signal PE_8_1_end : std_logic;
    signal PE_9_1_end : std_logic;
    signal PE_10_1_end : std_logic;
    signal PE_11_1_end : std_logic;
	
	signal PE_1_1_en : std_logic;
	signal PE_1_1_en_1 : std_logic;
	signal PE_1_1_en_2 : std_logic;
	signal PE_2_1_en : std_logic;
	signal PE_2_1_en_1 : std_logic;
	signal PE_2_1_en_2 : std_logic;
	signal PE_3_1_en : std_logic;
	signal PE_3_1_en_1 : std_logic;
	signal PE_3_1_en_2 : std_logic;
	signal PE_4_1_en : std_logic;
	signal PE_4_1_en_1 : std_logic;
	signal PE_4_1_en_2 : std_logic;
	signal PE_5_1_en : std_logic;
	signal PE_5_1_en_1 : std_logic;
	signal PE_5_1_en_2 : std_logic;
	signal PE_6_1_en : std_logic;
	signal PE_6_1_en_1 : std_logic;
	signal PE_6_1_en_2 : std_logic;
    signal PE_7_1_en : std_logic;
    signal PE_7_1_en_1 : std_logic;
    signal PE_7_1_en_2 : std_logic;
    signal PE_8_1_en : std_logic;
    signal PE_8_1_en_1 : std_logic;
    signal PE_8_1_en_2 : std_logic;
    signal PE_9_1_en : std_logic;
    signal PE_9_1_en_1 : std_logic;
    signal PE_9_1_en_2 : std_logic;
    signal PE_10_1_en : std_logic;
    signal PE_10_1_en_1 : std_logic;
    signal PE_10_1_en_2 : std_logic;
    signal PE_11_1_en : std_logic;
    signal PE_11_1_en_1 : std_logic;
    signal PE_11_1_en_2 : std_logic;

begin

spu_en_1 <= PE_1_1_en;
spu_en_2 <= PE_2_1_en;
spu_en_3 <= PE_3_1_en;
spu_en_4 <= PE_4_1_en;
spu_en_5 <= PE_5_1_en;
spu_en_6 <= PE_6_1_en;

fifo_end_1 <= FIFO_1_in_end;
fifo_end_2 <= FIFO_2_in_end;
fifo_end_3 <= FIFO_3_in_end;
fifo_end_4 <= FIFO_4_in_end;
fifo_end_5 <= FIFO_5_in_end;
fifo_end_6 <= FIFO_6_in_end;
 
--u_fifo_in_data_reg_Pa00: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
--port map(clk=>clk, rst=>rst, i_d=>ch_SOURCE_to_PE_1_1_b, o_d=>get_ch_data_1(0));
--u_fifo_in_data_reg_Pa01: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
--port map(clk=>clk, rst=>rst, i_d=>ch_SOURCE_to_PE_1_1_b_1, o_d=>get_ch_data_1(1));

ch_SOURCE_to_PE_1_1_a <= i_push_ch_data(0);
o_push_ch_full(0) <= ch_SOURCE_to_PE_1_1_full;
ch_SOURCE_to_PE_1_1_write <= i_push_ch_write(0);
ch_SOURCE_to_PE_1_1_a_1 <= i_push_ch_data(1);
o_push_ch_full(1) <= ch_SOURCE_to_PE_1_1_full_1;
ch_SOURCE_to_PE_1_1_write_1 <= i_push_ch_write(1);
ch_SOURCE_to_PE_1_1_read <= get_ch_read_1(0);
get_ch_data_1(0) <= ch_SOURCE_to_PE_1_1_b;
get_ch_empty_1(0) <= ch_SOURCE_to_PE_1_1_empty;
ch_SOURCE_to_PE_1_1_read_1 <= get_ch_read_1(1);
get_ch_data_1(1) <= ch_SOURCE_to_PE_1_1_b_1;
get_ch_empty_1(1) <= ch_SOURCE_to_PE_1_1_empty_1;

o_push_ch_empty(0) <= ch_SOURCE_to_PE_1_1_empty;
o_push_ch_empty(1) <= ch_SOURCE_to_PE_1_1_empty_1;

---- for test
--ch_SOURCE_to_PE_1_1_read <= i_pop_ch_read(0);
--o_pop_ch_data(0) <= ch_SOURCE_to_PE_1_1_b;
--o_pop_ch_empty(0) <= ch_SOURCE_to_PE_1_1_empty;
--o_pop_ch_full(0) <= ch_SOURCE_to_PE_1_1_full;
--ch_SOURCE_to_PE_1_1_read_1 <= i_pop_ch_read(1);
--o_pop_ch_data(1) <= ch_SOURCE_to_PE_1_1_b_1;
--o_pop_ch_empty(1) <= ch_SOURCE_to_PE_1_1_empty_1;
--o_pop_ch_full(1) <= ch_SOURCE_to_PE_1_1_full_1;
 
u_fifo_in_data_reg_Pa0: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_1(0), o_d=>ch_PE_1_1_to_PE_2_1_a);
u_fifo_in_data_reg_Pa1: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_1(1), o_d=>ch_PE_1_1_to_PE_2_1_a_1);

--ch_PE_1_1_to_PE_2_1_a <= put_ch_data_1(0);
put_ch_full_1(0) <= ch_PE_1_1_to_PE_2_1_full;
ch_PE_1_1_to_PE_2_1_write <= put_ch_write_1(0);
--ch_PE_1_1_to_PE_2_1_a_1 <= put_ch_data_1(1);
put_ch_full_1(1) <= ch_PE_1_1_to_PE_2_1_full_1;
ch_PE_1_1_to_PE_2_1_write_1 <= put_ch_write_1(1);
ch_PE_1_1_to_PE_2_1_read <= get_ch_read_2(0);
get_ch_data_2(0) <= ch_PE_1_1_to_PE_2_1_b;
get_ch_empty_2(0) <= ch_PE_1_1_to_PE_2_1_empty;
ch_PE_1_1_to_PE_2_1_read_1 <= get_ch_read_2(1);
get_ch_data_2(1) <= ch_PE_1_1_to_PE_2_1_b_1;
get_ch_empty_2(1) <= ch_PE_1_1_to_PE_2_1_empty_1;

---- for test
--ch_PE_1_1_to_PE_2_1_read <= i_pop_ch_read(0);
--o_pop_ch_data(0) <= ch_PE_1_1_to_PE_2_1_b;
--o_pop_ch_empty(0) <= ch_PE_1_1_to_PE_2_1_empty;
--o_pop_ch_full(0) <= ch_PE_1_1_to_PE_2_1_full;
--ch_PE_1_1_to_PE_2_1_read_1 <= i_pop_ch_read(1);
--o_pop_ch_data(1) <= ch_PE_1_1_to_PE_2_1_b_1;
--o_pop_ch_empty(1) <= ch_PE_1_1_to_PE_2_1_empty_1;
--o_pop_ch_full(1) <= ch_PE_1_1_to_PE_2_1_full_1;

u_fifo_in_data_reg_Pa2: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_2(0), o_d=>ch_PE_2_1_to_PE_3_1_a);
u_fifo_in_data_reg_Pa3: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_2(1), o_d=>ch_PE_2_1_to_PE_3_1_a_1);

--ch_PE_2_1_to_PE_3_1_a <= put_ch_data_2(0);
put_ch_full_2(0) <=ch_PE_2_1_to_PE_3_1_full;
ch_PE_2_1_to_PE_3_1_write <= put_ch_write_2(0);
--ch_PE_2_1_to_PE_3_1_a_1 <= put_ch_data_2(1);
put_ch_full_2(1) <= ch_PE_2_1_to_PE_3_1_full_1;
ch_PE_2_1_to_PE_3_1_write_1 <= put_ch_write_2(1);
ch_PE_2_1_to_PE_3_1_read <= get_ch_read_3(0);
get_ch_data_3(0) <= ch_PE_2_1_to_PE_3_1_b;
get_ch_empty_3(0) <= ch_PE_2_1_to_PE_3_1_empty;
ch_PE_2_1_to_PE_3_1_read_1 <= get_ch_read_3(1);
get_ch_data_3(1) <= ch_PE_2_1_to_PE_3_1_b_1;
get_ch_empty_3(1) <= ch_PE_2_1_to_PE_3_1_empty_1;

---- for test
--ch_PE_2_1_to_PE_3_1_read <= i_pop_ch_read(0);
--o_pop_ch_data(0) <= ch_PE_2_1_to_PE_3_1_b;
--o_pop_ch_empty(0) <= ch_PE_2_1_to_PE_3_1_empty;
--o_pop_ch_full(0) <= ch_PE_2_1_to_PE_3_1_full;
--ch_PE_2_1_to_PE_3_1_read_1 <= i_pop_ch_read(1);
--o_pop_ch_data(1) <= ch_PE_2_1_to_PE_3_1_b_1;
--o_pop_ch_empty(1) <= ch_PE_2_1_to_PE_3_1_empty_1;
--o_pop_ch_full(1) <= ch_PE_2_1_to_PE_3_1_full_1;

u_fifo_in_data_reg_Pa4: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_3(0), o_d=>ch_PE_3_1_to_PE_4_1_a);
u_fifo_in_data_reg_Pa5: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_3(1), o_d=>ch_PE_3_1_to_PE_4_1_a_1);

--ch_PE_3_1_to_PE_4_1_a <= put_ch_data_3(0);
put_ch_full_3(0) <= ch_PE_3_1_to_PE_4_1_full;
ch_PE_3_1_to_PE_4_1_write <= put_ch_write_3(0);
--ch_PE_3_1_to_PE_4_1_a_1 <= put_ch_data_3(1);
put_ch_full_3(1) <= ch_PE_3_1_to_PE_4_1_full_1;
ch_PE_3_1_to_PE_4_1_write_1 <= put_ch_write_3(1);
ch_PE_3_1_to_PE_4_1_read <= get_ch_read_4(0);
get_ch_data_4(0) <= ch_PE_3_1_to_PE_4_1_b;
get_ch_empty_4(0) <= ch_PE_3_1_to_PE_4_1_empty;
ch_PE_3_1_to_PE_4_1_read_1 <= get_ch_read_4(1);
get_ch_data_4(1) <= ch_PE_3_1_to_PE_4_1_b_1;
get_ch_empty_4(1) <= ch_PE_3_1_to_PE_4_1_empty_1;

u_fifo_in_data_reg_Pa6: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_4(0), o_d=>ch_PE_4_1_to_PE_5_1_a);
u_fifo_in_data_reg_Pa7: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_4(1), o_d=>ch_PE_4_1_to_PE_5_1_a_1);

--ch_PE_4_1_to_PE_5_1_a <= put_ch_data_4(0);
put_ch_full_4(0) <= ch_PE_4_1_to_PE_5_1_full;
ch_PE_4_1_to_PE_5_1_write <= put_ch_write_4(0);
--ch_PE_4_1_to_PE_5_1_a_1 <= put_ch_data_4(1);
put_ch_full_4(1) <= ch_PE_4_1_to_PE_5_1_full_1;
ch_PE_4_1_to_PE_5_1_write_1 <= put_ch_write_4(1);
ch_PE_4_1_to_PE_5_1_read <= get_ch_read_5(0);
get_ch_data_5(0) <= ch_PE_4_1_to_PE_5_1_b;
get_ch_empty_5(0) <= ch_PE_4_1_to_PE_5_1_empty;
ch_PE_4_1_to_PE_5_1_read_1 <= get_ch_read_5(1);
get_ch_data_5(1) <= ch_PE_4_1_to_PE_5_1_b_1;
get_ch_empty_5(1) <= ch_PE_4_1_to_PE_5_1_empty_1;

u_fifo_in_data_reg_Pa8: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_5(0), o_d=>ch_PE_5_1_to_PE_6_1_a);
u_fifo_in_data_reg_Pa9: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_5(1), o_d=>ch_PE_5_1_to_PE_6_1_a_1);

--ch_PE_5_1_to_PE_6_1_a <= put_ch_data_5(0);
put_ch_full_5(0) <= ch_PE_5_1_to_PE_6_1_full;
ch_PE_5_1_to_PE_6_1_write <= put_ch_write_5(0);
--ch_PE_5_1_to_PE_6_1_a_1 <= put_ch_data_5(1);
put_ch_full_5(1) <= ch_PE_5_1_to_PE_6_1_full_1;
ch_PE_5_1_to_PE_6_1_write_1 <= put_ch_write_5(1);
ch_PE_5_1_to_PE_6_1_read <= get_ch_read_6(0);
get_ch_data_6(0) <= ch_PE_5_1_to_PE_6_1_b;
get_ch_empty_6(0) <= ch_PE_5_1_to_PE_6_1_empty;
ch_PE_5_1_to_PE_6_1_read_1 <= get_ch_read_6(1);
get_ch_data_6(1) <= ch_PE_5_1_to_PE_6_1_b_1;
get_ch_empty_6(1) <= ch_PE_5_1_to_PE_6_1_empty_1;

u_fifo_in_data_reg_Pa10: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_6(0), o_d=>ch_PE_6_1_to_PE_7_1_a);
u_fifo_in_data_reg_Pa11: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_6(1), o_d=>ch_PE_6_1_to_PE_7_1_a_1);

--ch_PE_6_1_to_PE_7_1_a <= put_ch_data_6(0);
put_ch_full_6(0) <= ch_PE_6_1_to_PE_7_1_full;
ch_PE_6_1_to_PE_7_1_write <= put_ch_write_6(0);
--ch_PE_6_1_to_PE_7_1_a_1 <= put_ch_data_6(1);
put_ch_full_6(1) <= ch_PE_6_1_to_PE_7_1_full_1;
ch_PE_6_1_to_PE_7_1_write_1 <= put_ch_write_6(1);
ch_PE_6_1_to_PE_7_1_read <= get_ch_read_7(0);
get_ch_data_7(0) <= ch_PE_6_1_to_PE_7_1_b;
get_ch_empty_7(0) <= ch_PE_6_1_to_PE_7_1_empty;
ch_PE_6_1_to_PE_7_1_read_1 <= get_ch_read_7(1);
get_ch_data_7(1) <= ch_PE_6_1_to_PE_7_1_b_1;
get_ch_empty_7(1) <= ch_PE_6_1_to_PE_7_1_empty_1;

u_fifo_in_data_reg_Pa12: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_7(0), o_d=>ch_PE_7_1_to_PE_8_1_a);
u_fifo_in_data_reg_Pa13: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_7(1), o_d=>ch_PE_7_1_to_PE_8_1_a_1);

--ch_PE_7_1_to_PE_8_1_a <= put_ch_data_7(0);
put_ch_full_7(0) <= ch_PE_7_1_to_PE_8_1_full;
ch_PE_7_1_to_PE_8_1_write <= put_ch_write_7(0);
--ch_PE_7_1_to_PE_8_1_a_1 <= put_ch_data_7(1);
put_ch_full_7(1) <= ch_PE_7_1_to_PE_8_1_full_1;
ch_PE_7_1_to_PE_8_1_write_1 <= put_ch_write_7(1);
ch_PE_7_1_to_PE_8_1_read <= get_ch_read_8(0);
get_ch_data_8(0) <= ch_PE_7_1_to_PE_8_1_b;
get_ch_empty_8(0) <= ch_PE_7_1_to_PE_8_1_empty;
ch_PE_7_1_to_PE_8_1_read_1 <= get_ch_read_8(1);
get_ch_data_8(1) <= ch_PE_7_1_to_PE_8_1_b_1;
get_ch_empty_8(1) <= ch_PE_7_1_to_PE_8_1_empty_1;

u_fifo_in_data_reg_Pa14: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_8(0), o_d=>ch_PE_8_1_to_PE_9_1_a);
u_fifo_in_data_reg_Pa15: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_8(1), o_d=>ch_PE_8_1_to_PE_9_1_a_1);

--ch_PE_8_1_to_PE_9_1_a <= put_ch_data_8(0);
put_ch_full_8(0) <= ch_PE_8_1_to_PE_9_1_full;
ch_PE_8_1_to_PE_9_1_write <= put_ch_write_8(0);
--ch_PE_8_1_to_PE_9_1_a_1 <= put_ch_data_8(1);
put_ch_full_8(1) <= ch_PE_8_1_to_PE_9_1_full_1;
ch_PE_8_1_to_PE_9_1_write_1 <= put_ch_write_8(1);
ch_PE_8_1_to_PE_9_1_read <= get_ch_read_9(0);
get_ch_data_9(0) <= ch_PE_8_1_to_PE_9_1_b;
get_ch_empty_9(0) <= ch_PE_8_1_to_PE_9_1_empty;
ch_PE_8_1_to_PE_9_1_read_1 <= get_ch_read_9(1);
get_ch_data_9(1) <= ch_PE_8_1_to_PE_9_1_b_1;
get_ch_empty_9(1) <= ch_PE_8_1_to_PE_9_1_empty_1;

u_fifo_in_data_reg_Pa16: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_9(0), o_d=>ch_PE_9_1_to_PE_10_1_a);
u_fifo_in_data_reg_Pa17: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_9(1), o_d=>ch_PE_9_1_to_PE_10_1_a_1);

--ch_PE_9_1_to_PE_10_1_a <= put_ch_data_9(0);
put_ch_full_9(0) <= ch_PE_9_1_to_PE_10_1_full;
ch_PE_9_1_to_PE_10_1_write <= put_ch_write_9(0);
--ch_PE_9_1_to_PE_10_1_a_1 <= put_ch_data_9(1);
put_ch_full_9(1) <= ch_PE_9_1_to_PE_10_1_full_1;
ch_PE_9_1_to_PE_10_1_write_1 <= put_ch_write_9(1);
ch_PE_9_1_to_PE_10_1_read <= get_ch_read_10(0);
get_ch_data_10(0) <= ch_PE_9_1_to_PE_10_1_b;
get_ch_empty_10(0) <= ch_PE_9_1_to_PE_10_1_empty;
ch_PE_9_1_to_PE_10_1_read_1 <= get_ch_read_10(1);
get_ch_data_10(1) <= ch_PE_9_1_to_PE_10_1_b_1;
get_ch_empty_10(1) <= ch_PE_9_1_to_PE_10_1_empty_1;

u_fifo_in_data_reg_Pa18: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_10(0), o_d=>ch_PE_10_1_to_PE_11_1_a);
u_fifo_in_data_reg_Pa19: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_10(1), o_d=>ch_PE_10_1_to_PE_11_1_a_1);

--ch_PE_10_1_to_PE_11_1_a <= put_ch_data_10(0);
put_ch_full_10(0) <= ch_PE_10_1_to_PE_11_1_full;
ch_PE_10_1_to_PE_11_1_write <= put_ch_write_10(0);
--ch_PE_10_1_to_PE_11_1_a_1 <= put_ch_data_10(1);
put_ch_full_10(1) <= ch_PE_10_1_to_PE_11_1_full_1;
ch_PE_10_1_to_PE_11_1_write_1 <= put_ch_write_10(1);
ch_PE_10_1_to_PE_11_1_read <= get_ch_read_11(0);
get_ch_data_11(0) <= ch_PE_10_1_to_PE_11_1_b;
get_ch_empty_11(0) <= ch_PE_10_1_to_PE_11_1_empty;
ch_PE_10_1_to_PE_11_1_read_1 <= get_ch_read_11(1);
get_ch_data_11(1) <= ch_PE_10_1_to_PE_11_1_b_1;
get_ch_empty_11(1) <= ch_PE_10_1_to_PE_11_1_empty_1;

u_fifo_in_data_reg_Pa20: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
port map(clk=>clk, rst=>rst, i_d=>put_ch_data_11(0), o_d=>ch_PE_11_1_to_SINK_a);
--u_fifo_in_data_reg_Pa21: spu_generic_reg generic map(REG_NUM=>0, REG_WIDTH=>CORE_WIDTH)
--port map(clk=>clk, rst=>rst, i_d=>put_ch_data_11(1), o_d=>ch_PE_11_1_to_SINK_a_1);

--ch_PE_11_1_to_SINK_a <= put_ch_data_11(0);
put_ch_full_11(0) <= ch_PE_11_1_to_SINK_full;
ch_PE_11_1_to_SINK_write <= put_ch_write_11(0);
--ch_PE_11_1_to_SINK_a <= put_ch_data_11(0);
--put_ch_full_11(1) <= ch_PE_11_1_to_SINK_full_1;
--ch_PE_11_1_to_SINK_write_1 <= put_ch_write_11(1);
ch_PE_11_1_to_SINK_read <= i_pop_ch_read(0);
o_pop_ch_data(0) <= ch_PE_11_1_to_SINK_b;
o_pop_ch_empty(0) <= ch_PE_11_1_to_SINK_empty;
o_pop_ch_full(0) <= ch_PE_11_1_to_SINK_full;
		
FIFO_1_in_end <= ch_SOURCE_to_PE_1_1_full and ch_SOURCE_to_PE_1_1_full_1
                 and not ch_PE_1_1_to_PE_2_1_full and not ch_PE_1_1_to_PE_2_1_full_1;

o_data_last(0) <= FIFO_12_in_end;

u_fifo_SOURCE_to_PE_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_SOURCE_to_PE_1_1_a,
o_data  => ch_SOURCE_to_PE_1_1_b,
i_write  => ch_SOURCE_to_PE_1_1_write,
i_read  => ch_SOURCE_to_PE_1_1_read,
o_full  => ch_SOURCE_to_PE_1_1_full,
o_almostfull => open,
o_empty  => ch_SOURCE_to_PE_1_1_empty,
i_data_end_s   =>	FIFO_1_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_2_in_end, -- end of input data signal 
o_pc_en      =>	PE_1_1_en_1 -- output enable signal
);

u_fifo_SOURCE_to_PE_1_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_SOURCE_to_PE_1_1_a_1,
o_data  => ch_SOURCE_to_PE_1_1_b_1,
i_write  => ch_SOURCE_to_PE_1_1_write_1,
i_read  => ch_SOURCE_to_PE_1_1_read_1,
o_full  => ch_SOURCE_to_PE_1_1_full_1,
o_almostfull => open,
o_empty  => ch_SOURCE_to_PE_1_1_empty_1,
i_data_end_s   =>	FIFO_1_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_2_in_end, -- end of input data signal 
o_pc_en      =>	PE_1_1_en_2 -- output enable signal
);

PE_1_1_en <= PE_1_1_en_1 and PE_1_1_en_2;

u_core_0: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => 16384,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU0PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU0PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU0PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0,
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => false, 
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => false,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU0PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_1_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_1_1_end,
-- input ports
i_get_ch_data  => get_ch_data_1,
i_get_ch_empty => get_ch_empty_1,
o_get_ch_read => get_ch_read_1,
-- output ports
o_put_ch_data  => put_ch_data_1,
i_put_ch_full => put_ch_full_1,
o_put_ch_write => put_ch_write_1,
-- debug output ports
o_dput_ch_data  => dput_ch_data_1,
i_dput_ch_full => dput_ch_full_1,
o_dput_ch_write => dput_ch_write_1
);

FIFO_2_in_end <= (ch_PE_1_1_to_PE_2_1_full and ch_PE_1_1_to_PE_2_1_full_1
            and not ch_PE_2_1_to_PE_3_1_full and not ch_PE_2_1_to_PE_3_1_full_1);
--            or PE_1_1_end;

u_fifo_PE_1_1_to_PE_2_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_1_1_to_PE_2_1_a,
o_data  => ch_PE_1_1_to_PE_2_1_b,
i_write  => ch_PE_1_1_to_PE_2_1_write,
i_read  => ch_PE_1_1_to_PE_2_1_read,
o_full  => ch_PE_1_1_to_PE_2_1_full,
o_almostfull => open,
o_empty  => ch_PE_1_1_to_PE_2_1_empty,
i_data_end_s   =>	FIFO_2_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_3_in_end, -- end of input data signal 
o_pc_en      =>	PE_2_1_en_1 -- output enable signal
);
 
u_fifo_PE_1_1_to_PE_2_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_1_1_to_PE_2_1_a_1,
o_data  => ch_PE_1_1_to_PE_2_1_b_1,
i_write  => ch_PE_1_1_to_PE_2_1_write_1,
i_read  => ch_PE_1_1_to_PE_2_1_read_1,
o_full  => ch_PE_1_1_to_PE_2_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_1_1_to_PE_2_1_empty_1,
i_data_end_s   =>	FIFO_2_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_3_in_end, -- end of input data signal 
o_pc_en      =>	PE_2_1_en_2 -- output enable signal
);

PE_2_1_en <= PE_2_1_en_1 and PE_2_1_en_2;

u_core_1: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU1PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU1PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU1PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0,
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true, 
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU1PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_2_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_2_1_end,
-- input ports
i_get_ch_data  => get_ch_data_2,
i_get_ch_empty => get_ch_empty_2,
o_get_ch_read => get_ch_read_2,
-- output ports
o_put_ch_data  => put_ch_data_2,
i_put_ch_full => put_ch_full_2,
o_put_ch_write => put_ch_write_2,
-- debug output ports
o_dput_ch_data  => dput_ch_data_2,
i_dput_ch_full => dput_ch_full_2,
o_dput_ch_write => dput_ch_write_2
);

FIFO_3_in_end <= (ch_PE_2_1_to_PE_3_1_full and ch_PE_2_1_to_PE_3_1_full_1
            and not ch_PE_3_1_to_PE_4_1_full and not ch_PE_3_1_to_PE_4_1_full_1);
--            or PE_2_1_end;

u_fifo_PE_2_1_to_PE_3_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_2_1_to_PE_3_1_a,
o_data  => ch_PE_2_1_to_PE_3_1_b,
i_write  => ch_PE_2_1_to_PE_3_1_write,
i_read  => ch_PE_2_1_to_PE_3_1_read,
o_full  => ch_PE_2_1_to_PE_3_1_full,
o_almostfull => open,
o_empty  => ch_PE_2_1_to_PE_3_1_empty,
i_data_end_s   =>	FIFO_3_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_4_in_end, -- end of input data signal 
o_pc_en      =>	PE_3_1_en_1 -- output enable signal
);
 
u_fifo_PE_2_1_to_PE_3_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_2_1_to_PE_3_1_a_1,
o_data  => ch_PE_2_1_to_PE_3_1_b_1,
i_write  => ch_PE_2_1_to_PE_3_1_write_1,
i_read  => ch_PE_2_1_to_PE_3_1_read_1,
o_full  => ch_PE_2_1_to_PE_3_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_2_1_to_PE_3_1_empty_1,
i_data_end_s   =>	FIFO_3_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_4_in_end, -- end of input data signal 
o_pc_en      =>	PE_3_1_en_2 -- output enable signal
);

PE_3_1_en <= PE_3_1_en_1 and PE_3_1_en_2;

u_core_2: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU2PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU2PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU2PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0,
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,  
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false, 
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU2PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_3_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_3_1_end,
-- input ports
i_get_ch_data  => get_ch_data_3,
i_get_ch_empty => get_ch_empty_3,
o_get_ch_read => get_ch_read_3,
-- output ports
o_put_ch_data  => put_ch_data_3,
i_put_ch_full => put_ch_full_3,
o_put_ch_write => put_ch_write_3,
-- debug output ports
o_dput_ch_data  => dput_ch_data_3,
i_dput_ch_full => dput_ch_full_3,
o_dput_ch_write => dput_ch_write_3
);

FIFO_4_in_end <= (ch_PE_3_1_to_PE_4_1_full and ch_PE_3_1_to_PE_4_1_full_1
            and not ch_PE_4_1_to_PE_5_1_full and not ch_PE_4_1_to_PE_5_1_full_1);
--            or PE_3_1_end;

u_fifo_PE_3_1_to_PE_4_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_3_1_to_PE_4_1_a,
o_data  => ch_PE_3_1_to_PE_4_1_b,
i_write  => ch_PE_3_1_to_PE_4_1_write,
i_read  => ch_PE_3_1_to_PE_4_1_read,
o_full  => ch_PE_3_1_to_PE_4_1_full,
o_almostfull => open,
o_empty  => ch_PE_3_1_to_PE_4_1_empty,
i_data_end_s   =>	FIFO_4_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_5_in_end, -- end of input data signal 
o_pc_en      =>	PE_4_1_en_1 -- output enable signal
);
 
u_fifo_PE_3_1_to_PE_4_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_3_1_to_PE_4_1_a_1,
o_data  => ch_PE_3_1_to_PE_4_1_b_1,
i_write  => ch_PE_3_1_to_PE_4_1_write_1,
i_read  => ch_PE_3_1_to_PE_4_1_read_1,
o_full  => ch_PE_3_1_to_PE_4_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_3_1_to_PE_4_1_empty_1,
i_data_end_s   =>	FIFO_4_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_5_in_end, -- end of input data signal 
o_pc_en      =>	PE_4_1_en_2 -- output enable signal
);

PE_4_1_en <= PE_4_1_en_1 and PE_4_1_en_2;

u_core_3: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU3PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true, 
PM_INIT_FILE => "PMInit/pm_initSPU3PE0.mif",
DM_EN => false,
DM_SIZE => 128,
DM_ADDR_WIDTH => 7,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => false,
DM_INIT_FILE => "DMInit/dm_initSPU3PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0,
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU3PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_4_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_4_1_end,
-- input ports
i_get_ch_data  => get_ch_data_4,
i_get_ch_empty => get_ch_empty_4,
o_get_ch_read => get_ch_read_4,
-- output ports
o_put_ch_data  => put_ch_data_4,
i_put_ch_full => put_ch_full_4,
o_put_ch_write => put_ch_write_4,
-- debug output ports
o_dput_ch_data  => dput_ch_data_4,
i_dput_ch_full => dput_ch_full_4,
o_dput_ch_write => dput_ch_write_4
);

FIFO_5_in_end <= (ch_PE_4_1_to_PE_5_1_full and ch_PE_4_1_to_PE_5_1_full_1 
            and not ch_PE_5_1_to_PE_6_1_full and not ch_PE_5_1_to_PE_6_1_full_1);
--            or PE_4_1_end;

u_fifo_PE_4_1_to_PE_5_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_4_1_to_PE_5_1_a,
o_data  => ch_PE_4_1_to_PE_5_1_b,
i_write  => ch_PE_4_1_to_PE_5_1_write,
i_read  => ch_PE_4_1_to_PE_5_1_read,
o_full  => ch_PE_4_1_to_PE_5_1_full,
o_almostfull => open,
o_empty  => ch_PE_4_1_to_PE_5_1_empty,
i_data_end_s   =>	FIFO_5_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_6_in_end, -- end of input data signal 
o_pc_en      =>	PE_5_1_en_1 -- output enable signal
);
 
u_fifo_PE_4_1_to_PE_5_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_4_1_to_PE_5_1_a_1,
o_data  => ch_PE_4_1_to_PE_5_1_b_1,
i_write  => ch_PE_4_1_to_PE_5_1_write_1,
i_read  => ch_PE_4_1_to_PE_5_1_read_1,
o_full  => ch_PE_4_1_to_PE_5_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_4_1_to_PE_5_1_empty_1,
i_data_end_s   =>	FIFO_5_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_6_in_end, -- end of input data signal 
o_pc_en      =>	PE_5_1_en_2 -- output enable signal
);

PE_5_1_en <= PE_5_1_en_1 and PE_5_1_en_2;

u_core_4: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU4PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU4PE0.mif",
DM_EN => false,
DM_SIZE => 512,
DM_ADDR_WIDTH => 9,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU4PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU4PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_5_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_5_1_end,
-- input ports
i_get_ch_data  => get_ch_data_5,
i_get_ch_empty => get_ch_empty_5,
o_get_ch_read => get_ch_read_5,
-- output ports
o_put_ch_data  => put_ch_data_5,
i_put_ch_full => put_ch_full_5,
o_put_ch_write => put_ch_write_5,
-- debug output ports
o_dput_ch_data  => dput_ch_data_5,
i_dput_ch_full => dput_ch_full_5,
o_dput_ch_write => dput_ch_write_5
);

FIFO_6_in_end <= (ch_PE_5_1_to_PE_6_1_full and ch_PE_5_1_to_PE_6_1_full_1 
            and not ch_PE_6_1_to_PE_7_1_full and not ch_PE_6_1_to_PE_7_1_full_1);
--            or PE_5_1_end;

u_fifo_PE_5_1_to_PE_6_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_5_1_to_PE_6_1_a,
o_data  => ch_PE_5_1_to_PE_6_1_b,
i_write  => ch_PE_5_1_to_PE_6_1_write,
i_read  => ch_PE_5_1_to_PE_6_1_read,
o_full  => ch_PE_5_1_to_PE_6_1_full,
o_almostfull => open,
o_empty  => ch_PE_5_1_to_PE_6_1_empty,
i_data_end_s   =>	FIFO_6_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_7_in_end, -- end of input data signal 
o_pc_en      =>	PE_6_1_en_1 -- output enable signal
);
 
u_fifo_PE_5_1_to_PE_6_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_5_1_to_PE_6_1_a_1,
o_data  => ch_PE_5_1_to_PE_6_1_b_1,
i_write  => ch_PE_5_1_to_PE_6_1_write_1,
i_read  => ch_PE_5_1_to_PE_6_1_read_1,
o_full  => ch_PE_5_1_to_PE_6_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_5_1_to_PE_6_1_empty_1,
i_data_end_s   =>	FIFO_6_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_7_in_end, -- end of input data signal 
o_pc_en      =>	PE_6_1_en_2 -- output enable signal
);

PE_6_1_en <= PE_6_1_en_1 and PE_6_1_en_2;

u_core_5: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU5PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU5PE0.mif",
DM_EN => false,
DM_SIZE => 2048,
DM_ADDR_WIDTH => 11,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU5PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0,
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1, 
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1, 
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => true,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => true,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => true,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 32,
SM_ADDR_WIDTH => 5,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU5PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_6_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_6_1_end,
-- input ports
i_get_ch_data  => get_ch_data_6,
i_get_ch_empty => get_ch_empty_6,
o_get_ch_read => get_ch_read_6,
-- output ports
o_put_ch_data  => put_ch_data_6,
i_put_ch_full => put_ch_full_6,
o_put_ch_write => put_ch_write_6,
-- debug output ports
o_dput_ch_data  => dput_ch_data_6,
i_dput_ch_full => dput_ch_full_6,
o_dput_ch_write => dput_ch_write_6
);

FIFO_7_in_end <= (ch_PE_6_1_to_PE_7_1_full and ch_PE_6_1_to_PE_7_1_full_1 
            and not ch_PE_7_1_to_PE_8_1_full and not ch_PE_7_1_to_PE_8_1_full_1);
--            or PE_6_1_end;

u_fifo_PE_6_1_to_PE_7_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_6_1_to_PE_7_1_a,
o_data  => ch_PE_6_1_to_PE_7_1_b,
i_write  => ch_PE_6_1_to_PE_7_1_write,
i_read  => ch_PE_6_1_to_PE_7_1_read,
o_full  => ch_PE_6_1_to_PE_7_1_full,
o_almostfull => open,
o_empty  => ch_PE_6_1_to_PE_7_1_empty,
i_data_end_s   =>	FIFO_7_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_8_in_end, -- end of input data signal 
o_pc_en      =>	PE_7_1_en_1 -- output enable signal
);
 
u_fifo_PE_6_1_to_PE_7_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_6_1_to_PE_7_1_a_1,
o_data  => ch_PE_6_1_to_PE_7_1_b_1,
i_write  => ch_PE_6_1_to_PE_7_1_write_1,
i_read  => ch_PE_6_1_to_PE_7_1_read_1,
o_full  => ch_PE_6_1_to_PE_7_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_6_1_to_PE_7_1_empty_1,
i_data_end_s   =>	FIFO_7_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_8_in_end, -- end of input data signal 
o_pc_en      =>	PE_7_1_en_2 -- output enable signal
);

PE_7_1_en <= PE_7_1_en_1 and PE_7_1_en_2;

u_core_6: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU6PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU6PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU6PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 64,
SM_ADDR_WIDTH => 6,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU6PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_7_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_7_1_end,
-- input ports
i_get_ch_data  => get_ch_data_7,
i_get_ch_empty => get_ch_empty_7,
o_get_ch_read => get_ch_read_7,
-- output ports
o_put_ch_data  => put_ch_data_7,
i_put_ch_full => put_ch_full_7,
o_put_ch_write => put_ch_write_7,
-- debug output ports
o_dput_ch_data  => dput_ch_data_7,
i_dput_ch_full => dput_ch_full_7,
o_dput_ch_write => dput_ch_write_7
);

FIFO_8_in_end <= (ch_PE_7_1_to_PE_8_1_full and ch_PE_7_1_to_PE_8_1_full_1 
            and not ch_PE_8_1_to_PE_9_1_full and not ch_PE_8_1_to_PE_9_1_full_1);
--            or PE_7_1_end;

u_fifo_PE_7_1_to_PE_8_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_7_1_to_PE_8_1_a,
o_data  => ch_PE_7_1_to_PE_8_1_b,
i_write  => ch_PE_7_1_to_PE_8_1_write,
i_read  => ch_PE_7_1_to_PE_8_1_read,
o_full  => ch_PE_7_1_to_PE_8_1_full,
o_almostfull => open,
o_empty  => ch_PE_7_1_to_PE_8_1_empty,
i_data_end_s   =>	FIFO_8_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_9_in_end, -- end of input data signal 
o_pc_en      =>	PE_8_1_en_1 -- output enable signal
);
 
u_fifo_PE_7_1_to_PE_8_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_7_1_to_PE_8_1_a_1,
o_data  => ch_PE_7_1_to_PE_8_1_b_1,
i_write  => ch_PE_7_1_to_PE_8_1_write_1,
i_read  => ch_PE_7_1_to_PE_8_1_read_1,
o_full  => ch_PE_7_1_to_PE_8_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_7_1_to_PE_8_1_empty_1,
i_data_end_s   =>	FIFO_8_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_9_in_end, -- end of input data signal 
o_pc_en      =>	PE_8_1_en_2 -- output enable signal
);

PE_8_1_en <= PE_8_1_en_1 and PE_8_1_en_2;

u_core_7: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU7PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU7PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU7PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 128,
SM_ADDR_WIDTH => 7,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU7PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_8_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_8_1_end,
-- input ports
i_get_ch_data  => get_ch_data_8,
i_get_ch_empty => get_ch_empty_8,
o_get_ch_read => get_ch_read_8,
-- output ports
o_put_ch_data  => put_ch_data_8,
i_put_ch_full => put_ch_full_8,
o_put_ch_write => put_ch_write_8,
-- debug output ports
o_dput_ch_data  => dput_ch_data_8,
i_dput_ch_full => dput_ch_full_8,
o_dput_ch_write => dput_ch_write_8
);

FIFO_9_in_end <= (ch_PE_8_1_to_PE_9_1_full and ch_PE_8_1_to_PE_9_1_full_1 
            and not ch_PE_9_1_to_PE_10_1_full and not ch_PE_9_1_to_PE_10_1_full_1);
--            or PE_8_1_end;

u_fifo_PE_8_1_to_PE_9_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_8_1_to_PE_9_1_a,
o_data  => ch_PE_8_1_to_PE_9_1_b,
i_write  => ch_PE_8_1_to_PE_9_1_write,
i_read  => ch_PE_8_1_to_PE_9_1_read,
o_full  => ch_PE_8_1_to_PE_9_1_full,
o_almostfull => open,
o_empty  => ch_PE_8_1_to_PE_9_1_empty,
i_data_end_s   =>	FIFO_9_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_10_in_end, -- end of input data signal 
o_pc_en      =>	PE_9_1_en_1 -- output enable signal
);
 
u_fifo_PE_8_1_to_PE_9_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_8_1_to_PE_9_1_a_1,
o_data  => ch_PE_8_1_to_PE_9_1_b_1,
i_write  => ch_PE_8_1_to_PE_9_1_write_1,
i_read  => ch_PE_8_1_to_PE_9_1_read_1,
o_full  => ch_PE_8_1_to_PE_9_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_8_1_to_PE_9_1_empty_1,
i_data_end_s   =>	FIFO_9_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_10_in_end, -- end of input data signal 
o_pc_en      =>	PE_9_1_en_2 -- output enable signal
);

PE_9_1_en <= PE_9_1_en_1 and PE_9_1_en_2;

u_core_8: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU8PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU8PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU8PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 256,
SM_ADDR_WIDTH => 8,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU8PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_9_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_9_1_end,
-- input ports
i_get_ch_data  => get_ch_data_9,
i_get_ch_empty => get_ch_empty_9,
o_get_ch_read => get_ch_read_9,
-- output ports
o_put_ch_data  => put_ch_data_9,
i_put_ch_full => put_ch_full_9,
o_put_ch_write => put_ch_write_9,
-- debug output ports
o_dput_ch_data  => dput_ch_data_9,
i_dput_ch_full => dput_ch_full_9,
o_dput_ch_write => dput_ch_write_9
);

FIFO_10_in_end <= (ch_PE_9_1_to_PE_10_1_full and ch_PE_9_1_to_PE_10_1_full_1 
            and not ch_PE_10_1_to_PE_11_1_full and not ch_PE_10_1_to_PE_11_1_full_1);
--            or PE_9_1_end;

u_fifo_PE_9_1_to_PE_10_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_9_1_to_PE_10_1_a,
o_data  => ch_PE_9_1_to_PE_10_1_b,
i_write  => ch_PE_9_1_to_PE_10_1_write,
i_read  => ch_PE_9_1_to_PE_10_1_read,
o_full  => ch_PE_9_1_to_PE_10_1_full,
o_almostfull => open,
o_empty  => ch_PE_9_1_to_PE_10_1_empty,
i_data_end_s   =>	FIFO_10_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_11_in_end, -- end of input data signal 
o_pc_en      =>	PE_10_1_en_1 -- output enable signal
);
 
u_fifo_PE_9_1_to_PE_10_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_9_1_to_PE_10_1_a_1,
o_data  => ch_PE_9_1_to_PE_10_1_b_1,
i_write  => ch_PE_9_1_to_PE_10_1_write_1,
i_read  => ch_PE_9_1_to_PE_10_1_read_1,
o_full  => ch_PE_9_1_to_PE_10_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_9_1_to_PE_10_1_empty_1,
i_data_end_s   =>	FIFO_10_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_11_in_end, -- end of input data signal 
o_pc_en      =>	PE_10_1_en_2 -- output enable signal
);

PE_10_1_en <= PE_10_1_en_1 and PE_10_1_en_2;

u_core_9: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 2,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU9PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU9PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU9PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 512,
SM_ADDR_WIDTH => 9,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU9PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_10_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_10_1_end,
-- input ports
i_get_ch_data  => get_ch_data_10,
i_get_ch_empty => get_ch_empty_10,
o_get_ch_read => get_ch_read_10,
-- output ports
o_put_ch_data  => put_ch_data_10,
i_put_ch_full => put_ch_full_10,
o_put_ch_write => put_ch_write_10,
-- debug output ports
o_dput_ch_data  => dput_ch_data_10,
i_dput_ch_full => dput_ch_full_10,
o_dput_ch_write => dput_ch_write_10
);

FIFO_11_in_end <= (ch_PE_10_1_to_PE_11_1_full and ch_PE_10_1_to_PE_11_1_full_1 
                 and not ch_PE_11_1_to_SINK_full);
--                 or PE_10_1_end;

u_fifo_PE_10_1_to_PE_11_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_10_1_to_PE_11_1_a,
o_data  => ch_PE_10_1_to_PE_11_1_b,
i_write  => ch_PE_10_1_to_PE_11_1_write,
i_read  => ch_PE_10_1_to_PE_11_1_read,
o_full  => ch_PE_10_1_to_PE_11_1_full,
o_almostfull => open,
o_empty  => ch_PE_10_1_to_PE_11_1_empty,
i_data_end_s   =>	FIFO_11_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_12_in_end, -- end of input data signal 
o_pc_en      =>	PE_11_1_en_1 -- output enable signal
);
 
u_fifo_PE_10_1_to_PE_11_1_1: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => INPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_10_1_to_PE_11_1_a_1,
o_data  => ch_PE_10_1_to_PE_11_1_b_1,
i_write  => ch_PE_10_1_to_PE_11_1_write_1,
i_read  => ch_PE_10_1_to_PE_11_1_read_1,
o_full  => ch_PE_10_1_to_PE_11_1_full_1,
o_almostfull => open,
o_empty  => ch_PE_10_1_to_PE_11_1_empty_1,
i_data_end_s   =>	FIFO_11_in_end, -- end of input data signal 
i_data_end_e   =>	FIFO_12_in_end, -- end of input data signal 
o_pc_en      =>	PE_11_1_en_2 -- output enable signal
);

PE_11_1_en <= PE_11_1_en_1 and PE_11_1_en_2;

u_core_10: spu_core
generic map(
DATA_WIDTH => 16,
DATA_TYPE => 2,
SLICE_NUM => 4,
CORE_DATA_WIDTH => 32,
OPM_NUM => 2,
ALUM_NUM => 3,
FRAC_BITS => 14,
BSLAVE => false,
BMASTER => false,
BMASTER_NUM => 1,
VLEN => 1,
OPCODE_WIDTH => 4,
MULREG_EN => true,
PB0_DEPTH => 1,
PB1_DEPTH => 1,
PB2_DEPTH => 2,
PA0_DEPTH => 1,
PA1_DEPTH => 1,
PA1X_DEPTH => 0,
BRANCH_EN => false,
JMP_EN => true,
RPT_EN => false,
RPT_SPEC_1 => false,
RPT_LEVELS => 0,
RPT_CNT_LEN0 => 1,
RPT_CNT_LEN1 => 1,
RPT_CNT_LEN2 => 1,
RPT_CNT_LEN3 => 1,
RPT_CNT_LEN4 => 1,
RPT_BLK_LEN0 => 1,
RPT_BLK_LEN1 => 1,
RPT_BLK_LEN2 => 1,
RPT_BLK_LEN3 => 1,
RPT_BLK_LEN4 => 1,
MASK_EN => false,
MASKEQ_EN => false,
MASKGT_EN => false,
MASKLT_EN => false,
MASKGE_EN => false,
MASKLE_EN => false,
MASKNE_EN => false,
ALUSRA_EN => true,
ALUSRA_VAL => 1,
ABSDIFF_EN => false,
ABSDIFF_WITHACCUM => false,
DECONST_EN => false,
DEBUG_EN => false,
FLEXA_TYPE => 8,
FLEXB_TYPE => 4,
FLEXC_TYPE => 8,
FLEXB_IMM_VAL => -1,
DIRECT_WB_EN => true,
SHARE_GET_DATA => false,
EBITS_A => 0,
EBITS_B => 0,
EBITS_C => 0,
EBITS_D => 0,
DSP48E_EN => true,
GETI_EN => false,
GETCH_EN => false,
PUTCH_EN => false,
RX_CH_NUM => 2,
RX_CH_WIDTH => 1,
TX_CH_NUM => 1,
TX_CH_WIDTH => 1,
DTX_CH_NUM => 1,
DTX_CH_WIDTH => 1,
RF_EN => false,
RF_ADDR_WIDTH => 5,
RF_INIT_EN => false,
RF_INIT_FILE => "RFInit/rf_initSPU10PE.mif",
PM_SIZE => 3000,
PM_ADDR_WIDTH => 12,
PM_DATA_WIDTH => 32,
USE_BRAM_FOR_LARGE_PM => true,
PM_INIT_FILE => "PMInit/pm_initSPU10PE0.mif",
DM_EN => false,
DM_SIZE => 32,
DM_ADDR_WIDTH => 5,
DM_DATA_WIDTH => 32,
DM_INIT_EN => false,
USE_BRAM_FOR_LARGE_DM => true,
DM_INIT_FILE => "DMInit/dm_initSPU10PE",
DM_RB_M_NUM => 0,
DM_RB_N_NUM => 0,
DM_WB_NUM => 0,
DM_TRUE_2R1W => false,
DM_RB_M_INITIAL0 => 0,
DM_RB_M_INITIAL1 => 0, 
DM_RB_N_INITIAL0 => 0,
DM_RB_N_INITIAL1 => 0,
DM_WB_INITIAL0 => 0,
DM_WB_INITIAL1 => 0,
DM_RB_M_AUTOINC_SIZE0 => 1,
DM_RB_M_AUTOINC_SIZE1 => 1,
DM_RB_N_AUTOINC_SIZE0 => 1,
DM_RB_N_AUTOINC_SIZE1 => 1,
DM_WB_AUTOINC_SIZE0 => 1,
DM_WB_AUTOINC_SIZE1 => 1,
DM_OFFSET_EN => true,
DM_RB_M_SET_EN0 => false,
DM_RB_M_SET_EN1 => false,
DM_RB_N_SET_EN0 => false,
DM_RB_N_SET_EN1 => false,
DM_WB_SET_EN0 => false,
DM_WB_SET_EN1 => false,
DM_RB_M_AUTOINC_EN0 => false,
DM_RB_M_AUTOINC_EN1 => false,
DM_RB_N_AUTOINC_EN0 => false,
DM_RB_N_AUTOINC_EN1 => false,
DM_WB_AUTOINC_EN0 => false,
DM_WB_AUTOINC_EN1 => false,
DM_RB_M_INC_EN0 => false,
DM_RB_M_INC_EN1 => false,
DM_RB_N_INC_EN0 => false,
DM_RB_N_INC_EN1 => false,
DM_WB_INC_EN0 => false,
DM_WB_INC_EN1 => false,
SM_EN => true,
SM_SIZE => 1024,
SM_ADDR_WIDTH => 10,
USE_BRAM_FOR_LARGE_SM => true,
SM_INIT_FILE => "IMMInit/imm_initSPU10PE0.mif",
SM_OFFSET_EN => false,
SM_READONLY => true,
SM_RB_SET_EN0 => false,
SM_WB_SET_EN0 => false,
SM_RB_AUTOINC_SIZE0 => 1,
SM_WB_AUTOINC_SIZE0 => 1,
SM_RB_AUTOINC_EN0 => false,
SM_WB_AUTOINC_EN0 => false,
SM_RB_INC_EN0 => false,
SM_WB_INC_EN0 => false
)
port map(
clk => clk,
rst => rst,
i_ext_en_spu => PE_11_1_en,
o_ext_barrier => open,
i_ext_barrier => open,
o_ext_en_spu => open,
o_put_last => PE_11_1_end,
-- input ports
i_get_ch_data  => get_ch_data_11,
i_get_ch_empty => get_ch_empty_11,
o_get_ch_read => get_ch_read_11,
-- output ports
o_put_ch_data  => put_ch_data_11,
i_put_ch_full => put_ch_full_11,
o_put_ch_write => put_ch_write_11,
-- debug output ports
o_dput_ch_data  => dput_ch_data_11,
i_dput_ch_full => dput_ch_full_11,
o_dput_ch_write => dput_ch_write_11
);

FIFO_12_in_end <= ch_PE_11_1_to_SINK_full;
--                   and ch_PE_11_1_to_SINK_full_1;
--                 or PE_11_1_end;

u_fifo_PE_11_1_to_SINK: ssp_fifo_cache
generic map( WIDTH => CORE_WIDTH, DEPTH => OUTPUT_WORDS, OUT_REG_NUM=> 0, STATE_EN => true)
port map(
clk => clk,
rst => rst,
i_data  => ch_PE_11_1_to_SINK_a,
o_data  => ch_PE_11_1_to_SINK_b,
i_write  => ch_PE_11_1_to_SINK_write,
i_read  => ch_PE_11_1_to_SINK_read,
o_full  => ch_PE_11_1_to_SINK_full,
o_almostfull => open,
o_empty  => ch_PE_11_1_to_SINK_empty,
i_data_end_s   =>	FIFO_12_in_end, -- end of input data signal 
i_data_end_e   =>	tlast_asserted(0), -- end of input data signal 
o_pc_en      =>	open -- output enable signal
);

end Behavioral;
