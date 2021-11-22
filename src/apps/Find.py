from apps.App import App
from .Stream import *

from types import MethodType
import apps.tools
import os
import fnmatch
from apps.standardStreamExceptions import *


class Find(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.find)
        self.invalidPattern = ["\\", "/", "?", '"', "<", ">", "|"]

    def getStream(self) -> "Stream":
        return self.stream

    def isInvalidPattern(self, pattern):
        return any(char in self.invalidPattern for char in pattern)

    def findFiles(self):
        result = ""
        for root, _, files in os.walk(self.rootPath):
            for fName in files:
                if fnmatch.fnmatch(fName, self.pattern):
                    result += root + os.sep + fName + "\n"
        return result

    def checkExcept(self):
        if "pattern" not in self.params:
            self.exceptions.raiseException(exceptionType.paramType)

        if self.isInvalidPattern(self.params["pattern"][0]):
            self.exceptions.raiseException(exceptionType.pattern)

        rootPath = self.params["main"][0]
        if rootPath != "":
            if not (os.path.exists(rootPath) and os.path.isdir(rootPath)):
                self.exceptions.raiseException(exceptionType.dir)

    def appOperations(self):
        self.checkExcept()
        self.rootPath = self.params["main"][0]
        self.pattern = self.params["pattern"][0]
        relativePaths = self.findFiles()
        return Stream(
            sType=streamType.output,
            app="",
            params={"main": [relativePaths]},
            env={},
        )


class FindUnsafe(Find):
    def exec(self, stream: "Stream") -> "Stream":
        c = Find()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
