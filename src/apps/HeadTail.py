from apps.App import App
from apps.CanStdIn import CanStdIn
from apps.standardStreamExceptions import exceptionType, stdStreamExceptions
from Stream import *
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

    def processStream(self) -> int:
        if len(self.args) == 1:
            self.exceptions.lenCheck(self.param, exceptionType.paramNum, empty=True)
            self.num_lines = 10
        elif len(self.args) == 2:
            self.exceptions.lenCheck(self.param, exceptionType.paramNum, equalOne=True)
            if self.param[0] != "-n":
                self.exceptions.raiseException(exceptionType.paramType)
            self.num_lines = int(self.args[0])
        else:
            self.exceptions.raiseException(exceptionType.argNum)

    def processFiles(self):
        file = self.args[-1]
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
            params=[],
            args=output,
            env={},
        )

    def appOperations(self) -> "Stream":
        self.processStream()
        return self.fileStdinExec()
