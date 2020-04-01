# sFPE_PM

## Generics
  PM_SIZE, *integer*,
  PM_ADDR_WIDTH, *integer*,
  PM_DATA_WIDTH, *integer*,
  USE_BRAM_FOR_LARGE_PM, *boolean*,
  PM_INIT_FILE, *string*,
  PB0_DEPTH, *integer*,
  PB1_DEPTH, *integer*,

## Ports
  clk, *in std_logic*,
  rst, *in std_logic*,
  i_en, *in std_logic*,
  i_addr, *in std_logic_vector (PM_ADDR_WIDTH-1 downto 0)*,
  o_pm, *out std_logic_vector (PM_DATA_WIDTH-1 downto 0)*,
