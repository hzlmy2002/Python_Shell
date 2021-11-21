from .App import App
from .Stream import *

from types import MethodType
from . import tools
import os
from .standardStreamExceptions import *


class Cd(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.cd)

    def getStream(self) -> "Stream":
        return self.stream

    def appOperations(self) -> "Stream":
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
        c.exec = MethodType(tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
