from typing import List, Dict
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import hasArgument
from .Stream import *
from io import StringIO

@hasArgument
def cat(stream: "Stream"):
    fileNames = stream.getArgs()
    stdout = stream.getStdout()
    for file in fileNames:
        try:
            if type(file) == StringIO:
                with file as f:
                    stdout.write(f.read())
            else:
                with open(file, "r") as f:
                    stdout.write(f.read())
        except FileNotFoundError:
            raise InvalidFileOrDir(f"File {file} does not exist")
