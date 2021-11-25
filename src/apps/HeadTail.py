from apps.App import App
from apps.CanStdIn import CanStdIn
from apps.standardStreamExceptions import *
from .Stream import *
import apps.tools


class HeadTail(CanStdIn):
    """
    STREAM:
    app = head/tail
    param = [] / ["-n"]
    args = [FILENAME] / [num_line,FILENAME] if -n specified in param"""

    def __init__(self):
        self.num_lines = None
        self.exceptions = None

    def getStream(self) -> "Stream":
        return self.stream

    def fileOp(self, lines):
        """Requires implementation of child class"""
        raise NotImplementedError("Please Implement this method")

    def processFiles(self):
        file = self.params["main"][-1]
        output = []
        try:
            with open(file) as f:
                lines = f.readlines()
                output = self.fileOp(lines)
        except:
            self.exceptions.raiseException(exceptionType.file)
        return Stream(
            sType=streamType.output,
            app="",
            params={"main": output},
            env={},
        )

    def appOperations(self) -> "Stream":
        if len(self.params) == 2 and "n" not in self.params:
            self.exceptions.raiseException(exceptionType.paramType)
        if "n" not in self.params:
            self.num_lines = 10
        elif len(self.params["n"]) == 1:
            self.num_lines = int(self.params["n"][0])
        return self.fileStdinExec()
