signal	PUT_FIFO_XX_data  : std_logic_vector(YY downto 0);
signal	PUT_FIFO_XX_write : std_logic;
signal	PUT_FIFO_XX_ready : std_logic;



spoff_PUT_FIFO_XX : process
  variable  data_index : integer := 0;
  type  data_array is array (0 to ) of std_logic_vector(YY downto 0);
  constant test_data : data_array :=
  (

  );
  variable delay_index : integer := 0;
  variable curr_delay : integer := 0;
  type  delay_array is array (0 to ) of integer;
  constant delays : delay_array :=
  (

  );
begin
  PUT_FIFO_XX_ready <= '0';

  -- Flag existance for log checking
  report "PUT_FIFO_XX: Exists" severity note;

  wait until running = '1';

  -- Happen expected output
  while 0 <= data_index and data_index < test_data'Length loop
    -- Incrememnt delay
    wait until rising_edge(clock) ;
    curr_delay := curr_delay + 1;

    -- Check for output
    if PUT_FIFO_XX_write = '1' then

      -- Check not stalling
      assert(report_stall = '0' or report_stall = 'L')
        report "PUT_FIFO_XX: Output while stalling"
        severity error;

      -- Check FIFO ready
      assert(PUT_FIFO_XX_ready = '1')
        report "PUT_FIFO_XX: Output while not ready"
        severity error;

      -- Check the data is correct
      assert(PUT_FIFO_XX_data = test_data(data_index))
        report "PUT_FIFO_XX: Incorrect " & integer'Image(data_index) & " th output"
        severity error;
      assert(PUT_FIFO_XX_data /= test_data(data_index))
        report "PUT_FIFO_XX: Correct " & integer'Image(data_index) & " th output"
        severity note;

      -- Advance to output indexes
      data_index := data_index + 1;
      delay_index := (delay_index + 1) mod delays'length;

      -- Reset current delay
      curr_delay := 0;
    end if;

    -- Set ready signal
    if curr_delay >= delays(delay_index) then
      PUT_FIFO_XX_ready <= '1';
    else
      PUT_FIFO_XX_ready <= '0';
    end if;

  end loop;

  -- Flag all expected output given
  report "PUT_FIFO_XX: All expected output received" severity note;

  -- Check for unexpected output
  PUT_FIFO_XX_ready <= '1';
  loop
    wait until rising_edge(clock) and PUT_FIFO_XX_write = '1';
    report "PUT_FIFO_XX: Extra output" severity error;
  end loop;

end process;
