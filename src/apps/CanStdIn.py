from apps.App import App
from Stream import *
from standardStreamExceptions import exceptionType
import apps.tools
from abc import abstractmethod


class CanStdIn(App):
    def __init__(self) -> None:
        self.exceptions = None
        self.args = None

    def processStdin(self):
        if len(self.args) != 1:
            self.exceptions.raiseException(exceptionType.stdin)

        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[apps.tools.stdin2str(self.args[0])],
            env={},
        )

    @abstractmethod
    def processFiles(self) -> "Stream":
        raise NotImplementedError("Please Implement this method")

    def fileStdinExec(self):
        if apps.tools.isStdin(self.args[-1]):
            return self.processStdin()
        else:
            return self.processFiles()
