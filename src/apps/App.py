from Stream import Stream
from abc import ABC, abstractmethod
from typing import List, Dict


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
