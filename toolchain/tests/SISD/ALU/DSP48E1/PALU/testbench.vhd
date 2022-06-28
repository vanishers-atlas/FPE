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
	clock_gen : process
	begin
	  loop
	    clock <= not clock;
	    wait for 50 ns;
	  end loop;
	end process;

	-- Signal kickoff after 200 ns
	kickoff <= '1' after 200 ns, '0' after 300 ns;


	spoff_PUT_FIFO_0 : process
	  variable  data_index : integer := 0;
	  type  data_array is array (0 to 335) of std_logic_vector(3 downto 0);
	  constant test_data : data_array :=
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

			-- Test PNAND
			"1111", "1111", "1111", "0000",
			"1111", "1111", "1111", "0000",
			"1111", "1111", "1111", "0000",
			"1111", "0000", "1111", "0000",

			-- Test POR
			"0000", "1111", "1111", "1111",
			"0000", "1111", "1111", "1111",
			"0000", "1111", "1111", "1111",
			"0000", "1111", "0000", "1111",

			-- Test PNOR
			"1111", "0000", "0000", "0000",
			"1111", "0000", "0000", "0000",
			"1111", "0000", "0000", "0000",
			"1111", "0000", "1111", "0000",

			-- Test PXOR
			"0000", "1111", "1111", "0000",
			"0000", "1111", "1111", "0000",
			"0000", "1111", "1111", "0000",
			"0000", "0000", "0000", "0000",

			-- Test PXNOR
			"1111", "0000", "0000", "1111",
			"1111", "0000", "0000", "1111",
			"1111", "0000", "0000", "1111",
			"1111", "1111", "1111", "1111",

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
	  wait until running = '1';

	  -- Happen expected output
	  while 0 <= data_index and data_index < test_data'Length loop

	    wait until rising_edge(clock) and PUT_FIFO_0_write = '1';

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

	  -- Mark all expected output given
	  report "PUT_FIFO_0: All expected output received" severity note;

	  -- Check for unexpected output
	  loop
	    wait until rising_edge(clock) and PUT_FIFO_0_write = '1';
	    report "PUT_FIFO_0: Extra output" severity error;
	  end loop;

	end process;

end architecture;
