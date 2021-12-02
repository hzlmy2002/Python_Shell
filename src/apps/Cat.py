from typing import List, Dict
from apps.Exceptions import InvalidFileOrDir
from .Stream import *


def cat(stream: "Stream"):
    fileNames = stream.getArgs()
    if len(fileNames) == 0:  # no file specified
        fileNames = stream.getStdin()
    stdout = stream.getStdout()
    for file in fileNames:
        try:
            with open(file, "r") as f:
                stdout.write(f.read())
        except FileNotFoundError:
            raise InvalidFileOrDir(f"File {file} does not exist")
