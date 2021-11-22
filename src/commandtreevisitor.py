from commandtree import *
from stream import Stream
from functools import singledispatchmethod


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
    def _(self, node: "Parameter") -> None:
        param = node.getParam()
        self.stream.addParam(param)

    @visit.register
    def _(self, node: "InRedirection") -> None:
        path = node.getPath()
        self.stream.setStdIn(path)

    @visit.register
    def _(self, node: "OutRedirection") -> None:
        path = node.getPath()
        self.stream.setStdOut(path)

    @visit.register
    def _(self, node: "Call") -> None:
        app = node.getApp()
        args = node.getArgs()
        for a in args:
            a.accept(self)
        self.stream = app.exec(self.stream)

    @visit.register
    def _(self, node: "Seq") -> None:
        commands = node.getCommands()
        for c in commands:
            c.accept(self)
