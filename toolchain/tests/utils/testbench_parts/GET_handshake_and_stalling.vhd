
signal	GET_FIFO_XX_data : std_logic_vector(YY downto 0);
signal	GET_FIFO_XX_valid : std_logic;
signal	GET_FIFO_XX_adv  : std_logic;



spoff_GET_FIFO_XX : process
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
  -- Flag existance for log checking
  report "GET_FIFO_XX: Exists" severity note;

  GET_FIFO_XX_valid <= '0';

  wait until running = '1';

  -- Happen expected input
  while 0 <= data_index and data_index < test_data'Length loop
    if curr_delay >= delays(delay_index) then
      GET_FIFO_XX_valid <= '1';
      GET_FIFO_0_data <= test_data(data_index);
    else
      GET_FIFO_XX_valid <= '0';
      GET_FIFO_0_data <= (others => 'X');
    end if;

    wait until rising_edge(clock);
    if GET_FIFO_0_adv = '1' then
      -- Check not stalling input
      assert(report_stall = '0' or report_stall = 'L')
        report "GET_FIFO_0: Output while stalling"
        severity error;

      -- Advance to input index
      data_index := data_index + 1;
      delay_index := (delay_index + 1) mod delays'length;
      curr_delay := 0;
    else
      curr_delay := curr_delay + 1;
    end if;

  end loop;

  -- Flag all expected input taken
  report "GET_FIFO_XX: All expected input taken" severity note;

  -- Check for unexpected input
  loop
    wait until rising_edge(clock) and GET_FIFO_XX_adv = '1';
    report "GET_FIFO_XX: Trying to take extra input" severity error;
  end loop;

end process;
