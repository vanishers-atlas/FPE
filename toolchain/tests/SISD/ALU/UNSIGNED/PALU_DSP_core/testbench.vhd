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

	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal  PUT_FIFO_0_index : integer := 0;
	type  PUT_FIFO_0_data_array is array (0 to 287) of std_logic_vector(3 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
		-- Test PMOV and ACC persistances
		"0000", "0011", "1100", "1111",
		"0000", "0011", "1100", "1111",

		-- Test PLSH 1
		"0010", "0100", "1000", "0000",
		"0100", "1000", "0000", "0000",
		"1000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PLSH 2
		"0100", "1000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PLSH 2
		"1000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PLRL 1
		"0010", "0100", "1000", "0001",
		"0100", "1000", "0001", "0010",
		"1000", "0001", "0010", "0100",
		"0001", "0010", "0100", "1000",

		-- Test PLRL 2
		"0100", "1000", "0001", "0010",
		"0001", "0010", "0100", "1000",
		"0100", "1000", "0001", "0010",
		"0001", "0010", "0100", "1000",

		-- Test PLRL 3
		"1000", "0001", "0010", "0100",
		"0100", "1000", "0001", "0010",
		"0010", "0100", "1000", "0001",
		"0001", "0010", "0100", "1000",

		-- Test PRSH 1
		"0100", "0010", "0001", "0000",
		"0010", "0001", "0000", "0000",
		"0001", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PRSH 2
		"0010", "0001", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PRSH 3
		"0001", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PRRL 1
		"0100", "0010", "0001", "1000",
		"0010", "0001", "1000", "0100",
		"0001", "1000", "0100", "0010",
		"1000", "0100", "0010", "0001",

		-- Test PRRL 2
		"0010", "0001", "1000", "0100",
		"1000", "0100", "0010", "0001",
		"0010", "0001", "1000", "0100",
		"1000", "0100", "0010", "0001",

		-- Test PRRL 3
		"0001", "1000", "0100", "0010",
		"0010", "0001", "1000", "0100",
		"0100", "0010", "0001", "1000",
		"1000", "0100", "0010", "0001",

		-- Test PNOT
		"1111", "1100", "0011", "0000",
		"0000", "0011", "1100", "1111",

		-- Test PAND
		"0000", "0000", "0000", "1111",
		"0000", "0000", "0000", "1111",
		"0000", "0000", "0000", "1111",
		"0000", "1111", "0000", "1111",

		-- Test POR
		"0000", "1111", "1111", "1111",
		"0000", "1111", "1111", "1111",
		"0000", "1111", "1111", "1111",
		"0000", "1111", "0000", "1111",

		-- Test PXOR
		"0000", "1111", "1111", "0000",
		"0000", "1111", "1111", "0000",
		"0000", "1111", "1111", "0000",
		"0000", "0000", "0000", "0000",

		-- Test PADD
		"0000", "0010", "1111", "0000",
		"0000", "0010", "1111", "0000",
		"0000", "0010", "1111", "0000",
		"0000", "0010", "1100", "1110",

		-- Test PSUB
		"0010", "0000", "1111", "0000",
		"0010", "0000", "1111", "0000",
		"0010", "0000", "1111", "0000",
		"0000", "0000", "0000", "0000"

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
		wait for 250 us;

		-- Check all expected output was received
		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all expected output received"
			severity error;
		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all expected output received"
			severity note;
	end process;

end architecture;
