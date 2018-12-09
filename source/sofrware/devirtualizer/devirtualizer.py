import sys

#Check given args
if (len(sys.argv) != 4):
    print("Error ", sys.argv[0], " requires 3 filenames")
    print("A .vc filw, a .json file, a output filename,")
    print("The .vc file is the input virtualized code")
    print("The .json file is the parameters to be used to devirtualize the .vc file")
    print("The devirtualized code will be output in a new file named the third filename .vhd")
    exit(1);

if not(sys.argv[1].lower().endswith(".vc")):
    print("The first arg for this script must be a path to a .vc file")
    exit(1);
if not(sys.argv[2].lower().endswith(".json")):
    print("The first arg for this script must be a path to a .json file")
    exit(1);

#Read in json file
import json
print("loading ", sys.argv[2])
file = open(sys.argv[2], "r")
para = json.loads(file.read())
file.close()

print(para)

#Try and open passed files
print("loading ", sys.argv[1])
file = open(sys.argv[1], "r")
virtualCode = file.read()
file.close()

def printTree(root, level):
    #Print root details
    for i in range(level+ 1):
        print('>', end='')

    print(root.type, end=' ')
    try:
        print(repr(root.data), end='')
    except Exception as e:
        pass

    print("\n", end='')

    try:
        for subTree in root.children:
            printTree(subTree, level + 1)
    except Exception as e:
        pass

#Parse VCfile into Abstract Syntax Tree
from VCParser import createASTree
print("Creating Abstract Syntax Tree from .VC")
ASTree = createASTree(virtualCode)
printTree(ASTree, 0)
