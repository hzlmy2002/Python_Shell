from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from standardStreamExceptions import standardStreamExceptions


class Ls(App):
    def __init__(self) -> None:
        self.exceptions = standardStreamExceptions("Cd")

    def getStream(self) -> "Stream":
        return self.stream

    def listDirectory(self, ls_dir):
        dirs = []
        for file in os.listdir(ls_dir):
            if not file.startswith("."):
                dirs.append(file + "\n")
        return dirs

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
        self.exceptions.notNoneCheck()
        self.exceptions.argsLenCheck(self.stream.getArgs(), oneOrZero=True)
        self.exceptions.paramsLenCheck(self.stream.getParams, empty=True)
        if not self.args:
            ls_dir = os.getcwd()
        else:
            ls_dir = self.args[0]
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[ls_dir],
            env={},
        )

    """def exec(self):
        if len(self.args) == 0:
            ls_dir = os.getcwd()
        elif len(self.args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = self.args[0]
        self.list_directory(ls_dir)
        return self.output"""


class LsUnsafe(Cd):
    def exec(self, stream: "Stream") -> "Stream":
        c = Ls()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
