----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05.07.2017 14:58:39
-- Design Name: 
-- Module Name: tb_axi_stream_generator_all - Behavioral
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

entity tb_axi_slave_master_1st is
     generic(
          DATA_WIDTH : integer := 32; 
          SDATA_WIDTH  :  integer  :=  64;
          EXIN_FIFO_NUM : integer := 2;
          EXOUT_FIFO_NUM : integer := 1;
          DEXOUT_FIFO_NUM : integer := 1;
          NUMBER_OF_INPUT_WORDS  : integer := 1024; 
          NUMBER_OF_OUTPUT_WORDS : integer := 2048;
          NUMBER_OF_DOUTPUT_WORDS : integer := 1
     );
--  Port ( );
end tb_axi_slave_master_1st;

architecture Behavioral of tb_axi_slave_master_1st is


    component axis_slave_master_ip_v1_0_1st is
        generic (
            -- Users to add parameters here            
            -- SSP parameters
            DATA_WIDTH  :  integer  :=  32;
            SDATA_WIDTH  :  integer  :=  64;
            EXIN_FIFO_NUM : integer := 2;
            EXOUT_FIFO_NUM : integer := 1;
            DEXOUT_FIFO_NUM : integer := 1;
            NUMBER_OF_INPUT_WORDS  : integer := 1024; 
            NUMBER_OF_OUTPUT_WORDS : integer := 2048;
            NUMBER_OF_DOUTPUT_WORDS : integer := 1;
            -- User parameters ends
            -- Do not modify the parameters beyond this line
    
    
            -- Parameters of Axi Slave Bus Interface S00_AXIS
            C_S00_AXIS_TDATA_WIDTH	: integer	:= 64;
    
            -- Parameters of Axi Master Bus Interface M00_AXIS
            C_M00_AXIS_TDATA_WIDTH	: integer	:= 32;
            C_M00_AXIS_START_COUNT	: integer	:= 32
        );
        port (
            -- Users to add ports here
            in_fifo_full : out std_logic := '0';
            out_fifo_full : out std_logic := '0';
            axi_last_s : out std_logic := '0';
            axi_last_m : out std_logic := '0';
            ssp_end : out std_logic := '0';
            -- User ports ends
            -- Do not modify the ports beyond this line
    
    
            -- Ports of Axi Slave Bus Interface S00_AXIS
            s00_axis_aclk	: in std_logic := '0';
            s00_axis_aresetn	: in std_logic := '0';
            s00_axis_tready	: out std_logic := '0';
            s00_axis_tdata	: in std_logic_vector(C_S00_AXIS_TDATA_WIDTH-1 downto 0) := (others => '0');
            s00_axis_tstrb	: in std_logic_vector((C_S00_AXIS_TDATA_WIDTH/8)-1 downto 0) := (others => '0');
            s00_axis_tlast	: in std_logic := '0';
            s00_axis_tvalid	: in std_logic := '0';
    
            -- Ports of Axi Master Bus Interface M00_AXIS
            m00_axis_aclk	: in std_logic := '0';
            m00_axis_aresetn	: in std_logic := '0';
            m00_axis_tvalid	: out std_logic := '0';
            m00_axis_tdata	: out std_logic_vector(C_M00_AXIS_TDATA_WIDTH-1 downto 0) := (others => '0');
            m00_axis_tstrb	: out std_logic_vector((C_M00_AXIS_TDATA_WIDTH/8)-1 downto 0) := (others => '0');
            m00_axis_tlast	: out std_logic := '0';
            m00_axis_tready	: in std_logic := '0'
        );
    end component;
    
    signal ACLK_reg    :    std_logic; 
    signal ARESETN_reg    :    std_logic; 
	 
    signal S_AXIS_TREADY_reg    :    std_logic;
    signal S_AXIS_TDATA_reg    :    std_logic_vector(SDATA_WIDTH-1 downto 0);
    signal S_AXIS_TLAST_reg    :    std_logic;
    signal S_AXIS_TVALID_reg    :    std_logic;
	 
    signal M_AXIS_TVALID_reg    :   std_logic;
    signal M_AXIS_TDATA_reg    :    std_logic_vector(DATA_WIDTH-1 downto 0);
    signal M_AXIS_TLAST_reg    :    std_logic;
    signal M_AXIS_TREADY_reg    :    std_logic;
	 
    signal M_AXIS_TVALID_reg_1    :   std_logic;
    signal M_AXIS_TDATA_reg_1    :    std_logic_vector(SDATA_WIDTH-1 downto 0);
    signal M_AXIS_TLAST_reg_1    :    std_logic;
    signal M_AXIS_TREADY_reg_1    :    std_logic;
	 
    signal S_AXIS_TDATA_ssp_reg    :    std_logic_vector(SDATA_WIDTH-1 downto 0);
    signal M_AXIS_TDATA_ssp_reg    :    std_logic_vector(SDATA_WIDTH-1 downto 0);
    signal M_AXIS_TDATA_ssp_reg_1    :    std_logic_vector(SDATA_WIDTH-1 downto 0);
	 
	signal IN_DATA_COUNT_reg    :    std_logic_vector(11 downto 0);
	signal OUT_DATA_COUNT_reg    :    std_logic_vector(11 downto 0);
	signal OUT_DDATA_COUNT_reg    :    std_logic_vector(11 downto 0);
	signal IN_DATA_LAST_reg    :    std_logic;
	signal OUT_DATA_LAST_reg    :    std_logic;
	signal OUT_DDATA_LAST_reg    :    std_logic;

--        signal ap_start_reg        :  std_logic := '0';
--        signal ap_idle_reg         :  std_logic := '0';
--        signal ap_done_reg         :  std_logic := '0';
--        signal ap_ready_reg        :  std_logic := '0';
        
                --signal idle_state_reg         :  std_logic := '0';
                --signal read_state_reg         :  std_logic := '0';
                --signal write_state_reg        :  std_logic := '0';
        
    component axis_test_ip_v2_0_M00_AXIS is
        generic (
            -- Users to add parameters here
    
            -- User parameters ends
            -- Do not modify the parameters beyond this line
    
            -- Width of S_AXIS address bus. The slave accepts the read and write addresses of width C_M_AXIS_TDATA_WIDTH.
            C_M_AXIS_TDATA_WIDTH    : integer    := 32;
            -- Start count is the numeber of clock cycles the master will wait before initiating/issuing any transaction.
            C_M_START_COUNT    : integer    := 1
        );
        port (
            -- Users to add ports here
    
            -- User ports ends
            -- Do not modify the ports beyond this line
    
            -- Global ports
            M_AXIS_ACLK    : in std_logic;
            -- 
            M_AXIS_ARESETN    : in std_logic;
            -- Master Stream Ports. TVALID indicates that the master is driving a valid transfer, A transfer takes place when both TVALID and TREADY are asserted. 
            M_AXIS_TVALID    : out std_logic;
            -- TDATA is the primary payload that is used to provide the data that is passing across the interface from the master.
            M_AXIS_TDATA    : out std_logic_vector(C_M_AXIS_TDATA_WIDTH-1 downto 0);
            -- TSTRB is the byte qualifier that indicates whether the content of the associated byte of TDATA is processed as a data byte or a position byte.
            -- M_AXIS_TSTRB    : out std_logic_vector((C_M_AXIS_TDATA_WIDTH/8)-1 downto 0);
            -- TLAST indicates the boundary of a packet.
            M_AXIS_TLAST    : out std_logic;
            -- TREADY indicates that the slave can accept a transfer in the current cycle.
            M_AXIS_TREADY    : in std_logic
        );
    end component axis_test_ip_v2_0_M00_AXIS;
    
    component axis_test_ip_v2_0_S00_AXIS is
        generic (
            -- Users to add parameters here
    
            -- User parameters ends
            -- Do not modify the parameters beyond this line
    
            -- AXI4Stream sink: Data Width
            C_S_AXIS_TDATA_WIDTH    : integer    := 32;
				NUMBER_OF_INPUT_WORDS	: integer	:= 64
        );
        port (
            -- Users to add ports here
    
            -- User ports ends
            -- Do not modify the ports beyond this line
    
            -- AXI4Stream sink: Clock
            S_AXIS_ACLK    : in std_logic;
            -- AXI4Stream sink: Reset
            S_AXIS_ARESETN    : in std_logic;
            -- Ready to accept data in
            S_AXIS_TREADY    : out std_logic;
            -- Data in
            S_AXIS_TDATA    : in std_logic_vector(C_S_AXIS_TDATA_WIDTH-1 downto 0);
            -- Byte qualifier
            -- S_AXIS_TSTRB    : in std_logic_vector((C_S_AXIS_TDATA_WIDTH/8)-1 downto 0);
            -- Indicates boundary of last packet
            S_AXIS_TLAST    : in std_logic;
            -- Data is in valid
            S_AXIS_TVALID    : in std_logic
        );
    end component axis_test_ip_v2_0_S00_AXIS;
    
    -- Clock period definitions
    constant clk_in_period : time := 10 ns;
    
    --signal debug_port_reg : std_logic_vector(63 downto 0);
    --signal debug_port_reg1 : std_logic_vector(63 downto 0);
    signal in_fifo_full_reg    : std_logic;
    signal out_fifo_full_reg    : std_logic;
    signal axi_last_s_reg    : std_logic;
    signal axi_last_m_reg    : std_logic;
    signal ssp_end_reg    : std_logic;
        
begin

    uut: axis_slave_master_ip_v1_0_1st
	 generic map(
		  DATA_WIDTH =>  DATA_WIDTH,
		  SDATA_WIDTH =>  SDATA_WIDTH,
		  EXIN_FIFO_NUM  =>  EXIN_FIFO_NUM,
		  EXOUT_FIFO_NUM =>  EXOUT_FIFO_NUM,
          DEXOUT_FIFO_NUM =>  DEXOUT_FIFO_NUM,
		  NUMBER_OF_INPUT_WORDS  =>  NUMBER_OF_INPUT_WORDS,
		  NUMBER_OF_OUTPUT_WORDS =>  NUMBER_OF_OUTPUT_WORDS,
		  NUMBER_OF_DOUTPUT_WORDS =>  NUMBER_OF_DOUTPUT_WORDS,
          -- Parameters of Axi Slave Bus Interface S00_AXIS
          C_S00_AXIS_TDATA_WIDTH =>  SDATA_WIDTH,
  
          -- Parameters of Axi Master Bus Interface M00_AXIS
          C_M00_AXIS_TDATA_WIDTH =>  DATA_WIDTH,
          C_M00_AXIS_START_COUNT =>  32
	 )
    port map(
        -- Users to add ports here
        in_fifo_full => in_fifo_full_reg,
        out_fifo_full => out_fifo_full_reg,
        axi_last_s => axi_last_s_reg,
        axi_last_m => axi_last_m_reg,
        ssp_end => ssp_end_reg,
        -- User ports ends
        
        -- Do not modify the ports beyond this line        
        -- Ports of Axi Slave Bus Interface S00_AXIS
        s00_axis_aclk    => ACLK_reg,
        s00_axis_aresetn    => ARESETN_reg,
        s00_axis_tready    => S_AXIS_TREADY_reg,
        s00_axis_tdata    => S_AXIS_TDATA_reg,
        s00_axis_tstrb    => open,
        s00_axis_tlast    => S_AXIS_TLAST_reg,
        s00_axis_tvalid    => S_AXIS_TVALID_reg,

        -- Ports of Axi Master Bus Interface M00_AXIS
        m00_axis_aclk    => ACLK_reg,
        m00_axis_aresetn    => ARESETN_reg,
        m00_axis_tvalid    => M_AXIS_TVALID_reg,
        m00_axis_tdata    => M_AXIS_TDATA_reg,
        m00_axis_tstrb    => open,
        m00_axis_tlast    => M_AXIS_TLAST_reg,
        m00_axis_tready   => M_AXIS_TREADY_reg
    );
--	 S_AXIS_TDATA_ssp_reg <= S_AXIS_TDATA_reg;
--	 M_AXIS_TDATA_reg <= M_AXIS_TDATA_ssp_reg;
--	 M_AXIS_TDATA_reg_1 <= M_AXIS_TDATA_ssp_reg_1;
    
    uut1 : axis_test_ip_v2_0_M00_AXIS
	 generic map(
		C_M_AXIS_TDATA_WIDTH =>  SDATA_WIDTH,
		C_M_START_COUNT =>  1
	 )
    port map(
        M_AXIS_ACLK => ACLK_reg,
        M_AXIS_ARESETN => ARESETN_reg,
        M_AXIS_TVALID => S_AXIS_TVALID_reg,
        M_AXIS_TDATA => S_AXIS_TDATA_reg,
        M_AXIS_TLAST => S_AXIS_TLAST_reg,
        M_AXIS_TREADY => S_AXIS_TREADY_reg
    );
    
    uut2 : axis_test_ip_v2_0_S00_AXIS
	 generic map(
		C_S_AXIS_TDATA_WIDTH =>  DATA_WIDTH,
		NUMBER_OF_INPUT_WORDS =>  NUMBER_OF_OUTPUT_WORDS
	 )
    port map(
        S_AXIS_ACLK => ACLK_reg,
        S_AXIS_ARESETN => ARESETN_reg,
        S_AXIS_TREADY => M_AXIS_TREADY_reg,
        S_AXIS_TDATA => M_AXIS_TDATA_reg,
        S_AXIS_TLAST => M_AXIS_TLAST_reg,
        S_AXIS_TVALID => M_AXIS_TVALID_reg
    );
    
    uut3 : axis_test_ip_v2_0_S00_AXIS
	 generic map(
		C_S_AXIS_TDATA_WIDTH =>  SDATA_WIDTH,
		NUMBER_OF_INPUT_WORDS =>  NUMBER_OF_DOUTPUT_WORDS
	 )
    port map(
        S_AXIS_ACLK => ACLK_reg,
        S_AXIS_ARESETN => ARESETN_reg,
        S_AXIS_TREADY => M_AXIS_TREADY_reg_1,
        S_AXIS_TDATA => M_AXIS_TDATA_reg_1,
        S_AXIS_TLAST => M_AXIS_TLAST_reg_1,
        S_AXIS_TVALID => M_AXIS_TVALID_reg_1
    );


    -- Clock process definitions
    clk_in_process :process
    begin
        ACLK_reg <= '0';
        wait for clk_in_period/2;
        ACLK_reg <= '1';
        wait for clk_in_period/2;
    end process clk_in_process;
    
    -- Stimulus process
    stim_proc: process
    begin        
	 
         -- hold reset state for 100 ns.
         wait for 10*clk_in_period;   
         ARESETN_reg <= '0'; 
         wait for 10*clk_in_period;   
         ARESETN_reg <= '1'; 
         --ap_start_reg <= '1';
         wait for clk_in_period/2;
			wait for 10*clk_in_period; 
			wait for 10*clk_in_period; 
			wait for 10*clk_in_period; 
			wait for 500*clk_in_period; 
         wait;
			
    end process stim_proc;


end Behavioral;
