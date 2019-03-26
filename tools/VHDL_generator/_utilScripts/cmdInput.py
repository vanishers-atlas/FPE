#############################################################
###                 Command line Handling                 ###
#############################################################
class scriptSetting:
    def __init__(this):
        this.force = False
        this.jsonStr = None
        this.instrJson = None
        this.outputPath = None
        this.moduleName = None

import sys

def printUsage(includeIntr):
    print(sys.argv[0],"Usage:")
    print("Required Data Flags")
    print(" -j filename.json --the path to the parameter json file")
    if includeIntr:
        print(" -i filename.json --the path to the instr encoding json file")
    print(" -p path          --the path to the output folder json file")
    print(" -m moduleName    --the name of the produced module")
    print("Optional Flags")
    print(" -o               --Tells the cript to overwrite any existing files")
    exit()

def handle_json_flag(index, jsonStr, flag):
    #Check for multiple -json flags
    if jsonStr != None:
        raise ValueError("Error: multiple %s flags found."%(flag,))

    #Protect from buffer overflow within fuction
    if index + 1 >= len(sys.argv):
        raise BufferError("Error: %s flag occurred without enough data after."%(flag,))

    #Check given file path
    if not(sys.argv[index + 1].lower().endswith(".json")):
        raise FileNotFoundError("Error: filepath following %s flag doesn't point to a .json file"%(flag,))

    #Read in json file
    print("Loading ", sys.argv[index + 1])
    f = open(sys.argv[index + 1], "r")
    jsonStr = f.read()
    f.close()

    #Return updated index and red jsonStr
    return index + 2, jsonStr

def handle_p_flag(index, outputPath):
    #Check for multiple -p flags
    if outputPath != None:
        raise ValueError("Error: multiple -p flags found.")

    #Protect from buffer overflow within fuction
    if index + 1 >= len(sys.argv):
        raise BufferError("Error: -p flag occurred without enough data after.")

    #Update index and process remain cmd args
    outputPath = sys.argv[index + 1]
    return index + 2, outputPath

def handle_m_flag(index, moduleName):
    #Check for multiple -p flags
    if moduleName != None:
        raise ValueError("Error: multiple -m flags found.")

    #Protect from buffer overflow within fuction
    if index + 1 >= len(sys.argv):
        raise BufferError("Error: -m flag occurred without enough data after.")

    #Return updated index and moduleName
    moduleName = sys.argv[index + 1]
    return index + 2, moduleName

def handle_o_flag(index, force):
    #Check for multiple -o flags
    if force != False:
        raise ValueError("Error: multiple -o flags found.")

    return index + 1, True

def processCMDInput(includeIntr = False):
    #Print Usage if no data passed
    if len(sys.argv) == 1:
        printUsage(includeIntr)

    #Init cmd data to default values
    setting = scriptSetting()
    index = 1

    #Process all command args
    while index < len(sys.argv):
        if   sys.argv[index] == "-j":
            index, setting.jsonStr    = handle_json_flag(index, setting.jsonStr, "-j")
        elif includeIntr and sys.argv[index] == "-i":
            index, setting.instrJson  = handle_json_flag(index, setting.instrJson, "-i")
        elif sys.argv[index] == "-p":
            index, setting.outputPath = handle_p_flag(index, setting.outputPath)
        elif sys.argv[index] == "-m":
            index, setting.moduleName = handle_m_flag(index, setting.moduleName)
        elif sys.argv[index] == "-o":
            index, setting.force = handle_o_flag(index, setting.force)
        else:
            raise ValueError("Error: unknown flag \"" + sys.argv[index] + "\"")

    #Check required data has been given
    if includeIntr and setting.instrJson == None:
        raise ValueError("Error: No Intruction encodong json file given\n")
    if setting.jsonStr == None:
        raise ValueError("Error: No parameter json file given\n")
    if setting.outputPath == None:
        raise ValueError("Error: No output file given\n")
    if setting.moduleName == None:
        raise ValueError("Error: No module name given\n")

    #Return data
    return setting
