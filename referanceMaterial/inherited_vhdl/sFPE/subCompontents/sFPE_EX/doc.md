# sFPE_EX

##  Generics
*	DATA_WIDTH, *integer*,
*	CORE_DATA_WIDTH, *integer*,
*	DATA_TYPE, *integer*,
*	SLICE_NUM, *integer*,
*	OPM_NUM, *integer*,
*	ALUM_NUM, *integer*,
*	MULREG_EN, *boolean*,
*	FRAC_BITS, *integer*,
*	MASK_EN, *boolean*,
*	ALUSRA_VAL, *integer*,
*	BRANCH_EN, *boolean*,

## Ports
*	clk, *in  std_logic*,
*	rst, *in  std_logic*,
*	i_opmode, *in  std_logic_vector(7*OPM_NUM-1 downto 0)*,
*	i_alumode, *in  std_logic_vector(4*ALUM_NUM-1 downto 0)*,
*	i_src_a, *in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
*	i_src_b, *in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
*	i_src_c, *in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
*	o_sign, *out std_logic*,
*	o_zero, *out std_logic*,
*	o_dsp48_result, *out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
*	o_dsp48sra_result, *out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
