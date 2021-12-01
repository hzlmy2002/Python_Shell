from apps.Stream import Stream
import os
from apps.Exceptions import InvalidFileOrDir, InvalidArgumentError


def cd(stream: "Stream"):
    args = stream.getArgs()
    if len(args) != 1:
        raise InvalidArgumentError("Should specify only one directory")
    try:
        os.chdir(args[0])
        stream.addToEnv("workingDir", os.getcwd())
    except:
        raise InvalidFileOrDir("Directory does not exist")
