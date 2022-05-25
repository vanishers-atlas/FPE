library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;
	signal  external_stall : std_logic;
	signal  report_stall : std_logic;

	signal	PUT_FIFO_0_write : std_logic;
	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal  PUT_FIFO_0_index : integer := 0;
	type  PUT_FIFO_0_data_array is array (0 to 47) of std_logic_vector(3 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",

		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",

		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
	);

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

  -- Clock generate
  process
  begin
    loop
      clock <= not clock;
      wait for 50 ns;
    end loop;
  end process;

  -- Kickoff generation
	process
	begin
  	kickoff <= '0';
		wait for 250 ns;
		kickoff <= '1';
		wait until rising_edge(running);
		wait for 200 ns;
		kickoff <= '0';
		wait;
	end process;

	-- External stall generation
	process
	begin
		external_stall <= '0';
		wait for 500 ns;
		wait until falling_edge(clock);
		loop
			external_stall <= '1';
			wait for 400 ns;
			wait until falling_edge(clock);
			external_stall <= '0';
			wait for 400 ns;
			wait until falling_edge(clock);
		end loop;
	end process;

	-- Check external stall leads to a reported stall
	process(clock)
	begin
		if falling_edge(clock) then
			if external_stall = '1' then
				assert report_stall = '1'
					report "external_stall not raising reported stall"
					severity error;
			end if;
		end if;
	end process;

	-- Check output
	process (clock)
	begin
		if falling_edge(clock) and PUT_FIFO_0_write = '1' then
			-- Check expecting output
			assert(0 <= PUT_FIFO_0_index and PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)
				report "Unexpected output"
				severity error;

			-- Check not stalling output
			assert(report_stall = '0' or report_stall = 'L')
				report "Output while stalling output"
				severity error;

			-- Check the data is correct
			assert(PUT_FIFO_0_data = PUT_FIFO_0_test_data(PUT_FIFO_0_index))
				report "Incorrect " & integer'Image(PUT_FIFO_0_index) & " th output"
				severity error;
			assert(PUT_FIFO_0_data /= PUT_FIFO_0_test_data(PUT_FIFO_0_index))
				report "Correct " & integer'Image(PUT_FIFO_0_index) & " th output"
				severity note;

			-- Advance to output index
			PUT_FIFO_0_index <= PUT_FIFO_0_index + 1;
		end if;
	end process;

	-- Check end state
	process
	begin
		-- Wait until the end of simulation
		wait for 100 us;

		-- Check all ezpected output was received
		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all ezpected output recieved"
			severity error;
		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all ezpected output recieved"
			severity note;
	end process;

end architecture;
