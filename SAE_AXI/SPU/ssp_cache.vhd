library ieee;  
use ieee.std_logic_1164.all;
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

entity ssp_fifo_cache is
	generic ( 
		WIDTH    : integer := 16;  -- the data width of sync fifo
		DEPTH    : integer := 4096;  -- the size of sync fifo
		OUT_REG_NUM  : integer := 1;
		STATE_EN : boolean := true
	);  -- switch of state signal
	port(	 
		clk          : in     std_logic;  -- clock signal 
		rst          : in     std_logic := '1';  -- reset signal 
		i_data       : in     std_logic_vector (WIDTH -1 downto 0) := (others => '0');  -- input data
		o_data       : out    std_logic_vector (WIDTH -1 downto 0) := (others => '0');  -- output data
		i_write      : in     std_logic  := '0';  -- write fifo request signal 
		i_read       : in     std_logic  := '0';  -- read fifo request signal 
		o_full       : out    std_logic := '0';  -- fifo is full signal
		o_almostfull : out    std_logic := '0';  -- fifo is almost full signal 
		o_empty      : out    std_logic := '1';  -- fifo can take data signal 

		-- additive signal
		i_data_end_s   : in     std_logic := '0';  -- end of input data signal 
		i_data_end_e : in     std_logic := '0';  -- end of output data signal
		o_pc_en      : out    std_logic := '0'  -- output enable signal
	);
  
	attribute shreg_extract : string;
	attribute shreg_extract of ssp_fifo_cache : entity is "yes";

end ssp_fifo_cache ;

architecture rtl of ssp_fifo_cache is
	signal full           : std_logic := '0';
	signal empty          : std_logic := '1';
    signal empty0          : std_logic := '1';
    signal empty1          : std_logic := '1';
	signal almostfull_wire: std_logic := '0';
	signal full_wire		 : std_logic := '0';
	signal full_wire_delay   : std_logic := '0';
    signal empty_wire        : std_logic := '1';
	signal almostfull     : std_logic := '0';
	signal fifo_data      : std_logic_vector (WIDTH-1 downto 0) := (others=>'0');
	signal dataout : std_logic_vector(WIDTH-1 downto 0);
	signal datain  : std_logic_vector(WIDTH-1 downto 0);
--	signal dataout0, dataout1 : std_logic_vector(WIDTH-1 downto 0);
--	signal datain0, datain1  : std_logic_vector(WIDTH-1 downto 0);
	signal o_pc_en_reg    : std_logic := '0';
	signal write_wire : std_logic := '0';
	
	type STATE_TYPE is (wait4wr, wait4rd); 
	signal state        : STATE_TYPE := wait4wr;    
	signal i_data_end_s_delay : std_logic;
	
begin
	
    ---------------------------------------------------------
    -- Generate fifo state signal according to the switch
    ---------------------------------------------------------
	fifo_without_emptyfull_gen: if (STATE_EN = false) generate
		o_full  <= '0';  
		o_empty <= '0';
		o_almostfull <= '0';
	end generate;

	fifo_with_emptyfull_gen: if (STATE_EN = true) generate
		o_full  <= full;  
		o_empty <= empty;
		o_almostfull <= almostfull;
	end generate;
	
	-- enable the next units while input data finished and ouput data is not finished      
	o_pc_en <= o_pc_en_reg;
--	o_pc_en_reg <= '1' when state = Active else '0';
	pc_en_proc: process(clk,rst)
	begin
	  if rising_edge( clk ) and rst = '0' then
		  case state is 
--		  when Detect =>
--				if i_data_end_s = '1' then
--					state <= Active;
--				end if;
--				if (i_data_end_s = '0' and i_data_end_e = '1') then
--					state <= Idle;
--				end if;
		  when wait4rd =>
				--if (i_data_end_s_delay = '0' and i_data_end_e = '1' and full = '0') or empty = '1' then
				-- if (i_data_end_e = '1' and full = '0') or empty = '1' then
				if (i_data_end_e = '1' and full = '0')then
					state <= wait4wr;
				end if;
				o_pc_en_reg <= '1';
				
		  when wait4wr => 
                if (i_data_end_s_delay = '1') then
--				if (i_data_end_s_delay = '1' or full = '1') then
--				if (full = '1') then
					state <= wait4rd;
				end if;
				o_pc_en_reg <= '0';
				
		  end case; 
	  end if;
	end process;
	
	i_data_end_s_delay_proc: process(clk,rst)
	begin
	  if rising_edge( clk ) and rst = '0' then
			i_data_end_s_delay <= i_data_end_s;
	  end if;
	end process;
  
    ---------------------------------------------------------
    -- When depth equals 1, storage is a register
    ---------------------------------------------------------
    one_depth_fifo_gen: if (DEPTH = 1) generate
      proc_data :process( clk,rst ) begin
        if rising_edge( clk ) and rst = '0' then
		  -- if there is data i_write, just put the data and set the state signal 
          if i_data_end_s = '1' or i_write ='1' then
				fifo_data <= i_data;
				full <= '1';
				almostfull <= '1';
				empty <= '0';
			 else
				full <= '0';
				almostfull <= '0';
				empty <= '1';
          end if;
        end if;
      end process;
    end generate one_depth_fifo_gen;       
    
    ---------------------------------------------------------
    -- When depth is larger than 1, but less than 128 , storage uses SRL
    ---------------------------------------------------------
    large_srlfifo_gen: if DEPTH > 1 and DEPTH <= 128 generate
      type srl_array is array (DEPTH-1  downto 0) of std_logic_vector (WIDTH-1 downto 0);
      signal pointer        : integer range 0 to DEPTH - 1 := 0;
      signal fifo_store     : srl_array := (others => (others =>  '0'));   
    begin
      proc_data :process( clk,rst )
      begin
        if rising_edge( clk ) and rst = '0' then
		  -- fill the fifo store until data end and fifo can still receive data with write signal
          if i_write ='1' and full = '0' and pointer < DEPTH-1 then
            fifo_store <= fifo_store( fifo_store'left - 1 downto 0) & i_data;
          end if;
        end if;
      end process;

		-- update the ouput data when input data finished or the fifo is about to full with read signal
		fifo_data <= fifo_store(pointer) when i_read ='1' and empty = '0' else (others => '0');
            
		-- count the data in fifo to indicate if fifo is full or about to full
      almostfull_wire <= '1' when pointer = DEPTH - 6 else '0';
      full_wire <= '1' when pointer = DEPTH - 1 else '0';  
      process( clk ) begin
        if rising_edge( clk ) and rst = '0' then
             almostfull <= almostfull_wire;
			 full <= full_wire;
        end if;
      end process;
      
		-- update the fifo pointer
      process( clk,rst ) begin
        if rising_edge( clk ) and rst = '0' then      
          if (i_write ='1' and i_read ='0' and full_wire = '0') then
            if  (empty = '0') then
              pointer <= pointer + 1;
            else
              empty <= '0';
            end if;
          elsif (i_write ='0' and i_read ='1' and empty = '0') then
            if (pointer > 0) then
              pointer <= pointer - 1;
            else
              empty <= '1';
            end if;
          end if;
        end if;
      end process;
    end generate;
    
    ---------------------------------------------------------
    -- When depth is larger than 128, storage uses FIFO primitive
    ---------------------------------------------------------
    BUILTIN_FIFO_8BIT: if (WIDTH = 8) generate
      fifo8w2048d_gen: if (DEPTH > 128 and DEPTH <= 2048) generate
--        signal dataout : std_logic_vector(15 downto 0);
--        signal datain  : std_logic_vector(15 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
      begin
        FIFO18_inst : FIFO18
        generic map (
          ALMOST_FULL_OFFSET => X"006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"006", -- Sets the almost empty threshold
          DATA_WIDTH => 9, -- Sets data width to 4, 9, or 18
          DO_REG => 0, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => TRUE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
          DO => dataout, -- 16-bit data output
          DOP => open, -- 2-bit parity data output
          EMPTY => empty_wire, -- 1-bit empty output flag
          FULL => full_wire, -- 1-bit full output flag
          RDCOUNT => open, -- 12-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 12-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 16-bit data input
          DIP => "00", -- 2-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
		  
			process( clk,rst ) begin
			  if rising_edge( clk ) and rst = '0' then
				 almostfull <= almostfull_wire;
				 full <= full_wire;
				 empty <= empty_wire;
			  end if;
			end process;
        
        --datain <= "00000000" & i_data when full_wire = '0' and i_write = '1';
        --fifo_data <= dataout(7 downto 0) when i_read ='1' and empty_wire = '0';
        datain <= "00000000" & i_data;
        fifo_data <= dataout(7 downto 0);
      end generate;
      
      fifo8w4096d_gen: if (DEPTH > 2048 and DEPTH <= 4096) generate
--        signal dataout : std_logic_vector(31 downto 0);
--        signal datain  : std_logic_vector(31 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
      begin
        FIFO36_inst : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 9, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 0, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => TRUE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
          DO => dataout, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => empty_wire, -- 1-bit empty output flag
          FULL => full_wire, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
        
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then
               almostfull <= almostfull_wire;
               full <= full_wire;
               empty <= empty_wire;
            end if;
          end process;
        
--        datain <= X"000000" & i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout(7 downto 0) when i_read ='1' and empty_wire = '0';
        datain <= X"000000" & i_data;
        fifo_data <= dataout(7 downto 0);
      end generate;
      
    end generate;
    
    -- 16-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_16BIT: if (WIDTH = 16) generate
      fifo16w1024d_gen: if (DEPTH > 128 and DEPTH <= 1024) generate
--        signal dataout : std_logic_vector(15 downto 0);
--        signal datain  : std_logic_vector(15 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
      begin
        FIFO18_inst : FIFO18
        generic map (
          ALMOST_FULL_OFFSET => X"006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"006", -- Sets the almost empty threshold
          DATA_WIDTH => 18, -- Sets data width to 4, 9, or 18
          DO_REG => 0, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => TRUE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
          DO => dataout, -- 16-bit data output
          DOP => open, -- 2-bit parity data output
          EMPTY => empty_wire, -- 1-bit empty output flag
          FULL => full_wire, -- 1-bit full output flag
          RDCOUNT => open, -- 12-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 12-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 16-bit data input
          DIP => "00", -- 2-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
                  
        process( clk,rst ) begin
          if rising_edge( clk ) and rst = '0' then
             almostfull <= almostfull_wire;
             full <= full_wire;
             empty <= empty_wire;
          end if;
        end process;
		  
--        datain <= i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout when i_read ='1' and empty_wire = '0';
        datain <= i_data;
        fifo_data <= dataout;
      end generate;
		
		
      fifo16w2048d_gen: if (DEPTH > 1024 and DEPTH <= 2048) generate
      begin
        FIFO36_inst : FIFO36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DATA_WIDTH => 18, -- Sets data width to 4, 9, 18, or 36
          DO_REG => 0, -- Enable output register ( 0 or 1)
          -- Must be 1 if the EN_SYN = FALSE
          EN_SYN => TRUE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
          DO => dataout, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => empty_wire, -- 1-bit empty output flag
          FULL => full_wire, -- 1-bit full output flag
          RDCOUNT => open, -- 13-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 13-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
                            
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then
               almostfull <= almostfull_wire;
               full <= full_wire;
               empty <= empty_wire;
            end if;
          end process;
		  
--        datain <= X"0000" & i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout(15 downto 0) when i_read ='1' and empty_wire = '0';
        datain <= X"0000" & i_data;
        fifo_data <= dataout(15 downto 0);
		end generate;
    end generate;
    
    -- 32-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_32BIT: if (WIDTH = 32) generate
      fifo32w512d_gen: if (DEPTH > 128 and DEPTH <= 512) generate
--        signal dataout : std_logic_vector(31 downto 0);
--        signal datain  : std_logic_vector(31 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
        signal pointer        : integer range 0 to DEPTH - 1 := 0;
      begin
        FIFO18_36_inst : FIFO18_36
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DO_REG => 0, -- Enable output register (0 or 1)
          -- Must be 1 if EN_SYN = FALSE
          EN_SYN => TRUE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => open, -- 1-bit almost full output flag
          DO => dataout, -- 32-bit data output
          DOP => open, -- 4-bit parity data output
          EMPTY => open, -- 1-bit empty output flag
          FULL => open, -- 1-bit full output flag
          RDCOUNT => open, -- 9-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 9-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 32-bit data input
          DIP => "0000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
		  
--        datain <= i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout when i_read ='1' and empty_wire = '0';
--        datain <= i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout when i_read ='1' and empty_wire = '0';
        datain <= i_data;
        fifo_data <= dataout;
		
		  almostfull_wire <= '1' when pointer = DEPTH - 6 else '0';
		  full_wire <= '1' when pointer = DEPTH - 1 else '0';  
		  process( clk,rst ) begin
			if rising_edge( clk ) and rst = '0' then
				 almostfull <= almostfull_wire;
				 full <= full_wire;
				 empty <= empty_wire;
			end if;
		  end process;      
--                             full <= full_wire;
		  
			-- update the fifo pointer
		  process( clk,rst ) begin
			if rising_edge( clk ) and rst = '0' then      
			  if (i_write ='1' and i_read ='0' and full_wire = '0') then
				if  (empty_wire = '0') then
				  pointer <= pointer + 1;
				else
				  empty_wire <= '0';
				end if;
			  elsif (i_write ='0' and i_read ='1' and empty_wire = '0') then
				if (pointer > 0) then
				  pointer <= pointer - 1;
				else
				  empty_wire <= '1';
				end if;
			  end if;
			end if;
		  end process;
      end generate;
      
      fifo32w1024d_gen: if (DEPTH > 512 and DEPTH <= 1024) generate
--        signal dataout : std_logic_vector(31 downto 0);
--        signal datain  : std_logic_vector(31 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
        signal rdcount : std_logic_vector(12 downto 0);
        signal wrcount  : std_logic_vector(12 downto 0);
        signal almostful : std_logic := '0';
        signal almostempty : std_logic := '0';
        signal full_delay : std_logic := '0';
        signal dataout0 : std_logic_vector(63 downto 0);
        signal datain0 : std_logic_vector(63 downto 0);
        signal full_tmp : std_logic := '0';
        signal empty_tmp : std_logic := '0';
        signal pointer        : integer range 0 to DEPTH - 1 := 0;
      begin
--        FIFO36_inst : FIFO36
--        generic map (
--          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
--          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
--          DATA_WIDTH => 36, -- Sets data width to 4, 9, 18, or 36
--          DO_REG => 1, -- Enable output register ( 0 or 1)
--          -- Must be 1 if the EN_SYN = FALSE
--          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
--          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
--          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
--          -- Design Guide" for details
--        port map (
--          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
--          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
--          DO => dataout, -- 32-bit data output
--          DOP => open, -- 4-bit parity data output
--          EMPTY => empty, -- 1-bit empty output flag
--          FULL => full_wire, -- 1-bit full output flag
--          RDCOUNT => rdcount, -- 13-bit read count output
--          RDERR => open, -- 1-bit read error output
--          WRCOUNT => wrcount, -- 13-bit write count output
--          WRERR => open, -- 1-bit write error
--          DI => datain, -- 32-bit data input
--          DIP => "0000", -- 4-bit parity input
--          RDCLK => clk, -- 1-bit read clock input
--          RDEN => i_read, -- 1-bit read enable input
--          RST => rst, -- 1-bit reset input
--          WRCLK => clk, -- 1-bit write clock input
--          WREN => i_write -- 1-bit write enable input
--        );
        FIFO36E1_inst : FIFO36E1
        generic map (
            ALMOST_EMPTY_OFFSET => X"0080", -- Sets the almost empty threshold
            ALMOST_FULL_OFFSET => X"0080", -- Sets almost full threshold
            DATA_WIDTH => 36, -- Sets data width to 4-72
            DO_REG => 1, -- Enable output register (1-0) Must be 1 if EN_SYN = FALSE
            EN_ECC_READ => FALSE, -- Enable ECC decoder, FALSE, TRUE
            EN_ECC_WRITE => FALSE, -- Enable ECC encoder, FALSE, TRUE
            EN_SYN => FALSE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
            FIFO_MODE => "FIFO36", -- Sets mode to "FIFO36" or "FIFO36_72"
            FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to &VALUES
            INIT => X"000000000000000000", -- Initial values on output port
            SIM_DEVICE => "7SERIES", -- Must be set to "7SERIES" for simulation behavior
            SRVAL => X"000000000000000000" -- Set/Reset value for output port
            )
            port map (
            -- ECC Signals: 1-bit (each) output: Error Correction Circuitry ports
            DBITERR => open, -- 1-bit output: Double bit error status
            ECCPARITY => open, -- 8-bit output: Generated error correction parity
            SBITERR => open, -- 1-bit output: Single bit error status
            -- Read Data: 64-bit (each) output: Read output data
            DO => dataout0, -- 64-bit output: Data output
            DOP => open, -- 8-bit output: Parity data output
            -- Status: 1-bit (each) output: Flags and other FIFO status outputs
            ALMOSTEMPTY => open, -- 1-bit output: Almost empty flag
            ALMOSTFULL => open, -- 1-bit output: Almost full flag
            EMPTY => open, -- 1-bit output: Empty flag
            FULL => open, -- 1-bit output: Full flag
            RDCOUNT => rdcount, -- 13-bit output: Read count
            RDERR => open, -- 1-bit output: Read error
            WRCOUNT => wrcount, -- 13-bit output: Write count
            WRERR => open, -- 1-bit output: Write error
            -- ECC Signals: 1-bit (each) input: Error Correction Circuitry ports
            INJECTDBITERR => '0', -- 1-bit input: Inject a double bit error input
            INJECTSBITERR => '0',
            -- Read Control Signals: 1-bit (each) input: Read clock, enable and reset input signals
            RDCLK => clk, -- 1-bit input: Read clock
            RDEN => i_read, -- 1-bit input: Read enable
            REGCE => '1', -- 1-bit input: Clock enable
            RST => rst, -- 1-bit input: Reset
            RSTREG => '1', -- 1-bit input: Output register set/reset
            -- Write Control Signals: 1-bit (each) input: Write clock and enable input signals
            WRCLK => clk, -- 1-bit input: Rising edge write clock.
            WREN => i_write, -- 1-bit input: Write enable
            -- Write Data: 64-bit (each) input: Write input data
            DI => datain0, -- 64-bit input: Data input
            DIP => "00000000" -- 8-bit input: Parity input
        );
        
        dataout <= dataout0(WIDTH-1 downto 0);
----		fulltemp <='1' when (std_logic_vector(to_unsigned((DEPTH-1),10))=wrcount(9 downto 0)) else '0';
--        datain0 <= X"00000000" & i_data when full_wire = '0' and i_write = '1';
----        datain <= i_data when full = '0' and i_write = '1';
--        fifo_data <= dataout when i_read ='1' and empty_wire = '0';

        datain0 <= X"00000000" & i_data;
        fifo_data <= dataout;
        
--        u_empty_reg_Pa0: spu_generic_reg1 generic map(REG_NUM=>0)
--         port map(clk=>clk, rst=>rst, i_d=>empty_tmp, o_d=>empty);
--        u_full_reg_Pa0: spu_generic_reg1 generic map(REG_NUM=>8)
--         port map(clk=>clk, rst=>rst, i_d=>almostful, o_d=>full);

          almostfull_wire <= '1' when pointer = DEPTH - 6 else '0';
          full_wire <= '1' when pointer = DEPTH - 1 else '0';  
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then
                 almostfull <= almostfull_wire;
                 full <= full_wire_delay;
--                 empty <= empty_wire;
            end if;
          end process;      
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then
                 full_wire_delay <= full_wire;
            end if;
          end process;   
          
--          process( clk,rst ) begin
--            if rising_edge( clk ) and rst = '0' then      
--              if (i_write ='1' and i_read ='0' and full_wire = '0') then
--                write_wire <= '1';
--              else
--                write_wire <= '0';
--              end if;
--            end if;
--          end process;
--                             full <= full_wire;
                             empty <= empty_wire; 
            -- update the fifo pointer
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then      
              if (i_write ='1' and i_read ='0' and full_wire = '0') then
                if  (empty_wire = '0') then
                  pointer <= pointer + 1;
                else
                  empty_wire <= '0';
                end if;
              elsif (i_write ='0' and i_read ='1' and empty_wire = '0') then
                if (pointer > 0) then
                  pointer <= pointer - 1;
                else
                  empty_wire <= '1';
                end if;
              end if;
            end if;
          end process;
      end generate;
      
      fifo32w2048d_gen: if (DEPTH > 1024 and DEPTH <= 2048) generate
        signal dataout0, dataout1 : std_logic_vector(63 downto 0);
        signal datain0, datain1  : std_logic_vector(63 downto 0);
        signal rdcount1,rdcount2 : std_logic_vector(12 downto 0);
        signal wrcount1,wrcount2  : std_logic_vector(12 downto 0);
        signal almostful : std_logic := '0';
        signal almostful1 : std_logic := '0';
        signal almostful2 : std_logic := '0';
        signal almostempty : std_logic := '0';
        signal almostempty1 : std_logic := '0';
        signal almostempty2 : std_logic := '0';
		signal full1           : std_logic := '0';
		signal full2           : std_logic := '0';
        signal pointer        : integer range 0 to DEPTH - 1 := 0;
      begin
--        FIFO36_inst0 : FIFO36
--        generic map (
--          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
--          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
--          DATA_WIDTH => 18, -- Sets data width to 4, 9, 18, or 36
--          DO_REG => 1, -- Enable output register ( 0 or 1)
--          -- Must be 1 if the EN_SYN = FALSE
--          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
--          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
--          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
--          -- Design Guide" for details
--        port map (
--          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
--          ALMOSTFULL => almostful1, -- 1-bit almost full output flag
--          DO => dataout0, -- 32-bit data output
--          DOP => open, -- 4-bit parity data output
--          EMPTY => empty0, -- 1-bit empty output flag
--          FULL => full1, -- 1-bit full output flag
--          RDCOUNT => rdcount1, -- 13-bit read count output
--          RDERR => open, -- 1-bit read error output
--          WRCOUNT => wrcount1, -- 13-bit write count output
--          WRERR => open, -- 1-bit write error
--          DI => datain0, -- 32-bit data input
--          DIP => "0000", -- 4-bit parity input
--          RDCLK => clk, -- 1-bit read clock input
--          RDEN => i_read, -- 1-bit read enable input
--          RST => rst, -- 1-bit reset input
--          WRCLK => clk, -- 1-bit write clock input
--          WREN => i_write -- 1-bit write enable input
--        );
--        FIFO36_inst1 : FIFO36
--        generic map (
--          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
--          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
--          DATA_WIDTH => 18, -- Sets data width to 4, 9, 18, or 36
--          DO_REG => 1, -- Enable output register ( 0 or 1)
--          -- Must be 1 if the EN_SYN = FALSE
--          EN_SYN => FALSE, -- Specified FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
--          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
--          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
--          -- Design Guide" for details
--        port map (
--          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
--          ALMOSTFULL => almostful2, -- 1-bit almost full output flag
--          DO => dataout1, -- 32-bit data output
--          DOP => open, -- 4-bit parity data output
--          EMPTY => empty1, -- 1-bit empty output flag
--          FULL => full2, -- 1-bit full output flag
--          RDCOUNT => rdcount2, -- 13-bit read count output
--          RDERR => open, -- 1-bit read error output
--          WRCOUNT => wrcount2, -- 13-bit write count output
--          WRERR => open, -- 1-bit write error
--          DI => datain1, -- 32-bit data input
--          DIP => "0000", -- 4-bit parity input
--          RDCLK => clk, -- 1-bit read clock input
--          RDEN => i_read, -- 1-bit read enable input
--          RST => rst, -- 1-bit reset input
--          WRCLK => clk, -- 1-bit write clock input
--          WREN => i_write -- 1-bit write enable input
--        );
        
        FIFO36E1_inst0 : FIFO36E1
        generic map (
            ALMOST_EMPTY_OFFSET => X"0080", -- Sets the almost empty threshold
            ALMOST_FULL_OFFSET => X"0080", -- Sets almost full threshold
            DATA_WIDTH => 18, -- Sets data width to 4-72
            DO_REG => 1, -- Enable output register (1-0) Must be 1 if EN_SYN = FALSE
            EN_ECC_READ => FALSE, -- Enable ECC decoder, FALSE, TRUE
            EN_ECC_WRITE => FALSE, -- Enable ECC encoder, FALSE, TRUE
            EN_SYN => FALSE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
            FIFO_MODE => "FIFO36", -- Sets mode to "FIFO36" or "FIFO36_72"
            FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to &VALUES
            INIT => X"000000000000000000", -- Initial values on output port
            SIM_DEVICE => "7SERIES", -- Must be set to "7SERIES" for simulation behavior
            SRVAL => X"000000000000000000" -- Set/Reset value for output port
            )
            port map (
            -- ECC Signals: 1-bit (each) output: Error Correction Circuitry ports
            DBITERR => open, -- 1-bit output: Double bit error status
            ECCPARITY => open, -- 8-bit output: Generated error correction parity
            SBITERR => open, -- 1-bit output: Single bit error status
            -- Read Data: 64-bit (each) output: Read output data
            DO => dataout0, -- 64-bit output: Data output
            DOP => open, -- 8-bit output: Parity data output
            -- Status: 1-bit (each) output: Flags and other FIFO status outputs
            ALMOSTEMPTY => open, -- 1-bit output: Almost empty flag
            ALMOSTFULL => open, -- 1-bit output: Almost full flag
            EMPTY => open, -- 1-bit output: Empty flag
            FULL => open, -- 1-bit output: Full flag
            RDCOUNT => rdcount1, -- 13-bit output: Read count
            RDERR => open, -- 1-bit output: Read error
            WRCOUNT => wrcount1, -- 13-bit output: Write count
            WRERR => open, -- 1-bit output: Write error
            -- ECC Signals: 1-bit (each) input: Error Correction Circuitry ports
            INJECTDBITERR => '0', -- 1-bit input: Inject a double bit error input
            INJECTSBITERR => '0',
            -- Read Control Signals: 1-bit (each) input: Read clock, enable and reset input signals
            RDCLK => clk, -- 1-bit input: Read clock
            RDEN => i_read, -- 1-bit input: Read enable
            REGCE => '1', -- 1-bit input: Clock enable
            RST => rst, -- 1-bit input: Reset
            RSTREG => '1', -- 1-bit input: Output register set/reset
            -- Write Control Signals: 1-bit (each) input: Write clock and enable input signals
            WRCLK => clk, -- 1-bit input: Rising edge write clock.
            WREN => i_write, -- 1-bit input: Write enable
            -- Write Data: 64-bit (each) input: Write input data
            DI => datain0, -- 64-bit input: Data input
            DIP => "00000000" -- 8-bit input: Parity input
        );        
        FIFO36E1_inst1 : FIFO36E1
        generic map (
            ALMOST_EMPTY_OFFSET => X"0080", -- Sets the almost empty threshold
            ALMOST_FULL_OFFSET => X"0080", -- Sets almost full threshold
            DATA_WIDTH => 18, -- Sets data width to 4-72
            DO_REG => 1, -- Enable output register (1-0) Must be 1 if EN_SYN = FALSE
            EN_ECC_READ => FALSE, -- Enable ECC decoder, FALSE, TRUE
            EN_ECC_WRITE => FALSE, -- Enable ECC encoder, FALSE, TRUE
            EN_SYN => FALSE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
            FIFO_MODE => "FIFO36", -- Sets mode to "FIFO36" or "FIFO36_72"
            FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to &VALUES
            INIT => X"000000000000000000", -- Initial values on output port
            SIM_DEVICE => "7SERIES", -- Must be set to "7SERIES" for simulation behavior
            SRVAL => X"000000000000000000" -- Set/Reset value for output port
            )
            port map (
            -- ECC Signals: 1-bit (each) output: Error Correction Circuitry ports
            DBITERR => open, -- 1-bit output: Double bit error status
            ECCPARITY => open, -- 8-bit output: Generated error correction parity
            SBITERR => open, -- 1-bit output: Single bit error status
            -- Read Data: 64-bit (each) output: Read output data
            DO => dataout1, -- 64-bit output: Data output
            DOP => open, -- 8-bit output: Parity data output
            -- Status: 1-bit (each) output: Flags and other FIFO status outputs
            ALMOSTEMPTY => open, -- 1-bit output: Almost empty flag
            ALMOSTFULL => open, -- 1-bit output: Almost full flag
            EMPTY => open, -- 1-bit output: Empty flag
            FULL => open, -- 1-bit output: Full flag
            RDCOUNT => rdcount2, -- 13-bit output: Read count
            RDERR => open, -- 1-bit output: Read error
            WRCOUNT => wrcount2, -- 13-bit output: Write count
            WRERR => open, -- 1-bit output: Write error
            -- ECC Signals: 1-bit (each) input: Error Correction Circuitry ports
            INJECTDBITERR => '0', -- 1-bit input: Inject a double bit error input
            INJECTSBITERR => '0',
            -- Read Control Signals: 1-bit (each) input: Read clock, enable and reset input signals
            RDCLK => clk, -- 1-bit input: Read clock
            RDEN => i_read, -- 1-bit input: Read enable
            REGCE => '1', -- 1-bit input: Clock enable
            RST => rst, -- 1-bit input: Reset
            RSTREG => '1', -- 1-bit input: Output register set/reset
            -- Write Control Signals: 1-bit (each) input: Write clock and enable input signals
            WRCLK => clk, -- 1-bit input: Rising edge write clock.
            WREN => i_write, -- 1-bit input: Write enable
            -- Write Data: 64-bit (each) input: Write input data
            DI => datain1, -- 64-bit input: Data input
            DIP => "00000000" -- 8-bit input: Parity input
        );
		  		  
--        datain0 <= X"000000000000" & i_data(15 downto 0) when full_wire = '0' and i_write = '1';
--        datain1 <= X"000000000000" & i_data(31 downto 16) when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout1(15 downto 0) & dataout0(15 downto 0) when i_read ='1' and empty_wire = '0';
        datain0 <= X"000000000000" & i_data(15 downto 0);
        datain1 <= X"000000000000" & i_data(31 downto 16);
        fifo_data <= dataout1(15 downto 0) & dataout0(15 downto 0);
        
--        almostfull_wire <= almostful1 and almostful2;
--        empty_wire <= empty0 and empty1;
--        full_wire <= full1 and full2;

--        almostempty <= almostempty1 and almostempty2;
--        u_empty_reg_Pa0: spu_generic_reg1 generic map(REG_NUM=>0)
--         port map(clk=>clk, rst=>rst, i_d=>(empty0 and empty1), o_d=>empty);
        --u_full_reg_Pa0: spu_generic_reg1 generic map(REG_NUM=>5)
        -- port map(clk=>clk, rst=>rst, i_d=>almostful1, o_d=>full1);
        --u_full_reg_Pa1: spu_generic_reg1 generic map(REG_NUM=>5)
        -- port map(clk=>clk, rst=>rst, i_d=>almostful2, o_d=>full2);
--        almostful <= almostful1 and almostful2;
--        u_full_reg_Pa0: spu_generic_reg1 generic map(REG_NUM=>8)
--         port map(clk=>clk, rst=>rst, i_d=>almostful, o_d=>full);

          almostfull_wire <= '1' when pointer = DEPTH - 6 else '0';
          full_wire <= '1' when pointer = DEPTH - 1 else '0';  
          process( clk, rst ) begin
            if rising_edge( clk ) and rst = '0' then
                 almostfull <= almostfull_wire;
                 full <= full_wire_delay;
--                 empty <= empty_wire;
            end if;
          end process;        
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then
                 full_wire_delay <= full_wire;
            end if;
          end process;    
                   
--           process( clk,rst ) begin
--             if rising_edge( clk ) and rst = '0' then      
--               if (i_write ='1' and i_read ='0' and full_wire = '0') then
--                 write_wire <= '1';
--               else
--                 write_wire <= '0';
--               end if;
--             end if;             
--           end process;
--                             full <= full_wire; 
                           empty <= empty_wire; 
            -- update the fifo pointer
          process( clk,rst ) begin
            if rising_edge( clk ) and rst = '0' then      
              if (i_write ='1' and i_read ='0' and full_wire = '0') then
                if  (empty_wire = '0') then
                  pointer <= pointer + 1;
                else
                  empty_wire <= '0';
                end if;
              elsif (i_write ='0' and i_read ='1' and empty_wire = '0') then
                if (pointer > 0) then
                  pointer <= pointer - 1;
                else
                  empty_wire <= '1';
                end if;
              end if;
            end if;
          end process;
      end generate;
    end generate;
      
    -- 64-bit
    ----------------------------------------------------------------
    BUILTIN_FIFO_64BIT: if (WIDTH = 64) generate
      fifo64w512d_gen: if (DEPTH > 128 and DEPTH <= 512) generate
--        signal dataout : std_logic_vector(63 downto 0);
--        signal datain  : std_logic_vector(63 downto 0);
--			signal full           : std_logic := '0';
--			signal empty          : std_logic := '1';
--			signal almostfull_wire: std_logic := '0';
--			signal full_wire		 : std_logic := '0';
--			signal almostfull     : std_logic := '0';
      begin
        FIFO36_72_inst : FIFO36_72
        generic map (
          ALMOST_FULL_OFFSET => X"0006", -- Sets almost full threshold
          ALMOST_EMPTY_OFFSET => X"0006", -- Sets the almost empty threshold
          DO_REG => 0, -- Enable output register (0 or 1)
          -- Must be 1 if EN_SYN = FALSE
          EN_ECC_READ => FALSE, -- Enable ECC decoder, TRUE or FALSE
          EN_ECC_WRITE => FALSE, -- Enable ECC encoder, TRUE or FALSE
          EN_SYN => TRUE, -- Specifies FIFO as Asynchronous (FALSE) or Synchronous (TRUE)
          FIRST_WORD_FALL_THROUGH => TRUE, -- Sets the FIFO FWFT to TRUE or FALSE
          SIM_MODE => "SAFE") -- Simulation: "SAFE" vs "FAST", see "Synthesis and Simulation
          -- Design Guide" for details
        port map (
          ALMOSTEMPTY => open, -- 1-bit almost empty output flag
          ALMOSTFULL => almostfull_wire, -- 1-bit almost full output flag
          DBITERR => open, -- 1-bit double bit error status output
          DO => dataout, -- 64-bit data output
          DOP => open, -- 4-bit parity data output
          ECCPARITY => open, -- 8-bit generated error correction parity
          EMPTY => empty_wire, -- 1-bit empty output flag
          FULL => full_wire, -- 1-bit full output flag
          RDCOUNT => open, -- 9-bit read count output
          RDERR => open, -- 1-bit read error output
          WRCOUNT => open, -- 9-bit write count output
          WRERR => open, -- 1-bit write error
          DI => datain, -- 64-bit data input
          DIP => "00000000", -- 4-bit parity input
          RDCLK => clk, -- 1-bit read clock input
          RDEN => i_read, -- 1-bit read enable input
          RST => rst, -- 1-bit reset input
          WRCLK => clk, -- 1-bit write clock input
          WREN => i_write -- 1-bit write enable input
        );
		  
--        datain <= i_data when full_wire = '0' and i_write = '1';
--        fifo_data <= dataout when i_read ='1' and empty_wire = '0';
        datain <= i_data;
        fifo_data <= dataout;
                  
                  process( clk ) begin
                    if rising_edge( clk ) and rst = '0' then
                         almostfull <= almostfull_wire;
                         full <= full_wire;
                         empty <= empty_wire;
                    end if;
                  end process;      
      end generate;
    end generate;
    
    -- Register output
    u_data_reg_Pa0: spu_generic_reg generic map(REG_NUM=>OUT_REG_NUM, REG_WIDTH=>WIDTH)
      port map(clk=>clk, rst=>rst, i_d=>fifo_data, o_d=>o_data);
end rtl;
