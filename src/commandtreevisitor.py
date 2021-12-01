from io import StringIO
from commandTree import *
from apps.Stream import Stream
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
        # TODO: relative, absolute and system-independent paths, globbing
        path = node.getPath()
        try:
            stdin = open(path, "r")
        except FileNotFoundError:
            raise StdinNotFoundError
        self.stream.setStdin(stdin)

    @visit.register
    def _(self, node: "OutRedirection") -> None:
        # TODO: relative, absolute and system-independent paths, globbing
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
        shellStdout = self.stream.getStdout()
        commands = node.getCommands()
        for c in commands:
            c.accept(self)
            self.stream.clearArgs()
            self.stream.clearParams()
            self.stream.clearStdin()
            self.stream.setStdout(shellStdout)

    @visit.register
    def _(self, node: "Pipe"):
        shellStdout = self.stream.getStdout()
        calls = node.getCalls()
        for i in range(len(calls) - 1):
            stdout = StringIO()
            self.stream.setStdout(stdout)

            c = calls[i]
            c.accept(self)
            self.stream.setStdin(stdout)

            self.stream.clearArgs()
            self.stream.clearParams()

        self.stream.setStdout(shellStdout)
        calls[-1].accept(self)
