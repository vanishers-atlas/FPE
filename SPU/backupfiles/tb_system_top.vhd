--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   10:51:32 03/20/2013
-- Design Name:   
-- Module Name:   C:/_Design_/Hardware/_testFunctionality_/20130320iocore_baseR478/tb_system_top.vhd
-- Project Name:  OnePE
-- Target Device:  
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY tb_system_top IS
END tb_system_top;
 
ARCHITECTURE behavior OF tb_system_top IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT ssp_top
    PORT(
         clk : IN  std_logic;
         rst : IN  std_logic;
         o_mif_af_cmd : OUT  std_logic_vector(2 downto 0);
         o_mif_af_addr : OUT  std_logic_vector(30 downto 0);
         o_mif_af_wren : OUT  std_logic;
         i_mif_af_afull : IN  std_logic;
         o_mif_wdf_wren : OUT  std_logic;
         o_mif_wdf_data : OUT  std_logic_vector(127 downto 0);
         o_mif_wdf_mask_data : OUT  std_logic_vector(15 downto 0);
         i_mif_wdf_afull : IN  std_logic;
         i_mif_rd_data : IN  std_logic_vector(127 downto 0);
         i_mif_rd_valid : IN  std_logic
        );
    END COMPONENT;
    

   --Inputs
   signal clk : std_logic := '0';
   signal rst : std_logic := '1';
   signal i_mif_af_afull : std_logic := '0';
   signal i_mif_wdf_afull : std_logic := '0';
   signal i_mif_rd_data : std_logic_vector(127 downto 0) := (others => '0');
   signal i_mif_rd_valid : std_logic := '0';

 	--Outputs
   signal o_mif_af_cmd : std_logic_vector(2 downto 0);
   signal o_mif_af_addr : std_logic_vector(30 downto 0);
   signal o_mif_af_wren : std_logic;
   signal o_mif_wdf_wren : std_logic;
   signal o_mif_wdf_data : std_logic_vector(127 downto 0);
   signal o_mif_wdf_mask_data : std_logic_vector(15 downto 0);

   -- Clock period definitions
   constant clk_period : time := 10 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: ssp_top PORT MAP (
          clk => clk,
          rst => rst,
          o_mif_af_cmd => o_mif_af_cmd,
          o_mif_af_addr => o_mif_af_addr,
          o_mif_af_wren => o_mif_af_wren,
          i_mif_af_afull => i_mif_af_afull,
          o_mif_wdf_wren => o_mif_wdf_wren,
          o_mif_wdf_data => o_mif_wdf_data,
          o_mif_wdf_mask_data => o_mif_wdf_mask_data,
          i_mif_wdf_afull => i_mif_wdf_afull,
          i_mif_rd_data => i_mif_rd_data,
          i_mif_rd_valid => i_mif_rd_valid
        );

   -- Clock process definitions
   clk_process :process
   begin
		clk <= '0';
		wait for clk_period/2;
		clk <= '1';
		wait for clk_period/2;
   end process;

   -- Stimulus process
   stim_proc: process
   begin
      -- hold reset state for 100 ns.
      wait for 100 ns;	
      rst <= '0';
      
      -- transfer 16x16 reference block to 22 PEs      
      for j in 1 to 16 loop
        for i in 1 to 22 loop
          wait until o_mif_af_wren = '1';
          wait for clk_period*18;
          i_mif_rd_data <= X"02020202020202020202020202020202";
          i_mif_rd_valid <= '1'; 
          wait for clk_period*2;
          i_mif_rd_valid <= '0';       
        end loop;
      end loop;
      
      -- transfer 47x48 current block to 22 PEs
      for j in 1 to 47 loop
        for i in 1 to 22 loop
          wait until o_mif_af_wren = '1';
          wait for clk_period*18;
          i_mif_rd_data <= X"02020202020202020202020202020202";
          i_mif_rd_valid <= '1';
          wait for clk_period*2;
          i_mif_rd_valid <= '0';
          
          wait until o_mif_af_cmd = "001" and o_mif_af_wren = '1';
          wait for clk_period*18;
          i_mif_rd_data <= X"01010101010101010101010101010101";
          i_mif_rd_valid <= '1';
          wait for clk_period*2;
          i_mif_rd_valid <= '0';
          
          wait until o_mif_af_cmd = "001" and o_mif_af_wren = '1';
          wait for clk_period*18;
          i_mif_rd_data <= X"01010101010101010101010101010101";
          i_mif_rd_valid <= '1';
          wait for clk_period*2;
          i_mif_rd_valid <= '0';
        end loop;
      end loop;
      
      wait until o_mif_af_wren = '1';
      wait for clk_period*100;
      
      wait;
   end process;

END;
