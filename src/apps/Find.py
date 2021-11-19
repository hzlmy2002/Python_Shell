from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Find(App):
    def exec(self, stream):
        self.initExec(stream)

        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[],
            env={},
        )


class FindUnsafe(Find):
    def exec(self, stream: "Stream") -> "Stream":
        c = Find()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
