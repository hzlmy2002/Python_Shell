from apps.stream import Stream
from apps.decorators import notEmpty
from apps.exceptions import InvalidFileOrDir, MissingStdin
import re
from typing import List, TextIO


def match_line(lines: List[str], pattern: str, multFiles=False, fileName=""):
    # finds matching pattern given by args returns matched lines
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


def processFiles(fileNames: List[str], pattern: str) -> str:
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


def processStdin(stdin: TextIO, pattern: str) -> str:
    lines = stdin.readlines()
    matched = match_line(lines, pattern)
    return matched


@notEmpty
def grep(stream: "Stream"):
    args = stream.getArgs()
    length = len(args)
    pattern = args[0]
    if length == 1:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        res = processStdin(stdin, pattern)
    else:
        fileNames = args[1:]
        res = processFiles(fileNames, pattern)
    stdout = stream.getStdout()
    stdout.write(res)
