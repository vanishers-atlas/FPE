  library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.math_real.all;

library unisim;
use unisim.vcomponents.all;
library work;
use work.ssp_pkg.all;

-- Set DM_OFFSET_WIDTH with caution.

entity spu_sau is
  generic (
    DM_OFFSET_WIDTH      : integer:= 5;
    DM_ADDR_WIDTH        : integer:= 10;
    DM_DATA_WIDTH        : integer:= 16;
    DM_WB_NUM            : integer:= 1;
    DM_RB_M_NUM          : integer:= 1;
    DM_RB_N_NUM          : integer:= 1;
    
    -- The initial value of base
    DM_RB_M_INITIAL0      : integer:= 0;
    DM_RB_M_INITIAL1      : integer:= 0;
    DM_RB_N_INITIAL0      : integer:= 0;
    DM_RB_N_INITIAL1      : integer:= 0;
    DM_WB_INITIAL0        : integer:= 0;
    DM_WB_INITIAL1        : integer:= 0;
    
    DM_RB_M_AUTOINC_SIZE0 : integer:= 1;
    DM_RB_M_AUTOINC_SIZE1 : integer:= 1;
    DM_RB_N_AUTOINC_SIZE0 : integer:= 1;
    DM_RB_N_AUTOINC_SIZE1 : integer:= 1;
    DM_WB_AUTOINC_SIZE0   : integer:= 1;
    DM_WB_AUTOINC_SIZE1   : integer:= 1;
    
    DM_OFFSET_EN          : boolean:= false;
    DM_RB_M_SET_EN0       : boolean:= false;
    DM_RB_M_SET_EN1       : boolean:= false;
    DM_RB_N_SET_EN0       : boolean:= false;
    DM_RB_N_SET_EN1       : boolean:= false;
    DM_WB_SET_EN0         : boolean:= false;
    DM_WB_SET_EN1         : boolean:= false;
    DM_RB_M_AUTOINC_EN0   : boolean:= false;    
    DM_RB_M_AUTOINC_EN1   : boolean:= false;
    DM_RB_N_AUTOINC_EN0   : boolean:= false;
    DM_RB_N_AUTOINC_EN1   : boolean:= false;
    DM_WB_AUTOINC_EN0     : boolean:= false;
    DM_WB_AUTOINC_EN1     : boolean:= false;
    DM_RB_M_INC_EN0       : boolean:= false;
    DM_RB_M_INC_EN1       : boolean:= false;
    DM_RB_N_INC_EN0       : boolean:= false;
    DM_RB_N_INC_EN1       : boolean:= false;
    DM_WB_INC_EN0         : boolean:= false;
    DM_WB_INC_EN1         : boolean:= false
  );
  port (
    clk    :  in std_logic := '0';
    
    i_dm_rd_ofs_m     :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0) := (others => '0');
    i_dm_rd_ofs_n     :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0) := (others => '0');
    i_dm_rd_bs        :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others => '0');
    i_dm_set_rb_m0    :  in std_logic := '0';
    i_dm_set_rb_m1    :  in std_logic := '0';
    i_dm_set_rb_n0    :  in std_logic := '0';
    i_dm_set_rb_n1    :  in std_logic := '0';
    i_dm_inc_rb_m0    :  in std_logic := '0';
    i_dm_inc_rb_m1    :  in std_logic := '0';
    i_dm_inc_rb_n0    :  in std_logic := '0';
    i_dm_inc_rb_n1    :  in std_logic := '0';
    i_dm_autoinc_rb_m :  in std_logic := '0';
    i_dm_autoinc_rb_n :  in std_logic := '0';
    i_dm_rb_sel_m     :  in std_logic := '0';
    i_dm_rb_sel_n     :  in std_logic := '0';
    
    i_dm_wr_ofs       :  in std_logic_vector (DM_OFFSET_WIDTH-1 downto 0) := (others => '0');
    i_dm_wr_bs        :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others => '0');
    i_dm_set_wb_0      :  in std_logic := '0';
    i_dm_set_wb_1      :  in std_logic := '0';
    i_dm_inc_wb_0      :  in std_logic := '0';
    i_dm_inc_wb_1      :  in std_logic := '0';
    i_dm_autoinc_wb   :  in std_logic := '0';
    i_dm_wb_sel       :  in std_logic := '0';
    
    o_dm_rd_addr_0    :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others => '0');
    o_dm_rd_addr_1    :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others => '0');
    o_dm_wr_addr      :  out std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others => '0')
  );
end spu_sau;

architecture structure of spu_sau is
  signal dm_rd_addr_m, dm_rd_addr_n, dm_wr_addr : std_logic_vector (DM_ADDR_WIDTH-1 downto 0) := (others=>'0');
  signal dm_set_rb_m0, dm_set_rb_m1, dm_set_rb_n0, dm_set_rb_n1, dm_set_wb0, dm_set_wb1 :  std_logic := '0';
  signal dm_inc_rb_m0, dm_inc_rb_m1, dm_inc_rb_n0, dm_inc_rb_n1, dm_inc_wb0, dm_inc_wb1 :  std_logic := '0';
  signal dm_autoinc_rb_m0, dm_autoinc_rb_m1, dm_autoinc_rb_n0, dm_autoinc_rb_n1, dm_autoinc_wb0, dm_autoinc_wb1 : std_logic := '0';
begin
  -- Switch
  RM1: if (DM_RB_M_NUM > 0) generate
    SETRB: if (DM_RB_M_SET_EN0 = true) generate
      dm_set_rb_m0 <= i_dm_set_rb_m0;
    end generate;
    NOSETRB: if (DM_RB_M_SET_EN0 = false) generate
      dm_set_rb_m0 <= '0';
    end generate;

    RBINC: if (DM_RB_M_INC_EN0 = true) generate
      dm_inc_rb_m0 <= i_dm_inc_rb_m0;
    end generate;
    NORBINC: if (DM_RB_M_INC_EN0 = false) generate
      dm_inc_rb_m0 <= '0';
    end generate;
    
    RBAUTOINC: if (DM_RB_M_AUTOINC_EN0 = true) generate
      rb1_0_autoinc: if (DM_RB_M_NUM = 1) generate
        dm_autoinc_rb_m0 <= i_dm_autoinc_rb_m;
      end generate;
      rb2_0_autoinc: if (DM_RB_M_NUM = 2) generate
        dm_autoinc_rb_m0 <= i_dm_autoinc_rb_m when i_dm_rb_sel_m='0' else '0';
      end generate;
    end generate;
    NORBAUTOINC: if (DM_RB_M_AUTOINC_EN0 = false) generate
      dm_autoinc_rb_m0 <= '0';
    end generate;
  end generate;
  
  RM2: if (DM_RB_M_NUM = 2) generate    
    SETRB1: if (DM_RB_M_SET_EN1 = true) generate
      dm_set_rb_m1 <= i_dm_set_rb_m1;
    end generate;
    NOSETRB1: if (DM_RB_M_SET_EN1 = false) generate
      dm_set_rb_m1 <= '0';
    end generate;
    
    RBINC1: if (DM_RB_M_INC_EN1 = true) generate
      dm_inc_rb_m1 <= i_dm_inc_rb_m1;
    end generate;
    NORBINC1: if (DM_RB_M_INC_EN1 = false) generate
      dm_inc_rb_m1 <= '0';
    end generate;

    RBAUTOINC1: if (DM_RB_M_AUTOINC_EN1 = true) generate
      dm_autoinc_rb_m1 <= i_dm_autoinc_rb_m when i_dm_rb_sel_m='1' else '0';
    end generate;
    NORBAUTOINC1: if (DM_RB_M_AUTOINC_EN1 = false) generate
      dm_autoinc_rb_m1 <= '0';
    end generate;
  end generate;
  
  W1: if (DM_WB_NUM > 0) generate 
    SETWB: if (DM_WB_SET_EN0 = true) generate
      dm_set_wb0 <= i_dm_set_wb_0;
    end generate;
    NOSETWB: if (DM_WB_SET_EN0 = false) generate
      dm_set_wb0 <= '0';
    end generate;
    
    WBINC: if (DM_WB_INC_EN0 = true) generate
      dm_inc_wb0 <= i_dm_inc_wb_0;
    end generate;
    NOWBINC: if (DM_WB_INC_EN0 = false) generate
      dm_inc_wb0 <= '0';
    end generate;
    
    WBAUTOINC: if (DM_WB_AUTOINC_EN0 = true) generate
      wb_1_autoinc: if (DM_WB_NUM = 1) generate
        dm_autoinc_wb0 <= i_dm_autoinc_wb;
      end generate;
      wb_2_autoinc: if (DM_WB_NUM = 2) generate
        dm_autoinc_wb0 <= i_dm_autoinc_wb when i_dm_wb_sel='0' else '0';
      end generate;
    end generate;
    NOWBAUTOINC: if (DM_WB_AUTOINC_EN0 = false) generate
      dm_autoinc_wb0 <= '0';
    end generate;
  end generate;
  
  W2: if (DM_WB_NUM = 2) generate 
    SETWB1: if (DM_WB_SET_EN1 = true) generate
      dm_set_wb1 <= i_dm_set_wb_1;
    end generate;
    NOSETWB1: if (DM_WB_SET_EN1 = false) generate
      dm_set_wb1 <= '0';
    end generate;
    
    WBINC1: if (DM_WB_INC_EN1 = true) generate
      dm_inc_wb1 <= i_dm_inc_wb_1;
    end generate;
    NOWBINC1: if (DM_WB_INC_EN1 = false) generate
      dm_inc_wb1 <= '0';
    end generate;
    
    WBAUTOINC1: if (DM_WB_AUTOINC_EN1 = true) generate
      dm_autoinc_wb1 <= i_dm_autoinc_wb when i_dm_wb_sel='1' else '0';
    end generate;
    NOWBAUTOINC1: if (DM_WB_AUTOINC_EN1 = false) generate
      dm_autoinc_wb1 <= '0';
    end generate;
  end generate;
  
  RN1: if (DM_RB_N_NUM > 0) generate
    SETRB: if (DM_RB_N_SET_EN0 = true) generate
      dm_set_rb_n0 <= i_dm_set_rb_n0;
    end generate;
    NOSETRB: if (DM_RB_N_SET_EN0 = false) generate
      dm_set_rb_n0 <= '0';
    end generate;

    RBINC: if (DM_RB_N_INC_EN0 = true) generate
      dm_inc_rb_n0 <= i_dm_inc_rb_n0;
    end generate;
    NORBINC: if (DM_RB_N_INC_EN0 = false) generate
      dm_inc_rb_n0 <= '0';
    end generate;
    
    RBAUTOINC: if (DM_RB_N_AUTOINC_EN0 = true) generate
      rb1_0_autoinc: if (DM_RB_N_NUM = 1) generate
        dm_autoinc_rb_n0 <= i_dm_autoinc_rb_n;
      end generate;
      rb2_0_autoinc: if (DM_RB_N_NUM = 2) generate
        dm_autoinc_rb_n0 <= i_dm_autoinc_rb_n when i_dm_rb_sel_n='0' else '0';
      end generate;
    end generate;
    NORBAUTOINC: if (DM_RB_N_AUTOINC_EN0 = false) generate
      dm_autoinc_rb_n0 <= '0';
    end generate;
  end generate;
  
  RN2: if (DM_RB_N_NUM = 2) generate    
    SETRB1: if (DM_RB_N_SET_EN1 = true) generate
      dm_set_rb_n1 <= i_dm_set_rb_n1;
    end generate;
    NOSETRB1: if (DM_RB_N_SET_EN1 = false) generate
      dm_set_rb_n1 <= '0';
    end generate;
    
    RBINC1: if (DM_RB_N_INC_EN1 = true) generate
      dm_inc_rb_n1 <= i_dm_inc_rb_n1;
    end generate;
    NORBINC1: if (DM_RB_N_INC_EN1 = false) generate
      dm_inc_rb_n1 <= '0';
    end generate;

    RBAUTOINC1: if (DM_RB_N_AUTOINC_EN1 = true) generate
      dm_autoinc_rb_n1 <= i_dm_autoinc_rb_n when i_dm_rb_sel_n='1' else '0';
    end generate;
    NORBAUTOINC1: if (DM_RB_N_AUTOINC_EN1 = false) generate
      dm_autoinc_rb_n1 <= '0';
    end generate;
  end generate;
  
  -- Address generation
  -- If DM_OFFSET_WIDTH < DM_ADDR_WIDTH, it indicates it is not direct addressing.
  dm_blk_gen: if (DM_OFFSET_WIDTH < DM_ADDR_WIDTH) generate
    signal dm_rofs_m, dm_rofs_n, dm_wofs : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := (others => '0');
    signal dm_rb_m0  : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_RB_M_INITIAL0, DM_ADDR_WIDTH));    
    signal dm_rb_m1  : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_RB_M_INITIAL1, DM_ADDR_WIDTH));
    signal dm_rb_n0  : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_RB_N_INITIAL0, DM_ADDR_WIDTH));
    signal dm_rb_n1  : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_RB_N_INITIAL1, DM_ADDR_WIDTH));
    signal dm_wb_0   : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_WB_INITIAL0, DM_ADDR_WIDTH));
    signal dm_wb_1   : std_logic_vector(DM_ADDR_WIDTH-1 downto 0) := std_logic_vector(to_unsigned(DM_WB_INITIAL1, DM_ADDR_WIDTH));
    signal tmp_wr_set: std_logic_vector(DM_ADDR_WIDTH+DM_OFFSET_WIDTH-1 downto 0) := (others => '0');
    signal tmp_rd_set: std_logic_vector(DM_ADDR_WIDTH+DM_OFFSET_WIDTH-1 downto 0) := (others => '0');
  begin
    tmp_rd_set <= i_dm_rd_bs & (DM_OFFSET_WIDTH-1 downto 0 => '0');
    dm_rd_addr_proc: process(clk)
    begin
      if clk'event and clk = '1' then
        if dm_set_rb_m0 = '1' then
          dm_rb_m0 <= tmp_rd_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_rb_m0 = '1' then
          dm_rb_m0 <= std_logic_vector(signed(i_dm_rd_bs) + signed(dm_rb_m0));
        elsif dm_autoinc_rb_m0 = '1' then
          dm_rb_m0 <= std_logic_vector(DM_RB_M_AUTOINC_SIZE0 + signed(dm_rb_m0));
        end if;
        
        if dm_set_rb_m1 = '1' then
          dm_rb_m1 <= tmp_rd_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_rb_m1 = '1' then
          dm_rb_m1 <= std_logic_vector(signed(i_dm_rd_bs) + signed(dm_rb_m1));
        elsif dm_autoinc_rb_m1 = '1' then
          dm_rb_m1 <= std_logic_vector(DM_RB_M_AUTOINC_SIZE1 + signed(dm_rb_m1));
        end if;
        
        if dm_set_rb_n0 = '1' then
          dm_rb_n0 <= tmp_rd_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_rb_n0 = '1' then
          dm_rb_n0 <= std_logic_vector(signed(i_dm_rd_bs) + signed(dm_rb_n0));
        elsif dm_autoinc_rb_n0 = '1' then
          dm_rb_n0 <= std_logic_vector(DM_RB_N_AUTOINC_SIZE0 + signed(dm_rb_n0));
        end if;
        
        if dm_set_rb_n1 = '1' then
          dm_rb_n1 <= tmp_rd_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_rb_n1 = '1' then
          dm_rb_n1 <= std_logic_vector(signed(i_dm_rd_bs) + signed(dm_rb_n1));
        elsif dm_autoinc_rb_n1 = '1' then
          dm_rb_n1 <= std_logic_vector(DM_RB_N_AUTOINC_SIZE1 + signed(dm_rb_n1));
        end if;
      end if;
    end process;

    tmp_wr_set <= i_dm_wr_bs & (DM_OFFSET_WIDTH-1 downto 0 => '0');
    dm_wr_addr_proc: process(clk)
    begin
      if clk'event and clk = '1' then
        if dm_set_wb0 = '1' then
          dm_wb_0 <= tmp_wr_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_wb0 = '1' then
          dm_wb_0 <= std_logic_vector(signed(i_dm_wr_bs) + signed(dm_wb_0));
        elsif dm_autoinc_wb0 = '1' then
          dm_wb_0 <= std_logic_vector(DM_WB_AUTOINC_SIZE0 + signed(dm_wb_0));
        end if;
        if dm_set_wb1 = '1' then
          dm_wb_1 <= tmp_wr_set(DM_ADDR_WIDTH-1 downto 0);
        elsif dm_inc_wb1 = '1' then
          dm_wb_1 <= std_logic_vector(signed(i_dm_wr_bs) + signed(dm_wb_1));
        elsif dm_autoinc_wb1 = '1' then
          dm_wb_1 <= std_logic_vector(DM_WB_AUTOINC_SIZE1 + signed(dm_wb_1));
        end if;
      end if;
    end process;    
    
    offset_en: if DM_OFFSET_EN = true generate
      dm_rofs_m <= (DM_ADDR_WIDTH-1 downto DM_OFFSET_WIDTH => '0') & i_dm_rd_ofs_m;
      dm_rd_addr_m <= std_logic_vector(unsigned(dm_rofs_m) + unsigned(dm_rb_m0));
      
      dm_rofs_n <= (DM_ADDR_WIDTH-1 downto DM_OFFSET_WIDTH => '0') & i_dm_rd_ofs_n;
      dm_rd_addr_n <= std_logic_vector(unsigned(dm_rofs_n) + unsigned(dm_rb_n0));
      
      dm_wofs <= (DM_ADDR_WIDTH-1 downto DM_OFFSET_WIDTH => '0') & i_dm_wr_ofs;
      dm_wr_addr <= std_logic_vector(unsigned(dm_wofs) + unsigned(dm_wb_0));
    end generate;
	
    offset_dis: if DM_OFFSET_EN = false generate
      muxRBM1: if DM_RB_M_NUM = 1 generate
        dm_rd_addr_m <= dm_rb_m0;        
      end generate;
      muxRBM2: if DM_RB_M_NUM = 2 generate
        dm_rd_addr_m <= dm_rb_m0 when i_dm_rb_sel_m='0' else dm_rb_m1;
      end generate;
      
      muxRBN1: if DM_RB_N_NUM = 1 generate
        dm_rd_addr_n <= dm_rb_n0;        
      end generate;
      muxRBN2: if DM_RB_N_NUM = 2 generate
        dm_rd_addr_n <= dm_rb_n0 when i_dm_rb_sel_n='0' else dm_rb_n1;
      end generate;
      
      muxWB1: if DM_WB_NUM = 1 generate
        dm_wr_addr <= dm_wb_0;        
      end generate;
      muxWB2: if DM_WB_NUM = 2 generate
        dm_wr_addr <= dm_wb_0 when i_dm_wb_sel='0' else dm_wb_1;
      end generate;
    end generate;
  end generate;

  dm_noblk_gen: if (DM_OFFSET_WIDTH = DM_ADDR_WIDTH) generate
    dm_rd_addr_m <= i_dm_rd_ofs_m;
    dm_rd_addr_n <= i_dm_rd_ofs_n;
    dm_wr_addr   <= i_dm_wr_ofs;
  end generate;

  o_dm_rd_addr_0 <= dm_rd_addr_m;
  o_dm_rd_addr_1 <= dm_rd_addr_n;
  o_dm_wr_addr <= dm_wr_addr;
end structure;
