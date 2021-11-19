from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Cd(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Cd")

    def getStream(self) -> "Stream":
        return self.stream

    def appOperations(self) -> "Stream":
        self.exceptions.lenCheck(self.args, exceptionType.argNum, equalOne=True)
        self.exceptions.lenCheck(self.param, exceptionType.paramNum, empty=True)
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
