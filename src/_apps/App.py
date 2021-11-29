from abc import ABC, abstractmethod
from typing import List, Dict
from .standardStreamExceptions import *
from .Stream import *


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
        self.params = self.stream.getParams()
        self.exceptions.paramsLenCheck(self.params.keys())
        self.exceptions.mainArgsLenCheck(self.params["main"])
        self.exceptions.tagArgsLenCheck(
            dict(filter(lambda x: x[0] != "main", self.params.items())).values()
        )
