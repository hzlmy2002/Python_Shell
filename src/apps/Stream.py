from typing import Dict, List, TextIO


class Stream:
    def __init__(self, env: Dict[str, str], stdout):
        self.args: List[str] = []
        self.params = {}
        self.flags = []
        self.env = env
        self.stdin = None
        self.stdout = stdout

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

    def addToEnv(self, key: str, val: str) -> None:
        self.env[key] = val

    def getEnv(self, key: str) -> str:
        return self.env[key]

    def setStdin(self, stdin) -> None:
        self.stdin = stdin

    def getStdin(self):
        return self.stdin

    def setStdout(self, stdout) -> None:
        self.stdout = stdout

    def getStdout(self):
        return self.stdout

    def clearArgs(self) -> None:
        self.args = []

    def clearParams(self) -> None:
        self.params = {}

    def clearStdin(self) -> None:
        self.stdin = None

    def clearFlags(self) -> None:
        self.flags = []
