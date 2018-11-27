--Include packages used in package declaration
library ieee;
use ieee.std_logic_1164.all;

package sFPE_DM_pkg is
  component sFPE_DM is
    generic (
      DM_OFFSET_WIDTH      : integer:= 5;
      DM_SIZE              : integer:= 64;
      DM_ADDR_WIDTH        : integer:= 6;
      DM_DATA_WIDTH        : integer:= 16;
      DM_INIT_EN           : boolean:= false;
      USE_BRAM_FOR_LARGE_DM: boolean:= true;
      DM_INIT_FILE         : string := "mem.dat";
      DM_TWO_RD_PORTS      : boolean:= true;
      -- This parameter indicates using duplicated memory storage
      -- for two read and one write operation.
      DM_TRUE_2R1W         : boolean:= false;

      PA0_DEPTH            : integer:= 1;
      PA1_DEPTH            : integer:= 1
    );
    port (
      clk                  :  in std_logic;
      rst                  :  in std_logic;

      i_dm_rd_addr_0       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
      i_dm_rd_addr_1       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
      i_dm_wr_addr         :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);

      i_dm_wen             :  in std_logic;
      i_dm_din             :  in std_logic_vector (DM_DATA_WIDTH-1 downto 0);

      o_dm_dout0           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0);
      o_dm_dout1           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0)
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
use work.generic_multiplexers.all;

-- FFT has needs: direct addressing or base+offset addressing
-- Others: base + inc/autoinc
entity sFPE_DM is
  generic (
    DM_OFFSET_WIDTH      : integer:= 5;
    DM_SIZE              : integer:= 64;
    DM_ADDR_WIDTH        : integer:= 6;
    DM_DATA_WIDTH        : integer:= 16;
    DM_INIT_EN           : boolean:= false;
    USE_BRAM_FOR_LARGE_DM: boolean:= true;
    DM_INIT_FILE         : string := "mem.dat";
    DM_TWO_RD_PORTS      : boolean:= true;
    -- This parameter indicates using duplicated memory storage
    -- for two read and one write operation.
    DM_TRUE_2R1W         : boolean:= false;

    PA0_DEPTH            : integer:= 1;
    PA1_DEPTH            : integer:= 1
  );
  port (
    clk                  :  in std_logic;
    rst                  :  in std_logic;

    i_dm_rd_addr_0       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    i_dm_rd_addr_1       :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    i_dm_wr_addr         :  in std_logic_vector (DM_ADDR_WIDTH-1 downto 0);

    i_dm_wen             :  in std_logic;
    i_dm_din             :  in std_logic_vector (DM_DATA_WIDTH-1 downto 0);

    o_dm_dout0           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0);
    o_dm_dout1           :  out std_logic_vector (DM_DATA_WIDTH-1 downto 0)
  );
end entity;

architecture structure of sFPE_DM is

signal dm_rd_addr_m, dm_rd_addr_n, dm_wr_addr : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);

--**
--* Function init_mem. Initialise an Block RAM.
--*
--* @para mif_file_name The input MIF file name
--**
type mem_type is array (0 to DM_SIZE-1) of std_logic_vector (DM_DATA_WIDTH-1 downto 0);

impure function init_mem(mif_file_name : in string) return mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(DM_DATA_WIDTH-1 downto 0);
    variable temp_mem : mem_type;
begin
    if DM_INIT_EN = true then
      for i in mem_type'range loop
        if ENDFILE(mif_file) then
          exit;
        else
          readline(mif_file, mif_line);
          read(mif_line, temp_bv);
          temp_mem(i) := to_stdlogicvector(temp_bv);
        end if;
      end loop;
    end if;

    return temp_mem;
end function;

type small_mem_type is array (0 to DM_DATA_WIDTH-1) of bit_vector (2**DM_ADDR_WIDTH-1 downto 0);

--**
--* Function init_small_mem. Initialise an LUT RAM.
--*
--* @para mif_file_name The input MIF file name
--**
impure function init_small_mem(mif_file_name : in string) return small_mem_type is
    file mif_file : text open read_mode is mif_file_name;
    variable mif_line : line;
    variable temp_bv : bit_vector(2**DM_ADDR_WIDTH-1 downto 0);
    variable temp_mem : small_mem_type;
begin
    if DM_INIT_EN = true then
      for i in small_mem_type'range loop
        if ENDFILE(mif_file) then
          exit;
        else
          readline(mif_file, mif_line);
          read(mif_line, temp_bv);
          temp_mem(i) := temp_bv;
        end if;
      end loop;
    end if;

    return temp_mem;
end function;

begin
  process (i_dm_wr_addr) begin
    if (to_integer(unsigned( i_dm_wr_addr )) >= DM_SIZE) then
      dm_wr_addr <= (DM_ADDR_WIDTH-1 downto 0 =>'0');
    else
      dm_wr_addr   <= i_dm_wr_addr;
    end if;
  end process;

  process (i_dm_rd_addr_0) begin
    if (to_integer(unsigned( i_dm_rd_addr_0 )) >= DM_SIZE) then
      dm_rd_addr_m <= (DM_ADDR_WIDTH-1 downto 0 =>'0');
    else
      dm_rd_addr_m   <= i_dm_rd_addr_0;
    end if;
  end process;


  process (i_dm_rd_addr_1) begin
    if (to_integer(unsigned( i_dm_rd_addr_1 )) >= DM_SIZE) then
      dm_rd_addr_n <= (DM_ADDR_WIDTH-1 downto 0 =>'0');
    else
      dm_rd_addr_n   <= i_dm_rd_addr_1;
    end if;
  end process;

  -----------------------------------------------------------------
  -- LUT RAM
  -----------------------------------------------------------------
  -- 32-entry
  dm_rom_gen32:
  if (DM_ADDR_WIDTH = 5) generate
    signal dm_do  : std_logic_vector (DM_DATA_WIDTH-1 downto 0);
    signal dm_do1 : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    constant RAM : small_mem_type := init_small_mem(DM_INIT_FILE);
    signal dm_rd_addr_reg : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    signal dm_rd_addr1_reg : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
  begin
    u_dm_rdaddr_reg: generic_reg
      generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_m, o_d=>dm_rd_addr_reg);

    -- This is the default case
    ONE_READ_GEN: if (DM_TWO_RD_PORTS = false) generate
      ram_unit_gen:
      for i in 0 to DM_DATA_WIDTH-1 generate
        u_ram_unit: RAM32X1D
        generic map ( INIT => RAM(i))
        port map (
          DPO => dm_do(i), -- Read-only 1-bit data output
          A0 => dm_wr_addr(0), -- R/W address[0] input bit
          A1 => dm_wr_addr(1), -- R/W address[1] input bit
          A2 => dm_wr_addr(2), -- R/W address[2] input bit
          A3 => dm_wr_addr(3), -- R/W address[3] input bit
          A4 => dm_wr_addr(4), -- R/W address[4] input bit
          D => i_dm_din(i), -- Write 1-bit data input
          DPRA0 => dm_rd_addr_reg(0), -- Read-only address[0] input bit
          DPRA1 => dm_rd_addr_reg(1), -- Read-only address[1] input bit
          DPRA2 => dm_rd_addr_reg(2), -- Read-only address[2] input bit
          DPRA3 => dm_rd_addr_reg(3), -- Read-only address[3] input bit
          DPRA4 => dm_rd_addr_reg(4), -- Read-only address[4] input bit
          WCLK => clk, -- Write clock input
          WE => i_dm_wen -- Write enable input
        );
      end generate;

      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
    end generate;

    -- True two ports case. Used in M64S1 802.11ac
    -- The init data is not supported.
    TRUE_R_W: if (DM_TWO_RD_PORTS = true) generate
      u_dm_rdaddr1_reg: generic_reg
        generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_n, o_d=>dm_rd_addr1_reg);

      ram_unit_gen:
      for n in 0 to DM_DATA_WIDTH/2-1 generate
        u_ram_unit: RAM32M
        generic map (
          INIT_A => X"0000000000000000", -- Initial contents of A port
          INIT_B => X"0000000000000000", -- Initial contents of B port
          INIT_C => X"0000000000000000", -- Initial contents of C port
          INIT_D => X"0000000000000000"  -- Initial contents of D port
        )
        port map (
          DOA => dm_do((2*n +1) downto (2*n)), -- Read port A 2-bit output
          DOB => dm_do1((2*n +1) downto (2*n)), -- Read port B 2-bit output
          DOC => open, -- Read port C 2-bit output
          DOD => open, -- Read/Write port D 2-bit output
          ADDRA => dm_rd_addr_reg, -- Read port A 5-bit address input
          ADDRB => dm_rd_addr1_reg, -- Read port B 5-bit address input
          ADDRC => "00000", -- Read port C 5-bit address input
          ADDRD => dm_wr_addr, -- Read/Write port D 5-bit address input
          DIA => i_dm_din((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIB => i_dm_din((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIC => i_dm_din((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DID => i_dm_din((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          WCLK => clk, -- Write clock input
          WE => i_dm_wen -- Write enable input
        );
      end generate;

      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
      u_dm_dout1_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do1, o_d=>o_dm_dout1);
    end generate;
  end generate;

  -- 64-entry
  dm_rom_gen64:
  if (DM_ADDR_WIDTH = 6) generate
    signal dm_do : std_logic_vector (DM_DATA_WIDTH-1 downto 0);
    signal dm_do1 : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    constant RAM : small_mem_type := init_small_mem(DM_INIT_FILE);
    signal dm_rd_addr_reg  : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    signal dm_rd_addr1_reg : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
  begin
    u_dm_rdaddr_reg: generic_reg
      generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_m, o_d=>dm_rd_addr_reg);

    ONE_READ_GEN: if (DM_TWO_RD_PORTS = false) generate
      ram_unit_gen: for i in 0 to (DM_DATA_WIDTH-1) generate
        u_ram_unit: RAM64X1D
          generic map (INIT => RAM(i))
          port map (
            DPO => dm_do(i), -- Read-only 1-bit data output
            A0 => dm_wr_addr(0), -- R/W address[0] input bit
            A1 => dm_wr_addr(1), -- R/W address[1] input bit
            A2 => dm_wr_addr(2), -- R/W address[2] input bit
            A3 => dm_wr_addr(3), -- R/W address[3] input bit
            A4 => dm_wr_addr(4), -- R/W address[4] input bit
            A5 => dm_wr_addr(5),
            D => i_dm_din(i), -- Write 1-bit data input
            DPRA0 => dm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => dm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => dm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => dm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => dm_rd_addr_reg(4), -- Read-only address[4] input bit
            DPRA5 => dm_rd_addr_reg(5), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => i_dm_wen -- Write enable input
          );
      end generate;

      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
    end generate;

    TRUE_R_W: if (DM_TWO_RD_PORTS = true) generate
      u_dm_rdaddr1_reg: generic_reg
        generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_n, o_d=>dm_rd_addr1_reg);
      ram_unit_gen: for n in 0 to DM_DATA_WIDTH-1 generate
        u_ram_unit: RAM64M
          generic map (
            INIT_A => X"0000000000000000", -- Initial contents of A port
            INIT_B => X"0000000000000000", -- Initial contents of B port
            INIT_C => X"0000000000000000", -- Initial contents of C port
            INIT_D => X"0000000000000000"  -- Initial contents of D port
          )
          port map (
            DOA => dm_do(n), -- Read port A 1-bit output
            DOB => dm_do1(n), -- Read port B 1-bit output
            DOC => open, -- Read port C 1-bit output
            DOD => open, -- Read/Write port D 1-bit output
            ADDRA => dm_rd_addr_reg, -- Read port A 6-bit address input
            ADDRB => dm_rd_addr1_reg, -- Read port B 6-bit address input
            ADDRC => "000000", -- Read port C 6-bit address input
            ADDRD => dm_wr_addr, -- Read/Write port D 6-bit address input
            DIA => i_dm_din(n), -- RAM 1-bit data write input addressed by ADDRD,
            DIB => i_dm_din(n), -- RAM 1-bit data write input addressed by ADDRD,
            DIC => i_dm_din(n), -- RAM 1-bit data write input addressed by ADDRD,
            DID => i_dm_din(n), -- RAM 1-bit data write input addressed by ADDRD,
            WCLK => clk, -- Write clock input
            WE => i_dm_wen -- Write enable input
          );
		end generate;
      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
      u_dm_dout1_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do1, o_d=>o_dm_dout1);
    end generate;
  end generate;

  large_lut_memory_gen:
  if (USE_BRAM_FOR_LARGE_DM = false and DM_ADDR_WIDTH > 6) generate
    type blk_type is array (natural range <>) of std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    type blk_signal_type is array (natural range <>) of std_logic;
    constant blk_num  : integer := natural(ceil(real(DM_SIZE)/real(64)));

    signal blk_do : blk_type(blk_num-1 downto 0);
    signal blk_do1 : blk_type(blk_num-1 downto 0);
    signal dm_do  : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    signal dm_do1  : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    signal wen    : blk_signal_type(blk_num-1 downto 0);
    signal dm_rd_addr_reg : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);
    signal dm_rd_addr1_reg : std_logic_vector (DM_ADDR_WIDTH-1 downto 0);

    signal addr_mux : std_logic_vector(DM_ADDR_WIDTH-1 downto 0);
  begin
    u_dm_rdaddr_reg: generic_reg
      generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_m, o_d=>dm_rd_addr_reg);

    -- Demux write signal
    dm_write: process (dm_wr_addr, i_dm_wen)
    begin
      wen <= (others=>'0');
      if (i_dm_wen = '1') then
        if to_integer(unsigned(dm_wr_addr(DM_ADDR_WIDTH-1 downto 6))) < blk_num then
          wen(to_integer(unsigned(dm_wr_addr(DM_ADDR_WIDTH-1 downto 6)))) <= i_dm_wen;
        end if;
      end if;
    end process;

    ONERD_GEN: if (DM_TWO_RD_PORTS = false) generate
      blk_gen: for j in 0 to blk_num-1 generate
        dm_unit_gen: for i in 0 to DM_DATA_WIDTH-1 generate
          u_dm_unit: RAM64X1D
          generic map ( INIT => X"0000000000000000")
          port map (
            DPO => blk_do(j)(i), -- Read-only 1-bit data output
            A0 => dm_wr_addr(0), -- R/W address[0] input bit
            A1 => dm_wr_addr(1), -- R/W address[1] input bit
            A2 => dm_wr_addr(2), -- R/W address[2] input bit
            A3 => dm_wr_addr(3), -- R/W address[3] input bit
            A4 => dm_wr_addr(4), -- R/W address[4] input bit
            A5 => dm_wr_addr(5),
            D => i_dm_din(i), -- Write 1-bit data input
            DPRA0 => dm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => dm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => dm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => dm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => dm_rd_addr_reg(4), -- Read-only address[4] input bit
            DPRA5 => dm_rd_addr_reg(5), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => wen(j) -- Write enable input
          );
        end generate;
      end generate;

      dm_do <= blk_do(to_integer(unsigned(dm_rd_addr_reg(DM_ADDR_WIDTH-1 downto 6))));
      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
    end generate;

    TWORD_GEN: if (DM_TWO_RD_PORTS = true) generate
      assert (DM_TRUE_2R1W = false)
      report "When using LUT for large DM, true two read ports has not yet supported"
      severity failure;


      u_dm_rdaddr1_reg: generic_reg
        generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>DM_ADDR_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_rd_addr_n, o_d=>dm_rd_addr1_reg);

      u_mux:generic_mux_2to1
        generic map(DATA_WIDTH=>DM_ADDR_WIDTH)
        port map(i_d0=>dm_rd_addr1_reg, i_d1=>dm_wr_addr, sel=>i_dm_wen, o_d=>addr_mux);

      blk_gen: for j in 0 to blk_num-1 generate
        dm_unit_gen:  for i in 0 to DM_DATA_WIDTH-1 generate
        u_dm_unit: RAM64X1D
          generic map (INIT => X"0000000000000000")
          port map (
            DPO => blk_do(j)(i),  -- Read-only 1-bit data output
            SPO => blk_do1(j)(i), -- R/W 1-bit data output
            A0 => addr_mux(0), -- R/W address[0] input bit
            A1 => addr_mux(1), -- R/W address[1] input bit
            A2 => addr_mux(2), -- R/W address[2] input bit
            A3 => addr_mux(3), -- R/W address[3] input bit
            A4 => addr_mux(4), -- R/W address[4] input bit
            A5 => addr_mux(5),
            D => i_dm_din(i), -- Write 1-bit data input
            DPRA0 => dm_rd_addr_reg(0), -- Read-only address[0] input bit
            DPRA1 => dm_rd_addr_reg(1), -- Read-only address[1] input bit
            DPRA2 => dm_rd_addr_reg(2), -- Read-only address[2] input bit
            DPRA3 => dm_rd_addr_reg(3), -- Read-only address[3] input bit
            DPRA4 => dm_rd_addr_reg(4), -- Read-only address[4] input bit
            DPRA5 => dm_rd_addr_reg(5), -- Read-only address[4] input bit
            WCLK => clk, -- Write clock input
            WE => wen(j) -- Write enable input
          );
        end generate;
      end generate;
      dm_do <= blk_do(to_integer(unsigned(dm_rd_addr_reg(DM_ADDR_WIDTH-1 downto 6))));
      u_dm_dout_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do, o_d=>o_dm_dout0);
      dm_do1 <= blk_do1(to_integer(unsigned(dm_rd_addr1_reg(DM_ADDR_WIDTH-1 downto 6))));
      u_dm_dout1_reg: generic_reg
        generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>DM_DATA_WIDTH)
        port map(clk=>clk, rst=>rst, i_d=>dm_do1, o_d=>o_dm_dout1);
    end generate;
  end generate; -- large_lut_memory

  -----------------------------------------------------------------
  -- Block RAM (Dual-Port)
  -----------------------------------------------------------------
  dm_bram_gen:
  if (USE_BRAM_FOR_LARGE_DM = true and DM_ADDR_WIDTH > 6) generate
    signal dm_rd_addr_reg : std_logic_vector(DM_ADDR_WIDTH-1 downto 0);
    signal RAM : mem_type := init_mem(DM_INIT_FILE);
    signal dm_do0  : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
    signal dm_do1  : std_logic_vector(DM_DATA_WIDTH-1 downto 0);
  begin
    TWO_READ_GEN: if (DM_TWO_RD_PORTS = true) generate
      TRUE_2R1W: if (DM_TRUE_2R1W = true) generate
        process (clk)
        begin
          if (clk'event and clk = '1') then
            if i_dm_wen = '1' then
              RAM(to_integer(unsigned(dm_wr_addr))) <= i_dm_din;
            end if;
            dm_do1  <= RAM(to_integer(unsigned(dm_rd_addr_n)));
            dm_do0  <= RAM(to_integer(unsigned(dm_rd_addr_m)));
            o_dm_dout0 <= dm_do0;
            o_dm_dout1 <= dm_do1;
          end if;
        end process;
      end generate;

      SHARED_R_W: if (DM_TRUE_2R1W = false) generate
        signal addr_mux : std_logic_vector(DM_ADDR_WIDTH-1 downto 0);
      begin
        u_mux:generic_mux_2to1
          generic map(DATA_WIDTH=>DM_ADDR_WIDTH)
          port map(i_d0=>dm_rd_addr_n, i_d1=>dm_wr_addr, sel=>i_dm_wen, o_d=>addr_mux);

        process (clk)
        begin
          if (clk'event and clk = '1') then
            if i_dm_wen = '1' then
              RAM(to_integer(unsigned(addr_mux))) <= i_dm_din;
            else
              dm_do1  <= RAM(to_integer(unsigned(addr_mux)));
            end if;
            dm_do0  <= RAM(to_integer(unsigned(dm_rd_addr_m)));
            o_dm_dout0 <= dm_do0;
            o_dm_dout1 <= dm_do1;
          end if;
        end process;
      end generate;
    end generate;

    ONE_READ_GEN: if (DM_TWO_RD_PORTS = false) generate
      process (clk)
      begin
        if (clk'event and clk = '1') then
          if i_dm_wen = '1' then
            RAM(to_integer(unsigned(dm_wr_addr))) <= i_dm_din;
          end if;
          dm_do0  <= RAM(to_integer(unsigned(dm_rd_addr_m)));
          o_dm_dout0 <= dm_do0;
        end if;
      end process;
    end generate;
  end generate;
end architecture;
