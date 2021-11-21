from abc import ABC
from typing import List
from apps import App


class CommandTreeNode(ABC):
    def visit(self, visitor) -> None:
        visitor.accept(self)


class Argument(CommandTreeNode):
    def __init__(self, arg: str):
        self.arg = arg

    def getArg(self) -> str:
        return self.arg


class Redirection(CommandTreeNode):
    def __init__(self, path: str):
        self.path = path

    def getPath(self) -> str:
        return self.path


class InRedirection(Redirection):
    pass


class OutRedirection(Redirection):
    pass


class Call(CommandTreeNode):
    def __init__(self, app: "App", params: List[CommandTreeNode]):
        self.app = app
        self.params = params

    def getApp(self) -> "App":
        return self.app

    def getParams(self) -> List[CommandTreeNode]:
        return self.params


class Seq(CommandTreeNode):
    def __init__(self, commands: List[CommandTreeNode]):
        self.commands = commands

    def getCommands(self) -> List[CommandTreeNode]:
        return self.commands
