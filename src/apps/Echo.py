from apps.App import App
from Stream import *
from standardStreamExceptions import *
from types import MethodType
import apps.tools
from standardStreamExceptions import standardStreamExceptions


class Echo(App):
    def __init__(self) -> None:
        self.exceptions = standardStreamExceptions("Echo")

    def getStream(self) -> "Stream":
        return self.stream

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
        self.exceptions.notNoneCheck(stream)
        self.exceptions.argsLenCheck(self.stream.getArgs(), notEmpty=True)
        self.exceptions.paramsLenCheck(self.stream.getParams(), empty=True)
        output = " ".join(self.stream.getArgs()) + "\n"
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
