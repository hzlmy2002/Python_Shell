from apps.Stream import Stream
import os
from apps.Exceptions import InvalidFileOrDir, InvalidArgumentError
from apps.decorators import hasOneArgument


@hasOneArgument
def cd(stream: "Stream"):
    args = stream.getArgs()
    try:
        os.chdir(args[0])
        stream.addToEnv("workingDir", os.getcwd())
    except:
        raise InvalidFileOrDir("Directory does not exist")
