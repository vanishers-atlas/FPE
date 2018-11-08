library ieee;
use ieee.std_logic_1164.all;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_unsigned.all;
--use ieee.numeric_std.all;
library unisim;
use unisim.vcomponents.all;
library work;
use work.ssp_pkg.all;
use std.textio.all;

entity spu_rf is
  generic (
    RF_ADDR_WIDTH  : integer := 5;
    RF_DATA_WIDTH  : integer := 16;
    FRAC_BITS      : integer := 8;    
    RF_INIT_EN : boolean := true;
    RF_INIT_FILE: string := "RFInit/rf_init0.mif";
    PA0_DEPTH  : integer  := 1;
    PA1_DEPTH  : integer  := 1
  );
  port (
    clk: in std_logic;
    rst: in std_logic;

    i_rdaddr_a : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_rdaddr_b : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_rdaddr_c : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    o_rddata_a : out std_logic_vector (RF_DATA_WIDTH-1 downto 0);
    o_rddata_b : out std_logic_vector (RF_DATA_WIDTH-1 downto 0) ;
    o_rddata_c : out std_logic_vector (RF_DATA_WIDTH-1 downto 0);

    i_wraddr_d : in  std_logic_vector (RF_ADDR_WIDTH-1 downto 0);
    i_wrdata_d : in std_logic_vector (RF_DATA_WIDTH-1 downto 0);
    i_wen      : in std_logic
  );
end spu_rf;

architecture structure of spu_rf is
  signal rddata_a :std_logic_vector(RF_DATA_WIDTH-1 downto 0);
  signal rddata_b :std_logic_vector(RF_DATA_WIDTH-1 downto 0);
  signal rddata_c :std_logic_vector(RF_DATA_WIDTH-1 downto 0);
  signal rdaddr_a :std_logic_vector(RF_ADDR_WIDTH-1 downto 0);
  signal rdaddr_b :std_logic_vector(RF_ADDR_WIDTH-1 downto 0);
  signal rdaddr_c :std_logic_vector(RF_ADDR_WIDTH-1 downto 0);
  
  type rf32_type is array (0 to RF_DATA_WIDTH/2-1) of bit_vector (63 downto 0);

  impure function init_lut_mem_32(mif_file_name : in string) return rf32_type is
      file mif_file : text open read_mode is mif_file_name;
      variable mif_line : line;
      variable temp_bv : bit_vector(63 downto 0);
      variable temp_mem : rf32_type;
  begin
      for i in rf32_type'range loop
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
  
  type rf64_type is array (0 to RF_DATA_WIDTH-1) of bit_vector (2**RF_ADDR_WIDTH-1 downto 0);

  impure function init_lut_mem_64(mif_file_name : in string) return rf64_type is
      file mif_file : text open read_mode is mif_file_name;
      variable mif_line : line;
      variable temp_bv : bit_vector(2**RF_ADDR_WIDTH-1 downto 0);
      variable temp_mem : rf64_type;
  begin
      for i in rf64_type'range loop
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
  -- Address registering
  u_rdaddr_a_Pa0: spu_generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>i_rdaddr_a, o_d=>rdaddr_a);
  
  u_rdaddr_b_Pa0: spu_generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>i_rdaddr_b, o_d=>rdaddr_b);
  
  u_rdaddr_c_Pa0: spu_generic_reg generic map(REG_NUM=>PA0_DEPTH, REG_WIDTH=>RF_ADDR_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>i_rdaddr_c, o_d=>rdaddr_c);
  
  default_gen: if (RF_INIT_EN = false) generate
  -- 32 entry RF
  rf32_gen:
  if (RF_ADDR_WIDTH = 5) generate
    rf_unit_gen: for n in 0 to RF_DATA_WIDTH/2-1 generate begin      
      ONE_gen: if (n = FRAC_BITS/2) generate
        -- R31 is register ONE. In any format, a '1' would be in the highest two bits.
        
        -- When FRAC_BITS is even, '1' is in the 62th bit
        EVEN_GEN: if (FRAC_BITS mod 2 = 0) generate
          u_ram_unit: RAM32M
          generic map (
          INIT_A => X"4000000000000000", -- Initial contents of A port
          INIT_B => X"4000000000000000", -- Initial contents of B port
          INIT_C => X"4000000000000000", -- Initial contents of C port
          INIT_D => X"4000000000000000") -- Initial contents of D port
          port map (
          DOA => rddata_a((2*n +1) downto (2*n)), -- Read port A 2-bit output
          DOB => rddata_b((2*n +1) downto (2*n)), -- Read port B 2-bit output
          DOC => rddata_c((2*n +1) downto (2*n)), -- Read port C 2-bit output
          ADDRA => rdaddr_a, -- Read port A 5-bit address input
          ADDRB => rdaddr_b, -- Read port B 5-bit address input
          ADDRC => rdaddr_c, -- Read port C 5-bit address input
          ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input      
          DIA => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIB => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIC => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DID => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          WCLK => clk, -- Write clock input
          WE => i_wen -- Write enable input
          );
        end generate;
        
        -- When FRAC_BITS is odd, '1' is in the 63th bit
        ODD_GEN: if (FRAC_BITS mod 2 = 1) generate
          u_ram_unit: RAM32M
          generic map (
          INIT_A => X"8000000000000000", -- Initial contents of A port
          INIT_B => X"8000000000000000", -- Initial contents of B port
          INIT_C => X"8000000000000000", -- Initial contents of C port
          INIT_D => X"8000000000000000") -- Initial contents of D port
          port map (
          DOA => rddata_a((2*n +1) downto (2*n)), -- Read port A 2-bit output
          DOB => rddata_b((2*n +1) downto (2*n)), -- Read port B 2-bit output
          DOC => rddata_c((2*n +1) downto (2*n)), -- Read port C 2-bit output
          ADDRA => rdaddr_a, -- Read port A 5-bit address input
          ADDRB => rdaddr_b, -- Read port B 5-bit address input
          ADDRC => rdaddr_c, -- Read port C 5-bit address input
          ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input      
          DIA => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIB => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DIC => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          DID => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
          WCLK => clk, -- Write clock input
          WE => i_wen -- Write enable input
          );
        end generate;
        
      end generate;
      
      Others_gen: if (n /= FRAC_BITS/2) generate
        u_ram_unit: RAM32M
        generic map (
        INIT_A => X"0000000000000000", -- Initial contents of A port
        INIT_B => X"0000000000000000", -- Initial contents of B port
        INIT_C => X"0000000000000000", -- Initial contents of C port
        INIT_D => X"0000000000000000") -- Initial contents of D port
        port map (
        DOA => rddata_a((2*n +1) downto (2*n)), -- Read port A 2-bit output
        DOB => rddata_b((2*n +1) downto (2*n)), -- Read port B 2-bit output
        DOC => rddata_c((2*n +1) downto (2*n)), -- Read port C 2-bit output
        ADDRA => rdaddr_a, -- Read port A 5-bit address input
        ADDRB => rdaddr_b, -- Read port B 5-bit address input
        ADDRC => rdaddr_c, -- Read port C 5-bit address input
        ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input      
        DIA => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DIB => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DIC => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DID => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        WCLK => clk, -- Write clock input
        WE => i_wen -- Write enable input
        );
      end generate;
    end generate;
  end generate;
  
  -----------------------------------------------------------------
  -- 64 entry RF
  -----------------------------------------------------------------
  rf64_gen:
  if (RF_ADDR_WIDTH = 6) generate
    rf_unit_gen: for n in 0 to RF_DATA_WIDTH-1 generate begin
      ONE_gen: if (n = FRAC_BITS) generate
        -- R63 is register ONE. In 8.8 fixed point format, it's content is set
        -- to X"0100". Bit 8 is in the RAM unit 8, and reg 63 means they
        -- occupy the highest 1 bit, that is (63) in RAM unit 8.
        u_ram_unit: RAM64M
        generic map (
        INIT_A => X"8000000000000000", -- Initial contents of A port
        INIT_B => X"8000000000000000", -- Initial contents of B port
        INIT_C => X"8000000000000000", -- Initial contents of C port
        INIT_D => X"8000000000000000") -- Initial contents of D port
        port map (
        DOA => rddata_a(n), -- Read port A 2-bit output
        DOB => rddata_b(n), -- Read port B 2-bit output
        DOC => rddata_c(n), -- Read port C 2-bit output
        ADDRA => rdaddr_a, -- Read port A 5-bit address input
        ADDRB => rdaddr_b, -- Read port B 5-bit address input
        ADDRC => rdaddr_c, -- Read port C 5-bit address input
        ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input
        DIA => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIB => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIC => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DID => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        WCLK => clk, -- Write clock input
        WE => i_wen -- Write enable input
        );
      end generate;
      
      Others_gen: if (n /= FRAC_BITS) generate
        u_ram_unit: RAM64M
        generic map (
        INIT_A => X"0000000000000000", -- Initial contents of A port
        INIT_B => X"0000000000000000", -- Initial contents of B port
        INIT_C => X"0000000000000000", -- Initial contents of C port
        INIT_D => X"0000000000000000") -- Initial contents of D port
        port map (
        DOA => rddata_a(n), -- Read port A 2-bit output
        DOB => rddata_b(n), -- Read port B 2-bit output
        DOC => rddata_c(n), -- Read port C 2-bit output
        ADDRA => rdaddr_a, -- Read port A 5-bit address input
        ADDRB => rdaddr_b, -- Read port B 5-bit address input
        ADDRC => rdaddr_c, -- Read port C 5-bit address input
        ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input
        DIA => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIB => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIC => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DID => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        WCLK => clk, -- Write clock input
        WE => i_wen -- Write enable input
        );
      end generate;
    end generate;
  end generate;
  end generate; -- default_gen

  init_gen: if (RF_INIT_EN = true) generate    
    rf32_gen: if (RF_ADDR_WIDTH = 5) generate
      constant RAM : rf32_type := init_lut_mem_32(RF_INIT_FILE);
    begin
      rf_unit_gen: for n in 0 to RF_DATA_WIDTH/2-1 generate
        u_ram_unit: RAM32M
        generic map (
        INIT_A => RAM(n), -- Initial contents of A port
        INIT_B => RAM(n), -- Initial contents of B port
        INIT_C => RAM(n), -- Initial contents of C port
        INIT_D => RAM(n)) -- Initial contents of D port
        port map (
        DOA => rddata_a((2*n +1) downto (2*n)), -- Read port A 2-bit output
        DOB => rddata_b((2*n +1) downto (2*n)), -- Read port B 2-bit output
        DOC => rddata_c((2*n +1) downto (2*n)), -- Read port C 2-bit output
        ADDRA => rdaddr_a, -- Read port A 5-bit address input
        ADDRB => rdaddr_b, -- Read port B 5-bit address input
        ADDRC => rdaddr_c, -- Read port C 5-bit address input
        ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input      
        DIA => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DIB => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DIC => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        DID => i_wrdata_d((2*n +1) downto (2*n)), -- RAM 2-bit data write input addressed by ADDRD,
        WCLK => clk, -- Write clock input
        WE => i_wen -- Write enable input
        );    
      end generate;
    end generate;
      
    rf64_gen: if (RF_ADDR_WIDTH = 6) generate    
      constant RAM : rf64_type := init_lut_mem_64(RF_INIT_FILE);
    begin
      rf_unit_gen: for n in 0 to RF_DATA_WIDTH-1 generate
        u_ram_unit: RAM64M
        generic map (
        INIT_A => RAM(n), -- Initial contents of A port
        INIT_B => RAM(n), -- Initial contents of B port
        INIT_C => RAM(n), -- Initial contents of C port
        INIT_D => RAM(n)) -- Initial contents of D port
        port map (
        DOA => rddata_a(n), -- Read port A 2-bit output
        DOB => rddata_b(n), -- Read port B 2-bit output
        DOC => rddata_c(n), -- Read port C 2-bit output
        ADDRA => rdaddr_a, -- Read port A 5-bit address input
        ADDRB => rdaddr_b, -- Read port B 5-bit address input
        ADDRC => rdaddr_c, -- Read port C 5-bit address input
        ADDRD => i_wraddr_d, -- Read/Write port D 5-bit address input
        DIA => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIB => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DIC => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        DID => i_wrdata_d(n), -- RAM 2-bit data write input addressed by ADDRD,
        WCLK => clk, -- Write clock input
        WE => i_wen -- Write enable input
        );
      end generate;
    end generate;
  end generate; -- init_gen

  -- Output registrering
  u_src_a_reg_Pa1: spu_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>RF_DATA_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>rddata_a, o_d=>o_rddata_a);
  
  u_src_b_reg_Pa1: spu_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>RF_DATA_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>rddata_b, o_d=>o_rddata_b);
  
  u_src_c_reg_Pa1: spu_generic_reg generic map(REG_NUM=>PA1_DEPTH, REG_WIDTH=>RF_DATA_WIDTH) 
  port map(clk=>clk, rst=>rst, i_d=>rddata_c, o_d=>o_rddata_c);

end structure;
