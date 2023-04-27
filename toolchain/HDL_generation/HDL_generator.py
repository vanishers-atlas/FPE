# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import json
import importlib
import warnings

from FPE.toolchain.HDL_generation import utils as gen_utils


def generate_module(
    module_select,
    config,
    module_name = None,
    HDL_output_path=".",
    concat_naming = False,
    force_generation = True
):
    assert type(module_select) == str, "Module select must be a string"
    assert type(module_name) == str or module_name == None, "module_name select must be a string or None"
    assert type(config) == dict or type(config) == str, "config must be a dict, or file path to a json file"
    assert type(HDL_output_path) == str, "HDL_output_path select must be a filepath"
    assert type(concat_naming) == bool, "concat_naming must be a boolean"
    assert type(force_generation) == bool, "force_generation must be a boolean"

    # Load config if needed
    if type(config) == str:
        with open(config, "r") as f:
            config = json.load(f)

    # Import module generation script
    script = importlib.import_module(".".join(__name__.split(".")[0:-1] + module_select.split(".")))
    returned_interface, returned_name = script.generate_HDL(config, HDL_output_path, module_name, concat_naming, force_generation)

    return returned_interface, returned_name


def wrap_module(
    module_name,
    module_interface,
    wrapped_generics,
    wrapped_name = None,
    HDL_output_path=".",
    full_wrap = True
):
    assert type(module_name) == str, "module_name select must be a string"
    assert type(module_interface) == dict or type(module_interface) == str, "module_interface must be a dict, or file path to a json file"
    assert type(wrapped_generics) == dict, "wrapped_generics must be a dict"
    assert type(wrapped_name) == str or wrapped_name == None, "wrapped_name select must be a string or None"
    assert type(HDL_output_path) == str, "HDL_output_path select must be a filepath"
    assert type(full_wrap) == bool, "full_wrap select must be boolean"

    # Load module_interface if needed
    if type(module_interface) == str:
        with open(module_interface, "r") as f:
            module_interface = json.load(f)

    return _wrap_module_generate_hdl(module_name, module_interface, wrapped_generics, wrapped_name, HDL_output_path, full_wrap)

def _wrap_module_generate_hdl(module_name, module_interface, wrapped_generics, wrapped_name, HDL_output_path, full_wrap) :
    if wrapped_name == None:
        wrapped_name = module_name + "_wrapped"

    gen_det = gen_utils.generation_details({}, HDL_output_path, wrapped_name, False, False)
    com_det = gen_utils.component_details()

    com_det.add_import("ieee", "std_logic_1164", "all")

    # Ripple up generics
    if not full_wrap:
        for generic, details in module_interface["generics"].items():
            assert "type" in details.keys(), "Misformed module interface"
            if generic not in wrapped_generics.keys():
                 try:
                     com_det.add_generic(generic, details["type"], details["width"])
                 except KeyError:
                     com_det.add_generic(generic, details["type"])

    # Ripple up ports
    assert "ports" in module_interface.keys() and type(module_interface["ports"]) == dict, "Misformed module interface"
    for port, details in module_interface["ports"].items():
        assert "type" in details.keys(), "Misformed module interface"
        assert "direction" in details.keys(), "Misformed module interface"

        try:
            com_det.add_port(port, details["type"], details["direction"], details["width"])
        except KeyError:
            com_det.add_port(port, details["type"], details["direction"])

    # Onstancate wrapped module
    com_det.arch_body +=  "%s : entity work.%s(arch)\n\>"%(wrapped_name, module_name)

    if len(module_interface["generics"]) != 0:
        com_det.arch_body += "generic map (\>\n"

        for generic, details in module_interface["generics"].items():
            assert "type" in details.keys(), "Misformed module interface"
            if generic in wrapped_generics.keys():

                if details["type"] == "string" or details["type"].startswith("std_logic_vector"):
                    com_det.arch_body += "%s => \"%s\",\n"%(generic, wrapped_generics[generic])
                elif details["type"] == "std_logic":
                    com_det.arch_body += "%s => \'%s\',\n"%(generic, wrapped_generics[generic])
                else:
                    com_det.arch_body += "%s => %s,\n"%(generic, wrapped_generics[generic])
            elif full_wrap:
                raise KeyError("Generic not supplied, " + generic)
            else:
                com_det.arch_body += "%s => %s,\n"%(generic, generic)

        com_det.arch_body.drop_last_X(2)
        com_det.arch_body += "\<\n)\n"

    com_det.arch_body += "port map (\>\n"

    for port, details in module_interface["ports"].items():
        com_det.arch_body += "%s => %s,\n"%(port, port)

    com_det.arch_body.drop_last_X(2)
    com_det.arch_body += "\<\n);\n"

    com_det.arch_body += "\<\n"

    # Generate vhdl
    gen_utils.generate_files(gen_det, com_det)

    return com_det.get_interface(), gen_det.module_name


####################################################################

def generate(
    module_select,
    module_name,
    config,
    HDL_output_path=".",
    concat_naming = False,
    force_generation = True
):
    warnings.warn("generate is deprecated, please use generate_module")

    _, returned_name = generate_module(
        module_select = module_select,
        config = config,
        module_name = module_name,
        HDL_output_path = HDL_output_path,
        concat_naming = concat_naming,
        force_generation = force_generation
    )

    return returned_name
