from apps.App import App
import re
from Stream import *
from apps.CanStdIn import CanStdIn
from standardStreamExceptions import *
from types import MethodType
import apps.tools


class Grep(CanStdIn):
    """
    STREAM:
    app = grep
    param = [REGEX]
    args = [FILENAME, FILNAME2....]  stores the file names specified"""

    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions()

    def getStream(self) -> "Stream":
        return self.stream

    def initExec(self, stream):
        self.exceptions.notNoneCheck(stream)
        self.stream = stream
        self.args = self.stream.getArgs()
        self.param = self.stream.getParams()
        self.matched = ""

    def checkStream(self):
        self.exceptions.lenCheck(self.args, exceptionType.argNum, notEmpty=True)
        self.exceptions.lenCheck(self.param, exceptionType.paramNum, equalOne=True)

    def match_line(self, filename, pattern):
        """Finds matching pattern given by args returns matched lines"""
        try:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    if re.match(pattern, line):
                        if len(self.args) > 1:
                            self.matched += f"{filename}:{line}"
                        else:
                            self.matched += line
        except:
            self.exceptions.raiseException(exceptionType.file)

    def processFiles(self):
        pattern = self.param[0]
        for filename in self.args:
            self.match_line(filename, pattern)
        if not self.matched.endswith("\n"):
            self.matched += "\n"
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[self.matched],
            env={},
        )

    def exec(self, stream: "Stream") -> "Stream":
        self.initExec(stream)
        self.checkStream()
        return self.fileStdinExec()

    """def exec(self):
        self.outputs = []
        print(self.args)
        if len(self.args) < 2:
            raise ValueError("wrong number of command line arguments")
        pattern = self.args[0]
        files = self.args[1:]
        filelen = len(files)
        for filename in files:
            self.match_line(filename, filelen, pattern)
        print(self.outputs)
        return self.outputs"""


class GrepUnsafe(Grep):
    def exec(self, stream: "Stream") -> "Stream":
        c = Grep()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
