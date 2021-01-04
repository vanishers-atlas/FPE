# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 6
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import random
import math
from FPE.toolchain import utils as tc_utils

def run_generation(input_neurons, output_neurons, number_tests):
    input_r = input_c = 8
    input_d = 4
    number_tests = 16

    # Generate test input
    test_inputs = generate_test_input(input_r, input_c, input_d, number_tests)

    # Compute output for each test
    test_outputs = generate_test_output(input_r, input_c, input_d, number_tests, test_inputs)

    # Generate layer testbrench
    generate_testbrench_file(input_r, input_c, input_d, number_tests, test_inputs, test_outputs)

def generate_test_input(input_r, input_c, input_d, number_tests):
    test_input = []

    for _ in range(number_tests):
        test_input.append([])

        for _ in range(input_r):
            test_input[-1].append([])
            for _ in range(input_c):
                test_input[-1][-1].append([])

                input_value = random.randrange(2**input_d)
                for i in range(input_d):
                    # bit i th bit of input value is 0
                    if math.floor(input_value / 2**i) % 2 == 0:
                        test_input[-1][-1][-1].append(0)
                    else:
                        test_input[-1][-1][-1].append(1)
    return test_input

def generate_test_output(input_r, input_c, input_d, number_tests, test_inputs):
    test_output = []

    # Loop of each test
    for t in range(number_tests):
        test_output.append([])
        # Slide kernal over input
        for r in range(int(input_r/2)):
            test_output[t].append([])
            for c in range(int(input_c/2)):
                test_output[t][r].append([])
                # Loop over each kernal
                for d in range(input_d):
                    test_output[t][r][c].append(max(
                        [
                            test_inputs[t][2*r][2*c][d],
                            test_inputs[t][2*r][2*c+1][d],
                            test_inputs[t][2*r+1][2*c][d],
                            test_inputs[t][2*r+1][2*c+1][d],
                        ]
                    ))

    return test_output

def generate_testbrench_file(input_r, input_c, input_d, number_tests, test_inputs, test_outputs):
    with open("testbench_test.vhd", "w") as f:
        f.write("library ieee;\n")
        f.write("use ieee.std_logic_1164.all;\n")
        f.write("\n")
        f.write("entity testbench is\n")
        f.write("\n")
        f.write("end entity;\n")
        f.write("\n")
        f.write("architecture arch of testbench is\n")
        f.write("	signal 	clock : std_logic := '0';\n")
        f.write("	signal	kickoff : std_logic := '0';\n")
        f.write("	signal	running : std_logic;\n")
        f.write("\n")
        f.write("	signal	GET_FIFO_0_data : std_logic_vector(0 downto 0);\n")
        f.write("	signal	GET_FIFO_0_red  : std_logic;\n")
        f.write("	signal  GET_FIFO_0_index : integer := 0;\n")
        f.write("	type  GET_FIFO_0_data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                input_r * input_c * input_d * number_tests - 1,
            )
        )
        f.write("	constant GET_FIFO_0_test_data : GET_FIFO_0_data_array :=\n")
        f.write("	(\n")

        # Add input values to testbench
        f.write("\t\t%s\n"%(
            ",\n\n\t\t".join(
                [
                    ",\n\t\t".join(
                        [
                            ",\t\t".join(
                                [
                                    ", ".join(
                                        [
                                            "\"%s\""%(tc_utils.unsigned.encode(test_inputs[t][r][c][d], 1), )
                                            for d in range(input_d)
                                        ]
                                    )
                                    for c in range(input_c)
                                ]
                            )
                            for r in range(input_r)
                        ]
                    )
                    for t in range(number_tests)
                ]
            )
        ))

        f.write("	);\n")
        f.write("\n")
        f.write("	signal	PUT_FIFO_0_data  : std_logic_vector(0 downto 0);\n")
        f.write("	signal	PUT_FIFO_0_write : std_logic;\n")
        f.write("	signal  PUT_FIFO_0_index : integer := 0;\n")
        f.write("	type  PUT_FIFO_0_data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                input_r * input_c * input_d * number_tests / 4 - 1,
            )
        )
        f.write("	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=\n")
        f.write("	(\n")

        # Add input values to testbench
        # Add input values to testbench
        f.write("\t\t%s\n"%(
            ",\n\n\t\t".join(
                [
                    ",\n\t\t".join(
                        [
                            ",\t\t".join(
                                [
                                    ", ".join(
                                        [
                                            "\"%s\""%(tc_utils.unsigned.encode(test_outputs[t][r][c][d], 1), )
                                            for d in range(input_d)
                                        ]
                                    )
                                    for c in range(int(input_c/2))
                                ]
                            )
                            for r in range(int(input_r/2))
                        ]
                    )
                    for t in range(number_tests)
                ]
            )
        ))


        f.write("	);\n")
        f.write("\n")
        f.write("begin\n")
        f.write("  UUT : entity work.test_FPE_inst(arch)\n")
        f.write("		port map (\n")
        f.write("			GET_FIFO_0_data => GET_FIFO_0_data,\n")
        f.write("			GET_FIFO_0_red  => GET_FIFO_0_red,\n")
        f.write("			PUT_FIFO_0_data  => PUT_FIFO_0_data,\n")
        f.write("			PUT_FIFO_0_write => PUT_FIFO_0_write,\n")
        f.write("			clock => clock,\n")
        f.write("			kickoff => kickoff,\n")
        f.write("			running => running\n")
        f.write("		);\n")
        f.write("\n")
        f.write("   -- Clock generate process\n")
        f.write("   process\n")
        f.write("   begin\n")
        f.write("       loop\n")
        f.write("           clock <= not clock;\n")
        f.write("           wait for 2500 ps;\n")
        f.write("       end loop;\n")
        f.write("   end process;\n")
        f.write("\n")
        f.write("   -- Kickoff while there is input\n")
        f.write("   kickoff <= '1' when GET_FIFO_0_index < GET_FIFO_0_test_data'length else '0';\n")
        f.write("\n")
        f.write("	-- Provide input\n")
        f.write("	process (clock)\n")
        f.write("	begin\n")
        f.write("		if falling_edge(clock) and GET_FIFO_0_red = '1' then\n")
        f.write("			-- Check has input\n")
        f.write("			assert(0 <= GET_FIFO_0_index and GET_FIFO_0_index < GET_FIFO_0_test_data'Length)\n")
        f.write("				report \"Trying to take extra input\"\n")
        f.write("				severity error;\n")
        f.write("\n")
        f.write("			GET_FIFO_0_index <= GET_FIFO_0_index + 1;\n")
        f.write("		end if;\n")
        f.write("	end process;\n")
        f.write("	GET_FIFO_0_data <= GET_FIFO_0_test_data(GET_FIFO_0_index) when 0 <= GET_FIFO_0_index and GET_FIFO_0_index < GET_FIFO_0_test_data'Length\n")
        f.write("		else (others => 'U');\n")
        f.write("\n")
        f.write("	-- Check output\n")
        f.write("	process (clock)\n")
        f.write("	begin\n")
        f.write("		if rising_edge(clock) and PUT_FIFO_0_write = '1' then\n")
        f.write("			-- Check expecting output\n")
        f.write("			assert(0 <= PUT_FIFO_0_index and PUT_FIFO_0_index < PUT_FIFO_0_test_data'Length)\n")
        f.write("				report \"Unexpected output\"\n")
        f.write("				severity error;\n")
        f.write("\n")
        f.write("			-- Check the data is correct\n")
        f.write("			assert(PUT_FIFO_0_data = PUT_FIFO_0_test_data(PUT_FIFO_0_index))\n")
        f.write("				report \"Incorrect \" & integer'Image(PUT_FIFO_0_index) & \" th output\"\n")
        f.write("				severity error;\n")
        f.write("			assert(PUT_FIFO_0_data /= PUT_FIFO_0_test_data(PUT_FIFO_0_index))\n")
        f.write("				report \"Correct \" & integer'Image(PUT_FIFO_0_index) & \" th output\"\n")
        f.write("				severity note;\n")
        f.write("\n")
        f.write("			-- Advance to output index\n")
        f.write("			PUT_FIFO_0_index <= PUT_FIFO_0_index + 1;\n")
        f.write("		end if;\n")
        f.write("	end process;\n")
        f.write("\n")
        f.write("	-- Check end state\n")
        f.write("	process\n")
        f.write("	begin\n")
        f.write("		-- Wait until the end of simulation\n")
        f.write("		wait for 2 ms;\n")
        f.write("\n")
        f.write("		-- Check all input was taken\n")
        f.write("		assert(GET_FIFO_0_index  = GET_FIFO_0_test_data'Length)\n")
        f.write("			report \"Not all input taken\"\n")
        f.write("			severity error;\n")
        f.write("		assert(GET_FIFO_0_index /= GET_FIFO_0_test_data'Length)\n")
        f.write("			report\"all input taken\"\n")
        f.write("			severity note;\n")
        f.write("\n")
        f.write("		-- Check all ezpected output was received\n")
        f.write("		assert(PUT_FIFO_0_index  = PUT_FIFO_0_test_data'Length)\n")
        f.write("			report \"Not all ezpected output recieved\"\n")
        f.write("			severity error;\n")
        f.write("		assert(PUT_FIFO_0_index /= PUT_FIFO_0_test_data'Length)\n")
        f.write("			report \"all ezpected output recieve\"\n")
        f.write("			severity note;\n")
        f.write("	end process;\n")
        f.write("\n")
        f.write("end architecture;\n")


run_generation(8, 16, 32)
