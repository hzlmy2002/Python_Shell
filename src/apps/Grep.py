from io import StringIO
from apps.Stream import Stream
from apps.Tools import toList
from apps.decorators import hasArgument
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
import re
from typing import List


def match_line(lines: "List[str]", pattern: str, multFiles=False, fileName=""):
    """Finds matching pattern given by args returns matched lines"""
    res = ""
    for line in lines:
        if re.match(pattern, line):
            toAdd = ""
            if multFiles:
                toAdd = f"{fileName}:{line}"
            else:
                toAdd = line
            if not toAdd.endswith("\n"):
                toAdd += "\n"
            res += toAdd
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
        res = f.getvalue()
    lines = toList(res)
    matched = match_line(lines, pattern)
    return matched


@hasArgument
def grep(stream: "Stream"):
    args = stream.getArgs()
    length = len(args)
    pattern = args[0]
    if length == 1:
        stdin = stream.getStdin()
        if type(stdin) == StringIO:
            res = processStdin(stdin, pattern)
    else:
        fileNames = args[1:]
        res = processFiles(fileNames, pattern)
    stdout = stream.getStdout()
    stdout.write(res)
