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
    # Generate neuron parameters
    weights = generate_neuron_parameters(input_neurons, output_neurons)

    # Save Neuron parameters in a mem filw for t3esting
    generate_ROM_mem_file(weights)

    # Generate test input
    test_inputs = generate_test_input(input_neurons, number_tests)

    # Compute output for each test
    test_outputs = generate_test_output(test_inputs, weights)

    # Generate layer testbrench
    generate_testbrench_file(input_neurons, output_neurons, number_tests, test_inputs, test_outputs)

def generate_neuron_parameters(input_neurons, output_neurons):
    weights = []
    threasholds = []

    for _ in range(output_neurons):
        weight_value = random.randrange(2**input_neurons)
        weights.append([])
        for i in range(input_neurons):
            # bit i th bit of input value is 0
            if math.floor(weight_value / 2**i) % 2 == 0:
                weights[-1].append(0)
            else:
                weights[-1].append(1)

    return weights

def generate_ROM_mem_file(weights):
    ROM_width = 1

    with open("test_ROM.mem", "w") as f:
        for test in weights:
            for weight in test:
                f.write(tc_utils.unsigned.encode(weight, ROM_width))
                f.write("\n")

def generate_test_input(input_neurons, number_tests):
    test_input = []

    for _ in range(number_tests):
        test_input.append([])

        input_value = random.randrange(2**input_neurons)
        for i in range(input_neurons):
            # bit i th bit of input value is 0
            if math.floor(input_value / 2**i) % 2 == 0:
                test_input[-1].append(0)
            else:
                test_input[-1].append(1)

    return test_input

def generate_test_output(inputs, weights):
    test_output = []
    for input in inputs:
        test_output.append([])
        for neuron_weights in weights:
            products = [ w ^ i
                for (w, i) in zip(neuron_weights, input)
            ]

            popcount = sum(products)

            test_output[-1].append(popcount)

    return test_output

def generate_testbrench_file(input_neurons, output_neurons, number_tests, test_inputs, test_outputs):
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
                input_neurons * number_tests - 1,
            )
        )
        f.write("	constant GET_FIFO_0_test_data : GET_FIFO_0_data_array :=\n")
        f.write("	(\n")

        # Add input values to testbench
        f.write("\t\t%s\n"%(
            ",\n\t\t".join(
                [
                    ", ".join(
                        [
                            "\"%s\""%(tc_utils.unsigned.encode(v, 1), )
                            for v in test_input
                        ]
                    )
                    for test_input in test_inputs
                ]
            )
        ))

        f.write("	);\n")
        f.write("\n")
        f.write("	signal	PUT_FIFO_0_data  : std_logic_vector(3 downto 0);\n")
        f.write("	signal	PUT_FIFO_0_write : std_logic;\n")
        f.write("	signal  PUT_FIFO_0_index : integer := 0;\n")
        f.write("	type  PUT_FIFO_0_data_array is array (0 to %i) of std_logic_vector(3 downto 0);\n"%(
                output_neurons * number_tests - 1,
            )
        )
        f.write("	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=\n")
        f.write("	(\n")

        # Add input values to testbench
        f.write("\t\t%s\n"%(
            ",\n\t\t".join(
                [
                    ", ".join(
                        [
                            "\"%s\""%(tc_utils.unsigned.encode(v, 4), )
                            for v in test_output
                        ]
                    )
                    for test_output in test_outputs
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
        f.write("		wait for 100 us;\n")
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
