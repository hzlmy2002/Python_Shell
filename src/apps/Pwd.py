from apps.App import App
import os
from types import MethodType
import apps.tools
from Stream import *
from apps.standardStreamExceptions import *


class Pwd(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.pwd)

    def getStream(self) -> "Stream":
        return self.stream

    def appOperations(self) -> "Stream":
        output = os.getcwd() + "\n"
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[output],
            env={},
        )


class PwdUnsafe(Pwd):
    def exec(self, stream: "Stream") -> "Stream":
        c = Pwd()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
