import os
import sys

# Since visual studio is retarded and wont let me set a specific file root folder I made this garbage
# Fixes namespace.src.whatever to namespace.whatever (treats a subfolder as root instead)
# arguments are fixer.py [rootNamespace] [rootFolder]

if len(sys.argv) < 3:
    print("Not enough args! fixer.py [rootNamespace] [rootFolder]")
    exit(1)

rootNamespace = sys.argv[1]
rootFolder = sys.argv[2]


def pathToNamespace(path: str):
    pathNormalized = path.replace("\\", "/")
    folders = pathNormalized.split("/")

    for i in range(len(folders) - 1, -1, -1):
        if folders[i] == "":
            del folders[i]

    if len(folders) == 0:
        return rootNamespace

    return rootNamespace + "." + ".".join(folders)


if not os.path.exists(rootFolder):
    print("root folder doesn't exist!")
    exit(1)

os.chdir(rootFolder)
rootFolder = os.getcwd()

for path, dirs, files in os.walk(rootFolder):
    print(path, dirs, files)
    namespace = pathToNamespace(path[len(rootFolder) + 1 :])
    # print(namespace)

    for f in files:
        if not f.endswith(".cs"):
            continue

        print(f)
        lines = []
        with open(os.path.join(path, f), "r") as file:
            lines = file.readlines()
            foundNamespace = False

            for i in range(len(lines)):
                line = lines[i]

                if line.startswith("namespace"):
                    foundNamespace = True
                    line = f"namespace {namespace};\n"
                    lines[i] = line
                    # print(line, end="")

            if not foundNamespace:
                print(f"{f} is missing namespace!")
                exit(1)

        with open(os.path.join(path, f), "w") as file:
            file.writelines(lines)
