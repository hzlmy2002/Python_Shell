from typing import Dict, List


class Stream:
    def __init__(self):
        self.args: List[str] = []
        self.env: Dict[str, str] = {}
        self.stdin: str = ""
        self.stdout: str = ""

    def addArg(self, arg: str) -> None:
        self.args.append(arg)

    def getArgs(self) -> List[str]:
        return self.args

    def addToEnv(self, key: str, val: str) -> None:
        self.env[key] = val

    def getEnv(self) -> Dict[str, str]:
        return self.env

    def setStdIn(self, path) -> None:
        # TODO throw error if stdin not found
        # TODO abstract stdin
        self.stdin = path

    def getStdIn(self) -> str:
        return self.stdin

    def setStdOut(self, path) -> None:
        # TODO throw error if stdout not found
        # TODO abstract stdout
        self.stdout = path

    def getStdOut(self) -> str:
        return self.stdout
