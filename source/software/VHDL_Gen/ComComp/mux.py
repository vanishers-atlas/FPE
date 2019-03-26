class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        import math
        #Extract json fields to object fields, checking as goes
        this.number_inputs = para.getInt("number_inputs", gt = 0)
        this.binary_select  = para.getBool("binary_select")

        if this.binary_select: this.address_width = math.ceil(math.log(this.number_inputs, 2))

##################################################################################0

def genPackage(package, moduleName, ports):
    package += "--Include packages used in package declaration\n"
    package += "library ieee;\n"
    package += "use ieee.std_logic_1164.all;\n\n"
    package += "package " + moduleName + "_pkg is\n\t"
    package += "component " + moduleName + " is\n\t"
    package += ports
    package += "\bend component;\n"
    package += "\bend package;\n\n"
    package += "----------------------------------------------------------------------------------------------\n\n"
    return package

def printToFile(outputfile, force, fileText):
    import os
    outputfile += ".vhd"
    if not force and os.path.isfile(outputfile):
        raise FileExistsError(outputfile + " already exists")
    print("Creating " + outputfile)
    f = open(outputfile, "w")
    f.write(str(fileText))
    f.close()

##################################################################################

def genImports(imports):
    imports += "--Include packages used in implanentation\n"
    imports += "library ieee;\n"
    imports += "use ieee.std_logic_1164.ALL;\n"
    return imports

def genEntity(signals, moduleName, ports):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"

    #Add asserts for relationships before generics
    arch += "assert (data_width > 0)\n\t"
    arch += "report \"data_width must be positive\"\n"
    arch += "severity failure;\n\b\n"

    return arch

def genPorts(ports, para):
    ports += "generic (\n\t"
    ports += "data_width : integer := 8\n"
    ports += "\b);\n"
    ports += "port (\n\t"
    for i in range(para.number_inputs):
        ports += "input_%i : in std_logic_vector(data_width - 1 downto 0);\n"%(i,)
    if para.binary_select:
        ports += "input_select : in std_logic_vector(%i downto 0);\n"%(para.address_width - 1,)
    else:
        for i in range(para.number_inputs):
             ports += "select_%i : in std_logic;\n"%(i,)
    ports += "data_out : out std_logic_vector(data_width - 1 downto 0)\n"
    ports += "\b);\n"
    return ports

def genEncodedBehavour(para, arch):
    #Add entity behavour to arch string
    arch += "\nprocess (input_select"
    for i in range (para.number_inputs):
        arch += ", input_%i"%(i,)
    arch += ")\n"
    arch += "begin\n\t"
    arch += "--Mux data_out\n"
    arch += "case input_select is\n\t"
    for i in range (para.number_inputs - 1):
        arch += ("when \"{0:0%ib}\" =>\n\t"%(para.address_width,)).format(i)
        arch += "data_out <= input_%i;\n\b"%(i,)
    arch += "when others =>\n\t"
    arch += "data_out <= input_%i;\n\b"%(para.number_inputs - 1,)
    arch += "\bend case;\n"
    arch += "\bend process;\n"
    return arch

def genNonEncodedBehavour(para, arch):
    #Add entity behavour to arch string
    arch += "\nprocess ("
    comma = ""
    for i in range (para.number_inputs):
        arch += "%sinput_%i, select_%i"%(comma, i, i)
        comma = ", "
    arch += ")\n"
    arch += "begin\n\t"
    arch += "--Mux data_out\n"
    connector = ""
    for i in range (para.number_inputs):
        arch += "%sif select_%i = '1' then\n\t"%(connector, i)
        arch += "data_out <= input_%i;\n\b"%(i,)
        connector = "els"
    arch += "end if;\n"
    arch += "\bend process;\n"
    return arch

#Root Generate function
def generate(settings):
    #Process passed json parameters
    para = parameters(settings.jsonStr)

    #Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    #Add entity behavour to arch string
    if para.binary_select:
        arch = genEncodedBehavour(para, arch)
    else:
        arch = genNonEncodedBehavour(para, arch)

    #Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

    if para.binary_select:
        return para.address_width, 1
    else:
        return 1, para.number_inputs

##################################################################################
###                           Command line Handling                            ###
##################################################################################

import sys
if __name__ == '__main__':
    #Add Needed paths
    pathRoot = sys.path[0] + "\\.."
    sys.path.append(pathRoot)

    #Handle Commandline input
    sys.path.append(pathRoot + "\\_utilScripts")
    import cmdInput
    settings = cmdInput.processCMDInput()
    settings.pathRoot = pathRoot
    generate(settings)
