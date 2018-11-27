--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

library work;
use work.sFPE_typedef.all;

package sFPE_pkg is
  component sFPE is
    generic(
      DATA_WIDTH           : integer:= 16;  -- Data element width, e.g. real (and image) data width
      DATA_TYPE            : integer:= 1;
      SLICE_NUM            : integer:= 1;
      CORE_DATA_WIDTH      : integer:= 16; -- CPU data width, e.g. real (or real+image) width
      OPM_NUM              : integer:= 1;
      ALUM_NUM             : integer:= 1;
      FRAC_BITS            : integer:= 0;
      BSLAVE               : boolean:= false;
      BMASTER              : boolean:= false;
      BMASTER_NUM          : integer:= 1;
      VLEN                 : integer:= 1;

      OPCODE_WIDTH         : integer:= 6;

      -- Control Pipeline
      MULREG_EN            : boolean:= true;
      PB0_DEPTH            : integer:= 1;
      PB1_DEPTH            : integer:= 1;
      PB2_DEPTH            : integer:= 2;
      PA0_DEPTH            : integer:= 1;
      PA1_DEPTH            : integer:= 1;
      PA1X_DEPTH           : integer:= 0;

      -- Control Branch
      BRANCH_EN            : boolean:= false;
      JMP_EN               : boolean:= true;

      RPT_EN               : boolean:= false;
      RPT_SPEC_1           : boolean:= false;
      RPT_LEVELS           : integer:= 4;
      RPT_CNT_LEN0         : integer:= 5;
      RPT_CNT_LEN1         : integer:= 5;
      RPT_CNT_LEN2         : integer:= 5;
      RPT_CNT_LEN3         : integer:= 5;
      RPT_CNT_LEN4         : integer:= 1;
      RPT_BLK_LEN0         : integer:= 5;
      RPT_BLK_LEN1         : integer:= 5;
      RPT_BLK_LEN2         : integer:= 5;
      RPT_BLK_LEN3         : integer:= 5;
      RPT_BLK_LEN4         : integer:= 1;

      -- Control Supported Instructions
      MASK_EN              : boolean:= false;
      MASKEQ_EN            : boolean:= false;
      MASKGT_EN            : boolean:= false;
      MASKLT_EN            : boolean:= false;
      MASKGE_EN            : boolean:= false;
      MASKLE_EN            : boolean:= false;
      MASKNE_EN            : boolean:= false;
      ALUSRA_EN            : boolean:= false;
      ALUSRA_VAL           : integer:= 1;
      ABSDIFF_EN           : boolean:= false;
      ABSDIFF_WITHACCUM    : boolean:= true;

      -- Control Flexible Ports
      FLEXA_TYPE           : integer:= 1;
      FLEXB_TYPE           : integer:= 1;
      FLEXC_TYPE           : integer:= 1;

      -- Special Case
      FLEXB_IMM_VAL        : integer:= -1;
      DIRECT_WB_EN         : boolean:= false;
      SHARE_GET_DATA       : boolean:= false;

      -- Control Extensible Bits
      EBITS_A              : integer:= 0;
      EBITS_B              : integer:= 0;
      EBITS_C              : integer:= 0;
      EBITS_D              : integer:= 0;

      DSP48E_EN            : boolean:= true;

      -- Control FIFO
      GETI_EN              : boolean:= false;
      GETCH_EN             : boolean:= false;
      PUTCH_EN             : boolean:= false;
      RX_CH_NUM            : integer:= 4;
      RX_CH_WIDTH          : integer:= 2;
      TX_CH_NUM            : integer:= 4;
      TX_CH_WIDTH          : integer:= 2;

      -- Control memory
      RF_EN                : boolean:= true;
      RF_ADDR_WIDTH        : integer:= 5;
      RF_INIT_EN           : boolean:= false;
      RF_INIT_FILE         : string := "init0.mif";

      PM_SIZE              : integer:= 32;
      PM_ADDR_WIDTH        : integer:= 5;
      PM_DATA_WIDTH        : integer:= 32;
      USE_BRAM_FOR_LARGE_PM: boolean:= true;
      PM_INIT_FILE         : string := "init0.mif";

      DM_EN                : boolean:= false;
      DM_SIZE              : integer:= 32;
      DM_ADDR_WIDTH        : integer:= 5;
      DM_DATA_WIDTH        : integer:= 16;
      DM_INIT_EN           : boolean:= false;
      USE_BRAM_FOR_LARGE_DM: boolean:= true;
      DM_INIT_FILE         : string := "init0.mif";
      DM_RB_M_NUM          : integer:= 2;
      DM_RB_N_NUM          : integer:= 2;
      DM_WB_NUM            : integer:= 2;
      DM_TRUE_2R1W         : boolean:= true;
      DM_RB_M_INITIAL0     : integer:= 0;
      DM_RB_M_INITIAL1     : integer:= 0;
      DM_RB_N_INITIAL0     : integer:= 0;
      DM_RB_N_INITIAL1     : integer:= 0;
      DM_WB_INITIAL0       : integer:= 0;
      DM_WB_INITIAL1       : integer:= 0;
      DM_RB_M_AUTOINC_SIZE0: integer:= 1;
      DM_RB_M_AUTOINC_SIZE1: integer:= 1;
      DM_RB_N_AUTOINC_SIZE0: integer:= 1;
      DM_RB_N_AUTOINC_SIZE1: integer:= 1;
      DM_WB_AUTOINC_SIZE0  : integer:= 1;
      DM_WB_AUTOINC_SIZE1  : integer:= 1;
      DM_OFFSET_EN         : boolean:= false;
      DM_RB_M_SET_EN0      : boolean:= false;
      DM_RB_M_SET_EN1      : boolean:= false;
      DM_RB_N_SET_EN0      : boolean:= false;
      DM_RB_N_SET_EN1      : boolean:= false;
      DM_WB_SET_EN0        : boolean:= false;
      DM_WB_SET_EN1        : boolean:= false;
      DM_RB_M_AUTOINC_EN0  : boolean:= false;
      DM_RB_M_AUTOINC_EN1  : boolean:= false;
      DM_RB_N_AUTOINC_EN0  : boolean:= false;
      DM_RB_N_AUTOINC_EN1  : boolean:= false;
      DM_WB_AUTOINC_EN0    : boolean:= false;
      DM_WB_AUTOINC_EN1    : boolean:= false;
      DM_RB_M_INC_EN0      : boolean:= false;
      DM_RB_M_INC_EN1      : boolean:= false;
      DM_RB_N_INC_EN0      : boolean:= false;
      DM_RB_N_INC_EN1      : boolean:= false;
      DM_WB_INC_EN0        : boolean:= false;
      DM_WB_INC_EN1        : boolean:= false;

      SM_EN                : boolean:= false;
      SM_SIZE              : integer:= 32;
      SM_ADDR_WIDTH        : integer:= 5;
      USE_BRAM_FOR_LARGE_SM: boolean:= true;
      SM_INIT_FILE         : string := "IMMInit/imm_init0.mif";
      SM_OFFSET_EN         : boolean:= false;
      SM_READONLY          : boolean:= true;
      SM_RB_SET_EN0        : boolean:= false;
      SM_WB_SET_EN0        : boolean:= false;
      SM_RB_AUTOINC_SIZE0  : integer:= 1;
      SM_WB_AUTOINC_SIZE0  : integer:= 1;
      SM_RB_AUTOINC_EN0    : boolean:= false;
      SM_WB_AUTOINC_EN0    : boolean:= false;
      SM_RB_INC_EN0        : boolean:= false;
      SM_WB_INC_EN0        : boolean:= false
    );
    port(
      clk     : in std_logic;
      rst     : in std_logic;

      -- Control
      i_ext_en_sFPE   : in  std_logic  := '1';
      o_ext_barrier  : out std_logic_vector(BMASTER_NUM-1 downto 0);
      i_ext_barrier  : in  std_logic := '0';
      o_ext_en_sFPE   : out std_logic := '1';

      -- Communication port signals
      i_get_ch_data  :  in VDATA_TYPE(RX_CH_NUM*VLEN-1 downto 0);
      i_get_ch_empty :  in VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0) := (others=>'0');  -- vector channel empty
      o_get_ch_read  :  out VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0);    -- vector channel read

      -- Output channel
      o_put_ch_data  :  out VDATA_TYPE(TX_CH_NUM*VLEN-1 downto 0);
      i_put_ch_full  :  in VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0):= (others=>'0');
      o_put_ch_write  : out VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0)
    );
  end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in definations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library unisim;
use unisim.vcomponents.all;

library work;
use work.generic_multiplexers.all;
use work.generic_registers.all;

use work.sFPE_typedef.all;
use work.sFPE_PM_pkg.all;
use work.sFPE_DM_pkg.all;
use work.sFPE_SM_pkg.all;
use work.sFPE_RF_pkg.all;

use work.sFPE_ID_pkg.all;
use work.sFPE_PC_pkg.all;
use work.sFPE_branch_pkg.all;

use work.sFPE_comm_get_pkg.all;
use work.sFPE_comm_put_pkg.all;

use work.sFPE_wrtie_back_pkg.all;
use work.sFPE_SAU_pkg.all;
use work.sFPE_EX_pkg.all;

entity sFPE is
  generic(
    DATA_WIDTH           : integer:= 16;  -- Data element width, e.g. real (and image) data width
    DATA_TYPE            : integer:= 1;
    SLICE_NUM            : integer:= 1;
    CORE_DATA_WIDTH      : integer:= 16; -- CPU data width, e.g. real (or real+image) width
    OPM_NUM              : integer:= 1;
    ALUM_NUM             : integer:= 1;
    FRAC_BITS            : integer:= 0;
    BSLAVE               : boolean:= false;
    BMASTER              : boolean:= false;
    BMASTER_NUM          : integer:= 1;
    VLEN                 : integer:= 1;

    OPCODE_WIDTH         : integer:= 6;

    -- Control Pipeline
    MULREG_EN            : boolean:= true;
    PB0_DEPTH            : integer:= 1;
    PB1_DEPTH            : integer:= 1;
    PB2_DEPTH            : integer:= 2;
    PA0_DEPTH            : integer:= 1;
    PA1_DEPTH            : integer:= 1;
    PA1X_DEPTH           : integer:= 0;

    -- Control Branch
    BRANCH_EN            : boolean:= false;
    JMP_EN               : boolean:= true;

    RPT_EN               : boolean:= false;
    RPT_SPEC_1           : boolean:= false;
    RPT_LEVELS           : integer:= 4;
    RPT_CNT_LEN0         : integer:= 5;
    RPT_CNT_LEN1         : integer:= 5;
    RPT_CNT_LEN2         : integer:= 5;
    RPT_CNT_LEN3         : integer:= 5;
    RPT_CNT_LEN4         : integer:= 1;
    RPT_BLK_LEN0         : integer:= 5;
    RPT_BLK_LEN1         : integer:= 5;
    RPT_BLK_LEN2         : integer:= 5;
    RPT_BLK_LEN3         : integer:= 5;
    RPT_BLK_LEN4         : integer:= 1;

    -- Control Supported Instructions
    MASK_EN              : boolean:= false;
    MASKEQ_EN            : boolean:= false;
    MASKGT_EN            : boolean:= false;
    MASKLT_EN            : boolean:= false;
    MASKGE_EN            : boolean:= false;
    MASKLE_EN            : boolean:= false;
    MASKNE_EN            : boolean:= false;
    ALUSRA_EN            : boolean:= false;
    ALUSRA_VAL           : integer:= 1;
    ABSDIFF_EN           : boolean:= false;
    ABSDIFF_WITHACCUM    : boolean:= true;

    -- Control Flexible Ports
    FLEXA_TYPE           : integer:= 1;
    FLEXB_TYPE           : integer:= 1;
    FLEXC_TYPE           : integer:= 1;

    -- Special Case
    FLEXB_IMM_VAL        : integer:= -1;
    DIRECT_WB_EN         : boolean:= false;
    SHARE_GET_DATA       : boolean:= false;

    -- Control Extensible Bits
    EBITS_A              : integer:= 0;
    EBITS_B              : integer:= 0;
    EBITS_C              : integer:= 0;
    EBITS_D              : integer:= 0;

    DSP48E_EN            : boolean:= true;

    -- Control FIFO
    GETI_EN              : boolean:= false;
    GETCH_EN             : boolean:= false;
    PUTCH_EN             : boolean:= false;
    RX_CH_NUM            : integer:= 4;
    RX_CH_WIDTH          : integer:= 2;
    TX_CH_NUM            : integer:= 4;
    TX_CH_WIDTH          : integer:= 2;

    -- Control memory
    RF_EN                : boolean:= true;
    RF_ADDR_WIDTH        : integer:= 5;
    RF_INIT_EN           : boolean:= false;
    RF_INIT_FILE         : string := "init0.mif";

    PM_SIZE              : integer:= 32;
    PM_ADDR_WIDTH        : integer:= 5;
    PM_DATA_WIDTH        : integer:= 32;
    USE_BRAM_FOR_LARGE_PM: boolean:= true;
    PM_INIT_FILE         : string := "init0.mif";

    DM_EN                : boolean:= false;
    DM_SIZE              : integer:= 32;
    DM_ADDR_WIDTH        : integer:= 5;
    DM_DATA_WIDTH        : integer:= 16;
    DM_INIT_EN           : boolean:= false;
    USE_BRAM_FOR_LARGE_DM: boolean:= true;
    DM_INIT_FILE         : string := "init0.mif";
    DM_RB_M_NUM          : integer:= 2;
    DM_RB_N_NUM          : integer:= 2;
    DM_WB_NUM            : integer:= 2;
    DM_TRUE_2R1W         : boolean:= true;
    DM_RB_M_INITIAL0     : integer:= 0;
    DM_RB_M_INITIAL1     : integer:= 0;
    DM_RB_N_INITIAL0     : integer:= 0;
    DM_RB_N_INITIAL1     : integer:= 0;
    DM_WB_INITIAL0       : integer:= 0;
    DM_WB_INITIAL1       : integer:= 0;
    DM_RB_M_AUTOINC_SIZE0: integer:= 1;
    DM_RB_M_AUTOINC_SIZE1: integer:= 1;
    DM_RB_N_AUTOINC_SIZE0: integer:= 1;
    DM_RB_N_AUTOINC_SIZE1: integer:= 1;
    DM_WB_AUTOINC_SIZE0  : integer:= 1;
    DM_WB_AUTOINC_SIZE1  : integer:= 1;
    DM_OFFSET_EN         : boolean:= false;
    DM_RB_M_SET_EN0      : boolean:= false;
    DM_RB_M_SET_EN1      : boolean:= false;
    DM_RB_N_SET_EN0      : boolean:= false;
    DM_RB_N_SET_EN1      : boolean:= false;
    DM_WB_SET_EN0        : boolean:= false;
    DM_WB_SET_EN1        : boolean:= false;
    DM_RB_M_AUTOINC_EN0  : boolean:= false;
    DM_RB_M_AUTOINC_EN1  : boolean:= false;
    DM_RB_N_AUTOINC_EN0  : boolean:= false;
    DM_RB_N_AUTOINC_EN1  : boolean:= false;
    DM_WB_AUTOINC_EN0    : boolean:= false;
    DM_WB_AUTOINC_EN1    : boolean:= false;
    DM_RB_M_INC_EN0      : boolean:= false;
    DM_RB_M_INC_EN1      : boolean:= false;
    DM_RB_N_INC_EN0      : boolean:= false;
    DM_RB_N_INC_EN1      : boolean:= false;
    DM_WB_INC_EN0        : boolean:= false;
    DM_WB_INC_EN1        : boolean:= false;

    SM_EN                : boolean:= false;
    SM_SIZE              : integer:= 32;
    SM_ADDR_WIDTH        : integer:= 5;
    USE_BRAM_FOR_LARGE_SM: boolean:= true;
    SM_INIT_FILE         : string := "IMMInit/imm_init0.mif";
    SM_OFFSET_EN         : boolean:= false;
    SM_READONLY          : boolean:= true;
    SM_RB_SET_EN0        : boolean:= false;
    SM_WB_SET_EN0        : boolean:= false;
    SM_RB_AUTOINC_SIZE0  : integer:= 1;
    SM_WB_AUTOINC_SIZE0  : integer:= 1;
    SM_RB_AUTOINC_EN0    : boolean:= false;
    SM_WB_AUTOINC_EN0    : boolean:= false;
    SM_RB_INC_EN0        : boolean:= false;
    SM_WB_INC_EN0        : boolean:= false
  );
  port(
    clk     : in std_logic;
    rst     : in std_logic;

    -- Control
    i_ext_en_sFPE   : in  std_logic := '1';
    o_ext_en_sFPE   : out std_logic := '1';
    i_ext_barrier  : in  std_logic := '0';
    o_ext_barrier  : out std_logic_vector(BMASTER_NUM-1 downto 0);

    -- Communication port signals
    i_get_ch_data  :  in VDATA_TYPE(RX_CH_NUM*VLEN-1 downto 0);
    i_get_ch_empty :  in VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0) := (others=>'0');  -- vector channel empty
    o_get_ch_read  :  out VSIG_TYPE(RX_CH_NUM*VLEN-1 downto 0);    -- vector channel read

    -- Output channel
    o_put_ch_data  :  out VDATA_TYPE(TX_CH_NUM*VLEN-1 downto 0);
    i_put_ch_full  :  in VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0):= (others=>'0');
    o_put_ch_write  : out VSIG_TYPE(TX_CH_NUM*VLEN-1 downto 0)
  );
end entity;

architecture structure of sFPE is

  -- Help functions
  function setPax return integer is
    variable lev : integer := 0;
  begin
    if (DATA_WIDTH = 32 and DATA_TYPE = 1 and SLICE_NUM = 4) then
      return 3;
    else
      if (DATA_WIDTH = 16 and DATA_TYPE = 2 and SLICE_NUM = 4) then
        lev := 1;
      end if;
      if MULREG_EN = true then
        return lev + 1;
      else
        return lev;
      end if;
    end if;
  end function setPax;

  function setInputwidth return integer is
    variable res : integer := 0;
  begin
    if (DM_EN = true) then
      return DM_DATA_WIDTH;
    else
      return CORE_DATA_WIDTH;
    end if;
  end function setInputwidth;

  function hasTwoDMRdPorts return boolean is
  begin
    if (((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) = 1) or
       (((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1 and ((FLEXC_TYPE/2)rem 2) = 1) or
       (((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) /= 1 and ((FLEXC_TYPE/2)rem 2) = 1) then
      return true;
    else
      return false;
    end if;
  end function hasTwoDMRdPorts;

  function hasTwoFIFORdPorts return boolean is
  begin
    if ((((FLEXA_TYPE/8)rem 2) = 1 and ((FLEXB_TYPE/8)rem 2) = 1) or
       (((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) = 1 and ((FLEXC_TYPE/8)rem 2) = 1) or
       (((FLEXA_TYPE/8)rem 2) = 1 and ((FLEXB_TYPE/8)rem 2) /= 1 and ((FLEXC_TYPE/8)rem 2) = 1)) and (SHARE_GET_DATA = false) then
      return true;
    else
      return false;
    end if;
  end function hasTwoFIFORdPorts;

  function isBaseOffset return boolean is
  begin
    if (DM_EN = true) and (DM_RB_M_INC_EN0 = false) and (DM_RB_M_INC_EN1 = false) and (DM_RB_N_INC_EN0 = false) and (DM_RB_N_INC_EN1 = false) and
       (DM_RB_M_AUTOINC_EN0 = false) and (DM_RB_M_AUTOINC_EN1 = false) and (DM_RB_N_AUTOINC_EN0 = false) and (DM_RB_N_AUTOINC_EN1 = false) then
      return true;
    else
      return false;
    end if;
  end function isBaseOffset;

  function getDMOffsetWidth return integer is
    variable extbits : integer := 0;
  begin
    if (isBaseOffset = true) then
      if (((FLEXA_TYPE/2)rem 2)) = 1 then
        extbits := EBITS_A;
      elsif (((FLEXB_TYPE/2)rem 2)) = 1 then
        extbits := EBITS_B;
      elsif (((FLEXC_TYPE/2)rem 2)) = 1 then
        extbits := EBITS_C;
      end if;
      if (extbits+5 > DM_ADDR_WIDTH) then
        return DM_ADDR_WIDTH;
      else
        return extbits+5;
      end if;
    else
      return 3;
    end if;
  end function getDMOffsetWidth;

  function getSMOffsetWidth return integer is
    variable extbits : integer := 0;
  begin
    if (SM_EN = true) then
      if (((FLEXA_TYPE/4)rem 2)) = 1 then
        extbits := EBITS_A;
      elsif (((FLEXB_TYPE/4)rem 2)) = 1 then
        extbits := EBITS_B;
      elsif (((FLEXC_TYPE/4)rem 2)) = 1 then
        extbits := EBITS_C;
      end if;
      if (extbits+5 > SM_ADDR_WIDTH) then
        return SM_ADDR_WIDTH;
      else
        return extbits+5;
      end if;
    else
      return 5;
    end if;
  end function getSMOffsetWidth;

  -- Constants
  constant PaxLevel : integer := setPax;
  constant constInputWidth : integer := setInputwidth;
  constant constDMOffsetWidth : integer := getDMOffsetWidth;
  constant constSMOffsetWidth : integer := getSMOffsetWidth;

  type VPMOPERANDS_TYPE is array (natural range <>) of std_logic_vector(PM_DATA_WIDTH-OPCODE_WIDTH-1 downto 0);
  type VRFADDR_TYPE is array (natural range <>) of std_logic_vector(RF_ADDR_WIDTH-1 downto 0);
  type VDMOFS_TYPE is array (natural range <>) of std_logic_vector(constDMOffsetWidth-1 downto 0);
  type VDMADDR_TYPE is array (natural range <>) of std_logic_vector(DM_ADDR_WIDTH-1 downto 0);
  type VRXCHWIDTH_TYPE is array (natural range <>) of std_logic_vector(RX_CH_WIDTH-1 downto 0);
  type VTXCHWIDTH_TYPE is array (natural range <>) of std_logic_vector(TX_CH_WIDTH-1 downto 0);
  type VOPMODE_TYPE is array (natural range <>) of std_logic_vector(7*OPM_NUM-1 downto 0);
  type VALUMODE_TYPE is array (natural range <>) of std_logic_vector(4*ALUM_NUM-1 downto 0);
  type VCOREDATA_TYPE is array (natural range <>) of std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  type SELTYPE3 is array (natural range <>) of std_logic_vector(2 downto 0);
  type SELTYPE2 is array (natural range <>) of std_logic_vector(1 downto 0);

  -- These values should be in coincidence with CodeGen.
  -- Current instruction map |Inst|free|D|A|B|C|
  --                                    5 5 5 5

  signal pc_addr_Ps            : std_logic_vector(PM_ADDR_WIDTH-1 downto 0);
  signal branch_taken_Pa3      : std_logic;
  signal jmp_taken_Pb2         : std_logic;

  signal pm_do_Pb1             : std_logic_vector(PM_DATA_WIDTH-1 downto 0);
  signal pm_opcode_Pb1         : std_logic_vector(PM_DATA_WIDTH-1 downto PM_DATA_WIDTH-6);
  signal pm_operands_Pb1, pm_operands_Pb1x : std_logic_vector(PM_DATA_WIDTH-OPCODE_WIDTH-1 downto 0);
  signal pm_operands_Pb2       : VPMOPERANDS_TYPE(VLEN-1 downto 0);

  signal id_b_Pb1, id_b_Pb2    : std_logic;
  signal id_rpt_Pb1, id_rpt_Pb2: std_logic;
  signal cond_sign_Pa3         : VSIG_TYPE(VLEN-1 downto 0);
  signal cond_eq_Pa3           : VSIG_TYPE(VLEN-1 downto 0);
  signal id_beq_Pb1, id_beq_Pb2, id_beq_Pax, id_beq_Pa0, id_beq_Pa1, id_beq_Pa1x, id_beq_Pa2 : std_logic;
  signal id_bgt_Pb1, id_bgt_Pb2, id_bgt_Pax, id_bgt_Pa0, id_bgt_Pa1, id_bgt_Pa1x, id_bgt_Pa2 : std_logic;
  signal id_blt_Pb1, id_blt_Pb2, id_blt_Pax, id_blt_Pa0, id_blt_Pa1, id_blt_Pa1x, id_blt_Pa2 : std_logic;
  signal id_bge_Pb1, id_bge_Pb2, id_bge_Pax, id_bge_Pa0, id_bge_Pa1, id_bge_Pa1x, id_bge_Pa2 : std_logic;
  signal id_ble_Pb1, id_ble_Pb2, id_ble_Pax, id_ble_Pa0, id_ble_Pa1, id_ble_Pa1x, id_ble_Pa2 : std_logic;
  signal id_bne_Pb1, id_bne_Pb2, id_bne_Pax, id_bne_Pa0, id_bne_Pa1, id_bne_Pa1x, id_bne_Pa2 : std_logic;
  signal branch_addr_Pb2, branch_addr_Pax, branch_addr_Pa0, branch_addr_Pa1, branch_addr_Pa1x, branch_addr_Pa2 : std_logic_vector(PM_ADDR_WIDTH-1 downto 0);

  signal id_en_pc_Pb1          : std_logic;
  signal id_ext_barrier_Pb1, id_ext_barrier_Pb2 : std_logic_vector(BMASTER_NUM-1 downto 0);
  signal id_ext_en_sFPE_Pb1, id_ext_en_sFPE_Pb2   : std_logic;

  signal id_rddm0_Pb1, id_rddm0_Pb2, id_rddm0_Pa0 : std_logic;
  signal id_rddm0_Pa1 : std_logic_vector(VLEN-1 downto 0);
  signal id_rddm1_Pb1, id_rddm1_Pb2, id_rddm1_Pa0 : std_logic;
  signal id_rddm1_Pa1 : std_logic_vector(VLEN-1 downto 0);
  signal id_dm_set_rb_m0_Pb1, id_dm_set_rb_m0_Pb2 : std_logic;
  signal id_dm_set_rb_m1_Pb1, id_dm_set_rb_m1_Pb2 : std_logic;
  signal id_dm_set_rb_n0_Pb1, id_dm_set_rb_n0_Pb2 : std_logic;
  signal id_dm_set_rb_n1_Pb1, id_dm_set_rb_n1_Pb2 : std_logic;
  signal id_dm_inc_rb_m0_Pb1, id_dm_inc_rb_m0_Pb2 : std_logic;
  signal id_dm_inc_rb_m1_Pb1, id_dm_inc_rb_m1_Pb2 : std_logic;
  signal id_dm_inc_rb_n0_Pb1, id_dm_inc_rb_n0_Pb2 : std_logic;
  signal id_dm_inc_rb_n1_Pb1, id_dm_inc_rb_n1_Pb2 : std_logic;
  signal id_dm_autoinc_rb_m_Pb1, id_dm_autoinc_rb_m_Pb2: std_logic;
  signal id_dm_autoinc_rb_n_Pb1, id_dm_autoinc_rb_n_Pb2: std_logic;
  signal dm_rb_sel_m_Pb2       : std_logic;
  signal dm_rb_sel_n_Pb2       : std_logic;
  signal dm_wofs_addr_Pb2, dm_wofs_addr_Pax, dm_wofs_addr_Pa0, dm_wofs_addr_Pa1, dm_wofs_addr_Pa1x, dm_wofs_addr_Pa2 : std_logic_vector(constDMOffsetWidth-1 downto 0);
  signal dm_wb_addr_Pb2, dm_wb_addr_Pax, dm_wb_addr_Pa0, dm_wb_addr_Pa1, dm_wb_addr_Pa1x, dm_wb_addr_Pa2 : std_logic_vector(DM_ADDR_WIDTH-1 downto 0);
  signal id_wrdm_Pb1, id_wrdm_Pb2, id_wrdm_Pax, id_wrdm_Pa0, id_wrdm_Pa1, id_wrdm_Pa1x, id_wrdm_Pa2 : std_logic;
  signal id_wrdm_Pa3            : std_logic_vector(VLEN-1 downto 0);
  signal dm_wen_dmin            : std_logic_vector(VLEN-1 downto 0);
  signal dm_wb_sel_Pb2, dm_wb_sel_Pax, dm_wb_sel_Pa0, dm_wb_sel_Pa1, dm_wb_sel_Pa1x, dm_wb_sel_Pa2 : std_logic;
  signal id_dm_set_wb_0_Pb1, id_dm_set_wb_0_Pb2, id_dm_set_wb_0_Pax, id_dm_set_wb_0_Pa0, id_dm_set_wb_0_Pa1, id_dm_set_wb_0_Pa1x, id_dm_set_wb_0_Pa2 : std_logic;
  signal id_dm_set_wb_1_Pb1, id_dm_set_wb_1_Pb2, id_dm_set_wb_1_Pax, id_dm_set_wb_1_Pa0, id_dm_set_wb_1_Pa1, id_dm_set_wb_1_Pa1x, id_dm_set_wb_1_Pa2 : std_logic;
  signal id_dm_inc_wb_0_Pb1, id_dm_inc_wb_0_Pb2, id_dm_inc_wb_0_Pax, id_dm_inc_wb_0_Pa0, id_dm_inc_wb_0_Pa1, id_dm_inc_wb_0_Pa1x, id_dm_inc_wb_0_Pa2 : std_logic;
  signal id_dm_inc_wb_1_Pb1, id_dm_inc_wb_1_Pb2, id_dm_inc_wb_1_Pax, id_dm_inc_wb_1_Pa0, id_dm_inc_wb_1_Pa1, id_dm_inc_wb_1_Pa1x, id_dm_inc_wb_1_Pa2 : std_logic;
  signal id_dm_autoinc_wb_Pb1, id_dm_autoinc_wb_Pb2, id_dm_autoinc_wb_Pax, id_dm_autoinc_wb_Pa0, id_dm_autoinc_wb_Pa1, id_dm_autoinc_wb_Pa1x, id_dm_autoinc_wb_Pa2 : std_logic;
  signal dm_rdaddr_0           :  std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
  signal dm_rdaddr_1           :  std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
  signal dm_do0_Pa1            : VCOREDATA_TYPE(VLEN-1 downto 0):= (others=>(others=>'0'));
  signal dm_do1_Pa1            : VCOREDATA_TYPE(VLEN-1 downto 0):= (others=>(others=>'0'));
  signal dm_wraddr_Pa2 :  std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
  signal dm_wraddr_Pa3 :  VDMADDR_TYPE(VLEN-1 downto 0);
  signal dm_rofs_addr0_Pb2     : std_logic_vector(constDMOffsetWidth-1 downto 0);
  signal dm_rofs_addr1_Pb2     : std_logic_vector(constDMOffsetWidth-1 downto 0);
  signal dm_rb_addr_Pb2        : std_logic_vector(DM_ADDR_WIDTH-1 downto 0);

  signal id_rdsm_Pb1, id_rdsm_Pb2, id_rdsm_Pa0: std_logic;
  signal id_rdsm_Pa1 : std_logic_vector(VLEN-1 downto 0);
  signal id_sm_inc_rb_0_Pb1, id_sm_inc_rb_0_Pb2 : std_logic;
  signal id_sm_inc_wb_0_Pb1, id_sm_inc_wb_0_Pb2, id_sm_inc_wb_0_Pax, id_sm_inc_wb_0_Pa0, id_sm_inc_wb_0_Pa1, id_sm_inc_wb_0_Pa1x, id_sm_inc_wb_0_Pa2, id_sm_inc_wb_0_Pa3 : std_logic;
  signal id_sm_autoinc_rb_Pb1, id_sm_autoinc_rb_Pb2, id_sm_autoinc_wb_Pb1, id_sm_autoinc_wb_Pb2, id_sm_autoinc_wb_Pax, id_sm_autoinc_wb_Pa0, id_sm_autoinc_wb_Pa1, id_sm_autoinc_wb_Pa1x, id_sm_autoinc_wb_Pa2, id_sm_autoinc_wb_Pa3 : std_logic;
  signal id_sm_wen_Pb1, id_sm_wen_Pb2, id_sm_wen_Pax, id_sm_wen_Pa0, id_sm_wen_Pa1, id_sm_wen_Pa1x, id_sm_wen_Pa2, id_sm_wen_Pa3 : std_logic;
  signal id_sm_set_rb_0_Pb1, id_sm_set_rb_0_Pb2 : std_logic;
  signal id_sm_set_wb_0_Pb1, id_sm_set_wb_0_Pb2, id_sm_set_wb_0_Pax, id_sm_set_wb_0_Pa0, id_sm_set_wb_0_Pa1, id_sm_set_wb_0_Pa1x, id_sm_set_wb_0_Pa2, id_sm_set_wb_0_Pa3 : std_logic;
  signal sm_do_Pa1             : std_logic_vector (CORE_DATA_WIDTH-1 downto 0);
  signal sm_rb_addr_Pb2        : std_logic_vector(SM_ADDR_WIDTH-1 downto 0);
  signal sm_rofs_addr_Pb2      : std_logic_vector(constSMOffsetWidth-1 downto 0);
  signal sm_wb_addr_Pb2, sm_wb_addr_Pax, sm_wb_addr_Pa0, sm_wb_addr_Pa1, sm_wb_addr_Pa1x, sm_wb_addr_Pa2, sm_wb_addr_Pa3 : std_logic_vector(SM_ADDR_WIDTH-1 downto 0);

  signal rdaddr_a_Pb2          : VRFADDR_TYPE(VLEN-1 downto 0);
  signal rdaddr_b_Pb2          : VRFADDR_TYPE(VLEN-1 downto 0);
  signal rdaddr_c_Pb2          : VRFADDR_TYPE(VLEN-1 downto 0);
  signal src_a_Pa1, src_a_Pa1x : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal src_b_Pa1, src_b_Pa1x : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal src_c_Pa1, src_c_Pa1x : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal rf_wraddr_Pb2, rf_wraddr_Pax, rf_wraddr_Pa0, rf_wraddr_Pa1, rf_wraddr_Pa1x, rf_wraddr_Pa2 : std_logic_vector(RF_ADDR_WIDTH-1 downto 0);
  signal rf_wraddr_Pa3 : VRFADDR_TYPE(VLEN-1 downto 0);
  signal id_rf_wen_Pb1, id_rf_wen_Pb2, id_rf_wen_Pax, id_rf_wen_Pa0, id_rf_wen_Pa1, id_rf_wen_Pa1x, id_rf_wen_Pa2 : std_logic;
  signal id_rf_wen_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal rf_wen_rfin : std_logic_vector(VLEN-1 downto 0);

  signal src_a_muxout_Pa1      : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal src_b_muxout_Pa1      : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal src_c_muxout_Pa1      : VCOREDATA_TYPE(VLEN-1 downto 0);

  signal dsp48_result_Pa3      : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal dsp48sra_result_Pa3   : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal ex_result_Pa3         : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal absdiff_out_Pa3       : VCOREDATA_TYPE(VLEN-1 downto 0);

  signal id_get_inst0_Pb1 : std_logic;
  signal id_get_inst0_Pb2, id_get_inst0_Pb2_masked: std_logic_vector(VLEN-1 downto 0);
  signal id_get_inst1_Pb1 : std_logic;
  signal id_get_inst1_Pb2 : std_logic_vector(VLEN-1 downto 0);
  signal get_ch_sel0_Pb2  : VRXCHWIDTH_TYPE(VLEN-1 downto 0);
  signal id_rx_autoinc_Pb1, id_rx_autoinc_Pb2 : std_logic := '0';
  signal id_rx_reset_Pb1, id_rx_reset_Pb2 : std_logic := '0';
  signal id_get_or_peak0_Pb1, id_get_or_peak0_Pb2, id_get_or_peak0_Pa0: std_logic;
  signal id_get_or_peak0_Pa1 : std_logic_vector(VLEN-1 downto 0);
  signal id_get_or_peak1_Pb1, id_get_or_peak1_Pb2, id_get_or_peak1_Pa0: std_logic;
  signal id_get_or_peak1_Pa1, id_get_or_peak0_or_1_Pa1 : std_logic_vector(VLEN-1 downto 0);
  signal get_data0_Pa1 : VCOREDATA_TYPE(VLEN-1 downto 0):= (others=>(others=>'0'));
  signal get_data1_Pa1, get_data0_or_1_Pa1 : VCOREDATA_TYPE(VLEN-1 downto 0):= (others=>(others=>'0'));

  signal id_put_inst_Pb1, id_put_inst_Pb2, id_put_inst_Pax, id_put_inst_Pa0, id_put_inst_Pa1, id_put_inst_Pa1x : std_logic;
  signal id_put_inst_Pa2 : std_logic_vector(VLEN-1 downto 0);
  signal put_ch_sel_Pb2, put_ch_sel_Pax, put_ch_sel_Pa0, put_ch_sel_Pa1 : std_logic_vector(TX_CH_WIDTH-1 downto 0);
  signal put_ch_sel_Pa2 : VTXCHWIDTH_TYPE(VLEN-1 downto 0);
  signal id_tx_autoinc_Pb1, id_tx_autoinc_Pb2, id_tx_autoinc_Pax, id_tx_autoinc_Pa0, id_tx_autoinc_Pa1 : std_logic := '0';
  signal id_tx_autoinc_Pa2 : std_logic_vector(VLEN-1 downto 0);
  signal id_tx_reset_Pb1, id_tx_reset_Pb2, id_tx_reset_Pax, id_tx_reset_Pa0, id_tx_reset_Pa1 : std_logic := '0';
  signal id_tx_reset_Pa2 : std_logic_vector(VLEN-1 downto 0);
  signal put_data_Pa3 : VCOREDATA_TYPE(VLEN-1 downto 0):= (others=>(others=>'0'));

  signal mask_bit_Pb2, mask_bit_Pax, mask_bit_Pa0, mask_bit_Pa1, mask_bit_Pa1x, mask_bit_Pa2 : std_logic;
  signal mask_bit_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmaskeq_Pb1, id_setmaskeq_Pb2, id_setmaskeq_Pax, id_setmaskeq_Pa0, id_setmaskeq_Pa1, id_setmaskeq_Pa1x, id_setmaskeq_Pa2 : std_logic;
  signal id_setmaskeq_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmaskgt_Pb1, id_setmaskgt_Pb2, id_setmaskgt_Pax, id_setmaskgt_Pa0, id_setmaskgt_Pa1, id_setmaskgt_Pa1x, id_setmaskgt_Pa2 : std_logic;
  signal id_setmaskgt_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmasklt_Pb1, id_setmasklt_Pb2, id_setmasklt_Pax, id_setmasklt_Pa0, id_setmasklt_Pa1, id_setmasklt_Pa1x, id_setmasklt_Pa2 : std_logic;
  signal id_setmasklt_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmaskge_Pb1, id_setmaskge_Pb2, id_setmaskge_Pax, id_setmaskge_Pa0, id_setmaskge_Pa1, id_setmaskge_Pa1x, id_setmaskge_Pa2 : std_logic;
  signal id_setmaskge_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmaskle_Pb1, id_setmaskle_Pb2, id_setmaskle_Pax, id_setmaskle_Pa0, id_setmaskle_Pa1, id_setmaskle_Pa1x, id_setmaskle_Pa2 : std_logic;
  signal id_setmaskle_Pa3 : std_logic_vector(VLEN-1 downto 0);
  signal id_setmaskne_Pb1, id_setmaskne_Pb2, id_setmaskne_Pax, id_setmaskne_Pa0, id_setmaskne_Pa1, id_setmaskne_Pa1x, id_setmaskne_Pa2 : std_logic;
  signal id_setmaskne_Pa3 : std_logic_vector(VLEN-1 downto 0);

  signal id_opmode_Pb1, id_opmode_Pb2, id_opmode_Pa0 : std_logic_vector(7*OPM_NUM-1 downto 0);
  signal id_opmode_Pa1, id_opmode_Pa1x : VOPMODE_TYPE(VLEN-1 downto 0);
  signal id_alumode_Pb1, id_alumode_Pb2, id_alumode_Pa0 : std_logic_vector(4*ALUM_NUM-1 downto 0);
  signal id_alumode_Pa1, id_alumode_Pa1x : VALUMODE_TYPE(VLEN-1 downto 0);

  signal id_alusra_Pb1, id_alusra_Pb2, id_alusra_Pax, id_alusra_Pa0, id_alusra_Pa1, id_alusra_Pa1x, id_alusra_Pa2 : std_logic;
  signal id_alusra_Pa3 : std_logic_vector(VLEN-1 downto 0);

  -- absdiff through DSP48
  signal id_CA_absdiff_clr_Pb1, id_CA_absdiff_clr_Pb2, id_CA_absdiff_clr_Pax, id_CA_absdiff_clr_Pa0, id_CA_absdiff_clr_Pa1, id_CA_absdiff_clr_Pa1x : std_logic;
  signal id_CA_absdiff_clr_Pa2 : std_logic_vector(VLEN-1 downto 0);
  signal id_CA_absdiff_Pb1, id_CA_absdiff_Pb2, id_CA_absdiff_Pax, id_CA_absdiff_Pa0, id_CA_absdiff_Pa1, id_CA_absdiff_Pa1x : std_logic;
  signal id_CA_absdiff_Pa2, id_CA_absdiff_Pa3 : std_logic_vector(VLEN-1 downto 0);

begin
  -----------------------------------------------------------------------
  -- INSTRUCTION FETCH STAGE
  -----------------------------------------------------------------------
  --pc
  PC: sFPE_PC
    generic map(
      OPCODE_WIDTH => OPCODE_WIDTH,
      PM_ADDR_WIDTH=> PM_ADDR_WIDTH,
      PM_DATA_WIDTH=> PM_DATA_WIDTH,
      BRANCH_EN    => BRANCH_EN,
      JMP_EN       => JMP_EN,
      RPT_EN       => RPT_EN,
      RPT_SPEC_1   => RPT_SPEC_1,
      RPT_LEVELS   => RPT_LEVELS,
      RPT_CNT_LEN0 => RPT_CNT_LEN0,
      RPT_CNT_LEN1 => RPT_CNT_LEN1,
      RPT_CNT_LEN2 => RPT_CNT_LEN2,
      RPT_CNT_LEN3 => RPT_CNT_LEN3,
      RPT_CNT_LEN4 => RPT_CNT_LEN4,
      RPT_BLK_LEN0 => RPT_BLK_LEN0,
      RPT_BLK_LEN1 => RPT_BLK_LEN1,
      RPT_BLK_LEN2 => RPT_BLK_LEN2,
      RPT_BLK_LEN3 => RPT_BLK_LEN3,
      RPT_BLK_LEN4 => RPT_BLK_LEN4
    )
      port map(
      clk         =>  clk,
      rst         =>  rst,
      i_en        =>  id_en_pc_Pb1,
      i_inst_data =>  pm_operands_Pb1x,
      i_brc_taken =>  branch_taken_Pa3,
      i_brc_addr  =>  branch_addr_Pa2,
      i_rpt_taken =>  id_rpt_Pb2,
      i_jmp_taken =>  jmp_taken_Pb2,
      i_jmp_addr  =>  branch_addr_Pb2,
      o_pc        =>  pc_addr_Ps
    );

  --pm
  u_pm: sFPE_PM
    generic map(
      PM_SIZE        => PM_SIZE,
      PM_ADDR_WIDTH  => PM_ADDR_WIDTH,
      PM_DATA_WIDTH  => PM_DATA_WIDTH,
      USE_BRAM_FOR_LARGE_PM => USE_BRAM_FOR_LARGE_PM,
      PM_INIT_FILE => PM_INIT_FILE,
      PB0_DEPTH => PB0_DEPTH,
      PB1_DEPTH => PB1_DEPTH
    )
    port map(
      clk   => clk,
      rst   => rst,
      i_en  => id_en_pc_Pb1,
      i_addr=> pc_addr_Ps,
      o_pm  => pm_do_Pb1
    );

  pm_operands_Pb1 <= pm_do_Pb1(PM_DATA_WIDTH-OPCODE_WIDTH-1 downto 0);

  -----------------------------------------------------------------------
  -- FETCH STAGE PIPELINING
  -----------------------------------------------------------------------
  ADDR_5_GEN: if RF_ADDR_WIDTH = 5 generate
    operands_gen: for i in 0 to VLEN-1 generate
      rdaddr_a_Pb2(i) <= pm_operands_Pb2(i)(14 downto 10);
      rdaddr_b_Pb2(i) <= pm_operands_Pb2(i)(9 downto 5);
      rdaddr_c_Pb2(i) <= pm_operands_Pb2(i)(4 downto 0);
    end generate;
    rf_wraddr_Pb2 <= pm_operands_Pb2(0)(19 downto 15);
  end generate;

  ADDR_6_GEN: if RF_ADDR_WIDTH = 6 generate
    operands_gen: for i in 0 to VLEN-1 generate
      rdaddr_a_Pb2(i) <= pm_operands_Pb2(i)(22) & pm_operands_Pb2(i)(14 downto 10);
      rdaddr_b_Pb2(i) <= pm_operands_Pb2(i)(21) & pm_operands_Pb2(i)(9 downto 5);
      rdaddr_c_Pb2(i) <= pm_operands_Pb2(i)(20) & pm_operands_Pb2(i)(4 downto 0);
    end generate;
    rf_wraddr_Pb2 <= pm_operands_Pb2(0)(23) & pm_operands_Pb2(0)(19 downto 15);
  end generate;

  -- Offset is supported in two modes: base+offset or base+inc+offset. In base+offset mode,
  -- the two bits for stream index and autoinc can be saved.
  OFS_DM_GEN: if DM_EN = true generate
    SETOFS_GEN: if isBaseOffset = true generate

      G0: if ((FLEXA_TYPE/2)rem 2) = 1 generate
        EA_0: if EBITS_A = 0 generate
          dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(14 downto 10);
        end generate;
      EA_not0: if EBITS_A > 0 generate
        signal tmp : std_logic_vector(5+EBITS_A-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_A+EBITS_B+EBITS_C-1 downto
          20+EBITS_B+EBITS_C) & pm_operands_Pb2(0)(14 downto 10);
        dm_rofs_addr0_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G1: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
      EB_0: if EBITS_B = 0 generate
        dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(9 downto 5);
      end generate;
      EB_not0: if EBITS_B > 0 generate
        signal tmp : std_logic_vector(5+EBITS_B-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_B+EBITS_C-1 downto 20+EBITS_C) & pm_operands_Pb2(0)(9 downto 5);
        dm_rofs_addr0_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 and ((FLEXC_TYPE/2)rem 2) = 1 generate
      EC_0: if EBITS_C = 0 generate
        dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(4 downto 0);
      end generate;
      EC_not0: if EBITS_C > 0 generate
        signal tmp : std_logic_vector(5+EBITS_C-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_C-1 downto
          20) & pm_operands_Pb2(0)(4 downto 0);
        dm_rofs_addr0_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G3: if ((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
      EB_0: if EBITS_B = 0 generate
        dm_rofs_addr1_Pb2 <= pm_operands_Pb2(0)(9 downto 5);
      end generate;
      EB_not0: if EBITS_B > 0 generate
        signal tmp : std_logic_vector(5+EBITS_B-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_B+EBITS_C-1 downto 20+EBITS_C) & pm_operands_Pb2(0)(9 downto 5);
        dm_rofs_addr1_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G4: if ((((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1) or (((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) /= 1))
      and ((FLEXC_TYPE/2)rem 2) = 1 generate
      EC_0: if EBITS_C = 0 generate
        dm_rofs_addr1_Pb2 <= pm_operands_Pb2(0)(4 downto 0);
      end generate;
      EC_not0: if EBITS_C > 0 generate
        signal tmp : std_logic_vector(5+EBITS_C-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_C-1 downto 20) & pm_operands_Pb2(0)(4 downto 0);
        dm_rofs_addr1_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    ED_0: if EBITS_D = 0 generate
      dm_wofs_addr_Pb2 <= pm_operands_Pb2(0)(19 downto 15);
    end generate;
    ED_not0: if EBITS_D > 0 generate
      signal tmp : std_logic_vector(5+EBITS_D-1 downto 0);
    begin
      -- Special case for 802.11ac FFT
      FFT80211AC_GEN: if EBITS_D = 4 and EBITS_A = 4 and EBITS_C = 4 generate
        tmp <= pm_operands_Pb2(0)(20+EBITS_D-1 downto 20) & pm_operands_Pb2(0)(19 downto 15);
        dm_wofs_addr_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
      NORMAL_GEN: if not (EBITS_D = 4 and EBITS_A = 4 and EBITS_C = 4) generate
        tmp <= pm_operands_Pb2(0)(20+EBITS_D+EBITS_A+EBITS_B+EBITS_C-1 downto
          20+EBITS_A+EBITS_B+EBITS_C) & pm_operands_Pb2(0)(19 downto 15);
        dm_wofs_addr_Pb2 <= tmp(constDMOffsetWidth-1 downto 0);
      end generate;
    end generate;
  end generate;

  INCOFS_GEN: if isBaseOffset = false generate
    G0: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(14 downto 12);
      dm_rb_sel_m_Pb2 <= pm_operands_Pb2(0)(10);
    end generate;

    G1: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
      dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(9 downto 7);
      dm_rb_sel_m_Pb2 <= pm_operands_Pb2(0)(5);
    end generate;

    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1
      and ((FLEXC_TYPE/2)rem 2) = 1
    generate
      dm_rofs_addr0_Pb2 <= pm_operands_Pb2(0)(4 downto 2);
      dm_rb_sel_m_Pb2 <= pm_operands_Pb2(0)(0);
    end generate;

    G3: if ((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) = 1 generate
      dm_rofs_addr1_Pb2 <= pm_operands_Pb2(0)(9 downto 7);
      dm_rb_sel_n_Pb2 <= pm_operands_Pb2(0)(5);
    end generate;

    G4: if ((((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) = 1)
      or (((FLEXA_TYPE/2)rem 2) = 1 and ((FLEXB_TYPE/2)rem 2) /= 1))
      and ((FLEXC_TYPE/2)rem 2) = 1
    generate
      dm_rofs_addr1_Pb2 <= pm_operands_Pb2(0)(4 downto 2);
      dm_rb_sel_n_Pb2 <= pm_operands_Pb2(0)(0);
    end generate;

    dm_wofs_addr_Pb2 <= pm_operands_Pb2(0)(19 downto 17);
    dm_wb_sel_Pb2 <= pm_operands_Pb2(0)(15);
  end generate;

  dm_rb_addr_Pb2 <= pm_operands_Pb2(0)(DM_ADDR_WIDTH-1 downto 0);
  dm_wb_addr_Pb2 <= pm_operands_Pb2(0)(DM_ADDR_WIDTH-1 downto 0);
  end generate; -- DM_EN

  SM_ADR_GEN: if SM_EN = true generate
    G0: if ((FLEXA_TYPE/4)rem 2) = 1 generate
      EA_0: if EBITS_A = 0 generate
        sm_rofs_addr_Pb2 <= pm_operands_Pb2(0)(14 downto 10);
      end generate;
      EA_not0: if EBITS_A > 0 generate
        signal tmp : std_logic_vector(5+EBITS_A-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_A+EBITS_B+EBITS_C-1 downto
          20+EBITS_B+EBITS_C) & pm_operands_Pb2(0)(14 downto 10);
        sm_rofs_addr_Pb2 <= tmp(constSMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G1: if ((FLEXA_TYPE/4)rem 2) /= 1 and ((FLEXB_TYPE/4)rem 2) = 1 generate
      EB_0: if EBITS_B = 0 generate
        sm_rofs_addr_Pb2 <= pm_operands_Pb2(0)(9 downto 5);
      end generate;
      EB_not0: if EBITS_B > 0 generate
        signal tmp : std_logic_vector(5+EBITS_B-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_B+EBITS_C-1 downto
          20+EBITS_C) & pm_operands_Pb2(0)(9 downto 5);
        sm_rofs_addr_Pb2 <= tmp(constSMOffsetWidth-1 downto 0);
      end generate;
    end generate;

    G2: if ((FLEXA_TYPE/4)rem 2) /= 1 and ((FLEXB_TYPE/4)rem 2) /= 1 and ((FLEXC_TYPE/4)rem 2) = 1 generate
      EC_0: if EBITS_C = 0 generate
        sm_rofs_addr_Pb2 <= pm_operands_Pb2(0)(4 downto 0);
      end generate;
      EC_not0: if EBITS_C > 0 generate
        signal tmp : std_logic_vector(5+EBITS_C-1 downto 0);
      begin
        tmp <= pm_operands_Pb2(0)(20+EBITS_C-1 downto
          20) & pm_operands_Pb2(0)(4 downto 0);
        sm_rofs_addr_Pb2 <= tmp(constSMOffsetWidth-1 downto 0);
      end generate;
    end generate;

  sm_wb_addr_Pb2 <= pm_operands_Pb2(0)(SM_ADDR_WIDTH-1 downto 0);
  sm_rb_addr_Pb2 <= pm_operands_Pb2(0)(SM_ADDR_WIDTH-1 downto 0);
  end generate;

  branch_addr_Pb2 <= pm_operands_Pb1x(PM_ADDR_WIDTH-1 downto 0);

  RXCH_NOGEN: if GETCH_EN = false generate
    getchsel_repl_gen: for i in 0 to VLEN-1 generate
      G0: if ((FLEXA_TYPE/8)rem 2) = 1 generate
        get_ch_sel0_Pb2(i) <= pm_operands_Pb2(i)(10+RX_CH_WIDTH-1 downto 10);
      end generate;
      G1: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) = 1 generate
        get_ch_sel0_Pb2(i) <= pm_operands_Pb2(i)(5+RX_CH_WIDTH-1 downto 5);
      end generate;
      G2: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 and ((FLEXC_TYPE/8)rem 2) = 1 generate
        get_ch_sel0_Pb2(i) <= pm_operands_Pb2(i)(RX_CH_WIDTH-1 downto 0);
      end generate;
    end generate;
  end generate;

  TXCH_NOGEN: if PUTCH_EN = false generate
    put_ch_sel_Pb2 <= pm_operands_Pb2(0)(15+TX_CH_WIDTH-1 downto 15);
  end generate;

  MK_BIT_GEN: if MASK_EN = true generate
    mask_bit_Pb2 <= pm_operands_Pb2(0)(31-OPCODE_WIDTH);
  end generate;

  -----------------------------------------------------------------------
  -- INSTRUCTION DECODE/RF/SM STAGE
  -----------------------------------------------------------------------
  --id
  u_id: sFPE_ID
    generic map(
      DATA_WIDTH    =>  DATA_WIDTH,
      DATA_TYPE     =>  DATA_TYPE,
      SLICE_NUM     =>  SLICE_NUM,
      RF_ADDR_WIDTH =>  RF_ADDR_WIDTH,
      OPCODE_WIDTH  =>  OPCODE_WIDTH,
      PM_ADDR_WIDTH => PM_ADDR_WIDTH,
      OPM_NUM       =>  OPM_NUM,
      ALUM_NUM      =>  ALUM_NUM,
      FLEXA_TYPE    => FLEXA_TYPE,
      FLEXB_TYPE    => FLEXB_TYPE,
      FLEXC_TYPE    => FLEXC_TYPE,
      BSLAVE        => BSLAVE,
      BMASTER       => BMASTER,
      BMASTER_NUM  => BMASTER_NUM,
      BRANCH_EN     => BRANCH_EN,
      JMP_EN        => JMP_EN,
      RPT_EN        => RPT_EN,
      RF_EN         => RF_EN,
      DM_EN         => DM_EN,
      DM_TWO_RD_PORTS => hasTwoDMRdPorts,
      SM_EN         => SM_EN,
      GETCH_EN      => GETCH_EN,
      PUTCH_EN      => PUTCH_EN,
      MASKEQ_EN     => MASKEQ_EN,
      MASKGT_EN     => MASKGT_EN,
      MASKLT_EN     => MASKLT_EN,
      MASKGE_EN     => MASKGE_EN,
      MASKLE_EN     => MASKLE_EN,
      MASKNE_EN     => MASKNE_EN,
      ALUSRA_EN     => ALUSRA_EN,
      ABSDIFF_EN    => ABSDIFF_EN,
      ABSDIFF_WITHACCUM  => ABSDIFF_WITHACCUM
      )
    port map(
      clk               => clk,
      i_pm_do           => pm_do_Pb1,
      o_id_opmode       => id_opmode_Pb1,
      o_id_alumode      => id_alumode_Pb1,

      i_ext_barrier     => i_ext_barrier,
      o_en_pc           => id_en_pc_Pb1,
      o_ext_en_sFPE      => id_ext_en_sFPE_Pb1,
      o_ext_id_barrier  => id_ext_barrier_Pb1,
      i_ext_en_sFPE      => i_ext_en_sFPE,

      o_id_get_or_peak0 => id_get_or_peak0_Pb1,
      o_id_get_or_peak1 => id_get_or_peak1_Pb1,
      o_id_get0         => id_get_inst0_Pb1,
      o_id_get1         => id_get_inst1_Pb1,
      o_id_fifowrite    => id_put_inst_Pb1,
      o_id_rx_autoinc   => id_rx_autoinc_Pb1,
      o_id_rx_reset     => id_rx_reset_Pb1,
      o_id_tx_autoinc   => id_tx_autoinc_Pb1,
      o_id_tx_reset     => id_tx_reset_Pb1,

      o_id_rddm0        => id_rddm0_Pb1,
      o_id_rddm1        => id_rddm1_Pb1,
      o_id_wrdm         => id_wrdm_Pb1,
      o_id_dm_set_rb_m0 => id_dm_set_rb_m0_Pb1,
      o_id_dm_set_rb_m1 => id_dm_set_rb_m1_Pb1,
      o_id_dm_set_rb_n0 => id_dm_set_rb_n0_Pb1,
      o_id_dm_set_rb_n1 => id_dm_set_rb_n1_Pb1,
      o_id_dm_inc_rb_m0   => id_dm_inc_rb_m0_Pb1,
      o_id_dm_inc_rb_m1   => id_dm_inc_rb_m1_Pb1,
      o_id_dm_inc_rb_n0   => id_dm_inc_rb_n0_Pb1,
      o_id_dm_inc_rb_n1   => id_dm_inc_rb_n1_Pb1,
      o_id_dm_autoinc_rb_m=> id_dm_autoinc_rb_m_Pb1,
      o_id_dm_autoinc_rb_n=> id_dm_autoinc_rb_n_Pb1,
      o_id_dm_set_wb_0  => id_dm_set_wb_0_Pb1,
      o_id_dm_set_wb_1  => id_dm_set_wb_1_Pb1,
      o_id_dm_inc_wb_0  => id_dm_inc_wb_0_Pb1,
      o_id_dm_inc_wb_1  => id_dm_inc_wb_1_Pb1,
      o_id_dm_autoinc_wb=> id_dm_autoinc_wb_Pb1,

      o_id_sm_set_rb_0   => id_sm_set_rb_0_Pb1,
      o_id_sm_inc_rb_0   => id_sm_inc_rb_0_Pb1,
      o_id_sm_set_wb_0   => id_sm_set_wb_0_Pb1,
      o_id_sm_inc_wb_0   => id_sm_inc_wb_0_Pb1,
      o_id_sm_autoinc_rb => id_sm_autoinc_rb_Pb1,
      o_id_sm_autoinc_wb => id_sm_autoinc_wb_Pb1,
      o_id_sm_wen        => id_sm_wen_Pb1,
      o_id_rdsm          => id_rdsm_Pb1,

      o_id_rf_wen       => id_rf_wen_Pb1,

      o_id_b            => id_b_Pb1,
      o_id_beq          => id_beq_Pb1,
      o_id_bgt          => id_bgt_Pb1,
      o_id_blt          => id_blt_Pb1,
      o_id_bge          => id_bge_Pb1,
      o_id_ble          => id_ble_Pb1,
      o_id_bne          => id_bne_Pb1,
      o_id_rpt          => id_rpt_Pb1,

      o_id_setmaskeq    => id_setmaskeq_Pb1,
      o_id_setmaskgt    => id_setmaskgt_Pb1,
      o_id_setmasklt    => id_setmasklt_Pb1,
      o_id_setmaskge    => id_setmaskge_Pb1,
      o_id_setmaskle    => id_setmaskle_Pb1,
      o_id_setmaskne    => id_setmaskne_Pb1,

      o_id_alusra      => id_alusra_Pb1,
      o_id_CA_absdiff      => id_CA_absdiff_Pb1,
      o_id_CA_absdiff_clr  => id_CA_absdiff_clr_Pb1
    );

  -- rf
  rf_gen: if RF_EN = true generate
  begin
    v_rf_gen: for i in 0 to VLEN-1 generate
    u_rf: sFPE_RF
      generic map (
        RF_ADDR_WIDTH => RF_ADDR_WIDTH,
        RF_DATA_WIDTH => CORE_DATA_WIDTH,
        FRAC_BITS     => FRAC_BITS,
        RF_INIT_EN    => RF_INIT_EN,
        RF_INIT_FILE  => RF_INIT_FILE & integer'image(i) & ".mif",
        PA0_DEPTH     => PA0_DEPTH,
        PA1_DEPTH     => PA1_DEPTH)
      port map(
        clk => clk,
        rst => rst,
        i_rdaddr_a => rdaddr_a_Pb2(i),
        i_rdaddr_b => rdaddr_b_Pb2(i),
        i_rdaddr_c => rdaddr_c_Pb2(i),
        o_rddata_a => src_a_Pa1(i),
        o_rddata_b => src_b_Pa1(i),
        o_rddata_c => src_c_Pa1(i),

        i_wen      => rf_wen_rfin(i),
        i_wraddr_d => rf_wraddr_Pa3(i),
        i_wrdata_d => ex_result_Pa3(i));
    end generate;
  end generate;

-- dmsau_gen:
SAU_GEN:if DM_EN = true generate
  u_sau: sFPE_SAU
    generic map(
      DM_OFFSET_WIDTH        => constDMOffsetWidth,
      DM_ADDR_WIDTH          => DM_ADDR_WIDTH,
      DM_DATA_WIDTH          => DM_DATA_WIDTH,
      DM_WB_NUM              => DM_WB_NUM,
      DM_RB_M_NUM            => DM_RB_M_NUM,
      DM_RB_N_NUM            => DM_RB_N_NUM,
      DM_RB_M_INITIAL0       => DM_RB_M_INITIAL0,
      DM_RB_M_INITIAL1       => DM_RB_M_INITIAL1,
      DM_RB_N_INITIAL0       => DM_RB_N_INITIAL0,
      DM_RB_N_INITIAL1       => DM_RB_N_INITIAL1,
      DM_WB_INITIAL0         => DM_WB_INITIAL0,
      DM_WB_INITIAL1         => DM_WB_INITIAL1,
      DM_RB_M_AUTOINC_SIZE0  => DM_RB_M_AUTOINC_SIZE0,
      DM_RB_M_AUTOINC_SIZE1  => DM_RB_M_AUTOINC_SIZE1,
      DM_RB_N_AUTOINC_SIZE0  => DM_RB_N_AUTOINC_SIZE0,
      DM_RB_N_AUTOINC_SIZE1  => DM_RB_N_AUTOINC_SIZE1,
      DM_WB_AUTOINC_SIZE0    => DM_WB_AUTOINC_SIZE0,
      DM_WB_AUTOINC_SIZE1    => DM_WB_AUTOINC_SIZE1,
      DM_OFFSET_EN           => DM_OFFSET_EN,
      DM_RB_M_SET_EN0        => DM_RB_M_SET_EN0,
      DM_RB_M_SET_EN1        => DM_RB_M_SET_EN1,
      DM_RB_N_SET_EN0        => DM_RB_N_SET_EN0,
      DM_RB_N_SET_EN1        => DM_RB_N_SET_EN1,
      DM_WB_SET_EN0          => DM_WB_SET_EN0,
      DM_WB_SET_EN1          => DM_WB_SET_EN1,
      DM_RB_M_AUTOINC_EN0    => DM_RB_M_AUTOINC_EN0,
      DM_RB_M_AUTOINC_EN1    => DM_RB_M_AUTOINC_EN1,
      DM_RB_N_AUTOINC_EN0    => DM_RB_N_AUTOINC_EN0,
      DM_RB_N_AUTOINC_EN1    => DM_RB_N_AUTOINC_EN1,
      DM_WB_AUTOINC_EN0      => DM_WB_AUTOINC_EN0,
      DM_WB_AUTOINC_EN1      => DM_WB_AUTOINC_EN1,
      DM_RB_M_INC_EN0        => DM_RB_M_INC_EN0,
      DM_RB_M_INC_EN1        => DM_RB_M_INC_EN1,
      DM_RB_N_INC_EN0        => DM_RB_N_INC_EN0,
      DM_RB_N_INC_EN1        => DM_RB_N_INC_EN1,
      DM_WB_INC_EN0          => DM_WB_INC_EN0,
      DM_WB_INC_EN1          => DM_WB_INC_EN1
    )
    port map(
      clk=>clk,

      i_dm_rd_ofs_m=>dm_rofs_addr0_Pb2,
      i_dm_rd_ofs_n=>dm_rofs_addr1_Pb2,
      i_dm_rd_bs=>dm_rb_addr_Pb2,
      i_dm_set_rb_m0 => id_dm_set_rb_m0_Pb2,
      i_dm_set_rb_m1 => id_dm_set_rb_m1_Pb2,
      i_dm_set_rb_n0 => id_dm_set_rb_n0_Pb2,
      i_dm_set_rb_n1 => id_dm_set_rb_n1_Pb2,
      i_dm_inc_rb_m0    => id_dm_inc_rb_m0_Pb2,
      i_dm_inc_rb_m1    => id_dm_inc_rb_m1_Pb2,
      i_dm_inc_rb_n0    => id_dm_inc_rb_n0_Pb2,
      i_dm_inc_rb_n1    => id_dm_inc_rb_n1_Pb2,
      i_dm_autoinc_rb_m => id_dm_autoinc_rb_m_Pb2,
      i_dm_autoinc_rb_n => id_dm_autoinc_rb_n_Pb2,
      i_dm_rb_sel_m     => dm_rb_sel_m_Pb2,
      i_dm_rb_sel_n     => dm_rb_sel_n_Pb2,

      i_dm_wr_ofs      => dm_wofs_addr_Pa2,
      i_dm_wr_bs       => dm_wb_addr_Pa2,
      i_dm_set_wb_0    => id_dm_set_wb_0_Pa2,
      i_dm_set_wb_1    => id_dm_set_wb_1_Pa2,
      i_dm_inc_wb_0    => id_dm_inc_wb_0_Pa2,
      i_dm_inc_wb_1    => id_dm_inc_wb_0_Pa2,
      i_dm_autoinc_wb  => id_dm_autoinc_wb_Pa2,
      i_dm_wb_sel      => dm_wb_sel_Pa2,
      o_dm_rd_addr_0   => dm_rdaddr_0,
      o_dm_rd_addr_1   => dm_rdaddr_1,
      o_dm_wr_addr     => dm_wraddr_Pa2
    );
end generate;

-- dm
dm_gen: if DM_EN = true generate
begin
  v_dm_gen:
  for i in 0 to VLEN-1 generate
    u_dm: sFPE_DM
    generic map(
      DM_OFFSET_WIDTH      => constDMOffsetWidth,
      DM_SIZE              => DM_SIZE,
      DM_ADDR_WIDTH        => DM_ADDR_WIDTH,
      DM_DATA_WIDTH        => DM_DATA_WIDTH,
      DM_INIT_EN           => DM_INIT_EN,
      USE_BRAM_FOR_LARGE_DM=> USE_BRAM_FOR_LARGE_DM,
      DM_INIT_FILE         => DM_INIT_FILE & integer'image(i) & ".mif",
      DM_TWO_RD_PORTS      => hasTwoDMRdPorts,
      DM_TRUE_2R1W         => DM_TRUE_2R1W,
      PA0_DEPTH            => PA0_DEPTH,
      PA1_DEPTH            => PA1_DEPTH
    )
    port map(
      clk=>clk,
      rst=>rst,

      i_dm_rd_addr_0 => dm_rdaddr_0,
      i_dm_rd_addr_1 => dm_rdaddr_1,
      i_dm_wr_addr => dm_wraddr_Pa3(i),

      i_dm_wen=>dm_wen_dmin(i),
      i_dm_din=>ex_result_Pa3(i)(constInputWidth-1 downto 0),

      o_dm_dout0=>dm_do0_Pa1(i)(constInputWidth-1 downto 0),
      o_dm_dout1=>dm_do1_Pa1(i)(constInputWidth-1 downto 0)
    );
  end generate;
end generate;

-- sm
sm_gen: if SM_EN = true generate
  u_sm: sFPE_SM
  generic map(
    SM_OFFSET_WIDTH=>constSMOffsetWidth,
    SM_SIZE => SM_SIZE,
    SM_ADDR_WIDTH=>SM_ADDR_WIDTH,
    SM_DATA_WIDTH=>CORE_DATA_WIDTH,
    USE_BRAM_FOR_LARGE_SM => USE_BRAM_FOR_LARGE_SM,
    SM_INIT_FILE => SM_INIT_FILE,
    PA0_DEPTH => PA0_DEPTH,
    PA1_DEPTH => PA1_DEPTH,
    SM_OFFSET_EN => SM_OFFSET_EN,
    SM_READONLY => SM_READONLY,
    SM_RB_SET_EN0 => SM_RB_SET_EN0,
    SM_WB_SET_EN0 => SM_WB_SET_EN0,
    SM_RB_AUTOINC_SIZE0 => SM_RB_AUTOINC_SIZE0,
    SM_WB_AUTOINC_SIZE0 => SM_WB_AUTOINC_SIZE0,
    SM_RB_AUTOINC_EN0 => SM_RB_AUTOINC_EN0,
    SM_WB_AUTOINC_EN0 => SM_WB_AUTOINC_EN0,
    SM_RB_INC_EN0 => SM_RB_INC_EN0,
    SM_WB_INC_EN0 => SM_WB_INC_EN0
  )
  port map(clk=>clk, rst=> rst,
    i_sm_rd_bs => sm_rb_addr_Pb2,
    i_sm_wr_bs => sm_wb_addr_Pa3,
    i_sm_set_rb_0 => id_sm_set_rb_0_Pb2,
    i_sm_set_wb_0 => id_sm_set_wb_0_Pa3,
    i_sm_inc_rb_0 => id_sm_inc_rb_0_Pb2,
    i_sm_inc_wb_0 => id_sm_inc_wb_0_Pa3,
    i_sm_autoinc_rb => id_sm_autoinc_rb_Pb2,
    i_sm_autoinc_wb => id_sm_autoinc_wb_Pa3,
    i_sm_wen => id_sm_wen_Pa3,
    i_sm_rd_ofs  => sm_rofs_addr_Pb2,
    i_sm_din=>ex_result_Pa3(0),
    o_sm_dout => sm_do_Pa1
  );
end generate;

-- Source select from rf, sm and dm
SHAREGET: if (SHARE_GET_DATA = true) generate
  get_data0_or_1_Pa1 <= get_data0_Pa1;
  id_get_or_peak0_or_1_Pa1 <= id_get_or_peak0_Pa1;
end generate;
NOSHAREGET: if (SHARE_GET_DATA = false) generate
  get_data0_or_1_Pa1 <= get_data1_Pa1;
  id_get_or_peak0_or_1_Pa1 <= id_get_or_peak1_Pa1;
end generate;

FLEXA_R_GEN: if (FLEXA_TYPE = constFLEX_R) generate
  src_a_muxout_Pa1 <= src_a_Pa1;
end generate;
FLEXA_M_GEN: if (FLEXA_TYPE = constFLEX_M) generate
  src_a_muxout_Pa1 <= dm_do0_Pa1;
end generate;
FLEXA_RM_GEN: if (FLEXA_TYPE = constFLEX_RM) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>dm_do0_Pa1(i), sel=>id_rddm0_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_I_GEN: if (FLEXA_TYPE = constFLEX_I) generate
  mux_gen: for i in 0 to VLEN-1 generate
    src_a_muxout_Pa1(i) <= sm_do_Pa1;
  end generate;
end generate;
FLEXA_RI_GEN: if (FLEXA_TYPE = constFLEX_RI) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_MI_GEN: if (FLEXA_TYPE = constFLEX_MI) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux: generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>dm_do0_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_RMI_GEN: if (FLEXA_TYPE = constFLEX_RMI) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    sel(i) <= id_rdsm_Pa1(i) & id_rddm0_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>dm_do0_Pa1(i), i_d2=>sm_do_Pa1, sel=>sel(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_F_GEN: if (FLEXA_TYPE = constFLEX_F) generate
  src_a_muxout_Pa1 <= get_data0_Pa1;
end generate;
FLEXA_RF_GEN: if (FLEXA_TYPE = constFLEX_RF) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>get_data0_Pa1(i), sel=>id_get_or_peak0_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_MF_GEN: if (FLEXA_TYPE = constFLEX_MF) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>get_data0_Pa1(i), i_d1=>dm_do0_Pa1(i), sel=>id_rddm0_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_RMF_GEN: if (FLEXA_TYPE = constFLEX_RMF) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    sel(i) <= id_get_or_peak0_Pa1(i) & id_rddm0_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>dm_do0_Pa1(i), i_d2=>get_data0_Pa1(i), sel=>sel(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_IF_GEN: if (FLEXA_TYPE = constFLEX_IF) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>get_data0_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_RIF_GEN: if (FLEXA_TYPE = constFLEX_RIF) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    sel(i) <= id_get_or_peak0_Pa1(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>sm_do_Pa1, i_d2=>get_data0_Pa1(i), sel=>sel(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_MIF_GEN: if (FLEXA_TYPE = constFLEX_MIF) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    sel(i) <= id_get_or_peak0_Pa1(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>dm_do0_Pa1(i), i_d1=>sm_do_Pa1, i_d2=>get_data0_Pa1(i), sel=>sel(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;
FLEXA_RMIF_GEN: if (FLEXA_TYPE = constFLEX_RMIF) generate
  signal sel : SELTYPE3(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    sel(i) <= id_get_or_peak0_Pa1(i) & id_rdsm_Pa1(i) & id_rddm0_Pa1;
    u_mux: generic_mux_4to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_a_Pa1(i), i_d1=>dm_do0_Pa1(i), i_d2=>sm_do_Pa1, i_d3=>get_data0_Pa1(i), sel=>sel(i), o_d=>src_a_muxout_Pa1(i));
  end generate;
end generate;

-- Flex B
FLEXB_R_GEN: if (FLEXB_TYPE = constFLEX_R) generate
  src_b_muxout_Pa1 <= src_b_Pa1;
end generate;
FLEXB_M_GEN: if (FLEXB_TYPE = constFLEX_M) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
    src_b_muxout_Pa1 <= dm_do0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 generate
    src_b_muxout_Pa1 <= dm_do1_Pa1;
  end generate;
end generate;
FLEXB_RM_GEN: if (FLEXB_TYPE = constFLEX_RM) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_b_Pa1(i), i_d1=>dm_do0_Pa1(i), sel=>id_rddm0_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_b_Pa1(i), i_d1=>dm_do1_Pa1(i), sel=>id_rddm1_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXB_I_GEN: if (FLEXB_TYPE = constFLEX_I) generate
  FLEXB_IMM_gen: if (FLEXB_IMM_VAL /= -1) generate
    mux_gen: for i in 0 to VLEN-1 generate
      src_b_muxout_Pa1(i) <= std_logic_vector(to_unsigned(FLEXB_IMM_VAL, CORE_DATA_WIDTH));
    end generate;
  end generate;
  FLEXB_IMM_NOGEN: if (FLEXB_IMM_VAL = -1) generate
    mux_gen: for i in 0 to VLEN-1 generate
      src_b_muxout_Pa1(i) <= sm_do_Pa1;
    end generate;
  end generate;
end generate;
FLEXB_RI_GEN: if (FLEXB_TYPE = constFLEX_RI) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_MI_GEN: if (FLEXB_TYPE = constFLEX_MI) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux: generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>dm_do0_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      mux_gen: for i in 0 to VLEN-1 generate
      u_mux: generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>dm_do1_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXB_RMI_GEN: if (FLEXB_TYPE = constFLEX_RMI) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
      sel(i) <= id_rdsm_Pa1(i) & id_rddm0_Pa1(i);
      u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_b_Pa1(i), i_d1=>dm_do0_Pa1(i), i_d2=>sm_do_Pa1, sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
    G1: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      sel(i) <= id_rdsm_Pa1(i) & id_rddm1_Pa1(i);
      u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_b_Pa1(i), i_d1=>dm_do1_Pa1(i), i_d2=>sm_do_Pa1, sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXB_F_GEN: if (FLEXB_TYPE = constFLEX_F) generate
  G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
    src_b_muxout_Pa1 <= get_data0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
    src_b_muxout_Pa1 <= get_data0_or_1_Pa1;
  end generate;
end generate;
FLEXB_RF_GEN: if (FLEXB_TYPE = constFLEX_RF) generate
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>get_data0_Pa1(i), sel=>id_get_or_peak0_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>get_data0_or_1_Pa1(i), sel=>id_get_or_peak0_or_1_Pa1(i), o_d=>src_b_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXB_MF_GEN: if (FLEXB_TYPE = constFLEX_MF) generate
    signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
    signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
    signal tmp2 : std_logic_vector(VLEN-1 downto 0);
begin
  G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
    tmp0 <= get_data0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
    tmp0 <= get_data0_or_1_Pa1;
  end generate;
  G2: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
    tmp1 <= dm_do0_Pa1;
    tmp2 <= id_rddm0_Pa1;
  end generate;
  G3: if ((FLEXA_TYPE/2)rem 2) = 1 generate
    tmp1 <= dm_do1_Pa1;
    tmp2 <= id_rddm1_Pa1;
  end generate;
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>tmp1(i), sel=>tmp2(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_RMF_GEN: if (FLEXB_TYPE = constFLEX_RMF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal tmp3 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
      tmp3(i) <= id_rddm0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
      tmp3(i) <= id_rddm1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & tmp3(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>tmp0(i), i_d2=>tmp1(i), sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_IF_GEN: if (FLEXB_TYPE = constFLEX_IF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
      tmp0(i) <= get_data0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
      tmp0(i) <= get_data0_or_1_Pa1(i);
    end generate;
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_RIF_GEN: if (FLEXB_TYPE = constFLEX_RIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
      tmp0(i) <= get_data0_Pa1(i);
      tmp1(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
      tmp0(i) <= get_data0_or_1_Pa1(i);
      tmp1(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;

    sel(i) <= tmp1(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>sm_do_Pa1, i_d2=>tmp0(i), sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_MIF_GEN: if (FLEXB_TYPE = constFLEX_MIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>sm_do_Pa1, i_d2=>tmp1(i), sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;
FLEXB_RMIF_GEN: if (FLEXB_TYPE = constFLEX_RMIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal tmp3 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel : SELTYPE3(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
      tmp3(i) <= id_rddm0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
      tmp3(i) <= id_rddm1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & id_rdsm_Pa1(i) & tmp3(i);
    u_mux: generic_mux_4to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_b_Pa1(i), i_d1=>tmp0(i), i_d2=>sm_do_Pa1, i_d3=>tmp1(i), sel=>sel(i), o_d=>src_b_muxout_Pa1(i));
  end generate;
end generate;

-- Flex C
FLEXC_R_GEN: if (FLEXC_TYPE = constFLEX_R) generate
  src_c_muxout_Pa1 <= src_c_Pa1;
end generate;
FLEXC_M_GEN: if (FLEXC_TYPE = constFLEX_M) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
    src_c_muxout_Pa1 <= dm_do0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
    src_c_muxout_Pa1 <= dm_do1_Pa1;
  end generate;
end generate;
FLEXC_RM_GEN: if (FLEXC_TYPE = constFLEX_RM) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_c_Pa1(i), i_d1=>dm_do0_Pa1(i), sel=>id_rddm0_Pa1(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_c_Pa1(i), i_d1=>dm_do1_Pa1(i), sel=>id_rddm1_Pa1(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXC_I_GEN: if (FLEXC_TYPE = constFLEX_I) generate
  mux_gen: for i in 0 to VLEN-1 generate
    src_c_muxout_Pa1(i) <= sm_do_Pa1;
  end generate;
end generate;
FLEXC_RI_GEN: if (FLEXC_TYPE = constFLEX_RI) generate
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_MI_GEN: if (FLEXC_TYPE = constFLEX_MI) generate
  G0: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
    mux_gen: for i in 0 to VLEN-1 generate
      u_mux: generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>dm_do0_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
  G1: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
      mux_gen: for i in 0 to VLEN-1 generate
      u_mux: generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>dm_do1_Pa1(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXC_RMI_GEN: if (FLEXC_TYPE = constFLEX_RMI) generate
  signal sel : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
      sel(i) <= id_rdsm_Pa1(i) & id_rddm0_Pa1(i);
      u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_c_Pa1(i), i_d1=>dm_do0_Pa1(i), i_d2=>sm_do_Pa1, sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
    G1: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
      sel(i) <= id_rdsm_Pa1(i) & id_rddm1_Pa1(i);
      u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
        port map(i_d0=>src_c_Pa1(i), i_d1=>dm_do1_Pa1(i), i_d2=>sm_do_Pa1, sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXC_F_GEN: if (FLEXC_TYPE = constFLEX_F) generate
  G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
    src_c_muxout_Pa1 <= get_data0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
    src_c_muxout_Pa1 <= get_data0_or_1_Pa1;
  end generate;
end generate;
FLEXC_RF_GEN: if (FLEXC_TYPE = constFLEX_RF) generate
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
     u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>get_data0_Pa1(i), sel=>id_get_or_peak0_Pa1(i), o_d=>src_c_muxout_Pa1(i));
   end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
     u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>get_data0_or_1_Pa1(i), sel=>id_get_or_peak0_or_1_Pa1(i), o_d=>src_c_muxout_Pa1(i));
    end generate;
  end generate;
end generate;
FLEXC_MF_GEN: if (FLEXC_TYPE = constFLEX_MF) generate
    signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
    signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
    signal tmp2 : std_logic_vector(VLEN-1 downto 0);
begin
  G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
    tmp0 <= get_data0_Pa1;
  end generate;
  G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
    tmp0 <= get_data0_or_1_Pa1;
  end generate;
  G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
    tmp1 <= dm_do0_Pa1;
    tmp2 <= id_rddm0_Pa1;
  end generate;
  G3: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
    tmp1 <= dm_do1_Pa1;
    tmp2 <= id_rddm1_Pa1;
  end generate;
  mux_gen: for i in 0 to VLEN-1 generate
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>tmp1(i), sel=>tmp2(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_RMF_GEN: if (FLEXC_TYPE = constFLEX_RMF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal tmp3 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
      tmp3(i) <= id_rddm0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
      tmp3(i) <= id_rddm1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & tmp3(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>tmp0(i), i_d2=>tmp1(i), sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_IF_GEN: if (FLEXC_TYPE = constFLEX_IF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
      tmp0(i) <= get_data0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
      tmp0(i) <= get_data0_or_1_Pa1(i);
    end generate;
    u_mux:generic_mux_2to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>sm_do_Pa1, sel=>id_rdsm_Pa1(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_RIF_GEN: if (FLEXC_TYPE = constFLEX_RIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  tmp_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
      tmp0(i) <= get_data0_Pa1(i);
      tmp1(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
      tmp0(i) <= get_data0_or_1_Pa1(i);
      tmp1(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;

    sel(i) <= tmp1(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>sm_do_Pa1, i_d2=>tmp0(i), sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_MIF_GEN: if (FLEXC_TYPE = constFLEX_MIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel  : SELTYPE2(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & id_rdsm_Pa1(i);
    u_mux: generic_mux_3to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>tmp0(i), i_d1=>sm_do_Pa1, i_d2=>tmp1(i), sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;
FLEXC_RMIF_GEN: if (FLEXC_TYPE = constFLEX_RMIF) generate
  signal tmp0 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp1 : VCOREDATA_TYPE(VLEN-1 downto 0);
  signal tmp2 : VSIG_TYPE(VLEN-1 downto 0);
  signal tmp3 : VSIG_TYPE(VLEN-1 downto 0);
  signal sel : SELTYPE3(VLEN-1 downto 0);
begin
  mux_gen: for i in 0 to VLEN-1 generate
    G0: if ((FLEXA_TYPE/8)rem 2) /= 1 and ((FLEXB_TYPE/8)rem 2) /= 1 generate
      tmp1(i) <= get_data0_Pa1(i);
      tmp2(i) <= id_get_or_peak0_Pa1(i);
    end generate;
    G1: if ((FLEXA_TYPE/8)rem 2) = 1 or ((FLEXB_TYPE/8)rem 2) = 1 generate
      tmp1(i) <= get_data0_or_1_Pa1(i);
      tmp2(i) <= id_get_or_peak0_or_1_Pa1(i);
    end generate;
    G2: if ((FLEXA_TYPE/2)rem 2) /= 1 and ((FLEXB_TYPE/2)rem 2) /= 1 generate
      tmp0(i) <= dm_do0_Pa1(i);
      tmp3(i) <= id_rddm0_Pa1(i);
    end generate;
    G3: if ((FLEXA_TYPE/2)rem 2) = 1 or ((FLEXB_TYPE/2)rem 2) = 1 generate
      tmp0(i) <= dm_do1_Pa1(i);
      tmp3(i) <= id_rddm1_Pa1(i);
    end generate;
    sel(i) <= tmp2(i) & id_rdsm_Pa1(i) & tmp3(i);
    u_mux: generic_mux_4to1 generic map(DATA_WIDTH=>CORE_DATA_WIDTH)
      port map(i_d0=>src_c_Pa1(i), i_d1=>tmp0(i), i_d2=>sm_do_Pa1, i_d3=>tmp1(i), sel=>sel(i), o_d=>src_c_muxout_Pa1(i));
  end generate;
end generate;

-- mask control rf_wen and dm_wen
mask_en_gen: if MASK_EN = true generate
  signal mask_taken : std_logic_vector(VLEN-1 downto 0);
begin
  mask_taken_gen: for i in 0 to VLEN-1 generate
    process (clk) begin
      if (clk'event and clk = '1') then
        if (id_setmaskeq_Pa3(i)='1') then
          mask_taken(i) <= cond_eq_Pa3(i);
        elsif (id_setmaskgt_Pa3(i)='1') then
          mask_taken(i) <= (not cond_eq_Pa3(i)) and (not cond_sign_Pa3(i));
        elsif (id_setmasklt_Pa3(i)='1') then
          mask_taken(i) <= cond_sign_Pa3(i);
        elsif (id_setmaskge_Pa3(i)='1') then
          mask_taken(i) <= (not cond_sign_Pa3(i));
        elsif (id_setmaskle_Pa3(i)='1') then
          mask_taken(i) <= cond_eq_Pa3(i) or cond_sign_Pa3(i);
        elsif (id_setmaskne_Pa3(i)='1') then
          mask_taken(i) <= (not cond_eq_Pa3(i));
        end if;
      end if;
    end process;
  end generate;

  rfwren_mask_gen: for i in 0 to VLEN-1 generate
    process (id_wrdm_Pa3, id_rf_wen_Pa3, mask_bit_Pa3, mask_taken) begin
      if mask_taken(i) = '1' and mask_bit_Pa3(i) = '1' then
        rf_wen_rfin(i) <= '0';
        dm_wen_dmin(i) <= '0';
      else
        rf_wen_rfin(i) <= id_rf_wen_Pa3(i);
        dm_wen_dmin(i) <= id_wrdm_Pa3(i);
      end if;
    end process;
  end generate;
end generate;
mask_no_gen: if MASK_EN = false generate
  rf_wen_rfin <= id_rf_wen_Pa3;
  dm_wen_dmin <= id_wrdm_Pa3;
end generate;

o_ext_barrier <= id_ext_barrier_Pb2;
o_ext_en_sFPE  <= id_ext_en_sFPE_Pb2;
-----------------------------------------------------------------------
-- CUSTOM ACCELERATOR
-----------------------------------------------------------------------
-- absdiff accum component
AD_GEN: if ABSDIFF_EN = true generate
  absdiff_type2_gen: for i in 0 to VLEN-1 generate
    u_absdiff: spu_absdiffaccum generic map (
      DATA_WIDTH=>CORE_DATA_WIDTH,
      IN_DATA_WIDTH=>constInputWidth,
      ABSDIFF_WITHACCUM=>ABSDIFF_WITHACCUM)
      port map(
      clk=>clk,
      i_d0=>src_b_Pa1x(i)(constInputWidth-1 downto 0),
      i_d1=>src_c_Pa1x(i)(constInputWidth-1 downto 0),
      i_clr=>id_CA_absdiff_clr_Pa2(i),
      i_en=>id_CA_absdiff_Pa2(i),
      o_d=>absdiff_out_Pa3(i));
  end generate;
end generate;

-----------------------------------------------------------------------
-- EX STAGE & RESULT SELECTION & WB STAGE
-----------------------------------------------------------------------
--ex
DSP48_GEN: if DSP48E_EN = true generate
v_ex_gen:
for i in 0 to VLEN-1 generate
u_ex: sFPE_EX
  generic map(
    DATA_WIDTH => DATA_WIDTH,
    CORE_DATA_WIDTH   => CORE_DATA_WIDTH,
    DATA_TYPE  => DATA_TYPE,
    SLICE_NUM => SLICE_NUM,
    OPM_NUM  => OPM_NUM,
    ALUM_NUM => ALUM_NUM,
    MULREG_EN => MULREG_EN,
    FRAC_BITS => FRAC_BITS,
    MASK_EN   => MASK_EN,
    ALUSRA_VAL=> ALUSRA_VAL,
    BRANCH_EN => BRANCH_EN
    )
    port map(
    clk => clk, rst => rst,
    i_opmode   => id_opmode_Pa1x(i),
    i_alumode  => id_alumode_Pa1x(i),
    i_src_a    => src_a_Pa1x(i),
    i_src_b    => src_b_Pa1x(i),
    i_src_c    => src_c_Pa1x(i),
    o_sign     => cond_sign_Pa3(i),
    o_zero     => cond_eq_Pa3(i),
    o_dsp48_result => dsp48_result_Pa3(i),
    o_dsp48sra_result => dsp48sra_result_Pa3(i)
    );
end generate;
end generate;

DSP48_NOGEN: if DSP48E_EN = false generate
  data_gen_Pa2_3: for i in 0 to VLEN-1 generate
    u_buf_src_c_Pa1x:generic_reg generic map(REG_NUM=>PaxLevel+2, REG_WIDTH=>CORE_DATA_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>src_c_Pa1x(i), o_d=>dsp48_result_Pa3(i));
  end generate;
end generate;

----------------------------------------------------------------------
-- Branch control generation
-----------------------------------------------------------------------
branchdetc_gen:
if BRANCH_EN = true or JMP_EN = true generate
  u_branchdetect: sFPE_branch
  generic map(PC_ADDR_WIDTH => PM_ADDR_WIDTH, BRANCH_EN => BRANCH_EN,
              JMP_EN  => JMP_EN)
  port map(
    i_id_beq => id_beq_Pa2,
    i_id_bgt => id_bgt_Pa2,
    i_id_blt => id_blt_Pa2,
    i_id_bge => id_bge_Pa2,
    i_id_ble => id_ble_Pa2,
    i_id_bne => id_bne_Pa2,
    i_id_b   => id_b_Pb2,
    i_ex_zero  => cond_eq_Pa3(0),
    i_ex_sign  => cond_sign_Pa3(0),
    o_jmp_taken=> jmp_taken_Pb2,
    o_branch_taken=> branch_taken_Pa3);
end generate;

-----------------------------------------------------------------------
-- Communication generation
-----------------------------------------------------------------------
-- Instantiate communication component
commput_gen: for i in 0 to VLEN-1 generate
  u_comm: sFPE_comm_put
    generic map (
    DATA_WIDTH  => CORE_DATA_WIDTH,
    TX_CH_WIDTH => TX_CH_WIDTH,
    TX_CH_NUM   => TX_CH_NUM,
    PUTCH_EN    => PUTCH_EN,
    STATE_EN    => false)
    port map (
    clk    => clk, rst    => rst,
    i_put_ch_select  => put_ch_sel_Pa2(i),
    i_tx_autoinc   => id_tx_autoinc_Pa2(i),
    i_tx_reset     => id_tx_reset_Pa2(i),
    i_put_data     => put_data_Pa3(i), -- From processor core
    i_put_ch_full  => i_put_ch_full((i+1)*TX_CH_NUM-1 downto i*TX_CH_NUM),
    i_put_inst     => id_put_inst_Pa2(i),  -- PUT instruction, used as write enable signal
    o_put_ch_data  => o_put_ch_data((i+1)*TX_CH_NUM-1 downto i*TX_CH_NUM), -- to fifo
    o_put_ch_full  => open,-- To processor core
    o_put_ch_write => o_put_ch_write((i+1)*TX_CH_NUM-1 downto i*TX_CH_NUM)
    );
end generate;

ONEGET: if hasTwoFIFORdPorts = false generate
  commget_gen: for i in 0 to VLEN-1 generate
    u_comm: sFPE_comm_get
      generic map (
      DATA_WIDTH  => CORE_DATA_WIDTH,
      OUT_DATA_WIDTH  => constInputWidth,
      RX_CH_WIDTH => RX_CH_WIDTH,
      RX_CH_NUM   => RX_CH_NUM,
      GETCH_EN    => GETCH_EN,
      STATE_EN    => false)
      port map (
      clk    => clk, rst    => rst,
      i_get_ch_select  => get_ch_sel0_Pb2(i),
      i_get_ch_data   => i_get_ch_data((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM),
      i_get_ch_empty  => i_get_ch_empty((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM),
      o_get_ch_read   => o_get_ch_read((i+1)*RX_CH_NUM-1 downto i*RX_CH_NUM), -- to processor core
      i_get_inst      => id_get_inst0_Pb2_masked(i), --Get instruction, use as a read signal
      i_rx_reset      => id_rx_reset_Pb2,
      i_rx_autoinc    => id_rx_autoinc_Pb2,
      o_get_data      => get_data0_Pa1(i)(constInputWidth-1 downto 0),
      o_get_ch_empty  => open  --to processor core
      );
  end generate;
end generate;

TWOGET: if hasTwoFIFORdPorts = true generate
  assert (RX_CH_NUM = 2)
  report "When there are two commgets, RX_CH_NUM must be 2 and each commget only has 1 input"
  severity failure;

  -- Note that two get channels are switched. commget0 is at index 1 and commget1 is at index 0
  -- in i_get_ch_xx mapping.
  commget_gen: for i in 0 to VLEN-1 generate
    u_comm: sFPE_comm_get
      generic map (
      DATA_WIDTH     => CORE_DATA_WIDTH,
      OUT_DATA_WIDTH => constInputWidth,
      RX_CH_WIDTH => 1,
      RX_CH_NUM   => 1,
      GETCH_EN    => false,
      STATE_EN    => false)
      port map (
      clk => clk, rst => rst,
      i_get_ch_select => open,
      i_get_ch_data   => i_get_ch_data(2*i+1 downto 2*i+1),
      i_get_ch_empty  => i_get_ch_empty(2*i+1 downto 2*i+1),
      o_get_ch_read   => o_get_ch_read(2*i+1 downto 2*i+1),
      i_get_inst      => id_get_inst0_Pb2_masked(i), --Get instruction, use as a read signal
      i_rx_reset      => open,
      i_rx_autoinc    => open,
      o_get_data      => get_data0_Pa1(i)(constInputWidth-1 downto 0),
      o_get_ch_empty  => open  --to processor core
      );
  end generate;

  commget1_gen: for i in 0 to VLEN-1 generate
    u_comm: sFPE_comm_get
      generic map (
      DATA_WIDTH     => CORE_DATA_WIDTH,
      OUT_DATA_WIDTH => constInputWidth,
      RX_CH_WIDTH => 1,
      RX_CH_NUM   => 1,
      GETCH_EN    => false,
      STATE_EN    => false)
      port map (
      clk => clk, rst => rst,
      i_get_ch_select => open,
      i_get_ch_data   => i_get_ch_data(2*i downto 2*i),
      i_get_ch_empty  => i_get_ch_empty(2*i downto 2*i),
      o_get_ch_read   => o_get_ch_read(2*i downto 2*i),
      i_get_inst      => id_get_inst1_Pb2(i), --Get instruction, use as a read signal
      i_rx_autoinc    => open,
      i_rx_reset      => open,
      o_get_data      => get_data1_Pa1(i)(constInputWidth-1 downto 0),
      o_get_ch_empty  => open --to processor core
      );
  end generate;
end generate;

-----------------------------------------------------------------------
-- Result selection stage
-----------------------------------------------------------------------

DIRECT_WB_GEN: if DIRECT_WB_EN = true generate
  ALUSRA_GEN: if ALUSRA_EN = true generate
    put_data_Pa3 <= dsp48sra_result_Pa3;
    ex_result_Pa3 <= dsp48sra_result_Pa3;
  end generate;
  ABSDIFF_GEN: if ABSDIFF_EN = true generate
    put_data_Pa3 <= absdiff_out_Pa3;
    ex_result_Pa3 <= dsp48_result_Pa3;
  end generate;
  DSP48_GEN: if ALUSRA_EN = false and ABSDIFF_EN = false and DSP48E_EN = true generate
    put_data_Pa3 <= dsp48_result_Pa3;
    ex_result_Pa3 <= dsp48_result_Pa3;
  end generate;
end generate;

NORMAL_WB_GEN: if DIRECT_WB_EN = false generate
  v_wb_gen: for i in 0 to VLEN-1 generate
    u_wb: sFPE_wrtie_back
    generic map (
      CORE_DATA_WIDTH => CORE_DATA_WIDTH,
      ABSDIFF_EN      => ABSDIFF_EN,
      ALUSRA_EN       =>ALUSRA_EN)
    port map (
      i_dsp48_result    => dsp48_result_Pa3(i),
      i_dsp48sra_result => dsp48sra_result_Pa3(i),
      i_alusra          => id_alusra_Pa3(i),
      i_CA_absdiff      => id_CA_absdiff_Pa3(i),
      i_CA_absdiff_d    => absdiff_out_Pa3(i),
      o_result          => ex_result_Pa3(i)
    );
    put_data_Pa3(i) <= ex_result_Pa3(i);
  end generate;
end generate;

-----------------------------------------------------------------------
-- PIPELINE STAGE
-----------------------------------------------------------------------
-- pm_operands
u_buf_pm_operands_Pb1x:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>PM_DATA_WIDTH-OPCODE_WIDTH)
  port map(clk=>clk, rst=>rst, i_d=>pm_operands_Pb1, o_d=>pm_operands_Pb1x);
pm_operands_buf_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_pm_operands_Pb2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>PM_DATA_WIDTH-OPCODE_WIDTH)
  port map(clk=>clk, rst=>rst, i_d=>pm_operands_Pb1x, o_d=>pm_operands_Pb2(i));
end generate;

-- mask
mask_en_bufs_gen: if MASK_EN = true generate
  u_buf_mask_bit_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pb2, o_d=>mask_bit_Pax);
  u_buf_mask_bit_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pax, o_d=>mask_bit_Pa0);
  u_buf_mask_bit_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pa0, o_d=>mask_bit_Pa1);
  u_buf_mask_bit_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pa1, o_d=>mask_bit_Pa1x);
  u_buf_mask_bit_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pa1x, o_d=>mask_bit_Pa2);
  mask_bit_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_mask_bit_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>mask_bit_Pa2, o_d=>mask_bit_Pa3(i));
  end generate;
 M0: if MASKEQ_EN = true generate
  u_buf_id_setmaskeq_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pb1, o_d=>id_setmaskeq_Pb2);
  u_buf_id_setmaskeq_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pb2, o_d=>id_setmaskeq_Pax);
  u_buf_id_setmaskeq_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pax, o_d=>id_setmaskeq_Pa0);
  u_buf_id_setmaskeq_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pa0, o_d=>id_setmaskeq_Pa1);
  u_buf_id_setmaskeq_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pa1, o_d=>id_setmaskeq_Pa1x);
  u_buf_id_setmaskeq_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pa1x, o_d=>id_setmaskeq_Pa2);
  id_setmaskeq_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmaskeq_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmaskeq_Pa2, o_d=>id_setmaskeq_Pa3(i));
  end generate;
  end generate;

  M1: if MASKGT_EN = true generate
  u_buf_id_setmaskgt_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pb1, o_d=>id_setmaskgt_Pb2);
  u_buf_id_setmaskgt_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pb2, o_d=>id_setmaskgt_Pax);
  u_buf_id_setmaskgt_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pax, o_d=>id_setmaskgt_Pa0);
  u_buf_id_setmaskgt_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pa0, o_d=>id_setmaskgt_Pa1);
  u_buf_id_setmaskgt_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pa1, o_d=>id_setmaskgt_Pa1x);
  u_buf_id_setmaskgt_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pa1x, o_d=>id_setmaskgt_Pa2);
  id_setmaskgt_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmaskgt_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmaskgt_Pa2, o_d=>id_setmaskgt_Pa3(i));
  end generate;
  end generate;

  M2: if MASKLT_EN = true generate
  u_buf_id_setmasklt_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pb1, o_d=>id_setmasklt_Pb2);
  u_buf_id_setmasklt_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pb2, o_d=>id_setmasklt_Pax);
  u_buf_id_setmasklt_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pax, o_d=>id_setmasklt_Pa0);
  u_buf_id_setmasklt_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pa0, o_d=>id_setmasklt_Pa1);
  u_buf_id_setmasklt_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pa1, o_d=>id_setmasklt_Pa1x);
  u_buf_id_setmasklt_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pa1x, o_d=>id_setmasklt_Pa2);
  id_setmasklt_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmasklt_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmasklt_Pa2, o_d=>id_setmasklt_Pa3(i));
  end generate;
  end generate;

  M3: if MASKGE_EN = true generate
  u_buf_id_setmaskge_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pb1, o_d=>id_setmaskge_Pb2);
  u_buf_id_setmaskge_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pb2, o_d=>id_setmaskge_Pax);
  u_buf_id_setmaskge_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pax, o_d=>id_setmaskge_Pa0);
  u_buf_id_setmaskge_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pa0, o_d=>id_setmaskge_Pa1);
  u_buf_id_setmaskge_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pa1, o_d=>id_setmaskge_Pa1x);
  u_buf_id_setmaskge_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pa1x, o_d=>id_setmaskge_Pa2);
  id_setmaskge_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmaskge_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmaskge_Pa2, o_d=>id_setmaskge_Pa3(i));
  end generate;
  end generate;

  M4: if MASKLE_EN = true generate
  u_buf_id_setmaskle_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pb1, o_d=>id_setmaskle_Pb2);
  u_buf_id_setmaskle_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pb2, o_d=>id_setmaskle_Pax);
  u_buf_id_setmaskle_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pax, o_d=>id_setmaskle_Pa0);
  u_buf_id_setmaskle_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pa0, o_d=>id_setmaskle_Pa1);
  u_buf_id_setmaskle_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pa1, o_d=>id_setmaskle_Pa1x);
  u_buf_id_setmaskle_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pa1x, o_d=>id_setmaskle_Pa2);
  id_setmaskle_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmaskle_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmaskle_Pa2, o_d=>id_setmaskle_Pa3(i));
  end generate;
  end generate;

  M5: if MASKNE_EN = true generate
  u_buf_id_setmaskne_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pb1, o_d=>id_setmaskne_Pb2);
  u_buf_id_setmaskne_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pb2, o_d=>id_setmaskne_Pax);
  u_buf_id_setmaskne_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pax, o_d=>id_setmaskne_Pa0);
  u_buf_id_setmaskne_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pa0, o_d=>id_setmaskne_Pa1);
  u_buf_id_setmaskne_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pa1, o_d=>id_setmaskne_Pa1x);
  u_buf_id_setmaskne_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pa1x, o_d=>id_setmaskne_Pa2);
  id_setmaskne_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_setmaskne_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_setmaskne_Pa2, o_d=>id_setmaskne_Pa3(i));
  end generate;
  end generate;
end generate;

B0: if BMASTER = true or BSLAVE = true generate
u_buf_id_ext_barrier_Pb2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>BMASTER_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_ext_barrier_Pb1, o_d=>id_ext_barrier_Pb2);

u_buf_id_ext_en_sFPE_Pb2:generic_reg1 generic map(REG_NUM=>1)
  port map(clk=>clk, rst=>rst, i_d=>id_ext_en_sFPE_Pb1, o_d=>id_ext_en_sFPE_Pb2);
end generate;

-- get
get_inst0_buf_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_id_get_inst0_Pb2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_get_inst0_Pb1, o_d=>id_get_inst0_Pb2(i));
end generate;

RXCH_GEN: if GETCH_EN = true generate
  u_buf_id_rx_reset_Pb2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_rx_reset_Pb1, o_d=>id_rx_reset_Pb2);
  u_buf_id_rx_autoinc_Pb2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_rx_autoinc_Pb1, o_d=>id_rx_autoinc_Pb2);
end generate;

u_buf_id_get_or_peak0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak0_Pb1, o_d=>id_get_or_peak0_Pb2);
u_buf_id_get_or_peak0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak0_Pb2, o_d=>id_get_or_peak0_Pa0);
get_or_peak0_buffer_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_id_get_or_peak0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak0_Pa0, o_d=>id_get_or_peak0_Pa1(i));
end generate;

TWOGET_BUF_GEN: if hasTwoFIFORdPorts = true generate
  get_buf_repl1_gen: for i in 0 to VLEN-1 generate
    u_buf_id_get_inst_Pb2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_get_inst1_Pb1, o_d=>id_get_inst1_Pb2(i));
  end generate;

  u_buf_id_get_or_peak1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak1_Pb1, o_d=>id_get_or_peak1_Pb2);
  u_buf_id_get_or_peak1_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak1_Pb2, o_d=>id_get_or_peak1_Pa0);
  get_or_peak1_buffer_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_get_or_peak1_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_get_or_peak1_Pa0, o_d=>id_get_or_peak1_Pa1(i));
  end generate;
end generate;

-- GETI execution masks all get signals except the first
GETI_GEN: if GETI_EN = true generate
  assert (SM_EN = true and SM_READONLY = false)
  report "When using GETI, SM must be writable!"
  severity failure;

  get_mask_gen: for i in 0 to VLEN-1 generate
    enable_first_get_gen: if (i = 0) generate
      id_get_inst0_Pb2_masked(0) <= id_get_inst0_Pb2(0);
    end generate;

    disable_others_get_gen: if (i /= 0) generate
      id_get_inst0_Pb2_masked(i) <= '0' when (id_sm_wen_Pax = '1') else id_get_inst0_Pb2(i);
    end generate;
  end generate;
end generate;
NO_GETI_GEN: if GETI_EN = false generate
  get_mask_gen: for i in 0 to VLEN-1 generate
    id_get_inst0_Pb2_masked(i) <= id_get_inst0_Pb2(i);
  end generate;
end generate;

-- put replication
u_buf_id_put_inst_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pb1, o_d=>id_put_inst_Pb2);
u_buf_id_put_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pb2, o_d=>id_put_inst_Pax);
u_buf_id_put_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pax, o_d=>id_put_inst_Pa0);
u_buf_id_put_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pa0, o_d=>id_put_inst_Pa1);
u_buf_id_put_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pa1, o_d=>id_put_inst_Pa1x);
put_buf_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_id_put_Pa2:generic_reg1 generic map(REG_NUM=>1)
  port map(clk=>clk, rst=>rst, i_d=>id_put_inst_Pa1x, o_d=>id_put_inst_Pa2(i));
end generate;

-- put_ch_sel_Pb2
NOPUTCH: if PUTCH_EN = false generate
  u_buf_put_ch_sel_Pax:generic_reg generic map(REG_NUM=>PaxLevel, REG_WIDTH=>TX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>put_ch_sel_Pb2, o_d=>put_ch_sel_Pax);
  u_put_ch_sel_reg_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>put_ch_sel_Pax, o_d=>put_ch_sel_Pa0);
  u_put_ch_sel_reg_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>put_ch_sel_Pa0, o_d=>put_ch_sel_Pa1);
  put_ch_sel_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_put_ch_sel_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>TX_CH_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>put_ch_sel_Pa1, o_d=>put_ch_sel_Pa2(i));
  end generate;
end generate;
TXCH_GEN: if PUTCH_EN = true generate
  u_buf_id_tx_reset_Pb2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_reset_Pb1, o_d=>id_tx_reset_Pb2);
  u_buf_id_tx_reset_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_reset_Pb2, o_d=>id_tx_reset_Pax);
  u_id_tx_reset_reg_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_reset_Pax, o_d=>id_tx_reset_Pa0);
  u_id_tx_reset_reg_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_reset_Pa0, o_d=>id_tx_reset_Pa1);
  id_tx_reset_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_id_tx_reset_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_reset_Pa1, o_d=>id_tx_reset_Pa2(i));
  end generate;

  u_buf_id_tx_autoinc_Pb2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_autoinc_Pb1, o_d=>id_tx_autoinc_Pb2);
  u_buf_id_tx_autoinc_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_autoinc_Pb2, o_d=>id_tx_autoinc_Pax);
  u_id_tx_autoinc_reg_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_autoinc_Pax, o_d=>id_tx_autoinc_Pa0);
  u_id_tx_autoinc_reg_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_autoinc_Pa0, o_d=>id_tx_autoinc_Pa1);
  id_tx_autoinc_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_id_tx_autoinc_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_tx_autoinc_Pa1, o_d=>id_tx_autoinc_Pa2(i));
  end generate;
end generate;

-- branch instructions
jmp_buf_gen: if JMP_EN = true generate
u_buf_id_b_Pb2:generic_reg1 generic map(REG_NUM=>1)
  port map(clk=>clk, rst=>rst, i_d=>id_b_Pb1, o_d=>id_b_Pb2);
end generate;

rpt_buf_gen: if RPT_EN = true generate
u_buf_id_rpt_Pb2:generic_reg1 generic map(REG_NUM=>1)
  port map(clk=>clk, rst=>rst, i_d=>id_rpt_Pb1, o_d=>id_rpt_Pb2);
end generate;

branch_buf_gen:if BRANCH_EN = true generate
  u_buf_id_beq_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pb1, o_d=>id_beq_Pb2);
  u_buf_id_beq_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pb2, o_d=>id_beq_Pax);
  u_buf_id_beq_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pax, o_d=>id_beq_Pa0);
  u_buf_id_beq_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pa0, o_d=>id_beq_Pa1);
  u_buf_id_beq_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pa1, o_d=>id_beq_Pa1x);
  u_buf_id_beq_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_beq_Pa1x, o_d=>id_beq_Pa2);

  u_buf_id_bgt_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pb1, o_d=>id_bgt_Pb2);
  u_buf_id_bgt_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pb2, o_d=>id_bgt_Pax);
  u_buf_id_bgt_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pax, o_d=>id_bgt_Pa0);
  u_buf_id_bgt_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pa0, o_d=>id_bgt_Pa1);
  u_buf_id_bgt_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pa1, o_d=>id_bgt_Pa1x);
  u_buf_id_bgt_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_bgt_Pa1x, o_d=>id_bgt_Pa2);

  u_buf_id_blt_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pb1, o_d=>id_blt_Pb2);
  u_buf_id_blt_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pb2, o_d=>id_blt_Pax);
  u_buf_id_blt_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pax, o_d=>id_blt_Pa0);
  u_buf_id_blt_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pa0, o_d=>id_blt_Pa1);
  u_buf_id_blt_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pa1, o_d=>id_blt_Pa1x);
  u_buf_id_blt_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_blt_Pa1x, o_d=>id_blt_Pa2);

  u_buf_id_bge_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pb1, o_d=>id_bge_Pb2);
  u_buf_id_bge_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pb2, o_d=>id_bge_Pax);
  u_buf_id_bge_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pax, o_d=>id_bge_Pa0);
  u_buf_id_bge_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pa0, o_d=>id_bge_Pa1);
  u_buf_id_bge_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pa1, o_d=>id_bge_Pa1x);
  u_buf_id_bge_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_bge_Pa1x, o_d=>id_bge_Pa2);

  u_buf_id_ble_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pb1, o_d=>id_ble_Pb2);
  u_buf_id_ble_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pb2, o_d=>id_ble_Pax);
  u_buf_id_ble_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pax, o_d=>id_ble_Pa0);
  u_buf_id_ble_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pa0, o_d=>id_ble_Pa1);
  u_buf_id_ble_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pa1, o_d=>id_ble_Pa1x);
  u_buf_id_ble_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_ble_Pa1x, o_d=>id_ble_Pa2);

  u_buf_id_bne_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pb1, o_d=>id_bne_Pb2);
  u_buf_id_bne_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pb2, o_d=>id_bne_Pax);
  u_buf_id_bne_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pax, o_d=>id_bne_Pa0);
  u_buf_id_bne_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pa0, o_d=>id_bne_Pa1);
  u_buf_id_bne_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pa1, o_d=>id_bne_Pa1x);
  u_buf_id_bne_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_bne_Pa1x, o_d=>id_bne_Pa2);

  u_buf_branch_addr_Pax:generic_reg generic map(REG_NUM=>PaxLevel, REG_WIDTH=>PM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>branch_addr_Pb2, o_d=>branch_addr_Pax);
  u_buf_branch_addr_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>branch_addr_Pax, o_d=>branch_addr_Pa0);
  u_buf_branch_addr_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>branch_addr_Pa0, o_d=>branch_addr_Pa1);
  u_buf_branch_addr_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>branch_addr_Pa1, o_d=>branch_addr_Pa1x);
  u_buf_branch_addr_Pa2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>PM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>branch_addr_Pa1x, o_d=>branch_addr_Pa2);
end generate;

-- rf
rf_buf_gen: if RF_EN = true generate
  u_buf_id_rf_wen_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pb1, o_d=>id_rf_wen_Pb2);
  u_buf_id_rf_wen_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pb2, o_d=>id_rf_wen_Pax);
  u_buf_id_rf_wen_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pax, o_d=>id_rf_wen_Pa0);
  u_buf_id_rf_wen_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pa0, o_d=>id_rf_wen_Pa1);
  u_buf_id_rf_wen_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pa1, o_d=>id_rf_wen_Pa1x);
  u_buf_id_rf_wen_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pa1x, o_d=>id_rf_wen_Pa2);
  rfwren_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_rfwren_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_rf_wen_Pa2, o_d=>id_rf_wen_Pa3(i));
  end generate;

  u_buf_rf_wraddr_Pax:generic_reg generic map(REG_NUM=>PaxLevel, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pb2, o_d=>rf_wraddr_Pax);
  u_buf_rf_wraddr_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pax, o_d=>rf_wraddr_Pa0);
  u_buf_rf_wraddr_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pa0, o_d=>rf_wraddr_Pa1);
  u_buf_rf_wraddr_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pa1, o_d=>rf_wraddr_Pa1x);
  u_buf_rf_wraddr_Pa2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pa1x, o_d=>rf_wraddr_Pa2);
  rfwraddr_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_rfwraddr_Pa3:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>RF_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>rf_wraddr_Pa2, o_d=>rf_wraddr_Pa3(i));
  end generate;
end generate;

-- sm
sm_buf_gen: if SM_EN = true generate
  u_buf_id_sm_set_rb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_sm_set_rb_0_Pb1, o_d=>id_sm_set_rb_0_Pb2);
  u_buf_id_sm_inc_rb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_rb_0_Pb1, o_d=>id_sm_inc_rb_0_Pb2);

  u_buf_id_rdsm_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rdsm_Pb1, o_d=>id_rdsm_Pb2);
  u_buf_id_rdsm_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rdsm_Pb2, o_d=>id_rdsm_Pa0);
  rdsm_buffer_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_rdsm_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_rdsm_Pa0, o_d=>id_rdsm_Pa1(i));
  end generate;

  SM_NOT_READONLY_GEN: if SM_READONLY = false generate
    u_buf_sm_wb_addr_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>SM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>sm_wb_addr_Pb2, o_d=>sm_wb_addr_Pa0);
    u_buf_sm_wb_addr_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>SM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>sm_wb_addr_Pa0, o_d=>sm_wb_addr_Pa1);
    u_buf_sm_wb_addr_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>SM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>sm_wb_addr_Pa1, o_d=>sm_wb_addr_Pa1x);
    u_buf_sm_wb_addr_Pa2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>SM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>sm_wb_addr_Pa1x, o_d=>sm_wb_addr_Pa2);
    u_buf_sm_wb_addr_Pa3:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>SM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>sm_wb_addr_Pa2, o_d=>sm_wb_addr_Pa3);

    u_buf_id_sm_set_wb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pb1, o_d=>id_sm_set_wb_0_Pb2);
    u_buf_id_sm_set_wb_0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pb2, o_d=>id_sm_set_wb_0_Pa0);
    u_buf_id_sm_set_wb_0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pa0, o_d=>id_sm_set_wb_0_Pa1);
    u_buf_id_sm_set_wb_0_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pa1, o_d=>id_sm_set_wb_0_Pa1x);
    u_buf_id_sm_set_wb_0_Pa2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pa1x, o_d=>id_sm_set_wb_0_Pa2);
    u_buf_id_sm_set_wb_0_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_set_wb_0_Pa2, o_d=>id_sm_set_wb_0_Pa3);

    u_buf_id_sm_inc_wb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pb1, o_d=>id_sm_inc_wb_0_Pb2);
    u_buf_id_sm_inc_wb_0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pb2, o_d=>id_sm_inc_wb_0_Pa0);
    u_buf_id_sm_inc_wb_0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pa0, o_d=>id_sm_inc_wb_0_Pa1);
    u_buf_id_sm_inc_wb_0_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pa1, o_d=>id_sm_inc_wb_0_Pa1x);
    u_buf_id_sm_inc_wb_0_Pa2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pa1x, o_d=>id_sm_inc_wb_0_Pa2);
    u_buf_id_sm_inc_wb_0_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_inc_wb_0_Pa2, o_d=>id_sm_inc_wb_0_Pa3);

    u_buf_id_sm_autoinc_rb_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_rb_Pb1, o_d=>id_sm_autoinc_rb_Pb2);

    u_buf_id_sm_autoinc_wb_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pb1, o_d=>id_sm_autoinc_wb_Pb2);
    u_buf_id_sm_autoinc_wb_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pb2, o_d=>id_sm_autoinc_wb_Pa0);
    u_buf_id_sm_autoinc_wb_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pa0, o_d=>id_sm_autoinc_wb_Pa1);
    u_buf_id_sm_autoinc_wb_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pa1, o_d=>id_sm_autoinc_wb_Pa1x);
    u_buf_id_sm_autoinc_wb_Pa2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pa1x, o_d=>id_sm_autoinc_wb_Pa2);
    u_buf_id_sm_autoinc_wb_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_autoinc_wb_Pa2, o_d=>id_sm_autoinc_wb_Pa3);

    u_buf_id_sm_wen_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pb1, o_d=>id_sm_wen_Pb2);
    u_buf_id_sm_wen_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pb2, o_d=>id_sm_wen_Pa0);
    u_buf_id_sm_wen_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pa0, o_d=>id_sm_wen_Pa1);
    u_buf_id_sm_wen_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pa1, o_d=>id_sm_wen_Pa1x);
    u_buf_id_sm_wen_Pa2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pa1x, o_d=>id_sm_wen_Pa2);
    u_buf_id_sm_wen_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_sm_wen_Pa2, o_d=>id_sm_wen_Pa3);
  end generate;
end generate;

-- dm
dm_buf_gen: if DM_EN = true generate
  u_buf_id_rddm0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rddm0_Pb1, o_d=>id_rddm0_Pb2);
  u_buf_id_rddm0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rddm0_Pb2, o_d=>id_rddm0_Pa0);
  rddm0_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_rddm0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_rddm0_Pa0, o_d=>id_rddm0_Pa1(i));
  end generate;

  u_buf_id_rddm1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rddm1_Pb1, o_d=>id_rddm1_Pb2);
  u_buf_id_rddm1_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_rddm1_Pb2, o_d=>id_rddm1_Pa0);
  rddm1_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_rddm1_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_rddm1_Pa0, o_d=>id_rddm1_Pa1(i));
  end generate;

  u_buf_id_dm_set_rb_m0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_rb_m0_Pb1, o_d=>id_dm_set_rb_m0_Pb2);
  u_buf_id_dm_set_rb_m1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_rb_m1_Pb1, o_d=>id_dm_set_rb_m1_Pb2);

  u_buf_id_dm_set_rb_n0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_rb_n0_Pb1, o_d=>id_dm_set_rb_n0_Pb2);
  u_buf_id_dm_set_rb_n1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_rb_n1_Pb1, o_d=>id_dm_set_rb_n1_Pb2);

  u_buf_id_dm_inc_rb_m0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_rb_m0_Pb1, o_d=>id_dm_inc_rb_m0_Pb2);
  u_buf_id_dm_inc_rb_m1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_rb_m1_Pb1, o_d=>id_dm_inc_rb_m1_Pb2);

  u_buf_id_dm_inc_rb_n0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_rb_n0_Pb1, o_d=>id_dm_inc_rb_n0_Pb2);
  u_buf_id_dm_inc_rb_n1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_rb_n1_Pb1, o_d=>id_dm_inc_rb_n1_Pb2);

  u_buf_id_dm_autoinc_rb_m_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_rb_m_Pb1, o_d=>id_dm_autoinc_rb_m_Pb2);

  u_buf_id_dm_autoinc_rb_n_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_rb_n_Pb1, o_d=>id_dm_autoinc_rb_n_Pb2);

  -- wofs
  u_buf_dm_wofs_Pax:generic_reg generic map(REG_NUM=>PaxLevel, REG_WIDTH=>constDMOffsetWidth)
    port map(clk=>clk, rst=>rst, i_d=>dm_wofs_addr_Pb2, o_d=>dm_wofs_addr_Pax);
  u_buf_dm_wofs_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>constDMOffsetWidth)
    port map(clk=>clk, rst=>rst, i_d=>dm_wofs_addr_Pax, o_d=>dm_wofs_addr_Pa0);
  u_buf_dm_wofs_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>constDMOffsetWidth)
    port map(clk=>clk, rst=>rst, i_d=>dm_wofs_addr_Pa0, o_d=>dm_wofs_addr_Pa1);
  u_buf_dm_wofs_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>constDMOffsetWidth)
    port map(clk=>clk, rst=>rst, i_d=>dm_wofs_addr_Pa1, o_d=>dm_wofs_addr_Pa1x);
  u_buf_dm_wofs_Pa2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>constDMOffsetWidth)
    port map(clk=>clk, rst=>rst, i_d=>dm_wofs_addr_Pa1x, o_d=>dm_wofs_addr_Pa2);

  -- wb_addr
  u_buf_dm_wb_Pax:generic_reg generic map(REG_NUM=>PaxLevel, REG_WIDTH=>DM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_addr_Pb2, o_d=>dm_wb_addr_Pax);
  u_buf_dm_wb_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_addr_Pax, o_d=>dm_wb_addr_Pa0);
  u_buf_dm_wb_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_addr_Pa0, o_d=>dm_wb_addr_Pa1);
  u_buf_dm_wb_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_addr_Pa1, o_d=>dm_wb_addr_Pa1x);
  u_buf_dm_wb_Pa2:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_addr_Pa1x, o_d=>dm_wb_addr_Pa2);

  -- wrdm
  u_buf_id_wrdm_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pb1, o_d=>id_wrdm_Pb2);
  u_buf_id_wrdm_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pb2, o_d=>id_wrdm_Pax);
  u_buf_id_wrdm_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pax, o_d=>id_wrdm_Pa0);
  u_buf_id_wrdm_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pa0, o_d=>id_wrdm_Pa1);
  u_buf_id_wrdm_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pa1, o_d=>id_wrdm_Pa1x);
  u_buf_id_wrdm_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pa1x, o_d=>id_wrdm_Pa2);
  dmwren_buffer_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_dmwren_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_wrdm_Pa2, o_d=>id_wrdm_Pa3(i));
  end generate;

  -- dm_wb_sel
  u_buf_dm_wb_sel_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_sel_Pb2, o_d=>dm_wb_sel_Pax);
  u_buf_dm_wb_sel_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_sel_Pax, o_d=>dm_wb_sel_Pa0);
  u_buf_dm_wb_sel_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_sel_Pa0, o_d=>dm_wb_sel_Pa1);
  u_buf_dm_wb_sel_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_sel_Pa1, o_d=>dm_wb_sel_Pa1x);
  u_buf_dm_wb_sel_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>dm_wb_sel_Pa1x, o_d=>dm_wb_sel_Pa2);

  -- dm_set_wb
  u_buf_id_dm_set_wb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pb1, o_d=>id_dm_set_wb_0_Pb2);
  u_buf_id_dm_set_wb_0_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pb2, o_d=>id_dm_set_wb_0_Pax);
  u_buf_id_dm_set_wb_0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pax, o_d=>id_dm_set_wb_0_Pa0);
  u_buf_id_dm_set_wb_0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pa0, o_d=>id_dm_set_wb_0_Pa1);
  u_buf_id_dm_set_wb_0_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pa1, o_d=>id_dm_set_wb_0_Pa1x);
  u_buf_id_dm_set_wb_0_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_0_Pa1x, o_d=>id_dm_set_wb_0_Pa2);

  u_buf_id_dm_set_wb_1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pb1, o_d=>id_dm_set_wb_1_Pb2);
  u_buf_id_dm_set_wb_1_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pb2, o_d=>id_dm_set_wb_1_Pax);
  u_buf_id_dm_set_wb_1_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pax, o_d=>id_dm_set_wb_1_Pa0);
  u_buf_id_dm_set_wb_1_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pa0, o_d=>id_dm_set_wb_1_Pa1);
  u_buf_id_dm_set_wb_1_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pa1, o_d=>id_dm_set_wb_1_Pa1x);
  u_buf_id_dm_set_wb_1_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_set_wb_1_Pa1x, o_d=>id_dm_set_wb_1_Pa2);

  -- dm_inc_wb
  u_buf_id_dm_inc_wb_0_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pb1, o_d=>id_dm_inc_wb_0_Pb2);
  u_buf_id_dm_inc_wb_0_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pb2, o_d=>id_dm_inc_wb_0_Pax);
  u_buf_id_dm_inc_wb_0_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pax, o_d=>id_dm_inc_wb_0_Pa0);
  u_buf_id_dm_inc_wb_0_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pa0, o_d=>id_dm_inc_wb_0_Pa1);
  u_buf_id_dm_inc_wb_0_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pa1, o_d=>id_dm_inc_wb_0_Pa1x);
  u_buf_id_dm_inc_wb_0_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_0_Pa1x, o_d=>id_dm_inc_wb_0_Pa2);

  u_buf_id_dm_inc_wb_1_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pb1, o_d=>id_dm_inc_wb_1_Pb2);
  u_buf_id_dm_inc_wb_1_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pb2, o_d=>id_dm_inc_wb_1_Pax);
  u_buf_id_dm_inc_wb_1_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pax, o_d=>id_dm_inc_wb_1_Pa0);
  u_buf_id_dm_inc_wb_1_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pa0, o_d=>id_dm_inc_wb_1_Pa1);
  u_buf_id_dm_inc_wb_1_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pa1, o_d=>id_dm_inc_wb_1_Pa1x);
  u_buf_id_dm_inc_wb_1_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_inc_wb_1_Pa1x, o_d=>id_dm_inc_wb_1_Pa2);

  -- dm_autoinc_wb
  u_buf_id_dm_autoinc_wb_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pb1, o_d=>id_dm_autoinc_wb_Pb2);
  u_buf_id_dm_autoinc_wb_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pb2, o_d=>id_dm_autoinc_wb_Pax);
  u_buf_id_dm_autoinc_wb_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pax, o_d=>id_dm_autoinc_wb_Pa0);
  u_buf_id_dm_autoinc_wb_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pa0, o_d=>id_dm_autoinc_wb_Pa1);
  u_buf_id_dm_autoinc_wb_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pa1, o_d=>id_dm_autoinc_wb_Pa1x);
  u_buf_id_dm_autoinc_wb_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_dm_autoinc_wb_Pa1x, o_d=>id_dm_autoinc_wb_Pa2);

  wb_addr_buf: for i in 0 to VLEN-1 generate
    u_buf_dm_wr_addr_Pa3:generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dm_wraddr_Pa2, o_d=>dm_wraddr_Pa3(i));
  end generate;
end generate;

data_gen_Pa1x: for i in 0 to VLEN-1 generate
  u_buf_src_a_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>CORE_DATA_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>src_a_muxout_Pa1(i), o_d=>src_a_Pa1x(i));
  u_buf_src_b_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>CORE_DATA_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>src_b_muxout_Pa1(i), o_d=>src_b_Pa1x(i));
  u_buf_src_c_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>CORE_DATA_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>src_c_muxout_Pa1(i), o_d=>src_c_Pa1x(i));
end generate;

-- alusra
buf_alusra_gen: if ALUSRA_EN = true generate
  u_buf_id_alusra_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pb1, o_d=>id_alusra_Pb2);
  u_buf_id_alusra_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pb2, o_d=>id_alusra_Pax);
  u_buf_id_alusra_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pax, o_d=>id_alusra_Pa0);
  u_buf_id_alusra_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pa0, o_d=>id_alusra_Pa1);
  u_buf_id_alusra_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pa1, o_d=>id_alusra_Pa1x);
  u_buf_id_alusra_Pa2:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pa1x, o_d=>id_alusra_Pa2);

  alusra_buf_repl_gen:  for i in 0 to VLEN-1 generate
    u_buf_id_alusra_Pa3:generic_reg1 generic map(REG_NUM=>1)
    port map(clk=>clk, rst=>rst, i_d=>id_alusra_Pa2, o_d=>id_alusra_Pa3(i));
  end generate;
end generate;

-- opmode
u_buf_id_opmode_Pb2:generic_reg generic map(REG_NUM=>PB2_DEPTH, REG_WIDTH=>7*OPM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_opmode_Pb1, o_d=>id_opmode_Pb2);
u_buf_id_opmode_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>7*OPM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_opmode_Pb2, o_d=>id_opmode_Pa0);
id_opmode_buf_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_id_opmode_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>7*OPM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_opmode_Pa0, o_d=>id_opmode_Pa1(i));
  u_buf_id_opmode_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>7*OPM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_opmode_Pa1(i), o_d=>id_opmode_Pa1x(i));
end generate;

u_buf_id_alumode_Pb2:generic_reg generic map(REG_NUM=>PB2_DEPTH, REG_WIDTH=>4*ALUM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_alumode_Pb1, o_d=>id_alumode_Pb2);
u_buf_id_alumode_Pa0:generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>4*ALUM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_alumode_Pb2, o_d=>id_alumode_Pa0);
id_alumode_buf_repl_gen: for i in 0 to VLEN-1 generate
  u_buf_id_alumode_Pa1:generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>4*ALUM_NUM)
    port map(clk=>clk, rst=>rst, i_d=>id_alumode_Pa0, o_d=>id_alumode_Pa1(i));
  u_buf_id_alumode_Pa1x:generic_reg generic map(REG_NUM=>PA1X_DEPTH, REG_WIDTH=>4*ALUM_NUM)
  port map(clk=>clk, rst=>rst, i_d=>id_alumode_Pa1(i), o_d=>id_alumode_Pa1x(i));
end generate;

ABS_PIPE_GEN: if ABSDIFF_EN = true generate
begin
  -- CA_absdiff
  u_buf_id_CA_absdiff_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pb1, o_d=>id_CA_absdiff_Pb2);
  u_buf_id_CA_absdiff_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
    port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pb2, o_d=>id_CA_absdiff_Pax);
  u_buf_id_CA_absdiff_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pax, o_d=>id_CA_absdiff_Pa0);
  u_buf_id_CA_absdiff_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pa0, o_d=>id_CA_absdiff_Pa1);
  u_buf_id_CA_absdiff_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
    port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pa1, o_d=>id_CA_absdiff_Pa1x);
  id_CA_absdiff_buf_repl_gen: for i in 0 to VLEN-1 generate
    u_buf_id_CA_absdiff_Pa2:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pa1x, o_d=>id_CA_absdiff_Pa2(i));
    u_buf_id_CA_absdiff_Pa3:generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_Pa2(i), o_d=>id_CA_absdiff_Pa3(i));
  end generate;

  ACCUM_GEN: if ABSDIFF_WITHACCUM = true generate
    u_buf_id_CA_absdiff_clr_Pb2:generic_reg1 generic map(REG_NUM=>PB2_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pb1, o_d=>id_CA_absdiff_clr_Pb2);
    u_buf_id_CA_absdiffclr_Pax:generic_reg1 generic map(REG_NUM=>PaxLevel)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pb2, o_d=>id_CA_absdiff_clr_Pax);
    u_buf_id_CA_absdiff_clr_Pa0:generic_reg1 generic map(REG_NUM=>PA0_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pax, o_d=>id_CA_absdiff_clr_Pa0);
    u_buf_id_CA_absdiff_clr_Pa1:generic_reg1 generic map(REG_NUM=>PA1_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pa0, o_d=>id_CA_absdiff_clr_Pa1);
    u_buf_id_CA_absdiff_clr_Pa1x:generic_reg1 generic map(REG_NUM=>PA1X_DEPTH)
      port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pa1, o_d=>id_CA_absdiff_clr_Pa1x);
    id_CA_absdiff_clr_buf_repl_gen: for i in 0 to VLEN-1 generate
      u_buf_id_CA_absdiff_clr_Pa2:generic_reg1 generic map(REG_NUM=>1)
        port map(clk=>clk, rst=>rst, i_d=>id_CA_absdiff_clr_Pa1x, o_d=>id_CA_absdiff_clr_Pa2(i));
    end generate;
  end generate;
end generate;

end structure;
