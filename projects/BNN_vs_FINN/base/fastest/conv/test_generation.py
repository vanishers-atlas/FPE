# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 6
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import random
import math
from FPE.toolchain import utils as tc_utils

def run_generation(input_r, input_c, input_d, number_kernals, number_tests):
    # Generate parameters
    parameters = []
    for kernal, thresholds in zip(
        generate_kernals(number_kernals, input_d),
        generate_thresholds(number_kernals, input_r, input_c, input_d)
    ):
        parameters.append(
            {
                "kernal" : kernal,
                "thresholds" : thresholds,
            }
        )

    # Save parameters in a mem filw for testing
    generate_files(number_kernals, input_r, input_c, input_d, parameters)

    # Generate test input
    test_inputs = generate_test_input(input_r, input_c, input_d, number_tests)

    # Compute output for each test
    test_outputs = generate_test_output(number_kernals, input_r, input_c, input_d, number_tests, parameters, test_inputs)

    # Generate layer testbrench
    generate_testbrench_file(input_r, input_c, input_d, number_tests, number_kernals, test_inputs, test_outputs)

def generate_kernals(number_kernals, input_d):

    kernals = []
    for _ in range(number_kernals):
        kernals.append([])
        for _ in range(3):
            kernals[-1].append([])
            for _ in range(3):
                kernals[-1][-1].append([])

                weight_value = random.randrange(2**input_d)
                for i in range(input_d):
                    # bit i th bit of input value is 0
                    if math.floor(weight_value / 2**i) % 2 == 0:
                        kernals[-1][-1][-1].append(0)
                    else:
                        kernals[-1][-1][-1].append(1)

    return kernals

def generate_thresholds(number_kernals, input_r, input_c, input_d):

    thresholds = []
    for _ in range(number_kernals):
        thresholds.append([])
        for _ in range(input_r):
            thresholds[-1].append([])
            for _ in range(input_c):
                # + 2 as @
                # threashold can take any value of the popcount (0 to kernal_r * kernal_c * input_d + 1)
                # randrange returns 0 <= and < end, so + 1 tp include kernal_r * kernal_c * input_d + 1
                thresholds[-1][-1].append(random.randrange(3 * 3 * input_d + 2))

    return thresholds

def generate_files(number_kernals, input_r, input_c, input_d, parameters):

    # Generate ROM File
    ROM_width = tc_utils.unsigned.width(3 * 3 * input_d + 1)
    with open("test_ROM.mem", "w") as f:
        # Handle the kernals region
        for k in range(number_kernals):
            for r in range(3):
                for c in range(3):
                    for d in range(input_d):
                        f.write(tc_utils.unsigned.encode(parameters[k]["kernal"][r][c][d], ROM_width))
                        f.write("\n")

        # Handle threashold region
        for r in range(input_r):
            for c in range(input_c):
                for k in range(number_kernals):
                    f.write(tc_utils.unsigned.encode(parameters[k]["thresholds"][r][c], ROM_width))
                    f.write("\n")

    # Generate generics File
    with open("conv_layer_test_generics.json", "w") as f:
        f.write("{\n")
        f.write("\t\"BAM_0_base\": 0,\n")
        f.write("\t\"BAM_0_increment\": 1,\n")
        f.write("\t\"BAM_1_base\": %i,\n"%(0*(input_c + 2)*input_d), )
        f.write("\t\"BAM_1_increment\": 1,\n")
        f.write("\t\"BAM_2_base\": %i,\n"%(1*(input_c + 2)*input_d), )
        f.write("\t\"BAM_2_increment\": 1,\n")
        f.write("\t\"BAM_3_base\": %i,\n"%(2*(input_c + 2)*input_d), )
        f.write("\t\"BAM_3_increment\": 1,\n")
        f.write("\t\"BAM_4_base\": 0,\n")
        f.write("\t\"BAM_4_increment\": 1,\n")
        f.write("\t\"BAM_5_base\": %i,\n"%(3*3*input_d*number_kernals))
        f.write("\t\"BAM_5_increment\": 1,\n")
        f.write("\t\"ROM_mem_file\": \"..\\\\test_ROM.mem\"\n")
        f.write("}\n")

    # Generate generics File
    RAM_width = tc_utils.unsigned.width(3 * (input_c + 2) * input_d)
    RAM_depth = 2 ** RAM_width
    rom_kernal_span = 3 * 3 * input_d * number_kernals
    rom_thresholds_span = input_r * input_c * number_kernals
    with open("conv_layer_test_parameters.json", "w") as f:
        f.write("{\n")
        f.write("\t\"SIMD\": {\n")
        f.write("\t\t\"lanes\": 1\n")
        f.write("\t},\n")

        f.write("\t\"address_sources\": {\n")
        f.write("\t\t\"BAM_0\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_1\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_2\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_3\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(RAM_depth - 1, ) )
        f.write("\t\t\t\"step_max\": %i\n"%(3 * input_d, ) )
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_4\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(rom_kernal_span - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(rom_kernal_span - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"BAM_5\": {\n")
        f.write("\t\t\t\"addr_max\": %i,\n"%(rom_kernal_span + rom_thresholds_span - 1, ) )
        f.write("\t\t\t\"offset_max\": %i,\n"%(rom_thresholds_span - 1, ) )
        f.write("\t\t\t\"step_max\": 1\n")
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"data_memories\": {\n")
        f.write("\t\t\"GET\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"IMM\": {},\n")
        f.write("\t\t\"PUT\": {\n")
        f.write("\t\t\t\"FIFOs\": 1,\n")
        f.write("\t\t\t\"can_stall\": false,\n")
        f.write("\t\t\t\"data_width\": 1\n")
        f.write("\t\t},\n")
        f.write("\t\t\"RAM\": {\n")
        f.write("\t\t\t\"data_width\": 1,\n")
        f.write("\t\t\t\"depth\": %i\n"%(RAM_depth, ))
        f.write("\t\t},\n")
        f.write("\t\t\"REG\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(ROM_width, ))
        f.write("\t\t\t\"depth\": 2\n")
        f.write("\t\t},\n")
        f.write("\t\t\"ROM\": {\n")
        f.write("\t\t\t\"data_width\": %i,\n"%(ROM_width, ))
        f.write("\t\t\t\"depth\": %i\n"%(rom_kernal_span + rom_thresholds_span ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"execute_units\": {\n")
        f.write("\t\t\"ALU\": {\n")
        f.write("\t\t\t\"data_width\": %i\n"%(ROM_width + 1, ))
        f.write("\t\t}\n")
        f.write("\t},\n")

        f.write("\t\"instr_decoder\": {},\n")
        f.write("\t\"program_flow\": {}\n")
        f.write("}\n")

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

def generate_test_output(number_kernals, input_r, input_c, input_d, number_tests, parameters, test_inputs):
    test_output = []

    # Loop of each test
    for t in range(number_tests):
        test_output.append([])

        # Slide kernal over input
        for WR in range(input_r):
            test_output[-1].append([])
            for WC in range(input_c):
                test_output[-1][-1].append([])
                # Loop over each kernal
                for k in range(number_kernals):
                    popcount = 0
                    # Comput popcount for whole kernal
                    for KR in range(3):
                        for KC in range(3):
                            R = WR + KR - 1
                            C = WC + KC - 1

                            for d in range(input_d):
                                if 0 > R or input_r <= R:
                                    popcount += parameters[k]["kernal"][KR][KC][d] ^ 0
                                elif 0 > C or input_c <= C:
                                    popcount += parameters[k]["kernal"][KR][KC][d] ^ 0
                                else:
                                    popcount += parameters[k]["kernal"][KR][KC][d] ^ test_inputs[t][R][C][d]

                    # Perform sign function on popcount
                    if popcount > parameters[k]["thresholds"][WR][WC]:
                        test_output[-1][-1][-1].append(1)
                    else:
                        test_output[-1][-1][-1].append(0)

    return test_output

def generate_testbrench_file(input_r, input_c, input_d, number_tests, number_kernals, test_inputs, test_outputs):
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
                input_r * input_c * number_tests * number_kernals - 1,
            )
        )
        f.write("	constant PUT_FIFO_0_test_data : PUT_FIFO_0_data_array :=\n")
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
                                            "\"%s\""%(tc_utils.unsigned.encode(test_outputs[t][r][c][k], 1), )
                                            for k in range(number_kernals)
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
        f.write("		wait for 2500 us;\n")
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


run_generation(8, 8, 4, 6, 32)
