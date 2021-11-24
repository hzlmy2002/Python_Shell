from apps.App import App
from apps.CanStdIn import CanStdIn
from .Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Sort(CanStdIn):
    def getStream(self) -> "Stream":
        return self.stream

    def processFiles(self) -> "Stream":
        return Stream(
            sType=streamType.output,
            app="",
            params={},
            env={},
        )

    def appOperations(self):
        
        return self.fileStdinExec()


class SortUnsafe(Sort):
    def exec(self, stream: "Stream") -> "Stream":
        c = Sort()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
