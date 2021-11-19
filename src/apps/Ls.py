from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Ls(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Ls")

    def getStream(self) -> "Stream":
        return self.stream

    def listDirectory(self, ls_dir):
        # Returns a list containing a single string of directories that are followed by \n
        dirs = []
        try:
            for file in os.listdir(ls_dir):
                if not file.startswith("."):
                    dirs.append(file + "\n")
        except:
            self.exceptions.raiseException(exceptionType.dir)
        return ["".join(dirs)]

    def appOperations(self) -> "Stream":
        self.exceptions.lenCheck(self.args, exceptionType.argNum, oneOrZero=True)
        self.exceptions.lenCheck(self.param, exceptionType.paramNum, empty=True)
        if not self.args:
            ls_dir = os.getcwd()
        else:
            ls_dir = self.args[0]
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=self.listDirectory(ls_dir),
            env={},
        )


class LsUnsafe(Ls):
    def exec(self, stream: "Stream") -> "Stream":
        c = Ls()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
