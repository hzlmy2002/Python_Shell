from Stream import Stream
from abc import ABC, abstractmethod
from typing import List, Dict
from standardStreamExceptions import *
from Stream import *


class App(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def getStream(self) -> "Stream":
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def exec(self, stream: "Stream") -> "Stream":
        # exec should return an output stream
        raise NotImplementedError("Please Implement this method")

    def initExec(self, stream):
        self.exceptions.notNoneCheck(stream)
        self.stream = stream
        self.args = self.stream.getArgs()
        self.param = self.stream.getParams()
