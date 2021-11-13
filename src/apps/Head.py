from apps.HeadTail import HeadTail
from standardStreamExceptions import *
import apps.tools
from types import MethodType


class Head(HeadTail):
    def __init__(self) -> None:
        super().__init__()
        self.exceptions = stdStreamExceptions("Head")

    def file_op(self, lines):
        output = ""
        for i in range(0, min(len(lines), self.num_lines)):
            output += lines[i]
        return [output]


class HeadUnsafe(Head):
    def exec(self, stream: "Stream") -> "Stream":
        c = Head()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
