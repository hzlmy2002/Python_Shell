from apps.stream import Stream
from apps.exceptions import InvalidArgumentError, InvalidFileOrDir
from typing import List


def toList(newLineString: str) -> List[str]:
    res = [x + "\n" for x in newLineString.split("\n")]
    if res[-1] == "\n":
        res.pop()
    return res


def getLines(stream: "Stream") -> List[str]:
    # return content within a single file of name fileName as list of strings
    args = stream.getArgs()
    if len(args) != 1 or args[0] == "":
        raise InvalidArgumentError("Too many arguments given")
    fileName = args[0]
    try:
        with open(fileName, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise InvalidFileOrDir(f"File {fileName} does not exist")
    return lines
