from apps.CanStdIn import CanStdIn
from .Stream import *
from types import MethodType
import apps.tools
import os
from apps.standardStreamExceptions import *


class Cut(CanStdIn):
    def __init__(self) -> None:
        self.exceptions = stdStreamExceptions(appName.cut)

    def getStream(self) -> "Stream":
        return self.stream

    def checkDigit(self, n):
        return n.isdigit() and int(n) >= 1

    def parseTags(self, param) -> "List":
        res = param.split("-")
        if len(res) == 1:
            if self.checkDigit(res[0]):
                # Single positioned (e.g. 2)
                index = int(res[0])
                return [index - 1, index]
        elif len(res) == 2:
            if all(self.checkDigit(element) for element in res):
                # Has a start and end (e.g. 1-4)
                li = [int(res[0]) - 1, int(res[1])]
                if li[1] < li[0]:
                    self.exceptions.raiseException(exceptionType.decRange)
                return li

            if self.checkDigit(res[0]) and res[1] == "":
                # No end (e.g. 5-)
                return [int(res[0]) - 1, -1]

            if self.checkDigit(res[1]) and res[0] == "":
                # No start (e.g. -5)
                return [0, int(res[1])]

        self.exceptions.raiseException(exceptionType.tagType)

    def readBytesOfLine(self, byterange, line):
        if len(byterange) == 1:
            return line[byterange[0]]
        start = byterange[0]
        end = byterange[1]
        if end == -1:
            end = len(line)
        return "".join(line[start:end])

    def isBiggerEqual(self, x, y):
        # make -1 act like inf
        if x == -1:
            return True
        return x >= y

    def fixByteRanges(self, byteRanges):
        # Fix duplicates and byte ranges that includes others (e.g. 1-5 and 3, where 1-5 includes byte 3)
        bR = byteRanges.copy()
        bR.sort()
        res = [bR[0]]
        for ele in bR:
            if self.isBiggerEqual(res[-1][1], ele[0]):
                if ele[1] == -1 or res[-1][1] == -1:
                    res[-1][1] = -1
                else:
                    res[-1][1] = max(res[-1][1], ele[1])
            else:
                res.append([ele[0], ele[1]])
        return res

    def processFiles(self) -> "Stream":
        filePath = self.params["main"][0]
        if not os.path.isfile(filePath):
            self.exceptions.raiseException(exceptionType.file)
        tags = self.params["b"]
        byteRanges = self.fixByteRanges([self.parseTags(element) for element in tags])
        res = ""
        with open(filePath, "r") as f:
            lines = f.readlines()
            for line in lines:
                for byterange in byteRanges:
                    res += self.readBytesOfLine(byterange, line)
                if not res.endswith("\n"):
                    res += "\n"

        return Stream(
            sType=streamType.output,
            app="",
            params={"main": [res]},
            env={},
        )

    def appOperations(self):
        if "b" not in self.params:
            self.exceptions.raiseException(exceptionType.paramType)
        return self.fileStdinExec()


class CutUnsafe(Cut):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cut()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
