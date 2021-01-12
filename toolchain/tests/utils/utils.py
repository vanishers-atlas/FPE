# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import subprocess
import os

# import FPE toolchain
from FPE.toolchain.config_extractor   import config_extractor as extractor
from FPE.toolchain.HDL_generation     import HDL_generator    as generator
from FPE.toolchain.assembler          import assembler

def run_toolchain(program, parameters, generics, output_dir, processor, generate_name, force_generation):
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
        "processor.sFPE",
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

    print("\nToolchain finished")

def run_simulation(files, simulate_dir, part, design_top, sim_top, time):
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
        for file in files:
            f.write( "read_vhdl -library work %s;\n"%(file.replace("\\", "/"), ) )

        # Set tops for design and sim modes.
        f.write("set_property top %s [current_fileset];\n"%(design_top, ) )
        f.write("set_property top %s [current_fileset -simset];\n"%(sim_top, ) )

        # Run simulation
        f.write("launch_simulation -simset [current_fileset -simset];\n")
        f.write("run %s;\n"%(time,))
        f.write("close_sim -force;\n")

    print("\nRunning Vivado")
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

    # Check for error found by vivaso
    print("\nChecking Vivado Output")
    with open(log, "r") as f:
        for lineNum, line in enumerate(f.readlines()):
            if line.lower().startswith("error: "):
                print("Vivado Script error on line %i"%lineNum)
                print(line)
                return 1
    print("No Vivado Errors Found")
    return 0

def run_sweep_leaf(path, test_name, processor="test_FPE", part="xc7k160tiffv676-2L", sim_top="testbench", time="100us"):

    print("#####################################################")
    print("Running %s test"%(test_name, ) )
    print("#####################################################\n")

    output_dir = path + "\\toolchain_files"

    # Run toolchain for test
    run_toolchain(
        path + "\\test_program.fpea",
        path + "\\test_parameters.json",
        path + "\\test_generics.json",
        output_dir, processor, False, True
    )

    # Symulate testbench
    vhdl_files = [
        output_dir + "\\" + file
        for file in os.listdir(output_dir)
        if file.endswith(".vhd")
    ]
    vhdl_files.append(path + "\\testbench.vhd")
    result = run_simulation(
        vhdl_files,
        path + "\\simulation_files",
        part,
        processor + "_inst",
        sim_top,
        time
    )

    if result != 0:
        raise ValueError("%s test FAILED, result %i"%(test_name, result) )

    print("\n#####################################################")
    print("%s test PASSED"%(test_name, ) )
    print("#####################################################\n")
    return 0

def run_sweep_branch(branch_name, path, test_sets):

    print("#####################################################")
    print("Sweeping %s test set"%(branch_name, ) )
    print("#####################################################\n")

    for test_set in test_sets:
        print(test_set)
        test_set_name = test_set.__file__.split("\\")[-2]

        result = test_set.run_sweep(path="%s//%s" % (path, test_set_name))

        if result != 0:
            raise ValueError("%s test FAILED, result %i"%(test_set_name, result) )

    print("\n#####################################################")
    print("%s test set PASSED"%(branch_name, ) )
    print("#####################################################\n")

    return 0
