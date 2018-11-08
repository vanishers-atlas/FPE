library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.ssp_typedef.all;
use work.ssp_pkg.all;


entity spu_pc is
  generic (
    OPCODE_WIDTH  : integer := 6;
    PM_ADDR_WIDTH : integer := 10;
    PM_DATA_WIDTH : integer := 32;
    BRANCH_EN     : boolean := false;
    JMP_EN        : boolean := false;
    RPT_EN        : boolean := false;
    RPT_SPEC_1    : boolean := false;
    RPT_LEVELS    : integer := 4;
    RPT_CNT_LEN0  : integer := 5;
    RPT_CNT_LEN1  : integer := 5;
    RPT_CNT_LEN2  : integer := 4;
    RPT_CNT_LEN3  : integer := 4;
    RPT_CNT_LEN4  : integer := 4;
    RPT_BLK_LEN0  : integer := 5;
    RPT_BLK_LEN1  : integer := 3;
    RPT_BLK_LEN2  : integer := 3;
    RPT_BLK_LEN3  : integer := 2;
    RPT_BLK_LEN4  : integer := 3
  );
  port (
    clk           :  in std_logic;
    rst           :  in std_logic;
    i_en          :  in std_logic := '1';
    
    i_inst_data   :  in std_logic_vector(PM_DATA_WIDTH-OPCODE_WIDTH-1 downto 0);
    i_brc_taken   :  in std_logic;
    i_brc_addr    :  in std_logic_vector(PM_ADDR_WIDTH-1 downto 0);
  
    i_rpt_taken   :  in std_logic;
    
    i_jmp_taken   :  in std_logic;
    i_jmp_addr    :  in std_logic_vector(PM_ADDR_WIDTH-1 downto 0);
    o_pc          :  out std_logic_vector(PM_ADDR_WIDTH-1 downto 0)
  );  
end spu_pc;

architecture structure of spu_pc is

-- Type definition
type pc_type is array (0 to RPT_LEVELS-1) of std_logic_vector(PM_ADDR_WIDTH-1 downto 0);

signal pc_plus, pc_reg  : std_logic_vector(PM_ADDR_WIDTH-1 downto 0);

-- start and end instructions in repetition unit
signal rpt_bgn : pc_type := (others=>(others=>'0'));
signal rpt_end0   : std_logic_vector(RPT_BLK_LEN0-1 downto 0) := (others=>'0');
signal rpt_end1   : std_logic_vector(RPT_BLK_LEN1-1 downto 0) := (others=>'0');
signal rpt_end2   : std_logic_vector(RPT_BLK_LEN2-1 downto 0) := (others=>'0');
signal rpt_end3   : std_logic_vector(RPT_BLK_LEN3-1 downto 0) := (others=>'0');
signal rpt_end4   : std_logic_vector(RPT_BLK_LEN4-1 downto 0) := (others=>'0');
signal rpt_cnt0   : std_logic_vector(RPT_CNT_LEN0-1 downto 0) := (others=>'0');
signal rpt_cnt1   : std_logic_vector(RPT_CNT_LEN1-1 downto 0) := (others=>'0');
signal rpt_cnt2   : std_logic_vector(RPT_CNT_LEN2-1 downto 0) := (others=>'0');
signal rpt_cnt3   : std_logic_vector(RPT_CNT_LEN3-1 downto 0) := (others=>'0');
signal rpt_cnt4   : std_logic_vector(RPT_CNT_LEN4-1 downto 0) := (others=>'0');

signal jmp_addr : std_logic_vector(PM_ADDR_WIDTH-1 downto 0) := (others =>'0');
signal brc_addr : std_logic_vector(PM_ADDR_WIDTH-1 downto 0) := (others =>'0');

signal rpt_taken : std_logic := '0';
signal jmp_taken : std_logic := '0';
signal brc_taken : std_logic := '0';

begin

o_pc <= pc_reg;

-- Enable or disable PC. Actually, this only partially stops the PC, but the state
-- of RPT can not stopped completely. If i_en is deasserted at the end check
-- point in RPT AND it hasn't reach repeat count, the states can not be preserved.

-- NOTE i_en is asserted delay slot cycles after the can-cause-halt instruction issued.

pc_plus <= std_logic_vector(unsigned(pc_reg) + 1) when (i_en = '1') else pc_reg;
  
rpt_gen: if RPT_EN = true generate
  rpt_taken <= i_rpt_taken;
end generate;

RPT_NOTEN_GEN: if RPT_EN = false generate
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
        if jmp_taken = '1' then
          pc_reg <= jmp_addr;
        elsif brc_taken = '1' then
          pc_reg <= brc_addr;
        else
          pc_reg <= pc_plus;
        end if;
    end if;  
  end process;
end generate;

RPT_EN_GEN: if RPT_EN = true generate
-- A special case: level = 1, block number = 1
RPT1_b1: if RPT_SPEC_1 = true generate
  type state_type is (s_nml, s_rpt0);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
          pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
          pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if unsigned(rpt_cnt0) = 0 then
            state <= s_nml;
            pc_reg <= pc_plus;
          else            
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          end if;
      end case;
    end if;  
  end process;
end generate;

RPT1: if RPT_LEVELS = 1 and RPT_SPEC_1 = false generate
  type state_type is (s_nml, s_rpt0);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
            pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
            pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_bgn(0) <= pc_plus;
            rpt_end0 <= i_inst_data(10+RPT_BLK_LEN0-1 downto 10);
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if unsigned(rpt_cnt0) = 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            state <= s_nml;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt0) /= 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            pc_reg <= rpt_bgn(0);
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          else
            pc_reg <= pc_plus;
          end if;
      end case;
    end if;  
  end process;
end generate;

RPT2: if RPT_LEVELS = 2 generate  
  type state_type is (s_nml, s_rpt0,s_rpt1);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
            pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
            pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_bgn(0) <= pc_plus;
            rpt_end0 <= i_inst_data(10+RPT_BLK_LEN0-1 downto 10);
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if rpt_taken = '1' then
            state <= s_rpt1;
            pc_reg <= pc_plus;          
            rpt_bgn(1) <= pc_plus;
            rpt_end1 <= i_inst_data(10+RPT_BLK_LEN1-1 downto 10);
            rpt_cnt1 <= i_inst_data(RPT_CNT_LEN1-1 downto 0);
          elsif unsigned(rpt_cnt0) = 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            state <= s_nml;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt0) /= 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            pc_reg <= rpt_bgn(0);
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt1 =>
          if unsigned(rpt_cnt1) = 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            state <= s_rpt0;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt1) /= 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            pc_reg <= rpt_bgn(1);
            rpt_cnt1 <= std_logic_vector(unsigned(rpt_cnt1) - 1);
          else
            pc_reg <= pc_plus;
          end if;        
      end case;
    end if;  
  end process;
end generate;

RPT3: if RPT_LEVELS = 3 generate
  type state_type is (s_nml, s_rpt0,s_rpt1,s_rpt2);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
            pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
            pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_bgn(0) <= pc_plus;
            rpt_end0 <= i_inst_data(10+RPT_BLK_LEN0-1 downto 10);
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if rpt_taken = '1' then
            state <= s_rpt1;
            pc_reg <= pc_plus;          
            rpt_bgn(1) <= pc_plus;
            rpt_end1 <= i_inst_data(10+RPT_BLK_LEN1-1 downto 10);
            rpt_cnt1 <= i_inst_data(RPT_CNT_LEN1-1 downto 0);
          elsif unsigned(rpt_cnt0) = 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            state <= s_nml;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt0) /= 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            pc_reg <= rpt_bgn(0);
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt1 =>
          if rpt_taken = '1' then
            state <= s_rpt2;
            pc_reg <= pc_plus;
            rpt_bgn(2) <= pc_plus;
            rpt_end2 <= i_inst_data(10+RPT_BLK_LEN2-1 downto 10);
            rpt_cnt2 <= i_inst_data(RPT_CNT_LEN2-1 downto 0);
          elsif unsigned(rpt_cnt1) = 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            state <= s_rpt0;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt1) /= 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            pc_reg <= rpt_bgn(1);
            rpt_cnt1 <= std_logic_vector(unsigned(rpt_cnt1) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt2 =>
          if unsigned(rpt_cnt2) = 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            state <= s_rpt1;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt2) /= 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            pc_reg <= rpt_bgn(2);
            rpt_cnt2 <= std_logic_vector(unsigned(rpt_cnt2) - 1);
          else
            pc_reg <= pc_plus;
          end if;
      end case;
    end if;  
  end process;
end generate;

RPT4: if RPT_LEVELS = 4 generate
  type state_type is (s_nml, s_rpt0,s_rpt1,s_rpt2,s_rpt3);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
            pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
            pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_bgn(0) <= pc_plus;
            rpt_end0 <= i_inst_data(10+RPT_BLK_LEN0-1 downto 10);
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if rpt_taken = '1' then
            state <= s_rpt1;
            pc_reg <= pc_plus;          
            rpt_bgn(1) <= pc_plus;
            rpt_end1 <= i_inst_data(10+RPT_BLK_LEN1-1 downto 10);
            rpt_cnt1 <= i_inst_data(RPT_CNT_LEN1-1 downto 0);
          elsif unsigned(rpt_cnt0) = 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            state <= s_nml;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt0) /= 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            pc_reg <= rpt_bgn(0);
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt1 =>
          if rpt_taken = '1' then
            state <= s_rpt2;
            pc_reg <= pc_plus;
            rpt_bgn(2) <= pc_plus;
            rpt_end2 <= i_inst_data(10+RPT_BLK_LEN2-1 downto 10);
            rpt_cnt2 <= i_inst_data(RPT_CNT_LEN2-1 downto 0);
          elsif unsigned(rpt_cnt1) = 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            state <= s_rpt0;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt1) /= 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            pc_reg <= rpt_bgn(1);
            rpt_cnt1 <= std_logic_vector(unsigned(rpt_cnt1) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt2 =>
          if rpt_taken = '1' then
            state <= s_rpt3;
            pc_reg <= pc_plus;
            rpt_bgn(3) <= pc_plus;
            rpt_end3 <= i_inst_data(10+RPT_BLK_LEN3-1 downto 10);
            rpt_cnt3 <= i_inst_data(RPT_CNT_LEN3-1 downto 0);
          elsif unsigned(rpt_cnt2) = 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            state <= s_rpt1;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt2) /= 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            pc_reg <= rpt_bgn(2);
            rpt_cnt2 <= std_logic_vector(unsigned(rpt_cnt2) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt3 =>
          if unsigned(rpt_cnt3) = 0 and rpt_end3 = pc_reg(RPT_BLK_LEN3-1 downto 0) then
            state <= s_rpt2;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt3) /= 0 and rpt_end3 = pc_reg(RPT_BLK_LEN3-1 downto 0) then
            pc_reg <= rpt_bgn(3);
            rpt_cnt3 <= std_logic_vector(unsigned(rpt_cnt3) - 1);
          else
            pc_reg <= pc_plus;
          end if;
      end case;
    end if;  
  end process;
end generate;

RPT5: if RPT_LEVELS = 5 generate
  type state_type is (s_nml, s_rpt0,s_rpt1,s_rpt2,s_rpt3,s_rpt4);
  signal state: state_type;
begin
  fsm: process(clk, rst)
  begin
    if rst = '1' then
      pc_reg <= (others=>'0');
    elsif clk'event and clk = '1' then
      case state is
        when s_nml => 
          if jmp_taken = '1' then
            pc_reg <= jmp_addr;
          elsif brc_taken = '1' then
            pc_reg <= brc_addr;
          elsif rpt_taken = '1' then
            state <= s_rpt0;
            rpt_bgn(0) <= pc_plus;
            rpt_end0 <= i_inst_data(10+RPT_BLK_LEN0-1 downto 10);
            rpt_cnt0 <= i_inst_data(RPT_CNT_LEN0-1 downto 0);
            pc_reg <= pc_plus;
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt0 =>
          if rpt_taken = '1' then
            state <= s_rpt1;
            pc_reg <= pc_plus;          
            rpt_bgn(1) <= pc_plus;
            rpt_end1 <= i_inst_data(10+RPT_BLK_LEN1-1 downto 10);
            rpt_cnt1 <= i_inst_data(RPT_CNT_LEN1-1 downto 0);
          elsif unsigned(rpt_cnt0) = 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            state <= s_nml;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt0) /= 0 and rpt_end0 = pc_reg(RPT_BLK_LEN0-1 downto 0) then
            pc_reg <= rpt_bgn(0);
            rpt_cnt0 <= std_logic_vector(unsigned(rpt_cnt0) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt1 =>
          if rpt_taken = '1' then
            state <= s_rpt2;
            pc_reg <= pc_plus;
            rpt_bgn(2) <= pc_plus;
            rpt_end2 <= i_inst_data(10+RPT_BLK_LEN2-1 downto 10);
            rpt_cnt2 <= i_inst_data(RPT_CNT_LEN2-1 downto 0);
          elsif unsigned(rpt_cnt1) = 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            state <= s_rpt0;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt1) /= 0 and rpt_end1 = pc_reg(RPT_BLK_LEN1-1 downto 0) then
            pc_reg <= rpt_bgn(1);
            rpt_cnt1 <= std_logic_vector(unsigned(rpt_cnt1) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt2 =>
          if rpt_taken = '1' then
            state <= s_rpt3;
            pc_reg <= pc_plus;
            rpt_bgn(3) <= pc_plus;
            rpt_end3 <= i_inst_data(10+RPT_BLK_LEN3-1 downto 10);
            rpt_cnt3 <= i_inst_data(RPT_CNT_LEN3-1 downto 0);
          elsif unsigned(rpt_cnt2) = 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            state <= s_rpt1;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt2) /= 0 and rpt_end2 = pc_reg(RPT_BLK_LEN2-1 downto 0) then
            pc_reg <= rpt_bgn(2);
            rpt_cnt2 <= std_logic_vector(unsigned(rpt_cnt2) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt3 =>
          if rpt_taken = '1' then
            state <= s_rpt4;
            pc_reg <= pc_plus;
            rpt_bgn(4) <= pc_plus;
            rpt_end4 <= i_inst_data(10+RPT_BLK_LEN4-1 downto 10);
            rpt_cnt4 <= i_inst_data(RPT_CNT_LEN4-1 downto 0);
          elsif unsigned(rpt_cnt3) = 0 and rpt_end3 = pc_reg(RPT_BLK_LEN3-1 downto 0) then
            state <= s_rpt2;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt3) /= 0 and rpt_end3 = pc_reg(RPT_BLK_LEN3-1 downto 0) then
            pc_reg <= rpt_bgn(3);
            rpt_cnt3 <= std_logic_vector(unsigned(rpt_cnt3) - 1);
          else
            pc_reg <= pc_plus;
          end if;
        when s_rpt4 =>
          if unsigned(rpt_cnt4) = 0 and rpt_end4 = pc_reg(RPT_BLK_LEN4-1 downto 0) then
            state <= s_rpt3;
            pc_reg <= pc_plus;
          elsif unsigned(rpt_cnt4) /= 0 and rpt_end4 = pc_reg(RPT_BLK_LEN4-1 downto 0) then
            pc_reg <= rpt_bgn(4);
            rpt_cnt4 <= std_logic_vector(unsigned(rpt_cnt4) - 1);
          else
            pc_reg <= pc_plus;
          end if;
      end case;
    end if;  
  end process;
end generate;
end generate;

branch_gen:
if BRANCH_EN = true generate
 brc_taken <= i_brc_taken;
 brc_addr <= i_brc_addr;
end generate;

jmp_gen:
if JMP_EN = true generate
 jmp_taken <= i_jmp_taken;
 jmp_addr <= i_jmp_addr;
end generate;

end structure;