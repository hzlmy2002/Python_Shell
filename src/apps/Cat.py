from typing import List, Dict
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import hasArgument
from .Stream import *


@hasArgument
def cat(stream: "Stream"):
    fileNames = stream.getArgs()
    stdout = stream.getStdout()
    for file in fileNames:
        try:
            with open(file, "r") as f:
                stdout.write(f.read())
        except FileNotFoundError:
            raise InvalidFileOrDir(f"File {file} does not exist")
