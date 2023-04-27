import subprocess
import json
import os
import re

# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

from FPE.toolchain import utils as tc_utils

from FPE.FINNR import _utils as meas_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils
from FPE.toolchain.HDL_generation  import HDL_generator

from FPE.toolchain.tests.utils  import run_toolchain

import os
import math

def measure_area():
    PART="xc7z020clg400-1"

    # Measure the generated network's area nad timing
    dir_pathway = os.path.dirname(__file__)
    try:
        os.makedirs(dir_pathway + "\\toolchain_files")
    except FileExistsError:
        pass

    run_toolchain(
        program     = dir_pathway + "\\test_program.fpea",
        parameters  = dir_pathway + "\\test_parameters.json",
        generics    = dir_pathway + "\\test_generics.json",
        output_dir  = dir_pathway + "\\toolchain_files",
        processor_name      = "test_FPE",
        concat_naming       = True,
        force_generation    = True
    )

    # Collect all vhdl_files from generated network
    vhdl_files = [
        dir_pathway + "\\" + file
        for file in os.listdir(dir_pathway)
        if file.endswith(".vhd")
    ]
    code_dir = dir_pathway + "\\toolchain_files"
    vhdl_files += [
        code_dir + "\\" + file
        for file in os.listdir(code_dir)
        if file.endswith(".vhd")
    ]

    # Make sure project folder exists
    project_folder = dir_pathway + "\\measuring"

    if not os.path.exists(project_folder):
        os.mkdir(project_folder)

    # Generate vivado synthesis script
    print("\nPreparing Vivado Sript")
    script = "%s\\measure_network.tcl"%(project_folder)
    # tcl use / ("/") not \ ("\\") filepath seperator, within it use .replace("\\", "/") of all filepaths in it
    with open(script, "w") as f:
        # Create project
        f.write("create_project measuring %s -force -part %s;\n"%(project_folder.replace("\\", "/"), PART))
        f.write("\n")

        f.write("set_property target_language VHDL [current_project]\n")
        f.write("\n")


        # Load all vhdl files
        for file in vhdl_files:
            f.write("read_vhdl -library work %s;\n"%(file.replace("\\", "/"), ) )
        f.write("\n")

        #f.write("set_property library work [get_files  %s/toolchain_files/test_FPE_inst.vhd]\n"%(dir_pathway.replace("\\", "/"), ) )
        f.write("set_property top test_FPE_inst [current_fileset]\n\n")

        # Run implemention
        f.write("launch_runs impl_1 -jobs 4\n")
        f.write("wait_on_run impl_1\n")
        f.write("open_run impl_1\n")
        f.write("report_utilization -hierarchical\n")
        f.write("\n")


    # Run vivado synthesis script
    print("\nRunning Vivado")
    journal = "%s\\measuring.jou"%(project_folder)
    log = "%s\\measuring.log"%(project_folder)
    subprocess.run(
        [   "vivado.bat",
            "-mode"   , "batch",
            "-source" , script,
            "-journal", journal,
            "-log"    , log,
            "-tempDir", project_folder
        ]
    )

    # Load log file to extract area and times details
    with open(log, "r") as f:
        lines = f.readlines()

    # Extract Utilization region
    util_start = lines.index("Utilization Design Information\n")
    util_end = lines.index("* Note: The sum of lower-level cells may be larger than their parent cells total, due to cross-hierarchy LUT combining\n")
    util_region = lines[util_start + 9 : util_end - 1]
    with open("%s\\utilization_report.txt"%(dir_pathway, ), "w") as f:
        for line  in util_region:
            f.write(line)



if __name__ == "__main__":
    measure_area()
