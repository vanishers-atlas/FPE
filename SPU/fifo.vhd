library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.all;
library work;
use work.ssp_pkg.all;
library unisim;
use unisim.vcomponents.all;

-- NOTES:
-- almost_full signal is used for iocore only. Its use has restrictions:
-- The DEPTH must be larger than 5, as almost full means there are only
-- 5 locations. Since a put is issued, the almost full signals only updates
-- 5 cycles later. Thus there must be enough rooms for following puts before
-- the almost full signal updated.
--
-- full signal is not used, it is useless for control

entity fifo is
  generic ( 
    WIDTH    : integer := 8;
    DEPTH    : integer := 4096;
    STATE_EN : boolean := false);
  port(
    clk          : in     std_logic;
    i_data       : in     std_logic_vector (WIDTH -1 downto 0);
    o_data       : out    std_logic_vector (WIDTH -1 downto 0);
    write        : in     std_logic;
    read         : in     std_logic;
    o_full       : out    std_logic;
    o_almostfull : out    std_logic;
    o_empty      : out    std_logic
  );
  
  attribute shreg_extract : string;
  attribute shreg_extract of fifo : entity is "yes";

end fifo ;

architecture rtl of fifo is
  signal empty          : std_logic := '1';
  signal almostfull_wire: std_logic := '0';
  signal almostfull     : std_logic := '0';
  signal fifo_data      : std_logic_vector (WIDTH-1 downto 0) := (others=>'0');
begin
  fifo_without_emptyfull_gen: if (STATE_EN = false) generate
    o_full  <= '0';  
    o_empty <= '0';
  end generate;
  
  fifo_with_emptyfull_gen: if (STATE_EN = true) generate
    o_full  <= '0';  
    o_empty <= empty;
    o_almostfull <= almostfull;
  end generate;
    ---------------------------------------------------------
    -- When depth equals 1, storage is a register
    ---------------------------------------------------------
    one_depth_fifo_gen: if (DEPTH = 1) generate
      proc_data :process( clk ) begin
        if rising_edge( clk ) then
          if write = '1' then
            fifo_data <= i_data;
          end if;
        end if;
      end process;
    end generate one_depth_fifo_gen;       
    
    ---------------------------------------------------------
    -- When depth is larger than 1, storage uses SRL
    ---------------------------------------------------------
    large_srlfifo_gen: if DEPTH > 1 and DEPTH <= 128 generate
      type srl_array is array (DEPTH-1  downto 0) of std_logic_vector (WIDTH-1 downto 0);
      signal pointer        : integer range 0 to DEPTH - 1 := 0;
      signal fifo_store     : srl_array;      
    begin
      proc_data :process( clk )
      begin
        if rising_edge( clk ) then
          if write = '1' then
            fifo_store <= fifo_store( fifo_store'left - 1 downto 0) & i_data;
          end if;
        end if;
      end process;

--      o_data <= fifo_store(pointer);
      fifo_data <= i_data when (empty = '1' and write = '1') else fifo_store(pointer);
            
      --almostfull_wire <= '1' when pointer = DEPTH - 6 else '0';      
      process( clk ) begin
        if rising_edge( clk ) then
          almostfull <= almostfull_wire;
        end if;
      end process;
      
      process( clk ) begin
        if rising_edge( clk ) then      
          if (write = '1' and read = '0') then
            if  (empty = '0') then
              pointer <= pointer + 1;
            else
              empty <= '0';
            end if;
          elsif (write = '0' and read = '1') then
            if (pointer > 0) then
              pointer <= pointer - 1;
            else
              empty <= '1';
            end if;
          end if;
        end if;
      end process;
    end generate;
    
    ----------------------------------------------------------------
    BUILTIN_FIFO_8BIT: if (WIDTH = 8) generate
      fifo8w2048d_gen: if (DEPTH > 128 and DEPTH <= 2048) generate
        signal dataout : std_logic_vector(15 downto 0);
        signal datain  : std_logic_vector(15 downto 0);
      begin
        FIFO18_inst : FIFO18
        generic map (
          ALMOST_FULL_OFFSET => X"006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"006", -- Sets the almost empty threshold
          DATA_WIDTH => 9, -- Sets data width to 4, 9, or 18
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => dataout, -- 16-bit data output
          DOP => open, -- 2-bit parity data output
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 12-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 12-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 16-bit data input
          DIP => "00", -- 2-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
        
        datain <= "00000000" & i_data;
        fifo_data <= dataout(7 downto 0);
      end generate;
      
      fifo8w4096d_gen: if (DEPTH > 2048 and DEPTH <= 4096) generate
        signal dataout : std_logic_vector(31 downto 0);
        signal datain  : std_logic_vector(31 downto 0);
      begin
        FIFO36_inst : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 9, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => dataout, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
        
        datain <= X"000000" & i_data;
        fifo_data <= dataout(7 downto 0);
      end generate;
      
    end generate;
    
    -- 16-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_16BIT: if (WIDTH = 16) generate
      fifo16w1024d_gen: if (DEPTH > 128 and DEPTH <= 1024) generate
      begin
        FIFO18_inst : FIFO18
        generic map (
          ALMOST_FULL_OFFSET => X"006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"006", -- Sets the almost empty threshold
          DATA_WIDTH => 18, -- Sets data width to 4, 9, or 18
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => fifo_data, -- 16-bit data output
          DOP => open, -- 2-bit parity data output
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 12-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 12-bit write count output
          WRERR => open, -- 1-bit write error
          DI => i_data, -- 16-bit data input
          DIP => "00", -- 2-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
      end generate;
    end generate;
    
    -- 32-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_32BIT: if (WIDTH = 32) generate
      fifo32w512d_gen: if (DEPTH > 128 and DEPTH <= 512) generate
      begin
        FIFO18_36_inst : FIFO18_36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DO_REG => 1, -- Enable output register (0 or 1)
          -- Must be 1 if EN_SYN = FALSE
          EN_SYN => FALSE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => fifo_data, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 9-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 9-bit write count output
          WRERR => open, -- 1-bit write error
          DI => i_data, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
      end generate;
      
      fifo32w1024d_gen: if (DEPTH > 512 and DEPTH <= 1024) generate
      begin
        FIFO36_inst : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 36, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => fifo_data, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => i_data, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
      end generate;
      
      fifo32w2048d_gen: if (DEPTH > 1024 and DEPTH <= 2048) generate
        signal dataout0, dataout1 : std_logic_vector(31 downto 0);
        signal datain0, datain1  : std_logic_vector(31 downto 0);
      begin
        FIFO36_inst0 : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 18, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => dataout0, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => open, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain0, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
        FIFO36_inst1 : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 18, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 1, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => dataout1, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => open, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain1, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
        datain0 <= X"0000" & i_data(15 downto 0);
        datain1 <= X"0000" & i_data(31 downto 16);
        fifo_data <= dataout1(15 downto 0) & dataout0(15 downto 0);
      end generate;
    end generate;
      
    -- 64-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_64BIT: if (WIDTH = 64) generate
      fifo64w512d_gen: if (DEPTH > 128 and DEPTH <= 512) generate
      begin
        FIFO36_72_inst : FIFO36_72
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DO_REG => 1, -- Enable output register (0 or 1)
          -- Must be 1 if EN_SYN = FALSE
          EN_ECC_READ => FALSE, -- Enable ECC decoder, TRUE or FALSE
          EN_ECC_WRITE => FALSE, -- Enable ECC encoder, TRUE or FALSE
          EN_SYN => FALSE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DBITERR => open, -- 1-bit double bit error status output
          DO => fifo_data, -- 64-bit data output
          DOP => open, -- 4-bit parity data output
          ECCPARITY => open, -- 8-bit generated error correction parity
          EMPTY => empty, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 9-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 9-bit write count output
          WRERR => open, -- 1-bit write error
          DI => i_data, -- 64-bit data input
          DIP => "00000000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => read, -- 1-bit read enable input
          RST => '0', -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => write -- 1-bit write enable input
        );
      end generate;
    end generate;
    
    -- Register output
    u_data_reg_Pa0: spu_generic_reg generic map(REG_NUM=>1, REG_WIDTH=>WIDTH)
      port map(clk=>clk, rst=>'0', i_d=>fifo_data, o_d=>o_data);
end rtl;