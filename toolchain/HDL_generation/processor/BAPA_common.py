# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import math
import itertools as it
import re

from FPE.toolchain import utils as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation  import utils as gen_utils

from FPE.toolchain.HDL_generation.processor import BAPA_packed_wrapper as BAPA_packed
from FPE.toolchain.HDL_generation.processor import BAPA_split_wrapper  as BAPA_split

#####################################################################

def add_inst_config(instr_id, instr_set, config):
    if "pipelined_writes" not in config.keys():
        config["pipelined_writes"] = False

    if "allow_packed" not in config.keys():
        config["allow_packed"] = True

    if "allow_split" not in config.keys():
        config["allow_split"] = True

    reads, writes = _gather_reads_and_writes(instr_id, instr_set)
    assert len(reads) != 0, "unread memory found, " + instr_id

    min_read = min( read["min"] for read in reads)
    max_read = max( read["max"] for read in reads)
    if len(writes) == 0:
        min_write = 0
        max_write = 0
    else:
        min_write = min( write["min"] for write in writes)
        max_write = max( write["max"] for write in writes)

    # Check if BAPA is needed
    print(min_write, max_write, min_read, max_read)
    if max_read == 1 and max_write <= 1:
        return None
    # Check if pure padding could handle BAPA needs
    elif config["allow_packed"] and (config["pipelined_writes"] or max_write == 0 or (min_write == max_write and max_write >= max_read ) ):
        print("packed")
        return BAPA_packed.add_inst_config(instr_id, instr_set, config, reads, writes, min_read, max_read, min_write, max_write)
    # Fall back on split BAPA if allowed
    elif config["allow_split"]:
        print("split")
        return BAPA_split.add_inst_config(instr_id, instr_set, config, reads, writes, min_read, max_read, min_write, max_write)
    else:
        raise ValueError("Can't handle the BAPA rqwuirements fot mem, %s, try alloing other stragyies"%(instr_id, ) )

def _gather_reads_and_writes(instr_id, instr_set):
    reads = []
    writes = []

    for instr in instr_set:
        read = 0
        for fetch in asm_utils.instr_fetches(instr):
            if asm_utils.access_mem(fetch) == instr_id:
                mods = asm_utils.access_mods(fetch)
                if "BAPA" in mods.keys():
                    words = int(mods["BAPA"])
                else:
                    words = 1

                try:
                    if reads[read]["min"] > words:
                        reads[read]["min"] = words
                    elif reads[read]["max"] < words:
                        reads[read]["max"] = words
                except IndexError:
                    reads.append( {"min" : words, "max" : words} )
                read += 1

        write = 0
        for store in asm_utils.instr_stores(instr):
            if asm_utils.access_mem(store) == instr_id:
                mods = asm_utils.access_mods(store)
                if "BAPA" in mods.keys():
                    words = int(mods["BAPA"])
                else:
                    words = 1

                try:
                    if writes[write]["min"] > words:
                        writes[write]["min"] = words
                    elif writes[write]["max"] < words:
                        writes[write]["max"] = words
                except IndexError:
                    writes.append( {"min" : words, "max" : words} )
                write += 1

    return reads, writes

##########################################################################

def get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane):
    if   config["BAPA"]["type"] == "packed":
        return BAPA_packed.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    elif config["BAPA"]["type"] == "split":
        return BAPA_split.get_inst_pathways(instr_id, instr_prefix, instr_set, interface, config, lane)
    else:
        raise ValueError("Unknown BAPA type, " + gen_det.config["BAPA"]["type"])


def get_inst_controls(instr_id, instr_prefix, instr_set, interface, config):
    if   config["BAPA"]["type"] == "packed":
        return BAPA_packed.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    elif config["BAPA"]["type"] == "split":
        return BAPA_split.get_inst_controls(instr_id, instr_prefix, instr_set, interface, config)
    else:
        raise ValueError("Unknown BAPA type, " + gen_det.config["BAPA"]["type"])


#####################################################################

def preprocess_config(config_in):
    config_out = {}

    assert "type" in config_in.keys()
    assert config_in["type"] in ["packed", "split"]
    config_out["type"] = config_in["type"]

    if   config_out["type"] == "packed":
        config_out = {
            **config_out,
            **BAPA_packed.preprocess_config(config_in),
        }
    elif config_out["type"] == "split":
        config_out = {
            **config_out,
            **BAPA_split.preprocess_config(config_in),
        }
    else:
        raise ValueError("Unknown BAPA type, " + gen_det.config_out["BAPA"]["type"])

    return config_out


#####################################################################

def generate_HDL(config, output_path, module_name=None, concat_naming=False, force_generation=False):

    if   config["type"] == "packed":
        return BAPA_packed.generate_HDL(config, output_path, module_name, concat_naming, force_generation)
    elif config["type"] == "split":
        return BAPA_split.generate_HDL(config, output_path, module_name, concat_naming, force_generation)
    else:
        raise ValueError("Unknown BAPA type, " + gen_det.config["BAPA"]["type"])
