library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;

	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal	PUT_FIFO_0_ready : std_logic;
	signal	PUT_FIFO_0_delay : integer := 0;
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
	type  PUT_FIFO_0_delay_array is array (0 to 47) of integer;
	constant PUT_FIFO_0_test_delay : PUT_FIFO_0_delay_array :=
	(
		0, 0, 0, 0, 0, 0, 0, 0,
		1, 1, 1, 1, 1, 1, 1, 1,

		4, 4, 4, 4, 4, 4, 4, 4,
		8, 8, 8, 8, 8, 8, 8, 8,

		0, 1, 1, 0, 0, 4, 4, 0,
		0, 8, 8, 0, 0, 1, 4, 8
	);

begin
  UUT : entity work.test_FPE_inst(arch)
		port map (
			PUT_FIFO_0_data  => PUT_FIFO_0_data,
			PUT_FIFO_0_write => PUT_FIFO_0_write,
			PUT_FIFO_0_ready => PUT_FIFO_0_ready,
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

	-- Generate PUT ready signal
	process (clock)
	begin
		if falling_edge(clock) then
			if PUT_FIFO_0_write = '1' then
				PUT_FIFO_0_delay <= 0;
			else
				PUT_FIFO_0_delay <= PUT_FIFO_0_delay + 1;
			end if;
		end if;
	end process;
	PUT_FIFO_0_ready <= '1' when (0 <= PUT_FIFO_0_index and PUT_FIFO_0_index < PUT_FIFO_0_test_delay'Length)
	 		and PUT_FIFO_0_delay >= PUT_FIFO_0_test_delay(PUT_FIFO_0_index)
		else '0';

	-- Check output
	process (clock)
	begin
		if falling_edge(clock) and PUT_FIFO_0_write = '1' then
			-- Check expecting output
			assert(0 <= PUT_FIFO_0_index and PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)
				report "Unexpected output PUT_FIFO_0"
				severity error;

			-- Check ready for output
			assert(0 <= PUT_FIFO_0_index and PUT_FIFO_0_ready = '1')
				report "Output when PUT_FIFO_0 wasn't ready"
				severity error;


			-- Check the data is correct
			assert(PUT_FIFO_0_data = PUT_FIFO_0_test_data(PUT_FIFO_0_index))
				report "Incorrect " & integer'Image(PUT_FIFO_0_index) & " th output PUT_FIFO_0"
				severity error;
			assert(PUT_FIFO_0_data /= PUT_FIFO_0_test_data(PUT_FIFO_0_index))
				report "Correct " & integer'Image(PUT_FIFO_0_index) & " th output PUT_FIFO_0"
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
