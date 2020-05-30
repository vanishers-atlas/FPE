# Import ParseTreeWalker from antlr so extactors can walk loading tree
from antlr4 import ParseTreeWalker

# Import json for reading/writing json files
import json

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

# import config extractors
from . import parameter_detection
from . import feature_extraction

# import toolchain utils for computing addr widths
from .. import utils as tc_utils

def merge_parameters(required, given, config = None):
    # Copy required parameters into config
    if config == None:
        config = required.copy()

    # Loop over given parameters
    for k, v in given.items():
        if k not in config or not isinstance(v, dict):
            config[k] = v
        else:
            merge_parameters(None, v, config[k])
    return config

def check_for_none(data):
    for v in data.values():
        if isinstance(v, dict):
            if check_for_none(v):
                return True
        elif v == None:
            return True
    return False

def compute_widths(config):
    # Handle addr source ie bams
    for addr in config["address_sources"].values():
        if "addr_max" in addr:
            addr["addr_width"]   = tc_utils.unsigned.width(addr["addr_max"])
        if "offset_max" in addr:
            addr["offset_width"] = tc_utils.unsigned.width(addr["offset_max"])
        if "step_max" in addr:
            addr["step_width"]   = tc_utils.unsigned.width(addr["step_max"])

    # Handle memories
    for mem in config["data_memories"].values():
        if "depth" in mem:
            mem["addr_width"]= tc_utils.unsigned.width(mem["depth"] - 1)


def extract_config(assembly_file, parameter_file, config_file):
    program_context = FPEA.load_file(assembly_file)
    walker = ParseTreeWalker()

    # Take rollcall of components used in FPE
    extractor = parameter_detection.extractor(program_context)
    walker.walk(extractor, program_context["program_tree"])
    required_parameters = extractor.return_findings()

    # Handle parameter file
    try:
        # Load input parameter
        with open(parameter_file, "r") as f:
            given_parameters = json.loads(f.read())

        # Check that all required parameters are given
        config = merge_parameters(required_parameters, given_parameters)
        if check_for_none(config):
            # Create blank parameter file
            with open("required_parameters.json", "w") as f:
                f.write(json.dumps(config, sort_keys=True, indent=4))
            raise ValueError("Not all parameters given, a partual filled in parameter file was created, please replace the nulls")
    except FileNotFoundError:
        # Create blank parameter file
        with open("required_parameters.json", "w") as f:
            f.write(json.dumps(required_parameters, sort_keys=True, indent=4))
        raise ValueError("No parameter file given, a blank one was created, please replace the nulls")

    # Computer widths from config
    compute_widths(config)

    # Geneterate the rest of the config file
    for feature in feature_extraction.features:
        extractor = feature .extractor(program_context, config)
        walker.walk(extractor, program_context["program_tree"])
        config = extractor.get_updated_config()

    with open(config_file, "w") as f:
        f.write(json.dumps(config, sort_keys=True, indent=4))
