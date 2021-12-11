from apps.Stream import Stream
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from typing import List
from io import StringIO
from apps.decorators import hasArgument


def toList(newLineString: str) -> List[str]:

    res = [x + "\n" for x in newLineString.split("\n")]
    if res[-1] == "\n":
        res.pop()
    return res


def getLines(stream: "Stream") -> List[str]:
    # Return content within a single file of name fileName as list of string
    args = stream.getArgs()
    fileName = args[-1]
    lines = ""
    try:
        if type(fileName) == StringIO:
            with fileName as f:
                lines = f.getvalue()
                lines = toList(lines)
        else:
            with open(fileName, "r") as f:
                lines = f.readlines()
    except FileNotFoundError:
        raise InvalidFileOrDir(f"File {fileName} does not exist")
    return lines
