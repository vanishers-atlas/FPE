
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;
library work;
use work.ssp_pkg.all;

entity ca_sort is
generic (
  K_NUM : integer := 1;
  M_NUM : integer := 5;
  DATA_WIDTH : integer := 16
);
port(
  clk  : in std_logic;
  i_din  : in std_logic_vector(DATA_WIDTH-1 downto 0);
  i_id_sort : in std_logic;
  i_id_ld : in std_logic;
  i_id_unld : in std_logic;
  o_dout  : out std_logic_vector(DATA_WIDTH-1 downto 0)
);
end ca_sort;

architecture rtl of ca_sort is
  constant K_WIDTH : integer := integer(ceil(log2(real(K_NUM))));
    
  signal id_sort : std_logic := '0';
  signal id_ld : std_logic := '0';
  signal id_unld : std_logic := '0';
  signal din : std_logic_vector(DATA_WIDTH-1 downto 0);
  signal dout : std_logic_vector(DATA_WIDTH-1 downto 0);
  
  signal cmp_out : std_logic_vector(DATA_WIDTH-1 downto 0);
  signal idx_out : std_logic_vector(K_WIDTH-1 downto 0);
  signal idx_last : std_logic_vector(K_WIDTH-1 downto 0);
      
  signal repl : std_logic := '0';
  signal repl_reg : std_logic := '0';
  
  type VSORTDATA_TYPE is array (natural range <>) of std_logic_vector(DATA_WIDTH-1 downto 0);
begin
  id_ld <= i_id_ld;
  id_sort <= i_id_sort;
  id_unld <= i_id_unld;

--  u_din_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
--    port map(clk=>clk, rst=>'0', i_d=>i_din, o_d=>din);
  din <= i_din;
  K1M2_GEN: if M_NUM = 2 and K_NUM = 1 generate        
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
        
    cmp_out <= vec_0(0);
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_0(0);
          vec_0(0) <= vec_0(1);
        elsif (id_sort = '1' and repl_reg = '1') then
          vec_0 <= vec_in;
        end if;
      end if;
    end process;
  end generate;
  
  K1M5_GEN: if M_NUM = 5 and K_NUM = 1 generate        
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
        
    cmp_out <= vec_0(0);
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
        elsif (id_sort = '1' and repl_reg = '1') then
          vec_0 <= vec_in;
        end if;
      end if;
    end process;
  end generate;
  
  K1M9_GEN: if M_NUM = 9 and K_NUM = 1 generate        
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
        
    cmp_out <= vec_0(8);
    
    repl <= '1' when (vec_in(8) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8) <= vec_in(7);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
        elsif (id_sort = '1' and repl_reg = '1') then
          vec_0 <= vec_in;
        end if;
      end if;
    end process;
  end generate;
  
  K1M12_GEN: if M_NUM = 12 and K_NUM = 1 generate        
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
        
    cmp_out <= vec_0(0);
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8) <= vec_in(7);
          vec_in(9) <= vec_in(8);
          vec_in(10) <= vec_in(9);
          vec_in(11) <= vec_in(10);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
          vec_0(8) <= vec_0(9);
          vec_0(9) <= vec_0(10);
          vec_0(10) <= vec_0(11);
        elsif (id_sort = '1' and repl_reg = '1') then
          vec_0 <= vec_in;
        end if;
      end if;
    end process;
  end generate;
  
  K5M5_GEN: if M_NUM = 5 and K_NUM = 5 generate
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg;
    idx_lv1_1 <= idx_lv0_2_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;  
  
  K5M9_GEN: if M_NUM = 9 and K_NUM = 5 generate    
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg;
    idx_lv1_1 <= idx_lv0_2_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8) <= vec_in(7);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_4(5);
          vec_4(5) <= vec_4(6);
          vec_4(6) <= vec_4(7);
          vec_4(7) <= vec_4(8);
          vec_4(8) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_3(5);
          vec_3(5) <= vec_3(6);
          vec_3(6) <= vec_3(7);
          vec_3(7) <= vec_3(8);
          vec_3(8) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_2(5);
          vec_2(5) <= vec_2(6);
          vec_2(6) <= vec_2(7);
          vec_2(7) <= vec_2(8);
          vec_2(8) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_1(5);
          vec_1(5) <= vec_1(6);
          vec_1(6) <= vec_1(7);
          vec_1(7) <= vec_1(8);
          vec_1(8) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;  
    
  K5M13_GEN: if M_NUM = 13 and K_NUM = 5 generate
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg;
    idx_lv1_1 <= idx_lv0_2_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8)  <= vec_in(7);
          vec_in(9)  <= vec_in(8);
          vec_in(10) <= vec_in(9);
          vec_in(11) <= vec_in(10);
          vec_in(12) <= vec_in(11);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_4(5);
          vec_4(5) <= vec_4(6);
          vec_4(6) <= vec_4(7);
          vec_4(7) <= vec_4(8);
          vec_4(8)  <= vec_4(9 );
          vec_4(9 ) <= vec_4(10);
          vec_4(10) <= vec_4(11);
          vec_4(11) <= vec_4(12);
          vec_4(12) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_3(5);
          vec_3(5) <= vec_3(6);
          vec_3(6) <= vec_3(7);
          vec_3(7) <= vec_3(8);
          vec_3(8) <= vec_3(9 );
          vec_3(9 ) <= vec_3(10);
          vec_3(10) <= vec_3(11);
          vec_3(11) <= vec_3(12);
          vec_3(12) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_2(5);
          vec_2(5) <= vec_2(6);
          vec_2(6) <= vec_2(7);
          vec_2(7) <= vec_2(8);
          vec_2(8) <= vec_2(9 );
          vec_2(9 ) <= vec_2(10);
          vec_2(10) <= vec_2(11);
          vec_2(11) <= vec_2(12);
          vec_2(12) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_1(5);
          vec_1(5) <= vec_1(6);
          vec_1(6) <= vec_1(7);
          vec_1(7) <= vec_1(8);
          vec_1(8)  <= vec_1(9 );
          vec_1(9 ) <= vec_1(10);
          vec_1(10) <= vec_1(11);
          vec_1(11) <= vec_1(12);
          vec_1(12) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
          vec_0(8)  <= vec_0(9 );
          vec_0(9 ) <= vec_0(10);
          vec_0(10) <= vec_0(11);
          vec_0(11) <= vec_0(12);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;
  
  K8M5_GEN: if M_NUM = 5 and K_NUM = 8 generate
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_5  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_6  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_7  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0) when (vec_4(0) > vec_5(0)) else vec_5(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH)) when (vec_4(0) > vec_5(0)) 
      else std_logic_vector(to_unsigned(5, K_WIDTH));
    cmp_lv0_3 <= vec_6(0) when (vec_6(0) > vec_7(0)) else vec_7(0);
    idx_lv0_3 <= std_logic_vector(to_unsigned(6, K_WIDTH)) when (vec_6(0) > vec_7(0)) 
      else std_logic_vector(to_unsigned(7, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
    u_cmp_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_3, o_d=>cmp_lv0_3_reg);
    u_idx_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_3, o_d=>idx_lv0_3_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else cmp_lv0_3_reg;
    idx_lv1_1 <= idx_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else idx_lv0_3_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout     <= vec_7(0);
          vec_7(0) <= vec_7(1);
          vec_7(1) <= vec_7(2);
          vec_7(2) <= vec_7(3);
          vec_7(3) <= vec_7(4);
          vec_7(4) <= vec_6(0);
          vec_6(0) <= vec_6(1);
          vec_6(1) <= vec_6(2);
          vec_6(2) <= vec_6(3);
          vec_6(3) <= vec_6(4);
          vec_6(4) <= vec_5(0);
          vec_5(0) <= vec_5(1);
          vec_5(1) <= vec_5(2);
          vec_5(2) <= vec_5(3);
          vec_5(3) <= vec_5(4);
          vec_5(4) <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          elsif (idx_last = "101") then
            vec_5 <= vec_in;
          elsif (idx_last = "110") then
            vec_6 <= vec_in;
          elsif (idx_last = "111") then
            vec_7 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;  
  
  K8M9_GEN: if M_NUM = 9 and K_NUM = 8 generate
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_5  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_6  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_7  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0) when (vec_4(0) > vec_5(0)) else vec_5(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH)) when (vec_4(0) > vec_5(0)) 
      else std_logic_vector(to_unsigned(5, K_WIDTH));
    cmp_lv0_3 <= vec_6(0) when (vec_6(0) > vec_7(0)) else vec_7(0);
    idx_lv0_3 <= std_logic_vector(to_unsigned(6, K_WIDTH)) when (vec_6(0) > vec_7(0)) 
      else std_logic_vector(to_unsigned(7, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
    u_cmp_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_3, o_d=>cmp_lv0_3_reg);
    u_idx_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_3, o_d=>idx_lv0_3_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else cmp_lv0_3_reg;
    idx_lv1_1 <= idx_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else idx_lv0_3_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8) <= vec_in(7);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_7(0);          
          vec_7(0) <= vec_7(1);
          vec_7(1) <= vec_7(2);
          vec_7(2) <= vec_7(3);
          vec_7(3) <= vec_7(4);
          vec_7(4) <= vec_7(5);
          vec_7(5) <= vec_7(6);
          vec_7(6) <= vec_7(7);
          vec_7(7) <= vec_7(8);
          vec_7(8) <= vec_6(0);
          vec_6(0) <= vec_6(1);
          vec_6(1) <= vec_6(2);
          vec_6(2) <= vec_6(3);
          vec_6(3) <= vec_6(4);
          vec_6(4) <= vec_6(5);
          vec_6(5) <= vec_6(6);
          vec_6(6) <= vec_6(7);
          vec_6(7) <= vec_6(8);
          vec_6(8) <= vec_5(0);
          vec_5(0) <= vec_5(1);
          vec_5(1) <= vec_5(2);
          vec_5(2) <= vec_5(3);
          vec_5(3) <= vec_5(4);
          vec_5(4) <= vec_5(5);
          vec_5(5) <= vec_5(6);
          vec_5(6) <= vec_5(7);
          vec_5(7) <= vec_5(8);
          vec_5(8) <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_4(5);
          vec_4(5) <= vec_4(6);
          vec_4(6) <= vec_4(7);
          vec_4(7) <= vec_4(8);
          vec_4(8) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_3(5);
          vec_3(5) <= vec_3(6);
          vec_3(6) <= vec_3(7);
          vec_3(7) <= vec_3(8);
          vec_3(8) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_2(5);
          vec_2(5) <= vec_2(6);
          vec_2(6) <= vec_2(7);
          vec_2(7) <= vec_2(8);
          vec_2(8) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_1(5);
          vec_1(5) <= vec_1(6);
          vec_1(6) <= vec_1(7);
          vec_1(7) <= vec_1(8);
          vec_1(8) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          elsif (idx_last = "101") then
            vec_5 <= vec_in;
          elsif (idx_last = "110") then
            vec_6 <= vec_in;
          elsif (idx_last = "111") then
            vec_7 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;  
    
  K8M13_GEN: if M_NUM = 13 and K_NUM = 8 generate
    signal cmp_lv0_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0 : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1 : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0 : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal cmp_lv0_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_2_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv0_3_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv1_1_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal cmp_lv2_0_reg : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal idx_lv0_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_2_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv0_3_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv1_1_reg : std_logic_vector(K_WIDTH-1 downto 0);
    signal idx_lv2_0_reg : std_logic_vector(K_WIDTH-1 downto 0);
    
    signal vec_in : VSORTDATA_TYPE(M_NUM-1 downto 0);
    signal vec_0  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_1  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_2  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_3  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_4  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_5  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_6  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
    signal vec_7  : VSORTDATA_TYPE(M_NUM-1 downto 0) := (others=>(others=>'1'));
  begin
    cmp_lv0_0 <= vec_0(0) when (vec_0(0) > vec_1(0)) else vec_1(0);
    idx_lv0_0 <= std_logic_vector(to_unsigned(0, K_WIDTH)) when (vec_0(0) > vec_1(0)) 
      else std_logic_vector(to_unsigned(1, K_WIDTH));
    cmp_lv0_1 <= vec_2(0) when (vec_2(0) > vec_3(0)) else vec_3(0);
    idx_lv0_1 <= std_logic_vector(to_unsigned(2, K_WIDTH)) when (vec_2(0) > vec_3(0)) 
      else std_logic_vector(to_unsigned(3, K_WIDTH));
    cmp_lv0_2 <= vec_4(0) when (vec_4(0) > vec_5(0)) else vec_5(0);
    idx_lv0_2 <= std_logic_vector(to_unsigned(4, K_WIDTH)) when (vec_4(0) > vec_5(0)) 
      else std_logic_vector(to_unsigned(5, K_WIDTH));
    cmp_lv0_3 <= vec_6(0) when (vec_6(0) > vec_7(0)) else vec_7(0);
    idx_lv0_3 <= std_logic_vector(to_unsigned(6, K_WIDTH)) when (vec_6(0) > vec_7(0)) 
      else std_logic_vector(to_unsigned(7, K_WIDTH));
      
    u_cmp_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_0, o_d=>cmp_lv0_0_reg);
    u_idx_lv0_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_0, o_d=>idx_lv0_0_reg);
    u_cmp_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_1, o_d=>cmp_lv0_1_reg);
    u_idx_lv0_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_1, o_d=>idx_lv0_1_reg);
    u_cmp_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_2, o_d=>cmp_lv0_2_reg);
    u_idx_lv0_2_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_2, o_d=>idx_lv0_2_reg);
    u_cmp_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv0_3, o_d=>cmp_lv0_3_reg);
    u_idx_lv0_3_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv0_3, o_d=>idx_lv0_3_reg);
      
    cmp_lv1_0 <= cmp_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else cmp_lv0_1_reg;
    idx_lv1_0 <= idx_lv0_0_reg when (cmp_lv0_0_reg > cmp_lv0_1_reg) else idx_lv0_1_reg;
    cmp_lv1_1 <= cmp_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else cmp_lv0_3_reg;
    idx_lv1_1 <= idx_lv0_2_reg when (cmp_lv0_2_reg > cmp_lv0_3_reg) else idx_lv0_3_reg;
    
    u_cmp_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_0, o_d=>cmp_lv1_0_reg);
    u_idx_lv1_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_0, o_d=>idx_lv1_0_reg);
    u_cmp_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv1_1, o_d=>cmp_lv1_1_reg);
    u_idx_lv1_1_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv1_1, o_d=>idx_lv1_1_reg);
    
    cmp_lv2_0 <= cmp_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else cmp_lv1_1_reg;
    idx_lv2_0 <= idx_lv1_0_reg when (cmp_lv1_0_reg > cmp_lv1_1_reg) else idx_lv1_1_reg;
    
    u_cmp_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>DATA_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>cmp_lv2_0, o_d=>cmp_lv2_0_reg);
    u_idx_lv2_0_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_lv2_0, o_d=>idx_lv2_0_reg);
        
    cmp_out <= cmp_lv2_0_reg;
    idx_out <= idx_lv2_0_reg;
    
    repl <= '1' when (vec_in(0) < cmp_out) else '0';
    
    u_repl_reg:m_word_generic_reg1 generic map(REG_NUM=>1)
      port map(clk=>clk, rst=>'0', i_d=>repl, o_d=>repl_reg);  
    u_idx_last_reg:m_word_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>K_WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>idx_out, o_d=>idx_last);
     
    proc_ld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_ld = '1') then        
          vec_in(0) <= din;
          vec_in(1) <= vec_in(0);
          vec_in(2) <= vec_in(1);
          vec_in(3) <= vec_in(2);        
          vec_in(4) <= vec_in(3);
          vec_in(5) <= vec_in(4);
          vec_in(6) <= vec_in(5);
          vec_in(7) <= vec_in(6);
          vec_in(8)  <= vec_in(7);
          vec_in(9)  <= vec_in(8);
          vec_in(10) <= vec_in(9);
          vec_in(11) <= vec_in(10);
          vec_in(12) <= vec_in(11);
        end if;
      end if;
    end process;
    
    proc_unld:process (clk)
    begin
      if (clk'event and clk = '1') then
        if (id_unld = '1') then
          dout <= vec_7(0);
          vec_7(0) <= vec_7(1);
          vec_7(1) <= vec_7(2);
          vec_7(2) <= vec_7(3);
          vec_7(3) <= vec_7(4);
          vec_7(4) <= vec_7(5);
          vec_7(5) <= vec_7(6);
          vec_7(6) <= vec_7(7);
          vec_7(7) <= vec_7(8);
          vec_7(8)  <= vec_7(9 );
          vec_7(9 ) <= vec_7(10);
          vec_7(10) <= vec_7(11);
          vec_7(11) <= vec_7(12);
          vec_7(12) <= vec_6(0);
          vec_6(0) <= vec_6(1);
          vec_6(1) <= vec_6(2);
          vec_6(2) <= vec_6(3);
          vec_6(3) <= vec_6(4);
          vec_6(4) <= vec_6(5);
          vec_6(5) <= vec_6(6);
          vec_6(6) <= vec_6(7);
          vec_6(7) <= vec_6(8);
          vec_6(8)  <= vec_6(9 );
          vec_6(9 ) <= vec_6(10);
          vec_6(10) <= vec_6(11);
          vec_6(11) <= vec_6(12);
          vec_6(12) <= vec_5(0);
          vec_5(0) <= vec_5(1);
          vec_5(1) <= vec_5(2);
          vec_5(2) <= vec_5(3);
          vec_5(3) <= vec_5(4);
          vec_5(4) <= vec_5(5);
          vec_5(5) <= vec_5(6);
          vec_5(6) <= vec_5(7);
          vec_5(7) <= vec_5(8);
          vec_5(8)  <= vec_5(9 );
          vec_5(9 ) <= vec_5(10);
          vec_5(10) <= vec_5(11);
          vec_5(11) <= vec_5(12);
          vec_5(12) <= vec_4(0);
          vec_4(0) <= vec_4(1);
          vec_4(1) <= vec_4(2);
          vec_4(2) <= vec_4(3);
          vec_4(3) <= vec_4(4);
          vec_4(4) <= vec_4(5);
          vec_4(5) <= vec_4(6);
          vec_4(6) <= vec_4(7);
          vec_4(7) <= vec_4(8);
          vec_4(8)  <= vec_4(9 );
          vec_4(9 ) <= vec_4(10);
          vec_4(10) <= vec_4(11);
          vec_4(11) <= vec_4(12);
          vec_4(12) <= vec_3(0);
          vec_3(0) <= vec_3(1);
          vec_3(1) <= vec_3(2);
          vec_3(2) <= vec_3(3);
          vec_3(3) <= vec_3(4);
          vec_3(4) <= vec_3(5);
          vec_3(5) <= vec_3(6);
          vec_3(6) <= vec_3(7);
          vec_3(7) <= vec_3(8);
          vec_3(8) <= vec_3(9 );
          vec_3(9 ) <= vec_3(10);
          vec_3(10) <= vec_3(11);
          vec_3(11) <= vec_3(12);
          vec_3(12) <= vec_2(0);
          vec_2(0) <= vec_2(1);
          vec_2(1) <= vec_2(2);
          vec_2(2) <= vec_2(3);
          vec_2(3) <= vec_2(4);
          vec_2(4) <= vec_2(5);
          vec_2(5) <= vec_2(6);
          vec_2(6) <= vec_2(7);
          vec_2(7) <= vec_2(8);
          vec_2(8) <= vec_2(9 );
          vec_2(9 ) <= vec_2(10);
          vec_2(10) <= vec_2(11);
          vec_2(11) <= vec_2(12);
          vec_2(12) <= vec_1(0);
          vec_1(0) <= vec_1(1);
          vec_1(1) <= vec_1(2);
          vec_1(2) <= vec_1(3);
          vec_1(3) <= vec_1(4);
          vec_1(4) <= vec_1(5);
          vec_1(5) <= vec_1(6);
          vec_1(6) <= vec_1(7);
          vec_1(7) <= vec_1(8);
          vec_1(8)  <= vec_1(9 );
          vec_1(9 ) <= vec_1(10);
          vec_1(10) <= vec_1(11);
          vec_1(11) <= vec_1(12);
          vec_1(12) <= vec_0(0);
          vec_0(0) <= vec_0(1);
          vec_0(1) <= vec_0(2);
          vec_0(2) <= vec_0(3);
          vec_0(3) <= vec_0(4);
          vec_0(4) <= vec_0(5);
          vec_0(5) <= vec_0(6);
          vec_0(6) <= vec_0(7);
          vec_0(7) <= vec_0(8);
          vec_0(8)  <= vec_0(9 );
          vec_0(9 ) <= vec_0(10);
          vec_0(10) <= vec_0(11);
          vec_0(11) <= vec_0(12);
        elsif (id_sort = '1' and repl_reg = '1') then
          if (idx_last = "000") then
            vec_0 <= vec_in;
          elsif (idx_last = "001") then
            vec_1 <= vec_in;
          elsif (idx_last = "010") then
            vec_2 <= vec_in;
          elsif (idx_last = "011") then
            vec_3 <= vec_in;
          elsif (idx_last = "100") then
            vec_4 <= vec_in;
          elsif (idx_last = "101") then
            vec_5 <= vec_in;
          elsif (idx_last = "110") then
            vec_6 <= vec_in;
          elsif (idx_last = "111") then
            vec_7 <= vec_in;
          end if;
        end if;
      end if;
    end process;
  end generate;
  
  o_dout <= dout;
end rtl;
