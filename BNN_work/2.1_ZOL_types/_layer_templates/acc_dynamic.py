# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import os
import math

from FPE.toolchain import utils as tc_utils

from FPE.BNN_work import _utils as BNN_utils
from FPE.toolchain.tests import utils as test_utils

def realise_template(output_path, output_name, input_neurons, output_neurons, use_BRAMs, rom_mif=None):
    assert type(output_path) == str
    assert type(output_name) == str

    assert type(input_neurons) == int and math.log(input_neurons,2) % 1 == 0, "input_neurons must be a power of 2"
    assert type(output_neurons) == int and output_neurons > 1, "output_neurons must be a postive int"

    assert type(use_BRAMs) == bool
    assert rom_mif == None or type(rom_mif) == str

    popcount_width = tc_utils.unsigned.width(input_neurons)

    path_preface = "\\".join(__file__.split("\\")[:-1])
    BNN_utils.realise_template(
        output_path,
        output_name,
        path_preface + "\\acc_dynamic",
        {
            "INPUT_NEURONS" : input_neurons,
            "OUTPUT_NEURONS" : output_neurons,
            "POPCOUNT_WIDTH" : popcount_width,
            "ROM_TYPE" : "BLOCK" if use_BRAMs else "DIST",
            "RAM_TYPE" : "BLOCK" if use_BRAMs else "DIST",
            "ROM_MIF" : rom_mif if rom_mif else ".\\blankmem_1x%i.mem"%(input_neurons * (output_neurons + 2), )
        }
    )

    return (popcount_width, output_neurons, )

# When runing as script verity layer
if __name__ == '__main__':
    output_path = ".\\acc_dynamic"
    output_name = "acc_test"
    # Make sure pooling folder exists
    try:
        os.makedirs(output_path)
    except FileExistsError:
        pass

    number_tests, input_neurons, output_neurons = 12, 16, 8

    # Create FPEA, parameter, and generics files
    rom_file = "ROM.mif"
    realise_template(output_path, output_name, input_neurons, output_neurons, use_BRAMs=False, rom_mif = "..\\" + rom_file)

    # Generate test data
    test_input = BNN_utils.generate_1d_data(number_tests, input_neurons)
    parameters = BNN_utils.generate_parameters(output_neurons, input_neurons)
    test_output = BNN_utils.acc_outputs(number_tests, input_neurons, test_input, output_neurons, parameters)

    # Write ROM file+
    rom_width = 1
    with open(output_path + "\\" + rom_file, "w") as f:
        for o in range(output_neurons):
            for i in range(input_neurons):
                f.write(tc_utils.unsigned.encode(parameters[o]["weights"][i], rom_width))
                f.write("\n")


    # Write the toolbench file
    popcount_width = tc_utils.unsigned.width(input_neurons)
    with open(output_path + "\\testbench.vhd", "w") as f:
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

        f.write("\tsignal	GET_FIFO_0_data : std_logic_vector(0 downto 0);\n")
        f.write("\tsignal	GET_FIFO_0_adv  : std_logic;\n")
        f.write("\n")

        f.write("\tsignal	PUT_FIFO_0_data  : std_logic_vector(%i downto 0);\n"%(popcount_width - 1, ))
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

        f.write("\t\tfor k in 0 to %i loop\n"%(number_tests - 1))
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
        f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                number_tests * input_neurons - 1
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n")
        f.write(BNN_utils.format_1d_data(number_tests, input_neurons, test_input, line_start="\t\t\t", encode_width=1))
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
                number_tests * output_neurons - 1,
                popcount_width - 1,
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n")
        f.write(BNN_utils.format_1d_data(number_tests, output_neurons, test_output, line_start="\t\t\t", encode_width=popcount_width))
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

    # Run test
    test_name = "verifying_%s"%(__file__.split("\\")[-2], )

    test_utils.run_sweep_leaf(output_path, test_name,
        program_file=output_name + ".fpea",
        generics_file=output_name + "_generics.json",
        parameters_file=output_name + "_parameters.json",
        time="800us"
    )
