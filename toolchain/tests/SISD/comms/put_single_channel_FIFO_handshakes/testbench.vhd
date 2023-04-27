library ieee;
use ieee.std_logic_1164.all;

entity testbench is

end entity;

architecture arch of testbench is
	signal 	clock : std_logic := '0';
	signal	kickoff : std_logic := '0';
	signal	running : std_logic;
	signal  report_stall : std_logic;


	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);
	signal	PUT_FIFO_0_write : std_logic;
	signal	PUT_FIFO_0_ready : std_logic;
begin
  UUT : entity work.test_FPE_inst(arch)
		port map (
			PUT_FIFO_0_ready => PUT_FIFO_0_ready,
			PUT_FIFO_0_write => PUT_FIFO_0_write,
			PUT_FIFO_0_data  => PUT_FIFO_0_data,
			clock => clock,
			kickoff => kickoff,
			running => running,
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

	spoff_PUT_FIFO_0 : process
	  variable  data_index : integer := 0;
	  type  data_array is array (0 to 47) of std_logic_vector(3 downto 0);
	  constant test_data : data_array :=
	  (
		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",

		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111",

		"0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
		"1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"
	  );
	  variable delay_index : integer := 0;
	  variable curr_delay : integer := 0;
	  type  delay_array is array (0 to 7) of integer;
	  constant delays : delay_array :=
	  (
			8, 2, 0, 0, 1, 1, 0, 1
	  );
	begin
	  PUT_FIFO_0_ready <= '0';

	  -- Flag existance for log checking
	  report "PUT_FIFO_0: Exists" severity note;

	  wait until running = '1';

	  -- Happen expected output
	  while 0 <= data_index and data_index < test_data'Length loop
	    -- Incrememnt delay
	    wait until rising_edge(clock) ;
	    curr_delay := curr_delay + 1;

	    -- Check for output
	    if PUT_FIFO_0_write = '1' then

	      -- Check not stalling
	      assert(report_stall = '0' or report_stall = 'L')
	        report "PUT_FIFO_0: Output while stalling"
	        severity error;

	      -- Check FIFO ready
	      assert(PUT_FIFO_0_ready = '1')
	        report "PUT_FIFO_0: Output while not ready"
	        severity error;

	      -- Check the data is correct
	      assert(PUT_FIFO_0_data = test_data(data_index))
	        report "PUT_FIFO_0: Incorrect " & integer'Image(data_index) & " th output"
	        severity error;
	      assert(PUT_FIFO_0_data /= test_data(data_index))
	        report "PUT_FIFO_0: Correct " & integer'Image(data_index) & " th output"
	        severity note;

	      -- Advance to output indexes
	      data_index := data_index + 1;
	      delay_index := (delay_index + 1) mod delays'length;

	      -- Reset current delay
	      curr_delay := 0;
	    end if;

	    -- Set ready signal
	    if curr_delay >= delays(delay_index) then
	      PUT_FIFO_0_ready <= '1';
	    else
	      PUT_FIFO_0_ready <= '0';
	    end if;

	  end loop;

	  -- Flag all expected output given
	  report "PUT_FIFO_0: All expected output received" severity note;

	  -- Check for unexpected output
	  PUT_FIFO_0_ready <= '1';
	  loop
	    wait until rising_edge(clock) and PUT_FIFO_0_write = '1';
	    report "PUT_FIFO_0: Extra output" severity error;
	  end loop;

	end process;


end architecture;
