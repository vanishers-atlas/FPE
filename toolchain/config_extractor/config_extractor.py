# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

# Import ParseTreeWalker from antlr so extactors can walk loading tree
from antlr4 import ParseTreeWalker

# Import json for reading/writing json files
import json

import warnings

# import config extractors
from FPE.toolchain.config_extractor import parameter_rollcall
from FPE.toolchain.config_extractor import feature_extraction

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

##############################################################################

def extract_config(assembly_file, parameter_file, config_file):
    program_context = asm_utils.load_file(assembly_file)
    walker = ParseTreeWalker()

    # Take rollcall of components used in FPE
    extractor = parameter_rollcall.extractor(program_context)
    walker.walk(extractor, program_context["program_tree"])
    pare_from_file = extractor.return_findings()

    # Handle parameters from parameter file
    config = handle_parameter_file(parameter_file, pare_from_file)

    # Computer widths derived from parameters
    compute_widths(config)

    # Extraction rest of the config from asm code
    for feature in feature_extraction.features:
        extractor = feature.extractor(program_context, config)
        walker.walk(extractor, program_context["program_tree"])
        config = extractor.get_updated_config()

    with open(config_file, "w") as f:
        f.write(json.dumps(config, sort_keys=True, indent=4))

##############################################################################

def handle_parameter_file(parameter_file, pare_from_file):
    # Load parameter file
    try:
        with open(parameter_file, "r") as f:
            para_file = json.loads(f.read())
    except FileNotFoundError:
        # Create blank parameter file
        with open("required_parameters.json", "w") as f:
            f.write(json.dumps(pare_from_file, sort_keys=True, indent=4))
        raise ValueError("No parameter file given, a blank one was created, please replace the nulls")

    # Generate config from from parameter file
    config = process_parameter_file(pare_from_file, para_file)

    # Check all required paras are filled
    if check_for_none(config):
        # Create blank parameter file
        with open("required_parameters.json", "w") as f:
            f.write(json.dumps(config, sort_keys=True, indent=4))
        raise ValueError("Not all parameters given, a partual filled in parameter file was created, please replace the nulls")

    return config

def process_parameter_file(required, given, config = None, keys=[]):
    # Copy required parameters into config
    if config == None:
        config = required.copy()

    # Loop over given parameters
    for k, v in given.items():
        # Check parameter is required
        if k in required.keys():
            # Handle sub dicts
            if isinstance(v, dict):
                process_parameter_file(required[k], v, config[k], [*keys, k])
            # Handle plain values
            else:
                config[k] = v
        # Warn for given parameter being ig
        else:
            warnings.warn("Parameter \"%s\" given but not required, and so well be ignored"%(
                ".".join([*keys, k])
            ) )

    return config

def check_for_none(data):
    for v in data.values():
        if isinstance(v, dict):
            if check_for_none(v):
                return True
        elif v == None:
            return True
    return False


##############################################################################

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
        if "depth" in mem and "FIFOs" not in mem:
            mem["addr_width"]= tc_utils.unsigned.width(mem["depth"] - 1)
        elif "depth" not in mem and "FIFOs" in mem:
            mem["addr_width"]= tc_utils.unsigned.width(mem["FIFOs"] - 1)
        elif "depth" in mem and "FIFOs" in mem:
            raise ValueError("Both depth and FIFOs given for memory, $s, addr_width is ambiguous"%(mem))
