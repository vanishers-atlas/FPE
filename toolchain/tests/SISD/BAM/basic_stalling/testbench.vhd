library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;
	signal  report_stall : std_logic;

	signal  external_stall : std_logic;

	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	PUT_FIFO_0_write : std_logic;

begin
  UUT : entity work.test_FPE_inst(arch)
		port map (
			PUT_FIFO_0_write => PUT_FIFO_0_write,
			PUT_FIFO_0_data  => PUT_FIFO_0_data,
			clock => clock,
			kickoff => kickoff,
			running => running,
			external_stall => external_stall,
			report_stall => report_stall
		);

	clock_gen : process
	begin
	  loop
	    clock <= not clock;
	    wait for 50 ns;
	  end loop;
	end process;

	-- Signal kickoff after 200 ns
	kickoff <= '1' after 200 ns, '0' after 300 ns;


	stoff_external_stall : process
		variable period_index : integer := 0;
		variable curr_peroid : integer := 0;
		type  half_period_array is array (0 to 6) of integer;
		constant half_periods : half_period_array :=
		(
			1, 1 , 2, 4, 5, 6, 7
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

	spoff_PUT_FIFO_0 : process
	  variable  data_index : integer := 0;
	  type  data_array is array (0 to 79) of std_logic_vector(3 downto 0);
	  constant test_data : data_array :=
	  (
			"0000", "0001", "0001", "0010", "0010", "0011", "0011", "0100",
			"0100", "0101", "0101", "0110", "0110", "0111", "0111", "1000",
			"1000", "1001", "1001", "1010", "1010", "1011", "1011", "1100",
			"1100", "1101", "1101", "1110", "1110", "1111", "1111", "0000",

			"0000", "1111", "1111", "1110", "1110", "1101", "1101", "1100",
			"1100", "1011", "1011", "1010", "1010", "1001", "1001", "1000",
			"1000", "0111", "0111", "0110", "0110", "0101", "0101", "0100",
			"0100", "0011", "0011", "0010", "0010", "0001", "0001", "0000",

			"0011", "0110", "1001", "1100", "1111", "0010", "0101", "1000",

			"1101", "1010", "0111", "0100", "0001", "1110", "1011", "1000"
	  );
	begin
	  -- Flag existance for log checking
	  report "PUT_FIFO_0: Exists" severity note;

	  wait until running = '1';

	  -- Happen expected output
	  while 0 <= data_index and data_index < test_data'Length loop


	    wait until rising_edge(clock) and PUT_FIFO_0_write = '1';

	    -- Check not stalling output
	    assert(report_stall = '0' or report_stall = 'L')
	      report "PUT_FIFO_0: Output while stalling"
	      severity error;

	    -- Check the data is correct
	    assert(PUT_FIFO_0_data = test_data(data_index))
	      report "PUT_FIFO_0: Incorrect " & integer'Image(data_index) & " th output"
	      severity error;
	    assert(PUT_FIFO_0_data /= test_data(data_index))
	      report "PUT_FIFO_0: Correct " & integer'Image(data_index) & " th output"
	      severity note;

	    -- Advance to output index
	    data_index := data_index + 1;
	  end loop;

	  -- Flag all expected output given
	  report "PUT_FIFO_0: All expected output received" severity note;

	  -- Check for unexpected output
	  loop
	    wait until rising_edge(clock) and PUT_FIFO_0_write = '1';
	    report "PUT_FIFO_0: Extra output" severity error;
	  end loop;

	end process;


end architecture;
