from apps.HeadTail import HeadTail
from apps.standardStreamExceptions import *
import apps.tools
from types import MethodType


class Tail(HeadTail):
    def __init__(self) -> None:
        super().__init__()
        self.exceptions = stdStreamExceptions(appName.head)

    def fileOp(self, lines):
        output = ""
        display_length = min(len(lines), self.num_lines)
        for i in range(0, display_length):
            output += lines[len(lines) - display_length + i]
        return [output]


class TailUnsafe(Tail):
    def exec(self, stream: "Stream") -> "Stream":
        c = Tail()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
