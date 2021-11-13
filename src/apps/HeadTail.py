from apps.App import App
from standardStreamExceptions import exceptionType, stdStreamExceptions
from Stream import *


class HeadTail(App):
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

    def file_op(self, lines):
        """Requires implementation of child class"""
        raise NotImplementedError("Please Implement this method")

    def initExec(self, stream):
        self.exceptions.notNoneCheck(stream)
        self.stream = stream
        self.args = self.stream.getArgs()
        self.params = self.stream.getParams()

    def process_stream(self) -> int:
        if len(self.args) == 1:
            self.exceptions.lenCheck(self.params, exceptionType.paramNum, empty=True)
            self.num_lines = 10
        elif len(self.args) == 2:
            self.exceptions.lenCheck(self.params, exceptionType.paramNum, equalOne=True)
            if self.params[0] != "-n":
                self.exceptions.raiseException(exceptionType.paramType)
            self.num_lines = int(self.args[0])
        else:
            self.exceptions.raiseException(exceptionType.argNum)

    def processFile(self):
        file = self.args[-1]
        output = []
        try:
            with open(file) as f:
                lines = f.readlines()
                output = self.file_op(lines)
        except:
            self.exceptions.raiseException(exceptionType.file)
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=output,
            env={},
        )

    def exec(self, stream: "Stream") -> "Stream":
        self.initExec(stream)
        self.process_stream()
        return self.processFile()
