library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
library unisim;
use unisim.vcomponents.all; -- include for Xilinx primitives (DSP slices)
library work;
use work.ssp_pkg.all;

entity spu_ex is
generic(
  DATA_WIDTH : integer := 16; -- Real or Imag width
  CORE_DATA_WIDTH : integer := 16; -- Real + Imag width
  DATA_TYPE  : integer := 1;
  SLICE_NUM  : integer := 1;
  OPM_NUM    : integer   := 1;
  ALUM_NUM   : integer   := 1;
  MULREG_EN  : boolean  := false;
  FRAC_BITS  : integer := 0;
  MASK_EN    : boolean := false;
  ALUSRA_VAL : integer := 1;
  BRANCH_EN  : boolean := false
);
port (
  clk, rst   : in  std_logic;
  i_opmode   : in  std_logic_vector(7*OPM_NUM-1 downto 0);
  i_alumode  : in  std_logic_vector(4*ALUM_NUM-1 downto 0);
  i_src_a    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_src_b    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  i_src_c    : in  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  o_sign : out std_logic;
  o_zero : out std_logic;
  o_dsp48_result: out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  o_dsp48sra_result: out  std_logic_vector(CORE_DATA_WIDTH-1 downto 0)
);
end spu_ex;

architecture structure of spu_ex is
-- Help functions
function setUseMUL return string is
  constant UseMUL : string := "MULT";
  constant UseMULS : string := "MULT_S";
begin
  if MULREG_EN = true then
    return UseMULS;
  else
    return UseMUL;
  end if;
end function setUseMUL;

function setMREG return integer is
begin
  if MULREG_EN = true then
    return 1;
  else
    return 0;
  end if;
end function setMREG;

-- Function for setting AREG and BREG for complex ALU
function setABREG return integer is
begin
  if MULREG_EN = true then
    return 2;
  else
    return 1;
  end if;
end function setABREG;

-- Function for setting OPMODE and ALUMODE for complex ALU
function setOP_ALUREG return integer is
begin
  if MULREG_EN = true then
    return 1;
  else
    return 0;
  end if;
end function setOP_ALUREG;

function setPatDectect return string is
  constant NoPD : string := "NO_PATDET";
  constant UsePD : string := "PATDET";
begin
  if BRANCH_EN = true or MASK_EN = true then
    return UsePD;
  else
    return NoPD;
  end if;
end function setPatDectect;

--DSP48E component
component DSP48E -- Declare component generics and ports
  generic
  (
    ACASCREG : integer := 1; -- Number of pipeline registers between  A/ACIN input and ACOUT output, 0, 1, or 2
    ALUMODEREG : integer := 1; -- Number of pipeline registers on ALUMODE input, 0 or 1
    AREG : integer := 1;    -- Number of pipeline registers on the A input, 0, 1 or 2
    AUTORESET_PATTERN_DETECT : boolean := FALSE;-- Auto-reset upon pattern detect, TRUE or FALSE
    AUTORESET_PATTERN_DETECT_OPTINV : STRING := "MATCH";-- Reset if "MATCH" or "NOMATCH"
    A_INPUT : STRING := "DIRECT"; -- Selects A input used, "DIRECT" (A port) or "CASCADE" (ACIN port)
    BCASCREG : integer := 1;   -- Number of pipeline registers between B/BCIN input and BCOUT output, 0, 1, or 2
    BREG : integer := 1;      -- Number of pipeline registers on the B input, 0, 1 or 2
    B_INPUT : STRING := "DIRECT"; -- Selects B input used, "DIRECT" (B port) or "CASCADE" (BCIN port)
    CARRYINREG : integer := 1;   -- Number of pipeline registers for the CARRYIN input, 0 or 1
    CARRYINSELREG : integer := 1;  -- Number of pipeline registers for the CARRYINSEL input, 0 or 1
    CREG : integer := 1;          -- Number of pipeline registers on the C input, 0 or 1
    MASK : bit_vector := X"000000000000";  -- 48-bit Mask value for pattern detect
    MREG : integer := 1;                 -- Number of multiplier pipeline registers, 0 or 1  
    MULTCARRYINREG : integer := 1;      -- Number of pipeline registers for multiplier carry in bit, 0 or 1     
    OPMODEREG : integer :=1;            -- Number of pipeline registers on OPMODE input, 0 or 1
    PATTERN : bit_vector := X"000000000000";  -- 48-bit Pattern match for pattern detect
    PREG : integer := 1;                    -- Number of pipeline registers on the P output, 0 or 1             
    SEL_MASK : STRING := "MASK";            -- Select mask value between the "MASK" value or the value on the "C" port
    SEL_PATTERN : STRING := "PATTERN";      -- Select pattern value between the "PATTERN" value or the value on the "C" port
    SEL_ROUNDING_MASK : STRING := "SEL_MASK"; -- "SEL_MASK", "MODE1", "MODE2" 
    USE_MULT : STRING := "MULT_S";            -- Select multiplier usage, "MULT" (MREG => 0), -- "MULT_S" (MREG => 1), "NONE" (not using multiplier) 
    USE_PATTERN_DETECT : STRING := "NO_PATDET";  -- Enable pattern detect, "PATDET", "NO_PATDET"  
    USE_SIMD : STRING := "ONE48"                -- SIMD selection, "ONE48", "TWO24", "FOUR12"
  );
  port
  (
    ACOUT : out std_logic_vector(29 downto 0); -- 30-bit A port cascade output
    BCOUT : out std_logic_vector(17 downto 0); -- 18-bit B port cascade output
    CARRYCASCOUT : out STD_ULOGIC;             -- 1-bit cascade carry output
    CARRYOUT : out std_logic_vector(3 downto 0); -- 4-bit carry output
    MULTSIGNOUT : out STD_ULOGIC;               -- 1-bit multiplier sign cascade output  
    OVERFLOW : out STD_ULOGIC;                  -- 1-bit overflow in add/acc output
    P : out std_logic_vector(47 downto 0);      -- 48-bit output
    PATTERNBDETECT : out STD_ULOGIC;            -- 1-bit active high pattern bar detect output
    PATTERNDETECT : out STD_ULOGIC;             -- 1-bit active high pattern detect output
    PCOUT : out std_logic_vector(47 downto 0);  -- 48-bit cascade output
    UNDERFLOW : out STD_ULOGIC;                 -- 1-bit active high underflow in add/acc output
    A : in std_logic_vector(29 downto 0);       -- 30-bit A data input
    ACIN : in std_logic_vector(29 downto 0) := (others => '0');-- 30-bit A cascade data input 
    ALUMODE : in std_logic_vector(3 downto 0);   -- 4-bit ALU control input   
    B : in std_logic_vector(17 downto 0);       -- 18-bit B data input
    BCIN : in std_logic_vector(17 downto 0) := (others => '0'); -- 18-bit B cascade input
    C : in std_logic_vector(47 downto 0);        -- 48-bit C data input
    CARRYCASCIN : in STD_ULOGIC :='0';           -- 1-bit cascade carry input
    CARRYIN : in STD_ULOGIC:='0';               -- 1-bit carry input signal
    CARRYINSEL : in std_logic_vector(2 downto 0):="000";  -- 3-bit carry select input
    CEA1 : in STD_ULOGIC:='1';                  -- 1-bit active high clock enable input for 1st stage A registers
    CEA2 : in STD_ULOGIC:='1';                  -- 1-bit active high clock enable input for 2nd stage A registers
    CEALUMODE : in STD_ULOGIC:='1';-- 1-bit active high clock enable input for ALUMODE registers
    CEB1 : in STD_ULOGIC:='1';   -- 1-bit active high clock enable input for 1st stage B registers
    CEB2 : in STD_ULOGIC:='1';   -- 1-bit active high clock enable input for 2nd stage B registers
    CEC : in STD_ULOGIC:='1';   -- 1-bit active high clock enable input for C registers
    CECARRYIN : in STD_ULOGIC:='1'; -- 1-bit active high clock enable input for CARRYIN register
    CECTRL : in STD_ULOGIC:='1';    -- 1-bit active high clock enable input for OPMODE and carry registers
    CEM : in STD_ULOGIC:='1';       -- 1-bit active high clock enable input for multiplier registers
    CEMULTCARRYIN : in STD_ULOGIC:='1'; -- 1-bit active high clock enable for multiplier carry in register
    CEP : in STD_ULOGIC:='1';         -- 1-bit active high clock enable input for P registers
    CLK : in STD_ULOGIC;            -- Clock input
    MULTSIGNIN : in STD_ULOGIC:='0';  -- 1-bit multiplier sign input
    OPMODE : in std_logic_vector(6 downto 0);  -- 7-bit operation mode input
    PCIN : in std_logic_vector(47 downto 0);    -- 48-bit P cascade input
    RSTA : in STD_ULOGIC:='0';              -- 1-bit reset input for A pipeline registers   
    RSTALLCARRYIN : in STD_ULOGIC:='0';     -- 1-bit reset input for carry pipeline registers
    RSTALUMODE : in STD_ULOGIC:='0';        -- 1-bit reset input for ALUMODE pipeline registers
    RSTB : in STD_ULOGIC:='0';           -- 1-bit reset input for ALUMODE pipeline registers     
    RSTC : in STD_ULOGIC:='0';     -- 1-bit reset input for C pipeline registers
    RSTCTRL : in STD_ULOGIC:='0';    -- 1-bit reset input for OPMODE pipeline registers
    RSTM : in STD_ULOGIC:='0';    -- 1-bit reset input for multiplier registers
    RSTP : in STD_ULOGIC  :='0'  -- 1-bit reset input for P pipeline registers
  );
end component;

  attribute BOX_TYPE of DSP48E : component is "BLACK_BOX";
  signal p_d      : std_ulogic;
  signal alusra_result : std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  signal alu_result : std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
  
  -- Register C when MREG=1
  signal src_c : std_logic_vector(CORE_DATA_WIDTH-1 downto 0);
begin

o_dsp48_result <= alu_result;
o_dsp48sra_result <= alusra_result;

---------------------------------  
-- check positive/negative/zero
---------------------------------
o_sign  <= alu_result(DATA_WIDTH-1);    
o_zero  <= p_d;

-- Register C when MREG=1
src_c_mreg_gen: if (MULREG_EN = true) generate
  u_buf_src_c_Pmreg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>CORE_DATA_WIDTH) 
    port map(clk=>clk, rst=>'0', i_d=>i_src_c, o_d=>src_c);
end generate;
no_src_c_mreg_gen: if MULREG_EN = false generate
  src_c <= i_src_c;
end generate;
 
---------------------------------   
-- Real fixed-point ALU
---------------------------------
REAL_16_GEN:
if (DATA_WIDTH = 16 and DATA_TYPE=1 and SLICE_NUM=1) generate
  signal a_do     : std_logic_vector (29 downto 0);
  signal b_do    : std_logic_vector (17 downto 0);
  signal c_do    : std_logic_vector (47 downto 0);
  signal opmode_do  : std_logic_vector (6 downto 0);
  signal alumode_do  : std_logic_vector (3 downto 0);
  signal p_0      : std_logic_vector (47 downto 0);
begin
  a_do <= (29 downto DATA_WIDTH=>i_src_a(DATA_WIDTH-1)) & i_src_a;
  
  b_do <= (17 downto DATA_WIDTH=>i_src_b(DATA_WIDTH-1)) & i_src_b;    
  
  F0: if FRAC_BITS = 0 generate
  c_do <= (47 downto (DATA_WIDTH+FRAC_BITS)=> src_c(DATA_WIDTH-1)) & src_c(DATA_WIDTH-1 downto 0);
  end generate;
  F1: if FRAC_BITS > 0 generate
  c_do <= (47 downto (DATA_WIDTH+FRAC_BITS)=> src_c(DATA_WIDTH-1)) & src_c(DATA_WIDTH-1 downto 0) & (FRAC_BITS-1 downto 0=>'0');
  end generate;
  
  -- Register OPMODE, ALUMODE when MREG=1
  opmode_alumode_mreg_gen: if MULREG_EN = true generate
    u_buf_opmode_Pmreg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>i_opmode, o_d=>opmode_do);
    u_buf_alumode_Pmreg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>i_alumode, o_d=>alumode_do);
  end generate;
  no_opmode_alumode_mreg_gen: if MULREG_EN = false generate
    opmode_do <= i_opmode;
    alumode_do <= i_alumode;
  end generate;
  
  u_slice0 : DSP48E
    generic map (AREG=>1,BREG=>1,CREG=>1, MREG=>setMREG, USE_MULT=>setUseMUL, OPMODEREG=>1, ALUMODEREG=>1, PREG=> 1, 
                 CARRYINREG=>1, USE_PATTERN_DETECT=>setPatDectect)
    port map (A=>a_do, B=>b_do, C=>c_do, P=>p_0, CARRYIN=>'0', ALUMODE=>alumode_do, OPMODE=>opmode_do, CEA1=>'0', CEB1=>'0',
    CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, PCIN =>(others=>'0'), PATTERNDETECT=>p_d);  
  
  alu_result <= p_0(DATA_WIDTH+FRAC_BITS-1 downto FRAC_BITS);
  alusra_result <= (DATA_WIDTH-1 downto DATA_WIDTH-ALUSRA_VAL => alu_result(DATA_WIDTH-1)) 
    & alu_result(DATA_WIDTH-1 downto ALUSRA_VAL);
end generate;

-- REAL 32 only supports integer operation now! If want fixed-point support, we need
-- an extra DSP48.
REAL_32_4_GEN:
if (DATA_WIDTH = 32 and DATA_TYPE=1 and SLICE_NUM=4) generate
  signal opmode_3_r0, opmode_3_r1, opmode_3_r2 : std_logic_vector(6 downto 0);
  signal alumode_3_r0, alumode_3_r1, alumode_3_r2 : std_logic_vector(3 downto 0);
  signal al, bl : std_logic_vector(16 downto 0);
  signal ah, bh : std_logic_vector(14 downto 0);
  signal a0_sext, a1_sext, a2_sext, a3_sext : std_logic_vector(29 downto 0);
  signal b0_sext, b1_sext, b2_sext, b3_sext : std_logic_vector(17 downto 0);
  signal c3_sext : std_logic_vector(47 downto 0);
  signal p_0, pcout_0, pcout_1, p_2, p_3 : std_logic_vector(47 downto 0);
  signal p_0_r0, p_0_r1 : std_logic_vector(47 downto 0);
  signal axb    : std_logic_vector(31 downto 0);
  signal src_c_r0, src_c_r1, src_c_r2 : std_logic_vector(31 downto 0);
begin
  al <= i_src_a(16 downto 0);
  ah <= i_src_a(31 downto 17);
  bl <= i_src_b(16 downto 0);
  bh <= i_src_b(31 downto 17);
  
  u_buf_opmode_Pax:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>i_opmode, o_d=>opmode_3_r0);
  u_buf_opmode_Paxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>opmode_3_r0, o_d=>opmode_3_r1);
  u_buf_opmode_Paxxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>opmode_3_r1, o_d=>opmode_3_r2);
    
  u_buf_alumode_Pax:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>i_alumode, o_d=>alumode_3_r0);
  u_buf_alumode_Paxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_3_r0, o_d=>alumode_3_r1);
  u_buf_alumode_Paxxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_3_r1, o_d=>alumode_3_r2);
  
  u_buf_src_c_Pax:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>CORE_DATA_WIDTH) 
    port map(clk=>clk, rst=>'0', i_d=>src_c, o_d=>src_c_r0);
  u_buf_src_c_Paxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>CORE_DATA_WIDTH) 
    port map(clk=>clk, rst=>'0', i_d=>src_c_r0, o_d=>src_c_r1);
  u_buf_src_c_Paxxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>CORE_DATA_WIDTH) 
    port map(clk=>clk, rst=>'0', i_d=>src_c_r1, o_d=>src_c_r2);
  
  a0_sext <= (29 downto 17=>'0') & al;
  b0_sext <= '0' & bl;
  
  u_buf_p_0_Paxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>48) 
    port map(clk=>clk, rst=>'0', i_d=>p_0, o_d=>p_0_r0);
  u_buf_p_0_Paxxx:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>48) 
    port map(clk=>clk, rst=>'0', i_d=>p_0_r0, o_d=>p_0_r1);
  
  a1_sext <= (29 downto 15=>ah(14)) & ah;
  b1_sext <= '0' & bl;
  
  a2_sext <= (29 downto 17=>'0') & al;
  b2_sext <= (17 downto 15=>bh(14)) & bh;
  
  axb <= p_2(14 downto 0) & p_0_r1(16 downto 0);
  
  -- No need to use upper bits when in integer mode, so here 0-extend.
  a3_sext <= (29 downto 14=>'0') & axb(31 downto 18);
  b3_sext <= axb(17 downto 0);
--    c3_sext <= (47 downto (32+FRAC_BITS)=> src_c_r2(31)) & src_c_r2(31 downto 0) & (FRAC_BITS-1 downto 0=>'0');
  c3_sext <= (47 downto 32=> '0') & src_c_r2(31 downto 0);
  
  -- AL*BL
  slice0: DSP48E 
    generic map(AREG=>1,BREG=>1,CREG=>1, MREG=>0, USE_MULT=>"MULT", OPMODEREG=>1, ALUMODEREG=>1,PREG=>1)
    port map(A=>a0_sext, B=>b0_sext, C=>(others=>'0'), P=>p_0, PCOUT=>pcout_0,
             ALUMODE=>"0000",OPMODE=>"0000101",CEA1=>'0', CEB1=>'0',
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => (others=>'0'));
  -- AH*BL
  slice1: DSP48E 
    generic map(AREG=>1,BREG=>1,CREG=>1, MREG=>1, OPMODEREG=>1, ALUMODEREG=>1, PREG=> 1)
    port map(A=>a1_sext, B=>b1_sext, C=>(others=>'0'), PCOUT=>pcout_1,
             ALUMODE=>"0000",OPMODE=>"1010101", CEA1=>'0', CEB1=>'0',
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => pcout_0);
  -- AL*BH
  slice2: DSP48E 
    generic map(AREG=>2,BREG=>2,CREG=>1, MREG=>1, OPMODEREG=>1, ALUMODEREG=>1, PREG=>1)
    port map(A=>a2_sext, B=>b2_sext, C=>(others=>'0'), P=>p_2,
             ALUMODE=>"0000",OPMODE=>"0010101",
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => pcout_1);
  -- C+-A*B
  slice3: DSP48E
    generic map(AREG=>0,BREG=>0,ACASCREG=>0, BCASCREG=>0, CREG=>1, MREG=>0, USE_MULT=>"NONE", OPMODEREG=>1, ALUMODEREG=>1, PREG=>1)
    port map(A=>a3_sext, B=>b3_sext, C=>c3_sext, P=>p_3,
             ALUMODE=>alumode_3_r2,OPMODE=>opmode_3_r2, CEA1=>'0', CEB1=>'0',
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => (others=>'0'));
            
  alu_result <= p_3(32+FRAC_BITS-1 downto FRAC_BITS);
  
end generate;

CPLX16_4:
if (DATA_WIDTH = 16 and DATA_TYPE = 2 and SLICE_NUM = 4) generate
  signal p_0, p_1, p_2, p_3 : std_logic_vector(47 downto 0); --P_1 is the real part, P_3 is the imag part
  signal opmode_02, opmode_02_r,  opmode_13, opmode_13_r : std_logic_vector(6 downto 0);
  signal alumode_02, alumode_02_r, alumode_1, alumode_1_r, alumode_3, alumode_3_r : std_logic_vector(3 downto 0);
  signal a0_sext, a1_sext, a2_sext, a3_sext : std_logic_vector(29 downto 0);
  signal b0_sext, b1_sext, b2_sext, b3_sext : std_logic_vector(17 downto 0);
  signal c0_sext, c1_sext, c2_sext, c3_sext : std_logic_vector(47 downto 0);
  signal a_real, b_real, a_imag, b_imag, c_real, c_imag : std_logic_vector(DATA_WIDTH-1 downto 0);
begin

  opmode_02  <= i_opmode(13 downto 7);
  opmode_13  <= i_opmode(6 downto 0);
  alumode_02 <= i_alumode(11 downto 8);
  alumode_1 <= i_alumode(7 downto 4);
  alumode_3 <= i_alumode(3 downto 0);
  
  u_buf_opmode13_Pa2:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>opmode_13, o_d=>opmode_13_r);
  u_buf_alumode1_Pa2:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_1, o_d=>alumode_1_r);
  u_buf_alumode3_Pa2:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_3, o_d=>alumode_3_r);
 
  -- Register OPMODE, ALUMODE for upper DSP48Es when MREG=1
  opmode_alumode_mreg_gen: if MULREG_EN = true generate
    u_buf_opmode_Pmreg:spu_generic_reg generic map(REG_NUM=>2, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>opmode_02, o_d=>opmode_02_r);
    u_buf_alumode_Pmreg:spu_generic_reg generic map(REG_NUM=>2, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_02, o_d=>alumode_02_r);
  end generate;
  no_opmode_alumode_mreg_gen: if MULREG_EN = false generate
    u_buf_opmode_Pmreg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>7) 
    port map(clk=>clk, rst=>'0', i_d=>opmode_02, o_d=>opmode_02_r);
    u_buf_alumode_Pmreg:spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>4) 
    port map(clk=>clk, rst=>'0', i_d=>alumode_02, o_d=>alumode_02_r);
  end generate;

  a_imag<=i_src_a(2*DATA_WIDTH-1 downto DATA_WIDTH); 
  a_real<=i_src_a(DATA_WIDTH-1 downto 0);
  b_imag<=i_src_b(2*DATA_WIDTH-1 downto DATA_WIDTH);
  b_real<=i_src_b(DATA_WIDTH-1 downto 0);
  c_imag<=src_c(2*DATA_WIDTH-1 downto DATA_WIDTH);
  c_real<=src_c(DATA_WIDTH-1 downto 0);

  a0_sext<=(29 downto DATA_WIDTH=>a_real(DATA_WIDTH-1)) & a_real;
  b0_sext<=(17 downto DATA_WIDTH=>b_real(DATA_WIDTH-1)) & b_real;

  a1_sext<=(29 downto DATA_WIDTH=>a_imag(DATA_WIDTH-1)) & a_imag;
  b1_sext<=(17 downto DATA_WIDTH=>b_imag(DATA_WIDTH-1)) & b_imag;
  F0: if FRAC_BITS = 0 generate
    c1_sext<=(47 downto (DATA_WIDTH+FRAC_BITS)=> c_real(DATA_WIDTH-1)) & c_real(DATA_WIDTH-1 downto 0);
  end generate;
  F1: if FRAC_BITS > 0 generate
    c1_sext<=(47 downto (DATA_WIDTH+FRAC_BITS)=> c_real(DATA_WIDTH-1)) & c_real(DATA_WIDTH-1 downto 0) & (FRAC_BITS-1 downto 0=>'0');
  end generate;
  
  a2_sext<=(29 downto DATA_WIDTH=>a_real(DATA_WIDTH-1)) & a_real;
  b2_sext<=(17 downto DATA_WIDTH=>b_imag(DATA_WIDTH-1)) & b_imag;

  a3_sext<=(29 downto DATA_WIDTH=>a_imag(DATA_WIDTH-1)) & a_imag;
  b3_sext<=(17 downto DATA_WIDTH=>b_real(DATA_WIDTH-1)) & b_real;
  F2: if FRAC_BITS = 0 generate
    c3_sext<=(47 downto (DATA_WIDTH+FRAC_BITS)=> c_imag(DATA_WIDTH-1)) & c_imag(DATA_WIDTH-1 downto 0);
  end generate;
  F3: if FRAC_BITS > 0 generate
    c3_sext<=(47 downto (DATA_WIDTH+FRAC_BITS)=> c_imag(DATA_WIDTH-1)) & c_imag(DATA_WIDTH-1 downto 0) & (FRAC_BITS-1 downto 0=>'0');
  end generate;
  
  slice0: DSP48E 
    generic map(AREG=>setABREG,BREG=>setABREG,CREG=>1, MREG=>1, OPMODEREG=>1, ALUMODEREG=>1,PREG=>1)
    port map(A=>a0_sext, B=>b0_sext, C=>(others=>'0'), P=>p_0,
             ALUMODE=>alumode_02_r,OPMODE=>opmode_02_r,
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => p_1);
  -- Do not use CREG and MREG to reduce one pipeline
  slice1: DSP48E 
    generic map(AREG=>1,BREG=>1,CREG=>1, MREG=>setMREG, USE_MULT=>setUseMUL, OPMODEREG=>setOP_ALUREG, ALUMODEREG=>setOP_ALUREG, PREG=> 1)
    port map(A=>a1_sext, B=>b1_sext, C=>c1_sext, PCOUT=>p_1,
             ALUMODE=>alumode_1_r,OPMODE=>opmode_13_r, CEA1=>'0', CEB1=>'0',
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => (others=>'0'));
  slice2: DSP48E 
    generic map(AREG=>setABREG,BREG=>setABREG,CREG=>1, MREG=>1, OPMODEREG=>1, ALUMODEREG=>1, PREG=> 1)
    port map(A=>a2_sext, B=>b2_sext, C=>(others=>'0'), P=>p_2,
             ALUMODE=>alumode_02_r,OPMODE=>opmode_02_r, 
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => p_3);
  -- Do not use CREG and MREG to reduce one pipeline
  slice3: DSP48E
    generic map(AREG=>1,BREG=>1,CREG=>1, MREG=>setMREG, USE_MULT=>setUseMUL, OPMODEREG=>setOP_ALUREG, ALUMODEREG=>setOP_ALUREG, PREG=> 1)
    port map(A=>a3_sext, B=>b3_sext, C=>c3_sext, PCOUT=>p_3,
             ALUMODE=>alumode_3_r,OPMODE=>opmode_13_r, CEA1=>'0', CEB1=>'0', 
             CLK =>clk, RSTA=>rst, RSTB=>rst, RSTC=>rst, RSTP=>rst, RSTM=>rst, 
             PCIN => (others=>'0'));
            
  alu_result <= p_2(DATA_WIDTH+FRAC_BITS-1 downto FRAC_BITS) & p_0(DATA_WIDTH+FRAC_BITS-1 downto FRAC_BITS);
  alusra_result <= (DATA_WIDTH+FRAC_BITS-1 downto DATA_WIDTH+FRAC_BITS-ALUSRA_VAL => p_2(DATA_WIDTH+FRAC_BITS-1))
                   & p_2(DATA_WIDTH+FRAC_BITS-1 downto FRAC_BITS+ALUSRA_VAL) &
                   (DATA_WIDTH+FRAC_BITS-1 downto DATA_WIDTH+FRAC_BITS-ALUSRA_VAL => p_0(DATA_WIDTH+FRAC_BITS-1))
                   & p_0(DATA_WIDTH+FRAC_BITS-1 downto FRAC_BITS+ALUSRA_VAL);
end generate;


end structure;