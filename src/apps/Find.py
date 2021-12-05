from apps.Stream import Stream
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError, InvalidParamError
import os
import fnmatch


def findFiles(rootPath: str, pattern: str) -> str:
    result = ""
    for root, _, files in os.walk(rootPath):
        for fName in files:
            if fnmatch.fnmatch(fName, pattern):
                result += root + os.sep + fName + "\n"
    return result


@intParam("name", required=True)
@atMostOneArgument
def find(stream: "Stream"):
    arg = stream.getArgs()
    rootPath = "."
    if len(arg) == 1:
        rootPath = arg[0]
        if not (os.path.exists(rootPath) and os.path.isdir(rootPath)):
            raise InvalidFileOrDir("File or Directory does not exist")
    pattern = stream.getParam("name")
    stdout = stream.getStdout()
    relativePaths = findFiles(rootPath, pattern)
    stdout.write(relativePaths)
