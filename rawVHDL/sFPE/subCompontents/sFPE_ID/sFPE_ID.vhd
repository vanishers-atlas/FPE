--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package sFPE_ID_pkg is
  component sFPE_ID is
    generic(
      DATA_WIDTH       : integer:= 16;
      DATA_TYPE        : integer:= 1;
      SLICE_NUM        : integer:= 1;
      RF_ADDR_WIDTH    : integer:= 5;
      OPCODE_WIDTH     : integer:= 6;
      PM_ADDR_WIDTH    : integer:= 6;
      OPM_NUM          : integer:= 1;
      ALUM_NUM         : integer:= 1;
      FLEXA_TYPE       : integer:= 1;
      FLEXB_TYPE       : integer:= 1;
      FLEXC_TYPE       : integer:= 1;
      BSLAVE           : boolean:= false;
      BMASTER          : boolean:= false;
      BMASTER_NUM      : integer:= 1;
      BRANCH_EN        : boolean:= false;
      JMP_EN           : boolean:= false;
      RPT_EN           : boolean:= false;
      RF_EN            : boolean:= false;
      DM_EN            : boolean:= false;
      DM_TWO_RD_PORTS  : boolean:= false;
      SM_EN            : boolean:= false;
      GETCH_EN         : boolean:= false;
      PUTCH_EN         : boolean:= false;
      MASKEQ_EN        : boolean:= false;
      MASKGT_EN        : boolean:= false;
      MASKLT_EN        : boolean:= false;
      MASKGE_EN        : boolean:= false;
      MASKLE_EN        : boolean:= false;
      MASKNE_EN        : boolean:= false;
      ALUSRA_EN        : boolean:= false;
      ABSDIFF_EN       : boolean:= false;
      ABSDIFF_WITHACCUM: boolean:= false
    );
    port(
      clk                   : in std_logic;
      i_pm_do               : in std_logic_vector(31 downto 0);
      o_id_opmode           : out std_logic_vector(7*OPM_NUM-1 downto 0);
      o_id_alumode          : out std_logic_vector(4*ALUM_NUM-1 downto 0);
      -- Control signals
      i_ext_barrier         : in  std_logic:= '0'; -- from external master sFPE
      o_en_pc               : out std_logic;
      o_ext_en_sFPE          : out std_logic;
      o_ext_id_barrier      : out std_logic_vector(BMASTER_NUM-1 downto 0);
      i_ext_en_sFPE          : in  std_logic:= '1'; -- from external slave sFPE

      -- component signals
      o_id_get_or_peak0: out std_logic:= '0';
      o_id_get_or_peak1: out std_logic:= '0';
      o_id_get0        : out std_logic:= '0';
      o_id_get1        : out std_logic:= '0';
      o_id_fifowrite        : out std_logic:= '0';
      o_id_rx_autoinc       : out std_logic:= '0';
      o_id_rx_reset         : out std_logic:= '0';
      o_id_tx_autoinc       : out std_logic:= '0';
      o_id_tx_reset         : out std_logic:= '0';

      o_id_rddm0            : out std_logic:= '0';
      o_id_rddm1            : out std_logic:= '0';
      o_id_wrdm             : out std_logic:= '0';
      o_id_dm_set_rb_m0     : out std_logic:= '0';
      o_id_dm_set_rb_m1     : out std_logic:= '0';
      o_id_dm_set_rb_n0     : out std_logic:= '0';
      o_id_dm_set_rb_n1     : out std_logic:= '0';
      o_id_dm_inc_rb_m0     : out std_logic:= '0';
      o_id_dm_inc_rb_m1     : out std_logic:= '0';
      o_id_dm_inc_rb_n0     : out std_logic:= '0';
      o_id_dm_inc_rb_n1     : out std_logic:= '0';
      o_id_dm_autoinc_rb_m  : out std_logic:= '0';
      o_id_dm_autoinc_rb_n  : out std_logic:= '0';
      o_id_dm_set_wb_0      : out std_logic:= '0';
      o_id_dm_set_wb_1      : out std_logic:= '0';
      o_id_dm_inc_wb_0      : out std_logic:= '0';
      o_id_dm_inc_wb_1      : out std_logic:= '0';
      o_id_dm_autoinc_wb    : out std_logic:= '0';

      o_id_sm_set_rb_0      : out std_logic:= '0';
      o_id_sm_inc_rb_0      : out std_logic:= '0';
      o_id_sm_set_wb_0      : out std_logic:= '0';
      o_id_sm_inc_wb_0      : out std_logic:= '0';
      o_id_sm_autoinc_rb    : out std_logic:= '0';
      o_id_sm_autoinc_wb    : out std_logic:= '0';
      o_id_sm_wen           : out std_logic:= '0';
      o_id_rdsm             : out std_logic:= '0';

      o_id_rf_wen           : out std_logic:= '0';

      o_id_b                : out std_logic:= '0';
      o_id_rpt              : out std_logic:= '0';
      o_id_beq              : out std_logic:= '0';
      o_id_bgt              : out std_logic:= '0';
      o_id_blt              : out std_logic:= '0';
      o_id_bge              : out std_logic:= '0';
      o_id_ble              : out std_logic:= '0';
      o_id_bne              : out std_logic:= '0';

      o_id_setmaskeq        : out std_logic:= '0';
      o_id_setmaskgt        : out std_logic:= '0';
      o_id_setmasklt        : out std_logic:= '0';
      o_id_setmaskge        : out std_logic:= '0';
      o_id_setmaskle        : out std_logic:= '0';
      o_id_setmaskne        : out std_logic:= '0';

      o_id_alusra           : out std_logic:= '0';
      o_id_CA_absdiff       : out std_logic:= '0';
      o_id_CA_absdiff_clr   : out std_logic:= '0'
    );
  end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in definations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.sFPE_typedef.all;
use work.sFPE_inst_encoding.all;

entity sFPE_ID is
  generic(
    DATA_WIDTH       : integer:= 16;
    DATA_TYPE        : integer:= 1;
    SLICE_NUM        : integer:= 1;
    RF_ADDR_WIDTH    : integer:= 5;
    OPCODE_WIDTH     : integer:= 6;
    PM_ADDR_WIDTH    : integer:= 6;
    OPM_NUM          : integer:= 1;
    ALUM_NUM         : integer:= 1;
    FLEXA_TYPE       : integer:= 1;
    FLEXB_TYPE       : integer:= 1;
    FLEXC_TYPE       : integer:= 1;
    BSLAVE           : boolean:= false;
    BMASTER          : boolean:= false;
    BMASTER_NUM      : integer:= 1;
    BRANCH_EN        : boolean:= false;
    JMP_EN           : boolean:= false;
    RPT_EN           : boolean:= false;
    RF_EN            : boolean:= false;
    DM_EN            : boolean:= false;
    DM_TWO_RD_PORTS  : boolean:= false;
    SM_EN            : boolean:= false;
    GETCH_EN         : boolean:= false;
    PUTCH_EN         : boolean:= false;
    MASKEQ_EN        : boolean:= false;
    MASKGT_EN        : boolean:= false;
    MASKLT_EN        : boolean:= false;
    MASKGE_EN        : boolean:= false;
    MASKLE_EN        : boolean:= false;
    MASKNE_EN        : boolean:= false;
    ALUSRA_EN        : boolean:= false;
    ABSDIFF_EN       : boolean:= false;
    ABSDIFF_WITHACCUM: boolean:= false
  );
  port(
    clk                   : in std_logic;
    i_pm_do               : in std_logic_vector(31 downto 0);
    o_id_opmode           : out std_logic_vector(7*OPM_NUM-1 downto 0);
    o_id_alumode          : out std_logic_vector(4*ALUM_NUM-1 downto 0);
    -- Control signals
    i_ext_barrier         : in  std_logic:= '0'; -- from external master sFPE
    o_en_pc               : out std_logic;
    o_ext_en_sFPE          : out std_logic;
    o_ext_id_barrier      : out std_logic_vector(BMASTER_NUM-1 downto 0);
    i_ext_en_sFPE          : in  std_logic:= '1'; -- from external slave sFPE

    -- component signals
    o_id_get_or_peak0: out std_logic:= '0';
    o_id_get_or_peak1: out std_logic:= '0';
    o_id_get0        : out std_logic:= '0';
    o_id_get1        : out std_logic:= '0';
    o_id_fifowrite        : out std_logic:= '0';
    o_id_rx_autoinc       : out std_logic:= '0';
    o_id_rx_reset         : out std_logic:= '0';
    o_id_tx_autoinc       : out std_logic:= '0';
    o_id_tx_reset         : out std_logic:= '0';

    o_id_rddm0            : out std_logic:= '0';
    o_id_rddm1            : out std_logic:= '0';
    o_id_wrdm             : out std_logic:= '0';
    o_id_dm_set_rb_m0     : out std_logic:= '0';
    o_id_dm_set_rb_m1     : out std_logic:= '0';
    o_id_dm_set_rb_n0     : out std_logic:= '0';
    o_id_dm_set_rb_n1     : out std_logic:= '0';
    o_id_dm_inc_rb_m0     : out std_logic:= '0';
    o_id_dm_inc_rb_m1     : out std_logic:= '0';
    o_id_dm_inc_rb_n0     : out std_logic:= '0';
    o_id_dm_inc_rb_n1     : out std_logic:= '0';
    o_id_dm_autoinc_rb_m  : out std_logic:= '0';
    o_id_dm_autoinc_rb_n  : out std_logic:= '0';
    o_id_dm_set_wb_0      : out std_logic:= '0';
    o_id_dm_set_wb_1      : out std_logic:= '0';
    o_id_dm_inc_wb_0      : out std_logic:= '0';
    o_id_dm_inc_wb_1      : out std_logic:= '0';
    o_id_dm_autoinc_wb    : out std_logic:= '0';

    o_id_sm_set_rb_0      : out std_logic:= '0';
    o_id_sm_inc_rb_0      : out std_logic:= '0';
    o_id_sm_set_wb_0      : out std_logic:= '0';
    o_id_sm_inc_wb_0      : out std_logic:= '0';
    o_id_sm_autoinc_rb    : out std_logic:= '0';
    o_id_sm_autoinc_wb    : out std_logic:= '0';
    o_id_sm_wen           : out std_logic:= '0';
    o_id_rdsm             : out std_logic:= '0';

    o_id_rf_wen           : out std_logic:= '0';

    o_id_b                : out std_logic:= '0';
    o_id_rpt              : out std_logic:= '0';
    o_id_beq              : out std_logic:= '0';
    o_id_bgt              : out std_logic:= '0';
    o_id_blt              : out std_logic:= '0';
    o_id_bge              : out std_logic:= '0';
    o_id_ble              : out std_logic:= '0';
    o_id_bne              : out std_logic:= '0';

    o_id_setmaskeq        : out std_logic:= '0';
    o_id_setmaskgt        : out std_logic:= '0';
    o_id_setmasklt        : out std_logic:= '0';
    o_id_setmaskge        : out std_logic:= '0';
    o_id_setmaskle        : out std_logic:= '0';
    o_id_setmaskne        : out std_logic:= '0';

    o_id_alusra           : out std_logic:= '0';
    o_id_CA_absdiff       : out std_logic:= '0';
    o_id_CA_absdiff_clr   : out std_logic:= '0'
  );
end entity;

architecture structure of sFPE_ID is

  signal  opc        : std_logic_vector(OPCODE_WIDTH-1 downto 0);
  signal  dm_aibits     : std_logic_vector(2 downto 0) := (others=>'0');
  signal  sm_aibits     : std_logic_vector(1 downto 0) := (others=>'0');
  signal  fifo_aibits     : std_logic_vector(1 downto 0) := (others=>'0');
  signal  id_rddm0,id_rddm1  : std_logic := '0';
  signal  id_wrdm   : std_logic := '0';

  signal  id_rdsm : std_logic := '0';
  signal  id_wrsm : std_logic := '0';

  signal  id_get_or_peak0 : std_logic := '0';
  signal  id_fifowrite : std_logic := '0';

  signal  id_rx_autoinc : std_logic := '0';
  signal  id_rx_reset : std_logic := '0';
  signal  id_tx_autoinc : std_logic := '0';
  signal  id_tx_reset : std_logic := '0';

  -- Help functions
  function setPutAtMemRd0 return integer is
    variable default : integer := 2**OPCODE_WIDTH-1;
  begin
    if (DM_TWO_RD_PORTS = false) then
      default := to_integer(unsigned(PUT_FXXM));
    end if;
    return default;
  end function setPutAtMemRd0;

  function setPutAtMemRd1 return integer is
    variable default : integer := 2**OPCODE_WIDTH-1;
  begin
    if (DM_TWO_RD_PORTS = true) then
      default := to_integer(unsigned(PUT_FXXM));
    end if;
    return default;
  end function setPutAtMemRd1;

  constant putAtMemRd0 : std_logic_vector(OPCODE_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(setPutAtMemRd0, OPCODE_WIDTH));
  constant putAtMemRd1 : std_logic_vector(OPCODE_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(setPutAtMemRd1, OPCODE_WIDTH));
begin
  opc <= i_pm_do(31 downto 32-OPCODE_WIDTH);
  dm_aibits(2) <= i_pm_do(16);

  G0: if ((FLEXA_TYPE/2)rem 2) = 1 generate
    dm_aibits(1) <= i_pm_do(11);
  end generate;

  G1: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
    dm_aibits(1) <= i_pm_do(6);
  end generate;

  G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 and ((FLEXC_TYPE/2)rem 2) = 1 generate
    dm_aibits(1) <= i_pm_do(1);
  end generate;

  G3: if ((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
    dm_aibits(0) <= i_pm_do(6);
  end generate;

  G4: if (((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1 and ((FLEXC_TYPE/2)rem 2) = 1)
    or (((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXC_TYPE/2)rem 2) = 1)
  generate
     dm_aibits(0) <= i_pm_do(1);
  end generate;

  sm_aibits(1) <= i_pm_do(16);

  GS0: if ((FLEXA_TYPE/4)rem 2) = 1 generate
    sm_aibits(0) <= i_pm_do(11);
  end generate;

  GS1: if ((FLEXA_TYPE/4)rem 2) /= 1 and ((FLEXB_TYPE/4)rem 2) = 1 generate
    sm_aibits(0) <= i_pm_do(6);
  end generate;

  GS2: if ((FLEXA_TYPE/4)rem 2) /= 1 and ((FLEXB_TYPE/4)rem 2) /= 1 and ((FLEXC_TYPE/4)rem 2) = 1 generate
    sm_aibits(0) <= i_pm_do(1);
  end generate;

  fifo_aibits(1) <= i_pm_do(16);
  GR0: if ((FLEXA_TYPE/8)rem 2) = 1 generate
    fifo_aibits(0) <= i_pm_do(11);
  end generate;
  GR1: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) = 1 generate
    fifo_aibits(0) <= i_pm_do(6);
  end generate;
  GR2: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 and ((FLEXC_TYPE/8)rem 2) = 1 generate
    fifo_aibits(0) <= i_pm_do(1);
  end generate;

  -- rf_wen
  id_rf_en_gen: if RF_EN = true generate
    o_id_rf_wen <= '1' when
      opc = ADDMUL_RRRR or opc = ADDMUL_RRRM or opc = ADDMUL_RRRI or
      opc = ADDMUL_RRRF or opc = ADDMUL_RRRP or opc = ADDMUL_RRMR or
      opc = ADDMUL_RRMM or opc = ADDMUL_RRMI or opc = ADDMUL_RRMF or
      opc = ADDMUL_RRMP or opc = ADDMUL_RRIR or opc = ADDMUL_RRIM or
      opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or opc = ADDMUL_RRFR or
      opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or opc = ADDMUL_RRFF or
      opc = ADDMUL_RRFP or opc = ADDMUL_RRPR or opc = ADDMUL_RRPM or
      opc = ADDMUL_RRPI or opc = ADDMUL_RRPF or opc = ADDMUL_RRPP or
      opc = ADDMUL_RMRR or opc = ADDMUL_RMRM or opc = ADDMUL_RMRI or
      opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or opc = ADDMUL_RMMR or
      -- rf_wen
      opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
      opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or opc = ADDMUL_RMIF or
      opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
      opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
      opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
      opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRR or
      opc = ADDMUL_RIRM or opc = ADDMUL_RIRF or opc = ADDMUL_RIRP or
      opc = ADDMUL_RIMR or opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or
      opc = ADDMUL_RIMP or opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or
      opc = ADDMUL_RIFF or opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or
      opc = ADDMUL_RIPM or opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or
      opc = ADDMUL_RFRR or opc = ADDMUL_RFRM or opc = ADDMUL_RFRI or
      opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or opc = ADDMUL_RFMR or
      opc = ADDMUL_RFMM or opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or
      opc = ADDMUL_RFMP or opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or
      opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or opc = ADDMUL_RFFR or
      opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or opc = ADDMUL_RFPR or
      opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or opc = ADDMUL_RPRR or
      opc = ADDMUL_RPRM or opc = ADDMUL_RPRI or opc = ADDMUL_RPRF or
      opc = ADDMUL_RPRP or opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or
      opc = ADDMUL_RPMI or opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or
      opc = ADDMUL_RPIR or opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or
      opc = ADDMUL_RPIP or opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or
      opc = ADDMUL_RPFI or opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or
      opc = ADDMUL_RPPI or
      opc = SUBMUL_RRRR or opc = SUBMUL_RRRM or opc = SUBMUL_RRRI or
      opc = SUBMUL_RRRF or opc = SUBMUL_RRRP or opc = SUBMUL_RRMR or
      opc = SUBMUL_RRMM or opc = SUBMUL_RRMI or opc = SUBMUL_RRMF or
      opc = SUBMUL_RRMP or opc = SUBMUL_RRIR or opc = SUBMUL_RRIM or
      opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or opc = SUBMUL_RRFR or
      opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or opc = SUBMUL_RRFF or
      opc = SUBMUL_RRFP or opc = SUBMUL_RRPR or opc = SUBMUL_RRPM or
      opc = SUBMUL_RRPI or opc = SUBMUL_RRPF or opc = SUBMUL_RRPP or
      opc = SUBMUL_RMRR or opc = SUBMUL_RMRM or opc = SUBMUL_RMRI or
      opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or opc = SUBMUL_RMMR or
      opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
      opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or opc = SUBMUL_RMIF or
      opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
      -- rf_wen
      opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
      opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
      opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRR or
      opc = SUBMUL_RIRM or opc = SUBMUL_RIRF or opc = SUBMUL_RIRP or
      opc = SUBMUL_RIMR or opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or
      opc = SUBMUL_RIMP or opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or
      opc = SUBMUL_RIFF or opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or
      opc = SUBMUL_RIPM or opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or
      opc = SUBMUL_RFRR or opc = SUBMUL_RFRM or opc = SUBMUL_RFRI or
      opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or opc = SUBMUL_RFMR or
      opc = SUBMUL_RFMM or opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or
      opc = SUBMUL_RFMP or opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or
      opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or opc = SUBMUL_RFFR or
      opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or opc = SUBMUL_RFPR or
      opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or opc = SUBMUL_RPRR or
      opc = SUBMUL_RPRM or opc = SUBMUL_RPRI or opc = SUBMUL_RPRF or
      opc = SUBMUL_RPRP or opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or
      opc = SUBMUL_RPMI or opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or
      opc = SUBMUL_RPIR or opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or
      opc = SUBMUL_RPIP or opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or
      opc = SUBMUL_RPFI or opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or
      -- rf_wen
      opc = SUBMUL_RPPI or
      opc = ADDMULFWD_RRRX or opc = ADDMULFWD_RRMX or opc = ADDMULFWD_RRIX or
      opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RRPX or opc = ADDMULFWD_RMRX or
      opc = ADDMULFWD_RMMX or opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RMFX or
      opc = ADDMULFWD_RMPX or opc = ADDMULFWD_RIRX or opc = ADDMULFWD_RIMX or
      opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or opc = ADDMULFWD_RFRX or
      opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or opc = ADDMULFWD_RFFX or
      opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPRX or opc = ADDMULFWD_RPMX or
      opc = ADDMULFWD_RPIX or opc = ADDMULFWD_RPFX or opc = ADDMULFWD_RPPX or
      opc = SUBMULFWD_RRRX or opc = SUBMULFWD_RRMX or opc = SUBMULFWD_RRIX or
      opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RRPX or opc = SUBMULFWD_RMRX or
      opc = SUBMULFWD_RMMX or opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RMFX or
      opc = SUBMULFWD_RMPX or opc = SUBMULFWD_RIRX or opc = SUBMULFWD_RIMX or
      opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or opc = SUBMULFWD_RFRX or
      opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or opc = SUBMULFWD_RFFX or
      opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPRX or opc = SUBMULFWD_RPMX or
      opc = SUBMULFWD_RPIX or opc = SUBMULFWD_RPFX or opc = SUBMULFWD_RPPX or
      opc = ADDMULSRA_RRRR or opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRRI or
      opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMR or
      opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or
      opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIR or opc = ADDMULSRA_RRIM or
      opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or opc = ADDMULSRA_RRFR or
      opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRFF or
      opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or opc = ADDMULSRA_RRPM or
      opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RRPP or
      opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
      opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
      opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
      opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
      opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
      opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
      opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
      opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRR or
      opc = ADDMULSRA_RIRM or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or
      opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
      opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or
      opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or
      opc = ADDMULSRA_RIPM or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
      opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or
      opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or
      opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or
      -- rf_wen
      opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
      opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or
      opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or
      opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or
      opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or
      opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
      opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
      opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
      opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or
      opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or
      opc = ADDMULSRA_RPPI or
      opc = SUBMULSRA_RRRR or opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRRI or
      opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMR or
      opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or
      opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIR or opc = SUBMULSRA_RRIM or
      opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or opc = SUBMULSRA_RRFR or
      opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRFF or
      opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or opc = SUBMULSRA_RRPM or
      opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RRPP or
      opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
      opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
      opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
      opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
      opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
      opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
      opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
      opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRR or
      opc = SUBMULSRA_RIRM or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or
      opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
      opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or
      opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or
      opc = SUBMULSRA_RIPM or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
      opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or
      opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or
      opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or
      opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
      opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or
      opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or
      opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or
      -- rf_wen
      opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or
      opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
      opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
      opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
      opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or
      opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or
      opc = SUBMULSRA_RPPI or
      opc = ABSDIFF_RXRR or opc = ABSDIFF_RXRM or opc = ABSDIFF_RXRI or
      opc = ABSDIFF_RXRF or opc = ABSDIFF_RXRP or opc = ABSDIFF_RXMR or
      opc = ABSDIFF_RXMM or opc = ABSDIFF_RXMI or opc = ABSDIFF_RXMF or
      opc = ABSDIFF_RXMP or opc = ABSDIFF_RXIR or opc = ABSDIFF_RXIM or
      opc = ABSDIFF_RXIF or opc = ABSDIFF_RXIP or opc = ABSDIFF_RXFR or
      opc = ABSDIFF_RXFM or opc = ABSDIFF_RXFI or opc = ABSDIFF_RXFF or
      opc = ABSDIFF_RXFP or opc = ABSDIFF_RXPR or opc = ABSDIFF_RXPM or
      opc = ABSDIFF_RXPI or opc = ABSDIFF_RXPF or opc = ABSDIFF_RXPP or
      opc = ABSDIFFACCUM_RXRR or opc = ABSDIFFACCUM_RXRM or opc = ABSDIFFACCUM_RXRI or
      opc = ABSDIFFACCUM_RXRF or opc = ABSDIFFACCUM_RXRP or opc = ABSDIFFACCUM_RXMR or
      opc = ABSDIFFACCUM_RXMM or opc = ABSDIFFACCUM_RXMI or opc = ABSDIFFACCUM_RXMF or
      opc = ABSDIFFACCUM_RXMP or opc = ABSDIFFACCUM_RXIR or opc = ABSDIFFACCUM_RXIM or
      opc = ABSDIFFACCUM_RXIF or opc = ABSDIFFACCUM_RXIP or opc = ABSDIFFACCUM_RXFR or
      opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXFI or opc = ABSDIFFACCUM_RXFF or
      opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_RXPR or opc = ABSDIFFACCUM_RXPM or
      opc = ABSDIFFACCUM_RXPI or opc = ABSDIFFACCUM_RXPF or opc = ABSDIFFACCUM_RXPP or
      opc = GET_RXXF or
      opc = DECONST_RXXR or opc = DECONST_RXXM or opc = DECONST_RXXI or
      opc = DECONST_RXXF or opc = DECONST_RXXP or
      opc = UNLDSORT_RXXX or
      opc = CLR_RXXX
    else '0';
  end generate;

  -- dm rw
  o_id_rddm0  <= id_rddm0;
  o_id_rddm1  <= id_rddm1;
  o_id_wrdm  <=  id_wrdm;

  id_mem_rw_gen:
  if DM_EN = true generate
  begin
    id_rddm0 <= '1' when
      opc = ADDMUL_RRRM or opc = ADDMUL_RRMR or opc = ADDMUL_RRMM or
      opc = ADDMUL_RRMI or opc = ADDMUL_RRMF or opc = ADDMUL_RRMP or
      opc = ADDMUL_RRIM or opc = ADDMUL_RRFM or opc = ADDMUL_RRPM or
      opc = ADDMUL_RMRR or opc = ADDMUL_RMRM or opc = ADDMUL_RMRI or
      opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or opc = ADDMUL_RMMR or
      opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
      opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or opc = ADDMUL_RMIF or
      opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
      opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
      opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
      opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRM or
      opc = ADDMUL_RIMR or opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or
      opc = ADDMUL_RIMP or opc = ADDMUL_RIFM or opc = ADDMUL_RIPM or
      opc = ADDMUL_RFRM or opc = ADDMUL_RFMR or opc = ADDMUL_RFMM or
      opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or opc = ADDMUL_RFMP or
      opc = ADDMUL_RFIM or opc = ADDMUL_RFFM or opc = ADDMUL_RFPM or
      opc = ADDMUL_RPRM or opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or
      opc = ADDMUL_RPMI or opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or
      opc = ADDMUL_RPIM or opc = ADDMUL_RPFM or opc = ADDMUL_RPPM or
      opc = ADDMUL_MRRM or opc = ADDMUL_MRMR or opc = ADDMUL_MRMM or
      opc = ADDMUL_MRMI or opc = ADDMUL_MRMF or opc = ADDMUL_MRMP or
      opc = ADDMUL_MRIM or opc = ADDMUL_MRFM or opc = ADDMUL_MRPM or
      -- dm read0
      opc = ADDMUL_MMRR or opc = ADDMUL_MMRM or opc = ADDMUL_MMRI or
      opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or opc = ADDMUL_MMMR or
      opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or opc = ADDMUL_MMMP or
      opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or opc = ADDMUL_MMIF or
      opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or opc = ADDMUL_MMFM or
      opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or opc = ADDMUL_MMFP or
      opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or opc = ADDMUL_MMPI or
      opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or opc = ADDMUL_MIRM or
      opc = ADDMUL_MIMR or opc = ADDMUL_MIMM or opc = ADDMUL_MIMF or
      opc = ADDMUL_MIMP or opc = ADDMUL_MIFM or opc = ADDMUL_MIPM or
      opc = ADDMUL_MFRM or opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or
      opc = ADDMUL_MFMI or opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or
      opc = ADDMUL_MFIM or opc = ADDMUL_MFFM or opc = ADDMUL_MFPM or
      opc = ADDMUL_MPRM or opc = ADDMUL_MPMR or opc = ADDMUL_MPMM or
      opc = ADDMUL_MPMI or opc = ADDMUL_MPMF or opc = ADDMUL_MPMP or
      opc = ADDMUL_MPIM or opc = ADDMUL_MPFM or opc = ADDMUL_MPPM or
      opc = ADDMUL_FRRM or opc = ADDMUL_FRMR or opc = ADDMUL_FRMM or
      opc = ADDMUL_FRMI or opc = ADDMUL_FRMF or opc = ADDMUL_FRMP or
      opc = ADDMUL_FRIM or opc = ADDMUL_FRFM or opc = ADDMUL_FRPM or
      opc = ADDMUL_FMRR or opc = ADDMUL_FMRM or opc = ADDMUL_FMRI or
      opc = ADDMUL_FMRF or opc = ADDMUL_FMRP or opc = ADDMUL_FMMR or
      opc = ADDMUL_FMMI or opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or
      opc = ADDMUL_FMIR or opc = ADDMUL_FMIM or opc = ADDMUL_FMIF or
      opc = ADDMUL_FMIP or opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or
      opc = ADDMUL_FMFI or opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or
      opc = ADDMUL_FMPR or opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or
      opc = ADDMUL_FMPF or opc = ADDMUL_FMPP or opc = ADDMUL_FIRM or
      opc = ADDMUL_FIMR or opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or
      opc = ADDMUL_FIMP or opc = ADDMUL_FIFM or opc = ADDMUL_FIPM or
      opc = ADDMUL_FFRM or opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or
      opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or
      opc = ADDMUL_FFIM or opc = ADDMUL_FFFM or opc = ADDMUL_FFPM or
      opc = ADDMUL_FPRM or opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or
      opc = ADDMUL_FPMI or opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or
      opc = ADDMUL_FPIM or opc = ADDMUL_FPFM or opc = ADDMUL_FPPM or
      opc = SUBMUL_RRRM or opc = SUBMUL_RRMR or opc = SUBMUL_RRMM or
      opc = SUBMUL_RRMI or opc = SUBMUL_RRMF or opc = SUBMUL_RRMP or
      opc = SUBMUL_RRIM or opc = SUBMUL_RRFM or opc = SUBMUL_RRPM or
      opc = SUBMUL_RMRR or opc = SUBMUL_RMRM or opc = SUBMUL_RMRI or
      -- dm read0
      opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or opc = SUBMUL_RMMR or
      opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
      opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or opc = SUBMUL_RMIF or
      opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
      opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
      opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
      opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRM or
      opc = SUBMUL_RIMR or opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or
      opc = SUBMUL_RIMP or opc = SUBMUL_RIFM or opc = SUBMUL_RIPM or
      opc = SUBMUL_RFRM or opc = SUBMUL_RFMR or opc = SUBMUL_RFMM or
      opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or opc = SUBMUL_RFMP or
      opc = SUBMUL_RFIM or opc = SUBMUL_RFFM or opc = SUBMUL_RFPM or
      opc = SUBMUL_RPRM or opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or
      opc = SUBMUL_RPMI or opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or
      opc = SUBMUL_RPIM or opc = SUBMUL_RPFM or opc = SUBMUL_RPPM or
      opc = SUBMUL_MRRM or opc = SUBMUL_MRMR or opc = SUBMUL_MRMM or
      opc = SUBMUL_MRMI or opc = SUBMUL_MRMF or opc = SUBMUL_MRMP or
      opc = SUBMUL_MRIM or opc = SUBMUL_MRFM or opc = SUBMUL_MRPM or
      opc = SUBMUL_MMRR or opc = SUBMUL_MMRM or opc = SUBMUL_MMRI or
      opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or opc = SUBMUL_MMMR or
      opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or opc = SUBMUL_MMMP or
      opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or opc = SUBMUL_MMIF or
      opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or opc = SUBMUL_MMFM or
      opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or opc = SUBMUL_MMFP or
      opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or opc = SUBMUL_MMPI or
      opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or opc = SUBMUL_MIRM or
      opc = SUBMUL_MIMR or opc = SUBMUL_MIMM or opc = SUBMUL_MIMF or
      opc = SUBMUL_MIMP or opc = SUBMUL_MIFM or opc = SUBMUL_MIPM or
      opc = SUBMUL_MFRM or opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or
      opc = SUBMUL_MFMI or opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or
      opc = SUBMUL_MFIM or opc = SUBMUL_MFFM or opc = SUBMUL_MFPM or
      opc = SUBMUL_MPRM or opc = SUBMUL_MPMR or opc = SUBMUL_MPMM or
      opc = SUBMUL_MPMI or opc = SUBMUL_MPMF or opc = SUBMUL_MPMP or
      opc = SUBMUL_MPIM or opc = SUBMUL_MPFM or opc = SUBMUL_MPPM or
      opc = SUBMUL_FRRM or opc = SUBMUL_FRMR or opc = SUBMUL_FRMM or
      opc = SUBMUL_FRMI or opc = SUBMUL_FRMF or opc = SUBMUL_FRMP or
      -- dm read0
      opc = SUBMUL_FRIM or opc = SUBMUL_FRFM or opc = SUBMUL_FRPM or
      opc = SUBMUL_FMRR or opc = SUBMUL_FMRM or opc = SUBMUL_FMRI or
      opc = SUBMUL_FMRF or opc = SUBMUL_FMRP or opc = SUBMUL_FMMR or
      opc = SUBMUL_FMMI or opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or
      opc = SUBMUL_FMIR or opc = SUBMUL_FMIM or opc = SUBMUL_FMIF or
      opc = SUBMUL_FMIP or opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or
      opc = SUBMUL_FMFI or opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or
      opc = SUBMUL_FMPR or opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or
      opc = SUBMUL_FMPF or opc = SUBMUL_FMPP or opc = SUBMUL_FIRM or
      opc = SUBMUL_FIMR or opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or
      opc = SUBMUL_FIMP or opc = SUBMUL_FIFM or opc = SUBMUL_FIPM or
      opc = SUBMUL_FFRM or opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or
      opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or
      opc = SUBMUL_FFIM or opc = SUBMUL_FFFM or opc = SUBMUL_FFPM or
      opc = SUBMUL_FPRM or opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or
      opc = SUBMUL_FPMI or opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or
      opc = SUBMUL_FPIM or opc = SUBMUL_FPFM or opc = SUBMUL_FPPM or
      opc = ADDMULFWD_RRMX or opc = ADDMULFWD_RMRX or opc = ADDMULFWD_RMMX or
      opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RMFX or opc = ADDMULFWD_RMPX or
      opc = ADDMULFWD_RIMX or opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RPMX or
      opc = ADDMULFWD_MRMX or opc = ADDMULFWD_MMRX or opc = ADDMULFWD_MMMX or
      opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MMFX or opc = ADDMULFWD_MMPX or
      opc = ADDMULFWD_MIMX or opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MPMX or
      opc = ADDMULFWD_FRMX or opc = ADDMULFWD_FMRX or opc = ADDMULFWD_FMMX or
      opc = ADDMULFWD_FMIX or opc = ADDMULFWD_FMFX or opc = ADDMULFWD_FMPX or
      opc = ADDMULFWD_FIMX or opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FPMX or
      opc = SUBMULFWD_RRMX or opc = SUBMULFWD_RMRX or opc = SUBMULFWD_RMMX or
      opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RMFX or opc = SUBMULFWD_RMPX or
      -- dm read0
      opc = SUBMULFWD_RIMX or opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RPMX or
      opc = SUBMULFWD_MRMX or opc = SUBMULFWD_MMRX or opc = SUBMULFWD_MMMX or
      opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MMFX or opc = SUBMULFWD_MMPX or
      opc = SUBMULFWD_MIMX or opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MPMX or
      opc = SUBMULFWD_FRMX or opc = SUBMULFWD_FMRX or opc = SUBMULFWD_FMMX or
      opc = SUBMULFWD_FMIX or opc = SUBMULFWD_FMFX or opc = SUBMULFWD_FMPX or
      opc = SUBMULFWD_FIMX or opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FPMX or
      opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRMR or opc = ADDMULSRA_RRMM or
      opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or opc = ADDMULSRA_RRMP or
      opc = ADDMULSRA_RRIM or opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRPM or
      opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
      opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
      opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
      opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
      opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
      opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
      opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
      opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRM or
      opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
      opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFM or opc = ADDMULSRA_RIPM or
      opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFMR or opc = ADDMULSRA_RFMM or
      opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or opc = ADDMULSRA_RFMP or
      opc = ADDMULSRA_RFIM or opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFPM or
      opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
      opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
      opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPFM or opc = ADDMULSRA_RPPM or
      opc = ADDMULSRA_MRRM or opc = ADDMULSRA_MRMR or opc = ADDMULSRA_MRMM or
      opc = ADDMULSRA_MRMI or opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRMP or
      opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRPM or
      opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or opc = ADDMULSRA_MMRI or
      opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or opc = ADDMULSRA_MMMR or
      opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or opc = ADDMULSRA_MMMP or
      opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or opc = ADDMULSRA_MMIF or
      opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or opc = ADDMULSRA_MMFM or
      opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or opc = ADDMULSRA_MMFP or
      opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or opc = ADDMULSRA_MMPI or
      opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or opc = ADDMULSRA_MIRM or
      opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or opc = ADDMULSRA_MIMF or
      opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIPM or
      opc = ADDMULSRA_MFRM or opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or
      -- dm read0
      opc = ADDMULSRA_MFMI or opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or
      opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFPM or
      opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPMR or opc = ADDMULSRA_MPMM or
      opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or opc = ADDMULSRA_MPMP or
      opc = ADDMULSRA_MPIM or opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPPM or
      opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRMR or opc = ADDMULSRA_FRMM or
      opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRMP or
      opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRFM or opc = ADDMULSRA_FRPM or
      opc = ADDMULSRA_FMRR or opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or
      opc = ADDMULSRA_FMRF or opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or
      opc = ADDMULSRA_FMMI or opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or
      opc = ADDMULSRA_FMIR or opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or
      opc = ADDMULSRA_FMIP or opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or
      opc = ADDMULSRA_FMFI or opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or
      opc = ADDMULSRA_FMPR or opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or
      opc = ADDMULSRA_FMPF or opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRM or
      opc = ADDMULSRA_FIMR or opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or
      opc = ADDMULSRA_FIMP or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIPM or
      opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
      opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
      opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFFM or opc = ADDMULSRA_FFPM or
      opc = ADDMULSRA_FPRM or opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or
      opc = ADDMULSRA_FPMI or opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or
      opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPPM or
      opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRMR or opc = SUBMULSRA_RRMM or
      opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or opc = SUBMULSRA_RRMP or
      opc = SUBMULSRA_RRIM or opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRPM or
      opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
      opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
      opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
      opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
      opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
      opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
      opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
      opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRM or
      -- dm read0
      opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
      opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFM or opc = SUBMULSRA_RIPM or
      opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFMR or opc = SUBMULSRA_RFMM or
      opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or opc = SUBMULSRA_RFMP or
      opc = SUBMULSRA_RFIM or opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFPM or
      opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
      opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
      opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPFM or opc = SUBMULSRA_RPPM or
      opc = SUBMULSRA_MRRM or opc = SUBMULSRA_MRMR or opc = SUBMULSRA_MRMM or
      opc = SUBMULSRA_MRMI or opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRMP or
      opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRPM or
      opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or opc = SUBMULSRA_MMRI or
      opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or opc = SUBMULSRA_MMMR or
      opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or opc = SUBMULSRA_MMMP or
      opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or opc = SUBMULSRA_MMIF or
      opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or opc = SUBMULSRA_MMFM or
      opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or opc = SUBMULSRA_MMFP or
      opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or opc = SUBMULSRA_MMPI or
      opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or opc = SUBMULSRA_MIRM or
      opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or opc = SUBMULSRA_MIMF or
      opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIPM or
      opc = SUBMULSRA_MFRM or opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or
      opc = SUBMULSRA_MFMI or opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or
      opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFPM or
      opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPMR or opc = SUBMULSRA_MPMM or
      opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or opc = SUBMULSRA_MPMP or
      opc = SUBMULSRA_MPIM or opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPPM or
      opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRMR or opc = SUBMULSRA_FRMM or
      opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRMP or
      opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRFM or opc = SUBMULSRA_FRPM or
      opc = SUBMULSRA_FMRR or opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or
      opc = SUBMULSRA_FMRF or opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or
      -- dm read0
      opc = SUBMULSRA_FMMI or opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or
      opc = SUBMULSRA_FMIR or opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or
      opc = SUBMULSRA_FMIP or opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or
      opc = SUBMULSRA_FMFI or opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or
      opc = SUBMULSRA_FMPR or opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or
      opc = SUBMULSRA_FMPF or opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRM or
      opc = SUBMULSRA_FIMR or opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or
      opc = SUBMULSRA_FIMP or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIPM or
      opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
      opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
      opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFFM or opc = SUBMULSRA_FFPM or
      opc = SUBMULSRA_FPRM or opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or
      opc = SUBMULSRA_FPMI or opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or
      opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPPM or
      opc = ABSDIFF_RXRM or opc = ABSDIFF_RXMR or opc = ABSDIFF_RXMM or
      opc = ABSDIFF_RXMI or opc = ABSDIFF_RXMF or opc = ABSDIFF_RXMP or
      opc = ABSDIFF_RXIM or opc = ABSDIFF_RXFM or opc = ABSDIFF_RXPM or
      opc = ABSDIFF_MXRM or opc = ABSDIFF_MXMR or opc = ABSDIFF_MXMM or
      opc = ABSDIFF_MXMI or opc = ABSDIFF_MXMF or opc = ABSDIFF_MXMP or
      opc = ABSDIFF_MXIM or opc = ABSDIFF_MXFM or opc = ABSDIFF_MXPM or
      opc = ABSDIFF_FXRM or opc = ABSDIFF_FXMR or opc = ABSDIFF_FXMM or
      opc = ABSDIFF_FXMI or opc = ABSDIFF_FXMF or opc = ABSDIFF_FXMP or
      opc = ABSDIFF_FXIM or opc = ABSDIFF_FXFM or opc = ABSDIFF_FXPM or
      opc = ABSDIFFACCUM_RXRM or opc = ABSDIFFACCUM_RXMR or opc = ABSDIFFACCUM_RXMM or
      opc = ABSDIFFACCUM_RXMI or opc = ABSDIFFACCUM_RXMF or opc = ABSDIFFACCUM_RXMP or
      opc = ABSDIFFACCUM_RXIM or opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXPM or
      opc = ABSDIFFACCUM_MXRM or opc = ABSDIFFACCUM_MXMR or opc = ABSDIFFACCUM_MXMM or
      opc = ABSDIFFACCUM_MXMI or opc = ABSDIFFACCUM_MXMF or opc = ABSDIFFACCUM_MXMP or
      opc = ABSDIFFACCUM_MXIM or opc = ABSDIFFACCUM_MXFM or opc = ABSDIFFACCUM_MXPM or
      opc = ABSDIFFACCUM_FXRM or opc = ABSDIFFACCUM_FXMR or opc = ABSDIFFACCUM_FXMM or
      opc = ABSDIFFACCUM_FXMI or opc = ABSDIFFACCUM_FXMF or opc = ABSDIFFACCUM_FXMP or
      opc = ABSDIFFACCUM_FXIM or opc = ABSDIFFACCUM_FXFM or opc = ABSDIFFACCUM_FXPM or
      opc = ABSDIFFACCUM_XXRM or opc = ABSDIFFACCUM_XXMR or opc = ABSDIFFACCUM_XXMM or
      opc = ABSDIFFACCUM_XXMI or opc = ABSDIFFACCUM_XXMF or opc = ABSDIFFACCUM_XXMP or
      opc = ABSDIFFACCUM_XXIM or opc = ABSDIFFACCUM_XXFM or opc = ABSDIFFACCUM_XXPM or
      -- dm read0
      opc = CMP_XXRM or opc = CMP_XXMR or opc = CMP_XXMM or
      opc = CMP_XXMI or opc = CMP_XXMF or opc = CMP_XXMP or
      opc = CMP_XXIM or opc = CMP_XXFM or opc = CMP_XXPM or
      opc = CMPFWD_XXMX or
      opc = DECONST_RXXM or opc = DECONST_MXXM or opc = DECONST_FXXM or
      opc = LDSORT_XXXM or
      opc = putAtMemRd0 or
      opc = SETMASKLT_XXRM or opc = SETMASKLT_XXMR or opc = SETMASKLT_XXMM or
      opc = SETMASKLT_XXMI or opc = SETMASKLT_XXMF or opc = SETMASKLT_XXMP or
      opc = SETMASKLT_XXIM or opc = SETMASKLT_XXFM or opc = SETMASKLT_XXPM or
      opc = SETMASKGT_XXRM or opc = SETMASKGT_XXMR or opc = SETMASKGT_XXMM or
      opc = SETMASKGT_XXMI or opc = SETMASKGT_XXMF or opc = SETMASKGT_XXMP or
      opc = SETMASKGT_XXIM or opc = SETMASKGT_XXFM or opc = SETMASKGT_XXPM or
      opc = SETMASKEQ_XXRM or opc = SETMASKEQ_XXMR or opc = SETMASKEQ_XXMM or
      opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXMF or opc = SETMASKEQ_XXMP or
      opc = SETMASKEQ_XXIM or opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXPM or
      opc = SETMASKGE_XXRM or opc = SETMASKGE_XXMR or opc = SETMASKGE_XXMM or
      opc = SETMASKGE_XXMI or opc = SETMASKGE_XXMF or opc = SETMASKGE_XXMP or
      opc = SETMASKGE_XXIM or opc = SETMASKGE_XXFM or opc = SETMASKGE_XXPM or
      opc = SETMASKLE_XXRM or opc = SETMASKLE_XXMR or opc = SETMASKLE_XXMM or
      -- dm read0
      opc = SETMASKLE_XXMI or opc = SETMASKLE_XXMF or opc = SETMASKLE_XXMP or
      opc = SETMASKLE_XXIM or opc = SETMASKLE_XXFM or opc = SETMASKLE_XXPM or
      opc = SETMASKNE_XXRM or opc = SETMASKNE_XXMR or opc = SETMASKNE_XXMM or
      opc = SETMASKNE_XXMI or opc = SETMASKNE_XXMF or opc = SETMASKNE_XXMP or
      opc = SETMASKNE_XXIM or opc = SETMASKNE_XXFM or opc = SETMASKNE_XXPM
    else '0';

    id_rddm1 <= '1' when
      opc = ADDMUL_RRMM or opc = ADDMUL_RMRM or opc = ADDMUL_RMMR or
      opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
      opc = ADDMUL_RMIM or opc = ADDMUL_RMFM or opc = ADDMUL_RMPM or
      opc = ADDMUL_RIMM or opc = ADDMUL_RFMM or opc = ADDMUL_RPMM or
      opc = ADDMUL_MRMM or opc = ADDMUL_MMRM or opc = ADDMUL_MMMR or
      opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or opc = ADDMUL_MMMP or
      opc = ADDMUL_MMIM or opc = ADDMUL_MMFM or opc = ADDMUL_MMPM or
      opc = ADDMUL_MIMM or opc = ADDMUL_MFMM or opc = ADDMUL_MPMM or
      opc = ADDMUL_FRMM or opc = ADDMUL_FMRM or opc = ADDMUL_FMMR or
      opc = ADDMUL_FMMI or opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or
      opc = ADDMUL_FMIM or opc = ADDMUL_FMFM or opc = ADDMUL_FMPM or
      opc = ADDMUL_FIMM or opc = ADDMUL_FFMM or opc = ADDMUL_FPMM or
      opc = SUBMUL_RRMM or opc = SUBMUL_RMRM or opc = SUBMUL_RMMR or
      opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
      opc = SUBMUL_RMIM or opc = SUBMUL_RMFM or opc = SUBMUL_RMPM or
      opc = SUBMUL_RIMM or opc = SUBMUL_RFMM or opc = SUBMUL_RPMM or
      opc = SUBMUL_MRMM or opc = SUBMUL_MMRM or opc = SUBMUL_MMMR or
      opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or opc = SUBMUL_MMMP or
      opc = SUBMUL_MMIM or opc = SUBMUL_MMFM or opc = SUBMUL_MMPM or
      -- dm read1
      opc = SUBMUL_MIMM or opc = SUBMUL_MFMM or opc = SUBMUL_MPMM or
      opc = SUBMUL_FRMM or opc = SUBMUL_FMRM or opc = SUBMUL_FMMR or
      opc = SUBMUL_FMMI or opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or
      opc = SUBMUL_FMIM or opc = SUBMUL_FMFM or opc = SUBMUL_FMPM or
      opc = SUBMUL_FIMM or opc = SUBMUL_FFMM or opc = SUBMUL_FPMM or
      opc = ADDMULFWD_RMMX or opc = ADDMULFWD_MMMX or opc = ADDMULFWD_FMMX or
      opc = SUBMULFWD_RMMX or opc = SUBMULFWD_MMMX or opc = SUBMULFWD_FMMX or
      opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMMR or
      opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
      opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMFM or opc = ADDMULSRA_RMPM or
      opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RPMM or
      opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MMRM or opc = ADDMULSRA_MMMR or
      opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or opc = ADDMULSRA_MMMP or
      opc = ADDMULSRA_MMIM or opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMPM or
      opc = ADDMULSRA_MIMM or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MPMM or
      opc = ADDMULSRA_FRMM or opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMMR or
      opc = ADDMULSRA_FMMI or opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or
      opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMPM or
      opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FFMM or opc = ADDMULSRA_FPMM or
      opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMMR or
      opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
      opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMFM or opc = SUBMULSRA_RMPM or
      opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RPMM or
      opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MMRM or opc = SUBMULSRA_MMMR or
      opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or opc = SUBMULSRA_MMMP or
      opc = SUBMULSRA_MMIM or opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMPM or
      opc = SUBMULSRA_MIMM or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MPMM or
      opc = SUBMULSRA_FRMM or opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMMR or
      opc = SUBMULSRA_FMMI or opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or
      -- dm read1
      opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMPM or
      opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FFMM or opc = SUBMULSRA_FPMM or
      opc = ABSDIFF_RXMM or opc = ABSDIFF_MXMM or opc = ABSDIFF_FXMM or
      opc = ABSDIFFACCUM_RXMM or opc = ABSDIFFACCUM_MXMM or opc = ABSDIFFACCUM_FXMM or
      opc = ABSDIFFACCUM_XXMM or
      opc = putAtMemRd1 or
      opc = CMP_XXMM or
      opc = SETMASKLT_XXMM or
      opc = SETMASKGT_XXMM or
      opc = SETMASKEQ_XXMM or
      opc = SETMASKGE_XXMM or
      opc = SETMASKLE_XXMM or
      opc = SETMASKNE_XXMM
    else '0';

    id_wrdm <= '1' when
      opc = ADDMUL_MRRR or opc = ADDMUL_MRRM or opc = ADDMUL_MRRI or
      opc = ADDMUL_MRRF or opc = ADDMUL_MRRP or opc = ADDMUL_MRMR or
      opc = ADDMUL_MRMM or opc = ADDMUL_MRMI or opc = ADDMUL_MRMF or
      opc = ADDMUL_MRMP or opc = ADDMUL_MRIR or opc = ADDMUL_MRIM or
      opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or opc = ADDMUL_MRFR or
      opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or opc = ADDMUL_MRFF or
      opc = ADDMUL_MRFP or opc = ADDMUL_MRPR or opc = ADDMUL_MRPM or
      opc = ADDMUL_MRPI or opc = ADDMUL_MRPF or opc = ADDMUL_MRPP or
      opc = ADDMUL_MMRR or opc = ADDMUL_MMRM or opc = ADDMUL_MMRI or
      opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or opc = ADDMUL_MMMR or
      opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or opc = ADDMUL_MMMP or
      opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or opc = ADDMUL_MMIF or
      opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or opc = ADDMUL_MMFM or
      opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or opc = ADDMUL_MMFP or
      opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or opc = ADDMUL_MMPI or
      opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or opc = ADDMUL_MIRR or
      -- dm write0
      opc = ADDMUL_MIRM or opc = ADDMUL_MIRF or opc = ADDMUL_MIRP or
      opc = ADDMUL_MIMR or opc = ADDMUL_MIMM or opc = ADDMUL_MIMF or
      opc = ADDMUL_MIMP or opc = ADDMUL_MIFR or opc = ADDMUL_MIFM or
      opc = ADDMUL_MIFF or opc = ADDMUL_MIFP or opc = ADDMUL_MIPR or
      opc = ADDMUL_MIPM or opc = ADDMUL_MIPF or opc = ADDMUL_MIPP or
      opc = ADDMUL_MFRR or opc = ADDMUL_MFRM or opc = ADDMUL_MFRI or
      opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or opc = ADDMUL_MFMR or
      opc = ADDMUL_MFMM or opc = ADDMUL_MFMI or opc = ADDMUL_MFMF or
      opc = ADDMUL_MFMP or opc = ADDMUL_MFIR or opc = ADDMUL_MFIM or
      opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or opc = ADDMUL_MFFR or
      opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or opc = ADDMUL_MFPR or
      opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or opc = ADDMUL_MPRR or
      opc = ADDMUL_MPRM or opc = ADDMUL_MPRI or opc = ADDMUL_MPRF or
      opc = ADDMUL_MPRP or opc = ADDMUL_MPMR or opc = ADDMUL_MPMM or
      opc = ADDMUL_MPMI or opc = ADDMUL_MPMF or opc = ADDMUL_MPMP or
      opc = ADDMUL_MPIR or opc = ADDMUL_MPIM or opc = ADDMUL_MPIF or
      opc = ADDMUL_MPIP or opc = ADDMUL_MPFR or opc = ADDMUL_MPFM or
      opc = ADDMUL_MPFI or opc = ADDMUL_MPPR or opc = ADDMUL_MPPM or
      opc = ADDMUL_MPPI or
      opc = SUBMUL_MRRR or opc = SUBMUL_MRRM or opc = SUBMUL_MRRI or
      opc = SUBMUL_MRRF or opc = SUBMUL_MRRP or opc = SUBMUL_MRMR or
      opc = SUBMUL_MRMM or opc = SUBMUL_MRMI or opc = SUBMUL_MRMF or
      opc = SUBMUL_MRMP or opc = SUBMUL_MRIR or opc = SUBMUL_MRIM or
      opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or opc = SUBMUL_MRFR or
      opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or opc = SUBMUL_MRFF or
      opc = SUBMUL_MRFP or opc = SUBMUL_MRPR or opc = SUBMUL_MRPM or
      opc = SUBMUL_MRPI or opc = SUBMUL_MRPF or opc = SUBMUL_MRPP or
      opc = SUBMUL_MMRR or opc = SUBMUL_MMRM or opc = SUBMUL_MMRI or
      opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or opc = SUBMUL_MMMR or
      opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or opc = SUBMUL_MMMP or
      opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or opc = SUBMUL_MMIF or
      opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or opc = SUBMUL_MMFM or
      opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or opc = SUBMUL_MMFP or
      opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or opc = SUBMUL_MMPI or
      -- dm write0
      opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or opc = SUBMUL_MIRR or
      opc = SUBMUL_MIRM or opc = SUBMUL_MIRF or opc = SUBMUL_MIRP or
      opc = SUBMUL_MIMR or opc = SUBMUL_MIMM or opc = SUBMUL_MIMF or
      opc = SUBMUL_MIMP or opc = SUBMUL_MIFR or opc = SUBMUL_MIFM or
      opc = SUBMUL_MIFF or opc = SUBMUL_MIFP or opc = SUBMUL_MIPR or
      opc = SUBMUL_MIPM or opc = SUBMUL_MIPF or opc = SUBMUL_MIPP or
      opc = SUBMUL_MFRR or opc = SUBMUL_MFRM or opc = SUBMUL_MFRI or
      opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or opc = SUBMUL_MFMR or
      opc = SUBMUL_MFMM or opc = SUBMUL_MFMI or opc = SUBMUL_MFMF or
      opc = SUBMUL_MFMP or opc = SUBMUL_MFIR or opc = SUBMUL_MFIM or
      opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or opc = SUBMUL_MFFR or
      opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or opc = SUBMUL_MFPR or
      opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or opc = SUBMUL_MPRR or
      opc = SUBMUL_MPRM or opc = SUBMUL_MPRI or opc = SUBMUL_MPRF or
      opc = SUBMUL_MPRP or opc = SUBMUL_MPMR or opc = SUBMUL_MPMM or
      opc = SUBMUL_MPMI or opc = SUBMUL_MPMF or opc = SUBMUL_MPMP or
      opc = SUBMUL_MPIR or opc = SUBMUL_MPIM or opc = SUBMUL_MPIF or
      opc = SUBMUL_MPIP or opc = SUBMUL_MPFR or opc = SUBMUL_MPFM or
      opc = SUBMUL_MPFI or opc = SUBMUL_MPPR or opc = SUBMUL_MPPM or
      opc = SUBMUL_MPPI or
      opc = ADDMULFWD_MRRX or opc = ADDMULFWD_MRMX or opc = ADDMULFWD_MRIX or
      opc = ADDMULFWD_MRFX or opc = ADDMULFWD_MRPX or opc = ADDMULFWD_MMRX or
      opc = ADDMULFWD_MMMX or opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MMFX or
      opc = ADDMULFWD_MMPX or opc = ADDMULFWD_MIRX or opc = ADDMULFWD_MIMX or
      opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFRX or
      opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or
      opc = ADDMULFWD_MFPX or opc = ADDMULFWD_MPRX or opc = ADDMULFWD_MPMX or
      opc = ADDMULFWD_MPIX or opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or
      opc = SUBMULFWD_MRRX or opc = SUBMULFWD_MRMX or opc = SUBMULFWD_MRIX or
      opc = SUBMULFWD_MRFX or opc = SUBMULFWD_MRPX or opc = SUBMULFWD_MMRX or
      -- dm write0
      opc = SUBMULFWD_MMMX or opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MMFX or
      opc = SUBMULFWD_MMPX or opc = SUBMULFWD_MIRX or opc = SUBMULFWD_MIMX or
      opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFRX or
      opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or
      opc = SUBMULFWD_MFPX or opc = SUBMULFWD_MPRX or opc = SUBMULFWD_MPMX or
      opc = SUBMULFWD_MPIX or opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or
      opc = ADDMULSRA_MRRR or opc = ADDMULSRA_MRRM or opc = ADDMULSRA_MRRI or
      opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or opc = ADDMULSRA_MRMR or
      opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MRMI or opc = ADDMULSRA_MRMF or
      opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIR or opc = ADDMULSRA_MRIM or
      opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or opc = ADDMULSRA_MRFR or
      opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or opc = ADDMULSRA_MRFF or
      opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or opc = ADDMULSRA_MRPM or
      opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or opc = ADDMULSRA_MRPP or
      opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or opc = ADDMULSRA_MMRI or
      opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or opc = ADDMULSRA_MMMR or
      opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or opc = ADDMULSRA_MMMP or
      opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or opc = ADDMULSRA_MMIF or
      opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or opc = ADDMULSRA_MMFM or
      opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or opc = ADDMULSRA_MMFP or
      opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or opc = ADDMULSRA_MMPI or
      opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or opc = ADDMULSRA_MIRR or
      opc = ADDMULSRA_MIRM or opc = ADDMULSRA_MIRF or opc = ADDMULSRA_MIRP or
      opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or opc = ADDMULSRA_MIMF or
      opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFR or opc = ADDMULSRA_MIFM or
      opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIFP or opc = ADDMULSRA_MIPR or
      opc = ADDMULSRA_MIPM or opc = ADDMULSRA_MIPF or opc = ADDMULSRA_MIPP or
      opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or opc = ADDMULSRA_MFRI or
      opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or opc = ADDMULSRA_MFMR or
      opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or opc = ADDMULSRA_MFMF or
      opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or opc = ADDMULSRA_MFIM or
      opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or opc = ADDMULSRA_MFFR or
      opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or opc = ADDMULSRA_MFPR or
      opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or opc = ADDMULSRA_MPRR or
      opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPRI or opc = ADDMULSRA_MPRF or
      -- dm write0
      opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMR or opc = ADDMULSRA_MPMM or
      opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or opc = ADDMULSRA_MPMP or
      opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or opc = ADDMULSRA_MPIF or
      opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFR or opc = ADDMULSRA_MPFM or
      opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPR or opc = ADDMULSRA_MPPM or
      opc = ADDMULSRA_MPPI or
      opc = SUBMULSRA_MRRR or opc = SUBMULSRA_MRRM or opc = SUBMULSRA_MRRI or
      opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or opc = SUBMULSRA_MRMR or
      opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MRMI or opc = SUBMULSRA_MRMF or
      opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIR or opc = SUBMULSRA_MRIM or
      opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or opc = SUBMULSRA_MRFR or
      opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or opc = SUBMULSRA_MRFF or
      opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or opc = SUBMULSRA_MRPM or
      opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or opc = SUBMULSRA_MRPP or
      opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or opc = SUBMULSRA_MMRI or
      opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or opc = SUBMULSRA_MMMR or
      opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or opc = SUBMULSRA_MMMP or
      opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or opc = SUBMULSRA_MMIF or
      opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or opc = SUBMULSRA_MMFM or
      opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or opc = SUBMULSRA_MMFP or
      opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or opc = SUBMULSRA_MMPI or
      opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or opc = SUBMULSRA_MIRR or
      opc = SUBMULSRA_MIRM or opc = SUBMULSRA_MIRF or opc = SUBMULSRA_MIRP or
      opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or opc = SUBMULSRA_MIMF or
      opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFR or opc = SUBMULSRA_MIFM or
      opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIFP or opc = SUBMULSRA_MIPR or
      opc = SUBMULSRA_MIPM or opc = SUBMULSRA_MIPF or opc = SUBMULSRA_MIPP or
      opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or opc = SUBMULSRA_MFRI or
      opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or opc = SUBMULSRA_MFMR or
      opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or opc = SUBMULSRA_MFMF or
      opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or opc = SUBMULSRA_MFIM or
      opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or opc = SUBMULSRA_MFFR or
      opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or opc = SUBMULSRA_MFPR or
      opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or opc = SUBMULSRA_MPRR or
      opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPRI or opc = SUBMULSRA_MPRF or
      -- dm write0
      opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMR or opc = SUBMULSRA_MPMM or
      opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or opc = SUBMULSRA_MPMP or
      opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or opc = SUBMULSRA_MPIF or
      opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFR or opc = SUBMULSRA_MPFM or
      opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPR or opc = SUBMULSRA_MPPM or
      opc = SUBMULSRA_MPPI or
      opc = ABSDIFF_MXRR or opc = ABSDIFF_MXRM or opc = ABSDIFF_MXRI or
      opc = ABSDIFF_MXRF or opc = ABSDIFF_MXRP or opc = ABSDIFF_MXMR or
      opc = ABSDIFF_MXMM or opc = ABSDIFF_MXMI or opc = ABSDIFF_MXMF or
      opc = ABSDIFF_MXMP or opc = ABSDIFF_MXIR or opc = ABSDIFF_MXIM or
      opc = ABSDIFF_MXIF or opc = ABSDIFF_MXIP or opc = ABSDIFF_MXFR or
      opc = ABSDIFF_MXFM or opc = ABSDIFF_MXFI or opc = ABSDIFF_MXFF or
      opc = ABSDIFF_MXFP or opc = ABSDIFF_MXPR or opc = ABSDIFF_MXPM or
      opc = ABSDIFF_MXPI or opc = ABSDIFF_MXPF or opc = ABSDIFF_MXPP or
      opc = ABSDIFFACCUM_MXRR or opc = ABSDIFFACCUM_MXRM or opc = ABSDIFFACCUM_MXRI or
      opc = ABSDIFFACCUM_MXRF or opc = ABSDIFFACCUM_MXRP or opc = ABSDIFFACCUM_MXMR or
      opc = ABSDIFFACCUM_MXMM or opc = ABSDIFFACCUM_MXMI or opc = ABSDIFFACCUM_MXMF or
      opc = ABSDIFFACCUM_MXMP or opc = ABSDIFFACCUM_MXIR or opc = ABSDIFFACCUM_MXIM or
      opc = ABSDIFFACCUM_MXIF or opc = ABSDIFFACCUM_MXIP or opc = ABSDIFFACCUM_MXFR or
      opc = ABSDIFFACCUM_MXFM or opc = ABSDIFFACCUM_MXFI or opc = ABSDIFFACCUM_MXFF or
      opc = ABSDIFFACCUM_MXFP or opc = ABSDIFFACCUM_MXPR or opc = ABSDIFFACCUM_MXPM or
      opc = ABSDIFFACCUM_MXPI or opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_MXPP or
      opc = GET_MXXF or
      opc = DECONST_MXXR or opc = DECONST_MXXM or opc = DECONST_MXXI or
      opc = DECONST_MXXF or opc = DECONST_MXXP or
      opc = UNLDSORT_MXXX or
      opc = CLR_MXXX
    else '0';

    o_id_dm_set_rb_m0 <= '1' when (opc = SETDMRB_M0) else '0';
    o_id_dm_set_rb_m1 <= '1' when (opc = SETDMRB_M1) else '0';
    o_id_dm_set_rb_n0 <= '1' when (opc = SETDMRB_N0) else '0';
    o_id_dm_set_rb_n1 <= '1' when (opc = SETDMRB_N1) else '0';
    o_id_dm_set_wb_0  <= '1' when (opc = SETDMWB_0)  else '0';
    o_id_dm_set_wb_1  <= '1' when (opc = SETDMWB_1)  else '0';

    o_id_dm_inc_rb_m0 <= '1' when (opc = INCDMRB_M0 or opc = INCDMRB_ALL) else '0';
    o_id_dm_inc_rb_m1 <= '1' when (opc = INCDMRB_M1) else '0';
    o_id_dm_inc_rb_n0 <= '1' when (opc = INCDMRB_N0 or opc = INCDMRB_ALL) else '0';
    o_id_dm_inc_rb_n1 <= '1' when (opc = INCDMRB_N1 or opc = INCDMRB_ALL) else '0';
    o_id_dm_inc_wb_0  <= '1' when (opc = INCDMWB_0)  else '0';
    o_id_dm_inc_wb_1  <= '1' when (opc = INCDMWB_1)  else '0';

    o_id_dm_autoinc_rb_m <= '1' when id_rddm0 = '1' and dm_aibits(1) = '1' else '0';
    o_id_dm_autoinc_rb_n <= '1' when id_rddm1 = '1' and dm_aibits(0) = '1' else '0';
    o_id_dm_autoinc_wb <= '1'   when id_wrdm = '1' and dm_aibits(2) = '1' else '0';
  end generate;

  -- barrier master
  o_ext_id_barrier <= i_pm_do(BMASTER_NUM-1 downto 0) when (opc = BARRIERM) else (others=>'0');

  -- sm rw
  o_id_rdsm  <=  id_rdsm;
  o_id_sm_wen <= id_wrsm;

  id_sm_gen:if SM_EN = true generate
  begin
    o_id_sm_set_rb_0 <= '1' when (opc = SETSMRB_0) else '0';
    o_id_sm_set_wb_0 <= '1' when (opc = SETSMWB_0) else '0';

    o_id_sm_inc_rb_0 <= '1' when (opc = INCSMRB_0) else '0';
    o_id_sm_inc_wb_0 <= '1' when (opc = INCSMWB_0) else '0';

    o_id_sm_autoinc_rb <= '1' when id_rdsm = '1' and sm_aibits(0) = '1' else '0';
    o_id_sm_autoinc_wb <= '1' when id_wrsm = '1' and sm_aibits(1) = '1' else '0';

    id_rdsm <= '1' when
      opc = ADDMUL_RRRI or opc = ADDMUL_RRMI or opc = ADDMUL_RRIR or
      opc = ADDMUL_RRIM or opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or
      opc = ADDMUL_RRFI or opc = ADDMUL_RRPI or opc = ADDMUL_RMRI or
      opc = ADDMUL_RMMI or opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or
      opc = ADDMUL_RMIF or opc = ADDMUL_RMIP or opc = ADDMUL_RMFI or
      opc = ADDMUL_RMPI or opc = ADDMUL_RIRR or opc = ADDMUL_RIRM or
      opc = ADDMUL_RIRF or opc = ADDMUL_RIRP or opc = ADDMUL_RIMR or
      opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or opc = ADDMUL_RIMP or
      opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or opc = ADDMUL_RIFF or
      opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or opc = ADDMUL_RIPM or
      opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or opc = ADDMUL_RFRI or
      opc = ADDMUL_RFMI or opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or
      opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or opc = ADDMUL_RFFI or
      opc = ADDMUL_RFPI or opc = ADDMUL_RPRI or opc = ADDMUL_RPMI or
      opc = ADDMUL_RPIR or opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or
      opc = ADDMUL_RPIP or opc = ADDMUL_RPFI or opc = ADDMUL_RPPI or
      opc = ADDMUL_MRRI or opc = ADDMUL_MRMI or opc = ADDMUL_MRIR or
      opc = ADDMUL_MRIM or opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or
      opc = ADDMUL_MRFI or opc = ADDMUL_MRPI or opc = ADDMUL_MMRI or
      opc = ADDMUL_MMMI or opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or
      opc = ADDMUL_MMIF or opc = ADDMUL_MMIP or opc = ADDMUL_MMFI or
      opc = ADDMUL_MMPI or opc = ADDMUL_MIRR or opc = ADDMUL_MIRM or
      opc = ADDMUL_MIRF or opc = ADDMUL_MIRP or opc = ADDMUL_MIMR or
      opc = ADDMUL_MIMM or opc = ADDMUL_MIMF or opc = ADDMUL_MIMP or
      opc = ADDMUL_MIFR or opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or
      opc = ADDMUL_MIFP or opc = ADDMUL_MIPR or opc = ADDMUL_MIPM or
      opc = ADDMUL_MIPF or opc = ADDMUL_MIPP or opc = ADDMUL_MFRI or
      opc = ADDMUL_MFMI or opc = ADDMUL_MFIR or opc = ADDMUL_MFIM or
      opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or opc = ADDMUL_MFFI or
      opc = ADDMUL_MFPI or opc = ADDMUL_MPRI or opc = ADDMUL_MPMI or
      opc = ADDMUL_MPIR or opc = ADDMUL_MPIM or opc = ADDMUL_MPIF or
      opc = ADDMUL_MPIP or opc = ADDMUL_MPFI or opc = ADDMUL_MPPI or
      -- sm read
      opc = ADDMUL_FRRI or opc = ADDMUL_FRMI or opc = ADDMUL_FRIR or
      opc = ADDMUL_FRIM or opc = ADDMUL_FRIF or opc = ADDMUL_FRIP or
      opc = ADDMUL_FRFI or opc = ADDMUL_FRPI or opc = ADDMUL_FMRI or
      opc = ADDMUL_FMMI or opc = ADDMUL_FMIR or opc = ADDMUL_FMIM or
      opc = ADDMUL_FMIF or opc = ADDMUL_FMIP or opc = ADDMUL_FMFI or
      opc = ADDMUL_FMPI or opc = ADDMUL_FIRR or opc = ADDMUL_FIRM or
      opc = ADDMUL_FIRF or opc = ADDMUL_FIRP or opc = ADDMUL_FIMR or
      opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or opc = ADDMUL_FIMP or
      opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
      opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or opc = ADDMUL_FIPM or
      opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or opc = ADDMUL_FFRI or
      opc = ADDMUL_FFMI or opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or
      opc = ADDMUL_FFIF or opc = ADDMUL_FFIP or opc = ADDMUL_FFFI or
      opc = ADDMUL_FFPI or opc = ADDMUL_FPRI or opc = ADDMUL_FPMI or
      opc = ADDMUL_FPIR or opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or
      opc = ADDMUL_FPIP or opc = ADDMUL_FPFI or opc = ADDMUL_FPPI or
      opc = SUBMUL_RRRI or opc = SUBMUL_RRMI or opc = SUBMUL_RRIR or
      opc = SUBMUL_RRIM or opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or
      opc = SUBMUL_RRFI or opc = SUBMUL_RRPI or opc = SUBMUL_RMRI or
      opc = SUBMUL_RMMI or opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or
      opc = SUBMUL_RMIF or opc = SUBMUL_RMIP or opc = SUBMUL_RMFI or
      opc = SUBMUL_RMPI or opc = SUBMUL_RIRR or opc = SUBMUL_RIRM or
      opc = SUBMUL_RIRF or opc = SUBMUL_RIRP or opc = SUBMUL_RIMR or
      opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or opc = SUBMUL_RIMP or
      opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or opc = SUBMUL_RIFF or
      opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or opc = SUBMUL_RIPM or
      opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or opc = SUBMUL_RFRI or
      opc = SUBMUL_RFMI or opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or
      opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or opc = SUBMUL_RFFI or
      opc = SUBMUL_RFPI or opc = SUBMUL_RPRI or opc = SUBMUL_RPMI or
      opc = SUBMUL_RPIR or opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or
      opc = SUBMUL_RPIP or opc = SUBMUL_RPFI or opc = SUBMUL_RPPI or
      opc = SUBMUL_MRRI or opc = SUBMUL_MRMI or opc = SUBMUL_MRIR or
      opc = SUBMUL_MRIM or opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or
      opc = SUBMUL_MRFI or opc = SUBMUL_MRPI or opc = SUBMUL_MMRI or
      opc = SUBMUL_MMMI or opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or
      opc = SUBMUL_MMIF or opc = SUBMUL_MMIP or opc = SUBMUL_MMFI or
      opc = SUBMUL_MMPI or opc = SUBMUL_MIRR or opc = SUBMUL_MIRM or
      opc = SUBMUL_MIRF or opc = SUBMUL_MIRP or opc = SUBMUL_MIMR or
      opc = SUBMUL_MIMM or opc = SUBMUL_MIMF or opc = SUBMUL_MIMP or
      -- sm read
      opc = SUBMUL_MIFR or opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or
      opc = SUBMUL_MIFP or opc = SUBMUL_MIPR or opc = SUBMUL_MIPM or
      opc = SUBMUL_MIPF or opc = SUBMUL_MIPP or opc = SUBMUL_MFRI or
      opc = SUBMUL_MFMI or opc = SUBMUL_MFIR or opc = SUBMUL_MFIM or
      opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or opc = SUBMUL_MFFI or
      opc = SUBMUL_MFPI or opc = SUBMUL_MPRI or opc = SUBMUL_MPMI or
      opc = SUBMUL_MPIR or opc = SUBMUL_MPIM or opc = SUBMUL_MPIF or
      opc = SUBMUL_MPIP or opc = SUBMUL_MPFI or opc = SUBMUL_MPPI or
      opc = SUBMUL_FRRI or opc = SUBMUL_FRMI or opc = SUBMUL_FRIR or
      opc = SUBMUL_FRIM or opc = SUBMUL_FRIF or opc = SUBMUL_FRIP or
      opc = SUBMUL_FRFI or opc = SUBMUL_FRPI or opc = SUBMUL_FMRI or
      opc = SUBMUL_FMMI or opc = SUBMUL_FMIR or opc = SUBMUL_FMIM or
      opc = SUBMUL_FMIF or opc = SUBMUL_FMIP or opc = SUBMUL_FMFI or
      opc = SUBMUL_FMPI or opc = SUBMUL_FIRR or opc = SUBMUL_FIRM or
      opc = SUBMUL_FIRF or opc = SUBMUL_FIRP or opc = SUBMUL_FIMR or
      opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or opc = SUBMUL_FIMP or
      opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
      opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or opc = SUBMUL_FIPM or
      opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or opc = SUBMUL_FFRI or
      opc = SUBMUL_FFMI or opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or
      opc = SUBMUL_FFIF or opc = SUBMUL_FFIP or opc = SUBMUL_FFFI or
      opc = SUBMUL_FFPI or opc = SUBMUL_FPRI or opc = SUBMUL_FPMI or
      opc = SUBMUL_FPIR or opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or
      opc = SUBMUL_FPIP or opc = SUBMUL_FPFI or opc = SUBMUL_FPPI or
      -- sm read
      opc = ADDMULFWD_RRIX or opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RIRX or
      opc = ADDMULFWD_RIMX or opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or
      opc = ADDMULFWD_RFIX or opc = ADDMULFWD_RPIX or opc = ADDMULFWD_MRIX or
      opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MIRX or opc = ADDMULFWD_MIMX or
      opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFIX or
      opc = ADDMULFWD_MPIX or opc = ADDMULFWD_FRIX or opc = ADDMULFWD_FMIX or
      opc = ADDMULFWD_FIRX or opc = ADDMULFWD_FIMX or opc = ADDMULFWD_FIFX or
      opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FPIX or
      opc = SUBMULFWD_RRIX or opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RIRX or
      opc = SUBMULFWD_RIMX or opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or
      opc = SUBMULFWD_RFIX or opc = SUBMULFWD_RPIX or opc = SUBMULFWD_MRIX or
      opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MIRX or opc = SUBMULFWD_MIMX or
      opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFIX or
      opc = SUBMULFWD_MPIX or opc = SUBMULFWD_FRIX or opc = SUBMULFWD_FMIX or
      opc = SUBMULFWD_FIRX or opc = SUBMULFWD_FIMX or opc = SUBMULFWD_FIFX or
      opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FPIX or
      opc = ADDMULSRA_RRRI or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRIR or
      opc = ADDMULSRA_RRIM or opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or
      opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RMRI or
      opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or
      opc = ADDMULSRA_RMIF or opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFI or
      opc = ADDMULSRA_RMPI or opc = ADDMULSRA_RIRR or opc = ADDMULSRA_RIRM or
      opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or opc = ADDMULSRA_RIMR or
      opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or opc = ADDMULSRA_RIMP or
      opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or opc = ADDMULSRA_RIFF or
      -- sm read
      opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or opc = ADDMULSRA_RIPM or
      opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or opc = ADDMULSRA_RFRI or
      opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
      opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFI or
      opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPMI or
      opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
      opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPI or
      opc = ADDMULSRA_MRRI or opc = ADDMULSRA_MRMI or opc = ADDMULSRA_MRIR or
      opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
      opc = ADDMULSRA_MRFI or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MMRI or
      opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or
      opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFI or
      opc = ADDMULSRA_MMPI or opc = ADDMULSRA_MIRR or opc = ADDMULSRA_MIRM or
      opc = ADDMULSRA_MIRF or opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMR or
      opc = ADDMULSRA_MIMM or opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or
      opc = ADDMULSRA_MIFR or opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or
      opc = ADDMULSRA_MIFP or opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or
      opc = ADDMULSRA_MIPF or opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRI or
      opc = ADDMULSRA_MFMI or opc = ADDMULSRA_MFIR or opc = ADDMULSRA_MFIM or
      opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or opc = ADDMULSRA_MFFI or
      opc = ADDMULSRA_MFPI or opc = ADDMULSRA_MPRI or opc = ADDMULSRA_MPMI or
      opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or opc = ADDMULSRA_MPIF or
      opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPI or
      opc = ADDMULSRA_FRRI or opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRIR or
      opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRIF or opc = ADDMULSRA_FRIP or
      opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRPI or opc = ADDMULSRA_FMRI or
      opc = ADDMULSRA_FMMI or opc = ADDMULSRA_FMIR or opc = ADDMULSRA_FMIM or
      opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMIP or opc = ADDMULSRA_FMFI or
      opc = ADDMULSRA_FMPI or opc = ADDMULSRA_FIRR or opc = ADDMULSRA_FIRM or
      opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMR or
      opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
      opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
      opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
      opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRI or
      opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or
      opc = ADDMULSRA_FFIF or opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFI or
      opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPMI or
      -- sm read
      opc = ADDMULSRA_FPIR or opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or
      opc = ADDMULSRA_FPIP or opc = ADDMULSRA_FPFI or opc = ADDMULSRA_FPPI or
      opc = SUBMULSRA_RRRI or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRIR or
      opc = SUBMULSRA_RRIM or opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or
      opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RMRI or
      opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or
      opc = SUBMULSRA_RMIF or opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFI or
      opc = SUBMULSRA_RMPI or opc = SUBMULSRA_RIRR or opc = SUBMULSRA_RIRM or
      opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or opc = SUBMULSRA_RIMR or
      opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or opc = SUBMULSRA_RIMP or
      opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or opc = SUBMULSRA_RIFF or
      opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or opc = SUBMULSRA_RIPM or
      opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or opc = SUBMULSRA_RFRI or
      opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
      opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFI or
      opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPMI or
      opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
      opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPI or
      opc = SUBMULSRA_MRRI or opc = SUBMULSRA_MRMI or opc = SUBMULSRA_MRIR or
      opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
      opc = SUBMULSRA_MRFI or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MMRI or
      opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or
      opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFI or
      opc = SUBMULSRA_MMPI or opc = SUBMULSRA_MIRR or opc = SUBMULSRA_MIRM or
      opc = SUBMULSRA_MIRF or opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMR or
      opc = SUBMULSRA_MIMM or opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or
      opc = SUBMULSRA_MIFR or opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or
      opc = SUBMULSRA_MIFP or opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or
      opc = SUBMULSRA_MIPF or opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRI or
      opc = SUBMULSRA_MFMI or opc = SUBMULSRA_MFIR or opc = SUBMULSRA_MFIM or
      opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or opc = SUBMULSRA_MFFI or
      opc = SUBMULSRA_MFPI or opc = SUBMULSRA_MPRI or opc = SUBMULSRA_MPMI or
      -- sm read
      opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or opc = SUBMULSRA_MPIF or
      opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPI or
      opc = SUBMULSRA_FRRI or opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRIR or
      opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRIF or opc = SUBMULSRA_FRIP or
      opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRPI or opc = SUBMULSRA_FMRI or
      opc = SUBMULSRA_FMMI or opc = SUBMULSRA_FMIR or opc = SUBMULSRA_FMIM or
      opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMIP or opc = SUBMULSRA_FMFI or
      opc = SUBMULSRA_FMPI or opc = SUBMULSRA_FIRR or opc = SUBMULSRA_FIRM or
      opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMR or
      opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
      opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
      opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
      opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRI or
      opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or
      opc = SUBMULSRA_FFIF or opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFI or
      opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPMI or
      opc = SUBMULSRA_FPIR or opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or
      opc = SUBMULSRA_FPIP or opc = SUBMULSRA_FPFI or opc = SUBMULSRA_FPPI or
      opc = ABSDIFF_RXRI or opc = ABSDIFF_RXMI or opc = ABSDIFF_RXIR or
      opc = ABSDIFF_RXIM or opc = ABSDIFF_RXIF or opc = ABSDIFF_RXIP or
      opc = ABSDIFF_RXFI or opc = ABSDIFF_RXPI or opc = ABSDIFF_MXRI or
      opc = ABSDIFF_MXMI or opc = ABSDIFF_MXIR or opc = ABSDIFF_MXIM or
      opc = ABSDIFF_MXIF or opc = ABSDIFF_MXIP or opc = ABSDIFF_MXFI or
      opc = ABSDIFF_MXPI or opc = ABSDIFF_FXRI or opc = ABSDIFF_FXMI or
      opc = ABSDIFF_FXIR or opc = ABSDIFF_FXIM or opc = ABSDIFF_FXIF or
      opc = ABSDIFF_FXIP or opc = ABSDIFF_FXFI or opc = ABSDIFF_FXPI or
      -- sm read
      opc = ABSDIFFACCUM_RXRI or opc = ABSDIFFACCUM_RXMI or opc = ABSDIFFACCUM_RXIR or
      opc = ABSDIFFACCUM_RXIM or opc = ABSDIFFACCUM_RXIF or opc = ABSDIFFACCUM_RXIP or
      opc = ABSDIFFACCUM_RXFI or opc = ABSDIFFACCUM_RXPI or opc = ABSDIFFACCUM_MXRI or
      opc = ABSDIFFACCUM_MXMI or opc = ABSDIFFACCUM_MXIR or opc = ABSDIFFACCUM_MXIM or
      opc = ABSDIFFACCUM_MXIF or opc = ABSDIFFACCUM_MXIP or opc = ABSDIFFACCUM_MXFI or
      opc = ABSDIFFACCUM_MXPI or opc = ABSDIFFACCUM_FXRI or opc = ABSDIFFACCUM_FXMI or
      opc = ABSDIFFACCUM_FXIR or opc = ABSDIFFACCUM_FXIM or opc = ABSDIFFACCUM_FXIF or
      opc = ABSDIFFACCUM_FXIP or opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXPI or
      opc = ABSDIFFACCUM_XXRI or opc = ABSDIFFACCUM_XXMI or opc = ABSDIFFACCUM_XXIR or
      opc = ABSDIFFACCUM_XXIM or opc = ABSDIFFACCUM_XXIF or opc = ABSDIFFACCUM_XXIP or
      opc = ABSDIFFACCUM_XXFI or opc = ABSDIFFACCUM_XXPI or
      opc = CMP_XXRI or opc = CMP_XXMI or opc = CMP_XXIR or
      opc = CMP_XXIM or opc = CMP_XXIF or opc = CMP_XXIP or
      opc = CMP_XXFI or opc = CMP_XXPI or
      opc = CMPFWD_XXIX or
      opc = DECONST_RXXI or opc = DECONST_MXXI or opc = DECONST_FXXI or
      -- sm read
      opc = LDSORT_XXXI or
      opc = SETMASKLT_XXRI or opc = SETMASKLT_XXMI or opc = SETMASKLT_XXIR or
      opc = SETMASKLT_XXIM or opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or
      opc = SETMASKLT_XXFI or opc = SETMASKLT_XXPI or
      opc = SETMASKGT_XXRI or opc = SETMASKGT_XXMI or opc = SETMASKGT_XXIR or
      opc = SETMASKGT_XXIM or opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or
      opc = SETMASKGT_XXFI or opc = SETMASKGT_XXPI or
      opc = SETMASKEQ_XXRI or opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXIR or
      opc = SETMASKEQ_XXIM or opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or
      opc = SETMASKEQ_XXFI or opc = SETMASKEQ_XXPI or
      opc = SETMASKGE_XXRI or opc = SETMASKGE_XXMI or opc = SETMASKGE_XXIR or
      opc = SETMASKGE_XXIM or opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or
      opc = SETMASKGE_XXFI or opc = SETMASKGE_XXPI or
      opc = SETMASKLE_XXRI or opc = SETMASKLE_XXMI or opc = SETMASKLE_XXIR or
      opc = SETMASKLE_XXIM or opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or
      opc = SETMASKLE_XXFI or opc = SETMASKLE_XXPI or
      opc = SETMASKNE_XXRI or opc = SETMASKNE_XXMI or opc = SETMASKNE_XXIR or
      opc = SETMASKNE_XXIM or opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or
      opc = SETMASKNE_XXFI or opc = SETMASKNE_XXPI
    else '0';

    id_wrsm <= '1' when (opc = GET_IXXF or opc = CLR_IXXX) else '0';
  end generate;

  -- branch inst
  jmp_gen:
  if JMP_EN = true generate
    o_id_b <= '1' when (opc = JMP) else '0';
  end generate;

  rpt_gen:
  if RPT_EN = true generate
    o_id_rpt <= '1' when (opc = RPT) else '0';
  end generate;

  branch_gen: if BRANCH_EN = true generate
    o_id_beq <= '1' when (opc = BEQ) else '0';
    o_id_bgt <= '1' when (opc = BGT) else '0';
    o_id_blt <= '1' when (opc = BLT) else '0';
    o_id_bge <= '1' when (opc = BGE) else '0';
    o_id_ble <= '1' when (opc = BLE) else '0';
    o_id_bne <= '1' when (opc = BNE) else '0';
  end generate;

  --put/get inst
  o_id_get0  <= '1' when
    opc = ADDMUL_RRRF or opc = ADDMUL_RRMF or opc = ADDMUL_RRIF or
    opc = ADDMUL_RRFR or opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or
    opc = ADDMUL_RRFF or opc = ADDMUL_RRFP or opc = ADDMUL_RMRF or
    opc = ADDMUL_RMMF or opc = ADDMUL_RMIF or opc = ADDMUL_RMFR or
    opc = ADDMUL_RMFM or opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or
    opc = ADDMUL_RMFP or opc = ADDMUL_RIRF or opc = ADDMUL_RIMF or
    opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or opc = ADDMUL_RIFF or
    opc = ADDMUL_RIFP or opc = ADDMUL_RFRR or opc = ADDMUL_RFRM or
    opc = ADDMUL_RFRI or opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or
    opc = ADDMUL_RFMR or opc = ADDMUL_RFMM or opc = ADDMUL_RFMI or
    opc = ADDMUL_RFMF or opc = ADDMUL_RFMP or opc = ADDMUL_RFIR or
    opc = ADDMUL_RFIM or opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or
    opc = ADDMUL_RFFR or opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or
    opc = ADDMUL_RFPR or opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or
    opc = ADDMUL_MRRF or opc = ADDMUL_MRMF or opc = ADDMUL_MRIF or
    opc = ADDMUL_MRFR or opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or
    opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MMRF or
    opc = ADDMUL_MMMF or opc = ADDMUL_MMIF or opc = ADDMUL_MMFR or
    opc = ADDMUL_MMFM or opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or
    opc = ADDMUL_MMFP or opc = ADDMUL_MIRF or opc = ADDMUL_MIMF or
    opc = ADDMUL_MIFR or opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or
    opc = ADDMUL_MIFP or opc = ADDMUL_MFRR or opc = ADDMUL_MFRM or
    opc = ADDMUL_MFRI or opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or
    opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or opc = ADDMUL_MFMI or
    opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or opc = ADDMUL_MFIR or
    opc = ADDMUL_MFIM or opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or
    opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
    opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or
    opc = ADDMUL_FRRF or opc = ADDMUL_FRMF or opc = ADDMUL_FRIF or
    opc = ADDMUL_FRFR or opc = ADDMUL_FRFM or opc = ADDMUL_FRFI or
    opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or opc = ADDMUL_FMRF or
    opc = ADDMUL_FMMF or opc = ADDMUL_FMIF or opc = ADDMUL_FMFR or
    -- get0
    opc = ADDMUL_FMFM or opc = ADDMUL_FMFI or opc = ADDMUL_FMFF or
    opc = ADDMUL_FMFP or opc = ADDMUL_FIRF or opc = ADDMUL_FIMF or
    opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
    opc = ADDMUL_FIFP or opc = ADDMUL_FFRR or opc = ADDMUL_FFRM or
    opc = ADDMUL_FFRI or opc = ADDMUL_FFRF or opc = ADDMUL_FFRP or
    opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or opc = ADDMUL_FFMI or
    opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or opc = ADDMUL_FFIR or
    opc = ADDMUL_FFIM or opc = ADDMUL_FFIF or opc = ADDMUL_FFIP or
    opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or opc = ADDMUL_FFFI or
    opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or opc = ADDMUL_FFPI or
    opc = SUBMUL_RRRF or opc = SUBMUL_RRMF or opc = SUBMUL_RRIF or
    opc = SUBMUL_RRFR or opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or
    opc = SUBMUL_RRFF or opc = SUBMUL_RRFP or opc = SUBMUL_RMRF or
    opc = SUBMUL_RMMF or opc = SUBMUL_RMIF or opc = SUBMUL_RMFR or
    opc = SUBMUL_RMFM or opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or
    opc = SUBMUL_RMFP or opc = SUBMUL_RIRF or opc = SUBMUL_RIMF or
    opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or opc = SUBMUL_RIFF or
    opc = SUBMUL_RIFP or opc = SUBMUL_RFRR or opc = SUBMUL_RFRM or
    opc = SUBMUL_RFRI or opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or
    opc = SUBMUL_RFMR or opc = SUBMUL_RFMM or opc = SUBMUL_RFMI or
    opc = SUBMUL_RFMF or opc = SUBMUL_RFMP or opc = SUBMUL_RFIR or
    opc = SUBMUL_RFIM or opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or
    opc = SUBMUL_RFFR or opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or
    opc = SUBMUL_RFPR or opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or
    opc = SUBMUL_MRRF or opc = SUBMUL_MRMF or opc = SUBMUL_MRIF or
    opc = SUBMUL_MRFR or opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or
    opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MMRF or
    opc = SUBMUL_MMMF or opc = SUBMUL_MMIF or opc = SUBMUL_MMFR or
    opc = SUBMUL_MMFM or opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or
    opc = SUBMUL_MMFP or opc = SUBMUL_MIRF or opc = SUBMUL_MIMF or
    opc = SUBMUL_MIFR or opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or
    opc = SUBMUL_MIFP or opc = SUBMUL_MFRR or opc = SUBMUL_MFRM or
    opc = SUBMUL_MFRI or opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or
    opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or opc = SUBMUL_MFMI or
    opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or opc = SUBMUL_MFIR or
    opc = SUBMUL_MFIM or opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or
    opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
    opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or
    opc = SUBMUL_FRRF or opc = SUBMUL_FRMF or opc = SUBMUL_FRIF or
    opc = SUBMUL_FRFR or opc = SUBMUL_FRFM or opc = SUBMUL_FRFI or
    opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or opc = SUBMUL_FMRF or
    opc = SUBMUL_FMMF or opc = SUBMUL_FMIF or opc = SUBMUL_FMFR or
    opc = SUBMUL_FMFM or opc = SUBMUL_FMFI or opc = SUBMUL_FMFF or
    opc = SUBMUL_FMFP or opc = SUBMUL_FIRF or opc = SUBMUL_FIMF or
    opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
    opc = SUBMUL_FIFP or opc = SUBMUL_FFRR or opc = SUBMUL_FFRM or
    opc = SUBMUL_FFRI or opc = SUBMUL_FFRF or opc = SUBMUL_FFRP or
    opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or opc = SUBMUL_FFMI or
    opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or opc = SUBMUL_FFIR or
    opc = SUBMUL_FFIM or opc = SUBMUL_FFIF or opc = SUBMUL_FFIP or
    opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or opc = SUBMUL_FFFI or
    opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or opc = SUBMUL_FFPI or
    opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RMFX or opc = ADDMULFWD_RIFX or
    opc = ADDMULFWD_RFRX or opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or
    opc = ADDMULFWD_RFFX or opc = ADDMULFWD_RFPX or opc = ADDMULFWD_MRFX or
    opc = ADDMULFWD_MMFX or opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MFRX or
    opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or
    -- get0
    opc = ADDMULFWD_MFPX or opc = ADDMULFWD_FRFX or opc = ADDMULFWD_FMFX or
    opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FFRX or opc = ADDMULFWD_FFMX or
    opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or opc = ADDMULFWD_FFPX or
    opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RMFX or opc = SUBMULFWD_RIFX or
    opc = SUBMULFWD_RFRX or opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or
    opc = SUBMULFWD_RFFX or opc = SUBMULFWD_RFPX or opc = SUBMULFWD_MRFX or
    opc = SUBMULFWD_MMFX or opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MFRX or
    opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or
    opc = SUBMULFWD_MFPX or opc = SUBMULFWD_FRFX or opc = SUBMULFWD_FMFX or
    opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FFRX or opc = SUBMULFWD_FFMX or
    opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or opc = SUBMULFWD_FFPX or
    opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRMF or opc = ADDMULSRA_RRIF or
    opc = ADDMULSRA_RRFR or opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or
    opc = ADDMULSRA_RRFF or opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RMRF or
    opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMIF or opc = ADDMULSRA_RMFR or
    opc = ADDMULSRA_RMFM or opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or
    opc = ADDMULSRA_RMFP or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIMF or
    opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or opc = ADDMULSRA_RIFF or
    opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or
    opc = ADDMULSRA_RFRI or opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or
    opc = ADDMULSRA_RFMR or opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or
    opc = ADDMULSRA_RFMF or opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or
    opc = ADDMULSRA_RFIM or opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or
    opc = ADDMULSRA_RFFR or opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or
    opc = ADDMULSRA_RFPR or opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or
    opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRIF or
    opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
    opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MMRF or
    opc = ADDMULSRA_MMMF or opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMFR or
    opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or
    opc = ADDMULSRA_MMFP or opc = ADDMULSRA_MIRF or opc = ADDMULSRA_MIMF or
    opc = ADDMULSRA_MIFR or opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or
    opc = ADDMULSRA_MIFP or opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or
    opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or
    opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or
    opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or
    opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
    opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
    opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
    opc = ADDMULSRA_FRRF or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRIF or
    opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or opc = ADDMULSRA_FRFI or
    -- get0
    opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or opc = ADDMULSRA_FMRF or
    opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMFR or
    opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMFI or opc = ADDMULSRA_FMFF or
    opc = ADDMULSRA_FMFP or opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIMF or
    opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
    opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FFRR or opc = ADDMULSRA_FFRM or
    opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or opc = ADDMULSRA_FFRP or
    opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or opc = ADDMULSRA_FFMI or
    opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or opc = ADDMULSRA_FFIR or
    opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or opc = ADDMULSRA_FFIP or
    opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or opc = ADDMULSRA_FFFI or
    opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or opc = ADDMULSRA_FFPI or
    opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRMF or opc = SUBMULSRA_RRIF or
    opc = SUBMULSRA_RRFR or opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or
    opc = SUBMULSRA_RRFF or opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RMRF or
    opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMIF or opc = SUBMULSRA_RMFR or
    opc = SUBMULSRA_RMFM or opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or
    opc = SUBMULSRA_RMFP or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIMF or
    opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or opc = SUBMULSRA_RIFF or
    opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or
    opc = SUBMULSRA_RFRI or opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or
    opc = SUBMULSRA_RFMR or opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or
    opc = SUBMULSRA_RFMF or opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or
    opc = SUBMULSRA_RFIM or opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or
    opc = SUBMULSRA_RFFR or opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or
    opc = SUBMULSRA_RFPR or opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or
    opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRIF or
    opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
    opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MMRF or
    opc = SUBMULSRA_MMMF or opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMFR or
    opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or
    opc = SUBMULSRA_MMFP or opc = SUBMULSRA_MIRF or opc = SUBMULSRA_MIMF or
    opc = SUBMULSRA_MIFR or opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or
    opc = SUBMULSRA_MIFP or opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or
    opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or
    opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or
    opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or
    opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
    opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
    opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
    opc = SUBMULSRA_FRRF or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRIF or
    -- get0
    opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or opc = SUBMULSRA_FRFI or
    opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or opc = SUBMULSRA_FMRF or
    opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMFR or
    opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMFI or opc = SUBMULSRA_FMFF or
    opc = SUBMULSRA_FMFP or opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIMF or
    opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
    opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FFRR or opc = SUBMULSRA_FFRM or
    opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or opc = SUBMULSRA_FFRP or
    opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or opc = SUBMULSRA_FFMI or
    opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or opc = SUBMULSRA_FFIR or
    opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or opc = SUBMULSRA_FFIP or
    opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or opc = SUBMULSRA_FFFI or
    opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or opc = SUBMULSRA_FFPI or
    opc = ABSDIFF_RXRF or opc = ABSDIFF_RXMF or opc = ABSDIFF_RXIF or
    opc = ABSDIFF_RXFR or opc = ABSDIFF_RXFM or opc = ABSDIFF_RXFI or
    opc = ABSDIFF_RXFF or opc = ABSDIFF_RXFP or opc = ABSDIFF_MXRF or
    opc = ABSDIFF_MXMF or opc = ABSDIFF_MXIF or opc = ABSDIFF_MXFR or
    opc = ABSDIFF_MXFM or opc = ABSDIFF_MXFI or opc = ABSDIFF_MXFF or
    opc = ABSDIFF_MXFP or opc = ABSDIFF_FXRF or opc = ABSDIFF_FXMF or
    opc = ABSDIFF_FXIF or opc = ABSDIFF_FXFR or opc = ABSDIFF_FXFM or
    opc = ABSDIFF_FXFI or opc = ABSDIFF_FXFF or opc = ABSDIFF_FXFP or
    opc = ABSDIFFACCUM_RXRF or opc = ABSDIFFACCUM_RXMF or opc = ABSDIFFACCUM_RXIF or
    opc = ABSDIFFACCUM_RXFR or opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXFI or
    opc = ABSDIFFACCUM_RXFF or opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_MXRF or
    opc = ABSDIFFACCUM_MXMF or opc = ABSDIFFACCUM_MXIF or opc = ABSDIFFACCUM_MXFR or
    opc = ABSDIFFACCUM_MXFM or opc = ABSDIFFACCUM_MXFI or opc = ABSDIFFACCUM_MXFF or
    opc = ABSDIFFACCUM_MXFP or opc = ABSDIFFACCUM_FXRF or opc = ABSDIFFACCUM_FXMF or
    opc = ABSDIFFACCUM_FXIF or opc = ABSDIFFACCUM_FXFR or opc = ABSDIFFACCUM_FXFM or
    opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXFF or opc = ABSDIFFACCUM_FXFP or
    opc = ABSDIFFACCUM_XXRF or opc = ABSDIFFACCUM_XXMF or opc = ABSDIFFACCUM_XXIF or
    opc = ABSDIFFACCUM_XXFR or opc = ABSDIFFACCUM_XXFM or opc = ABSDIFFACCUM_XXFI or
    opc = ABSDIFFACCUM_XXFF or opc = ABSDIFFACCUM_XXFP or
    opc = CMP_XXRF or opc = CMP_XXMF or opc = CMP_XXIF or
    opc = CMP_XXFR or opc = CMP_XXFM or opc = CMP_XXFI or
    opc = CMP_XXFF or opc = CMP_XXFP or
    opc = CMPFWD_XXFX or
    opc = DECONST_RXXF or opc = DECONST_MXXF or opc = DECONST_FXXF or
    opc = LDSORT_XXXF or
    -- get0
    opc = PUT_FXXF or
    opc = GET_RXXF or opc = GET_MXXF or opc = GET_IXXF or
    opc = SETMASKLT_XXRF or opc = SETMASKLT_XXMF or opc = SETMASKLT_XXIF or
    opc = SETMASKLT_XXFR or opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or
    opc = SETMASKLT_XXFF or opc = SETMASKLT_XXFP or
    opc = SETMASKGT_XXRF or opc = SETMASKGT_XXMF or opc = SETMASKGT_XXIF or
    opc = SETMASKGT_XXFR or opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or
    opc = SETMASKGT_XXFF or opc = SETMASKGT_XXFP or
    opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXMF or opc = SETMASKEQ_XXIF or
    opc = SETMASKEQ_XXFR or opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or
    opc = SETMASKEQ_XXFF or opc = SETMASKEQ_XXFP or
    opc = SETMASKGE_XXRF or opc = SETMASKGE_XXMF or opc = SETMASKGE_XXIF or
    opc = SETMASKGE_XXFR or opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or
    opc = SETMASKGE_XXFF or opc = SETMASKGE_XXFP or
    opc = SETMASKLE_XXRF or opc = SETMASKLE_XXMF or opc = SETMASKLE_XXIF or
    opc = SETMASKLE_XXFR or opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or
    opc = SETMASKLE_XXFF or opc = SETMASKLE_XXFP or
    opc = SETMASKNE_XXRF or opc = SETMASKNE_XXMF or opc = SETMASKNE_XXIF or
    opc = SETMASKNE_XXFR or opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or
    opc = SETMASKNE_XXFF or opc = SETMASKNE_XXFP
  else '0';

  o_id_get_or_peak0 <= id_get_or_peak0;
  id_get_or_peak0 <= '1' when
    opc = ADDMUL_RRRF or opc = ADDMUL_RRRP or opc = ADDMUL_RRMF or
    opc = ADDMUL_RRMP or opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or
    opc = ADDMUL_RRFR or opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or
    opc = ADDMUL_RRFF or opc = ADDMUL_RRFP or opc = ADDMUL_RRPR or
    opc = ADDMUL_RRPM or opc = ADDMUL_RRPI or opc = ADDMUL_RRPF or
    opc = ADDMUL_RRPP or opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or
    opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or opc = ADDMUL_RMIF or
    opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
    opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
    opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
    opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRF or
    opc = ADDMUL_RIRP or opc = ADDMUL_RIMF or opc = ADDMUL_RIMP or
    opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or opc = ADDMUL_RIFF or
    opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or opc = ADDMUL_RIPM or
    opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or opc = ADDMUL_RFRR or
    opc = ADDMUL_RFRM or opc = ADDMUL_RFRI or opc = ADDMUL_RFRF or
    opc = ADDMUL_RFRP or opc = ADDMUL_RFMR or opc = ADDMUL_RFMM or
    opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or opc = ADDMUL_RFMP or
    opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or opc = ADDMUL_RFIF or
    opc = ADDMUL_RFIP or opc = ADDMUL_RFFR or opc = ADDMUL_RFFM or
    --id_get_or_peak0
    opc = ADDMUL_RFFI or opc = ADDMUL_RFPR or opc = ADDMUL_RFPM or
    opc = ADDMUL_RFPI or opc = ADDMUL_RPRR or opc = ADDMUL_RPRM or
    opc = ADDMUL_RPRI or opc = ADDMUL_RPRF or opc = ADDMUL_RPRP or
    opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or opc = ADDMUL_RPMI or
    opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or opc = ADDMUL_RPIR or
    opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or opc = ADDMUL_RPIP or
    opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or opc = ADDMUL_RPFI or
    opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or opc = ADDMUL_RPPI or
    opc = ADDMUL_MRRF or opc = ADDMUL_MRRP or opc = ADDMUL_MRMF or
    opc = ADDMUL_MRMP or opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or
    opc = ADDMUL_MRFR or opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or
    opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MRPR or
    opc = ADDMUL_MRPM or opc = ADDMUL_MRPI or opc = ADDMUL_MRPF or
    opc = ADDMUL_MRPP or opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or
    opc = ADDMUL_MMMF or opc = ADDMUL_MMMP or opc = ADDMUL_MMIF or
    opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or opc = ADDMUL_MMFM or
    opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or opc = ADDMUL_MMFP or
    opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or opc = ADDMUL_MMPI or
    opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or opc = ADDMUL_MIRF or
    opc = ADDMUL_MIRP or opc = ADDMUL_MIMF or opc = ADDMUL_MIMP or
    opc = ADDMUL_MIFR or opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or
    opc = ADDMUL_MIFP or opc = ADDMUL_MIPR or opc = ADDMUL_MIPM or
    opc = ADDMUL_MIPF or opc = ADDMUL_MIPP or opc = ADDMUL_MFRR or
    opc = ADDMUL_MFRM or opc = ADDMUL_MFRI or opc = ADDMUL_MFRF or
    opc = ADDMUL_MFRP or opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or
    --id_get_or_peak0
    opc = ADDMUL_MFMI or opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or
    opc = ADDMUL_MFIR or opc = ADDMUL_MFIM or opc = ADDMUL_MFIF or
    opc = ADDMUL_MFIP or opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or
    opc = ADDMUL_MFFI or opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or
    opc = ADDMUL_MFPI or opc = ADDMUL_MPRR or opc = ADDMUL_MPRM or
    opc = ADDMUL_MPRI or opc = ADDMUL_MPRF or opc = ADDMUL_MPRP or
    opc = ADDMUL_MPMR or opc = ADDMUL_MPMM or opc = ADDMUL_MPMI or
    opc = ADDMUL_MPMF or opc = ADDMUL_MPMP or opc = ADDMUL_MPIR or
    opc = ADDMUL_MPIM or opc = ADDMUL_MPIF or opc = ADDMUL_MPIP or
    opc = ADDMUL_MPFR or opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or
    opc = ADDMUL_MPPR or opc = ADDMUL_MPPM or opc = ADDMUL_MPPI or
    opc = ADDMUL_FRRF or opc = ADDMUL_FRRP or opc = ADDMUL_FRMF or
    opc = ADDMUL_FRMP or opc = ADDMUL_FRIF or opc = ADDMUL_FRIP or
    opc = ADDMUL_FRFR or opc = ADDMUL_FRFM or opc = ADDMUL_FRFI or
    opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or opc = ADDMUL_FRPR or
    opc = ADDMUL_FRPM or opc = ADDMUL_FRPI or opc = ADDMUL_FRPF or
    opc = ADDMUL_FRPP or opc = ADDMUL_FMRF or opc = ADDMUL_FMRP or
    opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or opc = ADDMUL_FMIF or
    opc = ADDMUL_FMIP or opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or
    opc = ADDMUL_FMFI or opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or
    opc = ADDMUL_FMPR or opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or
    opc = ADDMUL_FMPF or opc = ADDMUL_FMPP or opc = ADDMUL_FIRF or
    opc = ADDMUL_FIRP or opc = ADDMUL_FIMF or opc = ADDMUL_FIMP or
    opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
    opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or opc = ADDMUL_FIPM or
    opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or opc = ADDMUL_FFRR or
    opc = ADDMUL_FFRM or opc = ADDMUL_FFRI or opc = ADDMUL_FFRF or
    opc = ADDMUL_FFRP or opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or
    --id_get_or_peak0
    opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or
    opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or opc = ADDMUL_FFIF or
    opc = ADDMUL_FFIP or opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or
    opc = ADDMUL_FFFI or opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or
    opc = ADDMUL_FFPI or opc = ADDMUL_FPRR or opc = ADDMUL_FPRM or
    opc = ADDMUL_FPRI or opc = ADDMUL_FPRF or opc = ADDMUL_FPRP or
    opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or opc = ADDMUL_FPMI or
    opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or opc = ADDMUL_FPIR or
    opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or opc = ADDMUL_FPIP or
    opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
    opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or opc = ADDMUL_FPPI or
    opc = SUBMUL_RRRF or opc = SUBMUL_RRRP or opc = SUBMUL_RRMF or
    opc = SUBMUL_RRMP or opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or
    opc = SUBMUL_RRFR or opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or
    opc = SUBMUL_RRFF or opc = SUBMUL_RRFP or opc = SUBMUL_RRPR or
    opc = SUBMUL_RRPM or opc = SUBMUL_RRPI or opc = SUBMUL_RRPF or
    opc = SUBMUL_RRPP or opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or
    opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or opc = SUBMUL_RMIF or
    opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
    opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
    opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
    opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRF or
    opc = SUBMUL_RIRP or opc = SUBMUL_RIMF or opc = SUBMUL_RIMP or
    opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or opc = SUBMUL_RIFF or
    opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or opc = SUBMUL_RIPM or
    opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or opc = SUBMUL_RFRR or
    opc = SUBMUL_RFRM or opc = SUBMUL_RFRI or opc = SUBMUL_RFRF or
    opc = SUBMUL_RFRP or opc = SUBMUL_RFMR or opc = SUBMUL_RFMM or
    opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or opc = SUBMUL_RFMP or
    opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or opc = SUBMUL_RFIF or
    opc = SUBMUL_RFIP or opc = SUBMUL_RFFR or opc = SUBMUL_RFFM or
    opc = SUBMUL_RFFI or opc = SUBMUL_RFPR or opc = SUBMUL_RFPM or
    opc = SUBMUL_RFPI or opc = SUBMUL_RPRR or opc = SUBMUL_RPRM or
    opc = SUBMUL_RPRI or opc = SUBMUL_RPRF or opc = SUBMUL_RPRP or
    opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or opc = SUBMUL_RPMI or
    --id_get_or_peak0
    opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or opc = SUBMUL_RPIR or
    opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or opc = SUBMUL_RPIP or
    opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or opc = SUBMUL_RPFI or
    opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or opc = SUBMUL_RPPI or
    opc = SUBMUL_MRRF or opc = SUBMUL_MRRP or opc = SUBMUL_MRMF or
    opc = SUBMUL_MRMP or opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or
    opc = SUBMUL_MRFR or opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or
    opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MRPR or
    opc = SUBMUL_MRPM or opc = SUBMUL_MRPI or opc = SUBMUL_MRPF or
    opc = SUBMUL_MRPP or opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or
    opc = SUBMUL_MMMF or opc = SUBMUL_MMMP or opc = SUBMUL_MMIF or
    opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or opc = SUBMUL_MMFM or
    opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or opc = SUBMUL_MMFP or
    opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or opc = SUBMUL_MMPI or
    opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or opc = SUBMUL_MIRF or
    opc = SUBMUL_MIRP or opc = SUBMUL_MIMF or opc = SUBMUL_MIMP or
    opc = SUBMUL_MIFR or opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or
    opc = SUBMUL_MIFP or opc = SUBMUL_MIPR or opc = SUBMUL_MIPM or
    opc = SUBMUL_MIPF or opc = SUBMUL_MIPP or opc = SUBMUL_MFRR or
    opc = SUBMUL_MFRM or opc = SUBMUL_MFRI or opc = SUBMUL_MFRF or
    opc = SUBMUL_MFRP or opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or
    --id_get_or_peak0
    opc = SUBMUL_MFMI or opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or
    opc = SUBMUL_MFIR or opc = SUBMUL_MFIM or opc = SUBMUL_MFIF or
    opc = SUBMUL_MFIP or opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or
    opc = SUBMUL_MFFI or opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or
    opc = SUBMUL_MFPI or opc = SUBMUL_MPRR or opc = SUBMUL_MPRM or
    opc = SUBMUL_MPRI or opc = SUBMUL_MPRF or opc = SUBMUL_MPRP or
    opc = SUBMUL_MPMR or opc = SUBMUL_MPMM or opc = SUBMUL_MPMI or
    opc = SUBMUL_MPMF or opc = SUBMUL_MPMP or opc = SUBMUL_MPIR or
    opc = SUBMUL_MPIM or opc = SUBMUL_MPIF or opc = SUBMUL_MPIP or
    opc = SUBMUL_MPFR or opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or
    opc = SUBMUL_MPPR or opc = SUBMUL_MPPM or opc = SUBMUL_MPPI or
    opc = SUBMUL_FRRF or opc = SUBMUL_FRRP or opc = SUBMUL_FRMF or
    opc = SUBMUL_FRMP or opc = SUBMUL_FRIF or opc = SUBMUL_FRIP or
    opc = SUBMUL_FRFR or opc = SUBMUL_FRFM or opc = SUBMUL_FRFI or
    opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or opc = SUBMUL_FRPR or
    opc = SUBMUL_FRPM or opc = SUBMUL_FRPI or opc = SUBMUL_FRPF or
    opc = SUBMUL_FRPP or opc = SUBMUL_FMRF or opc = SUBMUL_FMRP or
    opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or opc = SUBMUL_FMIF or
    opc = SUBMUL_FMIP or opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or
    opc = SUBMUL_FMFI or opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or
    opc = SUBMUL_FMPR or opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or
    opc = SUBMUL_FMPF or opc = SUBMUL_FMPP or opc = SUBMUL_FIRF or
    opc = SUBMUL_FIRP or opc = SUBMUL_FIMF or opc = SUBMUL_FIMP or
    opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
    opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or opc = SUBMUL_FIPM or
    opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or opc = SUBMUL_FFRR or
    opc = SUBMUL_FFRM or opc = SUBMUL_FFRI or opc = SUBMUL_FFRF or
    opc = SUBMUL_FFRP or opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or
    opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or
    opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or opc = SUBMUL_FFIF or
    opc = SUBMUL_FFIP or opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or
    opc = SUBMUL_FFFI or opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or
    opc = SUBMUL_FFPI or opc = SUBMUL_FPRR or opc = SUBMUL_FPRM or
    opc = SUBMUL_FPRI or opc = SUBMUL_FPRF or opc = SUBMUL_FPRP or
    opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or opc = SUBMUL_FPMI or
    opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or opc = SUBMUL_FPIR or
    opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or opc = SUBMUL_FPIP or
    opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
    opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or opc = SUBMUL_FPPI or
    --id_get_or_peak0
    opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RRPX or opc = ADDMULFWD_RMFX or
    opc = ADDMULFWD_RMPX or opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or
    opc = ADDMULFWD_RFRX or opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or
    opc = ADDMULFWD_RFFX or opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPRX or
    opc = ADDMULFWD_RPMX or opc = ADDMULFWD_RPIX or opc = ADDMULFWD_RPFX or
    opc = ADDMULFWD_RPPX or opc = ADDMULFWD_MRFX or opc = ADDMULFWD_MRPX or
    opc = ADDMULFWD_MMFX or opc = ADDMULFWD_MMPX or opc = ADDMULFWD_MIFX or
    opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFRX or opc = ADDMULFWD_MFMX or
    opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or opc = ADDMULFWD_MFPX or
    opc = ADDMULFWD_MPRX or opc = ADDMULFWD_MPMX or opc = ADDMULFWD_MPIX or
    opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or opc = ADDMULFWD_FRFX or
    opc = ADDMULFWD_FRPX or opc = ADDMULFWD_FMFX or opc = ADDMULFWD_FMPX or
    opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFRX or
    opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or
    opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPRX or opc = ADDMULFWD_FPMX or
    opc = ADDMULFWD_FPIX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX or
    opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RRPX or opc = SUBMULFWD_RMFX or
    opc = SUBMULFWD_RMPX or opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or
    opc = SUBMULFWD_RFRX or opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or
    opc = SUBMULFWD_RFFX or opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPRX or
    opc = SUBMULFWD_RPMX or opc = SUBMULFWD_RPIX or opc = SUBMULFWD_RPFX or
    opc = SUBMULFWD_RPPX or opc = SUBMULFWD_MRFX or opc = SUBMULFWD_MRPX or
    opc = SUBMULFWD_MMFX or opc = SUBMULFWD_MMPX or opc = SUBMULFWD_MIFX or
    opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFRX or opc = SUBMULFWD_MFMX or
    opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or opc = SUBMULFWD_MFPX or
    opc = SUBMULFWD_MPRX or opc = SUBMULFWD_MPMX or opc = SUBMULFWD_MPIX or
    opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or opc = SUBMULFWD_FRFX or
    opc = SUBMULFWD_FRPX or opc = SUBMULFWD_FMFX or opc = SUBMULFWD_FMPX or
    opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFRX or
    opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or
    opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPRX or opc = SUBMULFWD_FPMX or
    --id_get_or_peak0
    opc = SUBMULFWD_FPIX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
    opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMF or
    opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or
    opc = ADDMULSRA_RRFR or opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or
    opc = ADDMULSRA_RRFF or opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or
    opc = ADDMULSRA_RRPM or opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or
    opc = ADDMULSRA_RRPP or opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or
    opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or opc = ADDMULSRA_RMIF or
    opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
    opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
    opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
    opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRF or
    opc = ADDMULSRA_RIRP or opc = ADDMULSRA_RIMF or opc = ADDMULSRA_RIMP or
    opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or opc = ADDMULSRA_RIFF or
    opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or opc = ADDMULSRA_RIPM or
    opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or opc = ADDMULSRA_RFRR or
    opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or opc = ADDMULSRA_RFRF or
    opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or opc = ADDMULSRA_RFMM or
    opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or opc = ADDMULSRA_RFMP or
    opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or opc = ADDMULSRA_RFIF or
    opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or opc = ADDMULSRA_RFFM or
    opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or opc = ADDMULSRA_RFPM or
    opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or opc = ADDMULSRA_RPRM or
    opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or opc = ADDMULSRA_RPRP or
    opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or opc = ADDMULSRA_RPMI or
    opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or opc = ADDMULSRA_RPIR or
    opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or opc = ADDMULSRA_RPIP or
    opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or opc = ADDMULSRA_RPFI or
    opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or opc = ADDMULSRA_RPPI or
    opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or opc = ADDMULSRA_MRMF or
    opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
    opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
    opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or
    opc = ADDMULSRA_MRPM or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or
    opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or
    opc = ADDMULSRA_MMMF or opc = ADDMULSRA_MMMP or opc = ADDMULSRA_MMIF or
    opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or opc = ADDMULSRA_MMFM or
    opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or opc = ADDMULSRA_MMFP or
    opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or opc = ADDMULSRA_MMPI or
    opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or opc = ADDMULSRA_MIRF or
    opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or
    opc = ADDMULSRA_MIFR or opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or
    opc = ADDMULSRA_MIFP or opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or
    opc = ADDMULSRA_MIPF or opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRR or
    opc = ADDMULSRA_MFRM or opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or
    opc = ADDMULSRA_MFRP or opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or
    opc = ADDMULSRA_MFMI or opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or
    opc = ADDMULSRA_MFIR or opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or
    opc = ADDMULSRA_MFIP or opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or
    opc = ADDMULSRA_MFFI or opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or
    opc = ADDMULSRA_MFPI or opc = ADDMULSRA_MPRR or opc = ADDMULSRA_MPRM or
    opc = ADDMULSRA_MPRI or opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or
    opc = ADDMULSRA_MPMR or opc = ADDMULSRA_MPMM or opc = ADDMULSRA_MPMI or
    opc = ADDMULSRA_MPMF or opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIR or
    opc = ADDMULSRA_MPIM or opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or
    --id_get_or_peak0
    opc = ADDMULSRA_MPFR or opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or
    opc = ADDMULSRA_MPPR or opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or
    opc = ADDMULSRA_FRRF or opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMF or
    opc = ADDMULSRA_FRMP or opc = ADDMULSRA_FRIF or opc = ADDMULSRA_FRIP or
    opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or opc = ADDMULSRA_FRFI or
    opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or opc = ADDMULSRA_FRPR or
    opc = ADDMULSRA_FRPM or opc = ADDMULSRA_FRPI or opc = ADDMULSRA_FRPF or
    opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMRF or opc = ADDMULSRA_FMRP or
    opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or opc = ADDMULSRA_FMIF or
    opc = ADDMULSRA_FMIP or opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or
    opc = ADDMULSRA_FMFI or opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or
    opc = ADDMULSRA_FMPR or opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or
    opc = ADDMULSRA_FMPF or opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRF or
    opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
    opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
    opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
    opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRR or
    opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or
    opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
    opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
    opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or
    opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or
    opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or
    opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or opc = ADDMULSRA_FPRM or
    opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or
    opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or opc = ADDMULSRA_FPMI or
    opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIR or
    opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
    opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
    opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI or
    opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMF or
    opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or
    --id_get_or_peak0
    opc = SUBMULSRA_RRFR or opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or
    opc = SUBMULSRA_RRFF or opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or
    opc = SUBMULSRA_RRPM or opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or
    opc = SUBMULSRA_RRPP or opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or
    opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or opc = SUBMULSRA_RMIF or
    opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
    opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
    opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
    opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRF or
    opc = SUBMULSRA_RIRP or opc = SUBMULSRA_RIMF or opc = SUBMULSRA_RIMP or
    opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or opc = SUBMULSRA_RIFF or
    opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or opc = SUBMULSRA_RIPM or
    opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or opc = SUBMULSRA_RFRR or
    opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or opc = SUBMULSRA_RFRF or
    opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or opc = SUBMULSRA_RFMM or
    opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or opc = SUBMULSRA_RFMP or
    opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or opc = SUBMULSRA_RFIF or
    opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or opc = SUBMULSRA_RFFM or
    opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or opc = SUBMULSRA_RFPM or
    opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or opc = SUBMULSRA_RPRM or
    opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or opc = SUBMULSRA_RPRP or
    opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or opc = SUBMULSRA_RPMI or
    opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or opc = SUBMULSRA_RPIR or
    opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or opc = SUBMULSRA_RPIP or
    opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or opc = SUBMULSRA_RPFI or
    opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or opc = SUBMULSRA_RPPI or
    opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or opc = SUBMULSRA_MRMF or
    opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
    opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
    opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or
    opc = SUBMULSRA_MRPM or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or
    opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or
    opc = SUBMULSRA_MMMF or opc = SUBMULSRA_MMMP or opc = SUBMULSRA_MMIF or
    opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or opc = SUBMULSRA_MMFM or
    opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or opc = SUBMULSRA_MMFP or
    opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or opc = SUBMULSRA_MMPI or
    opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or opc = SUBMULSRA_MIRF or
    opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or
    opc = SUBMULSRA_MIFR or opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or
    opc = SUBMULSRA_MIFP or opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or
    opc = SUBMULSRA_MIPF or opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRR or
    opc = SUBMULSRA_MFRM or opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or
    --id_get_or_peak0
    opc = SUBMULSRA_MFRP or opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or
    opc = SUBMULSRA_MFMI or opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or
    opc = SUBMULSRA_MFIR or opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or
    opc = SUBMULSRA_MFIP or opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or
    opc = SUBMULSRA_MFFI or opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or
    opc = SUBMULSRA_MFPI or opc = SUBMULSRA_MPRR or opc = SUBMULSRA_MPRM or
    opc = SUBMULSRA_MPRI or opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or
    opc = SUBMULSRA_MPMR or opc = SUBMULSRA_MPMM or opc = SUBMULSRA_MPMI or
    opc = SUBMULSRA_MPMF or opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIR or
    opc = SUBMULSRA_MPIM or opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or
    opc = SUBMULSRA_MPFR or opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or
    opc = SUBMULSRA_MPPR or opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or
    opc = SUBMULSRA_FRRF or opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMF or
    opc = SUBMULSRA_FRMP or opc = SUBMULSRA_FRIF or opc = SUBMULSRA_FRIP or
    opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or opc = SUBMULSRA_FRFI or
    opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or opc = SUBMULSRA_FRPR or
    opc = SUBMULSRA_FRPM or opc = SUBMULSRA_FRPI or opc = SUBMULSRA_FRPF or
    opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMRF or opc = SUBMULSRA_FMRP or
    opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or opc = SUBMULSRA_FMIF or
    opc = SUBMULSRA_FMIP or opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or
    opc = SUBMULSRA_FMFI or opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or
    opc = SUBMULSRA_FMPR or opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or
    opc = SUBMULSRA_FMPF or opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRF or
    opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
    opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
    opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
    opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRR or
    opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or
    opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
    opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
    opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or
    opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or
    opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or
    opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or opc = SUBMULSRA_FPRM or
    opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or
    opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or opc = SUBMULSRA_FPMI or
    opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIR or
    opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
    opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
    opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI or
    opc = ABSDIFF_RXRF or opc = ABSDIFF_RXRP or opc = ABSDIFF_RXMF or
    opc = ABSDIFF_RXMP or opc = ABSDIFF_RXIF or opc = ABSDIFF_RXIP or
    opc = ABSDIFF_RXFR or opc = ABSDIFF_RXFM or opc = ABSDIFF_RXFI or
    opc = ABSDIFF_RXFF or opc = ABSDIFF_RXFP or opc = ABSDIFF_RXPR or
    opc = ABSDIFF_RXPM or opc = ABSDIFF_RXPI or opc = ABSDIFF_RXPF or
    opc = ABSDIFF_RXPP or opc = ABSDIFF_MXRF or opc = ABSDIFF_MXRP or
    opc = ABSDIFF_MXMF or opc = ABSDIFF_MXMP or opc = ABSDIFF_MXIF or
    opc = ABSDIFF_MXIP or opc = ABSDIFF_MXFR or opc = ABSDIFF_MXFM or
    opc = ABSDIFF_MXFI or opc = ABSDIFF_MXFF or opc = ABSDIFF_MXFP or
    opc = ABSDIFF_MXPR or opc = ABSDIFF_MXPM or opc = ABSDIFF_MXPI or
    opc = ABSDIFF_MXPF or opc = ABSDIFF_MXPP or opc = ABSDIFF_FXRF or
    opc = ABSDIFF_FXRP or opc = ABSDIFF_FXMF or opc = ABSDIFF_FXMP or
    opc = ABSDIFF_FXIF or opc = ABSDIFF_FXIP or opc = ABSDIFF_FXFR or
    opc = ABSDIFF_FXFM or opc = ABSDIFF_FXFI or opc = ABSDIFF_FXFF or
    opc = ABSDIFF_FXFP or opc = ABSDIFF_FXPR or opc = ABSDIFF_FXPM or
    opc = ABSDIFF_FXPI or opc = ABSDIFF_FXPF or opc = ABSDIFF_FXPP or
    --id_get_or_peak0
    opc = ABSDIFFACCUM_RXRF or opc = ABSDIFFACCUM_RXRP or opc = ABSDIFFACCUM_RXMF or
    opc = ABSDIFFACCUM_RXMP or opc = ABSDIFFACCUM_RXIF or opc = ABSDIFFACCUM_RXIP or
    opc = ABSDIFFACCUM_RXFR or opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXFI or
    opc = ABSDIFFACCUM_RXFF or opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_RXPR or
    opc = ABSDIFFACCUM_RXPM or opc = ABSDIFFACCUM_RXPI or opc = ABSDIFFACCUM_RXPF or
    opc = ABSDIFFACCUM_RXPP or opc = ABSDIFFACCUM_MXRF or opc = ABSDIFFACCUM_MXRP or
    opc = ABSDIFFACCUM_MXMF or opc = ABSDIFFACCUM_MXMP or opc = ABSDIFFACCUM_MXIF or
    opc = ABSDIFFACCUM_MXIP or opc = ABSDIFFACCUM_MXFR or opc = ABSDIFFACCUM_MXFM or
    opc = ABSDIFFACCUM_MXFI or opc = ABSDIFFACCUM_MXFF or opc = ABSDIFFACCUM_MXFP or
    opc = ABSDIFFACCUM_MXPR or opc = ABSDIFFACCUM_MXPM or opc = ABSDIFFACCUM_MXPI or
    opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_MXPP or opc = ABSDIFFACCUM_FXRF or
    opc = ABSDIFFACCUM_FXRP or opc = ABSDIFFACCUM_FXMF or opc = ABSDIFFACCUM_FXMP or
    opc = ABSDIFFACCUM_FXIF or opc = ABSDIFFACCUM_FXIP or opc = ABSDIFFACCUM_FXFR or
    opc = ABSDIFFACCUM_FXFM or opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXFF or
    opc = ABSDIFFACCUM_FXFP or opc = ABSDIFFACCUM_FXPR or opc = ABSDIFFACCUM_FXPM or
    opc = ABSDIFFACCUM_FXPI or opc = ABSDIFFACCUM_FXPF or opc = ABSDIFFACCUM_FXPP or
    opc = ABSDIFFACCUM_XXRF or opc = ABSDIFFACCUM_XXRP or opc = ABSDIFFACCUM_XXMF or
    opc = ABSDIFFACCUM_XXMP or opc = ABSDIFFACCUM_XXIF or opc = ABSDIFFACCUM_XXIP or
    opc = ABSDIFFACCUM_XXFR or opc = ABSDIFFACCUM_XXFM or opc = ABSDIFFACCUM_XXFI or
    opc = ABSDIFFACCUM_XXFF or opc = ABSDIFFACCUM_XXFP or opc = ABSDIFFACCUM_XXPR or
    opc = ABSDIFFACCUM_XXPM or opc = ABSDIFFACCUM_XXPI or opc = ABSDIFFACCUM_XXPF or
    opc = ABSDIFFACCUM_XXPP or
    --id_get_or_peak0
    opc = CMP_XXRF or opc = CMP_XXRP or opc = CMP_XXMF or
    opc = CMP_XXMP or opc = CMP_XXIF or opc = CMP_XXIP or
    opc = CMP_XXFR or opc = CMP_XXFM or opc = CMP_XXFI or
    opc = CMP_XXFF or opc = CMP_XXFP or opc = CMP_XXPR or
    opc = CMP_XXPM or opc = CMP_XXPI or opc = CMP_XXPF or
    --id_get_or_peak0
    opc = CMP_XXPP or
    opc = CMPFWD_XXFX or opc = CMPFWD_XXPX or
    opc = DECONST_RXXF or opc = DECONST_RXXP or opc = DECONST_MXXF or
    opc = DECONST_MXXP or opc = DECONST_FXXF or opc = DECONST_FXXP or
    opc = LDSORT_XXXF or opc = LDSORT_XXXP or
    opc = PUT_FXXF or opc = PUT_FXXP or
    opc = GET_RXXF or opc = GET_MXXF or opc = GET_IXXF or
    opc = SETMASKLT_XXRF or opc = SETMASKLT_XXRP or opc = SETMASKLT_XXMF or
    opc = SETMASKLT_XXMP or opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or
    opc = SETMASKLT_XXFR or opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or
    opc = SETMASKLT_XXFF or opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPR or
    opc = SETMASKLT_XXPM or opc = SETMASKLT_XXPI or opc = SETMASKLT_XXPF or
    opc = SETMASKLT_XXPP or
    opc = SETMASKGT_XXRF or opc = SETMASKGT_XXRP or opc = SETMASKGT_XXMF or
    opc = SETMASKGT_XXMP or opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or
    opc = SETMASKGT_XXFR or opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or
    opc = SETMASKGT_XXFF or opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPR or
    opc = SETMASKGT_XXPM or opc = SETMASKGT_XXPI or opc = SETMASKGT_XXPF or
    opc = SETMASKGT_XXPP or
    opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXRP or opc = SETMASKEQ_XXMF or
    opc = SETMASKEQ_XXMP or opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or
    opc = SETMASKEQ_XXFR or opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or
    opc = SETMASKEQ_XXFF or opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPR or
    opc = SETMASKEQ_XXPM or opc = SETMASKEQ_XXPI or opc = SETMASKEQ_XXPF or
    opc = SETMASKEQ_XXPP or
    opc = SETMASKGE_XXRF or opc = SETMASKGE_XXRP or opc = SETMASKGE_XXMF or
    opc = SETMASKGE_XXMP or opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or
    opc = SETMASKGE_XXFR or opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or
    opc = SETMASKGE_XXFF or opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPR or
    opc = SETMASKGE_XXPM or opc = SETMASKGE_XXPI or opc = SETMASKGE_XXPF or
    opc = SETMASKGE_XXPP or
    --id_get_or_peak0
    opc = SETMASKLE_XXRF or opc = SETMASKLE_XXRP or opc = SETMASKLE_XXMF or
    opc = SETMASKLE_XXMP or opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or
    opc = SETMASKLE_XXFR or opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or
    opc = SETMASKLE_XXFF or opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPR or
    opc = SETMASKLE_XXPM or opc = SETMASKLE_XXPI or opc = SETMASKLE_XXPF or
    opc = SETMASKLE_XXPP or
    opc = SETMASKNE_XXRF or opc = SETMASKNE_XXRP or opc = SETMASKNE_XXMF or
    opc = SETMASKNE_XXMP or opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or
    opc = SETMASKNE_XXFR or opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or
    opc = SETMASKNE_XXFF or opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPR or
    opc = SETMASKNE_XXPM or opc = SETMASKNE_XXPI or opc = SETMASKNE_XXPF or
    opc = SETMASKNE_XXPP
  else '0';

  o_id_get1 <= '1' when
    opc = ADDMUL_RRFF or opc = ADDMUL_RRPF or opc = ADDMUL_RMFF or
    opc = ADDMUL_RMPF or opc = ADDMUL_RIFF or opc = ADDMUL_RIPF or
    opc = ADDMUL_RFRF or opc = ADDMUL_RFMF or opc = ADDMUL_RFIF or
    opc = ADDMUL_RFFR or opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or
    opc = ADDMUL_RPRF or opc = ADDMUL_RPMF or opc = ADDMUL_RPIF or
    opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or opc = ADDMUL_RPFI or
    opc = ADDMUL_MRFF or opc = ADDMUL_MRPF or opc = ADDMUL_MMFF or
    opc = ADDMUL_MMPF or opc = ADDMUL_MIFF or opc = ADDMUL_MIPF or
    opc = ADDMUL_MFRF or opc = ADDMUL_MFMF or opc = ADDMUL_MFIF or
    opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
    opc = ADDMUL_MPRF or opc = ADDMUL_MPMF or opc = ADDMUL_MPIF or
    opc = ADDMUL_MPFR or opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or
    opc = ADDMUL_FRFF or opc = ADDMUL_FRPF or opc = ADDMUL_FMFF or
    opc = ADDMUL_FMPF or opc = ADDMUL_FIFF or opc = ADDMUL_FIPF or
    opc = ADDMUL_FFRF or opc = ADDMUL_FFMF or opc = ADDMUL_FFIF or
    opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or opc = ADDMUL_FFFI or
    opc = ADDMUL_FPRF or opc = ADDMUL_FPMF or opc = ADDMUL_FPIF or
    --o_id_get1
    opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
    opc = SUBMUL_RRFF or opc = SUBMUL_RRPF or opc = SUBMUL_RMFF or
    opc = SUBMUL_RMPF or opc = SUBMUL_RIFF or opc = SUBMUL_RIPF or
    opc = SUBMUL_RFRF or opc = SUBMUL_RFMF or opc = SUBMUL_RFIF or
    opc = SUBMUL_RFFR or opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or
    opc = SUBMUL_RPRF or opc = SUBMUL_RPMF or opc = SUBMUL_RPIF or
    opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or opc = SUBMUL_RPFI or
    opc = SUBMUL_MRFF or opc = SUBMUL_MRPF or opc = SUBMUL_MMFF or
    opc = SUBMUL_MMPF or opc = SUBMUL_MIFF or opc = SUBMUL_MIPF or
    opc = SUBMUL_MFRF or opc = SUBMUL_MFMF or opc = SUBMUL_MFIF or
    opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
    opc = SUBMUL_MPRF or opc = SUBMUL_MPMF or opc = SUBMUL_MPIF or
    opc = SUBMUL_MPFR or opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or
    opc = SUBMUL_FRFF or opc = SUBMUL_FRPF or opc = SUBMUL_FMFF or
    opc = SUBMUL_FMPF or opc = SUBMUL_FIFF or opc = SUBMUL_FIPF or
    opc = SUBMUL_FFRF or opc = SUBMUL_FFMF or opc = SUBMUL_FFIF or
    opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or opc = SUBMUL_FFFI or
    opc = SUBMUL_FPRF or opc = SUBMUL_FPMF or opc = SUBMUL_FPIF or
    opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
    opc = ADDMULFWD_RFFX or opc = ADDMULFWD_RPFX or opc = ADDMULFWD_MFFX or
    opc = ADDMULFWD_MPFX or opc = ADDMULFWD_FFFX or opc = ADDMULFWD_FPFX or
    opc = SUBMULFWD_RFFX or opc = SUBMULFWD_RPFX or opc = SUBMULFWD_MFFX or
    opc = SUBMULFWD_MPFX or opc = SUBMULFWD_FFFX or opc = SUBMULFWD_FPFX or
    opc = ADDMULSRA_RRFF or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RMFF or
    opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIPF or
    opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFMF or opc = ADDMULSRA_RFIF or
    opc = ADDMULSRA_RFFR or opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or
    --o_id_get1
    opc = ADDMULSRA_RPRF or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPIF or
    opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or opc = ADDMULSRA_RPFI or
    opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRPF or opc = ADDMULSRA_MMFF or
    opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIPF or
    opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFIF or
    opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
    opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPMF or opc = ADDMULSRA_MPIF or
    opc = ADDMULSRA_MPFR or opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or
    opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FMFF or
    opc = ADDMULSRA_FMPF or opc = ADDMULSRA_FIFF or opc = ADDMULSRA_FIPF or
    opc = ADDMULSRA_FFRF or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFIF or
    opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or opc = ADDMULSRA_FFFI or
    opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPIF or
    opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
    opc = SUBMULSRA_RRFF or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RMFF or
    opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIPF or
    opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFMF or opc = SUBMULSRA_RFIF or
    opc = SUBMULSRA_RFFR or opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or
    opc = SUBMULSRA_RPRF or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPIF or
    opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or opc = SUBMULSRA_RPFI or
    opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRPF or opc = SUBMULSRA_MMFF or
    opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIPF or
    opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFIF or
    opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
    opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPMF or opc = SUBMULSRA_MPIF or
    opc = SUBMULSRA_MPFR or opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or
    opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FMFF or
    opc = SUBMULSRA_FMPF or opc = SUBMULSRA_FIFF or opc = SUBMULSRA_FIPF or
    opc = SUBMULSRA_FFRF or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFIF or
    opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or opc = SUBMULSRA_FFFI or
    opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPIF or
    opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
    opc = ABSDIFF_RXFF or opc = ABSDIFF_RXPF or opc = ABSDIFF_MXFF or
    opc = ABSDIFF_MXPF or opc = ABSDIFF_FXFF or opc = ABSDIFF_FXPF or
    --o_id_get1
    opc = ABSDIFFACCUM_RXFF or opc = ABSDIFFACCUM_RXPF or opc = ABSDIFFACCUM_MXFF or
    opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_FXFF or opc = ABSDIFFACCUM_FXPF or
    opc = ABSDIFFACCUM_XXFF or opc = ABSDIFFACCUM_XXPF or
    opc = CMP_XXFF or opc = CMP_XXPF or
    opc = SETMASKLT_XXFF or opc = SETMASKLT_XXPF or
    opc = SETMASKGT_XXFF or opc = SETMASKGT_XXPF or
    opc = SETMASKEQ_XXFF or opc = SETMASKEQ_XXPF or
    opc = SETMASKGE_XXFF or opc = SETMASKGE_XXPF or
    opc = SETMASKLE_XXFF or opc = SETMASKLE_XXPF or
    opc = SETMASKNE_XXFF or opc = SETMASKNE_XXPF
  else '0';

  o_id_get_or_peak1 <= '1' when
    opc = ADDMUL_RRFF or opc = ADDMUL_RRFP or opc = ADDMUL_RRPF or
    opc = ADDMUL_RRPP or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
    opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIFF or
    opc = ADDMUL_RIFP or opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or
    opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or opc = ADDMUL_RFMF or
    opc = ADDMUL_RFMP or opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or
    opc = ADDMUL_RFFR or opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or
    opc = ADDMUL_RFPR or opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or
    opc = ADDMUL_RPRF or opc = ADDMUL_RPRP or opc = ADDMUL_RPMF or
    opc = ADDMUL_RPMP or opc = ADDMUL_RPIF or opc = ADDMUL_RPIP or
    opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or opc = ADDMUL_RPFI or
    opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or opc = ADDMUL_RPPI or
    opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MRPF or
    opc = ADDMUL_MRPP or opc = ADDMUL_MMFF or opc = ADDMUL_MMFP or
    opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or opc = ADDMUL_MIFF or
    opc = ADDMUL_MIFP or opc = ADDMUL_MIPF or opc = ADDMUL_MIPP or
    opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or opc = ADDMUL_MFMF or
    opc = ADDMUL_MFMP or opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or
    opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
    opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or
    opc = ADDMUL_MPRF or opc = ADDMUL_MPRP or opc = ADDMUL_MPMF or
    opc = ADDMUL_MPMP or opc = ADDMUL_MPIF or opc = ADDMUL_MPIP or
    opc = ADDMUL_MPFR or opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or
    opc = ADDMUL_MPPR or opc = ADDMUL_MPPM or opc = ADDMUL_MPPI or
    opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or opc = ADDMUL_FRPF or
    opc = ADDMUL_FRPP or opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or
    opc = ADDMUL_FMPF or opc = ADDMUL_FMPP or opc = ADDMUL_FIFF or
    opc = ADDMUL_FIFP or opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or
    opc = ADDMUL_FFRF or opc = ADDMUL_FFRP or opc = ADDMUL_FFMF or
    opc = ADDMUL_FFMP or opc = ADDMUL_FFIF or opc = ADDMUL_FFIP or
    opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or opc = ADDMUL_FFFI or
    opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or opc = ADDMUL_FFPI or
    --o_id_get_or_peak1
    opc = ADDMUL_FPRF or opc = ADDMUL_FPRP or opc = ADDMUL_FPMF or
    opc = ADDMUL_FPMP or opc = ADDMUL_FPIF or opc = ADDMUL_FPIP or
    opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
    opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or opc = ADDMUL_FPPI or
    opc = SUBMUL_RRFF or opc = SUBMUL_RRFP or opc = SUBMUL_RRPF or
    opc = SUBMUL_RRPP or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
    opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIFF or
    opc = SUBMUL_RIFP or opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or
    opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or opc = SUBMUL_RFMF or
    opc = SUBMUL_RFMP or opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or
    opc = SUBMUL_RFFR or opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or
    opc = SUBMUL_RFPR or opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or
    opc = SUBMUL_RPRF or opc = SUBMUL_RPRP or opc = SUBMUL_RPMF or
    opc = SUBMUL_RPMP or opc = SUBMUL_RPIF or opc = SUBMUL_RPIP or
    opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or opc = SUBMUL_RPFI or
    opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or opc = SUBMUL_RPPI or
    opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MRPF or
    opc = SUBMUL_MRPP or opc = SUBMUL_MMFF or opc = SUBMUL_MMFP or
    opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or opc = SUBMUL_MIFF or
    opc = SUBMUL_MIFP or opc = SUBMUL_MIPF or opc = SUBMUL_MIPP or
    opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or opc = SUBMUL_MFMF or
    opc = SUBMUL_MFMP or opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or
    opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
    opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or
    opc = SUBMUL_MPRF or opc = SUBMUL_MPRP or opc = SUBMUL_MPMF or
    opc = SUBMUL_MPMP or opc = SUBMUL_MPIF or opc = SUBMUL_MPIP or
    opc = SUBMUL_MPFR or opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or
    opc = SUBMUL_MPPR or opc = SUBMUL_MPPM or opc = SUBMUL_MPPI or
    opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or opc = SUBMUL_FRPF or
    opc = SUBMUL_FRPP or opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or
    opc = SUBMUL_FMPF or opc = SUBMUL_FMPP or opc = SUBMUL_FIFF or
    opc = SUBMUL_FIFP or opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or
    opc = SUBMUL_FFRF or opc = SUBMUL_FFRP or opc = SUBMUL_FFMF or
    opc = SUBMUL_FFMP or opc = SUBMUL_FFIF or opc = SUBMUL_FFIP or
    opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or opc = SUBMUL_FFFI or
    opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or opc = SUBMUL_FFPI or
    opc = SUBMUL_FPRF or opc = SUBMUL_FPRP or opc = SUBMUL_FPMF or
    --o_id_get_or_peak1
    opc = SUBMUL_FPMP or opc = SUBMUL_FPIF or opc = SUBMUL_FPIP or
    opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
    opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or opc = SUBMUL_FPPI or
    opc = ADDMULFWD_RFFX or opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPFX or
    opc = ADDMULFWD_RPPX or opc = ADDMULFWD_MFFX or opc = ADDMULFWD_MFPX or
    opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or opc = ADDMULFWD_FFFX or
    opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX or
    opc = SUBMULFWD_RFFX or opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPFX or
    opc = SUBMULFWD_RPPX or opc = SUBMULFWD_MFFX or opc = SUBMULFWD_MFPX or
    opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or opc = SUBMULFWD_FFFX or
    opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
    opc = ADDMULSRA_RRFF or opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPF or
    opc = ADDMULSRA_RRPP or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
    opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIFF or
    opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
    opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMF or
    opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or
    opc = ADDMULSRA_RFFR or opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or
    opc = ADDMULSRA_RFPR or opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or
    opc = ADDMULSRA_RPRF or opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMF or
    opc = ADDMULSRA_RPMP or opc = ADDMULSRA_RPIF or opc = ADDMULSRA_RPIP or
    opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or opc = ADDMULSRA_RPFI or
    opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or opc = ADDMULSRA_RPPI or
    opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPF or
    opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMFF or opc = ADDMULSRA_MMFP or
    opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or opc = ADDMULSRA_MIFF or
    opc = ADDMULSRA_MIFP or opc = ADDMULSRA_MIPF or opc = ADDMULSRA_MIPP or
    opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or opc = ADDMULSRA_MFMF or
    opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
    opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
    opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
    opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMF or
    opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or
    opc = ADDMULSRA_MPFR or opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or
    opc = ADDMULSRA_MPPR or opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or
    opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or opc = ADDMULSRA_FRPF or
    opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or
    --o_id_get_or_peak1
    opc = ADDMULSRA_FMPF or opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIFF or
    opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or
    opc = ADDMULSRA_FFRF or opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMF or
    opc = ADDMULSRA_FFMP or opc = ADDMULSRA_FFIF or opc = ADDMULSRA_FFIP or
    opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or opc = ADDMULSRA_FFFI or
    opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or opc = ADDMULSRA_FFPI or
    opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or opc = ADDMULSRA_FPMF or
    opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
    opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
    opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI or
    opc = SUBMULSRA_RRFF or opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPF or
    opc = SUBMULSRA_RRPP or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
    opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIFF or
    opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
    opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMF or
    opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or
    opc = SUBMULSRA_RFFR or opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or
    opc = SUBMULSRA_RFPR or opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or
    opc = SUBMULSRA_RPRF or opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMF or
    opc = SUBMULSRA_RPMP or opc = SUBMULSRA_RPIF or opc = SUBMULSRA_RPIP or
    opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or opc = SUBMULSRA_RPFI or
    opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or opc = SUBMULSRA_RPPI or
    opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPF or
    opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMFF or opc = SUBMULSRA_MMFP or
    opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or opc = SUBMULSRA_MIFF or
    opc = SUBMULSRA_MIFP or opc = SUBMULSRA_MIPF or opc = SUBMULSRA_MIPP or
    opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or opc = SUBMULSRA_MFMF or
    opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
    opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
    opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
    opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMF or
    opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or
    opc = SUBMULSRA_MPFR or opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or
    opc = SUBMULSRA_MPPR or opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or
    opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or opc = SUBMULSRA_FRPF or
    opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or
    opc = SUBMULSRA_FMPF or opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIFF or
    opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or
    opc = SUBMULSRA_FFRF or opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMF or
    opc = SUBMULSRA_FFMP or opc = SUBMULSRA_FFIF or opc = SUBMULSRA_FFIP or
    opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or opc = SUBMULSRA_FFFI or
    opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or opc = SUBMULSRA_FFPI or
    --o_id_get_or_peak1
    opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or opc = SUBMULSRA_FPMF or
    opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
    opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
    opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI or
    opc = ABSDIFF_RXFF or opc = ABSDIFF_RXFP or opc = ABSDIFF_RXPF or
    opc = ABSDIFF_RXPP or opc = ABSDIFF_MXFF or opc = ABSDIFF_MXFP or
    opc = ABSDIFF_MXPF or opc = ABSDIFF_MXPP or opc = ABSDIFF_FXFF or
    opc = ABSDIFF_FXFP or opc = ABSDIFF_FXPF or opc = ABSDIFF_FXPP or
    opc = ABSDIFFACCUM_RXFF or opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_RXPF or
    opc = ABSDIFFACCUM_RXPP or opc = ABSDIFFACCUM_MXFF or opc = ABSDIFFACCUM_MXFP or
    opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_MXPP or opc = ABSDIFFACCUM_FXFF or
    opc = ABSDIFFACCUM_FXFP or opc = ABSDIFFACCUM_FXPF or opc = ABSDIFFACCUM_FXPP or
    opc = ABSDIFFACCUM_XXFF or opc = ABSDIFFACCUM_XXFP or opc = ABSDIFFACCUM_XXPF or
    opc = ABSDIFFACCUM_XXPP or
    opc = CMP_XXFF or opc = CMP_XXFP or opc = CMP_XXPF or
    opc = CMP_XXPP or
    opc = SETMASKLT_XXFF or opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPF or
    opc = SETMASKLT_XXPP or
    opc = SETMASKGT_XXFF or opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPF or
    opc = SETMASKGT_XXPP or
    opc = SETMASKEQ_XXFF or opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPF or
    opc = SETMASKEQ_XXPP or
    opc = SETMASKGE_XXFF or opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPF or
    opc = SETMASKGE_XXPP or
    opc = SETMASKLE_XXFF or opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPF or
    opc = SETMASKLE_XXPP or
    opc = SETMASKNE_XXFF or opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPF or
    opc = SETMASKNE_XXPP
  else '0';

  o_id_fifowrite <= id_fifowrite;
  id_fifowrite <= '1' when
    opc = PUTCA_FXXX or
    opc = ADDMUL_FRRR or opc = ADDMUL_FRRM or opc = ADDMUL_FRRI or
    opc = ADDMUL_FRRF or opc = ADDMUL_FRRP or opc = ADDMUL_FRMR or
    opc = ADDMUL_FRMM or opc = ADDMUL_FRMI or opc = ADDMUL_FRMF or
    opc = ADDMUL_FRMP or opc = ADDMUL_FRIR or opc = ADDMUL_FRIM or
    opc = ADDMUL_FRIF or opc = ADDMUL_FRIP or opc = ADDMUL_FRFR or
    opc = ADDMUL_FRFM or opc = ADDMUL_FRFI or opc = ADDMUL_FRFF or
    opc = ADDMUL_FRFP or opc = ADDMUL_FRPR or opc = ADDMUL_FRPM or
    opc = ADDMUL_FRPI or opc = ADDMUL_FRPF or opc = ADDMUL_FRPP or
    opc = ADDMUL_FMRR or opc = ADDMUL_FMRM or opc = ADDMUL_FMRI or
    opc = ADDMUL_FMRF or opc = ADDMUL_FMRP or opc = ADDMUL_FMMR or
    opc = ADDMUL_FMMI or opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or
    opc = ADDMUL_FMIR or opc = ADDMUL_FMIM or opc = ADDMUL_FMIF or
    opc = ADDMUL_FMIP or opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or
    opc = ADDMUL_FMFI or opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or
    opc = ADDMUL_FMPR or opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or
    opc = ADDMUL_FMPF or opc = ADDMUL_FMPP or opc = ADDMUL_FIRR or
    opc = ADDMUL_FIRM or opc = ADDMUL_FIRF or opc = ADDMUL_FIRP or
    opc = ADDMUL_FIMR or opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or
    opc = ADDMUL_FIMP or opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or
    opc = ADDMUL_FIFF or opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or
    opc = ADDMUL_FIPM or opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or
    opc = ADDMUL_FFRR or opc = ADDMUL_FFRM or opc = ADDMUL_FFRI or
    opc = ADDMUL_FFRF or opc = ADDMUL_FFRP or opc = ADDMUL_FFMR or
    opc = ADDMUL_FFMM or opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or
    opc = ADDMUL_FFMP or opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or
    opc = ADDMUL_FFIF or opc = ADDMUL_FFIP or opc = ADDMUL_FFFR or
    opc = ADDMUL_FFFM or opc = ADDMUL_FFFI or opc = ADDMUL_FFPR or
    opc = ADDMUL_FFPM or opc = ADDMUL_FFPI or opc = ADDMUL_FPRR or
    opc = ADDMUL_FPRM or opc = ADDMUL_FPRI or opc = ADDMUL_FPRF or
    opc = ADDMUL_FPRP or opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or
    opc = ADDMUL_FPMI or opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or
    opc = ADDMUL_FPIR or opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or
    opc = ADDMUL_FPIP or opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or
    opc = ADDMUL_FPFI or opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or
  -- id_fifowrite
    opc = ADDMUL_FPPI or
    opc = SUBMUL_FRRR or opc = SUBMUL_FRRM or opc = SUBMUL_FRRI or
    opc = SUBMUL_FRRF or opc = SUBMUL_FRRP or opc = SUBMUL_FRMR or
    opc = SUBMUL_FRMM or opc = SUBMUL_FRMI or opc = SUBMUL_FRMF or
    opc = SUBMUL_FRMP or opc = SUBMUL_FRIR or opc = SUBMUL_FRIM or
    opc = SUBMUL_FRIF or opc = SUBMUL_FRIP or opc = SUBMUL_FRFR or
    opc = SUBMUL_FRFM or opc = SUBMUL_FRFI or opc = SUBMUL_FRFF or
    opc = SUBMUL_FRFP or opc = SUBMUL_FRPR or opc = SUBMUL_FRPM or
    opc = SUBMUL_FRPI or opc = SUBMUL_FRPF or opc = SUBMUL_FRPP or
    opc = SUBMUL_FMRR or opc = SUBMUL_FMRM or opc = SUBMUL_FMRI or
    opc = SUBMUL_FMRF or opc = SUBMUL_FMRP or opc = SUBMUL_FMMR or
    opc = SUBMUL_FMMI or opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or
    opc = SUBMUL_FMIR or opc = SUBMUL_FMIM or opc = SUBMUL_FMIF or
    opc = SUBMUL_FMIP or opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or
    opc = SUBMUL_FMFI or opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or
    opc = SUBMUL_FMPR or opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or
    opc = SUBMUL_FMPF or opc = SUBMUL_FMPP or opc = SUBMUL_FIRR or
    opc = SUBMUL_FIRM or opc = SUBMUL_FIRF or opc = SUBMUL_FIRP or
    opc = SUBMUL_FIMR or opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or
    opc = SUBMUL_FIMP or opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or
    opc = SUBMUL_FIFF or opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or
    opc = SUBMUL_FIPM or opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or
    opc = SUBMUL_FFRR or opc = SUBMUL_FFRM or opc = SUBMUL_FFRI or
    opc = SUBMUL_FFRF or opc = SUBMUL_FFRP or opc = SUBMUL_FFMR or
    opc = SUBMUL_FFMM or opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or
    opc = SUBMUL_FFMP or opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or
    opc = SUBMUL_FFIF or opc = SUBMUL_FFIP or opc = SUBMUL_FFFR or
    opc = SUBMUL_FFFM or opc = SUBMUL_FFFI or opc = SUBMUL_FFPR or
    opc = SUBMUL_FFPM or opc = SUBMUL_FFPI or opc = SUBMUL_FPRR or
    opc = SUBMUL_FPRM or opc = SUBMUL_FPRI or opc = SUBMUL_FPRF or
    opc = SUBMUL_FPRP or opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or
    opc = SUBMUL_FPMI or opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or
    opc = SUBMUL_FPIR or opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or
    opc = SUBMUL_FPIP or opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or
    opc = SUBMUL_FPFI or opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or
    opc = SUBMUL_FPPI or
    opc = ADDMULFWD_FRRX or opc = ADDMULFWD_FRMX or opc = ADDMULFWD_FRIX or
    opc = ADDMULFWD_FRFX or opc = ADDMULFWD_FRPX or opc = ADDMULFWD_FMRX or
    opc = ADDMULFWD_FMMX or opc = ADDMULFWD_FMIX or opc = ADDMULFWD_FMFX or
    opc = ADDMULFWD_FMPX or opc = ADDMULFWD_FIRX or opc = ADDMULFWD_FIMX or
    opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFRX or
    opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or
    opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPRX or opc = ADDMULFWD_FPMX or
    opc = ADDMULFWD_FPIX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX or
    opc = SUBMULFWD_FRRX or opc = SUBMULFWD_FRMX or opc = SUBMULFWD_FRIX or
    opc = SUBMULFWD_FRFX or opc = SUBMULFWD_FRPX or opc = SUBMULFWD_FMRX or
    opc = SUBMULFWD_FMMX or opc = SUBMULFWD_FMIX or opc = SUBMULFWD_FMFX or
  -- id_fifowrite
    opc = SUBMULFWD_FMPX or opc = SUBMULFWD_FIRX or opc = SUBMULFWD_FIMX or
    opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFRX or
    opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or
    opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPRX or opc = SUBMULFWD_FPMX or
    opc = SUBMULFWD_FPIX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
    opc = ADDMULSRA_FRRR or opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRRI or
    opc = ADDMULSRA_FRRF or opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMR or
    opc = ADDMULSRA_FRMM or opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or
    opc = ADDMULSRA_FRMP or opc = ADDMULSRA_FRIR or opc = ADDMULSRA_FRIM or
    opc = ADDMULSRA_FRIF or opc = ADDMULSRA_FRIP or opc = ADDMULSRA_FRFR or
    opc = ADDMULSRA_FRFM or opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRFF or
    opc = ADDMULSRA_FRFP or opc = ADDMULSRA_FRPR or opc = ADDMULSRA_FRPM or
    opc = ADDMULSRA_FRPI or opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FRPP or
    opc = ADDMULSRA_FMRR or opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or
    opc = ADDMULSRA_FMRF or opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or
    opc = ADDMULSRA_FMMI or opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or
    opc = ADDMULSRA_FMIR or opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or
    opc = ADDMULSRA_FMIP or opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or
    opc = ADDMULSRA_FMFI or opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or
    opc = ADDMULSRA_FMPR or opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or
    opc = ADDMULSRA_FMPF or opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRR or
    opc = ADDMULSRA_FIRM or opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or
    opc = ADDMULSRA_FIMR or opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or
    opc = ADDMULSRA_FIMP or opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or
    opc = ADDMULSRA_FIFF or opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or
    opc = ADDMULSRA_FIPM or opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or
    opc = ADDMULSRA_FFRR or opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or
    opc = ADDMULSRA_FFRF or opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or
    opc = ADDMULSRA_FFMM or opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or
    opc = ADDMULSRA_FFMP or opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or
    opc = ADDMULSRA_FFIF or opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or
    opc = ADDMULSRA_FFFM or opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or
    opc = ADDMULSRA_FFPM or opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or
    opc = ADDMULSRA_FPRM or opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or
    opc = ADDMULSRA_FPRP or opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or
    opc = ADDMULSRA_FPMI or opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or
    opc = ADDMULSRA_FPIR or opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or
    opc = ADDMULSRA_FPIP or opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or
    opc = ADDMULSRA_FPFI or opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or
    opc = ADDMULSRA_FPPI or
    opc = SUBMULSRA_FRRR or opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRRI or
    opc = SUBMULSRA_FRRF or opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMR or
    opc = SUBMULSRA_FRMM or opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or
    opc = SUBMULSRA_FRMP or opc = SUBMULSRA_FRIR or opc = SUBMULSRA_FRIM or
    opc = SUBMULSRA_FRIF or opc = SUBMULSRA_FRIP or opc = SUBMULSRA_FRFR or
    opc = SUBMULSRA_FRFM or opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRFF or
    opc = SUBMULSRA_FRFP or opc = SUBMULSRA_FRPR or opc = SUBMULSRA_FRPM or
    opc = SUBMULSRA_FRPI or opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FRPP or
    opc = SUBMULSRA_FMRR or opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or
    opc = SUBMULSRA_FMRF or opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or
    opc = SUBMULSRA_FMMI or opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or
    opc = SUBMULSRA_FMIR or opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or
    opc = SUBMULSRA_FMIP or opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or
    opc = SUBMULSRA_FMFI or opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or
    opc = SUBMULSRA_FMPR or opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or
    opc = SUBMULSRA_FMPF or opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRR or
    opc = SUBMULSRA_FIRM or opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or
    opc = SUBMULSRA_FIMR or opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or
    opc = SUBMULSRA_FIMP or opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or
  -- id_fifowrite
    opc = SUBMULSRA_FIFF or opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or
    opc = SUBMULSRA_FIPM or opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or
    opc = SUBMULSRA_FFRR or opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or
    opc = SUBMULSRA_FFRF or opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or
    opc = SUBMULSRA_FFMM or opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or
    opc = SUBMULSRA_FFMP or opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or
    opc = SUBMULSRA_FFIF or opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or
    opc = SUBMULSRA_FFFM or opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or
    opc = SUBMULSRA_FFPM or opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or
    opc = SUBMULSRA_FPRM or opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or
    opc = SUBMULSRA_FPRP or opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or
    opc = SUBMULSRA_FPMI or opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or
    opc = SUBMULSRA_FPIR or opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or
    opc = SUBMULSRA_FPIP or opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or
    opc = SUBMULSRA_FPFI or opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or
    opc = SUBMULSRA_FPPI or
    opc = ABSDIFF_FXRR or opc = ABSDIFF_FXRM or opc = ABSDIFF_FXRI or
    opc = ABSDIFF_FXRF or opc = ABSDIFF_FXRP or opc = ABSDIFF_FXMR or
    opc = ABSDIFF_FXMM or opc = ABSDIFF_FXMI or opc = ABSDIFF_FXMF or
    opc = ABSDIFF_FXMP or opc = ABSDIFF_FXIR or opc = ABSDIFF_FXIM or
    opc = ABSDIFF_FXIF or opc = ABSDIFF_FXIP or opc = ABSDIFF_FXFR or
    opc = ABSDIFF_FXFM or opc = ABSDIFF_FXFI or opc = ABSDIFF_FXFF or
    opc = ABSDIFF_FXFP or opc = ABSDIFF_FXPR or opc = ABSDIFF_FXPM or
    opc = ABSDIFF_FXPI or opc = ABSDIFF_FXPF or opc = ABSDIFF_FXPP or
    opc = ABSDIFFACCUM_FXRR or opc = ABSDIFFACCUM_FXRM or opc = ABSDIFFACCUM_FXRI or
    opc = ABSDIFFACCUM_FXRF or opc = ABSDIFFACCUM_FXRP or opc = ABSDIFFACCUM_FXMR or
    opc = ABSDIFFACCUM_FXMM or opc = ABSDIFFACCUM_FXMI or opc = ABSDIFFACCUM_FXMF or
    opc = ABSDIFFACCUM_FXMP or opc = ABSDIFFACCUM_FXIR or opc = ABSDIFFACCUM_FXIM or
    opc = ABSDIFFACCUM_FXIF or opc = ABSDIFFACCUM_FXIP or opc = ABSDIFFACCUM_FXFR or
    opc = ABSDIFFACCUM_FXFM or opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXFF or
    opc = ABSDIFFACCUM_FXFP or opc = ABSDIFFACCUM_FXPR or opc = ABSDIFFACCUM_FXPM or
    opc = ABSDIFFACCUM_FXPI or opc = ABSDIFFACCUM_FXPF or opc = ABSDIFFACCUM_FXPP or
    opc = DECONST_FXXR or opc = DECONST_FXXM or opc = DECONST_FXXI or
    opc = DECONST_FXXF or opc = DECONST_FXXP or
    opc = UNLDSORT_FXXX or
    opc = PUT_FXXR or opc = PUT_FXXM or opc = PUT_FXXI or
    opc = PUT_FXXF or opc = PUT_FXXP or
    opc = PUTFWD_FXXX
  else '0';

  -- getch
  o_id_rx_autoinc <= id_rx_autoinc;
  o_id_rx_reset   <= id_rx_reset;
  id_getch_gen: if GETCH_EN = true generate
    id_rx_autoinc <= '1' when (id_get_or_peak0 = '1' and fifo_aibits(0) = '1') or (opc = INCRXIDXBY1) else '0';
    id_rx_reset <= '1' when (opc = RESETRXIDX) else '0';
  end generate;

  -- putch
  o_id_tx_autoinc <= id_tx_autoinc;
  o_id_tx_reset   <= id_tx_reset;
  id_putch_gen: if PUTCH_EN = true generate
    id_tx_autoinc <= '1' when (id_fifowrite = '1' and fifo_aibits(1) = '1') or (opc = INCTXIDXBY1) else '0';
    id_tx_reset <= '1' when (opc = RESETTXIDX) else '0';
  end generate;

  -- mask
  id_maskeq_gen: if MASKEQ_EN = true generate
    o_id_setmaskeq <= '1' when
  	opc = SETMASKEQ_XXRR or opc = SETMASKEQ_XXRM or opc = SETMASKEQ_XXRI or
    opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXRP or opc = SETMASKEQ_XXMR or
    opc = SETMASKEQ_XXMM or opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXMF or
    opc = SETMASKEQ_XXMP or opc = SETMASKEQ_XXIR or opc = SETMASKEQ_XXIM or
    opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or opc = SETMASKEQ_XXFR or
    opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or opc = SETMASKEQ_XXFF or
    opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPR or opc = SETMASKEQ_XXPM or
    opc = SETMASKEQ_XXPI or opc = SETMASKEQ_XXPF or opc = SETMASKEQ_XXPP
   else '0';
  end generate;
  id_maskgt_gen: if MASKGT_EN = true generate
    o_id_setmaskgt <= '1' when
  	opc = SETMASKGT_XXRR or opc = SETMASKGT_XXRM or opc = SETMASKGT_XXRI or
    opc = SETMASKGT_XXRF or opc = SETMASKGT_XXRP or opc = SETMASKGT_XXMR or
    opc = SETMASKGT_XXMM or opc = SETMASKGT_XXMI or opc = SETMASKGT_XXMF or
    opc = SETMASKGT_XXMP or opc = SETMASKGT_XXIR or opc = SETMASKGT_XXIM or
    opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or opc = SETMASKGT_XXFR or
    opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or opc = SETMASKGT_XXFF or
    opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPR or opc = SETMASKGT_XXPM or
    opc = SETMASKGT_XXPI or opc = SETMASKGT_XXPF or opc = SETMASKGT_XXPP
    else '0';
  end generate;
  id_masklt_gen: if MASKLT_EN = true generate
    o_id_setmasklt <= '1' when
    opc = SETMASKLT_XXRR or opc = SETMASKLT_XXRM or opc = SETMASKLT_XXRI or
    opc = SETMASKLT_XXRF or opc = SETMASKLT_XXRP or opc = SETMASKLT_XXMR or
    opc = SETMASKLT_XXMM or opc = SETMASKLT_XXMI or opc = SETMASKLT_XXMF or
    opc = SETMASKLT_XXMP or opc = SETMASKLT_XXIR or opc = SETMASKLT_XXIM or
    opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or opc = SETMASKLT_XXFR or
    opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or opc = SETMASKLT_XXFF or
    opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPR or opc = SETMASKLT_XXPM or
    opc = SETMASKLT_XXPI or opc = SETMASKLT_XXPF or opc = SETMASKLT_XXPP
    else '0';
  end generate;
  id_maskle_gen: if MASKLE_EN = true generate
    o_id_setmaskle <= '1' when
    opc = SETMASKLE_XXRR or opc = SETMASKLE_XXRM or opc = SETMASKLE_XXRI or
    opc = SETMASKLE_XXRF or opc = SETMASKLE_XXRP or opc = SETMASKLE_XXMR or
    opc = SETMASKLE_XXMM or opc = SETMASKLE_XXMI or opc = SETMASKLE_XXMF or
    opc = SETMASKLE_XXMP or opc = SETMASKLE_XXIR or opc = SETMASKLE_XXIM or
    opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or opc = SETMASKLE_XXFR or
    opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or opc = SETMASKLE_XXFF or
    opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPR or opc = SETMASKLE_XXPM or
    opc = SETMASKLE_XXPI or opc = SETMASKLE_XXPF or opc = SETMASKLE_XXPP
    else '0';
  end generate;
  id_maskge_gen: if MASKGE_EN = true generate
    o_id_setmaskge <= '1' when
  	opc = SETMASKGE_XXRR or opc = SETMASKGE_XXRM or opc = SETMASKGE_XXRI or
    opc = SETMASKGE_XXRF or opc = SETMASKGE_XXRP or opc = SETMASKGE_XXMR or
    opc = SETMASKGE_XXMM or opc = SETMASKGE_XXMI or opc = SETMASKGE_XXMF or
    opc = SETMASKGE_XXMP or opc = SETMASKGE_XXIR or opc = SETMASKGE_XXIM or
    opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or opc = SETMASKGE_XXFR or
    opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or opc = SETMASKGE_XXFF or
    opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPR or opc = SETMASKGE_XXPM or
    opc = SETMASKGE_XXPI or opc = SETMASKGE_XXPF or opc = SETMASKGE_XXPP
    else '0';
  end generate;
  id_maskne_gen: if MASKNE_EN = true generate
    o_id_setmaskne <= '1' when
    	opc = SETMASKNE_XXRR or opc = SETMASKNE_XXRM or opc = SETMASKNE_XXRI or
      opc = SETMASKNE_XXRF or opc = SETMASKNE_XXRP or opc = SETMASKNE_XXMR or
      opc = SETMASKNE_XXMM or opc = SETMASKNE_XXMI or opc = SETMASKNE_XXMF or
      opc = SETMASKNE_XXMP or opc = SETMASKNE_XXIR or opc = SETMASKNE_XXIM or
      opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or opc = SETMASKNE_XXFR or
      opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or opc = SETMASKNE_XXFF or
      opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPR or opc = SETMASKNE_XXPM or
      opc = SETMASKNE_XXPI or opc = SETMASKNE_XXPF or opc = SETMASKNE_XXPP
    else '0';
  end generate;

  -- DSP48E
  real16_1_gen:
  if (DATA_WIDTH = 16 and DATA_TYPE = 1 and SLICE_NUM = 1) generate
    signal opcode : std_logic_vector(10 downto 0);
  begin
    process (opc) begin
      if opc = CLR_RXXX or opc = CLR_MXXX or opc = CLR_IXXX then
        opcode <= "00000000000"; -- 0 (CLR)
      elsif opc = PUT_FXXR or opc = PUT_FXXM or opc = PUT_FXXI or
            opc = PUT_FXXF or opc = PUT_FXXP or
            opc = GET_RXXF or opc = GET_MXXF or opc = GET_IXXF
      then
        opcode <= "01100000000"; -- c (PUT, GET)
      elsif opc = PUTFWD_FXXX then
        opcode <= "01000000000"; -- p (PUTFWD)
      elsif opc = ADDMUL_RRRR or opc = ADDMUL_RRRM or opc = ADDMUL_RRRI or
        opc = ADDMUL_RRRF or opc = ADDMUL_RRRP or opc = ADDMUL_RRMR or
        opc = ADDMUL_RRMM or opc = ADDMUL_RRMI or opc = ADDMUL_RRMF or
        opc = ADDMUL_RRMP or opc = ADDMUL_RRIR or opc = ADDMUL_RRIM or
        opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or opc = ADDMUL_RRFR or
        opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or opc = ADDMUL_RRFF or
        opc = ADDMUL_RRFP or opc = ADDMUL_RRPR or opc = ADDMUL_RRPM or
        opc = ADDMUL_RRPI or opc = ADDMUL_RRPF or opc = ADDMUL_RRPP or
        opc = ADDMUL_RMRR or opc = ADDMUL_RMRM or opc = ADDMUL_RMRI or
        opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or opc = ADDMUL_RMMR or
        opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
        opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or opc = ADDMUL_RMIF or
        opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
        opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
        opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
        opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRR or
        opc = ADDMUL_RIRM or opc = ADDMUL_RIRF or opc = ADDMUL_RIRP or
        opc = ADDMUL_RIMR or opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or
        opc = ADDMUL_RIMP or opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or
        opc = ADDMUL_RIFF or opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or
        opc = ADDMUL_RIPM or opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or
        opc = ADDMUL_RFRR or opc = ADDMUL_RFRM or opc = ADDMUL_RFRI or
        opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or opc = ADDMUL_RFMR or
        opc = ADDMUL_RFMM or opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or
        opc = ADDMUL_RFMP or opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or
        opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or opc = ADDMUL_RFFR or
        opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or opc = ADDMUL_RFPR or
        opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or opc = ADDMUL_RPRR or
        opc = ADDMUL_RPRM or opc = ADDMUL_RPRI or opc = ADDMUL_RPRF or
        opc = ADDMUL_RPRP or opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or
        opc = ADDMUL_RPMI or opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or
        opc = ADDMUL_RPIR or opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or
        opc = ADDMUL_RPIP or opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or
        opc = ADDMUL_RPFI or opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or
        opc = ADDMUL_RPPI or opc = ADDMUL_MRRR or opc = ADDMUL_MRRM or
        opc = ADDMUL_MRRI or opc = ADDMUL_MRRF or opc = ADDMUL_MRRP or
        opc = ADDMUL_MRMR or opc = ADDMUL_MRMM or opc = ADDMUL_MRMI or
        opc = ADDMUL_MRMF or opc = ADDMUL_MRMP or opc = ADDMUL_MRIR or
        opc = ADDMUL_MRIM or opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or
        opc = ADDMUL_MRFR or opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or
        opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MRPR or
        opc = ADDMUL_MRPM or opc = ADDMUL_MRPI or opc = ADDMUL_MRPF or
        opc = ADDMUL_MRPP or opc = ADDMUL_MMRR or opc = ADDMUL_MMRM or
        opc = ADDMUL_MMRI or opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or
        opc = ADDMUL_MMMR or opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or
        opc = ADDMUL_MMMP or opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or
        opc = ADDMUL_MMIF or opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or
        opc = ADDMUL_MMFM or opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or
        opc = ADDMUL_MMFP or opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or
        opc = ADDMUL_MMPI or opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or
        opc = ADDMUL_MIRR or opc = ADDMUL_MIRM or opc = ADDMUL_MIRF or
        opc = ADDMUL_MIRP or opc = ADDMUL_MIMR or opc = ADDMUL_MIMM or
        opc = ADDMUL_MIMF or opc = ADDMUL_MIMP or opc = ADDMUL_MIFR or
        opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or opc = ADDMUL_MIFP or
        opc = ADDMUL_MIPR or opc = ADDMUL_MIPM or opc = ADDMUL_MIPF or
        opc = ADDMUL_MIPP or opc = ADDMUL_MFRR or opc = ADDMUL_MFRM or
        opc = ADDMUL_MFRI or opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or
        opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or opc = ADDMUL_MFMI or
        opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or opc = ADDMUL_MFIR or
        opc = ADDMUL_MFIM or opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or
        opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
        opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or
        opc = ADDMUL_MPRR or opc = ADDMUL_MPRM or opc = ADDMUL_MPRI or
        opc = ADDMUL_MPRF or opc = ADDMUL_MPRP or opc = ADDMUL_MPMR or
        opc = ADDMUL_MPMM or opc = ADDMUL_MPMI or opc = ADDMUL_MPMF or
        opc = ADDMUL_MPMP or opc = ADDMUL_MPIR or opc = ADDMUL_MPIM or
        opc = ADDMUL_MPIF or opc = ADDMUL_MPIP or opc = ADDMUL_MPFR or
        opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or opc = ADDMUL_MPPR or
        opc = ADDMUL_MPPM or opc = ADDMUL_MPPI or opc = ADDMUL_FRRR or
        -- real16_1_gen
        opc = ADDMUL_FRRM or opc = ADDMUL_FRRI or opc = ADDMUL_FRRF or
        opc = ADDMUL_FRRP or opc = ADDMUL_FRMR or opc = ADDMUL_FRMM or
        opc = ADDMUL_FRMI or opc = ADDMUL_FRMF or opc = ADDMUL_FRMP or
        opc = ADDMUL_FRIR or opc = ADDMUL_FRIM or opc = ADDMUL_FRIF or
        opc = ADDMUL_FRIP or opc = ADDMUL_FRFR or opc = ADDMUL_FRFM or
        opc = ADDMUL_FRFI or opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or
        opc = ADDMUL_FRPR or opc = ADDMUL_FRPM or opc = ADDMUL_FRPI or
        opc = ADDMUL_FRPF or opc = ADDMUL_FRPP or opc = ADDMUL_FMRR or
        opc = ADDMUL_FMRM or opc = ADDMUL_FMRI or opc = ADDMUL_FMRF or
        opc = ADDMUL_FMRP or opc = ADDMUL_FMMR or opc = ADDMUL_FMMI or
        opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or opc = ADDMUL_FMIR or
        opc = ADDMUL_FMIM or opc = ADDMUL_FMIF or opc = ADDMUL_FMIP or
        opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or opc = ADDMUL_FMFI or
        opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or opc = ADDMUL_FMPR or
        opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or opc = ADDMUL_FMPF or
        opc = ADDMUL_FMPP or opc = ADDMUL_FIRR or opc = ADDMUL_FIRM or
        opc = ADDMUL_FIRF or opc = ADDMUL_FIRP or opc = ADDMUL_FIMR or
        opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or opc = ADDMUL_FIMP or
        opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
        opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or opc = ADDMUL_FIPM or
        opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or opc = ADDMUL_FFRR or
        opc = ADDMUL_FFRM or opc = ADDMUL_FFRI or opc = ADDMUL_FFRF or
        opc = ADDMUL_FFRP or opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or
        opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or
        opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or opc = ADDMUL_FFIF or
        opc = ADDMUL_FFIP or opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or
        opc = ADDMUL_FFFI or opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or
        opc = ADDMUL_FFPI or opc = ADDMUL_FPRR or opc = ADDMUL_FPRM or
        opc = ADDMUL_FPRI or opc = ADDMUL_FPRF or opc = ADDMUL_FPRP or
        opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or opc = ADDMUL_FPMI or
        opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or opc = ADDMUL_FPIR or
        opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or opc = ADDMUL_FPIP or
        opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
        -- real16_1_gen
        opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or opc = ADDMUL_FPPI or
        opc = ADDMULSRA_RRRR or opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRRI or
        opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMR or
        opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or
        opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIR or opc = ADDMULSRA_RRIM or
        opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or opc = ADDMULSRA_RRFR or
        opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRFF or
        opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or opc = ADDMULSRA_RRPM or
        opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RRPP or
        opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
        opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
        opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
        opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
        opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
        opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
        opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
        opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRR or
        opc = ADDMULSRA_RIRM or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or
        opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
        opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or
        opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or
        opc = ADDMULSRA_RIPM or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
        opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or
        opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or
        opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or
        opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
        opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or
        opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or
        opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or
        opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or
        opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
        opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
        opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
        opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or
        opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or
        opc = ADDMULSRA_RPPI or opc = ADDMULSRA_MRRR or opc = ADDMULSRA_MRRM or
        opc = ADDMULSRA_MRRI or opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or
        opc = ADDMULSRA_MRMR or opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MRMI or
        -- real16_1_gen
        opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIR or
        opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
        opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
        opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or
        opc = ADDMULSRA_MRPM or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or
        opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or
        opc = ADDMULSRA_MMRI or opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or
        opc = ADDMULSRA_MMMR or opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or
        opc = ADDMULSRA_MMMP or opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or
        opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or
        opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or
        opc = ADDMULSRA_MMFP or opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or
        opc = ADDMULSRA_MMPI or opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or
        opc = ADDMULSRA_MIRR or opc = ADDMULSRA_MIRM or opc = ADDMULSRA_MIRF or
        opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or
        opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFR or
        opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIFP or
        opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or opc = ADDMULSRA_MIPF or
        opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or
        opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or
        opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or
        opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or
        opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
        opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
        opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
        opc = ADDMULSRA_MPRR or opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPRI or
        opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMR or
        opc = ADDMULSRA_MPMM or opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or
        opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or
        opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFR or
        opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPR or
        opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or opc = ADDMULSRA_FRRR or
        opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRRI or opc = ADDMULSRA_FRRF or
        opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMR or opc = ADDMULSRA_FRMM or
        opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRMP or
        opc = ADDMULSRA_FRIR or opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRIF or
        opc = ADDMULSRA_FRIP or opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or
        opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or
        -- real16_1_gen
        opc = ADDMULSRA_FRPR or opc = ADDMULSRA_FRPM or opc = ADDMULSRA_FRPI or
        opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMRR or
        opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or opc = ADDMULSRA_FMRF or
        opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or opc = ADDMULSRA_FMMI or
        opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or opc = ADDMULSRA_FMIR or
        opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMIP or
        opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMFI or
        opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or opc = ADDMULSRA_FMPR or
        opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or opc = ADDMULSRA_FMPF or
        opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRR or opc = ADDMULSRA_FIRM or
        opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMR or
        opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
        opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
        opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
        opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRR or
        opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or
        opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
        opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
        -- real16_1_gen
        opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or
        opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or
        opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or
        opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or opc = ADDMULSRA_FPRM or
        opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or
        opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or opc = ADDMULSRA_FPMI or
        opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIR or
        opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
        opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
        opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI
      then
        opcode <= "01101010000"; -- c+a*b
      elsif opc = SUBMUL_RRRR or opc = SUBMUL_RRRM or opc = SUBMUL_RRRI or
        opc = SUBMUL_RRRF or opc = SUBMUL_RRRP or opc = SUBMUL_RRMR or
        opc = SUBMUL_RRMM or opc = SUBMUL_RRMI or opc = SUBMUL_RRMF or
        opc = SUBMUL_RRMP or opc = SUBMUL_RRIR or opc = SUBMUL_RRIM or
        opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or opc = SUBMUL_RRFR or
        opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or opc = SUBMUL_RRFF or
        opc = SUBMUL_RRFP or opc = SUBMUL_RRPR or opc = SUBMUL_RRPM or
        opc = SUBMUL_RRPI or opc = SUBMUL_RRPF or opc = SUBMUL_RRPP or
        opc = SUBMUL_RMRR or opc = SUBMUL_RMRM or opc = SUBMUL_RMRI or
        opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or opc = SUBMUL_RMMR or
        opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
        opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or opc = SUBMUL_RMIF or
        opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
        opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
        opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
        opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRR or
        opc = SUBMUL_RIRM or opc = SUBMUL_RIRF or opc = SUBMUL_RIRP or
        opc = SUBMUL_RIMR or opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or
        opc = SUBMUL_RIMP or opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or
        opc = SUBMUL_RIFF or opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or
        opc = SUBMUL_RIPM or opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or
        opc = SUBMUL_RFRR or opc = SUBMUL_RFRM or opc = SUBMUL_RFRI or
        opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or opc = SUBMUL_RFMR or
        opc = SUBMUL_RFMM or opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or
        opc = SUBMUL_RFMP or opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or
        opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or opc = SUBMUL_RFFR or
        opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or opc = SUBMUL_RFPR or
        -- real16_1_gen
        opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or opc = SUBMUL_RPRR or
        opc = SUBMUL_RPRM or opc = SUBMUL_RPRI or opc = SUBMUL_RPRF or
        opc = SUBMUL_RPRP or opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or
        opc = SUBMUL_RPMI or opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or
        opc = SUBMUL_RPIR or opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or
        opc = SUBMUL_RPIP or opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or
        opc = SUBMUL_RPFI or opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or
        opc = SUBMUL_RPPI or opc = SUBMUL_MRRR or opc = SUBMUL_MRRM or
        opc = SUBMUL_MRRI or opc = SUBMUL_MRRF or opc = SUBMUL_MRRP or
        opc = SUBMUL_MRMR or opc = SUBMUL_MRMM or opc = SUBMUL_MRMI or
        opc = SUBMUL_MRMF or opc = SUBMUL_MRMP or opc = SUBMUL_MRIR or
        opc = SUBMUL_MRIM or opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or
        opc = SUBMUL_MRFR or opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or
        opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MRPR or
        opc = SUBMUL_MRPM or opc = SUBMUL_MRPI or opc = SUBMUL_MRPF or
        opc = SUBMUL_MRPP or opc = SUBMUL_MMRR or opc = SUBMUL_MMRM or
        opc = SUBMUL_MMRI or opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or
        opc = SUBMUL_MMMR or opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or
        opc = SUBMUL_MMMP or opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or
        opc = SUBMUL_MMIF or opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or
        opc = SUBMUL_MMFM or opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or
        opc = SUBMUL_MMFP or opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or
        opc = SUBMUL_MMPI or opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or
        opc = SUBMUL_MIRR or opc = SUBMUL_MIRM or opc = SUBMUL_MIRF or
        opc = SUBMUL_MIRP or opc = SUBMUL_MIMR or opc = SUBMUL_MIMM or
        opc = SUBMUL_MIMF or opc = SUBMUL_MIMP or opc = SUBMUL_MIFR or
        opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or opc = SUBMUL_MIFP or
        opc = SUBMUL_MIPR or opc = SUBMUL_MIPM or opc = SUBMUL_MIPF or
        opc = SUBMUL_MIPP or opc = SUBMUL_MFRR or opc = SUBMUL_MFRM or
        opc = SUBMUL_MFRI or opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or
        -- real16_1_gen
        opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or opc = SUBMUL_MFMI or
        opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or opc = SUBMUL_MFIR or
        opc = SUBMUL_MFIM or opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or
        opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
        opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or
        opc = SUBMUL_MPRR or opc = SUBMUL_MPRM or opc = SUBMUL_MPRI or
        opc = SUBMUL_MPRF or opc = SUBMUL_MPRP or opc = SUBMUL_MPMR or
        opc = SUBMUL_MPMM or opc = SUBMUL_MPMI or opc = SUBMUL_MPMF or
        opc = SUBMUL_MPMP or opc = SUBMUL_MPIR or opc = SUBMUL_MPIM or
        opc = SUBMUL_MPIF or opc = SUBMUL_MPIP or opc = SUBMUL_MPFR or
        opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or opc = SUBMUL_MPPR or
        opc = SUBMUL_MPPM or opc = SUBMUL_MPPI or opc = SUBMUL_FRRR or
        opc = SUBMUL_FRRM or opc = SUBMUL_FRRI or opc = SUBMUL_FRRF or
        opc = SUBMUL_FRRP or opc = SUBMUL_FRMR or opc = SUBMUL_FRMM or
        opc = SUBMUL_FRMI or opc = SUBMUL_FRMF or opc = SUBMUL_FRMP or
        opc = SUBMUL_FRIR or opc = SUBMUL_FRIM or opc = SUBMUL_FRIF or
        opc = SUBMUL_FRIP or opc = SUBMUL_FRFR or opc = SUBMUL_FRFM or
        opc = SUBMUL_FRFI or opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or
        opc = SUBMUL_FRPR or opc = SUBMUL_FRPM or opc = SUBMUL_FRPI or
        opc = SUBMUL_FRPF or opc = SUBMUL_FRPP or opc = SUBMUL_FMRR or
        opc = SUBMUL_FMRM or opc = SUBMUL_FMRI or opc = SUBMUL_FMRF or
        opc = SUBMUL_FMRP or opc = SUBMUL_FMMR or opc = SUBMUL_FMMI or
        opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or opc = SUBMUL_FMIR or
        opc = SUBMUL_FMIM or opc = SUBMUL_FMIF or opc = SUBMUL_FMIP or
        opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or opc = SUBMUL_FMFI or
        opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or opc = SUBMUL_FMPR or
        opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or opc = SUBMUL_FMPF or
        opc = SUBMUL_FMPP or opc = SUBMUL_FIRR or opc = SUBMUL_FIRM or
        opc = SUBMUL_FIRF or opc = SUBMUL_FIRP or opc = SUBMUL_FIMR or
        opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or opc = SUBMUL_FIMP or
        opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
        opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or opc = SUBMUL_FIPM or
        opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or opc = SUBMUL_FFRR or
        opc = SUBMUL_FFRM or opc = SUBMUL_FFRI or opc = SUBMUL_FFRF or
        opc = SUBMUL_FFRP or opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or
        opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or
        opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or opc = SUBMUL_FFIF or
        opc = SUBMUL_FFIP or opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or
        opc = SUBMUL_FFFI or opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or
        opc = SUBMUL_FFPI or opc = SUBMUL_FPRR or opc = SUBMUL_FPRM or
        opc = SUBMUL_FPRI or opc = SUBMUL_FPRF or opc = SUBMUL_FPRP or
        opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or opc = SUBMUL_FPMI or
        opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or opc = SUBMUL_FPIR or
        opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or opc = SUBMUL_FPIP or
        opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
        opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or opc = SUBMUL_FPPI or
        opc = SUBMULSRA_RRRR or opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRRI or
        opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMR or
        opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or
        opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIR or opc = SUBMULSRA_RRIM or
        opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or opc = SUBMULSRA_RRFR or
        opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRFF or
        opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or opc = SUBMULSRA_RRPM or
        opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RRPP or
        opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
        opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
        opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
        opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
        opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
        opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
        opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
        opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRR or
        -- real16_1_gen
        opc = SUBMULSRA_RIRM or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or
        opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
        opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or
        opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or
        opc = SUBMULSRA_RIPM or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
        opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or
        opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or
        opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or
        opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
        opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or
        opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or
        opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or
        opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or
        opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
        opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
        opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
        opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or
        opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or
        opc = SUBMULSRA_RPPI or opc = SUBMULSRA_MRRR or opc = SUBMULSRA_MRRM or
        opc = SUBMULSRA_MRRI or opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or
        opc = SUBMULSRA_MRMR or opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MRMI or
        opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIR or
        opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
        opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
        opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or
        opc = SUBMULSRA_MRPM or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or
        opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or
        opc = SUBMULSRA_MMRI or opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or
        opc = SUBMULSRA_MMMR or opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or
        opc = SUBMULSRA_MMMP or opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or
        opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or
        opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or
        opc = SUBMULSRA_MMFP or opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or
        opc = SUBMULSRA_MMPI or opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or
        opc = SUBMULSRA_MIRR or opc = SUBMULSRA_MIRM or opc = SUBMULSRA_MIRF or
        -- real16_1_gen
        opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or
        opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFR or
        opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIFP or
        opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or opc = SUBMULSRA_MIPF or
        opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or
        opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or
        opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or
        opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or
        opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
        opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
        opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
        opc = SUBMULSRA_MPRR or opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPRI or
        opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMR or
        opc = SUBMULSRA_MPMM or opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or
        opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or
        opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFR or
        opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPR or
        opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or opc = SUBMULSRA_FRRR or
        opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRRI or opc = SUBMULSRA_FRRF or
        opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMR or opc = SUBMULSRA_FRMM or
        opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRMP or
        opc = SUBMULSRA_FRIR or opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRIF or
        opc = SUBMULSRA_FRIP or opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or
        opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or
        opc = SUBMULSRA_FRPR or opc = SUBMULSRA_FRPM or opc = SUBMULSRA_FRPI or
        opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMRR or
        opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or opc = SUBMULSRA_FMRF or
        opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or opc = SUBMULSRA_FMMI or
        opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or opc = SUBMULSRA_FMIR or
        opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMIP or
        opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMFI or
        opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or opc = SUBMULSRA_FMPR or
        opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or opc = SUBMULSRA_FMPF or
        opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRR or opc = SUBMULSRA_FIRM or
        opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMR or
        opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
        opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
        opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
        opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRR or
        opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or
        opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
        opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
        opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or
        opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or
        opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or
        opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or opc = SUBMULSRA_FPRM or
        opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or
        opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or opc = SUBMULSRA_FPMI or
        opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIR or
        opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
        opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
        opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI or
        opc = SETMASKLT_XXRR or opc = SETMASKLT_XXRM or opc = SETMASKLT_XXRI or
        opc = SETMASKLT_XXRF or opc = SETMASKLT_XXRP or opc = SETMASKLT_XXMR or
        opc = SETMASKLT_XXMM or opc = SETMASKLT_XXMI or opc = SETMASKLT_XXMF or
        opc = SETMASKLT_XXMP or opc = SETMASKLT_XXIR or opc = SETMASKLT_XXIM or
        opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or opc = SETMASKLT_XXFR or
        opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or opc = SETMASKLT_XXFF or
        opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPR or opc = SETMASKLT_XXPM or
        opc = SETMASKLT_XXPI or opc = SETMASKLT_XXPF or opc = SETMASKLT_XXPP or
        opc = SETMASKGT_XXRR or opc = SETMASKGT_XXRM or opc = SETMASKGT_XXRI or
        opc = SETMASKGT_XXRF or opc = SETMASKGT_XXRP or opc = SETMASKGT_XXMR or
        -- real16_1_gen
        opc = SETMASKGT_XXMM or opc = SETMASKGT_XXMI or opc = SETMASKGT_XXMF or
        opc = SETMASKGT_XXMP or opc = SETMASKGT_XXIR or opc = SETMASKGT_XXIM or
        opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or opc = SETMASKGT_XXFR or
        opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or opc = SETMASKGT_XXFF or
        opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPR or opc = SETMASKGT_XXPM or
        opc = SETMASKGT_XXPI or opc = SETMASKGT_XXPF or opc = SETMASKGT_XXPP or
        opc = SETMASKEQ_XXRR or opc = SETMASKEQ_XXRM or opc = SETMASKEQ_XXRI or
        opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXRP or opc = SETMASKEQ_XXMR or
        opc = SETMASKEQ_XXMM or opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXMF or
        opc = SETMASKEQ_XXMP or opc = SETMASKEQ_XXIR or opc = SETMASKEQ_XXIM or
        opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or opc = SETMASKEQ_XXFR or
        opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or opc = SETMASKEQ_XXFF or
        opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPR or opc = SETMASKEQ_XXPM or
        opc = SETMASKEQ_XXPI or opc = SETMASKEQ_XXPF or opc = SETMASKEQ_XXPP or
        opc = SETMASKGE_XXRR or opc = SETMASKGE_XXRM or opc = SETMASKGE_XXRI or
        opc = SETMASKGE_XXRF or opc = SETMASKGE_XXRP or opc = SETMASKGE_XXMR or
        opc = SETMASKGE_XXMM or opc = SETMASKGE_XXMI or opc = SETMASKGE_XXMF or
        opc = SETMASKGE_XXMP or opc = SETMASKGE_XXIR or opc = SETMASKGE_XXIM or
        opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or opc = SETMASKGE_XXFR or
        opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or opc = SETMASKGE_XXFF or
        opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPR or opc = SETMASKGE_XXPM or
        opc = SETMASKGE_XXPI or opc = SETMASKGE_XXPF or opc = SETMASKGE_XXPP or
        opc = SETMASKLE_XXRR or opc = SETMASKLE_XXRM or opc = SETMASKLE_XXRI or
        opc = SETMASKLE_XXRF or opc = SETMASKLE_XXRP or opc = SETMASKLE_XXMR or
        opc = SETMASKLE_XXMM or opc = SETMASKLE_XXMI or opc = SETMASKLE_XXMF or
        opc = SETMASKLE_XXMP or opc = SETMASKLE_XXIR or opc = SETMASKLE_XXIM or
        opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or opc = SETMASKLE_XXFR or
        opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or opc = SETMASKLE_XXFF or
        opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPR or opc = SETMASKLE_XXPM or
        opc = SETMASKLE_XXPI or opc = SETMASKLE_XXPF or opc = SETMASKLE_XXPP or
        opc = SETMASKNE_XXRR or opc = SETMASKNE_XXRM or opc = SETMASKNE_XXRI or
        opc = SETMASKNE_XXRF or opc = SETMASKNE_XXRP or opc = SETMASKNE_XXMR or
        opc = SETMASKNE_XXMM or opc = SETMASKNE_XXMI or opc = SETMASKNE_XXMF or
        opc = SETMASKNE_XXMP or opc = SETMASKNE_XXIR or opc = SETMASKNE_XXIM or
        opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or opc = SETMASKNE_XXFR or
        opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or opc = SETMASKNE_XXFF or
        opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPR or opc = SETMASKNE_XXPM or
        opc = SETMASKNE_XXPI or opc = SETMASKNE_XXPF or opc = SETMASKNE_XXPP or
        opc = CMP_XXRR or opc = CMP_XXRM or opc = CMP_XXRI or
        opc = CMP_XXRF or opc = CMP_XXRP or opc = CMP_XXMR or
        opc = CMP_XXMM or opc = CMP_XXMI or opc = CMP_XXMF or
        opc = CMP_XXMP or opc = CMP_XXIR or opc = CMP_XXIM or
        opc = CMP_XXIF or opc = CMP_XXIP or opc = CMP_XXFR or
        opc = CMP_XXFM or opc = CMP_XXFI or opc = CMP_XXFF or
        opc = CMP_XXFP or opc = CMP_XXPR or opc = CMP_XXPM or
        opc = CMP_XXPI or opc = CMP_XXPF or opc = CMP_XXPP
      then
        opcode <= "01101010011"; -- c-a*b
      elsif opc = ADDMULFWD_RRRX or opc = ADDMULFWD_RRMX or opc = ADDMULFWD_RRIX or
        opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RRPX or opc = ADDMULFWD_RMRX or
        opc = ADDMULFWD_RMMX or opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RMFX or
        opc = ADDMULFWD_RMPX or opc = ADDMULFWD_RIRX or opc = ADDMULFWD_RIMX or
        opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or opc = ADDMULFWD_RFRX or
        opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or opc = ADDMULFWD_RFFX or
        opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPRX or opc = ADDMULFWD_RPMX or
        opc = ADDMULFWD_RPIX or opc = ADDMULFWD_RPFX or opc = ADDMULFWD_RPPX or
        -- real16_1_gen
        opc = ADDMULFWD_MRRX or opc = ADDMULFWD_MRMX or opc = ADDMULFWD_MRIX or
        opc = ADDMULFWD_MRFX or opc = ADDMULFWD_MRPX or opc = ADDMULFWD_MMRX or
        opc = ADDMULFWD_MMMX or opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MMFX or
        opc = ADDMULFWD_MMPX or opc = ADDMULFWD_MIRX or opc = ADDMULFWD_MIMX or
        opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFRX or
        opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or
        opc = ADDMULFWD_MFPX or opc = ADDMULFWD_MPRX or opc = ADDMULFWD_MPMX or
        opc = ADDMULFWD_MPIX or opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or
        opc = ADDMULFWD_FRRX or opc = ADDMULFWD_FRMX or opc = ADDMULFWD_FRIX or
        opc = ADDMULFWD_FRFX or opc = ADDMULFWD_FRPX or opc = ADDMULFWD_FMRX or
        opc = ADDMULFWD_FMMX or opc = ADDMULFWD_FMIX or opc = ADDMULFWD_FMFX or
        opc = ADDMULFWD_FMPX or opc = ADDMULFWD_FIRX or opc = ADDMULFWD_FIMX or
        opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFRX or
        opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or
        opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPRX or opc = ADDMULFWD_FPMX or
        opc = ADDMULFWD_FPIX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX
      then
        opcode <= "01001010000"; -- p+a*b
      elsif opc = SUBMULFWD_RRRX or opc = SUBMULFWD_RRMX or opc = SUBMULFWD_RRIX or
        opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RRPX or opc = SUBMULFWD_RMRX or
        opc = SUBMULFWD_RMMX or opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RMFX or
        opc = SUBMULFWD_RMPX or opc = SUBMULFWD_RIRX or opc = SUBMULFWD_RIMX or
        opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or opc = SUBMULFWD_RFRX or
        opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or opc = SUBMULFWD_RFFX or
        opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPRX or opc = SUBMULFWD_RPMX or
        opc = SUBMULFWD_RPIX or opc = SUBMULFWD_RPFX or opc = SUBMULFWD_RPPX or
        opc = SUBMULFWD_MRRX or opc = SUBMULFWD_MRMX or opc = SUBMULFWD_MRIX or
        opc = SUBMULFWD_MRFX or opc = SUBMULFWD_MRPX or opc = SUBMULFWD_MMRX or
        opc = SUBMULFWD_MMMX or opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MMFX or
        opc = SUBMULFWD_MMPX or opc = SUBMULFWD_MIRX or opc = SUBMULFWD_MIMX or
        opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFRX or
        opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or
        opc = SUBMULFWD_MFPX or opc = SUBMULFWD_MPRX or opc = SUBMULFWD_MPMX or
        opc = SUBMULFWD_MPIX or opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or
        opc = SUBMULFWD_FRRX or opc = SUBMULFWD_FRMX or opc = SUBMULFWD_FRIX or
        -- real16_1_gen
        opc = SUBMULFWD_FRFX or opc = SUBMULFWD_FRPX or opc = SUBMULFWD_FMRX or
        opc = SUBMULFWD_FMMX or opc = SUBMULFWD_FMIX or opc = SUBMULFWD_FMFX or
        opc = SUBMULFWD_FMPX or opc = SUBMULFWD_FIRX or opc = SUBMULFWD_FIMX or
        opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFRX or
        opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or
        opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPRX or opc = SUBMULFWD_FPMX or
        opc = SUBMULFWD_FPIX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
        opc = CMPFWD_XXRX or opc = CMPFWD_XXMX or opc = CMPFWD_XXIX or
        opc = CMPFWD_XXFX or opc = CMPFWD_XXPX
      then
        opcode <= "01001010011"; -- p-a*b
      else
        opcode <= "00000000000";
      end if;
    end process;

    o_id_opmode <= opcode(10 downto 4);
    o_id_alumode <= opcode(3 downto 0);
  end generate;

  REAL32_4_GEN: if (DATA_WIDTH = 32 and DATA_TYPE = 1 and SLICE_NUM = 4) generate
    signal opcode : std_logic_vector(10 downto 0);
  begin
    process (opc) begin
      if opc = CLR_RXXX or opc = CLR_MXXX or opc = CLR_IXXX then
        opcode <= "00000000000";
      elsif opc = PUT_FXXR or opc = PUT_FXXM or opc = PUT_FXXI or
        opc = PUT_FXXF or opc = PUT_FXXP or
        opc = GET_RXXF or opc = GET_MXXF or opc = GET_IXXF
  		then
        opcode <= "01100000000"; -- c
      elsif opc = PUTFWD_FXXX then
        opcode <= "01000000000"; -- p (PUTFWD)
      elsif opc = ADDMUL_RRRR or opc = ADDMUL_RRRM or opc = ADDMUL_RRRI or
        opc = ADDMUL_RRRF or opc = ADDMUL_RRRP or opc = ADDMUL_RRMR or
        opc = ADDMUL_RRMM or opc = ADDMUL_RRMI or opc = ADDMUL_RRMF or
        opc = ADDMUL_RRMP or opc = ADDMUL_RRIR or opc = ADDMUL_RRIM or
        opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or opc = ADDMUL_RRFR or
        opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or opc = ADDMUL_RRFF or
        opc = ADDMUL_RRFP or opc = ADDMUL_RRPR or opc = ADDMUL_RRPM or
        opc = ADDMUL_RRPI or opc = ADDMUL_RRPF or opc = ADDMUL_RRPP or
        opc = ADDMUL_RMRR or opc = ADDMUL_RMRM or opc = ADDMUL_RMRI or
        opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or opc = ADDMUL_RMMR or
        opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
        opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or opc = ADDMUL_RMIF or
        opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
        opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
        opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
        opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRR or
        opc = ADDMUL_RIRM or opc = ADDMUL_RIRF or opc = ADDMUL_RIRP or
        opc = ADDMUL_RIMR or opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or
        opc = ADDMUL_RIMP or opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or
        opc = ADDMUL_RIFF or opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or
        opc = ADDMUL_RIPM or opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or
        opc = ADDMUL_RFRR or opc = ADDMUL_RFRM or opc = ADDMUL_RFRI or
        opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or opc = ADDMUL_RFMR or
        opc = ADDMUL_RFMM or opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or
        opc = ADDMUL_RFMP or opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or
        -- real32_4_gen
        opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or opc = ADDMUL_RFFR or
        opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or opc = ADDMUL_RFPR or
        opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or opc = ADDMUL_RPRR or
        opc = ADDMUL_RPRM or opc = ADDMUL_RPRI or opc = ADDMUL_RPRF or
        opc = ADDMUL_RPRP or opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or
        opc = ADDMUL_RPMI or opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or
        opc = ADDMUL_RPIR or opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or
        opc = ADDMUL_RPIP or opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or
        opc = ADDMUL_RPFI or opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or
        opc = ADDMUL_RPPI or opc = ADDMUL_MRRR or opc = ADDMUL_MRRM or
        opc = ADDMUL_MRRI or opc = ADDMUL_MRRF or opc = ADDMUL_MRRP or
        opc = ADDMUL_MRMR or opc = ADDMUL_MRMM or opc = ADDMUL_MRMI or
        opc = ADDMUL_MRMF or opc = ADDMUL_MRMP or opc = ADDMUL_MRIR or
        opc = ADDMUL_MRIM or opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or
        opc = ADDMUL_MRFR or opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or
        opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MRPR or
        opc = ADDMUL_MRPM or opc = ADDMUL_MRPI or opc = ADDMUL_MRPF or
        opc = ADDMUL_MRPP or opc = ADDMUL_MMRR or opc = ADDMUL_MMRM or
        opc = ADDMUL_MMRI or opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or
        opc = ADDMUL_MMMR or opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or
        opc = ADDMUL_MMMP or opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or
        opc = ADDMUL_MMIF or opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or
        opc = ADDMUL_MMFM or opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or
        opc = ADDMUL_MMFP or opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or
        opc = ADDMUL_MMPI or opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or
        opc = ADDMUL_MIRR or opc = ADDMUL_MIRM or opc = ADDMUL_MIRF or
        opc = ADDMUL_MIRP or opc = ADDMUL_MIMR or opc = ADDMUL_MIMM or
        opc = ADDMUL_MIMF or opc = ADDMUL_MIMP or opc = ADDMUL_MIFR or
        opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or opc = ADDMUL_MIFP or
        opc = ADDMUL_MIPR or opc = ADDMUL_MIPM or opc = ADDMUL_MIPF or
        opc = ADDMUL_MIPP or opc = ADDMUL_MFRR or opc = ADDMUL_MFRM or
        opc = ADDMUL_MFRI or opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or
        opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or opc = ADDMUL_MFMI or
        opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or opc = ADDMUL_MFIR or
        opc = ADDMUL_MFIM or opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or
        opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
        opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or
        opc = ADDMUL_MPRR or opc = ADDMUL_MPRM or opc = ADDMUL_MPRI or
        opc = ADDMUL_MPRF or opc = ADDMUL_MPRP or opc = ADDMUL_MPMR or
        opc = ADDMUL_MPMM or opc = ADDMUL_MPMI or opc = ADDMUL_MPMF or
        opc = ADDMUL_MPMP or opc = ADDMUL_MPIR or opc = ADDMUL_MPIM or
        opc = ADDMUL_MPIF or opc = ADDMUL_MPIP or opc = ADDMUL_MPFR or
        opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or opc = ADDMUL_MPPR or
        opc = ADDMUL_MPPM or opc = ADDMUL_MPPI or opc = ADDMUL_FRRR or
        opc = ADDMUL_FRRM or opc = ADDMUL_FRRI or opc = ADDMUL_FRRF or
        opc = ADDMUL_FRRP or opc = ADDMUL_FRMR or opc = ADDMUL_FRMM or
        opc = ADDMUL_FRMI or opc = ADDMUL_FRMF or opc = ADDMUL_FRMP or
        opc = ADDMUL_FRIR or opc = ADDMUL_FRIM or opc = ADDMUL_FRIF or
        opc = ADDMUL_FRIP or opc = ADDMUL_FRFR or opc = ADDMUL_FRFM or
        opc = ADDMUL_FRFI or opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or
        opc = ADDMUL_FRPR or opc = ADDMUL_FRPM or opc = ADDMUL_FRPI or
        opc = ADDMUL_FRPF or opc = ADDMUL_FRPP or opc = ADDMUL_FMRR or
        opc = ADDMUL_FMRM or opc = ADDMUL_FMRI or opc = ADDMUL_FMRF or
        opc = ADDMUL_FMRP or opc = ADDMUL_FMMR or opc = ADDMUL_FMMI or
        opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or opc = ADDMUL_FMIR or
        opc = ADDMUL_FMIM or opc = ADDMUL_FMIF or opc = ADDMUL_FMIP or
        opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or opc = ADDMUL_FMFI or
        opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or opc = ADDMUL_FMPR or
        -- real32_4_gen
        opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or opc = ADDMUL_FMPF or
        opc = ADDMUL_FMPP or opc = ADDMUL_FIRR or opc = ADDMUL_FIRM or
        opc = ADDMUL_FIRF or opc = ADDMUL_FIRP or opc = ADDMUL_FIMR or
        opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or opc = ADDMUL_FIMP or
        opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
        opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or opc = ADDMUL_FIPM or
        opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or opc = ADDMUL_FFRR or
        opc = ADDMUL_FFRM or opc = ADDMUL_FFRI or opc = ADDMUL_FFRF or
        opc = ADDMUL_FFRP or opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or
        opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or
        opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or opc = ADDMUL_FFIF or
        opc = ADDMUL_FFIP or opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or
        opc = ADDMUL_FFFI or opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or
        opc = ADDMUL_FFPI or opc = ADDMUL_FPRR or opc = ADDMUL_FPRM or
        opc = ADDMUL_FPRI or opc = ADDMUL_FPRF or opc = ADDMUL_FPRP or
        opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or opc = ADDMUL_FPMI or
        opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or opc = ADDMUL_FPIR or
        opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or opc = ADDMUL_FPIP or
        opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
        opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or opc = ADDMUL_FPPI or
        opc = ADDMULSRA_RRRR or opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRRI or
        opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMR or
        opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or
        opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIR or opc = ADDMULSRA_RRIM or
        opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or opc = ADDMULSRA_RRFR or
        opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRFF or
        opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or opc = ADDMULSRA_RRPM or
        opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RRPP or
        opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
        opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
        -- real32_4_gen
        opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
        opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
        opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
        opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
        opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
        opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRR or
        opc = ADDMULSRA_RIRM or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or
        opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
        opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or
        opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or
        opc = ADDMULSRA_RIPM or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
        opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or
        opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or
        opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or
        opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
        opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or
        opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or
        opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or
        opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or
        opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
        opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
        opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
        opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or
        opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or
        opc = ADDMULSRA_RPPI or opc = ADDMULSRA_MRRR or opc = ADDMULSRA_MRRM or
        opc = ADDMULSRA_MRRI or opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or
        opc = ADDMULSRA_MRMR or opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MRMI or
        opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIR or
        opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
        opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
        opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or
        opc = ADDMULSRA_MRPM or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or
        opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or
        opc = ADDMULSRA_MMRI or opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or
        opc = ADDMULSRA_MMMR or opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or
        opc = ADDMULSRA_MMMP or opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or
        opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or
        opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or
        opc = ADDMULSRA_MMFP or opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or
        opc = ADDMULSRA_MMPI or opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or
        opc = ADDMULSRA_MIRR or opc = ADDMULSRA_MIRM or opc = ADDMULSRA_MIRF or
        -- real32_4_gen
        opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or
        opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFR or
        opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIFP or
        opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or opc = ADDMULSRA_MIPF or
        opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or
        opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or
        opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or
        opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or
        opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
        opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
        opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
        opc = ADDMULSRA_MPRR or opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPRI or
        opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMR or
        opc = ADDMULSRA_MPMM or opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or
        opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or
        opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFR or
        opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPR or
        opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or opc = ADDMULSRA_FRRR or
        opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRRI or opc = ADDMULSRA_FRRF or
        opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMR or opc = ADDMULSRA_FRMM or
        opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRMP or
        opc = ADDMULSRA_FRIR or opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRIF or
        opc = ADDMULSRA_FRIP or opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or
        opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or
        opc = ADDMULSRA_FRPR or opc = ADDMULSRA_FRPM or opc = ADDMULSRA_FRPI or
        opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMRR or
        opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or opc = ADDMULSRA_FMRF or
        opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or opc = ADDMULSRA_FMMI or
        opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or opc = ADDMULSRA_FMIR or
        opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMIP or
        opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMFI or
        opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or opc = ADDMULSRA_FMPR or
        opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or opc = ADDMULSRA_FMPF or
        opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRR or opc = ADDMULSRA_FIRM or
        opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMR or
        opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
        opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
        opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
        opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRR or
        opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or
        opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
        -- real32_4_gen
        opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
        opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or
        opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or
        opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or
        opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or opc = ADDMULSRA_FPRM or
        opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or
        opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or opc = ADDMULSRA_FPMI or
        opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIR or
        opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
        opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
        opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI
      then
        opcode <= "01100110000"; -- c+a*b
      elsif opc = SUBMUL_RRRR or opc = SUBMUL_RRRM or opc = SUBMUL_RRRI or
        opc = SUBMUL_RRRF or opc = SUBMUL_RRRP or opc = SUBMUL_RRMR or
        opc = SUBMUL_RRMM or opc = SUBMUL_RRMI or opc = SUBMUL_RRMF or
        opc = SUBMUL_RRMP or opc = SUBMUL_RRIR or opc = SUBMUL_RRIM or
        opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or opc = SUBMUL_RRFR or
        opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or opc = SUBMUL_RRFF or
        opc = SUBMUL_RRFP or opc = SUBMUL_RRPR or opc = SUBMUL_RRPM or
        opc = SUBMUL_RRPI or opc = SUBMUL_RRPF or opc = SUBMUL_RRPP or
        opc = SUBMUL_RMRR or opc = SUBMUL_RMRM or opc = SUBMUL_RMRI or
        opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or opc = SUBMUL_RMMR or
        opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
        opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or opc = SUBMUL_RMIF or
        opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
        opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
        opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
        opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRR or
        opc = SUBMUL_RIRM or opc = SUBMUL_RIRF or opc = SUBMUL_RIRP or
        opc = SUBMUL_RIMR or opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or
        opc = SUBMUL_RIMP or opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or
        -- real32_4_gen
        opc = SUBMUL_RIFF or opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or
        opc = SUBMUL_RIPM or opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or
        opc = SUBMUL_RFRR or opc = SUBMUL_RFRM or opc = SUBMUL_RFRI or
        opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or opc = SUBMUL_RFMR or
        opc = SUBMUL_RFMM or opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or
        opc = SUBMUL_RFMP or opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or
        opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or opc = SUBMUL_RFFR or
        opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or opc = SUBMUL_RFPR or
        opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or opc = SUBMUL_RPRR or
        opc = SUBMUL_RPRM or opc = SUBMUL_RPRI or opc = SUBMUL_RPRF or
        opc = SUBMUL_RPRP or opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or
        opc = SUBMUL_RPMI or opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or
        opc = SUBMUL_RPIR or opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or
        opc = SUBMUL_RPIP or opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or
        opc = SUBMUL_RPFI or opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or
        opc = SUBMUL_RPPI or opc = SUBMUL_MRRR or opc = SUBMUL_MRRM or
        opc = SUBMUL_MRRI or opc = SUBMUL_MRRF or opc = SUBMUL_MRRP or
        opc = SUBMUL_MRMR or opc = SUBMUL_MRMM or opc = SUBMUL_MRMI or
        opc = SUBMUL_MRMF or opc = SUBMUL_MRMP or opc = SUBMUL_MRIR or
        opc = SUBMUL_MRIM or opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or
        opc = SUBMUL_MRFR or opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or
        opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MRPR or
        opc = SUBMUL_MRPM or opc = SUBMUL_MRPI or opc = SUBMUL_MRPF or
        opc = SUBMUL_MRPP or opc = SUBMUL_MMRR or opc = SUBMUL_MMRM or
        opc = SUBMUL_MMRI or opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or
        opc = SUBMUL_MMMR or opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or
        opc = SUBMUL_MMMP or opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or
        opc = SUBMUL_MMIF or opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or
        opc = SUBMUL_MMFM or opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or
        opc = SUBMUL_MMFP or opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or
        opc = SUBMUL_MMPI or opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or
        opc = SUBMUL_MIRR or opc = SUBMUL_MIRM or opc = SUBMUL_MIRF or
        opc = SUBMUL_MIRP or opc = SUBMUL_MIMR or opc = SUBMUL_MIMM or
        opc = SUBMUL_MIMF or opc = SUBMUL_MIMP or opc = SUBMUL_MIFR or
        opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or opc = SUBMUL_MIFP or
        -- real32_4_gen
        opc = SUBMUL_MIPR or opc = SUBMUL_MIPM or opc = SUBMUL_MIPF or
        opc = SUBMUL_MIPP or opc = SUBMUL_MFRR or opc = SUBMUL_MFRM or
        opc = SUBMUL_MFRI or opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or
        opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or opc = SUBMUL_MFMI or
        opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or opc = SUBMUL_MFIR or
        opc = SUBMUL_MFIM or opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or
        opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
        opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or
        opc = SUBMUL_MPRR or opc = SUBMUL_MPRM or opc = SUBMUL_MPRI or
        opc = SUBMUL_MPRF or opc = SUBMUL_MPRP or opc = SUBMUL_MPMR or
        opc = SUBMUL_MPMM or opc = SUBMUL_MPMI or opc = SUBMUL_MPMF or
        opc = SUBMUL_MPMP or opc = SUBMUL_MPIR or opc = SUBMUL_MPIM or
        opc = SUBMUL_MPIF or opc = SUBMUL_MPIP or opc = SUBMUL_MPFR or
        opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or opc = SUBMUL_MPPR or
        opc = SUBMUL_MPPM or opc = SUBMUL_MPPI or opc = SUBMUL_FRRR or
        opc = SUBMUL_FRRM or opc = SUBMUL_FRRI or opc = SUBMUL_FRRF or
        opc = SUBMUL_FRRP or opc = SUBMUL_FRMR or opc = SUBMUL_FRMM or
        opc = SUBMUL_FRMI or opc = SUBMUL_FRMF or opc = SUBMUL_FRMP or
        opc = SUBMUL_FRIR or opc = SUBMUL_FRIM or opc = SUBMUL_FRIF or
        opc = SUBMUL_FRIP or opc = SUBMUL_FRFR or opc = SUBMUL_FRFM or
        opc = SUBMUL_FRFI or opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or
        opc = SUBMUL_FRPR or opc = SUBMUL_FRPM or opc = SUBMUL_FRPI or
        opc = SUBMUL_FRPF or opc = SUBMUL_FRPP or opc = SUBMUL_FMRR or
        opc = SUBMUL_FMRM or opc = SUBMUL_FMRI or opc = SUBMUL_FMRF or
        opc = SUBMUL_FMRP or opc = SUBMUL_FMMR or opc = SUBMUL_FMMI or
        opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or opc = SUBMUL_FMIR or
        opc = SUBMUL_FMIM or opc = SUBMUL_FMIF or opc = SUBMUL_FMIP or
        opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or opc = SUBMUL_FMFI or
        opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or opc = SUBMUL_FMPR or
        opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or opc = SUBMUL_FMPF or
        opc = SUBMUL_FMPP or opc = SUBMUL_FIRR or opc = SUBMUL_FIRM or
        opc = SUBMUL_FIRF or opc = SUBMUL_FIRP or opc = SUBMUL_FIMR or
        opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or opc = SUBMUL_FIMP or
        opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
        opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or opc = SUBMUL_FIPM or
        opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or opc = SUBMUL_FFRR or
        opc = SUBMUL_FFRM or opc = SUBMUL_FFRI or opc = SUBMUL_FFRF or
        opc = SUBMUL_FFRP or opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or
        opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or
        opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or opc = SUBMUL_FFIF or
        opc = SUBMUL_FFIP or opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or
        opc = SUBMUL_FFFI or opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or
        opc = SUBMUL_FFPI or opc = SUBMUL_FPRR or opc = SUBMUL_FPRM or
        opc = SUBMUL_FPRI or opc = SUBMUL_FPRF or opc = SUBMUL_FPRP or
        opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or opc = SUBMUL_FPMI or
        opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or opc = SUBMUL_FPIR or
        opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or opc = SUBMUL_FPIP or
        opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
        -- real32_4_gen
        opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or opc = SUBMUL_FPPI or
        opc = SUBMULSRA_RRRR or opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRRI or
        opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMR or
        opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or
        opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIR or opc = SUBMULSRA_RRIM or
        opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or opc = SUBMULSRA_RRFR or
        opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRFF or
        opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or opc = SUBMULSRA_RRPM or
        opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RRPP or
        opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
        opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
        opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
        opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
        opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
        opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
        opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
        opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRR or
        opc = SUBMULSRA_RIRM or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or
        opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
        opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or
        opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or
        opc = SUBMULSRA_RIPM or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
        opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or
        opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or
        opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or
        opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
        opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or
        opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or
        opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or
        opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or
        opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
        -- real32_4_gen
        opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
        opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
        opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or
        opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or
        opc = SUBMULSRA_RPPI or opc = SUBMULSRA_MRRR or opc = SUBMULSRA_MRRM or
        opc = SUBMULSRA_MRRI or opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or
        opc = SUBMULSRA_MRMR or opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MRMI or
        opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIR or
        opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
        opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
        opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or
        opc = SUBMULSRA_MRPM or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or
        opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or
        opc = SUBMULSRA_MMRI or opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or
        opc = SUBMULSRA_MMMR or opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or
        opc = SUBMULSRA_MMMP or opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or
        opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or
        opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or
        opc = SUBMULSRA_MMFP or opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or
        opc = SUBMULSRA_MMPI or opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or
        opc = SUBMULSRA_MIRR or opc = SUBMULSRA_MIRM or opc = SUBMULSRA_MIRF or
        opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or
        opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFR or
        opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIFP or
        opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or opc = SUBMULSRA_MIPF or
        opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or
        opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or
        opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or
        opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or
        opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
        opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
        opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
        opc = SUBMULSRA_MPRR or opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPRI or
        opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMR or
        opc = SUBMULSRA_MPMM or opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or
        opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or
        opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFR or
        opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPR or
        opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or opc = SUBMULSRA_FRRR or
        opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRRI or opc = SUBMULSRA_FRRF or
        opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMR or opc = SUBMULSRA_FRMM or
        opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRMP or
        opc = SUBMULSRA_FRIR or opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRIF or
        opc = SUBMULSRA_FRIP or opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or
        opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or
        opc = SUBMULSRA_FRPR or opc = SUBMULSRA_FRPM or opc = SUBMULSRA_FRPI or
        opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMRR or
        -- real32_4_gen
        opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or opc = SUBMULSRA_FMRF or
        opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or opc = SUBMULSRA_FMMI or
        opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or opc = SUBMULSRA_FMIR or
        opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMIP or
        opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMFI or
        opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or opc = SUBMULSRA_FMPR or
        opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or opc = SUBMULSRA_FMPF or
        opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRR or opc = SUBMULSRA_FIRM or
        opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMR or
        opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
        opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
        opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
        opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRR or
        opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or
        opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
        opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
        opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or
        opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or
        opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or
        opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or opc = SUBMULSRA_FPRM or
        opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or
        opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or opc = SUBMULSRA_FPMI or
        opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIR or
        opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
        opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
        opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI or
        opc = SETMASKLT_XXRR or opc = SETMASKLT_XXRM or opc = SETMASKLT_XXRI or
        opc = SETMASKLT_XXRF or opc = SETMASKLT_XXRP or opc = SETMASKLT_XXMR or
        opc = SETMASKLT_XXMM or opc = SETMASKLT_XXMI or opc = SETMASKLT_XXMF or
        opc = SETMASKLT_XXMP or opc = SETMASKLT_XXIR or opc = SETMASKLT_XXIM or
        opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or opc = SETMASKLT_XXFR or
        opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or opc = SETMASKLT_XXFF or
        opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPR or opc = SETMASKLT_XXPM or
        opc = SETMASKLT_XXPI or opc = SETMASKLT_XXPF or opc = SETMASKLT_XXPP or
        opc = SETMASKGT_XXRR or opc = SETMASKGT_XXRM or opc = SETMASKGT_XXRI or
        opc = SETMASKGT_XXRF or opc = SETMASKGT_XXRP or opc = SETMASKGT_XXMR or
        opc = SETMASKGT_XXMM or opc = SETMASKGT_XXMI or opc = SETMASKGT_XXMF or
        opc = SETMASKGT_XXMP or opc = SETMASKGT_XXIR or opc = SETMASKGT_XXIM or
        opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or opc = SETMASKGT_XXFR or
        opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or opc = SETMASKGT_XXFF or
        opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPR or opc = SETMASKGT_XXPM or
        opc = SETMASKGT_XXPI or opc = SETMASKGT_XXPF or opc = SETMASKGT_XXPP or
        opc = SETMASKEQ_XXRR or opc = SETMASKEQ_XXRM or opc = SETMASKEQ_XXRI or
        opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXRP or opc = SETMASKEQ_XXMR or
        opc = SETMASKEQ_XXMM or opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXMF or
        opc = SETMASKEQ_XXMP or opc = SETMASKEQ_XXIR or opc = SETMASKEQ_XXIM or
        opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or opc = SETMASKEQ_XXFR or
        -- real32_4_gen
        opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or opc = SETMASKEQ_XXFF or
        opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPR or opc = SETMASKEQ_XXPM or
        opc = SETMASKEQ_XXPI or opc = SETMASKEQ_XXPF or opc = SETMASKEQ_XXPP or
        opc = SETMASKGE_XXRR or opc = SETMASKGE_XXRM or opc = SETMASKGE_XXRI or
        opc = SETMASKGE_XXRF or opc = SETMASKGE_XXRP or opc = SETMASKGE_XXMR or
        opc = SETMASKGE_XXMM or opc = SETMASKGE_XXMI or opc = SETMASKGE_XXMF or
        opc = SETMASKGE_XXMP or opc = SETMASKGE_XXIR or opc = SETMASKGE_XXIM or
        opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or opc = SETMASKGE_XXFR or
        opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or opc = SETMASKGE_XXFF or
        opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPR or opc = SETMASKGE_XXPM or
        opc = SETMASKGE_XXPI or opc = SETMASKGE_XXPF or opc = SETMASKGE_XXPP or
        opc = SETMASKLE_XXRR or opc = SETMASKLE_XXRM or opc = SETMASKLE_XXRI or
        opc = SETMASKLE_XXRF or opc = SETMASKLE_XXRP or opc = SETMASKLE_XXMR or
        opc = SETMASKLE_XXMM or opc = SETMASKLE_XXMI or opc = SETMASKLE_XXMF or
        opc = SETMASKLE_XXMP or opc = SETMASKLE_XXIR or opc = SETMASKLE_XXIM or
        opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or opc = SETMASKLE_XXFR or
        opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or opc = SETMASKLE_XXFF or
        opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPR or opc = SETMASKLE_XXPM or
        opc = SETMASKLE_XXPI or opc = SETMASKLE_XXPF or opc = SETMASKLE_XXPP or
        opc = SETMASKNE_XXRR or opc = SETMASKNE_XXRM or opc = SETMASKNE_XXRI or
        opc = SETMASKNE_XXRF or opc = SETMASKNE_XXRP or opc = SETMASKNE_XXMR or
        opc = SETMASKNE_XXMM or opc = SETMASKNE_XXMI or opc = SETMASKNE_XXMF or
        opc = SETMASKNE_XXMP or opc = SETMASKNE_XXIR or opc = SETMASKNE_XXIM or
        opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or opc = SETMASKNE_XXFR or
        opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or opc = SETMASKNE_XXFF or
        opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPR or opc = SETMASKNE_XXPM or
        opc = SETMASKNE_XXPI or opc = SETMASKNE_XXPF or opc = SETMASKNE_XXPP or
        opc = CMP_XXRR or opc = CMP_XXRM or opc = CMP_XXRI or
        opc = CMP_XXRF or opc = CMP_XXRP or opc = CMP_XXMR or
        opc = CMP_XXMM or opc = CMP_XXMI or opc = CMP_XXMF or
        opc = CMP_XXMP or opc = CMP_XXIR or opc = CMP_XXIM or
        opc = CMP_XXIF or opc = CMP_XXIP or opc = CMP_XXFR or
        opc = CMP_XXFM or opc = CMP_XXFI or opc = CMP_XXFF or
        opc = CMP_XXFP or opc = CMP_XXPR or opc = CMP_XXPM or
        -- real32_4_gen
        opc = CMP_XXPI or opc = CMP_XXPF or opc = CMP_XXPP
      then
        opcode <= "01100110011"; -- c-a*b
      elsif opc = ADDMULFWD_RRRX or opc = ADDMULFWD_RRMX or opc = ADDMULFWD_RRIX or
        opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RRPX or opc = ADDMULFWD_RMRX or
        opc = ADDMULFWD_RMMX or opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RMFX or
        opc = ADDMULFWD_RMPX or opc = ADDMULFWD_RIRX or opc = ADDMULFWD_RIMX or
        opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or opc = ADDMULFWD_RFRX or
        opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or opc = ADDMULFWD_RFFX or
        opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPRX or opc = ADDMULFWD_RPMX or
        opc = ADDMULFWD_RPIX or opc = ADDMULFWD_RPFX or opc = ADDMULFWD_RPPX or
        opc = ADDMULFWD_MRRX or opc = ADDMULFWD_MRMX or opc = ADDMULFWD_MRIX or
        opc = ADDMULFWD_MRFX or opc = ADDMULFWD_MRPX or opc = ADDMULFWD_MMRX or
        opc = ADDMULFWD_MMMX or opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MMFX or
        opc = ADDMULFWD_MMPX or opc = ADDMULFWD_MIRX or opc = ADDMULFWD_MIMX or
        opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFRX or
        opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or
        opc = ADDMULFWD_MFPX or opc = ADDMULFWD_MPRX or opc = ADDMULFWD_MPMX or
        opc = ADDMULFWD_MPIX or opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or
        opc = ADDMULFWD_FRRX or opc = ADDMULFWD_FRMX or opc = ADDMULFWD_FRIX or
        opc = ADDMULFWD_FRFX or opc = ADDMULFWD_FRPX or opc = ADDMULFWD_FMRX or
        opc = ADDMULFWD_FMMX or opc = ADDMULFWD_FMIX or opc = ADDMULFWD_FMFX or
        opc = ADDMULFWD_FMPX or opc = ADDMULFWD_FIRX or opc = ADDMULFWD_FIMX or
        opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFRX or
        opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or
        opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPRX or opc = ADDMULFWD_FPMX or
        opc = ADDMULFWD_FPIX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX
      then
        opcode <= "01000110000"; -- p+a*b
      elsif opc = SUBMULFWD_RRRX or opc = SUBMULFWD_RRMX or opc = SUBMULFWD_RRIX or
        opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RRPX or opc = SUBMULFWD_RMRX or
        opc = SUBMULFWD_RMMX or opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RMFX or
        opc = SUBMULFWD_RMPX or opc = SUBMULFWD_RIRX or opc = SUBMULFWD_RIMX or
        opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or opc = SUBMULFWD_RFRX or
        opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or opc = SUBMULFWD_RFFX or
        opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPRX or opc = SUBMULFWD_RPMX or
        opc = SUBMULFWD_RPIX or opc = SUBMULFWD_RPFX or opc = SUBMULFWD_RPPX or
        opc = SUBMULFWD_MRRX or opc = SUBMULFWD_MRMX or opc = SUBMULFWD_MRIX or
        opc = SUBMULFWD_MRFX or opc = SUBMULFWD_MRPX or opc = SUBMULFWD_MMRX or
        opc = SUBMULFWD_MMMX or opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MMFX or
        opc = SUBMULFWD_MMPX or opc = SUBMULFWD_MIRX or opc = SUBMULFWD_MIMX or
        opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFRX or
        opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or
        opc = SUBMULFWD_MFPX or opc = SUBMULFWD_MPRX or opc = SUBMULFWD_MPMX or
        opc = SUBMULFWD_MPIX or opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or
        opc = SUBMULFWD_FRRX or opc = SUBMULFWD_FRMX or opc = SUBMULFWD_FRIX or
        opc = SUBMULFWD_FRFX or opc = SUBMULFWD_FRPX or opc = SUBMULFWD_FMRX or
        opc = SUBMULFWD_FMMX or opc = SUBMULFWD_FMIX or opc = SUBMULFWD_FMFX or
        -- real32_4_gen
        opc = SUBMULFWD_FMPX or opc = SUBMULFWD_FIRX or opc = SUBMULFWD_FIMX or
        opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFRX or
        opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or
        opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPRX or opc = SUBMULFWD_FPMX or
        opc = SUBMULFWD_FPIX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
        opc = CMPFWD_XXRX or opc = CMPFWD_XXMX or opc = CMPFWD_XXIX or
        opc = CMPFWD_XXFX or opc = CMPFWD_XXPX
      then
        opcode <= "01000110011"; -- p-a*b
      else
        opcode <= "00000000000";
      end if;
    end process;

    o_id_opmode <= opcode(10 downto 4);
    o_id_alumode <= opcode(3 downto 0);
  end generate REAL32_4_GEN;

  CPLX16_4:
  if (DATA_WIDTH = 16 and DATA_TYPE = 2 and SLICE_NUM = 4) generate
    signal opmode_02, opmode_13 : std_logic_vector(6 downto 0); -- 0-2 and 1-3 are same
    signal alumode_02, alumode_1, alumode_3 : std_logic_vector(3 downto 0); -- 0-2 same
    signal opcode0, opcode1, opcode2, opcode3 : std_logic_vector(10 downto 0);
  begin
    process (opc) begin
      -- Overally, the pattern is
      -- cr +- ai*bi +- ar*br and ci +- ai*br +- ar*bi
      if opc = CLR_RXXX or opc = CLR_MXXX or opc = CLR_IXXX then
        opcode0 <=  "00000000000";
        opcode1 <=  "00000000000";
        opcode2 <=  "00000000000";
        opcode3 <=  "00000000000";
      elsif opc = PUT_FXXR or opc = PUT_FXXM or opc = PUT_FXXI or
        opc = PUT_FXXF or opc = PUT_FXXP or
        opc = GET_RXXF or opc = GET_MXXF or opc = GET_IXXF
      then
        -- put (is cr + 0 + 0 and ci + 0 + 0)
        opcode0 <=  "00100000000";
        opcode1 <=  "01100000000";
        opcode2 <=  "00100000000";
        opcode3 <=  "01100000000";
      elsif opc = PUTFWD_FXXX then
        opcode0 <=  "01000000000";
        opcode1 <=  "00000000000";
        opcode2 <=  "01000000000";
        opcode3 <=  "00000000000"; -- p (PUTFWD)
      elsif opc = ADDMUL_RRRR or opc = ADDMUL_RRRM or opc = ADDMUL_RRRI or
        opc = ADDMUL_RRRF or opc = ADDMUL_RRRP or opc = ADDMUL_RRMR or
        opc = ADDMUL_RRMM or opc = ADDMUL_RRMI or opc = ADDMUL_RRMF or
        opc = ADDMUL_RRMP or opc = ADDMUL_RRIR or opc = ADDMUL_RRIM or
        opc = ADDMUL_RRIF or opc = ADDMUL_RRIP or opc = ADDMUL_RRFR or
        opc = ADDMUL_RRFM or opc = ADDMUL_RRFI or opc = ADDMUL_RRFF or
        opc = ADDMUL_RRFP or opc = ADDMUL_RRPR or opc = ADDMUL_RRPM or
        opc = ADDMUL_RRPI or opc = ADDMUL_RRPF or opc = ADDMUL_RRPP or
        opc = ADDMUL_RMRR or opc = ADDMUL_RMRM or opc = ADDMUL_RMRI or
        opc = ADDMUL_RMRF or opc = ADDMUL_RMRP or opc = ADDMUL_RMMR or
        opc = ADDMUL_RMMI or opc = ADDMUL_RMMF or opc = ADDMUL_RMMP or
        opc = ADDMUL_RMIR or opc = ADDMUL_RMIM or opc = ADDMUL_RMIF or
        opc = ADDMUL_RMIP or opc = ADDMUL_RMFR or opc = ADDMUL_RMFM or
        opc = ADDMUL_RMFI or opc = ADDMUL_RMFF or opc = ADDMUL_RMFP or
        opc = ADDMUL_RMPR or opc = ADDMUL_RMPM or opc = ADDMUL_RMPI or
        opc = ADDMUL_RMPF or opc = ADDMUL_RMPP or opc = ADDMUL_RIRR or
        opc = ADDMUL_RIRM or opc = ADDMUL_RIRF or opc = ADDMUL_RIRP or
        opc = ADDMUL_RIMR or opc = ADDMUL_RIMM or opc = ADDMUL_RIMF or
        opc = ADDMUL_RIMP or opc = ADDMUL_RIFR or opc = ADDMUL_RIFM or
        opc = ADDMUL_RIFF or opc = ADDMUL_RIFP or opc = ADDMUL_RIPR or
        opc = ADDMUL_RIPM or opc = ADDMUL_RIPF or opc = ADDMUL_RIPP or
        opc = ADDMUL_RFRR or opc = ADDMUL_RFRM or opc = ADDMUL_RFRI or
        opc = ADDMUL_RFRF or opc = ADDMUL_RFRP or opc = ADDMUL_RFMR or
        opc = ADDMUL_RFMM or opc = ADDMUL_RFMI or opc = ADDMUL_RFMF or
        opc = ADDMUL_RFMP or opc = ADDMUL_RFIR or opc = ADDMUL_RFIM or
        opc = ADDMUL_RFIF or opc = ADDMUL_RFIP or opc = ADDMUL_RFFR or
        opc = ADDMUL_RFFM or opc = ADDMUL_RFFI or opc = ADDMUL_RFPR or
        opc = ADDMUL_RFPM or opc = ADDMUL_RFPI or opc = ADDMUL_RPRR or
        -- complx16_4_gen
        opc = ADDMUL_RPRM or opc = ADDMUL_RPRI or opc = ADDMUL_RPRF or
        opc = ADDMUL_RPRP or opc = ADDMUL_RPMR or opc = ADDMUL_RPMM or
        opc = ADDMUL_RPMI or opc = ADDMUL_RPMF or opc = ADDMUL_RPMP or
        opc = ADDMUL_RPIR or opc = ADDMUL_RPIM or opc = ADDMUL_RPIF or
        opc = ADDMUL_RPIP or opc = ADDMUL_RPFR or opc = ADDMUL_RPFM or
        opc = ADDMUL_RPFI or opc = ADDMUL_RPPR or opc = ADDMUL_RPPM or
        opc = ADDMUL_RPPI or opc = ADDMUL_MRRR or opc = ADDMUL_MRRM or
        opc = ADDMUL_MRRI or opc = ADDMUL_MRRF or opc = ADDMUL_MRRP or
        opc = ADDMUL_MRMR or opc = ADDMUL_MRMM or opc = ADDMUL_MRMI or
        opc = ADDMUL_MRMF or opc = ADDMUL_MRMP or opc = ADDMUL_MRIR or
        opc = ADDMUL_MRIM or opc = ADDMUL_MRIF or opc = ADDMUL_MRIP or
        opc = ADDMUL_MRFR or opc = ADDMUL_MRFM or opc = ADDMUL_MRFI or
        opc = ADDMUL_MRFF or opc = ADDMUL_MRFP or opc = ADDMUL_MRPR or
        opc = ADDMUL_MRPM or opc = ADDMUL_MRPI or opc = ADDMUL_MRPF or
        opc = ADDMUL_MRPP or opc = ADDMUL_MMRR or opc = ADDMUL_MMRM or
        opc = ADDMUL_MMRI or opc = ADDMUL_MMRF or opc = ADDMUL_MMRP or
        opc = ADDMUL_MMMR or opc = ADDMUL_MMMI or opc = ADDMUL_MMMF or
        opc = ADDMUL_MMMP or opc = ADDMUL_MMIR or opc = ADDMUL_MMIM or
        opc = ADDMUL_MMIF or opc = ADDMUL_MMIP or opc = ADDMUL_MMFR or
        opc = ADDMUL_MMFM or opc = ADDMUL_MMFI or opc = ADDMUL_MMFF or
        opc = ADDMUL_MMFP or opc = ADDMUL_MMPR or opc = ADDMUL_MMPM or
        opc = ADDMUL_MMPI or opc = ADDMUL_MMPF or opc = ADDMUL_MMPP or
        opc = ADDMUL_MIRR or opc = ADDMUL_MIRM or opc = ADDMUL_MIRF or
        opc = ADDMUL_MIRP or opc = ADDMUL_MIMR or opc = ADDMUL_MIMM or
        opc = ADDMUL_MIMF or opc = ADDMUL_MIMP or opc = ADDMUL_MIFR or
        opc = ADDMUL_MIFM or opc = ADDMUL_MIFF or opc = ADDMUL_MIFP or
        opc = ADDMUL_MIPR or opc = ADDMUL_MIPM or opc = ADDMUL_MIPF or
        opc = ADDMUL_MIPP or opc = ADDMUL_MFRR or opc = ADDMUL_MFRM or
        opc = ADDMUL_MFRI or opc = ADDMUL_MFRF or opc = ADDMUL_MFRP or
        opc = ADDMUL_MFMR or opc = ADDMUL_MFMM or opc = ADDMUL_MFMI or
        opc = ADDMUL_MFMF or opc = ADDMUL_MFMP or opc = ADDMUL_MFIR or
        opc = ADDMUL_MFIM or opc = ADDMUL_MFIF or opc = ADDMUL_MFIP or
        opc = ADDMUL_MFFR or opc = ADDMUL_MFFM or opc = ADDMUL_MFFI or
        opc = ADDMUL_MFPR or opc = ADDMUL_MFPM or opc = ADDMUL_MFPI or
        opc = ADDMUL_MPRR or opc = ADDMUL_MPRM or opc = ADDMUL_MPRI or
        opc = ADDMUL_MPRF or opc = ADDMUL_MPRP or opc = ADDMUL_MPMR or
        opc = ADDMUL_MPMM or opc = ADDMUL_MPMI or opc = ADDMUL_MPMF or
        opc = ADDMUL_MPMP or opc = ADDMUL_MPIR or opc = ADDMUL_MPIM or
        opc = ADDMUL_MPIF or opc = ADDMUL_MPIP or opc = ADDMUL_MPFR or
        opc = ADDMUL_MPFM or opc = ADDMUL_MPFI or opc = ADDMUL_MPPR or
        opc = ADDMUL_MPPM or opc = ADDMUL_MPPI or opc = ADDMUL_FRRR or
        opc = ADDMUL_FRRM or opc = ADDMUL_FRRI or opc = ADDMUL_FRRF or
        opc = ADDMUL_FRRP or opc = ADDMUL_FRMR or opc = ADDMUL_FRMM or
        opc = ADDMUL_FRMI or opc = ADDMUL_FRMF or opc = ADDMUL_FRMP or
        opc = ADDMUL_FRIR or opc = ADDMUL_FRIM or opc = ADDMUL_FRIF or
        opc = ADDMUL_FRIP or opc = ADDMUL_FRFR or opc = ADDMUL_FRFM or
        opc = ADDMUL_FRFI or opc = ADDMUL_FRFF or opc = ADDMUL_FRFP or
        opc = ADDMUL_FRPR or opc = ADDMUL_FRPM or opc = ADDMUL_FRPI or
        opc = ADDMUL_FRPF or opc = ADDMUL_FRPP or opc = ADDMUL_FMRR or
        opc = ADDMUL_FMRM or opc = ADDMUL_FMRI or opc = ADDMUL_FMRF or
        opc = ADDMUL_FMRP or opc = ADDMUL_FMMR or opc = ADDMUL_FMMI or
        opc = ADDMUL_FMMF or opc = ADDMUL_FMMP or opc = ADDMUL_FMIR or
        opc = ADDMUL_FMIM or opc = ADDMUL_FMIF or opc = ADDMUL_FMIP or
        opc = ADDMUL_FMFR or opc = ADDMUL_FMFM or opc = ADDMUL_FMFI or
        -- complx16_4_gen
        opc = ADDMUL_FMFF or opc = ADDMUL_FMFP or opc = ADDMUL_FMPR or
        opc = ADDMUL_FMPM or opc = ADDMUL_FMPI or opc = ADDMUL_FMPF or
        opc = ADDMUL_FMPP or opc = ADDMUL_FIRR or opc = ADDMUL_FIRM or
        opc = ADDMUL_FIRF or opc = ADDMUL_FIRP or opc = ADDMUL_FIMR or
        opc = ADDMUL_FIMM or opc = ADDMUL_FIMF or opc = ADDMUL_FIMP or
        opc = ADDMUL_FIFR or opc = ADDMUL_FIFM or opc = ADDMUL_FIFF or
        opc = ADDMUL_FIFP or opc = ADDMUL_FIPR or opc = ADDMUL_FIPM or
        opc = ADDMUL_FIPF or opc = ADDMUL_FIPP or opc = ADDMUL_FFRR or
        opc = ADDMUL_FFRM or opc = ADDMUL_FFRI or opc = ADDMUL_FFRF or
        opc = ADDMUL_FFRP or opc = ADDMUL_FFMR or opc = ADDMUL_FFMM or
        opc = ADDMUL_FFMI or opc = ADDMUL_FFMF or opc = ADDMUL_FFMP or
        opc = ADDMUL_FFIR or opc = ADDMUL_FFIM or opc = ADDMUL_FFIF or
        opc = ADDMUL_FFIP or opc = ADDMUL_FFFR or opc = ADDMUL_FFFM or
        opc = ADDMUL_FFFI or opc = ADDMUL_FFPR or opc = ADDMUL_FFPM or
        opc = ADDMUL_FFPI or opc = ADDMUL_FPRR or opc = ADDMUL_FPRM or
        opc = ADDMUL_FPRI or opc = ADDMUL_FPRF or opc = ADDMUL_FPRP or
        opc = ADDMUL_FPMR or opc = ADDMUL_FPMM or opc = ADDMUL_FPMI or
        opc = ADDMUL_FPMF or opc = ADDMUL_FPMP or opc = ADDMUL_FPIR or
        opc = ADDMUL_FPIM or opc = ADDMUL_FPIF or opc = ADDMUL_FPIP or
        opc = ADDMUL_FPFR or opc = ADDMUL_FPFM or opc = ADDMUL_FPFI or
        opc = ADDMUL_FPPR or opc = ADDMUL_FPPM or opc = ADDMUL_FPPI or
        opc = ADDMULSRA_RRRR or opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRRI or
        opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMR or
        opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or
        opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIR or opc = ADDMULSRA_RRIM or
        opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or opc = ADDMULSRA_RRFR or
        opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRFF or
        opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or opc = ADDMULSRA_RRPM or
        opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RRPP or
        opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
        opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
        opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
        opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
        opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
        opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
        opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
        opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRR or
        opc = ADDMULSRA_RIRM or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or
        opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
        -- complx16_4_gen
        opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or
        opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or
        opc = ADDMULSRA_RIPM or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
        opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or
        opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or
        opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or
        opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
        opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or
        opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or
        opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or
        opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or
        opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
        opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
        opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
        opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or
        opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or
        opc = ADDMULSRA_RPPI or opc = ADDMULSRA_MRRR or opc = ADDMULSRA_MRRM or
        opc = ADDMULSRA_MRRI or opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or
        opc = ADDMULSRA_MRMR or opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MRMI or
        opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIR or
        opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
        opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
        opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or
        opc = ADDMULSRA_MRPM or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or
        opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or
        opc = ADDMULSRA_MMRI or opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or
        opc = ADDMULSRA_MMMR or opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or
        opc = ADDMULSRA_MMMP or opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or
        opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or
        opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or
        opc = ADDMULSRA_MMFP or opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or
        opc = ADDMULSRA_MMPI or opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or
        opc = ADDMULSRA_MIRR or opc = ADDMULSRA_MIRM or opc = ADDMULSRA_MIRF or
        opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or
        opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFR or
        opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIFP or
        opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or opc = ADDMULSRA_MIPF or
        opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or
        -- complx16_4_gen
        opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or
        opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or
        opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or
        opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
        opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
        opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
        opc = ADDMULSRA_MPRR or opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPRI or
        opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMR or
        opc = ADDMULSRA_MPMM or opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or
        opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or
        opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFR or
        opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPR or
        opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or opc = ADDMULSRA_FRRR or
        opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRRI or opc = ADDMULSRA_FRRF or
        opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMR or opc = ADDMULSRA_FRMM or
        opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRMP or
        opc = ADDMULSRA_FRIR or opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRIF or
        opc = ADDMULSRA_FRIP or opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or
        opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or
        opc = ADDMULSRA_FRPR or opc = ADDMULSRA_FRPM or opc = ADDMULSRA_FRPI or
        opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMRR or
        opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or opc = ADDMULSRA_FMRF or
        opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or opc = ADDMULSRA_FMMI or
        opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or opc = ADDMULSRA_FMIR or
        opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMIP or
        opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMFI or
        opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or opc = ADDMULSRA_FMPR or
        opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or opc = ADDMULSRA_FMPF or
        opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRR or opc = ADDMULSRA_FIRM or
        opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMR or
        opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
        opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
        opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
        opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRR or
        opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or
        opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
        opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
        opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or
        opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or
        opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or
        opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or opc = ADDMULSRA_FPRM or
        opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or
        opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or opc = ADDMULSRA_FPMI or
        opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIR or
        opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
        -- complx16_4_gen
        opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
        opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI
      then
        -- addmul (is cr - ai*bi + ar*br and ci + ai*br + ar*bi)
        -- mul (is 0 - ai*bi + ar*br and 0 + ai*br + ar*bi)
        -- add (is cr - 0*bi + 1*br and ci + 0*br + 1*bi)
        opcode0 <=  "00101010000";
        opcode1 <=  "01101010011";
        opcode2 <=  "00101010000";
        opcode3 <=  "01101010000";
      elsif opc = SUBMUL_RRRR or opc = SUBMUL_RRRM or opc = SUBMUL_RRRI or
        opc = SUBMUL_RRRF or opc = SUBMUL_RRRP or opc = SUBMUL_RRMR or
        opc = SUBMUL_RRMM or opc = SUBMUL_RRMI or opc = SUBMUL_RRMF or
        opc = SUBMUL_RRMP or opc = SUBMUL_RRIR or opc = SUBMUL_RRIM or
        opc = SUBMUL_RRIF or opc = SUBMUL_RRIP or opc = SUBMUL_RRFR or
        opc = SUBMUL_RRFM or opc = SUBMUL_RRFI or opc = SUBMUL_RRFF or
        opc = SUBMUL_RRFP or opc = SUBMUL_RRPR or opc = SUBMUL_RRPM or
        opc = SUBMUL_RRPI or opc = SUBMUL_RRPF or opc = SUBMUL_RRPP or
        opc = SUBMUL_RMRR or opc = SUBMUL_RMRM or opc = SUBMUL_RMRI or
        opc = SUBMUL_RMRF or opc = SUBMUL_RMRP or opc = SUBMUL_RMMR or
        opc = SUBMUL_RMMI or opc = SUBMUL_RMMF or opc = SUBMUL_RMMP or
        opc = SUBMUL_RMIR or opc = SUBMUL_RMIM or opc = SUBMUL_RMIF or
        opc = SUBMUL_RMIP or opc = SUBMUL_RMFR or opc = SUBMUL_RMFM or
        opc = SUBMUL_RMFI or opc = SUBMUL_RMFF or opc = SUBMUL_RMFP or
        opc = SUBMUL_RMPR or opc = SUBMUL_RMPM or opc = SUBMUL_RMPI or
        opc = SUBMUL_RMPF or opc = SUBMUL_RMPP or opc = SUBMUL_RIRR or
        opc = SUBMUL_RIRM or opc = SUBMUL_RIRF or opc = SUBMUL_RIRP or
        opc = SUBMUL_RIMR or opc = SUBMUL_RIMM or opc = SUBMUL_RIMF or
        opc = SUBMUL_RIMP or opc = SUBMUL_RIFR or opc = SUBMUL_RIFM or
        opc = SUBMUL_RIFF or opc = SUBMUL_RIFP or opc = SUBMUL_RIPR or
        opc = SUBMUL_RIPM or opc = SUBMUL_RIPF or opc = SUBMUL_RIPP or
        opc = SUBMUL_RFRR or opc = SUBMUL_RFRM or opc = SUBMUL_RFRI or
        opc = SUBMUL_RFRF or opc = SUBMUL_RFRP or opc = SUBMUL_RFMR or
        opc = SUBMUL_RFMM or opc = SUBMUL_RFMI or opc = SUBMUL_RFMF or
        opc = SUBMUL_RFMP or opc = SUBMUL_RFIR or opc = SUBMUL_RFIM or
        opc = SUBMUL_RFIF or opc = SUBMUL_RFIP or opc = SUBMUL_RFFR or
        opc = SUBMUL_RFFM or opc = SUBMUL_RFFI or opc = SUBMUL_RFPR or
        opc = SUBMUL_RFPM or opc = SUBMUL_RFPI or opc = SUBMUL_RPRR or
        opc = SUBMUL_RPRM or opc = SUBMUL_RPRI or opc = SUBMUL_RPRF or
        -- complx16_4_gen
        opc = SUBMUL_RPRP or opc = SUBMUL_RPMR or opc = SUBMUL_RPMM or
        opc = SUBMUL_RPMI or opc = SUBMUL_RPMF or opc = SUBMUL_RPMP or
        opc = SUBMUL_RPIR or opc = SUBMUL_RPIM or opc = SUBMUL_RPIF or
        opc = SUBMUL_RPIP or opc = SUBMUL_RPFR or opc = SUBMUL_RPFM or
        opc = SUBMUL_RPFI or opc = SUBMUL_RPPR or opc = SUBMUL_RPPM or
        opc = SUBMUL_RPPI or opc = SUBMUL_MRRR or opc = SUBMUL_MRRM or
        opc = SUBMUL_MRRI or opc = SUBMUL_MRRF or opc = SUBMUL_MRRP or
        opc = SUBMUL_MRMR or opc = SUBMUL_MRMM or opc = SUBMUL_MRMI or
        opc = SUBMUL_MRMF or opc = SUBMUL_MRMP or opc = SUBMUL_MRIR or
        opc = SUBMUL_MRIM or opc = SUBMUL_MRIF or opc = SUBMUL_MRIP or
        opc = SUBMUL_MRFR or opc = SUBMUL_MRFM or opc = SUBMUL_MRFI or
        opc = SUBMUL_MRFF or opc = SUBMUL_MRFP or opc = SUBMUL_MRPR or
        opc = SUBMUL_MRPM or opc = SUBMUL_MRPI or opc = SUBMUL_MRPF or
        opc = SUBMUL_MRPP or opc = SUBMUL_MMRR or opc = SUBMUL_MMRM or
        opc = SUBMUL_MMRI or opc = SUBMUL_MMRF or opc = SUBMUL_MMRP or
        opc = SUBMUL_MMMR or opc = SUBMUL_MMMI or opc = SUBMUL_MMMF or
        opc = SUBMUL_MMMP or opc = SUBMUL_MMIR or opc = SUBMUL_MMIM or
        opc = SUBMUL_MMIF or opc = SUBMUL_MMIP or opc = SUBMUL_MMFR or
        opc = SUBMUL_MMFM or opc = SUBMUL_MMFI or opc = SUBMUL_MMFF or
        opc = SUBMUL_MMFP or opc = SUBMUL_MMPR or opc = SUBMUL_MMPM or
        opc = SUBMUL_MMPI or opc = SUBMUL_MMPF or opc = SUBMUL_MMPP or
        opc = SUBMUL_MIRR or opc = SUBMUL_MIRM or opc = SUBMUL_MIRF or
        opc = SUBMUL_MIRP or opc = SUBMUL_MIMR or opc = SUBMUL_MIMM or
        opc = SUBMUL_MIMF or opc = SUBMUL_MIMP or opc = SUBMUL_MIFR or
        opc = SUBMUL_MIFM or opc = SUBMUL_MIFF or opc = SUBMUL_MIFP or
        opc = SUBMUL_MIPR or opc = SUBMUL_MIPM or opc = SUBMUL_MIPF or
        opc = SUBMUL_MIPP or opc = SUBMUL_MFRR or opc = SUBMUL_MFRM or
        opc = SUBMUL_MFRI or opc = SUBMUL_MFRF or opc = SUBMUL_MFRP or
        opc = SUBMUL_MFMR or opc = SUBMUL_MFMM or opc = SUBMUL_MFMI or
        opc = SUBMUL_MFMF or opc = SUBMUL_MFMP or opc = SUBMUL_MFIR or
        opc = SUBMUL_MFIM or opc = SUBMUL_MFIF or opc = SUBMUL_MFIP or
        opc = SUBMUL_MFFR or opc = SUBMUL_MFFM or opc = SUBMUL_MFFI or
        opc = SUBMUL_MFPR or opc = SUBMUL_MFPM or opc = SUBMUL_MFPI or
        opc = SUBMUL_MPRR or opc = SUBMUL_MPRM or opc = SUBMUL_MPRI or
        opc = SUBMUL_MPRF or opc = SUBMUL_MPRP or opc = SUBMUL_MPMR or
        opc = SUBMUL_MPMM or opc = SUBMUL_MPMI or opc = SUBMUL_MPMF or
        opc = SUBMUL_MPMP or opc = SUBMUL_MPIR or opc = SUBMUL_MPIM or
        opc = SUBMUL_MPIF or opc = SUBMUL_MPIP or opc = SUBMUL_MPFR or
        -- complx16_4_gen
        opc = SUBMUL_MPFM or opc = SUBMUL_MPFI or opc = SUBMUL_MPPR or
        opc = SUBMUL_MPPM or opc = SUBMUL_MPPI or opc = SUBMUL_FRRR or
        opc = SUBMUL_FRRM or opc = SUBMUL_FRRI or opc = SUBMUL_FRRF or
        opc = SUBMUL_FRRP or opc = SUBMUL_FRMR or opc = SUBMUL_FRMM or
        opc = SUBMUL_FRMI or opc = SUBMUL_FRMF or opc = SUBMUL_FRMP or
        opc = SUBMUL_FRIR or opc = SUBMUL_FRIM or opc = SUBMUL_FRIF or
        opc = SUBMUL_FRIP or opc = SUBMUL_FRFR or opc = SUBMUL_FRFM or
        opc = SUBMUL_FRFI or opc = SUBMUL_FRFF or opc = SUBMUL_FRFP or
        opc = SUBMUL_FRPR or opc = SUBMUL_FRPM or opc = SUBMUL_FRPI or
        opc = SUBMUL_FRPF or opc = SUBMUL_FRPP or opc = SUBMUL_FMRR or
        opc = SUBMUL_FMRM or opc = SUBMUL_FMRI or opc = SUBMUL_FMRF or
        opc = SUBMUL_FMRP or opc = SUBMUL_FMMR or opc = SUBMUL_FMMI or
        opc = SUBMUL_FMMF or opc = SUBMUL_FMMP or opc = SUBMUL_FMIR or
        opc = SUBMUL_FMIM or opc = SUBMUL_FMIF or opc = SUBMUL_FMIP or
        opc = SUBMUL_FMFR or opc = SUBMUL_FMFM or opc = SUBMUL_FMFI or
        opc = SUBMUL_FMFF or opc = SUBMUL_FMFP or opc = SUBMUL_FMPR or
        opc = SUBMUL_FMPM or opc = SUBMUL_FMPI or opc = SUBMUL_FMPF or
        opc = SUBMUL_FMPP or opc = SUBMUL_FIRR or opc = SUBMUL_FIRM or
        opc = SUBMUL_FIRF or opc = SUBMUL_FIRP or opc = SUBMUL_FIMR or
        opc = SUBMUL_FIMM or opc = SUBMUL_FIMF or opc = SUBMUL_FIMP or
        opc = SUBMUL_FIFR or opc = SUBMUL_FIFM or opc = SUBMUL_FIFF or
        opc = SUBMUL_FIFP or opc = SUBMUL_FIPR or opc = SUBMUL_FIPM or
        opc = SUBMUL_FIPF or opc = SUBMUL_FIPP or opc = SUBMUL_FFRR or
        opc = SUBMUL_FFRM or opc = SUBMUL_FFRI or opc = SUBMUL_FFRF or
        opc = SUBMUL_FFRP or opc = SUBMUL_FFMR or opc = SUBMUL_FFMM or
        opc = SUBMUL_FFMI or opc = SUBMUL_FFMF or opc = SUBMUL_FFMP or
        opc = SUBMUL_FFIR or opc = SUBMUL_FFIM or opc = SUBMUL_FFIF or
        opc = SUBMUL_FFIP or opc = SUBMUL_FFFR or opc = SUBMUL_FFFM or
        opc = SUBMUL_FFFI or opc = SUBMUL_FFPR or opc = SUBMUL_FFPM or
        opc = SUBMUL_FFPI or opc = SUBMUL_FPRR or opc = SUBMUL_FPRM or
        opc = SUBMUL_FPRI or opc = SUBMUL_FPRF or opc = SUBMUL_FPRP or
        opc = SUBMUL_FPMR or opc = SUBMUL_FPMM or opc = SUBMUL_FPMI or
        opc = SUBMUL_FPMF or opc = SUBMUL_FPMP or opc = SUBMUL_FPIR or
        opc = SUBMUL_FPIM or opc = SUBMUL_FPIF or opc = SUBMUL_FPIP or
        opc = SUBMUL_FPFR or opc = SUBMUL_FPFM or opc = SUBMUL_FPFI or
        -- complx16_4_gen
        opc = SUBMUL_FPPR or opc = SUBMUL_FPPM or opc = SUBMUL_FPPI or
        opc = SUBMULSRA_RRRR or opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRRI or
        opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMR or
        opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or
        opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIR or opc = SUBMULSRA_RRIM or
        opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or opc = SUBMULSRA_RRFR or
        opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRFF or
        opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or opc = SUBMULSRA_RRPM or
        opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RRPP or
        opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
        opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
        opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
        opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
        opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
        opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
        opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
        opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRR or
        opc = SUBMULSRA_RIRM or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or
        opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
        opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or
        opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or
        opc = SUBMULSRA_RIPM or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
        opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or
        opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or
        opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or
        opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
        opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or
        opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or
        opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or
        opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or
        opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
        opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
        opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
        opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or
        opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or
        opc = SUBMULSRA_RPPI or opc = SUBMULSRA_MRRR or opc = SUBMULSRA_MRRM or
        opc = SUBMULSRA_MRRI or opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or
        opc = SUBMULSRA_MRMR or opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MRMI or
        -- complx16_4_gen
        opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIR or
        opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
        opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
        opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or
        opc = SUBMULSRA_MRPM or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or
        opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or
        opc = SUBMULSRA_MMRI or opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or
        opc = SUBMULSRA_MMMR or opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or
        opc = SUBMULSRA_MMMP or opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or
        opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or
        opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or
        opc = SUBMULSRA_MMFP or opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or
        opc = SUBMULSRA_MMPI or opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or
        opc = SUBMULSRA_MIRR or opc = SUBMULSRA_MIRM or opc = SUBMULSRA_MIRF or
        opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or
        opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFR or
        opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIFP or
        opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or opc = SUBMULSRA_MIPF or
        opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or
        opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or
        opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or
        opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or
        opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
        opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
        opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
        opc = SUBMULSRA_MPRR or opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPRI or
        opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMR or
        opc = SUBMULSRA_MPMM or opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or
        opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or
        opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFR or
        opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPR or
        opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or opc = SUBMULSRA_FRRR or
        opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRRI or opc = SUBMULSRA_FRRF or
        opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMR or opc = SUBMULSRA_FRMM or
        opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRMP or
        opc = SUBMULSRA_FRIR or opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRIF or
        opc = SUBMULSRA_FRIP or opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or
        -- complx16_4_gen
        opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or
        opc = SUBMULSRA_FRPR or opc = SUBMULSRA_FRPM or opc = SUBMULSRA_FRPI or
        opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMRR or
        opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or opc = SUBMULSRA_FMRF or
        opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or opc = SUBMULSRA_FMMI or
        opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or opc = SUBMULSRA_FMIR or
        opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMIP or
        opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMFI or
        opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or opc = SUBMULSRA_FMPR or
        opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or opc = SUBMULSRA_FMPF or
        opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRR or opc = SUBMULSRA_FIRM or
        opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMR or
        opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
        opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
        opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
        opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRR or
        opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or
        opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
        opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
        opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or
        opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or
        opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or
        opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or opc = SUBMULSRA_FPRM or
        opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or
        opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or opc = SUBMULSRA_FPMI or
        opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIR or
        opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
        opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
        opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI or
        opc = SETMASKLT_XXRR or opc = SETMASKLT_XXRM or opc = SETMASKLT_XXRI or
        opc = SETMASKLT_XXRF or opc = SETMASKLT_XXRP or opc = SETMASKLT_XXMR or
        opc = SETMASKLT_XXMM or opc = SETMASKLT_XXMI or opc = SETMASKLT_XXMF or
        opc = SETMASKLT_XXMP or opc = SETMASKLT_XXIR or opc = SETMASKLT_XXIM or
        opc = SETMASKLT_XXIF or opc = SETMASKLT_XXIP or opc = SETMASKLT_XXFR or
        opc = SETMASKLT_XXFM or opc = SETMASKLT_XXFI or opc = SETMASKLT_XXFF or
        -- complx16_4_gen
        opc = SETMASKLT_XXFP or opc = SETMASKLT_XXPR or opc = SETMASKLT_XXPM or
        opc = SETMASKLT_XXPI or opc = SETMASKLT_XXPF or opc = SETMASKLT_XXPP or
        opc = SETMASKGT_XXRR or opc = SETMASKGT_XXRM or opc = SETMASKGT_XXRI or
        opc = SETMASKGT_XXRF or opc = SETMASKGT_XXRP or opc = SETMASKGT_XXMR or
        opc = SETMASKGT_XXMM or opc = SETMASKGT_XXMI or opc = SETMASKGT_XXMF or
        opc = SETMASKGT_XXMP or opc = SETMASKGT_XXIR or opc = SETMASKGT_XXIM or
        opc = SETMASKGT_XXIF or opc = SETMASKGT_XXIP or opc = SETMASKGT_XXFR or
        opc = SETMASKGT_XXFM or opc = SETMASKGT_XXFI or opc = SETMASKGT_XXFF or
        opc = SETMASKGT_XXFP or opc = SETMASKGT_XXPR or opc = SETMASKGT_XXPM or
        opc = SETMASKGT_XXPI or opc = SETMASKGT_XXPF or opc = SETMASKGT_XXPP or
        opc = SETMASKEQ_XXRR or opc = SETMASKEQ_XXRM or opc = SETMASKEQ_XXRI or
        opc = SETMASKEQ_XXRF or opc = SETMASKEQ_XXRP or opc = SETMASKEQ_XXMR or
        opc = SETMASKEQ_XXMM or opc = SETMASKEQ_XXMI or opc = SETMASKEQ_XXMF or
        opc = SETMASKEQ_XXMP or opc = SETMASKEQ_XXIR or opc = SETMASKEQ_XXIM or
        opc = SETMASKEQ_XXIF or opc = SETMASKEQ_XXIP or opc = SETMASKEQ_XXFR or
        opc = SETMASKEQ_XXFM or opc = SETMASKEQ_XXFI or opc = SETMASKEQ_XXFF or
        opc = SETMASKEQ_XXFP or opc = SETMASKEQ_XXPR or opc = SETMASKEQ_XXPM or
        opc = SETMASKEQ_XXPI or opc = SETMASKEQ_XXPF or opc = SETMASKEQ_XXPP or
        opc = SETMASKGE_XXRR or opc = SETMASKGE_XXRM or opc = SETMASKGE_XXRI or
        opc = SETMASKGE_XXRF or opc = SETMASKGE_XXRP or opc = SETMASKGE_XXMR or
        opc = SETMASKGE_XXMM or opc = SETMASKGE_XXMI or opc = SETMASKGE_XXMF or
        opc = SETMASKGE_XXMP or opc = SETMASKGE_XXIR or opc = SETMASKGE_XXIM or
        opc = SETMASKGE_XXIF or opc = SETMASKGE_XXIP or opc = SETMASKGE_XXFR or
        opc = SETMASKGE_XXFM or opc = SETMASKGE_XXFI or opc = SETMASKGE_XXFF or
        opc = SETMASKGE_XXFP or opc = SETMASKGE_XXPR or opc = SETMASKGE_XXPM or
        opc = SETMASKGE_XXPI or opc = SETMASKGE_XXPF or opc = SETMASKGE_XXPP or
        opc = SETMASKLE_XXRR or opc = SETMASKLE_XXRM or opc = SETMASKLE_XXRI or
        opc = SETMASKLE_XXRF or opc = SETMASKLE_XXRP or opc = SETMASKLE_XXMR or
        opc = SETMASKLE_XXMM or opc = SETMASKLE_XXMI or opc = SETMASKLE_XXMF or
        opc = SETMASKLE_XXMP or opc = SETMASKLE_XXIR or opc = SETMASKLE_XXIM or
        opc = SETMASKLE_XXIF or opc = SETMASKLE_XXIP or opc = SETMASKLE_XXFR or
        opc = SETMASKLE_XXFM or opc = SETMASKLE_XXFI or opc = SETMASKLE_XXFF or
        opc = SETMASKLE_XXFP or opc = SETMASKLE_XXPR or opc = SETMASKLE_XXPM or
        opc = SETMASKLE_XXPI or opc = SETMASKLE_XXPF or opc = SETMASKLE_XXPP or
        opc = SETMASKNE_XXRR or opc = SETMASKNE_XXRM or opc = SETMASKNE_XXRI or
        opc = SETMASKNE_XXRF or opc = SETMASKNE_XXRP or opc = SETMASKNE_XXMR or
        opc = SETMASKNE_XXMM or opc = SETMASKNE_XXMI or opc = SETMASKNE_XXMF or
        opc = SETMASKNE_XXMP or opc = SETMASKNE_XXIR or opc = SETMASKNE_XXIM or
        opc = SETMASKNE_XXIF or opc = SETMASKNE_XXIP or opc = SETMASKNE_XXFR or
        opc = SETMASKNE_XXFM or opc = SETMASKNE_XXFI or opc = SETMASKNE_XXFF or
        opc = SETMASKNE_XXFP or opc = SETMASKNE_XXPR or opc = SETMASKNE_XXPM or
        opc = SETMASKNE_XXPI or opc = SETMASKNE_XXPF or opc = SETMASKNE_XXPP or
        -- complx16_4_gen
        opc = CMP_XXRR or opc = CMP_XXRM or opc = CMP_XXRI or
        opc = CMP_XXRF or opc = CMP_XXRP or opc = CMP_XXMR or
        opc = CMP_XXMM or opc = CMP_XXMI or opc = CMP_XXMF or
        opc = CMP_XXMP or opc = CMP_XXIR or opc = CMP_XXIM or
        opc = CMP_XXIF or opc = CMP_XXIP or opc = CMP_XXFR or
        opc = CMP_XXFM or opc = CMP_XXFI or opc = CMP_XXFF or
        opc = CMP_XXFP or opc = CMP_XXPR or opc = CMP_XXPM or
        opc = CMP_XXPI or opc = CMP_XXPF or opc = CMP_XXPP
      then
        -- submul (is cr + ai*bi - ar*br and ci - ai*br - ar*bi)
        -- sub (is cr + 0*bi - 1*br and ci - 0*br - 1*bi)
        opcode0 <=  "00101010011";
        opcode1 <=  "01101010000";
        opcode2 <=  "00101010011";
        opcode3 <=  "01101010011";
      elsif opc = ADDMULFWD_RRRX or opc = ADDMULFWD_RRMX or opc = ADDMULFWD_RRIX or
        opc = ADDMULFWD_RRFX or opc = ADDMULFWD_RRPX or opc = ADDMULFWD_RMRX or
        opc = ADDMULFWD_RMMX or opc = ADDMULFWD_RMIX or opc = ADDMULFWD_RMFX or
        opc = ADDMULFWD_RMPX or opc = ADDMULFWD_RIRX or opc = ADDMULFWD_RIMX or
        opc = ADDMULFWD_RIFX or opc = ADDMULFWD_RIPX or opc = ADDMULFWD_RFRX or
        opc = ADDMULFWD_RFMX or opc = ADDMULFWD_RFIX or opc = ADDMULFWD_RFFX or
        opc = ADDMULFWD_RFPX or opc = ADDMULFWD_RPRX or opc = ADDMULFWD_RPMX or
        opc = ADDMULFWD_RPIX or opc = ADDMULFWD_RPFX or opc = ADDMULFWD_RPPX or
        opc = ADDMULFWD_MRRX or opc = ADDMULFWD_MRMX or opc = ADDMULFWD_MRIX or
        opc = ADDMULFWD_MRFX or opc = ADDMULFWD_MRPX or opc = ADDMULFWD_MMRX or
        opc = ADDMULFWD_MMMX or opc = ADDMULFWD_MMIX or opc = ADDMULFWD_MMFX or
        opc = ADDMULFWD_MMPX or opc = ADDMULFWD_MIRX or opc = ADDMULFWD_MIMX or
        opc = ADDMULFWD_MIFX or opc = ADDMULFWD_MIPX or opc = ADDMULFWD_MFRX or
        opc = ADDMULFWD_MFMX or opc = ADDMULFWD_MFIX or opc = ADDMULFWD_MFFX or
        opc = ADDMULFWD_MFPX or opc = ADDMULFWD_MPRX or opc = ADDMULFWD_MPMX or
        opc = ADDMULFWD_MPIX or opc = ADDMULFWD_MPFX or opc = ADDMULFWD_MPPX or
        opc = ADDMULFWD_FRRX or opc = ADDMULFWD_FRMX or opc = ADDMULFWD_FRIX or
        opc = ADDMULFWD_FRFX or opc = ADDMULFWD_FRPX or opc = ADDMULFWD_FMRX or
        opc = ADDMULFWD_FMMX or opc = ADDMULFWD_FMIX or opc = ADDMULFWD_FMFX or
        -- complx16_4_gen
        opc = ADDMULFWD_FMPX or opc = ADDMULFWD_FIRX or opc = ADDMULFWD_FIMX or
        opc = ADDMULFWD_FIFX or opc = ADDMULFWD_FIPX or opc = ADDMULFWD_FFRX or
        opc = ADDMULFWD_FFMX or opc = ADDMULFWD_FFIX or opc = ADDMULFWD_FFFX or
        opc = ADDMULFWD_FFPX or opc = ADDMULFWD_FPRX or opc = ADDMULFWD_FPMX or
        opc = ADDMULFWD_FPIX or opc = ADDMULFWD_FPFX or opc = ADDMULFWD_FPPX
      then
        -- addfwd (is 0 + 0  Pr + 1*br and 0 + 0  Pi + 1*bi)
        opcode0 <=  "01001010000";
        opcode1 <=  "00000000000";
        opcode2 <=  "01001010000";
        opcode3 <=  "00000000000";
      elsif opc = SUBMULFWD_RRRX or opc = SUBMULFWD_RRMX or opc = SUBMULFWD_RRIX or
        opc = SUBMULFWD_RRFX or opc = SUBMULFWD_RRPX or opc = SUBMULFWD_RMRX or
        opc = SUBMULFWD_RMMX or opc = SUBMULFWD_RMIX or opc = SUBMULFWD_RMFX or
        opc = SUBMULFWD_RMPX or opc = SUBMULFWD_RIRX or opc = SUBMULFWD_RIMX or
        opc = SUBMULFWD_RIFX or opc = SUBMULFWD_RIPX or opc = SUBMULFWD_RFRX or
        opc = SUBMULFWD_RFMX or opc = SUBMULFWD_RFIX or opc = SUBMULFWD_RFFX or
        opc = SUBMULFWD_RFPX or opc = SUBMULFWD_RPRX or opc = SUBMULFWD_RPMX or
        opc = SUBMULFWD_RPIX or opc = SUBMULFWD_RPFX or opc = SUBMULFWD_RPPX or
        opc = SUBMULFWD_MRRX or opc = SUBMULFWD_MRMX or opc = SUBMULFWD_MRIX or
        opc = SUBMULFWD_MRFX or opc = SUBMULFWD_MRPX or opc = SUBMULFWD_MMRX or
        opc = SUBMULFWD_MMMX or opc = SUBMULFWD_MMIX or opc = SUBMULFWD_MMFX or
        opc = SUBMULFWD_MMPX or opc = SUBMULFWD_MIRX or opc = SUBMULFWD_MIMX or
        opc = SUBMULFWD_MIFX or opc = SUBMULFWD_MIPX or opc = SUBMULFWD_MFRX or
        opc = SUBMULFWD_MFMX or opc = SUBMULFWD_MFIX or opc = SUBMULFWD_MFFX or
        opc = SUBMULFWD_MFPX or opc = SUBMULFWD_MPRX or opc = SUBMULFWD_MPMX or
        opc = SUBMULFWD_MPIX or opc = SUBMULFWD_MPFX or opc = SUBMULFWD_MPPX or
        -- complx16_4_gen
        opc = SUBMULFWD_FRRX or opc = SUBMULFWD_FRMX or opc = SUBMULFWD_FRIX or
        opc = SUBMULFWD_FRFX or opc = SUBMULFWD_FRPX or opc = SUBMULFWD_FMRX or
        opc = SUBMULFWD_FMMX or opc = SUBMULFWD_FMIX or opc = SUBMULFWD_FMFX or
        opc = SUBMULFWD_FMPX or opc = SUBMULFWD_FIRX or opc = SUBMULFWD_FIMX or
        opc = SUBMULFWD_FIFX or opc = SUBMULFWD_FIPX or opc = SUBMULFWD_FFRX or
        opc = SUBMULFWD_FFMX or opc = SUBMULFWD_FFIX or opc = SUBMULFWD_FFFX or
        opc = SUBMULFWD_FFPX or opc = SUBMULFWD_FPRX or opc = SUBMULFWD_FPMX or
        opc = SUBMULFWD_FPIX or opc = SUBMULFWD_FPFX or opc = SUBMULFWD_FPPX or
        opc = CMPFWD_XXRX or opc = CMPFWD_XXMX or opc = CMPFWD_XXIX or
        opc = CMPFWD_XXFX or opc = CMPFWD_XXPX
      then
        --subfwd (is 0 + 0  Pr - 1*br and 0 + 0  Pi - 1*bi)
        opcode0 <=  "01001010011";
        opcode1 <=  "00000000000";
        opcode2 <=  "01001010011";
        opcode3 <=  "00000000000";
      else
        opcode0 <=  "00000000000";
        opcode1 <=  "00000000000";
        opcode2 <=  "00000000000";
        opcode3 <=  "00000000000";
      end if;
    end process;

    opmode_02 <= opcode0(10 downto 4);
    opmode_13 <= opcode1(10 downto 4);

    alumode_02 <= opcode0(3 downto 0);
    alumode_1 <= opcode1(3 downto 0);
    alumode_3 <= opcode3(3 downto 0);

    o_id_opmode <= opmode_02 & opmode_13;
    o_id_alumode <= alumode_02 & alumode_1 & alumode_3;
  end generate;

  BARRIERSLAVE_GEN: if BSLAVE = true  and BMASTER = false generate
    signal cnter : std_logic_vector(1 downto 0) := "00";
    type state_type is (s_nml, s_wait);
    signal state: state_type;
  begin
    -- en_pc
    o_en_pc <= '0' when (opc = BARRIERS and i_ext_barrier = '0') else '1';
    -- en_sFPE
    -- every time both reaches barrier point, it needs to wait several cycles to recover sFPE (to
    -- deassert i_ext_barrier). IOCore keeps running after it checks barrier point, so if we do not
    -- have a state of 'wait', o_ext_en_sFPE will be wrongly asserted again.
    process (clk) begin
      if (clk'event and clk = '1') then
        case state is
          when s_nml =>
            if (opc = BARRIERS and i_ext_barrier = '1') then
              state <= s_wait;
            end if;
          when s_wait =>
            if (cnter = "11") then
              state <= s_nml;
            end if;
            cnter <= std_logic_vector(unsigned(cnter)+1);
        end case;
      end if;
    end process;

    o_ext_en_sFPE <= '0' when (state = s_nml and opc /= BARRIERS and i_ext_barrier = '1') else '1';
  end generate;

  -- To improve performance, barrier is responded two cycles latter.
  -- So it should stall the pipeline for two cycles.
  BARRIERMASTER_GEN: if BSLAVE = false and BMASTER = true generate
    signal shifter: std_logic_vector (1 downto 0) := (others=>'0');
    signal start_shifter : std_logic := '0';
    signal clear_shifter : std_logic := '0';
  begin
    process(opc, shifter(1), i_ext_en_sFPE)
    begin
      o_en_pc <= '1';
      start_shifter <= '0';
      if(opc = BARRIERM and shifter(1) = '0') then
        o_en_pc <= '0';
        start_shifter <= '1';
      else
        o_en_pc <= i_ext_en_sFPE;
      end if;
    end process;

    clear_shifter <= '1' when opc /= BARRIERM else '0';

    process(clk) begin
      if rising_edge(clk) then
        if (clear_shifter = '1') then
          shifter <= "00";
        elsif (start_shifter = '1') then
          shifter <= shifter(0) & '1';
        end if;
      end if;
    end process;
  end generate;

  BARRIER_MASTER_SLAVE_GEN: if BSLAVE = true  and BMASTER = true generate
    signal shifter: std_logic_vector (1 downto 0) := (others=>'0');
    signal start_shifter : std_logic := '0';
    signal clear_shifter : std_logic := '0';
    signal cnter : std_logic_vector(1 downto 0) := "00";
    type state_type is (s_nml, s_wait);
    signal state: state_type;
  begin
    -- en_pc
    process(opc, shifter(1), i_ext_en_sFPE, i_ext_barrier)
    begin
      o_en_pc <= '1';
      start_shifter <= '0';
      if (opc = BARRIERS and i_ext_barrier = '0') then
        -- Slave is faster
        o_en_pc <= '0';
      elsif (opc = BARRIERM and shifter(1) = '0') then
        -- Master is waiting for response
        o_en_pc <= '0';
        start_shifter <= '1';
      else
        -- Master is decided by slave's response
        o_en_pc <= i_ext_en_sFPE;
      end if;
    end process;

    clear_shifter <= '1' when opc /= BARRIERM else '0';
    process(clk) begin
      if rising_edge(clk) then
        if (clear_shifter = '1') then
          shifter <= "00";
        elsif (start_shifter = '1') then
          shifter <= shifter(0) & '1';
        end if;
      end if;
    end process;

    -- en_sFPE
    -- every time both reaches barrier point, it needs to wait several cycles to recover sFPE (to
    -- deassert i_ext_barrier). IOCore keeps running after it checks barrier point, so if we do not
    -- have a state of 'wait', o_ext_en_sFPE will be wrongly asserted again.
    process (clk) begin
      if (clk'event and clk = '1') then
        case state is
          when s_nml =>
            if (opc = BARRIERS and i_ext_barrier = '1') then
              -- Both reaches the point, slave waits master to release i_ext_barrier.
              state <= s_wait;
            end if;
          when s_wait =>
            if (cnter = "11") then
              state <= s_nml;
            end if;
            cnter <= std_logic_vector(unsigned(cnter)+1);
        end case;
      end if;
    end process;

    -- Master is faster, stop master
    o_ext_en_sFPE <= '0' when (state = s_nml and opc /= BARRIERS and i_ext_barrier = '1') else '1';
  end generate;

  NOIOCORE_GEN: if (BSLAVE = false and BMASTER = false) generate
    o_en_pc <= '1';
  end generate;
  ----------------------------------------------------
  -- Custom Instruction
  ----------------------------------------------------
  -- ALU result shift right arithmetic by 1
  ALUSRA_GEN: if ALUSRA_EN = true generate
    o_id_alusra <= '1' when
      opc = ADDMULSRA_RRRR or opc = ADDMULSRA_RRRM or opc = ADDMULSRA_RRRI or
      opc = ADDMULSRA_RRRF or opc = ADDMULSRA_RRRP or opc = ADDMULSRA_RRMR or
      opc = ADDMULSRA_RRMM or opc = ADDMULSRA_RRMI or opc = ADDMULSRA_RRMF or
      opc = ADDMULSRA_RRMP or opc = ADDMULSRA_RRIR or opc = ADDMULSRA_RRIM or
      opc = ADDMULSRA_RRIF or opc = ADDMULSRA_RRIP or opc = ADDMULSRA_RRFR or
      opc = ADDMULSRA_RRFM or opc = ADDMULSRA_RRFI or opc = ADDMULSRA_RRFF or
      opc = ADDMULSRA_RRFP or opc = ADDMULSRA_RRPR or opc = ADDMULSRA_RRPM or
      opc = ADDMULSRA_RRPI or opc = ADDMULSRA_RRPF or opc = ADDMULSRA_RRPP or
      opc = ADDMULSRA_RMRR or opc = ADDMULSRA_RMRM or opc = ADDMULSRA_RMRI or
      opc = ADDMULSRA_RMRF or opc = ADDMULSRA_RMRP or opc = ADDMULSRA_RMMR or
      opc = ADDMULSRA_RMMI or opc = ADDMULSRA_RMMF or opc = ADDMULSRA_RMMP or
      opc = ADDMULSRA_RMIR or opc = ADDMULSRA_RMIM or opc = ADDMULSRA_RMIF or
      opc = ADDMULSRA_RMIP or opc = ADDMULSRA_RMFR or opc = ADDMULSRA_RMFM or
      opc = ADDMULSRA_RMFI or opc = ADDMULSRA_RMFF or opc = ADDMULSRA_RMFP or
      opc = ADDMULSRA_RMPR or opc = ADDMULSRA_RMPM or opc = ADDMULSRA_RMPI or
      opc = ADDMULSRA_RMPF or opc = ADDMULSRA_RMPP or opc = ADDMULSRA_RIRR or
      opc = ADDMULSRA_RIRM or opc = ADDMULSRA_RIRF or opc = ADDMULSRA_RIRP or
      opc = ADDMULSRA_RIMR or opc = ADDMULSRA_RIMM or opc = ADDMULSRA_RIMF or
      opc = ADDMULSRA_RIMP or opc = ADDMULSRA_RIFR or opc = ADDMULSRA_RIFM or
      opc = ADDMULSRA_RIFF or opc = ADDMULSRA_RIFP or opc = ADDMULSRA_RIPR or
      opc = ADDMULSRA_RIPM or opc = ADDMULSRA_RIPF or opc = ADDMULSRA_RIPP or
      opc = ADDMULSRA_RFRR or opc = ADDMULSRA_RFRM or opc = ADDMULSRA_RFRI or
      opc = ADDMULSRA_RFRF or opc = ADDMULSRA_RFRP or opc = ADDMULSRA_RFMR or
      opc = ADDMULSRA_RFMM or opc = ADDMULSRA_RFMI or opc = ADDMULSRA_RFMF or
      opc = ADDMULSRA_RFMP or opc = ADDMULSRA_RFIR or opc = ADDMULSRA_RFIM or
      opc = ADDMULSRA_RFIF or opc = ADDMULSRA_RFIP or opc = ADDMULSRA_RFFR or
      opc = ADDMULSRA_RFFM or opc = ADDMULSRA_RFFI or opc = ADDMULSRA_RFPR or
      opc = ADDMULSRA_RFPM or opc = ADDMULSRA_RFPI or opc = ADDMULSRA_RPRR or
      opc = ADDMULSRA_RPRM or opc = ADDMULSRA_RPRI or opc = ADDMULSRA_RPRF or
      opc = ADDMULSRA_RPRP or opc = ADDMULSRA_RPMR or opc = ADDMULSRA_RPMM or
      opc = ADDMULSRA_RPMI or opc = ADDMULSRA_RPMF or opc = ADDMULSRA_RPMP or
      opc = ADDMULSRA_RPIR or opc = ADDMULSRA_RPIM or opc = ADDMULSRA_RPIF or
      opc = ADDMULSRA_RPIP or opc = ADDMULSRA_RPFR or opc = ADDMULSRA_RPFM or
      opc = ADDMULSRA_RPFI or opc = ADDMULSRA_RPPR or opc = ADDMULSRA_RPPM or
      opc = ADDMULSRA_RPPI or opc = ADDMULSRA_MRRR or opc = ADDMULSRA_MRRM or
      opc = ADDMULSRA_MRRI or opc = ADDMULSRA_MRRF or opc = ADDMULSRA_MRRP or
      opc = ADDMULSRA_MRMR or opc = ADDMULSRA_MRMM or opc = ADDMULSRA_MRMI or
      opc = ADDMULSRA_MRMF or opc = ADDMULSRA_MRMP or opc = ADDMULSRA_MRIR or
      opc = ADDMULSRA_MRIM or opc = ADDMULSRA_MRIF or opc = ADDMULSRA_MRIP or
      opc = ADDMULSRA_MRFR or opc = ADDMULSRA_MRFM or opc = ADDMULSRA_MRFI or
      opc = ADDMULSRA_MRFF or opc = ADDMULSRA_MRFP or opc = ADDMULSRA_MRPR or
      opc = ADDMULSRA_MRPM or opc = ADDMULSRA_MRPI or opc = ADDMULSRA_MRPF or
      opc = ADDMULSRA_MRPP or opc = ADDMULSRA_MMRR or opc = ADDMULSRA_MMRM or
      opc = ADDMULSRA_MMRI or opc = ADDMULSRA_MMRF or opc = ADDMULSRA_MMRP or
      opc = ADDMULSRA_MMMR or opc = ADDMULSRA_MMMI or opc = ADDMULSRA_MMMF or
      opc = ADDMULSRA_MMMP or opc = ADDMULSRA_MMIR or opc = ADDMULSRA_MMIM or
      opc = ADDMULSRA_MMIF or opc = ADDMULSRA_MMIP or opc = ADDMULSRA_MMFR or
      opc = ADDMULSRA_MMFM or opc = ADDMULSRA_MMFI or opc = ADDMULSRA_MMFF or
      opc = ADDMULSRA_MMFP or opc = ADDMULSRA_MMPR or opc = ADDMULSRA_MMPM or
      opc = ADDMULSRA_MMPI or opc = ADDMULSRA_MMPF or opc = ADDMULSRA_MMPP or
      opc = ADDMULSRA_MIRR or opc = ADDMULSRA_MIRM or opc = ADDMULSRA_MIRF or
      opc = ADDMULSRA_MIRP or opc = ADDMULSRA_MIMR or opc = ADDMULSRA_MIMM or
      opc = ADDMULSRA_MIMF or opc = ADDMULSRA_MIMP or opc = ADDMULSRA_MIFR or
      opc = ADDMULSRA_MIFM or opc = ADDMULSRA_MIFF or opc = ADDMULSRA_MIFP or
      opc = ADDMULSRA_MIPR or opc = ADDMULSRA_MIPM or opc = ADDMULSRA_MIPF or
      opc = ADDMULSRA_MIPP or opc = ADDMULSRA_MFRR or opc = ADDMULSRA_MFRM or
      opc = ADDMULSRA_MFRI or opc = ADDMULSRA_MFRF or opc = ADDMULSRA_MFRP or
      opc = ADDMULSRA_MFMR or opc = ADDMULSRA_MFMM or opc = ADDMULSRA_MFMI or
      opc = ADDMULSRA_MFMF or opc = ADDMULSRA_MFMP or opc = ADDMULSRA_MFIR or
      opc = ADDMULSRA_MFIM or opc = ADDMULSRA_MFIF or opc = ADDMULSRA_MFIP or
      opc = ADDMULSRA_MFFR or opc = ADDMULSRA_MFFM or opc = ADDMULSRA_MFFI or
      opc = ADDMULSRA_MFPR or opc = ADDMULSRA_MFPM or opc = ADDMULSRA_MFPI or
      opc = ADDMULSRA_MPRR or opc = ADDMULSRA_MPRM or opc = ADDMULSRA_MPRI or
      opc = ADDMULSRA_MPRF or opc = ADDMULSRA_MPRP or opc = ADDMULSRA_MPMR or
      opc = ADDMULSRA_MPMM or opc = ADDMULSRA_MPMI or opc = ADDMULSRA_MPMF or
      opc = ADDMULSRA_MPMP or opc = ADDMULSRA_MPIR or opc = ADDMULSRA_MPIM or
      opc = ADDMULSRA_MPIF or opc = ADDMULSRA_MPIP or opc = ADDMULSRA_MPFR or
      opc = ADDMULSRA_MPFM or opc = ADDMULSRA_MPFI or opc = ADDMULSRA_MPPR or
      opc = ADDMULSRA_MPPM or opc = ADDMULSRA_MPPI or opc = ADDMULSRA_FRRR or
      opc = ADDMULSRA_FRRM or opc = ADDMULSRA_FRRI or opc = ADDMULSRA_FRRF or
      opc = ADDMULSRA_FRRP or opc = ADDMULSRA_FRMR or opc = ADDMULSRA_FRMM or
      opc = ADDMULSRA_FRMI or opc = ADDMULSRA_FRMF or opc = ADDMULSRA_FRMP or
      opc = ADDMULSRA_FRIR or opc = ADDMULSRA_FRIM or opc = ADDMULSRA_FRIF or
      opc = ADDMULSRA_FRIP or opc = ADDMULSRA_FRFR or opc = ADDMULSRA_FRFM or
      opc = ADDMULSRA_FRFI or opc = ADDMULSRA_FRFF or opc = ADDMULSRA_FRFP or
      opc = ADDMULSRA_FRPR or opc = ADDMULSRA_FRPM or opc = ADDMULSRA_FRPI or
      opc = ADDMULSRA_FRPF or opc = ADDMULSRA_FRPP or opc = ADDMULSRA_FMRR or
      opc = ADDMULSRA_FMRM or opc = ADDMULSRA_FMRI or opc = ADDMULSRA_FMRF or
      opc = ADDMULSRA_FMRP or opc = ADDMULSRA_FMMR or opc = ADDMULSRA_FMMI or
      opc = ADDMULSRA_FMMF or opc = ADDMULSRA_FMMP or opc = ADDMULSRA_FMIR or
      opc = ADDMULSRA_FMIM or opc = ADDMULSRA_FMIF or opc = ADDMULSRA_FMIP or
      opc = ADDMULSRA_FMFR or opc = ADDMULSRA_FMFM or opc = ADDMULSRA_FMFI or
      opc = ADDMULSRA_FMFF or opc = ADDMULSRA_FMFP or opc = ADDMULSRA_FMPR or
      opc = ADDMULSRA_FMPM or opc = ADDMULSRA_FMPI or opc = ADDMULSRA_FMPF or
      opc = ADDMULSRA_FMPP or opc = ADDMULSRA_FIRR or opc = ADDMULSRA_FIRM or
      opc = ADDMULSRA_FIRF or opc = ADDMULSRA_FIRP or opc = ADDMULSRA_FIMR or
      opc = ADDMULSRA_FIMM or opc = ADDMULSRA_FIMF or opc = ADDMULSRA_FIMP or
      opc = ADDMULSRA_FIFR or opc = ADDMULSRA_FIFM or opc = ADDMULSRA_FIFF or
      opc = ADDMULSRA_FIFP or opc = ADDMULSRA_FIPR or opc = ADDMULSRA_FIPM or
      opc = ADDMULSRA_FIPF or opc = ADDMULSRA_FIPP or opc = ADDMULSRA_FFRR or
      opc = ADDMULSRA_FFRM or opc = ADDMULSRA_FFRI or opc = ADDMULSRA_FFRF or
      opc = ADDMULSRA_FFRP or opc = ADDMULSRA_FFMR or opc = ADDMULSRA_FFMM or
      opc = ADDMULSRA_FFMI or opc = ADDMULSRA_FFMF or opc = ADDMULSRA_FFMP or
      opc = ADDMULSRA_FFIR or opc = ADDMULSRA_FFIM or opc = ADDMULSRA_FFIF or
      opc = ADDMULSRA_FFIP or opc = ADDMULSRA_FFFR or opc = ADDMULSRA_FFFM or
      opc = ADDMULSRA_FFFI or opc = ADDMULSRA_FFPR or opc = ADDMULSRA_FFPM or
      opc = ADDMULSRA_FFPI or opc = ADDMULSRA_FPRR or opc = ADDMULSRA_FPRM or
      opc = ADDMULSRA_FPRI or opc = ADDMULSRA_FPRF or opc = ADDMULSRA_FPRP or
      opc = ADDMULSRA_FPMR or opc = ADDMULSRA_FPMM or opc = ADDMULSRA_FPMI or
      opc = ADDMULSRA_FPMF or opc = ADDMULSRA_FPMP or opc = ADDMULSRA_FPIR or
      opc = ADDMULSRA_FPIM or opc = ADDMULSRA_FPIF or opc = ADDMULSRA_FPIP or
      opc = ADDMULSRA_FPFR or opc = ADDMULSRA_FPFM or opc = ADDMULSRA_FPFI or
      opc = ADDMULSRA_FPPR or opc = ADDMULSRA_FPPM or opc = ADDMULSRA_FPPI or
      opc = SUBMULSRA_RRRR or opc = SUBMULSRA_RRRM or opc = SUBMULSRA_RRRI or
      opc = SUBMULSRA_RRRF or opc = SUBMULSRA_RRRP or opc = SUBMULSRA_RRMR or
      opc = SUBMULSRA_RRMM or opc = SUBMULSRA_RRMI or opc = SUBMULSRA_RRMF or
      opc = SUBMULSRA_RRMP or opc = SUBMULSRA_RRIR or opc = SUBMULSRA_RRIM or
      opc = SUBMULSRA_RRIF or opc = SUBMULSRA_RRIP or opc = SUBMULSRA_RRFR or
      opc = SUBMULSRA_RRFM or opc = SUBMULSRA_RRFI or opc = SUBMULSRA_RRFF or
      opc = SUBMULSRA_RRFP or opc = SUBMULSRA_RRPR or opc = SUBMULSRA_RRPM or
      opc = SUBMULSRA_RRPI or opc = SUBMULSRA_RRPF or opc = SUBMULSRA_RRPP or
      opc = SUBMULSRA_RMRR or opc = SUBMULSRA_RMRM or opc = SUBMULSRA_RMRI or
      opc = SUBMULSRA_RMRF or opc = SUBMULSRA_RMRP or opc = SUBMULSRA_RMMR or
      opc = SUBMULSRA_RMMI or opc = SUBMULSRA_RMMF or opc = SUBMULSRA_RMMP or
      opc = SUBMULSRA_RMIR or opc = SUBMULSRA_RMIM or opc = SUBMULSRA_RMIF or
      opc = SUBMULSRA_RMIP or opc = SUBMULSRA_RMFR or opc = SUBMULSRA_RMFM or
      opc = SUBMULSRA_RMFI or opc = SUBMULSRA_RMFF or opc = SUBMULSRA_RMFP or
      opc = SUBMULSRA_RMPR or opc = SUBMULSRA_RMPM or opc = SUBMULSRA_RMPI or
      opc = SUBMULSRA_RMPF or opc = SUBMULSRA_RMPP or opc = SUBMULSRA_RIRR or
      opc = SUBMULSRA_RIRM or opc = SUBMULSRA_RIRF or opc = SUBMULSRA_RIRP or
      opc = SUBMULSRA_RIMR or opc = SUBMULSRA_RIMM or opc = SUBMULSRA_RIMF or
      opc = SUBMULSRA_RIMP or opc = SUBMULSRA_RIFR or opc = SUBMULSRA_RIFM or
      opc = SUBMULSRA_RIFF or opc = SUBMULSRA_RIFP or opc = SUBMULSRA_RIPR or
      opc = SUBMULSRA_RIPM or opc = SUBMULSRA_RIPF or opc = SUBMULSRA_RIPP or
      opc = SUBMULSRA_RFRR or opc = SUBMULSRA_RFRM or opc = SUBMULSRA_RFRI or
      opc = SUBMULSRA_RFRF or opc = SUBMULSRA_RFRP or opc = SUBMULSRA_RFMR or
      opc = SUBMULSRA_RFMM or opc = SUBMULSRA_RFMI or opc = SUBMULSRA_RFMF or
      opc = SUBMULSRA_RFMP or opc = SUBMULSRA_RFIR or opc = SUBMULSRA_RFIM or
      opc = SUBMULSRA_RFIF or opc = SUBMULSRA_RFIP or opc = SUBMULSRA_RFFR or
      opc = SUBMULSRA_RFFM or opc = SUBMULSRA_RFFI or opc = SUBMULSRA_RFPR or
      opc = SUBMULSRA_RFPM or opc = SUBMULSRA_RFPI or opc = SUBMULSRA_RPRR or
      opc = SUBMULSRA_RPRM or opc = SUBMULSRA_RPRI or opc = SUBMULSRA_RPRF or
      opc = SUBMULSRA_RPRP or opc = SUBMULSRA_RPMR or opc = SUBMULSRA_RPMM or
      opc = SUBMULSRA_RPMI or opc = SUBMULSRA_RPMF or opc = SUBMULSRA_RPMP or
      opc = SUBMULSRA_RPIR or opc = SUBMULSRA_RPIM or opc = SUBMULSRA_RPIF or
      opc = SUBMULSRA_RPIP or opc = SUBMULSRA_RPFR or opc = SUBMULSRA_RPFM or
      opc = SUBMULSRA_RPFI or opc = SUBMULSRA_RPPR or opc = SUBMULSRA_RPPM or
      opc = SUBMULSRA_RPPI or opc = SUBMULSRA_MRRR or opc = SUBMULSRA_MRRM or
      opc = SUBMULSRA_MRRI or opc = SUBMULSRA_MRRF or opc = SUBMULSRA_MRRP or
      opc = SUBMULSRA_MRMR or opc = SUBMULSRA_MRMM or opc = SUBMULSRA_MRMI or
      opc = SUBMULSRA_MRMF or opc = SUBMULSRA_MRMP or opc = SUBMULSRA_MRIR or
      opc = SUBMULSRA_MRIM or opc = SUBMULSRA_MRIF or opc = SUBMULSRA_MRIP or
      opc = SUBMULSRA_MRFR or opc = SUBMULSRA_MRFM or opc = SUBMULSRA_MRFI or
      opc = SUBMULSRA_MRFF or opc = SUBMULSRA_MRFP or opc = SUBMULSRA_MRPR or
      opc = SUBMULSRA_MRPM or opc = SUBMULSRA_MRPI or opc = SUBMULSRA_MRPF or
      opc = SUBMULSRA_MRPP or opc = SUBMULSRA_MMRR or opc = SUBMULSRA_MMRM or
      opc = SUBMULSRA_MMRI or opc = SUBMULSRA_MMRF or opc = SUBMULSRA_MMRP or
      opc = SUBMULSRA_MMMR or opc = SUBMULSRA_MMMI or opc = SUBMULSRA_MMMF or
      opc = SUBMULSRA_MMMP or opc = SUBMULSRA_MMIR or opc = SUBMULSRA_MMIM or
      opc = SUBMULSRA_MMIF or opc = SUBMULSRA_MMIP or opc = SUBMULSRA_MMFR or
      opc = SUBMULSRA_MMFM or opc = SUBMULSRA_MMFI or opc = SUBMULSRA_MMFF or
      opc = SUBMULSRA_MMFP or opc = SUBMULSRA_MMPR or opc = SUBMULSRA_MMPM or
      opc = SUBMULSRA_MMPI or opc = SUBMULSRA_MMPF or opc = SUBMULSRA_MMPP or
      opc = SUBMULSRA_MIRR or opc = SUBMULSRA_MIRM or opc = SUBMULSRA_MIRF or
      opc = SUBMULSRA_MIRP or opc = SUBMULSRA_MIMR or opc = SUBMULSRA_MIMM or
      opc = SUBMULSRA_MIMF or opc = SUBMULSRA_MIMP or opc = SUBMULSRA_MIFR or
      opc = SUBMULSRA_MIFM or opc = SUBMULSRA_MIFF or opc = SUBMULSRA_MIFP or
      opc = SUBMULSRA_MIPR or opc = SUBMULSRA_MIPM or opc = SUBMULSRA_MIPF or
      opc = SUBMULSRA_MIPP or opc = SUBMULSRA_MFRR or opc = SUBMULSRA_MFRM or
      opc = SUBMULSRA_MFRI or opc = SUBMULSRA_MFRF or opc = SUBMULSRA_MFRP or
      opc = SUBMULSRA_MFMR or opc = SUBMULSRA_MFMM or opc = SUBMULSRA_MFMI or
      opc = SUBMULSRA_MFMF or opc = SUBMULSRA_MFMP or opc = SUBMULSRA_MFIR or
      opc = SUBMULSRA_MFIM or opc = SUBMULSRA_MFIF or opc = SUBMULSRA_MFIP or
      opc = SUBMULSRA_MFFR or opc = SUBMULSRA_MFFM or opc = SUBMULSRA_MFFI or
      opc = SUBMULSRA_MFPR or opc = SUBMULSRA_MFPM or opc = SUBMULSRA_MFPI or
      opc = SUBMULSRA_MPRR or opc = SUBMULSRA_MPRM or opc = SUBMULSRA_MPRI or
      opc = SUBMULSRA_MPRF or opc = SUBMULSRA_MPRP or opc = SUBMULSRA_MPMR or
      opc = SUBMULSRA_MPMM or opc = SUBMULSRA_MPMI or opc = SUBMULSRA_MPMF or
      opc = SUBMULSRA_MPMP or opc = SUBMULSRA_MPIR or opc = SUBMULSRA_MPIM or
      opc = SUBMULSRA_MPIF or opc = SUBMULSRA_MPIP or opc = SUBMULSRA_MPFR or
      opc = SUBMULSRA_MPFM or opc = SUBMULSRA_MPFI or opc = SUBMULSRA_MPPR or
      opc = SUBMULSRA_MPPM or opc = SUBMULSRA_MPPI or opc = SUBMULSRA_FRRR or
      opc = SUBMULSRA_FRRM or opc = SUBMULSRA_FRRI or opc = SUBMULSRA_FRRF or
      opc = SUBMULSRA_FRRP or opc = SUBMULSRA_FRMR or opc = SUBMULSRA_FRMM or
      opc = SUBMULSRA_FRMI or opc = SUBMULSRA_FRMF or opc = SUBMULSRA_FRMP or
      opc = SUBMULSRA_FRIR or opc = SUBMULSRA_FRIM or opc = SUBMULSRA_FRIF or
      opc = SUBMULSRA_FRIP or opc = SUBMULSRA_FRFR or opc = SUBMULSRA_FRFM or
      opc = SUBMULSRA_FRFI or opc = SUBMULSRA_FRFF or opc = SUBMULSRA_FRFP or
      opc = SUBMULSRA_FRPR or opc = SUBMULSRA_FRPM or opc = SUBMULSRA_FRPI or
      opc = SUBMULSRA_FRPF or opc = SUBMULSRA_FRPP or opc = SUBMULSRA_FMRR or
      opc = SUBMULSRA_FMRM or opc = SUBMULSRA_FMRI or opc = SUBMULSRA_FMRF or
      opc = SUBMULSRA_FMRP or opc = SUBMULSRA_FMMR or opc = SUBMULSRA_FMMI or
      opc = SUBMULSRA_FMMF or opc = SUBMULSRA_FMMP or opc = SUBMULSRA_FMIR or
      opc = SUBMULSRA_FMIM or opc = SUBMULSRA_FMIF or opc = SUBMULSRA_FMIP or
      opc = SUBMULSRA_FMFR or opc = SUBMULSRA_FMFM or opc = SUBMULSRA_FMFI or
      opc = SUBMULSRA_FMFF or opc = SUBMULSRA_FMFP or opc = SUBMULSRA_FMPR or
      opc = SUBMULSRA_FMPM or opc = SUBMULSRA_FMPI or opc = SUBMULSRA_FMPF or
      opc = SUBMULSRA_FMPP or opc = SUBMULSRA_FIRR or opc = SUBMULSRA_FIRM or
      opc = SUBMULSRA_FIRF or opc = SUBMULSRA_FIRP or opc = SUBMULSRA_FIMR or
      opc = SUBMULSRA_FIMM or opc = SUBMULSRA_FIMF or opc = SUBMULSRA_FIMP or
      opc = SUBMULSRA_FIFR or opc = SUBMULSRA_FIFM or opc = SUBMULSRA_FIFF or
      opc = SUBMULSRA_FIFP or opc = SUBMULSRA_FIPR or opc = SUBMULSRA_FIPM or
      opc = SUBMULSRA_FIPF or opc = SUBMULSRA_FIPP or opc = SUBMULSRA_FFRR or
      opc = SUBMULSRA_FFRM or opc = SUBMULSRA_FFRI or opc = SUBMULSRA_FFRF or
      opc = SUBMULSRA_FFRP or opc = SUBMULSRA_FFMR or opc = SUBMULSRA_FFMM or
      opc = SUBMULSRA_FFMI or opc = SUBMULSRA_FFMF or opc = SUBMULSRA_FFMP or
      opc = SUBMULSRA_FFIR or opc = SUBMULSRA_FFIM or opc = SUBMULSRA_FFIF or
      opc = SUBMULSRA_FFIP or opc = SUBMULSRA_FFFR or opc = SUBMULSRA_FFFM or
      opc = SUBMULSRA_FFFI or opc = SUBMULSRA_FFPR or opc = SUBMULSRA_FFPM or
      opc = SUBMULSRA_FFPI or opc = SUBMULSRA_FPRR or opc = SUBMULSRA_FPRM or
      opc = SUBMULSRA_FPRI or opc = SUBMULSRA_FPRF or opc = SUBMULSRA_FPRP or
      opc = SUBMULSRA_FPMR or opc = SUBMULSRA_FPMM or opc = SUBMULSRA_FPMI or
      opc = SUBMULSRA_FPMF or opc = SUBMULSRA_FPMP or opc = SUBMULSRA_FPIR or
      opc = SUBMULSRA_FPIM or opc = SUBMULSRA_FPIF or opc = SUBMULSRA_FPIP or
      opc = SUBMULSRA_FPFR or opc = SUBMULSRA_FPFM or opc = SUBMULSRA_FPFI or
      opc = SUBMULSRA_FPPR or opc = SUBMULSRA_FPPM or opc = SUBMULSRA_FPPI
    else '0';
  end generate;

  ABSDIFF_GEN: if ABSDIFF_EN = true generate
    o_id_CA_absdiff_clr <= '1' when
      opc = ABSDIFFCLR or
      opc = ABSDIFFACCUM_RXRR or opc = ABSDIFFACCUM_RXRM or opc = ABSDIFFACCUM_RXRI or
      opc = ABSDIFFACCUM_RXRF or opc = ABSDIFFACCUM_RXRP or opc = ABSDIFFACCUM_RXMR or
      opc = ABSDIFFACCUM_RXMM or opc = ABSDIFFACCUM_RXMI or opc = ABSDIFFACCUM_RXMF or
      opc = ABSDIFFACCUM_RXMP or opc = ABSDIFFACCUM_RXIR or opc = ABSDIFFACCUM_RXIM or
      opc = ABSDIFFACCUM_RXIF or opc = ABSDIFFACCUM_RXIP or opc = ABSDIFFACCUM_RXFR or
      opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXFI or opc = ABSDIFFACCUM_RXFF or
      opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_RXPR or opc = ABSDIFFACCUM_RXPM or
      opc = ABSDIFFACCUM_RXPI or opc = ABSDIFFACCUM_RXPF or opc = ABSDIFFACCUM_RXPP or
      opc = ABSDIFFACCUM_MXRR or opc = ABSDIFFACCUM_MXRM or opc = ABSDIFFACCUM_MXRI or
      opc = ABSDIFFACCUM_MXRF or opc = ABSDIFFACCUM_MXRP or opc = ABSDIFFACCUM_MXMR or
      opc = ABSDIFFACCUM_MXMM or opc = ABSDIFFACCUM_MXMI or opc = ABSDIFFACCUM_MXMF or
      opc = ABSDIFFACCUM_MXMP or opc = ABSDIFFACCUM_MXIR or opc = ABSDIFFACCUM_MXIM or
      opc = ABSDIFFACCUM_MXIF or opc = ABSDIFFACCUM_MXIP or opc = ABSDIFFACCUM_MXFR or
      opc = ABSDIFFACCUM_MXFM or opc = ABSDIFFACCUM_MXFI or opc = ABSDIFFACCUM_MXFF or
      opc = ABSDIFFACCUM_MXFP or opc = ABSDIFFACCUM_MXPR or opc = ABSDIFFACCUM_MXPM or
      opc = ABSDIFFACCUM_MXPI or opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_MXPP or
      opc = ABSDIFFACCUM_FXRR or opc = ABSDIFFACCUM_FXRM or opc = ABSDIFFACCUM_FXRI or
      opc = ABSDIFFACCUM_FXRF or opc = ABSDIFFACCUM_FXRP or opc = ABSDIFFACCUM_FXMR or
      opc = ABSDIFFACCUM_FXMM or opc = ABSDIFFACCUM_FXMI or opc = ABSDIFFACCUM_FXMF or
      opc = ABSDIFFACCUM_FXMP or opc = ABSDIFFACCUM_FXIR or opc = ABSDIFFACCUM_FXIM or
      opc = ABSDIFFACCUM_FXIF or opc = ABSDIFFACCUM_FXIP or opc = ABSDIFFACCUM_FXFR or
      opc = ABSDIFFACCUM_FXFM or opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXFF or
      opc = ABSDIFFACCUM_FXFP or opc = ABSDIFFACCUM_FXPR or opc = ABSDIFFACCUM_FXPM or
      opc = ABSDIFFACCUM_FXPI or opc = ABSDIFFACCUM_FXPF or opc = ABSDIFFACCUM_FXPP
    else '0';
    o_id_CA_absdiff <= '1' when
      opc = ABSDIFF_RXRR or opc = ABSDIFF_RXRM or opc = ABSDIFF_RXRI or
      opc = ABSDIFF_RXRF or opc = ABSDIFF_RXRP or opc = ABSDIFF_RXMR or
      opc = ABSDIFF_RXMM or opc = ABSDIFF_RXMI or opc = ABSDIFF_RXMF or
      opc = ABSDIFF_RXMP or opc = ABSDIFF_RXIR or opc = ABSDIFF_RXIM or
      opc = ABSDIFF_RXIF or opc = ABSDIFF_RXIP or opc = ABSDIFF_RXFR or
      opc = ABSDIFF_RXFM or opc = ABSDIFF_RXFI or opc = ABSDIFF_RXFF or
      opc = ABSDIFF_RXFP or opc = ABSDIFF_RXPR or opc = ABSDIFF_RXPM or
      opc = ABSDIFF_RXPI or opc = ABSDIFF_RXPF or opc = ABSDIFF_RXPP or
      opc = ABSDIFF_MXRR or opc = ABSDIFF_MXRM or opc = ABSDIFF_MXRI or
      opc = ABSDIFF_MXRF or opc = ABSDIFF_MXRP or opc = ABSDIFF_MXMR or
      opc = ABSDIFF_MXMM or opc = ABSDIFF_MXMI or opc = ABSDIFF_MXMF or
      opc = ABSDIFF_MXMP or opc = ABSDIFF_MXIR or opc = ABSDIFF_MXIM or
      opc = ABSDIFF_MXIF or opc = ABSDIFF_MXIP or opc = ABSDIFF_MXFR or
      opc = ABSDIFF_MXFM or opc = ABSDIFF_MXFI or opc = ABSDIFF_MXFF or
      opc = ABSDIFF_MXFP or opc = ABSDIFF_MXPR or opc = ABSDIFF_MXPM or
      opc = ABSDIFF_MXPI or opc = ABSDIFF_MXPF or opc = ABSDIFF_MXPP or
      opc = ABSDIFF_FXRR or opc = ABSDIFF_FXRM or opc = ABSDIFF_FXRI or
      opc = ABSDIFF_FXRF or opc = ABSDIFF_FXRP or opc = ABSDIFF_FXMR or
      opc = ABSDIFF_FXMM or opc = ABSDIFF_FXMI or opc = ABSDIFF_FXMF or
      opc = ABSDIFF_FXMP or opc = ABSDIFF_FXIR or opc = ABSDIFF_FXIM or
      opc = ABSDIFF_FXIF or opc = ABSDIFF_FXIP or opc = ABSDIFF_FXFR or
      opc = ABSDIFF_FXFM or opc = ABSDIFF_FXFI or opc = ABSDIFF_FXFF or
      opc = ABSDIFF_FXFP or opc = ABSDIFF_FXPR or opc = ABSDIFF_FXPM or
      opc = ABSDIFF_FXPI or opc = ABSDIFF_FXPF or opc = ABSDIFF_FXPP or
      opc = ABSDIFFACCUM_RXRR or opc = ABSDIFFACCUM_RXRM or opc = ABSDIFFACCUM_RXRI or
      opc = ABSDIFFACCUM_RXRF or opc = ABSDIFFACCUM_RXRP or opc = ABSDIFFACCUM_RXMR or
      opc = ABSDIFFACCUM_RXMM or opc = ABSDIFFACCUM_RXMI or opc = ABSDIFFACCUM_RXMF or
      opc = ABSDIFFACCUM_RXMP or opc = ABSDIFFACCUM_RXIR or opc = ABSDIFFACCUM_RXIM or
      opc = ABSDIFFACCUM_RXIF or opc = ABSDIFFACCUM_RXIP or opc = ABSDIFFACCUM_RXFR or
      opc = ABSDIFFACCUM_RXFM or opc = ABSDIFFACCUM_RXFI or opc = ABSDIFFACCUM_RXFF or
      opc = ABSDIFFACCUM_RXFP or opc = ABSDIFFACCUM_RXPR or opc = ABSDIFFACCUM_RXPM or
      opc = ABSDIFFACCUM_RXPI or opc = ABSDIFFACCUM_RXPF or opc = ABSDIFFACCUM_RXPP or
      opc = ABSDIFFACCUM_MXRR or opc = ABSDIFFACCUM_MXRM or opc = ABSDIFFACCUM_MXRI or
      opc = ABSDIFFACCUM_MXRF or opc = ABSDIFFACCUM_MXRP or opc = ABSDIFFACCUM_MXMR or
      opc = ABSDIFFACCUM_MXMM or opc = ABSDIFFACCUM_MXMI or opc = ABSDIFFACCUM_MXMF or
      opc = ABSDIFFACCUM_MXMP or opc = ABSDIFFACCUM_MXIR or opc = ABSDIFFACCUM_MXIM or
      opc = ABSDIFFACCUM_MXIF or opc = ABSDIFFACCUM_MXIP or opc = ABSDIFFACCUM_MXFR or
      opc = ABSDIFFACCUM_MXFM or opc = ABSDIFFACCUM_MXFI or opc = ABSDIFFACCUM_MXFF or
      opc = ABSDIFFACCUM_MXFP or opc = ABSDIFFACCUM_MXPR or opc = ABSDIFFACCUM_MXPM or
      opc = ABSDIFFACCUM_MXPI or opc = ABSDIFFACCUM_MXPF or opc = ABSDIFFACCUM_MXPP or
      opc = ABSDIFFACCUM_FXRR or opc = ABSDIFFACCUM_FXRM or opc = ABSDIFFACCUM_FXRI or
      opc = ABSDIFFACCUM_FXRF or opc = ABSDIFFACCUM_FXRP or opc = ABSDIFFACCUM_FXMR or
      opc = ABSDIFFACCUM_FXMM or opc = ABSDIFFACCUM_FXMI or opc = ABSDIFFACCUM_FXMF or
      opc = ABSDIFFACCUM_FXMP or opc = ABSDIFFACCUM_FXIR or opc = ABSDIFFACCUM_FXIM or
      opc = ABSDIFFACCUM_FXIF or opc = ABSDIFFACCUM_FXIP or opc = ABSDIFFACCUM_FXFR or
      opc = ABSDIFFACCUM_FXFM or opc = ABSDIFFACCUM_FXFI or opc = ABSDIFFACCUM_FXFF or
      opc = ABSDIFFACCUM_FXFP or opc = ABSDIFFACCUM_FXPR or opc = ABSDIFFACCUM_FXPM or
      opc = ABSDIFFACCUM_FXPI or opc = ABSDIFFACCUM_FXPF or opc = ABSDIFFACCUM_FXPP or
      opc = ABSDIFFACCUM_XXRR or opc = ABSDIFFACCUM_XXRM or opc = ABSDIFFACCUM_XXRI or
      opc = ABSDIFFACCUM_XXRF or opc = ABSDIFFACCUM_XXRP or opc = ABSDIFFACCUM_XXMR or
      opc = ABSDIFFACCUM_XXMM or opc = ABSDIFFACCUM_XXMI or opc = ABSDIFFACCUM_XXMF or
      opc = ABSDIFFACCUM_XXMP or opc = ABSDIFFACCUM_XXIR or opc = ABSDIFFACCUM_XXIM or
      opc = ABSDIFFACCUM_XXIF or opc = ABSDIFFACCUM_XXIP or opc = ABSDIFFACCUM_XXFR or
      opc = ABSDIFFACCUM_XXFM or opc = ABSDIFFACCUM_XXFI or opc = ABSDIFFACCUM_XXFF or
      opc = ABSDIFFACCUM_XXFP or opc = ABSDIFFACCUM_XXPR or opc = ABSDIFFACCUM_XXPM or
      opc = ABSDIFFACCUM_XXPI or opc = ABSDIFFACCUM_XXPF or opc = ABSDIFFACCUM_XXPP
    else '0';
  end generate;
end structure;
