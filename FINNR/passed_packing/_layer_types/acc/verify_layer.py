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


def generate_parameters(input_neurons, output_neurons):
    parameters = {}
    for output in range(output_neurons):
        parameters[output] = {}

        # compute weights
        parameters[output]["weights"] = {}
        rand_weight = random.randrange(2**input_neurons)
        for i in range(input_neurons):
            # bit i th bit of input value is 0
            if math.floor(rand_weight / 2**i) % 2 == 0:
                parameters[output]["weights"][i] = 0
            else:
                parameters[output]["weights"][i] = 1

    return parameters

def generate_data_input(number_tests, input_neurons):
    tests = {}

    for test in range(number_tests):
        tests[test] = {}

        input_value = random.randrange(2**input_neurons)
        for i in range(input_neurons):
            # bit i th bit of input value is 0
            if math.floor(input_value / 2**i) % 2 == 0:
                tests[test][i] = 0
            else:
                tests[test][i] = 1
    return tests

def generate_data_output(data_input, parameters):
    input_neurons = len(data_input[0])
    output_neurons = len(parameters)

    test_output = {}

    for test in range(len(data_input)):
        assert len(data_input[test]) == input_neurons, "test with incorrect input_neurons"

        test_output[test] = {}

        for output in range(output_neurons):
            assert len(parameters[output]["weights"]) == input_neurons, "output with incorrect number of weights"

            # Perform MAC step
            acc = 0
            for input in range(input_neurons):
                xnor = 1 if data_input[test][input] == parameters[output]["weights"][input] else 0
                acc += xnor

            test_output[test][output] = acc

    return test_output


def packer(data, packing):
    assert len(data) % packing == 0
    sorted_keys = sorted(data.keys())
    for i in range(0, len(data), packing):
        acc = ""
        for j in range(packing):
            key = sorted_keys[i + j]
            acc += str(data[key])
        yield acc

def generate_testbrench_file(input_data, output_data, input_packing):
    popcount_width = tc_utils.unsigned.width(len(input_data[0]))

    with open(".\\verifying\\testbench.vhd", "w") as f:
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

        f.write("\tsignal	GET_FIFO_0_data : std_logic_vector(%i downto 0);\n"%(
                input_packing - 1,
            )
        )
        f.write("\tsignal	GET_FIFO_0_adv  : std_logic;\n")
        f.write("\n")

        f.write("\tsignal	PUT_FIFO_0_data  : std_logic_vector(%i downto 0);\n"%(
                popcount_width - 1,
            )
        )
        f.write("\tsignal	PUT_FIFO_0_write : std_logic;\n")
        f.write("\n")

        f.write("begin\n")
        f.write("\tUUT : entity work.test_FPE_inst(arch)\n")
        f.write("\t\tport map (\n")
        f.write("\t\t\tGET_FIFO_0_data => GET_FIFO_0_data,\n")
        f.write("\t\t\tGET_FIFO_0_adv  => GET_FIFO_0_adv,\n")
        f.write("\t\t\tPUT_FIFO_0_data  => PUT_FIFO_0_data,\n")
        f.write("\t\t\tPUT_FIFO_0_write => PUT_FIFO_0_write,\n")
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

        f.write("\t\tfor k in 0 to %i loop\n"%(len(input_data) - 1))
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

        f.write("\tspoff_GET_FIFO_0 : process\n")
        f.write("\t\tvariable  data_index : integer := 0;\n")
        f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(%i downto 0);\n"%(
                (len(input_data) * len(input_data[0]) / input_packing) - 1,
                input_packing - 1,
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n\t\t\t")
        for test in sorted(input_data.keys()):
            for word in packer(input_data[test], input_packing):
                f.write("\"%s\", "%(word, ) )
            f.write("\n\t\t\t")
        f.seek(f.tell() - 7) # - 6: 1 \n, 1 \r (added as part of \n), 3 \t, 1 ",", 1 " "
        f.write("\n\t\t);\n")

        f.write("\tbegin\n")
        f.write("\t\t-- Flag existance for log checking\n")
        f.write("\t\treport \"GET_FIFO_0: Exists\" severity note;\n")
        f.write("\n")

        f.write("\t\twait until running = '1';\n")
        f.write("\n")

        f.write("\t\t-- Happen expected input\n")
        f.write("\t\twhile 0 <= data_index and data_index < test_data'Length loop\n")
        f.write("\t\t\tGET_FIFO_0_data <= test_data(data_index);\n")
        f.write("\t\t\twait until rising_edge(clock);\n")
        f.write("\t\t\tif GET_FIFO_0_adv = '1' then\n")
        f.write("\t\t\t\t-- Advance to input index\n")
        f.write("\t\t\t\tdata_index := data_index + 1;\n")
        f.write("\t\t\tend if;\n")
        f.write("\t\tend loop;\n")
        f.write("\n")

        f.write("\t\t-- Flag all expected input taken\n")
        f.write("\t\treport \"GET_FIFO_0: All expected input taken\" severity note;\n")
        f.write("\n")

        f.write("\t\t-- Check for unexpected input\n")
        f.write("\t\tloop\n")
        f.write("\t\t\twait until rising_edge(clock) and GET_FIFO_0_adv = '1';\n")
        f.write("\t\t\treport \"GET_FIFO_0: Trying to take extra input\" severity error;\n")
        f.write("\t\tend loop;\n")

        f.write("\tend process;\n")
        f.write("\n")

        f.write("\tspoff_PUT_FIFO_0 : process\n")
        f.write("\t\tvariable  data_index : integer := 0;\n")
        f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(%i downto 0);\n"%(
                len(output_data) * len(output_data[0]) - 1,
                popcount_width - 1,
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n\t\t\t")
        for t in sorted(output_data.keys()):
            for o in sorted(output_data[t].keys()):
                f.write("\"%s\", "%(tc_utils.unsigned.encode(output_data[t][o], popcount_width), ) )
            f.write("\n\t\t\t")
        f.seek(f.tell() - 7) # - 6: 1 \n, 1 \r (added as part of \n), 3 \t, 1 ",", 1 " "
        f.write("\n\t\t);\n")

        f.write("\tbegin\n")
        f.write("\t\t-- Flag existance for log checking\n")
        f.write("\t\treport \"PUT_FIFO_0: Exists\" severity note;\n")
        f.write("\n")

        f.write("\t\twait until running = '1';\n")
        f.write("\n")

        f.write("\t\t-- Handle expected output\n")
        f.write("\t\twhile 0 <= data_index and data_index < test_data'Length loop\n")
        f.write("\t\t\twait until rising_edge(clock) and PUT_FIFO_0_write = '1';\n")
        f.write("\t\t\t-- Check the data is correct\n")
        f.write("\t\t\tassert(PUT_FIFO_0_data = test_data(data_index))\n")
        f.write("\t\t\t\treport \"PUT_FIFO_0: Incorrect \" & integer'Image(data_index) & \" th output\"\n")
        f.write("\t\t\t\tseverity error;\n")
        f.write("\t\t\tassert(PUT_FIFO_0_data /= test_data(data_index))\n")
        f.write("\t\t\t\treport \"PUT_FIFO_0: Correct \" & integer'Image(data_index) & \" th output\"\n")
        f.write("\t\t\t\tseverity note;\n")
        f.write("\n")

        f.write("\t\t\t-- Advance to output index\n")
        f.write("\t\t\tdata_index := data_index + 1;\n")
        f.write("\t\tend loop;\n")
        f.write("\n")

        f.write("\t\t-- Flag all expected output given\n")
        f.write("\t\treport \"PUT_FIFO_0: All expected output received\" severity note;\n")
        f.write("\n")

        f.write("\t\t-- Check for unexpected output\n")
        f.write("\t\tloop\n")
        f.write("\t\t\twait until rising_edge(clock) and PUT_FIFO_0_write = '1';\n")
        f.write("\t\t\treport \"PUT_FIFO_0: Extra output\" severity error;\n")
        f.write("\t\tend loop;\n")

        f.write("\tend process;\n")
        f.write("\n")


        f.write("end architecture;\n")


def test_layer(input_neurons, output_neurons, input_packing, number_tests, test_time):
    # Generate parameters
    parameters = generate_parameters(input_neurons, output_neurons)

    # Generate ROMs
    rom_A = []
    for output in range(output_neurons):
        # Add weights for this output neuron
        for weight in range(input_neurons):
            if weight % input_packing == 0:
                acc = parameters[output]["weights"][weight]
            else:
                acc *= 2
                acc += parameters[output]["weights"][weight]
                if (weight + 1) % input_packing == 0:
                    rom_A.append(acc)


    with open(".\\verifying\\varifying_ROM_A.mem", "w") as f:
        for value in rom_A:
            f.write(tc_utils.unsigned.encode(value, 1))
            f.write("\n")

    # Generate program files
    generate_layer.generate_layer(".\\verifying", "varifying", input_neurons, output_neurons, input_packing, use_BRAMs=False, pregened_memfiles=["ROM_A"] )

    # Generate testbench
    test_input = generate_data_input(number_tests, input_neurons)
    test_output = generate_data_output(test_input, parameters)

    generate_testbrench_file(test_input, test_output, input_packing)

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

    input_neurons = 32
    output_neurons = 16
    number_tests = 8
    test_time = "5ms"


    print("verifying input_packing factor = input_neurons")
    test_layer(input_neurons, output_neurons, input_neurons, number_tests, test_time)
    print()

    print("verifying input_packing factor = factor of input_neurons")
    test_layer(input_neurons, output_neurons, int(input_neurons/4), number_tests, test_time)
    print()
