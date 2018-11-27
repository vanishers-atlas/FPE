# sFPE_comm_get

##  Generics
*	DATA_WIDTH, *integer*,
  - the internal data width
*	OUT_DATA_WIDTH, *integer*,
  - the output (to sFPE) data width
  * Must be <= DATA_WIDTH
*	RX_CH_WIDTH, *integer*,
  - The number of bits used for selecting the fifo to read from
*	RX_CH_NUM, *integer*,
  - The number of fifo's inputs to the unit
  - Must be less than 2^(RX_CH_WIDTH)
*	GETCH_EN, *boolean*,
  - Controls if the unit works in a round robin or addressed style
  - false for addressed
  - true for round robin
*	STATE_EN, *boolean*,
  - Controls if the FIFO's state signals are percived to the sFPE

##  Ports
*	clk, *in std_logic*,
  -  Clock signal
*	rst, *in std_logic*,
  - Resets all data buffers
*	i_get_ch_select, *in std_logic_vector(RX_CH_WIDTH-1 downto 0)*,
  - Address of the selected fifo
  - Only has an effect in addressing mode
*	i_get_ch_data, *in VDATA_TYPE(RX_CH_NUM-1 downto 0)*,
  - A concated array of all FIFO data
  * Each fifo has a 32 bit section due to VHDL generic limits
*	i_get_ch_empty, *in VSIG_TYPE(RX_CH_NUM-1 downto 0)*,
  - A concated array of the fifos' empty state signals
*	i_get_inst, *in std_logic*,
  - Acts as a read signal
*	i_rx_autoinc, *in std_logic*,
  - When high the selected fifo addressed will be increased by one on clk raising get_data_wiring_gen
  - Requires the unit to be in robin robin mode
*	i_rx_reset, *in std_logic*,
  -  resets to round robin address back to the first fifo
  - Requires the unit to be in robin robin mode
*	o_get_data, *out std_logic_vector(OUT_DATA_WIDTH-1 downto 0)*,
  - The data red from the selected fifo
*	o_get_ch_empty, *out std_logic*,
  - The selected fifo's state output
*	o_get_ch_read, *out VSIG_TYPE(RX_CH_NUM-1 downto 0)*,
