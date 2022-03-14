library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;

	signal	PUT_FIFO_0_data  : std_logic_vector(19 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal  PUT_FIFO_0_index : integer := 0;
	type  PUT_FIFO_0_data_array is array (0 to 223) of std_logic_vector(19 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
		-- Test MOV and ACC persistances
		"00000000000000000000", "00000000000000000000", "00000000001111111111", "00000000001111111111",
		"11111111110000000000", "11111111110000000000", "11111111111111111111", "11111111111111111111",

		-- Test LSH 1
		"00100010001000100010", "01000100010001000100",	"10001000100010001000", "00010001000100010000",
		"01000100010001000100", "10001000100010001000", "00010001000100010000", "00100010001000100000",
		"10001000100010001000", "00010001000100010000", "00100010001000100000", "01000100010001000000",
		"00010001000100010000", "00100010001000100000", "01000100010001000000", "10001000100010000000",

		-- Test LSH 2
		"01000100010001000100", "00010001000100010000", "01000100010001000000", "00010001000100000000",
		"10001000100010001000", "00100010001000100000", "10001000100010000000", "00100010001000000000",
		"00010001000100010000", "01000100010001000000", "00010001000100000000", "01000100010000000000",
		"00100010001000100000", "10001000100010000000", "00100010001000000000", "10001000100000000000",

		-- Test LSH 3
		"10001000100010001000", "01000100010001000000", "00100010001000000000", "00010001000000000000",
		"00010001000100010000", "10001000100010000000", "01000100010000000000", "00100010000000000000",
		"00100010001000100000", "00010001000100000000", "10001000100000000000", "01000100000000000000",
		"01000100010001000000", "00100010001000000000", "00010001000000000000", "10001000000000000000",

		-- Test LRL 1
		"00100010001000100010", "01000100010001000100", "10001000100010001000", "00010001000100010001",
		"01000100010001000100", "10001000100010001000", "00010001000100010001", "00100010001000100010",
		"10001000100010001000", "00010001000100010001", "00100010001000100010", "01000100010001000100",
		"00010001000100010001", "00100010001000100010", "01000100010001000100", "10001000100010001000",

		-- Test LRL 2
		"01000100010001000100", "00010001000100010001", "01000100010001000100", "00010001000100010001",
		"10001000100010001000", "00100010001000100010", "10001000100010001000", "00100010001000100010",
		"00010001000100010001", "01000100010001000100", "00010001000100010001", "01000100010001000100",
		"00100010001000100010", "10001000100010001000", "00100010001000100010", "10001000100010001000",

		-- Test LRL 3
		"10001000100010001000", "01000100010001000100", "00100010001000100010", "00010001000100010001",
		"00010001000100010001", "10001000100010001000", "01000100010001000100", "00100010001000100010",
		"00100010001000100010", "00010001000100010001", "10001000100010001000", "01000100010001000100",
		"01000100010001000100", "00100010001000100010", "00010001000100010001", "10001000100010001000",

		-- Test RSH 1
		"01000100010001000100", "00100010001000100010", "00010001000100010001", "00001000100010001000",
		"00100010001000100010", "00010001000100010001", "00001000100010001000", "00000100010001000100",
		"00010001000100010001", "00001000100010001000", "00000100010001000100", "00000010001000100010",
		"00001000100010001000", "00000100010001000100", "00000010001000100010", "00000001000100010001",

		-- Test RSH 2
		"00100010001000100010", "00001000100010001000", "00000010001000100010", "00000000100010001000",
		"00010001000100010001", "00000100010001000100", "00000001000100010001", "00000000010001000100",
		"00001000100010001000", "00000010001000100010", "00000000100010001000", "00000000001000100010",
		"00000100010001000100", "00000001000100010001", "00000000010001000100", "00000000000100010001",

		-- Test RSH 3
		"00010001000100010001", "00000010001000100010", "00000000010001000100", "00000000000010001000",
		"00001000100010001000", "00000001000100010001", "00000000001000100010", "00000000000001000100",
		"00000100010001000100", "00000000100010001000", "00000000000100010001", "00000000000000100010",
		"00000010001000100010", "00000000010001000100", "00000000000010001000", "00000000000000010001",

		-- Test RRL 1
		"01000100010001000100", "00100010001000100010", "00010001000100010001", "10001000100010001000",
		"00100010001000100010", "00010001000100010001", "10001000100010001000", "01000100010001000100",
		"00010001000100010001", "10001000100010001000", "01000100010001000100", "00100010001000100010",
		"10001000100010001000", "01000100010001000100", "00100010001000100010", "00010001000100010001",

		-- Test RRL 2
		"00100010001000100010", "10001000100010001000", "00100010001000100010", "10001000100010001000",
		"00010001000100010001", "01000100010001000100", "00010001000100010001", "01000100010001000100",
		"10001000100010001000", "00100010001000100010", "10001000100010001000", "00100010001000100010",
		"01000100010001000100", "00010001000100010001", "01000100010001000100", "00010001000100010001",

		-- Test RRL 3
		"00010001000100010001", "00100010001000100010", "01000100010001000100", "10001000100010001000",
		"10001000100010001000", "00010001000100010001", "00100010001000100010", "01000100010001000100",
		"01000100010001000100", "10001000100010001000", "00010001000100010001", "00100010001000100010",
		"00100010001000100010", "01000100010001000100", "10001000100010001000", "00010001000100010001",

		-- Test NOT
		"11111111111111111111", "00000000000000000000",
		"11111111110000000000", "00000000001111111111",
		"00000000001111111111", "11111111110000000000",
		"00000000000000000000", "11111111111111111111",

		-- Test MUL
		"00000000000000000000", "00000000000000000000", "00000000000000000001", "00001111111000000001",
		"00000000000000000000", "00000000000000000000", "00000000000000000001", "00001111111000000001",
		"00000000000000000000", "00000000000000000000", "00000000000000000001", "00001111111000000001",
		"00000000000000000000", "00000000000000000001", "00000000000000000100", "00001111111000000001"

	);

begin
  UUT : entity work.test_FPE_inst(arch)
		port map (
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

  -- Signal kickoff after 250 ns
  kickoff <= '1' after 250 ns, '0' after 350 ns;

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
				report "Incorrect " & integer'Image(PUT_FIFO_0_index) & "th output" & lf & ""
				& integer'Image(to_integer(unsigned(PUT_FIFO_0_data))) & " != " & integer'Image(to_integer(unsigned(PUT_FIFO_0_test_data(PUT_FIFO_0_index))))
				severity error;
			assert(PUT_FIFO_0_data /= PUT_FIFO_0_test_data(PUT_FIFO_0_index))
				report "Correct " & integer'Image(PUT_FIFO_0_index) & "th output" & lf & ""
				& integer'Image(to_integer(unsigned(PUT_FIFO_0_data))) & " = " & integer'Image(to_integer(unsigned(PUT_FIFO_0_test_data(PUT_FIFO_0_index))))
				severity note;

			-- Advance to output index
			PUT_FIFO_0_index <= PUT_FIFO_0_index + 1;
		end if;
	end process;

	-- Check end state
	process
	begin
		-- Wait until the end of simulation
		wait for 150 us;

		-- Check all expected output was received
		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all expected output received"
			severity error;
		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all expected output received"
			severity note;
	end process;

end architecture;
