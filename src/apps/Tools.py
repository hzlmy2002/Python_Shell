from apps.Stream import Stream
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from typing import List


def getLines(stream: "Stream") -> List:
    args = stream.getArgs()
    if len(args) == 0:  # no file specified
        lines = stream.getStdin()
        if lines is None:
            raise InvalidArgumentError("Argument is invalid")
    else:
        fileName = args[-1]
        try:
            with open(fileName, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise InvalidFileOrDir(f"File {fileName} does not exist")
    return lines
