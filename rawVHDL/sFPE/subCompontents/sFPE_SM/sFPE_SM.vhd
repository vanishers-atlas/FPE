--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package sFPE_SM_pkg is
  component sFPE_SM is
    generic(
      SM_OFFSET_WIDTH     : integer  := 5;
      SM_SIZE             : integer  := 32;
      SM_ADDR_WIDTH       : integer  := 5;
      SM_DATA_WIDTH       : integer  := 16;
      USE_BRAM_FOR_LARGE_SM : boolean := true;
      SM_INIT_FILE        : string   := "IMMInit/imm_init0.mif";
      PA0_DEPTH           : integer  := 1;
      PA1_DEPTH           : integer  := 1;

      SM_OFFSET_EN        : boolean  := false;

      SM_READONLY         : boolean  := true;
      SM_WB_SET_EN0       : boolean  := false;
      SM_RB_SET_EN0       : boolean  := false;

      SM_RB_AUTOINC_SIZE0 : integer  := 1;
      SM_WB_AUTOINC_SIZE0 : integer  := 1;

      SM_RB_AUTOINC_EN0   : boolean  := true;
      SM_WB_AUTOINC_EN0   : boolean  := true;

      SM_RB_INC_EN0       : boolean  := true;
      SM_WB_INC_EN0       : boolean  := true
      );
    port(
      clk              : in std_logic;
      rst              : in std_logic;

      i_sm_rd_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
      i_sm_wr_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
      i_sm_set_rb_0    : in std_logic;
      i_sm_set_wb_0    : in std_logic;
      i_sm_inc_rb_0    : in std_logic;
      i_sm_inc_wb_0    : in std_logic;
      i_sm_autoinc_rb  : in std_logic;
      i_sm_autoinc_wb  : in std_logic;

      i_sm_wen         : in std_logic;
      i_sm_rd_ofs      : in std_logic_vector(SM_OFFSET_WIDTH-1 downto 0);
      i_sm_din         : in std_logic_vector(SM_DATA_WIDTH-1 downto 0);
      o_sm_dout        : out std_logic_vector(SM_DATA_WIDTH-1 downto 0)
    );
  end component;
end package;

----------------------------------------------------------------------------------------------

--Include packages used in definations
use std.textio.all;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

library unisim;
use unisim.vcomponents.all;

library work;
use work.generic_registers.all;

entity sFPE_SM is
  generic(
    SM_OFFSET_WIDTH     : integer  := 5;
    SM_SIZE             : integer  := 32;
    SM_ADDR_WIDTH       : integer  := 5;
    SM_DATA_WIDTH       : integer  := 16;
    USE_BRAM_FOR_LARGE_SM : boolean := true;
    SM_INIT_FILE        : string   := "IMMInit/imm_init0.mif";
    PA0_DEPTH           : integer  := 1;
    PA1_DEPTH           : integer  := 1;

    SM_OFFSET_EN        : boolean  := false;

    SM_READONLY         : boolean  := true;
    SM_WB_SET_EN0       : boolean  := false;
    SM_RB_SET_EN0       : boolean  := false;

    SM_RB_AUTOINC_SIZE0 : integer  := 1;
    SM_WB_AUTOINC_SIZE0 : integer  := 1;

    SM_RB_AUTOINC_EN0   : boolean  := true;
    SM_WB_AUTOINC_EN0   : boolean  := true;

    SM_RB_INC_EN0       : boolean  := true;
    SM_WB_INC_EN0       : boolean  := true
    );
  port(
    clk              : in std_logic;
    rst              : in std_logic;

    i_sm_rd_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
    i_sm_wr_bs       : in std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
    i_sm_set_rb_0    : in std_logic;
    i_sm_set_wb_0    : in std_logic;
    i_sm_inc_rb_0    : in std_logic;
    i_sm_inc_wb_0    : in std_logic;
    i_sm_autoinc_rb  : in std_logic;
    i_sm_autoinc_wb  : in std_logic;

    i_sm_wen         : in std_logic;
    i_sm_rd_ofs      : in std_logic_vector(SM_OFFSET_WIDTH-1 downto 0);
    i_sm_din         : in std_logic_vector(SM_DATA_WIDTH-1 downto 0);
    o_sm_dout        : out std_logic_vector(SM_DATA_WIDTH-1 downto 0)
  );
end entity;

architecture structure of sFPE_SM is

  signal sm_rd_addr, sm_wr_addr : std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
  signal sm_rd_addr_reg : std_logic_vector (SM_ADDR_WIDTH-1 downto 0);
  signal sm_set_rb_0, sm_set_wb_0 :  std_logic := '0';
  signal sm_inc_rb_0, sm_inc_wb_0 :  std_logic := '0';
  signal sm_autoinc_rb_0, sm_autoinc_wb_0 :  std_logic := '0';

  signal dod : std_logic_vector (SM_DATA_WIDTH-1 downto 0);

  type mem_type is array (0 to SM_SIZE-1) of std_logic_vector (SM_DATA_WIDTH-1 downto 0);

  impure function init_mem(mif_file_name : in string) return mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(SM_DATA_WIDTH-1 downto 0);
    variable temp_mem : mem_type;
  begin
    for i in mem_type'range loop
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

  -- LUT memory help function
  type small_mem_type is array (0 to SM_DATA_WIDTH-1) of bit_vector (2**SM_ADDR_WIDTH-1 downto 0);

  impure function init_small_mem(mif_file_name : in string) return small_mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(2**SM_ADDR_WIDTH-1 downto 0);
    variable temp_mem : small_mem_type;
  begin
    for i in small_mem_type'range loop
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
  SETRB: if (SM_RB_SET_EN0 = true) generate
    sm_set_rb_0 <= i_sm_set_rb_0;
  end generate;
  NOSETRB: if (SM_RB_SET_EN0 = false) generate
    sm_set_rb_0 <= '0';
  end generate;

  SETWB: if (SM_WB_SET_EN0 = true) generate
    sm_set_wb_0 <= i_sm_set_wb_0;
  end generate;
  NOSETWB: if (SM_WB_SET_EN0 = false) generate
    sm_set_wb_0 <= '0';
  end generate;

  RBINC: if (SM_RB_INC_EN0 = true) generate
    sm_inc_rb_0 <= i_sm_inc_rb_0;
  end generate;
  NORBINC: if (SM_RB_INC_EN0 = false) generate
    sm_inc_rb_0 <= '0';
  end generate;
  WBINC: if (SM_WB_INC_EN0 = true) generate
    sm_inc_wb_0 <= i_sm_inc_wb_0;
  end generate;
  NOWBINC: if (SM_WB_INC_EN0 = false) generate
    sm_inc_wb_0 <= '0';
  end generate;

  RBAUTOINC: if (SM_RB_AUTOINC_EN0 = true) generate
    sm_autoinc_rb_0 <= i_sm_autoinc_rb;
  end generate;
  NORBAUTOINC: if (SM_RB_AUTOINC_EN0 = false) generate
    sm_autoinc_rb_0 <= '0';
  end generate;
  WBAUTOINC: if (SM_WB_AUTOINC_EN0 = true) generate
    sm_autoinc_wb_0 <= i_sm_autoinc_wb;
  end generate;
  NOWBAUTOINC: if (SM_WB_AUTOINC_EN0 = false) generate
    sm_autoinc_wb_0 <= '0';
  end generate;

  -- Address generation
  sm_blk_gen: if (SM_OFFSET_WIDTH < SM_ADDR_WIDTH) generate
    signal sm_rofs : std_logic_vector(SM_ADDR_WIDTH-1 downto 0) := (others => '0');
    signal sm_rb_0 : std_logic_vector(SM_ADDR_WIDTH-1 downto 0) := (others => '0');
    signal sm_wb_0 : std_logic_vector(SM_ADDR_WIDTH-1 downto 0) := (others => '0');
    signal tmp  : std_logic_vector(SM_ADDR_WIDTH + SM_OFFSET_WIDTH - 1 downto 0);
    signal tmp1 : std_logic_vector(SM_ADDR_WIDTH + SM_OFFSET_WIDTH - 1 downto 0);
  begin
    tmp <= i_sm_rd_bs & (SM_OFFSET_WIDTH-1 downto 0 => '0');
    sm_rd_addr_proc: process(clk)
    begin
      if clk'event and clk = '1' then
        if sm_set_rb_0 = '1' then
          sm_rb_0 <= tmp(SM_ADDR_WIDTH-1 downto 0);
        elsif sm_inc_rb_0 = '1' then
          sm_rb_0 <= std_logic_vector(signed(i_sm_rd_bs) + signed(sm_rb_0));
        elsif sm_autoinc_rb_0 = '1' then
          sm_rb_0 <= std_logic_vector(SM_RB_AUTOINC_SIZE0 + signed(sm_rb_0));
        end if;
      end if;
    end process;

    tmp1 <= i_sm_wr_bs & (SM_OFFSET_WIDTH-1 downto 0 => '0');
    sm_wr_addr_proc: process(clk)
    begin
      if clk'event and clk = '1' then
        if sm_set_wb_0 = '1' then
          sm_wb_0 <= tmp1(SM_ADDR_WIDTH-1 downto 0);
        elsif sm_inc_wb_0 = '1' then
          sm_wb_0 <= std_logic_vector(signed(i_sm_wr_bs) + signed(sm_wb_0));
        elsif sm_autoinc_wb_0 = '1' then
          sm_wb_0 <= std_logic_vector(SM_WB_AUTOINC_SIZE0 + signed(sm_wb_0));
        end if;
      end if;
    end process;

    -- When offset is on, it is only used for simple case
    offset_en: if SM_OFFSET_EN = true generate
      assert (SM_READONLY = true)
      report "Offset is only for read-only mode!"
      severity failure;

      sm_rofs <= (SM_ADDR_WIDTH-1 downto SM_OFFSET_WIDTH => '0') & i_sm_rd_ofs;
      sm_rd_addr <= std_logic_vector(unsigned(sm_rofs) + unsigned(sm_rb_0));
    end generate;
    offset_dis: if SM_OFFSET_EN = false generate
      sm_wr_addr <= sm_wb_0;
      sm_rd_addr <= sm_rb_0;
    end generate;
  end generate;

  sm_direct_gen: if (SM_OFFSET_WIDTH = SM_ADDR_WIDTH) generate
    assert (SM_READONLY = true)
    report "Direct addressing is only for read-only only!"
    severity failure;

    sm_rd_addr <= i_sm_rd_ofs;
  end generate;

  u_sm_rd_addr_reg: generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>SM_ADDR_WIDTH)
    port map(clk=>clk, rst=>rst, i_d=>sm_rd_addr, o_d=>sm_rd_addr_reg);

  SM_READONLY_GEN: if (SM_READONLY = true) generate
    -- LUT RAM
    sm_rom_gen32: if (SM_ADDR_WIDTH = 5) generate
      constant RAM : small_mem_type := init_small_mem(SM_INIT_FILE);
    begin
      rom_unit_gen:
      for i in 0 to SM_DATA_WIDTH-1 generate
        u_rom_unit: RAM32X1S
          generic map (INIT => RAM(i))
          port map (
            O => dod(i), -- 1-bit data output
            A0 => sm_rd_addr_reg(0), -- Address[0] input bit
            A1 => sm_rd_addr_reg(1), -- Address[1] input bit
            A2 => sm_rd_addr_reg(2), -- Address[2] input bit
            A3 => sm_rd_addr_reg(3), -- Address[3] input bit
            A4 => sm_rd_addr_reg(4), -- Address[4] input bit
            D => '0', -- 1-bit data input
            WCLK => clk, -- Write clock input
            WE => '0'  -- Write enable input
          );
      end generate;
    end generate;

    sm_rom_gen64: if (SM_ADDR_WIDTH = 6) generate
      constant RAM : small_mem_type := init_small_mem(SM_INIT_FILE);
    begin
      rom_unit_gen:
      for i in 0 to (SM_DATA_WIDTH-1) generate
        u_rom_unit: RAM64X1S
          generic map (INIT => RAM(i))
          port map (
            O => dod(i), -- 1-bit data output
            A0 => sm_rd_addr_reg(0), -- Address[0] input bit
            A1 => sm_rd_addr_reg(1), -- Address[1] input bit
            A2 => sm_rd_addr_reg(2), -- Address[2] input bit
            A3 => sm_rd_addr_reg(3), -- Address[3] input bit
            A4 => sm_rd_addr_reg(4), -- Address[4] input bit
            A5 => sm_rd_addr_reg(5), -- Address[5] input bit
            D => '0', -- 1-bit data input
            WCLK => clk, -- Write clock input
            WE => '0'  -- Write enable input
          );
      end generate;
    end generate;

    large_sm_gen_lut: if (USE_BRAM_FOR_LARGE_SM = false and SM_ADDR_WIDTH > 6) generate
      type blk_type is array (natural range <>) of std_logic_vector(SM_DATA_WIDTH-1 downto 0);
      constant blk_num  : integer := natural(ceil(real(SM_SIZE)/real(64)));

      signal blk_do : blk_type(blk_num-1 downto 0);
    begin
      blk_gen: for j in 0 to blk_num-1 generate
        rom_unit_gen:
        for i in 0 to SM_DATA_WIDTH-1 generate
        u_rom_unit: RAM64X1S
          generic map (INIT => X"05020aaa0300bb0a")
          port map (
            O => blk_do(j)(i), -- 1-bit data output
            A0 => sm_rd_addr_reg(0), -- Address[0] input bit
            A1 => sm_rd_addr_reg(1), -- Address[1] input bit
            A2 => sm_rd_addr_reg(2), -- Address[2] input bit
            A3 => sm_rd_addr_reg(3), -- Address[3] input bit
            A4 => sm_rd_addr_reg(4), -- Address[4] input bit
            A5 => sm_rd_addr_reg(5), -- Address[5] input bit
            D => '0', -- 1-bit data input
            WCLK => clk, -- Write clock input
            WE => '0'  -- Write enable input
          );
        end generate;
      end generate;

      dod <= blk_do(to_integer(unsigned(sm_rd_addr_reg(SM_ADDR_WIDTH-1 downto 6))));
    end generate;

    -- BRAM
    large_imm_gen_bram:
    if (USE_BRAM_FOR_LARGE_SM = true and SM_ADDR_WIDTH > 6) generate
      signal RAM : mem_type := init_mem(SM_INIT_FILE);
    begin
      process (clk)
      begin
        if (clk'event and clk = '1') then
          dod <= RAM(to_integer(unsigned(sm_rd_addr)));
        end if;
      end process;
    end generate;

    -- output pipeline
    u_sm_dout_reg: generic_reg
      generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>SM_DATA_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dod, o_d=>o_sm_dout);
  end generate;

  SM_NOT_READONLY_GEN: if (SM_READONLY = false) generate
    -----------------------------------------------------------------
    -- LUT RAM
    -----------------------------------------------------------------
    -- 32-entry
    sm_rom_gen32:
    if (SM_ADDR_WIDTH = 5) generate
      ram_unit_gen:
      for i in 0 to SM_DATA_WIDTH-1 generate
        u_ram_unit: RAM32X1D
          generic map (INIT => X"00000000")
          port map (
            DPO => dod(i), -- Read-only 1-bit data output
            A0 => sm_wr_addr(0), -- R/W address[0] input bit
            A1 => sm_wr_addr(1), -- R/W address[1] input bit
            A2 => sm_wr_addr(2), -- R/W address[2] input bit
            A3 => sm_wr_addr(3), -- R/W address[3] input bit
            A4 => sm_wr_addr(4), -- R/W address[4] input bit
            D => i_sm_din(i), -- Write 1-bit data input
            DPRA0 => sm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => sm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => sm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => sm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => sm_rd_addr_reg(4), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => i_sm_wen -- Write enable input
          );
      end generate;

      u_sm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>SM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dod, o_d=>o_sm_dout);
    end generate;

    -- 64-entry
    sm_rom_gen64:
    if (SM_ADDR_WIDTH = 6) generate
      ram_unit_gen:
      for i in 0 to (SM_DATA_WIDTH-1) generate
        u_ram_unit: RAM64X1D
          generic map (INIT => X"0000000000000000")
          port map (
            DPO => dod(i), -- Read-only 1-bit data output
            A0 => sm_wr_addr(0), -- R/W address[0] input bit
            A1 => sm_wr_addr(1), -- R/W address[1] input bit
            A2 => sm_wr_addr(2), -- R/W address[2] input bit
            A3 => sm_wr_addr(3), -- R/W address[3] input bit
            A4 => sm_wr_addr(4), -- R/W address[4] input bit
            A5 => sm_wr_addr(5),
            D => i_sm_din(i), -- Write 1-bit data input
            DPRA0 => sm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => sm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => sm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => sm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => sm_rd_addr_reg(4), -- Read-only address[4] input bit
            DPRA5 => sm_rd_addr_reg(5), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => i_sm_wen -- Write enable input
          );
      end generate;

      u_sm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>SM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dod, o_d=>o_sm_dout);
    end generate;

    large_lut_memory_gen:
    if (USE_BRAM_FOR_LARGE_SM = false and SM_ADDR_WIDTH > 6) generate
      type blk_type is array (natural range <>) of std_logic_vector(SM_DATA_WIDTH-1 downto 0);
      type blk_signal_type is array (natural range <>) of std_logic;
      constant blk_num  : integer := natural(ceil(real(SM_SIZE)/real(64)));

      signal blk_do : blk_type(blk_num-1 downto 0);
      signal wen    : blk_signal_type(blk_num-1 downto 0);
    begin
      blk_gen:
      for j in 0 to blk_num-1 generate
        sm_unit_gen:
        for i in 0 to SM_DATA_WIDTH-1 generate
        u_sm_unit: RAM64X1D
          generic map ( INIT => X"0000000000000000")
          port map (
            DPO => blk_do(j)(i), -- Read-only 1-bit data output
            A0 => sm_wr_addr(0), -- R/W address[0] input bit
            A1 => sm_wr_addr(1), -- R/W address[1] input bit
            A2 => sm_wr_addr(2), -- R/W address[2] input bit
            A3 => sm_wr_addr(3), -- R/W address[3] input bit
            A4 => sm_wr_addr(4), -- R/W address[4] input bit
            A5 => sm_wr_addr(5),
            D => i_sm_din(i), -- Write 1-bit data input
            DPRA0 => sm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => sm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => sm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => sm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => sm_rd_addr_reg(4), -- Read-only address[4] input bit
            DPRA5 => sm_rd_addr_reg(5), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => wen(j) -- Write enable input
          );
        end generate;
      end generate;

      -- Demux write signal
      sm_write: process (sm_wr_addr, i_sm_wen)
      begin
        wen <= (others=>'0');
        if (i_sm_wen = '1') then
          if to_integer(unsigned(sm_wr_addr(SM_ADDR_WIDTH-1 downto 6))) < blk_num then
            wen(to_integer(unsigned(sm_wr_addr(SM_ADDR_WIDTH-1 downto 6)))) <= i_sm_wen;
          end if;
        end if;
      end process;

      dod <= blk_do(to_integer(unsigned(sm_rd_addr_reg(SM_ADDR_WIDTH-1 downto 6))));

      u_sm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>SM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dod, o_d=>o_sm_dout);

    end generate;

    -----------------------------------------------------------------
    -- Block RAM (Dual-Port)
    -----------------------------------------------------------------
    sm_bram_gen:
    if (USE_BRAM_FOR_LARGE_SM = true and SM_ADDR_WIDTH > 6) generate
      signal RAM : mem_type := init_mem(SM_INIT_FILE);
    begin
      process (clk)
      begin
        if (clk'event and clk = '1') then
          if i_sm_wen = '1' then
            RAM(to_integer(unsigned(sm_wr_addr))) <= i_sm_din;
          end if;
          dod  <= RAM(to_integer(unsigned(sm_rd_addr)));
        end if;
      end process;

      process (clk) begin
        if (clk'event and clk = '1') then
            o_sm_dout <= dod;
        end if;
      end process;
    end generate;
  end generate;
end architecture;
