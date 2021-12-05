from apps.Stream import Stream
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError
import re


def match_line(filename, pattern, multFiles):
    """Finds matching pattern given by args returns matched lines"""
    res = ""
    try:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(pattern, line):
                    if multFiles:
                        res += f"{filename}:{line}"
                    else:
                        res += line
        return res
    except FileNotFoundError:
        raise InvalidFileOrDir("File does not exist")


def processFiles(fileNames, pattern):
    matched = ""
    multFiles = len(fileNames) > 1
    for filename in fileNames:
        matched += match_line(filename, pattern, multFiles)
    if not matched.endswith("\n"):
        matched += "\n"
    return matched


def getFileNameAndPattern(stream: "Stream"):
    args = stream.getArgs()
    pattern = args[0]
    if len(args) == 1:  # no file names specified
        fileNames = stream.getStdin()
        if fileNames is None:
            raise InvalidArgumentError("Argument is invalid")
    else:
        fileNames = args[1:]

    return fileNames, pattern


@hasArgument
def grep(stream: "Stream"):
    fileNames, pattern = getFileNameAndPattern(stream)
    res = processFiles(fileNames, pattern)
    stdout = stream.getStdout()
    stdout.write(res)
