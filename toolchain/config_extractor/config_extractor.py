# Import ParseTreeWalker from antlr so extactors can walk loading tree
from antlr4 import ParseTreeWalker

# Import json for reading/writing json files
import json

# import FPE assembly handling module
from .. import FPE_assembly as FPEA

# import config extractors
from . import parameter_detection
from . import instruction_set_extraction
from . import IMM_extraction
from . import BAM_extraction
from . import ZOL_extraction
from . import PC_extraction

# import toolchain utils for computing addr widths
from .. import utils

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
    # Handle addr_widths
    config["addr_width"] = 0
    for mem in config["data_memories"].values():
        if "depth" in mem.keys():
            config["addr_width"] = max([config["addr_width"], utils.unsigned.width(mem["depth"] - 1)])

    # Handle Pc width
    config["fetch_decode"]["PC_width"] = utils.unsigned.width(config["fetch_decode"]["program_length"] - 1)

    # Update data width with PC wisth if jumping occurs
    jumps = ("JMP#", "JLT#")
    if any([op_id.startswith(jumps) for op_id in config["instr_set"].keys()]):
        config["data_width"] = max([config["data_width"], config["fetch_decode"]["PC_width"] ])

def extract_config(assembly_file, parameter_file, config_file):
    assembly = FPEA.load_file(assembly_file)
    walker = ParseTreeWalker()

    # Take rollcall of components used in FPE
    extractor = parameter_detection.extractor()
    walker.walk(extractor, assembly)
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

    # Geneterate the rest of the config file
    for feature in [
        instruction_set_extraction,
        IMM_extraction,
        BAM_extraction,
        ZOL_extraction,
        PC_extraction,
    ]:
        extractor = feature.extractor(config)
        walker.walk(extractor, assembly)
        config = extractor.get_updated_config()

    # Computer widths from config
    compute_widths(config)

    with open(config_file, "w") as f:
        f.write(json.dumps(config, sort_keys=True, indent=4))
