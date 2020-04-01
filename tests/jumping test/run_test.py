import os
import sys
import subprocess

part = "xc7k160tiffv676-2L"
run_tcl = True 

# Add FPE to PYTHONPATH
sys.path.append("\\".join(os.getcwd().split("\\")[:-3]))

# import FPE toolchain
from FPE.toolchain.config_extractor   import config_extractor as extractor
from FPE.toolchain.HDL_generation     import HDL_generator    as generator
from FPE.toolchain.assembler          import assembler

# Run toolchain for test
print("\nRunning Config Extractor")
extractor.extract_config("test_program.fpea", "test_parameters.json", "temp_files\\generated_config.json")

print("\nRunning RTL Generator")
generator.generate("FPE.sFPE", "sFPE", "temp_files\\generated_config.json", "temp_files\\", append_hash=False)

print("\nRunning Aassembler")
assembler.run("test_program.fpea", "temp_files\\generated_config.json", "temp_files\\sFPE.inter", "test_generics.json", "sFPE", "temp_files\\")

if run_tcl:
    # Read all vhdl files
    vhdl_files = [f for f in os.listdir(".\\temp_files\\") if f.endswith(".vhd") ]

    # Run vivado synthesis script
    print("\nPreparing Vivado Sript")
    with open("temp_files\\run_test.tcl", "w") as f:
        # Create project
        f.write("create_project testing ./temp_files -force -part %s;\n"%(part))

        # Load like vhdl files
        f.write("".join(["read_vhdl -library work ./temp_files/%s;\n"%(vhdl_file) for vhdl_file in vhdl_files]))
        f.write("read_vhdl -library work ./testbench.vhd;\n")

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
        f.write("report_utilization -file utilization.rpt;\n")
        f.write("report_timing -file timing.rpt;\n")

    print("Running Vivado")
    result = subprocess.run(
        [   "vivado.bat",
            "-mode"   , "batch",
            "-source" , "temp_files\\run_test.tcl",
            "-journal", "temp_files\\test.jou",
            "-log"    , "temp_files\\test.log",
            "-tempDir", "temp_files"
        ],
        stderr = subprocess.PIPE
    )
    if len(result.stderr) != 0:
        print("Vivado Script Failure")
        print(result.stderr.decode("utf-8"))
        exit(-1)
    print("Vivado Script Finished")


exit(0)
