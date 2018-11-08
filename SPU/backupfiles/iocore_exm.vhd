----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    10:03:03 03/04/2013 
-- Design Name: 
-- Module Name:    iocore_exm - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.math_real.all;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity iocore_exm is
generic(
  DATA_WIDTH  : integer  := 16;
  DQ_WIDTH    : integer  := 64;
  MASK_WIDTH  : integer  := 8;
  BURST_LEN   : integer  := 4;
  
  EM_RB_NUM      : integer:= 2;  
  EM_RB_INITIAL0 : integer:= 10000;
  EM_RB_INITIAL1 : integer:= 20000;
  EM_WB_INITIAL0 : integer:= 30000;
  
  EM_RB_AUTOINC_SIZE0 : integer:= 16;
  EM_RB_AUTOINC_SIZE1 : integer:= 16;
  EM_WB_AUTOINC_SIZE0 : integer:= 16;
  
  EM_RB_AUTOINC_EN0   : boolean:= true;    
  EM_RB_AUTOINC_EN1   : boolean:= true;
  EM_WB_AUTOINC_EN0   : boolean:= true;
  
  EM_RB_INC_EN0       : boolean:= true;
  EM_RB_INC_EN1       : boolean:= true;
  EM_WB_INC_EN0       : boolean:= true
);
port(
  clk            : in  std_logic;
  
  i_em_rd_bs       :  in std_logic_vector (30 downto 0);
  i_em_wr_bs       :  in std_logic_vector (30 downto 0);
  i_em_inc_rb_0    :  in std_logic;
  i_em_inc_rb_1    :  in std_logic;
  i_em_inc_wb_0    :  in std_logic;
  i_em_autoinc_rb  :  in std_logic;
  i_em_rb_sel      :  in std_logic;
  i_em_autoinc_wb  :  in std_logic;
    
  o_mif_af_cmd   : out std_logic_vector(2 downto 0);
  o_mif_af_addr  : out std_logic_vector(30 downto 0);
  o_mif_af_wren  : out std_logic := '0';
  i_mif_af_afull : in  std_logic;

  o_mif_wdf_wren : out std_logic;
  o_mif_wdf_data : out std_logic_vector(2*DQ_WIDTH-1 downto 0);
  o_mif_wdf_mask_data: out std_logic_vector(2*MASK_WIDTH-1 downto 0);
  i_mif_wdf_afull: in  std_logic;

  i_mif_rd_data  : in  std_logic_vector(2*DQ_WIDTH-1 downto 0);
  i_mif_rd_valid : in  std_logic;
  o_mif_rd_valid : out std_logic;

  i_ldexmem      : in  std_logic;
  i_shiftcacheline: in std_logic := '0';
  i_ldcache      : in  std_logic;
  o_core_data    : out std_logic_vector(DATA_WIDTH-1 downto 0);
  i_core_data    : in  std_logic_vector(DATA_WIDTH-1 downto 0);
  i_stexmem      : in  std_logic;
  i_stcache      : in  std_logic
);
end iocore_exm;

architecture Behavioral of iocore_exm is
  constant cAPP_DATA_WIDTH : integer := 2*DQ_WIDTH;
  constant cWORD_NUM : integer := cAPP_DATA_WIDTH/DATA_WIDTH;
  constant cWORD_IDX_WIDTH : integer := integer(ceil(log2(real(cWORD_NUM))));
  constant cMASK_OFF : std_logic_vector(2*MASK_WIDTH-1 downto 0) := "0000000000000000";
  constant cMASK_ON  : std_logic_vector(2*MASK_WIDTH-1 downto 0) := "1111111111111111";
  
  signal em_rd_addr, em_wr_addr : std_logic_vector (30 downto 0);
  
  signal em_inc_rb_0, em_inc_rb_1, em_inc_wb_0 :  std_logic := '0';
  signal em_autoinc_rb_0, em_autoinc_rb_1, em_autoinc_wb_0 :  std_logic := '0';  
  signal em_rb_0 : std_logic_vector(30 downto 0) := std_logic_vector(to_unsigned(EM_RB_INITIAL0, 31));    
  signal em_rb_1 : std_logic_vector(30 downto 0) := std_logic_vector(to_unsigned(EM_RB_INITIAL1, 31));
  signal em_wb_0 : std_logic_vector(30 downto 0) := std_logic_vector(to_unsigned(EM_WB_INITIAL0, 31));
  
--  
--  constant cLINE_WIDTH : integer := integer(ceil(log2(real(BURST_LEN/2))));
--  constant cLINE_NUM : integer := BURST_LEN/2;
--  
--  type CACHE_TYPE is array (natural range <>) of std_logic_vector(cAPP_DATA_WIDTH-1 downto 0); 
--  signal st_cache_line : CACHE_TYPE(cLINE_NUM-1 downto 0);
--  signal st_core2line_cnter  : std_logic_vector(cLINEWIDTH-1 downto 0) := (others=>'0');
--  signal st_line2exmem_cnter : std_logic_vector(cLINEWIDTH-1 downto 0) := (others=>'0');
--  
--  signal ld_cache_line : CACHE_TYPE(cLINE_NUM-1 downto 0);
--  signal idx1_reg0 : std_logic_vector(IDX_WIDTH1-1 downto 0);
--  signal ld_cnter  : std_logic_vector(cLINE_NUM-1 downto 0) := std_logic_vector(to_unsigned(1, cLINE_NUM));
begin
  -- Switch on/off
  S1: if (EM_RB_NUM > 0) generate
    RBINC: if (EM_RB_INC_EN0 = true) generate
      em_inc_rb_0 <= i_em_inc_rb_0;
    end generate;
    NORBINC: if (EM_RB_INC_EN0 = false) generate
      em_inc_rb_0 <= '0';
    end generate;
    WBINC: if (EM_WB_INC_EN0 = true) generate
      em_inc_wb_0 <= i_em_inc_wb_0;
    end generate;
    NOWBINC: if (EM_WB_INC_EN0 = false) generate
      em_inc_wb_0 <= '0';
    end generate;
    
    RBAUTOINC: if (EM_RB_AUTOINC_EN0 = true) generate
      rb1_0_autoinc: if (EM_RB_NUM = 1) generate
        em_autoinc_rb_0 <= i_em_autoinc_rb;
      end generate;
      rb2_0_autoinc: if (EM_RB_NUM = 2) generate
        em_autoinc_rb_0 <= i_em_autoinc_rb when i_em_rb_sel='0' else '0';
      end generate;
    end generate;
    NORBAUTOINC: if (EM_RB_AUTOINC_EN0 = false) generate
      em_autoinc_rb_0 <= '0';
    end generate;
    WBAUTOINC: if (EM_WB_AUTOINC_EN0 = true) generate
      em_autoinc_wb_0 <= i_em_autoinc_wb;
    end generate;
    NOWBAUTOINC: if (EM_WB_AUTOINC_EN0 = false) generate
      em_autoinc_wb_0 <= '0';
    end generate;
  end generate;
  
  S2: if (EM_RB_NUM > 1) generate    
    RBINC1: if (EM_RB_INC_EN1 = true) generate
      em_inc_rb_1 <= i_em_inc_rb_1;
    end generate;
    NORBINC1: if (EM_RB_INC_EN1 = false) generate
      em_inc_rb_1 <= '0';
    end generate;
    
    RBAUTOINC1: if (EM_RB_AUTOINC_EN1 = true) generate
      rb2_1_autoinc: if (EM_RB_NUM = 2) generate
        em_autoinc_rb_1 <= i_em_autoinc_rb when i_em_rb_sel='1' else '0';
      end generate;
    end generate;
    NORBAUTOINC1: if (EM_RB_AUTOINC_EN1 = false) generate
      em_autoinc_rb_1 <= '0';
    end generate;
  end generate;
  
  em_rd_addr_proc: process(clk)
  begin
    if clk'event and clk = '1' then
      if em_inc_rb_0 = '1' then
        em_rb_0 <= std_logic_vector(signed(i_em_rd_bs) + signed(em_rb_0));
      elsif em_autoinc_rb_0 = '1' then
        em_rb_0 <= std_logic_vector(EM_RB_AUTOINC_SIZE0 + signed(em_rb_0));
      end if;
      
      if em_inc_rb_1 = '1' then
        em_rb_1 <= std_logic_vector(signed(i_em_rd_bs) + signed(em_rb_1));
      elsif em_autoinc_rb_1 = '1' then
        em_rb_1 <= std_logic_vector(EM_RB_AUTOINC_SIZE1 + signed(em_rb_1));
      end if;        
    end if;
  end process;

  em_wr_addr_proc: process(clk)
  begin
    if clk'event and clk = '1' then
      if em_inc_wb_0 = '1' then
        em_wb_0 <= std_logic_vector(signed(i_em_wr_bs) + signed(em_wb_0));
      elsif em_autoinc_wb_0 = '1' then
        em_wb_0 <= std_logic_vector(EM_WB_AUTOINC_SIZE0 + signed(em_wb_0));
      end if;
    end if;
  end process;
  
  em_wr_addr <= em_wb_0;
  muxRB1: if EM_RB_NUM = 1 generate
    em_rd_addr <= em_rb_0;        
  end generate;

  muxRB2: if EM_RB_NUM = 2 generate
    em_rd_addr <= em_rb_0 when i_em_rb_sel='0' else em_rb_1;
  end generate;
  
  o_mif_rd_valid <= i_mif_rd_valid;
  
  -- A simplified case is only one cache line. Because burst can not be disabled, here use masks.
  -- Burst length for memory controller is set to 4.
  BURST_2: if BURST_LEN = 2 generate
    signal st_cache : std_logic_vector(cAPP_DATA_WIDTH-1 downto 0);
    signal ld_cache : std_logic_vector(cAPP_DATA_WIDTH-1 downto 0);
    signal ld_word_cnter : std_logic_vector(cWORD_IDX_WIDTH-1 downto 0) := (others=>'0');
    type CACHE_TYPE is array (natural range <>) of std_logic_vector(DATA_WIDTH-1 downto 0); 
    signal ld_cache_wire : CACHE_TYPE(cWORD_NUM-1 downto 0);
    
    type state_type is (s_nml, s_stExmem, s_ldExmem, s_ldWait);
    signal state: state_type;
  begin
    wire_gen: for i in 0 to cWORD_NUM-1 generate
      ld_cache_wire(i) <= ld_cache((i+1)*DATA_WIDTH-1 downto i*DATA_WIDTH);
    end generate;
    
    process (clk) begin
      if (clk'event and clk = '1') then
        if (i_stcache = '1') then
          st_cache(DATA_WIDTH-1 downto 0) <= i_core_data;
          st_cache(cAPP_DATA_WIDTH-1 downto DATA_WIDTH) <= st_cache(cAPP_DATA_WIDTH-DATA_WIDTH-1 downto 0);
        end if;
        
        o_core_data <= ld_cache_wire(to_integer(unsigned(ld_word_cnter)));
        
        if (i_ldcache = '1') then
          ld_word_cnter <= std_logic_vector(unsigned(ld_word_cnter)+1);
        end if;
        
        o_mif_wdf_data <= st_cache;
        o_mif_wdf_mask_data <= cMASK_OFF;
        case state is
          when s_nml =>
            o_mif_af_wren  <= '0';
            if (i_stexmem = '1') then
              o_mif_af_cmd   <= "000";
              o_mif_af_wren  <= '1';
              o_mif_af_addr  <= em_wr_addr;
              o_mif_wdf_wren <= '1';
              state <= s_stExmem;
            elsif (i_ldexmem = '1') then
              o_mif_af_cmd   <= "001";
              o_mif_af_wren  <= '1';
              o_mif_af_addr  <= em_rd_addr;
              state <= s_ldExmem;
            end if;                        
          when s_stExmem =>
            o_mif_af_wren  <= '0';
            o_mif_wdf_mask_data <= cMASK_ON;
            state <= s_nml;
          when s_ldExmem =>
            o_mif_af_wren  <= '0';
            if (i_mif_rd_valid = '1') then
              ld_cache <= i_mif_rd_data;
              state <= s_ldWait;
            end if;
          when s_ldWait =>
            -- this state is necessary, as when ioCore is waiting for data it halts
            -- the LDEXMEM. When rd_valid is asserted, the ioCore resumes, but several
            -- cycles later the LDCACHE instruction can arrive. If jump back directly 
            -- to s_nml, it will jump to s_ldExmem again faltly.
            if (i_ldexmem = '0') then
              state <= s_nml;
            end if;
        end case;
      end if;
    end process;
  end generate;
  
  -- Burst 4 is only for store operation, while load is always burst 2.
  BURST_4: if BURST_LEN = 4 generate
    signal st_cache : std_logic_vector(cAPP_DATA_WIDTH-1 downto 0);
    signal ld_cache0 : std_logic_vector(cAPP_DATA_WIDTH-1 downto 0);
    signal ld_cache1 : std_logic_vector(cAPP_DATA_WIDTH-1 downto 0);
    signal ld_word_cnter : std_logic_vector(cWORD_IDX_WIDTH-1 downto 0) := (others=>'0');
    type CACHE_TYPE is array (natural range <>) of std_logic_vector(DATA_WIDTH-1 downto 0); 
    signal ld_cache_wire : CACHE_TYPE(cWORD_NUM-1 downto 0);
    
    type state_type is (s_nml, s_stExmem, s_ldExmem, s_ldExmem1, s_ldWait);
    signal state: state_type;
  begin
    wire_gen: for i in 0 to cWORD_NUM-1 generate
      ld_cache_wire(i) <= ld_cache0((i+1)*DATA_WIDTH-1 downto i*DATA_WIDTH);
    end generate;
    
    process (clk) begin
      if (clk'event and clk = '1') then
        if (i_stcache = '1') then
          st_cache(DATA_WIDTH-1 downto 0) <= i_core_data;
          st_cache(cAPP_DATA_WIDTH-1 downto DATA_WIDTH) <= st_cache(cAPP_DATA_WIDTH-DATA_WIDTH-1 downto 0);
        end if;
        
        o_core_data <= ld_cache_wire(to_integer(unsigned(ld_word_cnter)));
        
        if (i_shiftcacheline = '1') then
          ld_cache0 <= ld_cache1;
        end if;
        
        if (i_ldcache = '1') then
          ld_word_cnter <= std_logic_vector(unsigned(ld_word_cnter)+1);
        end if;
        
        o_mif_wdf_data <= st_cache;
        o_mif_wdf_mask_data <= cMASK_OFF;
        case state is
          when s_nml =>
            o_mif_af_wren  <= '0';
            if (i_stexmem = '1') then
              o_mif_af_cmd   <= "000";
              o_mif_af_wren  <= '1';
              o_mif_af_addr  <= em_wr_addr;
              o_mif_wdf_wren <= '1';
              state <= s_stExmem;
            elsif (i_ldexmem = '1') then
              o_mif_af_cmd   <= "001";
              o_mif_af_wren  <= '1';
              o_mif_af_addr  <= em_rd_addr;
              state <= s_ldExmem;
            end if;                        
          when s_stExmem =>
            o_mif_af_wren  <= '0';
            o_mif_wdf_mask_data <= cMASK_ON;
            state <= s_nml;
          when s_ldExmem =>
            o_mif_af_wren  <= '0';
            if (i_mif_rd_valid = '1') then
              ld_cache0 <= i_mif_rd_data;
              state <= s_ldExmem1;
            end if;
          when s_ldExmem1 =>
            ld_cache1 <= i_mif_rd_data;
            state <= s_ldWait;
          when s_ldWait =>
            -- this state is necessary, as when ioCore is waiting for data it halts
            -- the LDEXMEM. When rd_valid is asserted, the ioCore resumes, but several
            -- cycles later the LDCACHE instruction can arrive. If jump back directly 
            -- to s_nml, it will jump to s_ldExmem again faltly.
            if (i_ldexmem = '0') then
              state <= s_nml;
            end if;
        end case;
      end if;
    end process;
  end generate;
end Behavioral;
