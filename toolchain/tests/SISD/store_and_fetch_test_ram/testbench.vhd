library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;

	signal	GET_FIFO_0_data : std_logic_vector(3 downto 0);
	signal	GET_FIFO_0_red  : std_logic;
	signal  GET_FIFO_0_index : integer := 0;
	type  GET_FIFO_0_data_array is array (0 to 15) of std_logic_vector(3 downto 0);
	constant GET_FIFO_0_test_data : GET_FIFO_0_data_array :=
	(
		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
	);

	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal  PUT_FIFO_0_index : integer := 0;
	type  PUT_FIFO_0_data_array is array (0 to 15) of std_logic_vector(3 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
	);

begin
  UUT : entity work.sFPE_inst(arch)
		port map (
			GET_FIFO_0_data => GET_FIFO_0_data,
			GET_FIFO_0_red  => GET_FIFO_0_red,
			PUT_FIFO_0_data  => PUT_FIFO_0_data,
			PUT_FIFO_0_write => PUT_FIFO_0_write,
			clock => clock,
			kickoff => kickoff,
			running => running
		);

  -- Clock generate process
  process
  begin
    loop
      clock <= not clock;
      wait for 50 ns;
    end loop;
  end process;

  -- Sigbal kickoff after 250 ns
  kickoff <= '1' after 250 ns, '0' after 350 ns;

	-- Provide input
	process (clock)
	begin
		if falling_edge(clock) and GET_FIFO_0_red = '1' then
			-- Check has input
			assert(0 <= GET_FIFO_0_index and GET_FIFO_0_index < GET_FIFO_0_test_data'Length)
				report "Trying to take extra input"
				severity error;

			GET_FIFO_0_index <= GET_FIFO_0_index + 1;
		end if;
	end process;
	GET_FIFO_0_data <= GET_FIFO_0_test_data(GET_FIFO_0_index) when 0 <= GET_FIFO_0_index and GET_FIFO_0_index < GET_FIFO_0_test_data'Length
		else (others => 'U');

	-- Check output
	process (clock)
	begin
		if rising_edge(clock) and PUT_FIFO_0_write = '1' then
			-- Check expecting output
			assert(0 <= PUT_FIFO_0_index and PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)
				report "Unexpected output"
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

		-- Check all input was taken
		assert(GET_FIFO_0_index  = GET_FIFO_0_test_data'Length)
			report "Not all input taken"
			severity error;
		assert(GET_FIFO_0_index /= GET_FIFO_0_test_data'Length)
			report"all input taken"
			severity note;

		-- Check all ezpected output was received
		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all ezpected output recieved"
			severity error;
		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all ezpected output recieved"
			severity note;
	end process;

end architecture;
