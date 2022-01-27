from FPE.toolchain.HDL_generation.utils import indented_string as inStr

import json, zlib


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

        # Handle old list style generics
        if type(interface["generics"]) == list:
            for generic in interface["generics"]:
                try:
                    text += "%s : %s(%i downto 0);\n"%(generic["name"], generic["type"], generic["width"] - 1, )
                except Exception as e:
                    text += "%s : %s;\n"%(generic["name"], generic["type"], )
        # Handle new dict style generics
        if type(interface["generics"]) == dict:
            for generic, details in interface["generics"].items():
                try:
                    text += "%s : %s(%i downto 0);\n"%(generic, details["type"], details["width"] - 1, )
                except Exception as e:
                    text += "%s : %s;\n"%(generic, details["type"], )
        text.drop_last_X(2)
        text += "\n\<);\n"

    # Handle ports
    if len(interface["ports"]) != 0:
        text += "port (\n\>"
        # Handle old list style ports
        if type(interface["ports"]) == list:
            for port in interface["ports"]:
                try:
                    text += "%s : %s %s(%i downto 0);\n"%(port["name"], port["direction"], port["type"], port["width"] - 1, )
                except Exception as e:
                    text += "%s : %s %s;\n"%(port["name"], port["direction"], port["type"], )
        # Handle new dict style ports
        if type(interface["ports"]) == dict:
            for port, details in interface["ports"].items():
                try:
                    text += "%s : %s %s(%i downto 0);\n"%(port, details["direction"], details["type"], details["width"] - 1, )
                except Exception as e:
                    text += "%s : %s %s;\n"%(port, details["direction"], details["type"], )
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
