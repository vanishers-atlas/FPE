
signal	GET_FIFO_XX_data : std_logic_vector(YY downto 0);
signal	GET_FIFO_XX_adv  : std_logic;



spoff_GET_FIFO_XX : process
  variable  data_index : integer := 0;
  type  data_array is array (0 to ) of std_logic_vector(YY downto 0);
  constant test_data : data_array :=
  (

  );
begin
  -- Flag existance for log checking
  report "GET_FIFO_XX: Exists" severity note;

  wait until running = '1';

  -- Happen expected input
  while 0 <= data_index and data_index < test_data'Length loop
    GET_FIFO_XX_data <= test_data(data_index);

    wait until rising_edge(clock);
    if GET_FIFO_0_adv = '1' then
      -- Advance to input index
      data_index := data_index + 1;
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
