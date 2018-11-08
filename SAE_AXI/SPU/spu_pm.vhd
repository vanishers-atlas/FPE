library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

library unisim;
use unisim.vcomponents.all;
library work;
use work.ssp_pkg.all;
use std.textio.all;

entity spu_pm is
  generic (
    PM_SIZE        : integer := 4095;
    PM_ADDR_WIDTH  : integer := 12;
    PM_DATA_WIDTH  : integer := 32;
    USE_BRAM_FOR_LARGE_PM   : boolean := true;
    PM_INIT_FILE: string := "PMInit/pm_initSPU0PE0.mif";
    PB0_DEPTH   : integer  := 1;
    PB1_DEPTH   : integer  := 1
  );
  port (
    clk    :  in std_logic := '0';
    rst    :  in std_logic := '0';
    i_en   :  in std_logic := '1';
    
    i_addr  :  in std_logic_vector (PM_ADDR_WIDTH-1 downto 0) := (others => '0');
    o_pm  :  out std_logic_vector (PM_DATA_WIDTH-1 downto 0) := (others => '0')
  );
end spu_pm;

architecture structure of spu_pm is

type infer_mem_type is array (0 to PM_SIZE-1) of std_logic_vector (PM_DATA_WIDTH-1 downto 0);

impure function infer_init_mem(mif_file_name : in string) return infer_mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(PM_DATA_WIDTH-1 downto 0);
    variable temp_mem : infer_mem_type;
begin
    for i in infer_mem_type'range loop
      if ENDFILE(mif_file) then
        exit;
      else
        readline(mif_file, mif_line);
        read(mif_line, temp_bv);
        temp_mem(i) := to_stdlogicvector(temp_bv);
      end if;
    end loop;
    return temp_mem;
end function;

type lut_mem_type is array (0 to PM_DATA_WIDTH-1) of bit_vector (2**PM_ADDR_WIDTH-1 downto 0);

impure function init_lut_mem_32_64(mif_file_name : in string) return lut_mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(2**PM_ADDR_WIDTH-1 downto 0);
    variable temp_mem : lut_mem_type;
begin
    for i in lut_mem_type'range loop
      if ENDFILE(mif_file) then
        exit;
      else
        readline(mif_file, mif_line);
        read(mif_line, temp_bv);
        temp_mem(i) := temp_bv;
      end if;
    end loop;
    return temp_mem;
end function;

type lut_block_mem_type is array (0 to natural(ceil(real(PM_SIZE)/real(64)))*PM_DATA_WIDTH-1) of bit_vector (63 downto 0);

impure function init_lut_block_mem(mif_file_name : in string) return lut_block_mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(63 downto 0);
    variable temp_mem : lut_block_mem_type;
begin
    for i in lut_block_mem_type'range loop
      if ENDFILE(mif_file) then
        exit;
      else
        readline(mif_file, mif_line);
        read(mif_line, temp_bv);
        temp_mem(i) := temp_bv;
      end if;
    end loop;
    return temp_mem;
end function;

  begin
  
  pm_rom_gen32:
  if (PM_ADDR_WIDTH = 5) generate
    signal pm_do : std_logic_vector (PM_DATA_WIDTH-1 downto 0);
    constant RAM : lut_mem_type := init_lut_mem_32_64(PM_INIT_FILE);
    signal addr_Pb0 : std_logic_vector (PM_ADDR_WIDTH-1 downto 0) := (others=>'0');
  begin  
    u_pm_reg_Pb0: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB0_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>i_addr, o_d=>addr_Pb0);
    
    rom_unit_gen: 
    for i in 0 to PM_DATA_WIDTH-1 generate
      u_rom_unit: RAM32X1S
      generic map (
      INIT => RAM(i))
      port map (
      O => pm_do(i), -- 1-bit data output
      A0 => addr_Pb0(0), -- Address[0] input bit
      A1 => addr_Pb0(1), -- Address[1] input bit
      A2 => addr_Pb0(2), -- Address[2] input bit
      A3 => addr_Pb0(3), -- Address[3] input bit
      A4 => addr_Pb0(4), -- Address[4] input bit
      D => '0', -- 1-bit data input
      WCLK => clk, -- Write clock input
      WE => '0'  -- Write enable input
      );        
    end generate;
    
    u_pm_reg_Pb1: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB1_DEPTH, REG_WIDTH=>PM_DATA_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>pm_do, o_d=>o_pm);
    
  end generate;
  
  pm_rom_gen64: 
  if (PM_ADDR_WIDTH = 6) generate
    signal pm_do : std_logic_vector (PM_DATA_WIDTH-1 downto 0) := (others=>'0');
    constant RAM : lut_mem_type := init_lut_mem_32_64(PM_INIT_FILE);
    signal addr_Pb0 : std_logic_vector (PM_ADDR_WIDTH-1 downto 0) := (others=>'0');
  begin  
    u_pm_reg_Pb0: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB0_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>i_addr, o_d=>addr_Pb0);
  
    rom_unit_gen: 
    for i in 0 to (PM_DATA_WIDTH-1) generate
      u_rom_unit: RAM64X1S
      generic map (
      INIT => RAM(i))
      port map (
      O => pm_do(i), -- 1-bit data output
      A0 => addr_Pb0(0), -- Address[0] input bit
      A1 => addr_Pb0(1), -- Address[1] input bit
      A2 => addr_Pb0(2), -- Address[2] input bit
      A3 => addr_Pb0(3), -- Address[3] input bit
      A4 => addr_Pb0(4), -- Address[4] input bit
      A5 => addr_Pb0(5), -- Address[5] input bit
      D => '0', -- 1-bit data input
      WCLK => clk, -- Write clock input
      WE => '0'  -- Write enable input
      );
    end generate;
    
    u_pm_reg_Pb1: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB1_DEPTH, REG_WIDTH=>PM_DATA_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>pm_do, o_d=>o_pm);
  end generate;
  
  large_pm_gen_lut:
  if (USE_BRAM_FOR_LARGE_PM = false and PM_ADDR_WIDTH > 6) generate
    type blk_type is array (natural range <>) of std_logic_vector(PM_DATA_WIDTH-1 downto 0); 
    constant blk_num  : integer := natural(ceil(real(PM_SIZE)/real(64)));
    constant RAM : lut_block_mem_type := init_lut_block_mem(PM_INIT_FILE);
    signal blk_do : blk_type(blk_num-1 downto 0);
    signal pm_do : std_logic_vector(PM_DATA_WIDTH-1 downto 0);    
    signal addr_Pb0 : std_logic_vector (PM_ADDR_WIDTH-1 downto 0) := (others=>'0');
  begin  
    u_pm_reg_Pb0: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB0_DEPTH, REG_WIDTH=>PM_ADDR_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>i_addr, o_d=>addr_Pb0);
    
    blk_gen:
    for j in 0 to blk_num-1 generate
      rom_unit_gen: 
      for i in 0 to PM_DATA_WIDTH-1 generate
      u_rom_unit: RAM64X1S
      generic map (
      INIT => RAM(j*PM_DATA_WIDTH+i))
      port map (
      O => blk_do(j)(i), -- 1-bit data output
      A0 => addr_Pb0(0), -- Address[0] input bit
      A1 => addr_Pb0(1), -- Address[1] input bit
      A2 => addr_Pb0(2), -- Address[2] input bit
      A3 => addr_Pb0(3), -- Address[3] input bit
      A4 => addr_Pb0(4), -- Address[4] input bit
      A5 => addr_Pb0(5), -- Address[5] input bit
      D => '0', -- 1-bit data input
      WCLK => clk, -- Write clock input
      WE => '0'  -- Write enable input
      );
      end generate;
    end generate;

    pm_do <= blk_do(to_integer(unsigned(addr_Pb0(PM_ADDR_WIDTH-1 downto 6))));
    u_pm_reg_Pb1: spu_generic_reg_with_en 
    generic map(REG_NUM=>PB1_DEPTH, REG_WIDTH=>PM_DATA_WIDTH) 
    port map(clk=>clk, rst=>rst, i_en=>i_en, i_d=>pm_do, o_d=>o_pm);
    
  end generate;
  
--   BRAM generation  
  large_pm_gen_bram:
  if (USE_BRAM_FOR_LARGE_PM = true and PM_ADDR_WIDTH > 6) generate    
    signal pm_do_reg : std_logic_vector(PM_DATA_WIDTH-1 downto 0)  := (others=>'0');
    signal RAM : infer_mem_type := infer_init_mem(PM_INIT_FILE);    
  begin
    -- Pipeline b0 is implied in BRAM's input register
    process (clk) begin
      if (clk'event and clk = '1') then
        if (i_en = '1') then
          pm_do_reg <= RAM(to_integer(unsigned(i_addr)));
        end if;
      end if;
    end process;
    
    process (clk) begin
      if (clk'event and clk = '1') then
        if (i_en = '1') then
          o_pm <= pm_do_reg;
        end if;
      end if;
    end process;
  end generate;
  
end structure;
