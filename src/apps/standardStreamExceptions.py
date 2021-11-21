from typing import List
from enum import Enum


class exceptionType(Enum):
    argNum = "arguments"
    tagNum = "tags"
    paramNum = "parameters"
    paramType = "parameterType"
    file = "file"
    dir = "directory"
    stdin = "stdin"
    none = "none"


class appName(Enum):
    cat = "Cat"
    cd = "Cd"
    cut = "Cut"
    echo = "Echo"
    find = "Find"
    grep = "Grep"
    head = "Head"
    ls = "Ls"
    pwd = "Pwd"
    sort = "Sort"
    tail = "Tail"
    uniq = "Uniq"


inputLengthRestrict = Enum(
    # Restrictions on length that the input list could take
    "inputLengthRestrict",
    ["NotEmpty", "Empty", "EqualsOne", "EqualsTwo", "OneOrZero", "OneOrTwo"],
)


class stdExceptionMessage:
    def __init__(self) -> None:
        self.message = {
            exceptionType.none: "No stream to process",
            exceptionType.file: "File not found",
            exceptionType.stdin: "Ilegal stdin",
            exceptionType.argNum: "Invalid number of command line arguments",
            exceptionType.tagNum: "Invalid number of command line tags",
            exceptionType.paramNum: "Invalid number of command line parameters",
            exceptionType.paramType: "Invalid parameter type",
            exceptionType.dir: "Invalid Directory",
        }

    def exceptionMsg(self, type: "exceptionType"):
        return self.message[type]


class stdStreamExceptions:
    def __init__(self, appname: "appName") -> None:
        self.appname = appname
        """[main args length restriction,params length restriction,tags length restriction]"""
        self.lenRestrictMap = {
            appName.cat: [
                inputLengthRestrict.NotEmpty,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.Empty,
            ],
            appName.cd: [
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.Empty,
            ],
            appName.cut: [],
            appName.echo: [
                inputLengthRestrict.NotEmpty,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.Empty,
            ],
            appName.find: [
                inputLengthRestrict.OneOrZero,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.EqualsOne,
            ],
            appName.grep: [
                inputLengthRestrict.NotEmpty,
                inputLengthRestrict.EqualsTwo,
                inputLengthRestrict.EqualsOne,
            ],
            appName.head: [
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.OneOrTwo,
                inputLengthRestrict.OneOrZero,
            ],
            appName.ls: [
                inputLengthRestrict.OneOrZero,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.Empty,
            ],
            appName.pwd: [
                inputLengthRestrict.Empty,
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.Empty,
            ],
            appName.sort: [],
            appName.tail: [
                inputLengthRestrict.EqualsOne,
                inputLengthRestrict.OneOrTwo,
                inputLengthRestrict.OneOrZero,
            ],
            appName.uniq: [],
        }
        self.stdMsg = stdExceptionMessage()
        self.argLenRestrict = self.lenRestrictMap[self.appname][0]
        self.paramLenRestrict = self.lenRestrictMap[self.appname][1]
        self.tagLenRestrict = self.lenRestrictMap[self.appname][2]

    def raiseException(self, type: "exceptionType"):
        raise Exception(f"{self.appname.value}: {self.stdMsg.exceptionMsg(type)}")

    def notNoneCheck(self, stream):
        if stream == None:
            self.raiseException(exceptionType.none)

    def lenCheck(
        self,
        listLength,
        restrictLengthType: "inputLengthRestrict",
        type: "exceptionType",
    ):
        if (
            (restrictLengthType == inputLengthRestrict.NotEmpty and listLength == 0)
            or (restrictLengthType == inputLengthRestrict.Empty and listLength != 0)
            or (restrictLengthType == inputLengthRestrict.EqualsOne and listLength != 1)
            or (restrictLengthType == inputLengthRestrict.OneOrZero and listLength > 1)
            or (
                restrictLengthType == inputLengthRestrict.OneOrTwo
                and (listLength > 2 or listLength == 0)
            )
            or (restrictLengthType == inputLengthRestrict.EqualsTwo and listLength != 2)
        ):
            self.raiseException(type)

    def mainArgsLenCheck(self, checkList: "List"):
        self.lenCheck(len(checkList), self.argLenRestrict, exceptionType.argNum)

    def tagArgsLenCheck(self, checkList: "List"):
        # Tags are arguments associated with an option (e.g. -n)
        # Ensures the length of number of tags passed
        self.lenCheck(
            sum(len(li) for li in checkList), self.tagLenRestrict, exceptionType.tagNum
        )

    def paramsLenCheck(self, checkList: "List"):
        self.lenCheck(len(checkList), self.paramLenRestrict, exceptionType.paramNum)
