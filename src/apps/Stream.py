from typing import Dict, List
from shellOutput import ShellOutput


class Stream:
    def __init__(self, env: Dict[str, str] = {}, stdout=None):
        self.args: List[str] = []
        self.params = {}
        self.flags = []
        self.env = (
            env.copy()
        )  # variable starts with _ is for internal use only,
        # hide from the user
        self.stdout: "ShellOutput" = stdout

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
        return self.env[key] if key in self.env else ""

    def getStdout(self) -> "ShellOutput":
        return self.stdout

    def alterStdout(self, stdout: "ShellOutput") -> None:
        self.stdout = stdout

    def clearArgs(self) -> None:
        self.args.clear()

    def clearParams(self) -> None:
        self.params.clear()

    def clearStdin(self) -> None:
        self.stdin = None

    def clearFlags(self) -> None:
        self.flags.clear()

    def reset(self) -> None:
        self.clearArgs()
        self.clearParams()
        self.clearStdin()
        self.clearFlags()
        for key in list(self.env.keys()):
            if key.startswith("_"):  # remove hidden variables
                del self.env[key]
