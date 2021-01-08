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

	signal	PUT_FIFO_0_data  : std_logic_vector(31 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal  PUT_FIFO_0_index : integer := 0;
	type  PUT_FIFO_0_data_array is array (0 to 46) of std_logic_vector(31 downto 0);
	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=
	(
		-- Test MOV,
		"00111100001111000011110000111100",
		"11000011110000111100001111000011",
		"01101001011010010110100101101001",
		"01101001011010010110100101101001",

		-- Test left shifts
		"10011000011110000111100001100110",
		"10011000011110000111100001100110",
		"00110000111100001111000011001100",
		"00110000111100001111000011001100",

		-- Test right shifts
		"01100110000111100001111000011001",
		"01100110000111100001111000011001",
		"00110011000011110000111100001100",
		"00110011000011110000111100001100",

		-- Test left rolls
		"10011000011110000111100001100111",
		"10011000011110000111100001100111",
		"00110000111100001111000011001111",
		"00110000111100001111000011001111",


		-- Test right rolls
		"11100110000111100001111000011001",
		"11100110000111100001111000011001",
		"11110011000011110000111100001100",
		"11110011000011110000111100001100",


		-- Test multipleation
		"00000000000000000000000000000100",
		"00000000000000000000000000000100",
		"00000000000000000000000000000100",
		"00000000000000000000000000000100",


		-- Test ADD
		"00100000000000000000000000000100",
		"00100000000000000000000000000100",
		"00100000000000000000000000000100",
		"00100000000000000000000000000100",


		-- Test SUB
		"00000000000000000000000000000001",
		"11111111111111111111111111111111",
		"00000000000000000000000000000001",
		"00000000000000000000000000000001",
		"00000000000000000000000000000000",

		-- Test NOT
		"10101010101010101010101010101010",
		"10101010101010101010101010101010",

		-- Test OR
		"01110111011101110111011101110111",
		"01110111011101110111011101110111",
		"01110111011101110111011101110111",
		"01010101010101010101010101010101",


		-- Test AND
		"00010001000100010001000100010001",
		"00010001000100010001000100010001",
		"00010001000100010001000100010001",
		"01010101010101010101010101010101",

		-- Test XOR
		"01100110011001100110011001100110",
		"01100110011001100110011001100110",
		"01100110011001100110011001100110",
		"00000000000000000000000000000000"
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
		wait for 100 us;

		-- Check all expected output was received
		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)
			report "Not all expected output received"
			severity error;
		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)
			report "all expected output received"
			severity note;
	end process;

end architecture;
