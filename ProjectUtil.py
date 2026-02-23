import argparse
import json
import os
import subprocess


def setVersion(args):
    infoFile = args.pluginInfoFile
    print(infoFile)
    version = args.version
    print("New version", version)

    with open("ThunderStore/manifest.json", "r+") as original:
        test = json.load(original)
        test["version_number"] = version
        original.seek(0)
        original.truncate()
        json.dump(test, original, indent=4)

    with open(infoFile, "r+") as info:
        lines = info.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if " string VERSION = " in line:
                string = line[: line.find("=") + 2]
                string += f'"{version}";\n'
                lines[i] = string
                break

        info.seek(0)
        info.truncate(0)
        info.writelines(lines)


def renameProject(args):
    print(args)
    files = os.listdir()
    newName = args.newName
    solution = ""
    for file in files:
        if file.endswith(".sln"):
            solution = file
            print("Solution:", solution)

    targetProj = solution[: solution.rfind(".")] + ".csproj"
    targetProjPath = ""
    for path, dirs, files in os.walk(os.getcwd()):
        # print(files)
        for file in files:
            if file == targetProj:
                print("Found project file!")
                targetProj = os.path.join(path, targetProj)
                targetProjPath = path

    # rename solution, remove old project, rename proj and readd
    os.rename(solution, newName + ".sln")
    os.system("dotnet solution remove " + targetProj)

    newCsproj = os.path.join(targetProjPath, newName + ".csproj")
    os.rename(targetProj, newCsproj)
    os.system("dotnet solution add " + newCsproj)

    lines = []
    with open(newCsproj, "r+") as file:
        lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]

            if (pos := line.find("<AssemblyName>")) != -1:
                nameProp = f"<AssemblyName>{newName}</AssemblyName>\n"
                lines[i] = line.replace(line[pos:], nameProp)
                continue

            if (pos := line.find("<RootNamespace>")) != -1:
                nameProp = f"<RootNamespace>{newName}</RootNamespace>\n"
                lines[i] = line.replace(line[pos:], nameProp)
                continue

    with open(newCsproj, "w") as file:
        file.writelines(lines)


def pathToNamespace(rootNamespace: str, path: str):
    pathNormalized = path.replace("\\", "/")
    folders = pathNormalized.split("/")

    for i in range(len(folders) - 1, -1, -1):
        if folders[i] == "":
            del folders[i]

    if len(folders) == 0:
        return rootNamespace

    return rootNamespace + "." + ".".join(folders)


def fixNamespaces(args):
    rootNamespace = args.rootNamespace
    rootFolder = args.rootFolder

    if not os.path.exists(rootFolder):
        print("root folder doesn't exist!")
        exit(1)

    os.chdir(rootFolder)
    rootFolder = os.getcwd()

    for path, dirs, files in os.walk(rootFolder):
        print(path, dirs, files)
        namespace = pathToNamespace(rootNamespace, path[len(rootFolder) + 1 :])
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

                if not foundNamespace:
                    print(f"{f} is missing namespace!")
                    exit(1)

            with open(os.path.join(path, f), "w") as file:
                file.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atlyss python utils")
    sub = parser.add_subparsers(dest="cmd", required=True)

    vSet = sub.add_parser("set-version", help="Set new semantic version")
    vSet.add_argument("version")
    vSet.add_argument("pluginInfoFile")
    vSet.set_defaults(func=setVersion)

    rename = sub.add_parser("rename-project", help="Rename the solution and project")
    rename.add_argument("newName")
    rename.set_defaults(func=renameProject)

    rename = sub.add_parser(
        "fix-namespaces", help="Fix all namespaces caused by src folder"
    )
    rename.add_argument("rootNamespace")
    rename.add_argument("rootFolder")
    rename.set_defaults(func=fixNamespaces)

    help = sub.add_parser("help", help="Show help")
    help.set_defaults(func=lambda args: parser.print_help())

    args = parser.parse_args()
    args.func(args)
