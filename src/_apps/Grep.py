from apps.App import App
import re
from .Stream import *
from apps.CanStdIn import CanStdIn
from apps.standardStreamExceptions import *
from types import MethodType
import apps.tools


class Grep(CanStdIn):
    """
    STREAM:
    app = grep
    param = [REGEX]
    args = [FILENAME, FILNAME2....]  stores the file names specified"""

    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.grep)

    def getStream(self) -> "Stream":
        return self.stream

    def match_line(self, filename, pattern):
        """Finds matching pattern given by args returns matched lines"""
        try:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    if re.match(pattern, line):
                        if len(self.params["main"]) > 1:
                            self.matched += f"{filename}:{line}"
                        else:
                            self.matched += line
        except FileNotFoundError:
            self.exceptions.raiseException(exceptionType.file)

    def processFiles(self):
        pattern = self.params["pattern"][0]
        for filename in self.params["main"]:
            self.match_line(filename, pattern)
        if not self.matched.endswith("\n"):
            self.matched += "\n"
        return Stream(
            sType=streamType.output,
            app="",
            params={"main": [self.matched]},
            env={},
        )

    def appOperations(self) -> "Stream":
        self.matched = ""
        return self.fileStdinExec()


class GrepUnsafe(Grep):
    def exec(self, stream: "Stream") -> "Stream":
        c = Grep()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
