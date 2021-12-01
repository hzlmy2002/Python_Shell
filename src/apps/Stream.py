from typing import Dict, List, TextIO


class Stream:
    def __init__(self, env: Dict[str, str], stdout):
        self.args: List[str] = []
        self.env = env
        self.stdin = None
        self.stdout = stdout

    def addArg(self, arg: str) -> None:
        self.args.append(arg)

    def getArgs(self) -> List[str]:
        return self.args[:]

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

    def clearStdin(self) -> None:
        self.stdin = None
