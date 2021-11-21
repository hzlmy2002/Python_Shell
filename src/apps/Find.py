from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Find(App):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.find)

    def matchFileName(self):
        pass

    def findFiles(self, root):
        # Returns string of the relative path to the root of the specified file pattern
        pass

    def appOperations(self):
        rootPath = self.args[0]
        self.pattern = self.param[0]
        relativePaths = self.findFiles(rootPath)
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[relativePaths],
            env={},
        )


class FindUnsafe(Find):
    def exec(self, stream: "Stream") -> "Stream":
        c = Find()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
