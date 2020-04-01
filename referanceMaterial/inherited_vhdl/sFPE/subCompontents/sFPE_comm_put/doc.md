# sFPE_comm_put

##  Generics
*	DATA_WIDTH, *integer*,
*	TX_CH_WIDTH, *integer*,
*	TX_CH_NUM, *integer*,
*	PUTCH_EN, *boolean*,
*	STATE_EN, *boolean*,

##  Ports
*	clk, *in std_logic*,
*	rst, *in std_logic*,
*	i_put_ch_select, *in std_logic_vector(TX_CH_WIDTH-1 downto 0)*,
*	i_tx_autoinc, *in std_logic*,
*	i_tx_reset, *in std_logic*,
*	i_put_data, *in std_logic_vector(DATA_WIDTH-1 downto 0)*,
*	i_put_ch_full, *in VSIG_TYPE(TX_CH_NUM-1 downto 0)*,
*	i_put_inst, *in std_logic*,  
*	o_put_ch_data, *out VDATA_TYPE(TX_CH_NUM-1 downto 0)*,
*	o_put_ch_full, *out std_logic*,
*	o_put_ch_write, *out VSIG_TYPE(TX_CH_NUM-1 downto 0)*,
