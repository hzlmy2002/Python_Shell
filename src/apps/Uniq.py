from apps.App import App
from apps.CanStdIn import CanStdIn
from Stream import *

from types import MethodType
import apps.tools
import os
from standardStreamExceptions import *


class Uniq(CanStdIn):
    def exec(self, stream):
        self.initExec(stream)

        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[],
            env={},
        )


class UniqUnsafe(Uniq):
    def exec(self, stream: "Stream") -> "Stream":
        c = Uniq()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
