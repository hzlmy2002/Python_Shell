from apps.App import App
from apps.CanStdIn import CanStdIn
from .Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Uniq(CanStdIn):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.uniq)

    def getStream(self) -> "Stream":
        return self.stream

    def processFiles(self) -> "Stream":
        fileName = self.params["main"][0]
        if not os.path.isfile(fileName):
            self.exceptions.raiseException(exceptionType.file)
        res = ""
        last = ""
        with open(fileName, "r") as f:
            content = f.readlines()
            for i in range(0, len(content)):
                line = content[i]
                compLine = line
                if self.caseSensitive:
                    compLine = compLine.upper()
                if not compLine == last:
                    last = compLine
                    res += line

        return Stream(
            sType=streamType.output,
            app="",
            params={"main": [res]},
            env={},
        )

    def appOperations(self):
        self.caseSensitive = "i" in self.params
        if len(self.params) == 2 and not self.caseSensitive:
            self.exceptions.raiseException(exceptionType.paramType)
        return self.fileStdinExec()


class UniqUnsafe(Uniq):
    def exec(self, stream: "Stream") -> "Stream":
        c = Uniq()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
