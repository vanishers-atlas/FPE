# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    import os
    levels_below_FPE = 3
    sys.path.append("\\".join(os.getcwd().split("\\")[:-levels_below_FPE]))

import subprocess
import os

# import FPE toolchain
from FPE.toolchain.config_extractor   import config_extractor as extractor
from FPE.toolchain.HDL_generation     import HDL_generator    as generator
from FPE.toolchain.assembler          import assembler

def run_toolchain(
    program, parameters, generics,
    output_dir, processor,
    generate_name, force_generation
):
    config = "%s\\%s_config.json"%(output_dir, processor, )

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print("\nRunning Config Extractor")
    extractor.extract_config(
        program,
        parameters,
        config
    )

    print("\nRunning RTL Generator")
    generator.generate(
        "FPE.sFPE",
        processor,
        config,
        output_dir,
        generate_name = generate_name,
        force_generation = force_generation
    )

    print("\nRunning Assembler")
    assembler.run(
        program,
        config,
        "%s\\%s.inter"%(output_dir, processor),
        generics,
        processor,
        output_dir
    )

def run_simulation(files, simulate_dir, part, time="100 us"):
    if not os.path.exists(simulate_dir):
        os.mkdir(simulate_dir)

    # Run vivado synthesis script
    print("\nPreparing Vivado Sript")
    script = "%s\\run_test.tcl"%(simulate_dir)
    # tcl use / ("/") not \ ("\\") filepath seperator within use .replace("\\", "/") of all filepaths in it
    with open(script, "w") as f:
        # Create project
        f.write("create_project testing %s -force -part %s;\n"%(simulate_dir.replace("\\", "/"), part))

        # Load all vhdl files
        f.write("".join([
            "read_vhdl -library work %s;\n"%(file.replace("\\", "/"))
            for file
            in files
        ]))

        # Set top module
        f.write("set_property top testbench [current_fileset -simset];\n")

        # Run simulation
        f.write("launch_simulation -simset [current_fileset -simset];\n")
        f.write("run %s;\n"%(time,))
        f.write("close_sim -force;\n")

    print("Running Vivado")
    journal = "%s\\test.jou"%(simulate_dir)
    log = "%s\\test.log"%(simulate_dir)
    subprocess.run(
        [   "vivado.bat",
            "-mode"   , "batch",
            "-source" , script,
            "-journal", journal,
            "-log"    , log,
            "-tempDir", simulate_dir
        ]
    )
    print("Vivado Script Finished")

    with open(log, "r") as f:
        for lineNum, line in enumerate(f.readlines()):
            if line.startswith("Error: "):
                print("Vivado Script error on line %i"%lineNum)
                print(line)
                return -1

    return 0
