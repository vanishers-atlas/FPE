import json
import importlib

def generate(
    module_select, module_name,
    config_filename, HDL_output_path=".",
    generate_name = True, force_generation = True
):
    with open(config_filename, "r") as f:
        config = json.load(f)

    # Import module generation script
    script = importlib.import_module(".".join(__name__.split(".")[0:-1] + module_select.split(".")))
    _, returned_name = script.generate_HDL(config, HDL_output_path, module_name, generate_name, force_generation)

    return returned_name
