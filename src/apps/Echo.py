from apps.App import App
from Stream import *
from apps.standardStreamExceptions import *
from types import MethodType
import apps.tools


class Echo(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions("Echo")

    def getStream(self) -> "Stream":
        return self.stream

    def appOperations(self) -> "Stream":
        self.exceptions.lenCheck(self.args, exceptionType.argNum, notEmpty=True)
        self.exceptions.lenCheck(self.param, exceptionType.paramNum, empty=True)
        output = " ".join(self.args) + "\n"
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[output],
            env={},
        )


class EchoUnsafe(Echo):
    def exec(self, stream: "Stream") -> "Stream":
        c = Echo()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
