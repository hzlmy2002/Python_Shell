from Stream import Stream
from abc import ABC, abstractmethod
from typing import List, Dict
from apps.standardStreamExceptions import *
from Stream import *


class App(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def getStream(self) -> "Stream":
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def appOperations(self):
        # appOperations carries out app specific operatoins and should return an output stream
        raise NotImplementedError("Please Implement this method")

    def exec(self, stream: "Stream") -> "Stream":
        # exec runs the initilization and return output of app operation
        self.initExec(stream)
        return self.appOperations()

    def initExec(self, stream):
        self.exceptions.notNoneCheck(stream)
        self.stream = stream
        self.args = self.stream.getArgs()
        self.param = self.stream.getParams()
        self.exceptions.argsLenCheck(self.args)
        self.exceptions.paramsLenCheck(self.param)
