from FPE.toolchain.HDL_generation.utils import indented_string as inStr

import json, zlib

def handle_module_name(module_name, config, name_append_hash):
    if name_append_hash:
        return "%s_%s"%(module_name, str(hex(zlib.adler32(json.dumps(config, sort_keys=True).encode('utf-8'))).lstrip("0x").zfill(8)))
    else:
        return module_name

###################################################################
class FilesInvalid (Exception):
    pass

def load_files(force_generation, output_path, module_name):
    if not force_generation:
        try:
            with open(output_path + "\\" + module_name + ".inter") as f:
                inter = json.loads(f.read())

            with open(output_path + "\\" + module_name + ".vhd") as f:
                hash = zlib.adler32(f.read().encode('utf-8') )

            if inter["VHD_hash"] == hash:
                print("Re-using %s.vhd and %s.inter"%(module_name, module_name) )
                return inter, module_name
            else:
                raise FilesInvalid()
        except FileNotFoundError:
            raise FilesInvalid()
    else:
        raise FilesInvalid()


###################################################################

def generate_files(output_path, module_name, imports, arch_head, arch_body, interface):
    text = inStr.indented_string()

    # include imports
    last_lib = ""
    for element in sorted(imports, key=lambda e : e["library"] ):
        # Generate linray import statements
        if last_lib != element["library"]:
            text += "\nlibrary %s;\n"%(element["library"], )
            last_lib = element["library"]

        # Add use statements
        text += "use %s.%s.%s;\n"%(element["library"], element["package"], element["parts"])

    # start entity
    text += "\nentity " + module_name +" is\n\>"

    # Handle generics
    if len(interface["generics"]) != 0:
        text += "generic (\n\>"
        for generic in interface["generics"]:
            text += "%s : %s;\n"%(generic["name"], generic["type"])
        text.drop_last_X(2)
        text += "\n\<);\n"

    # Handle ports
    if len(interface["ports"]) != 0:
        text += "port (\n\>"
        for port in interface["ports"]:
            text += "%s : %s %s;\n"%(port["name"], port["direction"], port["type"])
        text.drop_last_X(2)
        text += "\n\<);"

    # end entity and start architecture
    text += "\n\<end entity;\n"
    text += "\narchitecture arch of " + module_name + " is\n\>"

    # Handle arch signals
    text += arch_head

    # Handle arch body
    text += "\<begin\n\>"
    text += arch_body
    text += "\<end architecture;\n"

    print("Creating %s.vhd and %s.inter"%(module_name, module_name) )
    with open(output_path + "\\" + module_name + ".vhd", "w") as f:
        f.write(str(text))

    interface["VHD_hash"] = zlib.adler32( str(text).encode('utf-8') )

    with open(output_path + "\\" + module_name + ".inter", "w") as f:
        f.write(json.dumps(interface, indent=4, sort_keys=True))
