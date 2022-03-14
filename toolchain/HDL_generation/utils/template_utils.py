from FPE.toolchain.HDL_generation.utils import indented_string as inStr

import json, zlib

class FilesInvalid (Exception):
    pass


###################################################################

class generation_details ():
    def __init__(this, config, output_path, module_name, concat_naming, force_generation):
        assert type(config) == dict, "config must be a dist"
        this.config = config

        assert type(output_path) == str, "output_path must be a string"
        this.output_path = output_path

        assert type(module_name) == str, "module_name must be a string"
        this.module_name = module_name

        assert type(concat_naming) == bool, "concat_naming must be a bool"
        this.concat_naming = concat_naming

        assert type(force_generation) == bool, "force_generation must be a bool"
        this.force_generation = force_generation

class component_details ():
    def __init__(this):
        this.arch_head = inStr.indented_string()
        this.arch_body = inStr.indented_string()

        this._imports = []

        this._ports = {}
        this._generics = {}
        this._misc_interface_items = {}


    def add_import(this, library, package, parts):
        this._imports.append( {
            "library" : library,
            "package" : package,
            "parts" : parts
        } )

    def get_imports(this):
        return this._imports


    def add_port(this, port_name, port_type, port_direction, port_width=None):
        assert type(port_name) == str, "port_name must be a string"
        assert port_name not in this._ports.keys(), "there already us a port called " + port_name

        assert type(port_type) == str, "port_type must be a string"

        assert type(port_direction) == str, "port_direction must be a string"

        assert port_width == None or type(port_width) == int, "port_width must be an int or absent"
        assert port_width == None or port_width > 0,  "port_width must be greater than 0"

        this._ports[port_name] = {
            "type" : port_type,
            "direction" : port_direction,
        }
        if port_width != None:
            this._ports[port_name]["width"] = port_width

    def add_generic(this, generic_name, generic_type, generic_width=None):
        assert type(generic_name) == str, "generic_name must be a string"
        assert generic_name not in this._generics.keys(), "there already us a generic called " + generic_name

        assert type(generic_type) == str, "generic_type must be a string"

        assert generic_width == None or type(generic_width) == int, "generic_width must be an int or absent"
        assert generic_width == None or generic_width > 0,  "generic_width must be greater than 0"

        this._generics[generic_name] = {
            "type" : generic_type,
        }
        if generic_width != None:
            this._generics[generic_name]["width"] = generic_width

    def add_interface_item(this, key, value):
        assert type(key) == str, "key must be a string"
        assert key not in this._misc_interface_items.keys(), "there already us an interface item called " + add_interface_item
        assert key not in ["ports", "generics"], "ports and generics should be added to the inferace via the add_port and add_generic functions"

        this._misc_interface_items[key] = value

    def get_interface(this):
        return {
            **this._misc_interface_items,
            "generics" : this._generics,
            "ports" : this._ports,
        }


###################################################################

def load_files(*args):
    # Handle input arg(s)
    if len(args) == 1:
        gen_det = args[0]
        assert type(gen_det) == generation_details, "Invalid usage, in collecton parameter mode, args[0] (gen_det) must be a generation_details"

        force_generation = gen_det.force_generation
        output_path = gen_det.output_path
        module_name = gen_det.module_name
    elif len(args) == 3:
        force_generation = args[0]
        assert type(force_generation) == bool, "Invalid usage, in seperate parameter mode, args[0] (force_generation)  must be a bool"

        output_path = args[1]
        assert type(output_path) == str, "Invalid usage, in seperate parameter mode, args[1] (output_path)  must be a str"

        module_name = args[2]
        assert type(module_name) == str, "Invalid usage, in seperate parameter mode, args[2] (module_name)  must be a str"
    else:
        raise SyntaxError("Invalad usage, load_files has 2 possible modes of usage: collecton parameters and seperate parameters. "
            + "in collecton parameter mode 1 paremeteris requiredL gen_det (generation_details). "
            + "In seperate parameter mode 3 parameters are required: force_generation(bool), output_path(str), and module_name(str)"
        )

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

def generate_files(*args):

    # Handle input arg(s)
    if len(args) == 2:
        assert type(args[0]) == generation_details, "Invalid usage, in collecton parameter mode, args[0] (gen_det) must be a generation_details"
        gen_det = args[0]

        assert type(args[1]) == component_details, "Invalid usage, in collecton parameter mode, args[1] (com_det) must be a component_details"
        com_det = args[1]

        output_path = gen_det.output_path
        module_name = gen_det.module_name

        imports = com_det.get_imports()
        arch_head = com_det.arch_head
        arch_body = com_det.arch_body
        interface = com_det.get_interface()

    elif len(args) == 6:
        output_path = args[0]
        assert type(output_path) == str, "Invalid usage, in seperate parameter mode, args[0] (output_path)  must be a str"

        module_name = args[1]
        assert type(module_name) == str, "Invalid usage, in seperate parameter mode, args[1] (module_name)  must be a str"

        imports = args[2]
        assert type(imports) == list, "Invalid usage, in seperate parameter mode, args[2] (imports)  must be a list"

        arch_head = args[3]
        assert type(arch_head) == inStr.indented_string, "Invalid usage, in seperate parameter mode, args[3] (arch_head)  must be an indented_string"

        arch_body = args[4]
        assert type(arch_body) == inStr.indented_string, "Invalid usage, in seperate parameter mode, args[4] (arch_body)  must be an indented_string"

        interface = args[5]
        assert type(interface) == dict, "Invalid usage, in seperate parameter mode, args[5] (interface)  must be a dict"
    else:
        raise SyntaxError("Invalad usage, generate_files has 2 possible modes of usage: collecton parameters and seperate parameters. "
            + "in collecton parameter mode 2 paremeteris requiredL gen_det(generation_details), and com_det(component_details). "
            + "In seperate parameter mode 6 parameters are required: output_path(str), module_name(str), imports(list), arch_head(indented_string), arch_body(indented_string), and imports(dict)"
        )

    output_path, module_name, imports, arch_head, arch_body, interface



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
