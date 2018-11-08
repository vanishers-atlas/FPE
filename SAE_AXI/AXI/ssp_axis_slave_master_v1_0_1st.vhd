
library ieee;  
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.numeric_std.all;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;
library unisim;
use unisim.vcomponents.all;

entity axis_slave_master_ip_v1_0_1st is
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
        spu_en_1: out std_logic := '0';
        spu_en_2: out std_logic := '0';
        spu_en_3: out std_logic := '0';
        spu_en_4: out std_logic := '0';
        spu_en_5: out std_logic := '0';
        spu_en_6: out std_logic := '0';
        fifo_end_1: out std_logic;
        fifo_end_2: out std_logic;
        fifo_end_3: out std_logic;
        fifo_end_4: out std_logic;
        fifo_end_5: out std_logic;
        fifo_end_6: out std_logic;
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
end axis_slave_master_ip_v1_0_1st;

architecture arch_imp of axis_slave_master_ip_v1_0_1st is 

   
	COMPONENT ssp_cache_core_wrap_stage_1st
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
			clk : in std_logic;
			rst : in std_logic;
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
			o_ddata_last : out VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');		
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
	END COMPONENT;	
	
    signal spu_en_1_reg: std_logic;
    signal spu_en_2_reg: std_logic;
    signal spu_en_3_reg: std_logic;
    signal spu_en_4_reg: std_logic;
    signal spu_en_5_reg: std_logic;
    signal spu_en_6_reg: std_logic;
        
    signal fifo_end_1_reg: std_logic;
    signal fifo_end_2_reg: std_logic;
    signal fifo_end_3_reg: std_logic;
    signal fifo_end_4_reg: std_logic;
    signal fifo_end_5_reg: std_logic;
    signal fifo_end_6_reg: std_logic;
	
    signal clk : std_logic := '0';
    signal rst : std_logic := '0';
    signal i_data_last : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
    signal o_data_last : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal o_pc_en1 : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
    signal o_pc_en2 : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');

    signal push_ch_data : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal push_ch_full : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
    signal push_ch_empty : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
    signal push_ch_write : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');
    signal push_ch_read : VSIG_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>'0');

    signal pop_ch_data : VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data1 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data2 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data3 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data4 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data5 : VDATA_TYPE(EXIN_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));
    signal pop_ch_data6 : VDATA_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));    
    signal pop_ch_write : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal pop_ch_read : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal pop_ch_read_reg : std_logic := '0';
    signal pop_ch_read_delay_reg : std_logic := '0';
    signal pop_ch_full : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal pop_ch_empty : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal pop_ch_empty_reg : std_logic := '0';
    signal pop_ch_empty_reg_delay : std_logic := '0';
    signal tlast_asserted_reg : VSIG_TYPE(EXOUT_FIFO_NUM-1 downto 0) := (others=>'0');

    signal o_ddata_last : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal dpop_ch_data : VDATA_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>(others=>'0'));    
    signal dpop_ch_write : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal dpop_ch_read : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal dpop_ch_empty : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal dtlast_asserted_reg : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
    signal o_pc_en3 : VSIG_TYPE(DEXOUT_FIFO_NUM-1 downto 0) := (others=>'0');
       
    signal IN_DATA_COUNT_reg : std_logic_vector(11 downto 0);
    signal OUT_DATA_COUNT_reg : std_logic_vector(11 downto 0);
    
    signal s00_axis_tvalid_reg : std_logic;
    signal s00_axis_tready_reg : std_logic;
    signal m00_axis_tvalid_reg : std_logic;
    signal m00_axis_tready_reg : std_logic;
    signal m00_axis_tlast_reg : std_logic;
    
	signal SSP_RDEN_OUT_reg : std_logic;
	signal SSP_DATA_OUT_reg : std_logic_vector(C_S00_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0');
	signal SSP_DATA_IN_reg : std_logic_vector(C_M00_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0');

	signal start : std_logic;
	signal ssp_wren_reg : std_logic;
	signal ssp_rden_reg : std_logic;

	-- component declaration
	component axis_slave_master_ip_v1_0_S00_AXIS is
		generic (
		C_S_AXIS_TDATA_WIDTH	: integer	:= 32;
        NUMBER_OF_INPUT_WORDS : integer := 1024
		);
		port (
		S_AXIS_ACLK	: in std_logic := '0';
		S_AXIS_ARESETN	: in std_logic := '0';
		S_AXIS_TREADY	: out std_logic := '0';
		S_AXIS_TDATA	: in std_logic_vector(C_S_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0');
		S_AXIS_TSTRB	: in std_logic_vector((C_S_AXIS_TDATA_WIDTH/8)-1 downto 0) := (others=>'0');
		S_AXIS_TLAST	: in std_logic := '0';
		S_AXIS_TVALID	: in std_logic := '0';
		
		start : out std_logic := '0';
        SSP_WREN : out std_logic;
		SSP_DATA_OUT : out std_logic_vector(C_S_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0')
		);
	end component axis_slave_master_ip_v1_0_S00_AXIS;

	component axis_slave_master_ip_v1_0_M00_AXIS is
		generic (
		C_M_AXIS_TDATA_WIDTH	: integer	:= 32;
		C_M_START_COUNT	: integer	:= 32;
        NUMBER_OF_OUTPUT_WORDS : integer := 2048
		);
		port (
		M_AXIS_ACLK	: in std_logic := '0';
		M_AXIS_ARESETN	: in std_logic := '0';
		M_AXIS_TVALID	: out std_logic := '0';
		M_AXIS_TDATA	: out std_logic_vector(C_M_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0');
		M_AXIS_TSTRB	: out std_logic_vector((C_M_AXIS_TDATA_WIDTH/8)-1 downto 0) := (others=>'0');
		M_AXIS_TLAST	: out std_logic := '0';
		M_AXIS_TREADY	: in std_logic := '0';
		
		start : in std_logic := '0';
        SSP_RDEN : out std_logic;
		SSP_DATA_IN : in std_logic_vector(C_M_AXIS_TDATA_WIDTH-1 downto 0) := (others=>'0')
		);
	end component axis_slave_master_ip_v1_0_M00_AXIS;

begin

-- Instantiation of Axi Bus Interface S00_AXIS
axis_slave_master_ip_v1_0_S00_AXIS_inst : axis_slave_master_ip_v1_0_S00_AXIS
	generic map (
		C_S_AXIS_TDATA_WIDTH	=> C_S00_AXIS_TDATA_WIDTH,
        NUMBER_OF_INPUT_WORDS    => NUMBER_OF_INPUT_WORDS
	)
	port map (
		S_AXIS_ACLK	=> s00_axis_aclk,
		S_AXIS_ARESETN	=> s00_axis_aresetn,
		S_AXIS_TREADY	=> s00_axis_tready_reg,
		S_AXIS_TDATA	=> s00_axis_tdata,
		S_AXIS_TSTRB	=> s00_axis_tstrb,
		S_AXIS_TLAST	=> s00_axis_tlast,
		S_AXIS_TVALID	=> s00_axis_tvalid_reg,
		start => open,
        SSP_WREN => ssp_wren_reg,
		SSP_DATA_OUT => SSP_DATA_OUT_reg
	);
	s00_axis_tvalid_reg <= s00_axis_tvalid;
	s00_axis_tready <= s00_axis_tready_reg;

-- Instantiation of Axi Bus Interface M00_AXIS
axis_slave_master_ip_v1_0_M00_AXIS_inst : axis_slave_master_ip_v1_0_M00_AXIS
	generic map (
		C_M_AXIS_TDATA_WIDTH	=> C_M00_AXIS_TDATA_WIDTH,
		C_M_START_COUNT	=> C_M00_AXIS_START_COUNT,
        NUMBER_OF_OUTPUT_WORDS	=> NUMBER_OF_OUTPUT_WORDS
	)
	port map (
		M_AXIS_ACLK	=> m00_axis_aclk,
		M_AXIS_ARESETN	=> m00_axis_aresetn,
		M_AXIS_TVALID	=> m00_axis_tvalid_reg,
		M_AXIS_TDATA	=> m00_axis_tdata,
		M_AXIS_TSTRB	=> m00_axis_tstrb,
		M_AXIS_TLAST	=> m00_axis_tlast_reg,
		M_AXIS_TREADY	=> m00_axis_tready_reg,
		start => start,
        SSP_RDEN => ssp_rden_reg,
		SSP_DATA_IN  =>  SSP_DATA_IN_reg
	);
	m00_axis_tvalid <= m00_axis_tvalid_reg;
	m00_axis_tready_reg <= m00_axis_tready;
	m00_axis_tlast <= m00_axis_tlast_reg;

	-- Add user logic here
	ssp_cache_core: ssp_cache_core_wrap_stage_1st 
	generic map( 
		CORE_WIDTH => DATA_WIDTH,
		INPUT_WIDTH => DATA_WIDTH,
		OUTPUT_WIDTH => DATA_WIDTH,
		EXIN_FIFO_NUM => EXIN_FIFO_NUM,
		EXOUT_FIFO_NUM => EXOUT_FIFO_NUM,
		DEXOUT_FIFO_NUM => DEXOUT_FIFO_NUM,
		INPUT_WORDS => NUMBER_OF_INPUT_WORDS, 
		OUTPUT_WORDS => NUMBER_OF_OUTPUT_WORDS,
		DOUTPUT_WORDS => NUMBER_OF_DOUTPUT_WORDS,
		IOFIFODEPTH => 1024
	)  -- switch of state signal
	port map(
		clk => clk,
		rst => rst,
		i_data_last => i_data_last,
		o_data_last => o_data_last,
		i_push_ch_data => push_ch_data,
		i_push_ch_write => push_ch_write,
		o_push_ch_read => push_ch_read,
		o_push_ch_full => push_ch_full,
		o_push_ch_empty => push_ch_empty,
		o_push_ch_en => o_pc_en1,
		o_pop_ch_data => pop_ch_data,
		o_pop_ch_write => pop_ch_write,
		i_pop_ch_read => pop_ch_read,
		o_pop_ch_full => pop_ch_full,
		o_pop_ch_empty => pop_ch_empty,
		o_pop_ch_en => o_pc_en2,
		tlast_asserted => tlast_asserted_reg,
		-- debug
		o_ddata_last => open,
		o_dpop_ch_data => open,
		o_dpop_ch_write => open,
		i_dpop_ch_read => open,
		o_dpop_ch_empty => open,
		o_dpop_ch_en => open,
		dtlast_asserted => open,
        -- for debug signal 
        spu_en_1 => spu_en_1_reg,
        spu_en_2 => spu_en_2_reg,
        spu_en_3 => spu_en_3_reg,
        spu_en_4 => spu_en_4_reg,
        spu_en_5 => spu_en_5_reg,
        spu_en_6 => spu_en_6_reg,
        fifo_end_1 => fifo_end_1_reg,
        fifo_end_2 => fifo_end_2_reg,
        fifo_end_3 => fifo_end_3_reg,
        fifo_end_4 => fifo_end_4_reg,
        fifo_end_5 => fifo_end_5_reg,
        fifo_end_6 => fifo_end_6_reg
	);
	
	clk <= s00_axis_aclk;
	rst <= not s00_axis_aresetn;
	
--  i_data_last(0) <= '1' when push_ch_full(0) = '1' and push_ch_full(1) = '1' else '0'; -- added for ssp
--  i_data_last(1) <= '1' when push_ch_full(0) = '1' and push_ch_full(1) = '1' else '0'; -- added for ssp
    i_data_last(0) <= push_ch_full(0) and push_ch_full(1); -- added for ssp
    i_data_last(1) <= push_ch_full(0) and push_ch_full(1); -- added for ssp
	push_ch_data(0) <= SSP_DATA_OUT_reg(31 downto 0);
	push_ch_data(1) <= SSP_DATA_OUT_reg(63 downto 32);
--	push_ch_write(0) <= '1' when ssp_wren_reg = '1' else '0';
--	push_ch_write(1) <= '1' when ssp_wren_reg = '1' else '0';
    push_ch_write(0) <= ssp_wren_reg;
    push_ch_write(1) <= ssp_wren_reg;
	
--	pop_ch_read(0) <= '1' when ssp_rden_reg = '1' else '0';
--  pop_ch_read(1) <= '1' when ssp_rden_reg = '1' else '0';
    pop_ch_read(0) <= ssp_rden_reg;
--    pop_ch_read(1) <= ssp_rden_reg;
	SSP_DATA_IN_reg <= pop_ch_data(0);
--    SSP_DATA_IN_reg <= pop_ch_data(1) & pop_ch_data(0);
--	start <= '1' when o_data_last(0) = '1' else '0';
    start <= o_data_last(0);
--	tlast_asserted_reg(0) <= '1' when m00_axis_tlast_reg = '1' else '0';
    tlast_asserted_reg(0) <= m00_axis_tlast_reg;
	
--	in_fifo_full <= '1' when push_ch_full(0) = '1' and push_ch_full(1) = '1';
--	out_fifo_full <= '1' when pop_ch_full(0) = '1';
--	axi_last_s <= '1' when s00_axis_tlast = '1';
--	axi_last_m <= '1' when m00_axis_tlast_reg = '1';
--	ssp_end <= '1' when o_data_last(0) = '1';
        
--    spu_en_1 <= '1' when spu_en_1_reg = '1';
--    spu_en_2 <= '1' when spu_en_2_reg = '1';
--    spu_en_3 <= '1' when spu_en_3_reg = '1';
--    spu_en_4 <= '1' when spu_en_4_reg = '1';
--    spu_en_5 <= '1' when spu_en_5_reg = '1';
--    spu_en_6 <= '1' when spu_en_6_reg = '1';
--        spu_en_1 <= '1';
--        spu_en_2 <= '1';
--        spu_en_3 <= '1';
--        spu_en_4 <= '1';
--        spu_en_5 <= '1';
--        spu_en_6 <= '1';
    u_led: process(clk)
    begin
        if clk'event and clk = '1' then
            if spu_en_1_reg = '1' then
                spu_en_1 <= '1';
            end if;
            if spu_en_2_reg = '1' then
                spu_en_2 <= '1';
            end if;
            if spu_en_3_reg = '1' then
                spu_en_3 <= '1';
            end if;
            if spu_en_4_reg = '1' then
                spu_en_4 <= '1';
            end if;
            if spu_en_5_reg = '1' then
                spu_en_5 <= '1';
            end if;
            if spu_en_6_reg = '1' then
                spu_en_6 <= '1';
            end if;
            if fifo_end_1_reg = '1' then
                fifo_end_1 <= '1';
            end if;
            if fifo_end_2_reg = '1' then
                fifo_end_2 <= '1';
            end if;
            if fifo_end_3_reg = '1' then
                fifo_end_3 <= '1';
            end if;
            if fifo_end_4_reg = '1' then
                fifo_end_4 <= '1';
            end if;
            if fifo_end_5_reg = '1' then
                fifo_end_5 <= '1';
            end if;
            if fifo_end_6_reg = '1' then
                fifo_end_6 <= '1';
            end if;
            if push_ch_full(0) = '1' and push_ch_full(1) = '1' then
                in_fifo_full <= '1';
            end if;
            if pop_ch_full(0) = '1' then
                out_fifo_full <= '1';
            end if;
            if s00_axis_tlast = '1' then
                axi_last_s <= '1';
            end if;
            if m00_axis_tlast_reg = '1' then
                axi_last_m <= '1';
            end if;
            if o_data_last(0) = '1' then
                ssp_end <= '1';
            end if;
        end if;
    end process;
	-- User logic ends

end arch_imp;
