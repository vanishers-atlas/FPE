# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import random
import copy
import math
import json
import os

from FPE.toolchain import utils as tc_utils
from FPE.toolchain.tests import utils as tests_utils


import generate_layer


def generate_data_input(number_tests, data_rows, data_cols, data_depth):
    tests = {}

    for test in range(number_tests):
        tests[test] = {}

        for row in range(data_rows):
            tests[test][row] = {}
            for col in range(data_cols):
                tests[test][row][col] = {}

                input_value = random.randrange(2**data_depth)
                for depth in range(data_depth):
                    # bit i th bit of input value is 0
                    if math.floor(input_value / 2**depth) % 2 == 0:
                        tests[test][row][col][depth] = 0
                    else:
                        tests[test][row][col][depth] = 1
    return tests

def generate_data_output(data_input):
    data_rows = len(data_input[0])
    assert data_rows % 2 == 0
    data_cols = len(data_input[0][0])
    assert data_cols % 2 == 0
    data_depth = len(data_input[0][0][0])

    test_output = {}

    for test in range(len(data_input)):
        test_output[test] = {}

        assert len(data_input[test]) == data_rows, "test with incorrect number of rows"
        for ro, ri in enumerate(range(0, data_rows, 2)):
            test_output[test][ro] = {}

            assert len(data_input[test][ri]) == data_cols, "test with incorrect number of cols"
            for co, ci in enumerate(range(0, data_cols, 2)):
                test_output[test][ro][co] = {}

                assert len(data_input[test][ri][ci]) == data_depth, "test with incorrect data width"
                for d in range(data_depth):
                    # Perfrom Pooling
                    acc = 0
                    acc = max(acc, data_input[test][ri    ][ci    ][d])
                    acc = max(acc, data_input[test][ri    ][ci + 1][d])
                    acc = max(acc, data_input[test][ri + 1][ci    ][d])
                    acc = max(acc, data_input[test][ri + 1][ci + 1][d])

                    test_output[test][ro][co][d] = acc

    return test_output


def generate_testbrench_file(input_data, output_data, num_lanes):
    with open(".\\verifying\\testbench.vhd", "w") as f:

        assert len(input_data) == num_lanes
        assert len(output_data) == num_lanes

        f.write("library ieee;\n")
        f.write("use ieee.std_logic_1164.all;\n")
        f.write("\n")

        f.write("entity testbench is\n")
        f.write("\n")
        f.write("end entity;\n")
        f.write("\n")

        f.write("architecture arch of testbench is\n")

        f.write("\tsignal 	clock : std_logic := '0';\n")
        f.write("\tsignal	kickoff : std_logic := '0';\n")
        f.write("\tsignal	running : std_logic;\n")
        f.write("\n")

        for lane in range(num_lanes):
            f.write("\tsignal	LANE_%i_GET_FIFO_0_data : std_logic_vector(0 downto 0);\n"%(lane, ) )
            f.write("\tsignal	LANE_%i_GET_FIFO_0_adv  : std_logic;\n"%(lane, ) )
            f.write("\n")

            f.write("\tsignal	LANE_%i_PUT_FIFO_0_data  : std_logic_vector(0 downto 0);\n"%(lane, ) )
            f.write("\tsignal	LANE_%i_PUT_FIFO_0_write : std_logic;\n"%(lane, ) )
            f.write("\n")

        f.write("begin\n")
        f.write("\tUUT : entity work.test_FPE_inst(arch)\n")
        f.write("\t\tport map (\n")
        for lane in range(num_lanes):
            f.write("\t\t\tLANE_%i_GET_FIFO_0_data => LANE_%i_GET_FIFO_0_data,\n"%(lane, lane, ) )
            f.write("\t\t\tLANE_%i_GET_FIFO_0_adv  => LANE_%i_GET_FIFO_0_adv,\n" %(lane, lane, ) )
            f.write("\t\t\tLANE_%i_PUT_FIFO_0_data  => LANE_%i_PUT_FIFO_0_data,\n" %(lane, lane,) )
            f.write("\t\t\tLANE_%i_PUT_FIFO_0_write => LANE_%i_PUT_FIFO_0_write,\n"%(lane, lane,) )
        f.write("\t\t\tclock => clock,\n")
        f.write("\t\t\tkickoff => kickoff,\n")
        f.write("\t\t\trunning => running\n")
        f.write("\t\t);\n")
        f.write("\n")

        f.write("\tclock_gen : process\n")
        f.write("\tbegin\n")
        f.write("\t\tloop\n")
        f.write("\t\t\tclock <= not clock;\n")
        f.write("\t\t\twait for 50 ns;\n")
        f.write("\t\tend loop;\n")
        f.write("\tend process;\n")
        f.write("\n")

        f.write("\tKickoff_gen : process\n")
        f.write("\tbegin\n")
        f.write("\t\tkickoff <= '0';\n")
        f.write("\t\twait for 1000 ns;\n")

        f.write("\t\tfor k in 0 to %i loop\n"%(len(input_data[0]) - 1))
        f.write("\t\t\twait until rising_edge(clock);\n")
        f.write("\t\t\tkickoff <= '1';\n")
        f.write("\t\t\twait until running = '1';\n")
        f.write("\t\t\twait until rising_edge(clock);\n")
        f.write("\t\t\tkickoff <= '0';\n")
        f.write("\t\t\twait until running = '0';\n")
        f.write("\t\tend loop;\n")
        f.write("\t\twait;\n")
        f.write("\tend process;\n")
        f.write("\n")

        for lane in range(num_lanes):
            f.write("\tspoff_LANE_%i_GET_FIFO_0 : process\n"%(lane, ))
            f.write("\t\tvariable  data_index : integer := 0;\n")
            f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                    len(input_data[lane]) * len(input_data[lane][0]) * len(input_data[lane][0][0]) * len(input_data[lane][0][0][0]) - 1,
                )
            )
            f.write("\t\tconstant test_data : data_array :=\n")
            f.write("\t\t(\n\t\t\t")
            for t in sorted(input_data[lane].keys()):
                for r in sorted(input_data[lane][t].keys()):
                    for c in sorted(input_data[lane][t][r].keys()):
                        for d in sorted(input_data[lane][t][r][c].keys()):
                            f.write("\"%i\","%(input_data[lane][t][r][c][d], ) )
                        f.write("\t")
                    f.write("\n\t\t\t")
                f.write("\n\t\t\t")
            f.seek(f.tell() - 12) # - 12: 2 \n, 2 \r (added as part of \n), 7 \t, 1 ","
            f.write("\n\t\t);\n")

            f.write("\tbegin\n")
            f.write("\t\t-- Flag existance for log checking\n")
            f.write("\t\treport \"LANE_%i_GET_FIFO_0: Exists\" severity note;\n"%(lane, ) )
            f.write("\n")

            f.write("\t\twait until running = '1';\n")
            f.write("\n")

            f.write("\t\t-- Happen expected input\n")
            f.write("\t\twhile 0 <= data_index and data_index < test_data'Length loop\n")
            f.write("\t\t\tLANE_%i_GET_FIFO_0_data <= test_data(data_index);\n"%(lane, ) )
            f.write("\t\t\twait until rising_edge(clock);\n")
            f.write("\t\t\tif LANE_%i_GET_FIFO_0_adv = '1' then\n"%(lane, ))
            f.write("\t\t\t\t-- Advance to input index\n")
            f.write("\t\t\t\tdata_index := data_index + 1;\n")
            f.write("\t\t\tend if;\n")
            f.write("\t\tend loop;\n")
            f.write("\n")

            f.write("\t\t-- Flag all expected input taken\n")
            f.write("\t\treport \"LANE_%i_GET_FIFO_0: All expected input taken\" severity note;\n"%(lane, ))
            f.write("\n")

            f.write("\t\t-- Check for unexpected input\n")
            f.write("\t\tloop\n")
            f.write("\t\t\twait until rising_edge(clock) and LANE_%i_GET_FIFO_0_adv = '1';\n"%(lane, ))
            f.write("\t\t\treport \"LANE_%i_GET_FIFO_0: Trying to take extra input\" severity error;\n"%(lane, ))
            f.write("\t\tend loop;\n")

            f.write("\tend process;\n")
            f.write("\n")

            f.write("\tspoff_LANE_%i_PUT_FIFO_0 : process\n"%(lane, ))
            f.write("\t\tvariable  data_index : integer := 0;\n")
            f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                    len(output_data[lane]) * len(output_data[lane][0]) * len(output_data[lane][0][0]) * len(output_data[lane][0][0][0]) - 1,
                )
            )
            f.write("\t\tconstant test_data : data_array :=\n")
            f.write("\t\t(\n\t\t\t")
            for t in sorted(output_data[lane].keys()):
                for r in sorted(output_data[lane][t].keys()):
                    for c in sorted(output_data[lane][t][r].keys()):
                        for d in sorted(output_data[lane][t][r][c].keys()):
                            f.write("\"%i\","%(output_data[lane][t][r][c][d], ) )
                        f.write("\t")
                    f.write("\n\t\t\t")
                f.write("\n\t\t\t")
            f.seek(f.tell() - 12) # - 10: 2 \n, 2 \r (added as part of \n), 7 \t, 1 ","
            f.write("\n\t\t);\n")

            f.write("\tbegin\n")
            f.write("\t\t-- Flag existance for log checking\n")
            f.write("\t\treport \"LANE_%i_PUT_FIFO_0: Exists\" severity note;\n"%(lane, ))
            f.write("\n")

            f.write("\t\twait until running = '1';\n")
            f.write("\n")

            f.write("\t\t-- Handle expected output\n")
            f.write("\t\twhile 0 <= data_index and data_index < test_data'Length loop\n")
            f.write("\t\t\twait until rising_edge(clock) and LANE_%i_PUT_FIFO_0_write = '1';\n"%(lane, ))
            f.write("\t\t\t-- Check the data is correct\n")
            f.write("\t\t\tassert(LANE_%i_PUT_FIFO_0_data = test_data(data_index))\n"%(lane, ))
            f.write("\t\t\t\treport \"LANE_%i_PUT_FIFO_0: Incorrect \" & integer'Image(data_index) & \" th output\"\n"%(lane, ))
            f.write("\t\t\t\tseverity error;\n")
            f.write("\t\t\tassert(LANE_%i_PUT_FIFO_0_data /= test_data(data_index))\n"%(lane, ))
            f.write("\t\t\t\treport \"LANE_%i_PUT_FIFO_0: Correct \" & integer'Image(data_index) & \" th output\"\n"%(lane, ))
            f.write("\t\t\t\tseverity note;\n")
            f.write("\n")

            f.write("\t\t\t-- Advance to output index\n")
            f.write("\t\t\tdata_index := data_index + 1;\n")
            f.write("\t\tend loop;\n")
            f.write("\n")

            f.write("\t\t-- Flag all expected output given\n")
            f.write("\t\treport \"LANE_%i_PUT_FIFO_0: All expected output received\" severity note;\n"%(lane, ))
            f.write("\n")

            f.write("\t\t-- Check for unexpected output\n")
            f.write("\t\tloop\n")
            f.write("\t\t\twait until rising_edge(clock) and LANE_%i_PUT_FIFO_0_write = '1';\n"%(lane, ))
            f.write("\t\t\treport \"LANE_%i_PUT_FIFO_0: Extra output\" severity error;\n"%(lane, ))
            f.write("\t\tend loop;\n")

            f.write("\tend process;\n")
            f.write("\n")


        f.write("end architecture;\n")


def test_layer(data_rows, data_cols, data_depth, num_lanes, number_tests, test_time):

    # Generate program files
    generate_layer.generate_layer(".\\verifying", "varifying", data_rows, data_cols, data_depth, num_lanes, use_BRAMs=False, pregened_memfiles={} )

    # # Generate testbench
    test_input = []
    test_output = []
    for lane in range(num_lanes):
        test_input.append(generate_data_input(number_tests, data_rows, data_cols, data_depth))
        test_output.append(generate_data_output(test_input[-1]))

    generate_testbrench_file(test_input, test_output, num_lanes)

    # Run test
    test_name = "verifying_%s"%(__file__.split("\\")[-2], )

    tests_utils.run_sweep_leaf(".\\verifying", test_name,
        program_file="varifying_program.fpea",
        generics_file="varifying_generics.json",
        parameters_file="varifying_parameters.json",
        time=test_time
    )

if __name__ == "__main__":
    # Make sure verifying folder exists
    try:
        os.makedirs(".\\verifying")
    except FileExistsError:
        pass

    data_rows = 6
    data_cols = 4
    data_depth = 8
    number_tests = 8
    test_time = "5ms"

    test_layer(data_rows, data_cols, data_depth, 1, number_tests, test_time)
