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

def realise_template(output_path, output_name, data_rows, data_cols, data_depth, num_kernals, use_BRAMs, romA_mif=None, romB_mif=None):
    assert type(output_path) == str
    assert type(output_name) == str

    assert type(data_rows) == int and data_rows > 1, "data_rows must be a postive int"
    assert type(data_cols) == int and data_cols > 1, "data_cols must be a postive int"
    assert type(data_depth) == int and data_depth > 1, "data_depth must be a postive int"
    assert type(num_kernals) == int and num_kernals > 1, "num_kernals must be a postive int"

    assert type(use_BRAMs) == bool
    assert romA_mif == None or type(romA_mif) == str
    assert romB_mif == None or type(romB_mif) == str

    RAM_depth = 2 ** math.ceil(math.log((3 * (1 + data_cols) * data_depth), 2))
    popcount_width = tc_utils.unsigned.width(3 * 3 * data_depth)
    ROM_depth = num_kernals * (9 * data_depth + 2)

    path_preface = "\\".join(__file__.split("\\")[:-1])
    BNN_utils.realise_template(
        output_path,
        output_name,
        path_preface + "\\conv_counter",
        {
            "DATA_ROWS" : data_rows,
            "DATA_COLS" : data_cols,
            "DATA_DEPTH" : data_depth,
            "NUM_KERNALS" : num_kernals,
            "RAM_DEPTH" : RAM_depth,
            "ROMA_DEPTH" : ROM_depth,
            "ROMB_DEPTH" : num_kernals,
            "POPCOUNT_WIDTH" : popcount_width,
            "ROM_TYPE" : "BLOCK" if use_BRAMs else "DIST",
            "RAM_TYPE" : "BLOCK" if use_BRAMs else "DIST",
            "ROMA_MIF" : romA_mif if romA_mif else ".\\blankmem_1x%i.mem"%(ROM_depth, ),
            "ROMB_MIF" : romB_mif if romB_mif else ".\\blankmem_1x%i.mem"%(num_kernals, )
        }
    )

    return (data_rows, data_cols, num_kernals,)

# When runing as script verity layer
if __name__ == '__main__':
    output_path = ".\\conv_counter"
    output_name = "conv_test"
    # Make sure pooling folder exists
    try:
        os.makedirs(output_path)
    except FileExistsError:
        pass

    number_tests, data_rows, data_cols, data_depth, num_kernals = 5, 8, 4, 6, 9

    # Create FPEA, parameter, and generics files
    romA_file = "ROMA.mif"
    romB_file = "ROMB.mif"
    realise_template(output_path, output_name, data_rows, data_cols, data_depth, num_kernals, use_BRAMs=False, romA_mif = "..\\" + romA_file, romB_mif = "..\\" + romB_file)

    # Generate test data
    test_input = BNN_utils.generate_2d_data(number_tests, data_rows, data_cols, data_depth)
    kernals = BNN_utils.generate_kernals(num_kernals, data_depth)
    test_output = BNN_utils.conv_outputs(number_tests, data_rows, data_cols, data_depth, test_input, num_kernals, kernals)

    # Write ROM file+
    with open(output_path + "\\" + romA_file, "w") as f:
        for k in range(num_kernals):
            for x in [-1, 0, 1]:
                for d in range(data_depth):
                    for y in [-1, 0, 1]:
                        f.write(tc_utils.unsigned.encode(kernals[k]["weights"][x][y][d], 1))
                        f.write("\n")
            f.write(tc_utils.unsigned.encode(kernals[k]["gamma"], 1))
            f.write("\n")

    rom_width = tc_utils.unsigned.width(3 * 3 * data_depth)
    with open(output_path + "\\" + romB_file, "w") as f:
        for k in range(num_kernals):
            f.write(tc_utils.unsigned.encode(kernals[k]["threashold"], rom_width))
            f.write("\n")


    # Write the toolbench file
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

        f.write("\tsignal	PUT_FIFO_0_data  : std_logic_vector(0 downto 0);\n")
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
                number_tests * data_rows * data_cols * data_depth - 1,
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n")
        f.write(BNN_utils.format_2d_data(number_tests, data_rows, data_cols, data_depth, test_input, line_start="\t\t\t", encode_width=1))
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
        f.write("\t\ttype  data_array is array (0 to %i) of std_logic_vector(0 downto 0);\n"%(
                number_tests * data_rows * data_cols * num_kernals - 1,
            )
        )
        f.write("\t\tconstant test_data : data_array :=\n")
        f.write("\t\t(\n")
        f.write(BNN_utils.format_2d_data(number_tests, data_rows, data_cols, num_kernals, test_output, line_start="\t\t\t", encode_width=1))
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
        time="25ms"
    )
