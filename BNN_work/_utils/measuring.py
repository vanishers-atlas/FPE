import subprocess
import json
import os
import re

note_line_pattern = re.compile("Note: layer_(\\d+) (starting|finished) frame (\\d+)")
time_line_pattern = re.compile("Time: (\\d+) (ns|us) ")

def impl_and_simulate_network(network_name, network_folder, dir_pathway, measure_area=True, measure_timing=True, compute_timing_metrics=True):
    PART="xc7z020clg400-1"

    # Collect all vhdl_files from generated network
    vhdl_files = [
        network_folder + "\\" + file
        for file in os.listdir(network_folder)
        if file.endswith(".vhd")
    ]
    code_dir = network_folder + "\\toolchain_files"
    vhdl_files += [
        code_dir + "\\" + file
        for file in os.listdir(code_dir)
        if file.endswith(".vhd")
    ]

    # Make sure project folder exists
    project_folder = network_folder + "\\measuring"

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
        f.write("set_property STEPS.SYNTH_DESIGN.ARGS.FLATTEN_HIERARCHY none [get_runs synth_1]\n")
        f.write("\n")


        # Load all vhdl files
        for file in vhdl_files:
            f.write("read_vhdl -library work %s;\n"%(file.replace("\\", "/"), ) )
        f.write("\n")

        f.write("source %s/gen_block_diagram.tcl\n"%(network_folder.replace("\\", "/"), ) )
        f.write("set_property top testbench [get_filesets sim_1]\n\n")

        # Run implemention
        if measure_area:
            f.write("launch_runs impl_1 -jobs 4\n")
            f.write("wait_on_run impl_1\n")
            f.write("open_run impl_1\n")
            f.write("report_utilization -hierarchical\n")
            f.write("\n")

        # Run simulation
        if measure_timing:
            f.write("launch_simulation -simset [current_fileset -simset];\n")
            f.write("run 500 ms;\n")
            f.write("close_sim -force;\n")
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
    if measure_area:
        util_start = lines.index("Utilization Design Information\n")
        util_end = lines.index("* Note: The sum of lower-level cells may be larger than their parent cells total, due to cross-hierarchy LUT combining\n")
        util_region = lines[util_start + 9 : util_end - 1]
        with open("%s\\utilization_report.txt"%(network_folder, ), "w") as f:
            for line  in util_region:
                f.write(line)


    # Extract timing data
    if measure_timing:
        timing_data = {}
        timing_start = lines.index("## current_wave_config\n")
        timing_end = lines.index("# close_sim -force;\n")
        timing_region = lines[timing_start : timing_end]

        for note_line, time_line, in zip(timing_region[0:], timing_region[1:]):
            note_match = note_line_pattern.match(note_line)
            time_match = time_line_pattern.match(time_line)
            if note_match != None and time_match != None :
                layer, start_end, frame = note_match.groups()
                time, unit = time_match.groups()

                # Convert time to ns
                if unit == "ns":
                    time_ns = int(time)
                elif unit == "us":
                    time_ns = 1000*int(time)

                if start_end == "starting":
                    try:
                        timing_data[layer]["frame_starts"].append(time_ns)
                    except KeyError:
                        timing_data[layer] = {
                            "frame_starts" : [time_ns, ],
                            "frame_ends" : [],
                        }
                else:
                    timing_data[layer]["frame_ends"].append(time_ns)

        with open("%s\\timing_data.json"%(network_folder, ), "w") as f:
            f.write(json.dumps(timing_data, indent=2))

    if compute_timing_metrics:
        if not measure_timing:
            with open("%s\\timing_data.json"%(network_folder, ), "r") as f:
                timing_data = json.reads(f.read())

        LAST_LAYER = str(len(timing_data.keys()) - 1)
        # Compute the latancy of each completed frame
        latancies = []
        for frame, end_time in enumerate(timing_data[LAST_LAYER]["frame_ends" ]):
            start_time = timing_data["0"]["frame_starts"][frame]
            latancies.append(end_time - start_time)

        # Compute the thorughput for rolled blocks
        FRANE_PER_BLOCK = 10
        thorughputs = []
        for block_start, block_end in zip(timing_data[LAST_LAYER]["frame_ends" ][0:], timing_data[LAST_LAYER]["frame_ends" ][FRANE_PER_BLOCK - 1:]):
            time_peroid = block_end - block_start
            thorughputs.append(FRANE_PER_BLOCK / (time_peroid / 10 ** 9))

        with open("%s\\timing_results.csv"%(network_folder, ), "w") as f:
            f.write("latancies,")
            for latancy in latancies:
                f.write(str(latancy))
                f.write(",")
            f.write("\n")
            f.write("thorughputs,")
            for thorughput in thorughputs:
                f.write(str(thorughput))
                f.write(",")
            f.write("\n")
