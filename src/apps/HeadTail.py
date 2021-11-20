from apps.App import App
from apps.CanStdIn import CanStdIn
from apps.standardStreamExceptions import *
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
        if len(self.param) == 0:
            if len(self.args) != 1:
                self.exceptions.raiseException(exceptionType.argNum)
            self.num_lines = 10
        elif len(self.param) == 1:
            if self.param[0] != "-n":
                self.exceptions.raiseException(exceptionType.paramType)
            if len(self.args) != 2:
                self.exceptions.raiseException(exceptionType.argNum)
            self.num_lines = int(self.args[0])
        return self.fileStdinExec()
