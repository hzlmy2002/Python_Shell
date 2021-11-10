from Stream import Stream
from abc import ABC, abstractmethod
from typing import List, Dict


class App(ABC):
    @abstractmethod
    def __init__(self, stream: "Stream") -> None:
        pass

    @abstractmethod
    def getStream(self) -> "Stream":
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def exec(self) -> "Stream":
        # exec should return an output stream
        raise NotImplementedError("Please Implement this method")
