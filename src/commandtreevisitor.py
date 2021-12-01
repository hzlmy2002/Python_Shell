from commandtree import *
from apps.stream import Stream
from functools import singledispatchmethod


class StdinNotFoundError(RuntimeError):
    pass


class CommandTreeVisitor:
    def __init__(self, stream: "Stream"):
        self.stream = stream

    @singledispatchmethod
    def visit(self, node) -> None:
        pass

    @visit.register
    def _(self, node: "Argument") -> None:
        arg = node.getArg()
        self.stream.addArg(arg)

    @visit.register
    def _(self, node: "InRedirection") -> None:
        path = node.getPath()
        try:
            stdin = open(path, "r")
        except FileNotFoundError:
            raise StdinNotFoundError
        self.stream.setStdin(stdin)

    @visit.register
    def _(self, node: "OutRedirection") -> None:
        path = node.getPath()
        stdout = open(path, "a", newline="\n")
        self.stream.setStdout(stdout)

    @visit.register
    def _(self, node: "Call") -> None:
        app = node.getApp()
        args = node.getArgs()
        for a in args:
            a.accept(self)
        app(self.stream)

    @visit.register
    def _(self, node: "Seq"):
        commands = node.getCommands()
        shellStdout = self.stream.getStdout()
        for c in commands:
            c.accept(self)
            self.stream.clearArgs()
            self.stream.clearStdin()
            self.stream.setStdout(shellStdout)
