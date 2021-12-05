from apps.Stream import Stream
import os
from apps.Exceptions import InvalidFileOrDir, InvalidArgumentError
from apps.decorators import atMostOneArgument


def listDirectory(ls_dir):
    # Returns a list containing a single string of directories that are followed by \n
    dirs = []
    try:
        for file in os.listdir(ls_dir):
            if not file.startswith("."):
                dirs.append(file + "\n")
    except FileNotFoundError:
        raise InvalidFileOrDir("No such file or directory")
    return "".join(dirs)


@atMostOneArgument
def ls(stream: "Stream"):
    args = stream.getArgs()
    stdout = stream.getStdout()
    if len(args) == 0:
        stdout.write(listDirectory(os.getcwd()))
    elif len(args) == 1:
        stdout.write(listDirectory(args[0]))
    else:
        raise InvalidArgumentError("Should specify only one directory")
