from apps.Stream import Stream
import os
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import hasOneArgument


@hasOneArgument
def cd(stream: "Stream"):
    args = stream.getArgs()
    try:
        os.chdir(args[0])
        stream.addToEnv("workingDir", os.getcwd())
    except FileNotFoundError:
        raise InvalidFileOrDir("Directory does not exist")
