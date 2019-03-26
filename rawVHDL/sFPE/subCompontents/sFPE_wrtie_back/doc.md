# sFPE_wrtie_back
## Generics
* CORE_DATA_WIDTH, *integer*,
* ABSDIFF_EN, *boolean*,
- ALUSRA_EN, *boolean*,

## Ports
* i_dsp48_result, *in std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
* i_dsp48sra_result, *in std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
* i_alusra, *in std_logic*,
* i_CA_absdiff, *in std_logic*
* i_CA_absdiff_d, *in std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*
* o_result, *out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)*,
