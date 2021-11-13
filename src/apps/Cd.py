from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from standardStreamExceptions import *


class Cd(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Cd")

    def getStream(self) -> "Stream":
        return self.stream

    def initAndCheckStream(self, stream):
        self.stream = stream
        self.exceptions.notNoneCheck(stream)
        self.args = self.stream.getArgs()
        self.exceptions.lenCheck(self.args, exceptionType.argNum, equalOne=True)
        self.exceptions.lenCheck(
            self.stream.getParams(), exceptionType.paramNum, empty=True
        )

    def exec(self, stream: "Stream") -> "Stream":
        self.initAndCheckStream(stream)
        try:
            os.chdir(self.args[0])
        except:
            self.exceptions.raiseException(exceptionType.dir)
        new_env = self.stream.getEnv()
        new_env["working_dir"] = os.getcwd()
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[],
            env=new_env,
        )


class CdUnsafe(Cd):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cd()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
