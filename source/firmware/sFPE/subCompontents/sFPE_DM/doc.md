# sFPE_DM

## Generics
*	DM_OFFSET_WIDTH, *integer*,
*	DM_SIZE, *integer*,
*	DM_ADDR_WIDTH, *integer*,
*	DM_DATA_WIDTH, *integer*,
*	DM_INIT_EN, *boolean*,
*	USE_BRAM_FOR_LARGE_DM, *boolean*,
*	DM_INIT_FILE, *string*,
*	DM_TWO_RD_PORTS, *boolean*,
*	DM_TRUE_2R1W, *boolean*,
*	PA0_DEPTH, *integer*,
*	PA1_DEPTH, *integer*,

##  Ports
*	clk, *in std_logic*,
*	rst, *in std_logic*,
*	i_dm_rd_addr_0, *in std_logic_vector (DM_ADDR_WIDTH-1 downto 0)*,
*	i_dm_rd_addr_1, *in std_logic_vector (DM_ADDR_WIDTH-1 downto 0)*,
*	i_dm_wr_addr, *in std_logic_vector (DM_ADDR_WIDTH-1 downto 0)*,
*	i_dm_wen, *in std_logic*,
*	i_dm_din, *in std_logic_vector (DM_DATA_WIDTH-1 downto 0)*,
*	o_dm_dout0, *out std_logic_vector (DM_DATA_WIDTH-1 downto 0)*,
*	o_dm_dout1, *out std_logic_vector (DM_DATA_WIDTH-1 downto 0)*,
