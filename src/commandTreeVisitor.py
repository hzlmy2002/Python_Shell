# coding:utf-8
from io import StringIO
from commandTree import (
    Argument,
    InRedirection,
    OutRedirection,
    Call,
    Seq,
    Pipe,
)
from apps.Stream import Stream
from functools import singledispatchmethod
from pathlib import Path


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
        path = Path(self.stream.workingDir, node.getPath())
        try:
            stdin = open(path, "r")
        except FileNotFoundError:
            raise StdinNotFoundError("stdin not found.")
        self.stream.setStdin(stdin)

    @visit.register
    def _(self, node: "OutRedirection") -> None:
        path = Path(self.stream.workingDir, node.getPath())
        stdout = open(path, "w")
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
        initialStdout = self.stream.getStdout()
        commands = node.getCommands()
        for c in commands:
            c.accept(self)
            self.stream.reset()
            self.stream.setStdout(initialStdout)

    @visit.register
    def _(self, node: "Pipe"):
        initialStdout = self.stream.getStdout()
        calls = node.getCalls()
        for i in range(len(calls) - 1):
            stdout = StringIO()
            self.stream.setStdout(stdout)

            calls[i].accept(self)

            self.stream.reset()
            self.stream.setStdin(stdout)

        self.stream.setStdout(initialStdout)
        calls[-1].accept(self)
        self.stream.reset()
