# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 6
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import os
from FPE.toolchain.tests import utils

def run_test(path="."):
    output_dir = path + "\\toolchain_files"
    processor = "test_FPE"
    generate_name = False
    force_generation = True

    # Run toolchain for test
    utils.run_toolchain(
        path + "\\test_program.fpea",
        path + "\\test_parameters.json",
        path + "\\test_generics.json",
        output_dir, processor, generate_name, force_generation
    )

    exit()
    
    # Symulate testbench
    vhdl_files = [
        output_dir + "\\" + file
        for file in os.listdir(output_dir)
        if file.endswith(".vhd")
    ]
    vhdl_files.append(path + "\\testbench.vhd")
    simulation_dir = path + "\\simulation_files"
    part = "xc7k160tiffv676-2L"

    return utils.run_simulation(
        vhdl_files,
        simulation_dir,
        part
    )

if __name__ == "__main__":
    exit(run_test())
