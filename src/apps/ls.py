from apps.stream import Stream
import os
from apps.exceptions import InvalidFileOrDir
from apps.decorators import argumentLimit


def listDirectory(dir):
    # returns a list containing a single string of directories
    # that are followed by \n
    dirs = []
    try:
        for file in os.listdir(dir):
            if not file.startswith("."):
                dirs.append(file + "\n")
    except FileNotFoundError:
        raise InvalidFileOrDir(f"No such directory {dir}")
    return "".join(dirs)


@argumentLimit(1, strict=False)
def ls(stream: "Stream"):
    args = stream.getArgs()
    stdout = stream.getStdout()
    workingDir = stream.getWorkingDir()
    if len(args) == 0:
        stdout.write(listDirectory(workingDir))
    else:
        stdout.write(listDirectory(args[0]))
