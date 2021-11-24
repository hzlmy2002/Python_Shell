from apps.CanStdIn import CanStdIn
from .Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Sort(CanStdIn):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.sort)

    def getStream(self) -> "Stream":
        return self.stream

    def fixNewLine(self, li):
        for i in range(len(li) - 1):
            if not li[i].endswith("\n"):
                li[i] = li[i] + "\n"

    def processFiles(self) -> "Stream":
        fileName = self.params["main"][0]
        if not os.path.isfile(fileName):
            self.exceptions.raiseException(exceptionType.file)
        content = []
        with open(fileName, "r") as f:
            content = f.readlines()
            content.sort(reverse=self.doReverse)
        self.fixNewLine(content)
        return Stream(
            sType=streamType.output,
            app="",
            params={"main": ["".join(content)]},
            env={},
        )

    def appOperations(self):
        self.doReverse = "r" in self.params
        if len(self.params) == 2 and not self.doReverse:
            self.exceptions.raiseException(exceptionType.paramType)
        return self.fileStdinExec()


class SortUnsafe(Sort):
    def exec(self, stream: "Stream") -> "Stream":
        c = Sort()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
