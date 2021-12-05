from apps.Stream import Stream
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from typing import List

from apps.decorators import hasArgument


def getLines(stream: "Stream") -> List[str]:
    # Return content within a single file of name fileName as list of string
    args = stream.getArgs()
    fileName = args[-1]
    lines = ""
    try:
        with open(fileName, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise InvalidFileOrDir(f"File {fileName} does not exist")
    return lines
