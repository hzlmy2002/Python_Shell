from apps.CanStdIn import CanStdIn
from Stream import *

from types import MethodType
import apps.tools
import os
from standardStreamExceptions import *


class Cut(CanStdIn):
    def appOperations(self):

        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[],
            env={},
        )


class CutUnsafe(Cut):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cut()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
