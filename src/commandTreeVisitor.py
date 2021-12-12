# coding:utf-8
from io import StringIO
from commandTree import Argument, InRedirection, \
    OutRedirection, Call, Seq, Pipe, Substitution
from apps.Stream import Stream
from functools import singledispatchmethod
from shellOutput import ShellOutput, stdout
from typing import List
from parser import parseCommand
from pathlib import Path
import re
import os


class StdinNotFoundError(RuntimeError):
    pass


class CommandTreeVisitor:
    def __init__(self, stream: "Stream"):
        self.stream = stream

    @staticmethod
    def str2args(input: str) -> List[Argument]:
        if "\n" in input:
            input = re.sub(r'\n', ' ', input)
        if "'" not in input and '"' not in input:
            return [Argument(i) for i in input.split()]
        else:
            tmpCMD = f"echo {input}"
            tree = parseCommand(tmpCMD)
            result = tree.getCommands()[0].getArgs()
            return result

    @staticmethod
    def expandGlobbling(path):
        parts = path.split("*")
        rootDir = Path(parts[0])
        globbling = "*"+"*".join(parts[1:])
        files = rootDir.glob(globbling)
        result = [str(i) for i in files]
        return result

    @staticmethod
    def sandBoxedExecution(cmd, env={"workingDir": os.getcwd()}) -> str:
        tree = parseCommand(cmd)

        sandboxStream = Stream(env.copy())
        sandboxStdout = ShellOutput(sandboxStream)
        sandboxStream.alterStdout(sandboxStdout)
        sandboxStream.getStdout().setMode(stdout.subs)
        fakeVisitor = CommandTreeVisitor(sandboxStream)

        fakeVisitor.visit(tree)
        return sandboxStream.getStdout().getSubstitutedRecord()

    @singledispatchmethod
    def visit(self, node) -> None:
        pass

    @visit.register
    def _(self, node: "Argument") -> None:
        arg = node.getArg()
        isGlobblingDisabled = True if self.stream.getEnv(
            "_disableGlobbling") == "True" else False
        if "*" in arg and not isGlobblingDisabled:
            files = CommandTreeVisitor.expandGlobbling(arg)
            for file in files:
                self.stream.addArg(file)
        else:
            self.stream.addArg(arg)

    @visit.register
    def _(self, node: "InRedirection") -> None:
        # TODO: relative, absolute and system-independent paths, globbing
        path = node.getPath()
        try:
            with open(path, "r") as f:
                content = StringIO(f.read())
                self.stream.addArg(content)
        except FileNotFoundError:
            raise StdinNotFoundError

    @visit.register
    def _(self, node: "OutRedirection") -> None:
        path = node.getPath()
        self.stream.getStdout().setMode(stdout.redir)
        self.stream.getStdout().setRedirFileName(path)

    @visit.register
    def _(self, node: "Call") -> None:
        disableGlobbling = ["find", "grep"]
        appName = node.getAppName()
        if appName in disableGlobbling or appName[1:] in disableGlobbling:
            self.stream.addToEnv("_disableGlobbling", "True")
        app = node.getApp()
        args = node.getArgs()
        for a in args:
            a.accept(self)
        app(self.stream)

    @visit.register
    def _(self, node: "Seq"):
        commands = node.getCommands()
        for c in commands:
            c.accept(self)
            self.stream.reset()
            self.stream.getStdout().reset()

    @visit.register
    def _(self, node: "Pipe"):
        self.stream.getStdout().setMode(stdout.pipe)
        calls = node.getCalls()

        firstCall = calls[0]
        firstCall.accept(self)
        self.stream.reset()

        for i in range(1, len(calls) - 1):
            currentCall = calls[i]
            prev = StringIO(self.stream.getStdout().getBuffer())
            currentCall.addArg(Argument(prev))
            self.stream.getStdout().cleanBuffer()

            currentCall.accept(self)
            self.stream.reset()

        lastCall = calls[-1]
        prev = StringIO(self.stream.getStdout().getBuffer())
        lastCall.addArg(Argument(prev))
        self.stream.getStdout().setMode(stdout.std)
        lastCall.accept(self)
        self.stream.reset()
        prev.close()

    @visit.register
    def _(self, node: "Substitution"):
        command = node.getCmdline()
        result = CommandTreeVisitor.sandBoxedExecution(
            command, self.stream.env.copy())
        args = CommandTreeVisitor.str2args(result)
        for i in args:
            i.accept(self)