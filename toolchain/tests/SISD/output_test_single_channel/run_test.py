import subprocess
import os

if __name__ == "__main__":
    import sys
    # Add FPE to PYTHONPATH
    sys.path.append("\\".join(os.getcwd().split("\\")[:-5]))

# import FPE toolchain
from FPE.toolchain.config_extractor   import config_extractor as extractor
from FPE.toolchain.HDL_generation     import HDL_generator    as generator
from FPE.toolchain.assembler          import assembler

def run_test(part = "xc7k160tiffv676-2L", run_tcl = True, path="."):
    # Run toolchain for test
    print("\nRunning Config Extractor")
    extractor.extract_config(path + "\\test_program.fpea", path + "\\test_parameters.json", path + "\\temp_files\\generated_config.json")

    print("\nRunning RTL Generator")
    generator.generate("FPE.sFPE", "sFPE", path + "\\temp_files\\generated_config.json", path + "\\temp_files\\", append_hash=False)

    print("\nRunning Aassembler")
    assembler.run(path + "\\test_program.fpea", path + "\\temp_files\\generated_config.json", path + "\\temp_files\\sFPE.inter", path + "\\test_generics.json", "sFPE", path + "\\temp_files\\")

    if run_tcl:
        # Read all vhdl files
        vhdl_files = [f for f in os.listdir(path + "\\temp_files\\") if f.endswith(".vhd") ]

        # Run vivado synthesis script
        print("\nPreparing Vivado Sript")
        with open(path + "\\temp_files\\run_test.tcl", "w") as f:
            # Create project
            f.write("create_project testing %s/temp_files -force -part %s;\n"%(path, part))

            # Load like vhdl files
            f.write("".join(["read_vhdl -library work %s/temp_files/%s;\n"%(path, vhdl_file) for vhdl_file in vhdl_files]))
            f.write("read_vhdl -library work %s/testbench.vhd;\n"%(path))

            # Set top module
            f.write("set_property top testbench [current_fileset -simset];\n")
            f.write("set_property top sFPE_inst [current_fileset];\n")

            # Run simulation
            f.write("launch_simulation -simset [current_fileset -simset];\n")
            f.write("run 100 us;\n")
            f.write("close_sim -force;\n")

            # Run Synthesis
            f.write("synth_design;\n")

            # Report Timing and Utilization from synthesised design
            f.write("report_utilization -file %s/utilization.rpt;\n"%(path))
            f.write("report_timing -file %s/timing.rpt;\n"%(path))

        print("Running Vivado")
        subprocess.run(
            [   "vivado.bat",
                "-mode"   , "batch",
                "-source" , path + "\\temp_files\\run_test.tcl",
                "-journal", path + "\\temp_files\\test.jou",
                "-log"    , path + "\\temp_files\\test.log",
                "-tempDir", path + "\\temp_files"
            ]
        )
        print("Vivado Script Finished")

        with open(path + "\\temp_files\\test.log", "r") as f:
            for lineNum, line in  enumerate(f.readlines()):
                if line.startswith("Error: "):
                    print("Vivado Script error on line %i"%lineNum)
                    print(line)
                    return -1

    return 0

if __name__ == "__main__":
    exit(run_test())
