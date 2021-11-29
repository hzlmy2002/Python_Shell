from typing import Dict, List, TextIO


class StdInNotFound(RuntimeError):
    pass


class Stream:
    def __init__(self, env: Dict[str, str]):
        self.args: List[str] = []
        self.env = env
        self.stdin: TextIO = None
        self.stdout: TextIO = None

    def addArg(self, arg: str) -> None:
        self.args.append(arg)

    def getArgs(self) -> List[str]:
        return self.args[:]

    def addToEnv(self, key: str, val: str) -> None:
        self.env[key] = val

    def getEnv(self, key: str) -> str:
        return self.env[key]

    def setStdIn(self, path: str) -> None:
        try:
            self.stdin = open(path, "r")
        except FileNotFoundError:
            raise StdInNotFound("stdin not found.")

    def getStdIn(self) -> TextIO:
        return self.stdin

    def setStdOut(self, path: str) -> None:
        self.stdout = open(path, "w")

    def getStdOut(self) -> TextIO:
        return self.stdout

    def clear(self) -> None:
        self.args = []
        self.stdin = None
        self.stdout = None
