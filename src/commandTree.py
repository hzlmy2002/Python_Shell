from abc import ABC
from typing import Callable, List
from apps.stream import Stream


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
    def __init__(self, app: Callable[["Stream"], None], args: List[CommandTreeNode]):
        self.app = app
        self.args = args

    def getApp(self) -> Callable[["Stream"], None]:
        return self.app

    def getArgs(self) -> List[CommandTreeNode]:
        return self.args


class Seq(CommandTreeNode):
    def __init__(self, commands: List[CommandTreeNode]):
        self.commands = commands

    def getCommands(self) -> List[CommandTreeNode]:
        return self.commands


class Pipe(CommandTreeNode):
    def __init__(self, calls: List[Call]):
        self.calls = calls

    def getCalls(self):
        return self.calls
