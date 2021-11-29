from .App import App
from .Stream import *
from .standardStreamExceptions import exceptionType
from . import tools
from abc import abstractmethod


class CanStdIn(App):
    def __init__(self) -> None:
        pass

    def processStdin(self):
        if len(self.params["main"]) != 1:
            self.exceptions.raiseException(exceptionType.stdin)

        return Stream(
            sType=streamType.output,
            app="",
            params={"main": [tools.stdin2str(self.params["main"][-1])]},
            env={},
        )

    @abstractmethod
    def processFiles(self) -> "Stream":
        # Specify method of processing argument of file/files, returns the result in Stream format
        raise NotImplementedError("Please Implement this method")

    def fileStdinExec(self):
        if tools.isStdin(self.params["main"][0]):
            if len(self.params["main"])==1:
                return self.processStdin()
            else:
                raise self.exceptions.raiseException(exceptionType.stdin)
        else:
            return self.processFiles()
