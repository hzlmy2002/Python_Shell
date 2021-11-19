from apps.App import App
from typing import List, Dict
from Stream import *
from apps.CanStdIn import CanStdIn
import apps.tools
from types import MethodType
import os
from apps.standardStreamExceptions import *


class Cat(CanStdIn):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Cat")

    def processFiles(self):
        output = []
        for arg in self.args:
            if os.path.exists(arg):
                with open(arg, "r") as f:
                    output.append(f.read())
            else:
                self.exceptions.raiseException(exceptionType.file)
        ouputStream = Stream(
            sType=streamType.output, app="", params=[], args=["".join(output)], env={}
        )
        return ouputStream

    def appOperations(self) -> "Stream":
        self.exceptions.lenCheck(self.args, exceptionType.argNum, notEmpty=True)
        self.exceptions.lenCheck(self.param, exceptionType.paramNum, empty=True)
        if apps.tools.isStdin(self.args[0]):
            return self.processStdin()
        else:
            return self.processFiles()

    def getStream(self) -> "Stream":
        return self.stream


class CatUnsafe(Cat):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cat()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
