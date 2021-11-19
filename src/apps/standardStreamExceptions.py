from typing import List
from enum import Enum


class exceptionType(Enum):
    argNum = "arguments"
    paramNum = "parameters"
    paramType = "parameterType"
    file = "file"
    dir = "directory"
    stdin = "stdin"
    none = "none"


class stdExceptionMessage:
    def __init__(self) -> None:
        self.message = {
            exceptionType.none: "No stream to process",
            exceptionType.file: "File not found",
            exceptionType.stdin: "Ilegal stdin",
            exceptionType.argNum: "Invalid number of command line arguments",
            exceptionType.paramNum: "Invalid number of command line parameters",
            exceptionType.paramType: "Invalid parameter type",
            exceptionType.dir: "Invalid Directory",
        }

    def exceptionMsg(self, type: "exceptionType"):
        return self.message[type]


class stdStreamExceptions:
    def __init__(self, appname) -> None:
        self.appname = appname
        self.stdMsg = stdExceptionMessage()

    def raiseException(self, type: "exceptionType"):
        raise Exception(f"{self.appname}: {self.stdMsg.exceptionMsg(type)}")

    def notNoneCheck(self, stream):
        if stream == None:
            self.raiseException(exceptionType.none)

    def lenCheck(
        self,
        checkList: "List",
        type: "exceptionType",
        notEmpty=False,
        empty=False,
        equalOne=False,
        oneOrZero=False,
    ):
        length = len(checkList)
        if (
            (notEmpty and length == 0)
            or (empty and length != 0)
            or (equalOne and length != 1)
            or (oneOrZero and length > 1)
        ):
            self.raiseException(type)
