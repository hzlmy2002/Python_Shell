from apps.Stream import Stream
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError, InvalidParamError
from apps.Tools import getLines
import os
import fnmatch


def isInvalidPattern(pattern):
    return any(char in ["\\", "/", "?", '"', "<", ">", "|"] for char in pattern)


def findFiles(rootPath: str, pattern: str) -> str:
    result = ""
    for root, _, files in os.walk(rootPath):
        for fName in files:
            if fnmatch.fnmatch(fName, pattern):
                result += root + os.sep + fName + "\n"
    return result


@intParam("name", required=True)
def find(stream: "Stream"):
    arg = stream.getArgs()
    rootPath = "."
    if len(arg) == 1:
        rootPath = arg[0]
        if not (os.path.exists(rootPath) and os.path.isdir(rootPath)):
            raise InvalidFileOrDir("File or Directory does not exist")
    elif len(arg) != 0:
        raise InvalidArgumentError("Invalid Argument")
    pattern = stream.getParam("name")
    if isInvalidPattern(pattern):
        raise InvalidParamError("Invalid pattern entered")
    stdout = stream.getStdout()
    relativePaths = findFiles(rootPath, pattern)
    stdout.write(relativePaths)
