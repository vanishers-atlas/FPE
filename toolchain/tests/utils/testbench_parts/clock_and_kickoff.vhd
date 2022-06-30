signal 	clock : std_logic := '0';
signal	kickoff : std_logic := '0';
signal	running : std_logic;

signal  report_stall : std_logic;


clock_gen : process
begin
  loop
    clock <= not clock;
    wait for 50 ns;
  end loop;
end process;

-- Signal kickoff after 200 ns
kickoff <= '1' after 200 ns, '0' after 300 ns;
