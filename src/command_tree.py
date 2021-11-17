from abc import ABC
from typing import List


class CommandTreeNode(ABC):
    def visit(self, visitor) -> None:
        visitor.accept(self)


class Argument(CommandTreeNode):
    def __init__(self, arg: str):
        self._arg = arg

    def get_arg(self) -> str:
        return self._arg


class Redirection(CommandTreeNode):
    def __init__(self, path: str):
        self._path = path

    def get_path(self) -> str:
        return self._path


class InRedirection(Redirection):
    pass


class OutRedirection(Redirection):
    pass


class Call(CommandTreeNode):
    def __init__(self, args: List[CommandTreeNode]):
        self._args = args

    def get_args(self) -> List[CommandTreeNode]:
        return self._args


class Seq(CommandTreeNode):
    def __init__(self, commands: List[CommandTreeNode]):
        self._commands = commands

    def get_commands(self) -> List[CommandTreeNode]:
        return self._commands
