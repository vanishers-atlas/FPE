class parameters:
    def __init__(this, jsonStr):
        #Bind JSON string to jsonExtractor
        import jsonExtractor
        para = jsonExtractor.jsonExtractor()
        para.bindJSON(jsonStr)

        #Extract json fields to object fields, checking as goes


        #Calulate para derived values


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

def genEntity(signals, moduleName, ports, para):
    signals += "\nentity " + moduleName +" is\n\t"
    signals += ports
    signals += "\bend entity;\n\n"
    signals += "architecture arch of " + moduleName + " is\n\t"
    return signals

def genArch(arch):
    arch += "\bbegin\n\t"

    #Add asserts for relationships before generics
    arch += "assert ()\n\t"
    arch += "report \" \"\n"
    arch += "severity failure;\n\b"

    return arch

def genPorts(ports, para):
    ports += "generic (\n\t"

    ports += "\b);\n"
    ports += "port (\n\t"

    ports += "\b);\n"
    return ports

#Root Generate function
def generate(settings):
    #Process passed json parameters
    para = parameters(settings.jsonStr)

    #Start creating VHDL
    import indentedString
    arch    = genArch   (indentedString.indentedString())
    ports   = genPorts  (indentedString.indentedString(), para)
    signals = genEntity (indentedString.indentedString(), settings.moduleName, ports, para)
    package = genPackage(indentedString.indentedString(), settings.moduleName, ports)
    imports = genImports(indentedString.indentedString())

    #Add entity behavour to arch string


    #Close architecture and save VHDL
    arch += "\bend architecture;"
    printToFile(settings.outputPath + "\\" + settings.moduleName, settings.force, package + imports + signals + arch)

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
