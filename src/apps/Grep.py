from io import StringIO
from apps.Stream import Stream
from apps.Tools import toList
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError
import re
from typing import List


def match_line(lines: "List[str]", pattern: str, multFiles=False, fileName=""):
    """Finds matching pattern given by args returns matched lines"""
    res = ""
    for line in lines:
        if re.match(pattern, line):
            if multFiles:
                res += f"{fileName}:{line}"
            else:
                res += line
    return res


def processFiles(fileNames: "List[str]", pattern: str) -> str:
    matched = ""
    multFiles = len(fileNames) > 1
    for filename in fileNames:
        try:
            with open(filename) as f:
                lines = f.readlines()
                matched += match_line(lines, pattern, multFiles, filename)
        except FileNotFoundError:
            raise InvalidFileOrDir("File does not exist")
    return matched


def processStdin(string: StringIO, pattern: str) -> str:
    res = ""
    with string as f:
        res = f.read()
    lines = toList(res)
    matched = match_line(lines, pattern)
    return matched


@hasArgument
def grep(stream: "Stream"):
    args = stream.getArgs()
    length = len(args)
    if length < 2:
        raise InvalidArgumentError("Invalid argument")
    pattern = args[0]
    if length == 2 and type(args[1]) == StringIO:
        res = processStdin(args[1], pattern)
    else:
        fileNames = args[1:]
        res = processFiles(fileNames, pattern)
    if not res.endswith("\n"):
        res += "\n"
    stdout = stream.getStdout()
    stdout.write(res)
