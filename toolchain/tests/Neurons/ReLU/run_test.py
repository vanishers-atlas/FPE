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

def run_test(test_program = "test_program.fpea", temp_files_dir = "temp_files", part = "xc7k160tiffv676-2L", run_tcl = True, path="."):
    if not os.path.exists(temp_files_dir):
        os.mkdir(temp_files_dir)

    # Run toolchain for test
    print("\nRunning Config Extractor")
    extractor.extract_config(path + "\\%s"%(test_program), path + "\\test_parameters.json", path + "\\%s\\generated_config.json"%(temp_files_dir))

    print("\nRunning RTL Generator")
    generator.generate("FPE.sFPE", "sFPE", path + "\\%s\\generated_config.json"%(temp_files_dir), path + "\\%s\\"%(temp_files_dir), append_hash=False)

    print("\nRunning Assembler")
    assembler.run(path + "\\%s"%(test_program), path + "\\%s\\generated_config.json"%(temp_files_dir), path + "\\%s\\sFPE.inter"%(temp_files_dir), path + "\\test_generics.json", "sFPE", path + "\\%s\\"%(temp_files_dir))

    if run_tcl:
        # Read all vhdl files
        vhdl_files = [f for f in os.listdir(path + "\\%s\\"%(temp_files_dir)) if f.endswith(".vhd") ]

        # Run vivado synthesis script
        print("\nPreparing Vivado Sript")
        with open(path + "\\%s\\run_test.tcl"%(temp_files_dir), "w") as f:
            # Create project
            f.write("create_project testing %s/%s -force -part %s;\n"%(path, temp_files_dir, part))

            # Load like vhdl files
            f.write("".join(["read_vhdl -library work %s/%s/%s;\n"%(path, temp_files_dir, vhdl_file) for vhdl_file in vhdl_files]))
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
                "-source" , path + "\\%s\\run_test.tcl"%(temp_files_dir),
                "-journal", path + "\\%s\\test.jou"%(temp_files_dir),
                "-log"    , path + "\\%s\\test.log"%(temp_files_dir),
                "-tempDir", path + "\\%s"%(temp_files_dir)
            ]
        )
        print("Vivado Script Finished")

        with open(path + "\\%s\\test.log"%(temp_files_dir), "r") as f:
            for lineNum, line in enumerate(f.readlines()):
                if line.startswith("Error: "):
                    print("Vivado Script error on line %i"%lineNum)
                    print(line)
                    return -1

    return 0

if __name__ == "__main__":
    exit(run_test(test_program="relu_activation.fpea", part="xc7z020-1clg400"))
