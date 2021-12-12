from abc import ABC
from typing import Callable, List
from apps.Stream import Stream


class CommandTreeNode(ABC):
    def accept(self, visitor) -> None:
        visitor.visit(self)


class Argument(CommandTreeNode):
    def __init__(self, arg: str):
        self.arg = arg

    def getArg(self) -> str:
        return self.arg


class Redirection(CommandTreeNode):
    def __init__(self, path: "Argument"):
        self.path = path.getArg()

    def getPath(self) -> str:
        return self.path


class InRedirection(Redirection):
    pass


class OutRedirection(Redirection):
    pass


class Call(CommandTreeNode):
    def __init__(self, appName: str, app: Callable[["Stream"], None],
                 args: List[CommandTreeNode]):
        self.appName = appName
        self.app = app
        self.args = args

    def getApp(self) -> Callable[["Stream"], None]:
        return self.app

    def getAppName(self) -> str:
        return self.appName

    def getArgs(self) -> List[CommandTreeNode]:
        return self.args

    def addArg(self, arg: CommandTreeNode) -> None:
        self.args.append(arg)


class Seq(CommandTreeNode):
    def __init__(self, commands: List[CommandTreeNode]):
        self.commands = commands

    def getCommands(self) -> List[CommandTreeNode]:
        return self.commands


class Pipe(CommandTreeNode):
    def __init__(self, calls: List[Call]):
        self.calls = calls

    def getCalls(self) -> List[Call]:
        return self.calls


class Substitution(CommandTreeNode):
    def __init__(self, cmdline: str):
        self.cmdline = cmdline

    def getCmdline(self) -> str:
        return self.cmdline
