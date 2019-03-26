*	# sFPE_RF

## Generics
*	RF_ADDR_WIDTH, *integer*,
*	RF_DATA_WIDTH, *integer*,
*	FRAC_BITS, *integer*,
*	RF_INIT_EN, *boolean*,
*	RF_INIT_FILE, *string*,
*	PA0_DEPTH, *integer*,
*	PA1_DEPTH, *integer*,

## Ports
*	clk, *in std_logic*,
*	rst, *in std_logic*,
*	i_rdaddr_a, *in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0)*,
*	i_rdaddr_b, *in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0)*,
*	i_rdaddr_c, *in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0)*,
*	o_rddata_a, *out std_logic_vector (RF_DATA_WIDTH-1 downto 0)*,
*	o_rddata_b, *out std_logic_vector (RF_DATA_WIDTH-1 downto 0)*,
*	o_rddata_c, *out std_logic_vector (RF_DATA_WIDTH-1 downto 0)*,
*	i_wraddr_d, *in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0)*,
*	i_wrdata_d, *in std_logic_vector (RF_DATA_WIDTH-1 downto 0)*,
*	i_wen, *in std_logic*,
