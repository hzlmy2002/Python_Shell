from apps.App import App
from Stream import *
from standardStreamExceptions import *
from types import MethodType
import apps.tools


class Echo(App):
    def __init__(self) -> None:
        self.exceptions = standardStreamExceptions("Echo")

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
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
