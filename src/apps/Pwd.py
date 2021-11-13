from apps.App import App
import os
from types import MethodType
import apps.tools
from Stream import *
from standardStreamExceptions import *


class Pwd(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Pwd")

    def getStream(self) -> "Stream":
        return self.stream

    def exec(self, stream: "Stream") -> "Stream":
        self.exceptions.notNoneCheck(stream)
        self.stream = stream
        self.exceptions.lenCheck(
            self.stream.getArgs(), exceptionType.argNum, empty=True
        )
        self.exceptions.lenCheck(
            self.stream.getParams(), exceptionType.paramNum, empty=True
        )
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
