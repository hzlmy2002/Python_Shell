from typing import List, TextIO


class Stream:
    def __init__(self, workingDir: str):
        self.workingDir = workingDir
        self.stdout: TextIO = None
        self.stdin: TextIO = None

        self.args: List[str] = []
        self.params = {}
        self.flags: List[str] = []

    def addArg(self, arg: str) -> None:
        self.args.append(arg)

    def getArgs(self) -> List[str]:
        return self.args[:]

    def removeArg(self, index: int) -> None:
        self.args.pop(index)

    def addParam(self, key: str, val) -> None:
        self.params[key] = val

    def getParam(self, key: str) -> str:
        return self.params[key]

    def addFlag(self, flag: str) -> None:
        self.flags.append(flag)

    def getFlag(self, flag: str) -> bool:
        return flag in self.flags

    def getStdout(self) -> TextIO:
        return self.stdout

    def setStdout(self, stdout: TextIO) -> None:
        self.stdout = stdout

    def getStdin(self) -> TextIO:
        return self.stdin

    def setStdin(self, stdin: TextIO) -> None:
        self.stdin = stdin

    def setWorkingDir(self, workingDir: str) -> None:
        self.workingDir = workingDir

    def getWorkingDir(self) -> str:
        return self.workingDir

    def clearArgs(self) -> None:
        self.args.clear()

    def clearParams(self) -> None:
        self.params.clear()

    def clearFlags(self) -> None:
        self.flags.clear()

    def clearStdin(self) -> None:
        self.stdin = None

    def reset(self) -> None:
        self.clearArgs()
        self.clearParams()
        self.clearFlags()
        self.clearStdin()
