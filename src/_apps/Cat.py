from .App import App
from typing import List, Dict
from .Stream import *
from .CanStdIn import CanStdIn
from . import tools
from types import MethodType
import os
from .standardStreamExceptions import *


class Cat(CanStdIn):
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
        return self.stream


class CatUnsafe(Cat):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cat()
        c.exec = MethodType(tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
