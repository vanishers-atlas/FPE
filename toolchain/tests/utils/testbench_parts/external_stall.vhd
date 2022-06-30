signal  external_stall : std_logic;


stoff_external_stall : process
  variable period_index : integer := 0;
  variable curr_peroid : integer := 0;
  type  half_period_array is array (0 to ) of integer;
  constant half_periods : half_period_array :=
  (

  );
begin
  external_stall <= '0';
  wait until running = '1';
  loop
    wait until rising_edge(clock);
      -- Handle stall toggleing
      curr_peroid := curr_peroid + 1;
      if curr_peroid >= half_periods(period_index) then
        curr_peroid := 0;
        period_index := (period_index + 1) mod half_periods'length;
        external_stall <= not external_stall;
      end if;

    -- Handle stall checking
    if external_stall = '1' then
      assert(report_stall = '1')
	      report "External stall not raising reported stall"
	      severity error;
    end if;

  end loop;
end process;
