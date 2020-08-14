library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;

	signal	LANE_0_PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	LANE_0_PUT_FIFO_0_write : std_logic;
	signal  LANE_0_PUT_FIFO_0_index : integer := 0;

	signal	LANE_1_PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	LANE_1_PUT_FIFO_0_write : std_logic;
	signal  LANE_1_PUT_FIFO_0_index : integer := 0;

	type  PUT_FIFO_0_data_array is array (0 to 31) of std_logic_vector(3 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
	"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
	"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",

	"0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011",

	"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
	);

begin
  UUT : entity work.test_FPE_inst(arch)
		port map (
			LANE_0_PUT_FIFO_0_data  => LANE_0_PUT_FIFO_0_data,
			LANE_0_PUT_FIFO_0_write => LANE_0_PUT_FIFO_0_write,
			LANE_1_PUT_FIFO_0_data  => LANE_1_PUT_FIFO_0_data,
			LANE_1_PUT_FIFO_0_write => LANE_1_PUT_FIFO_0_write,
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

	-- Check output
	process (clock)
	begin
		if rising_edge(clock) and LANE_0_PUT_FIFO_0_write = '1' then
			-- Check expecting output
			assert(0 <= LANE_0_PUT_FIFO_0_index and LANE_0_PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)
				report "Unexpected output"
				severity error;

			-- Check the data is correct
			assert(LANE_0_PUT_FIFO_0_data  = PUT_FIFO_0_test_data(LANE_0_PUT_FIFO_0_index))
				report "Incorrect " & integer'Image(LANE_0_PUT_FIFO_0_index) & " th output lane 0"
				severity error;
			assert(LANE_0_PUT_FIFO_0_data /= PUT_FIFO_0_test_data(LANE_0_PUT_FIFO_0_index))
				report "Correct " & integer'Image(LANE_0_PUT_FIFO_0_index) & " th output lane 0"
				severity note;

			-- Advance to output index
			LANE_0_PUT_FIFO_0_index <= LANE_0_PUT_FIFO_0_index + 1;
		end if;

		if rising_edge(clock) and LANE_1_PUT_FIFO_0_write = '1' then
			-- Check expecting output
			assert(0 <= LANE_1_PUT_FIFO_0_index and LANE_1_PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)
				report "Unexpected output"
				severity error;

			-- Check the data is correct
			assert(LANE_1_PUT_FIFO_0_data  = PUT_FIFO_0_test_data(LANE_1_PUT_FIFO_0_index))
				report "Incorrect " & integer'Image(LANE_1_PUT_FIFO_0_index) & " th output lane 1"
				severity error;
			assert(LANE_1_PUT_FIFO_0_data /= PUT_FIFO_0_test_data(LANE_1_PUT_FIFO_0_index))
				report "Correct " & integer'Image(LANE_1_PUT_FIFO_0_index) & " th output lane 1"
				severity note;

			-- Advance to output index
			LANE_1_PUT_FIFO_0_index <= LANE_1_PUT_FIFO_0_index + 1;
		end if;
	end process;

	-- Check end state
	process
	begin
		-- Wait until the end of simulation
		wait for 100 us;

		-- Check all ezpected output was received
		assert(LANE_0_PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all ezpected output recieved lane 0"
			severity error;
		assert(LANE_0_PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all ezpected output recieved lane 0"
			severity note;

		-- Check all ezpected output was received
		assert(LANE_1_PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all ezpected output recieved lane 1"
			severity error;
		assert(LANE_1_PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all ezpected output recieved lane 1"
			severity note;
	end process;

end architecture;
