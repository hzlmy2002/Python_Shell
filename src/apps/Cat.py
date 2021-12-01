from typing import List, Dict
from unittest.case import TestCase

from apps.Exceptions import InvalidFileOrDir
from .Stream import *
from types import MethodType
import os


"""class Cat(CanStdIn):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.cat)

    def processFiles(self):
        output = []
        for arg in self.params["main"]:
            if os.path.exists(arg):
                with open(arg, "r") as f:
                    output.append(f.read())
            else:
                self.exceptions.raiseException(exceptionType.file)
        ouputStream = Stream(
            sType=streamType.output, app="", params={"main": ["".join(output)]}, env={}
        )
        return ouputStream

    def appOperations(self) -> "Stream":
        if tools.isStdin(self.params["main"][0]):
            if len(self.params["main"]) == 1:
                return self.processStdin()
            else:
                raise self.exceptions.raiseException(exceptionType.stdin)
        else:
            return self.processFiles()

    def getStream(self) -> "Stream":
        return self.stream"""


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
