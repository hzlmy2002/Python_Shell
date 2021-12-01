import sys
import os
from parser import parseCommand
from typing import TextIO
from apps.stream import Stream
from commandtreevisitor import CommandTreeVisitor


class ShellStdout:
    def __init__(self, sh: "Shell"):
        self.sh = sh

    def write(self, s: str):
        self.sh.output(s)


class Shell:
    def __init__(self, workingDir):
        env = {"workingDir": workingDir}
        self.stdout = ShellStdout(self)

        self.stream = Stream(env, self.stdout)
        self.commandTreeVisitor = CommandTreeVisitor(self.stream)

    def evaluate(self, cmdline):
        commandTree = parseCommand(cmdline)
        self.commandTreeVisitor.visit(commandTree)

    def output(self, line):
        print(line, end="")

    def repl(self):
        while True:
            workingDir = self.stream.getEnv("workingDir")
            self.output(workingDir + "> ")
            cmdline = input()
            self.evaluate(cmdline)


if __name__ == "__main__":
    workingDir = os.getcwd()
    sh = Shell(workingDir)

    args = sys.argv[1:]
    argsNum = len(args)

    if argsNum > 0:
        if argsNum != 2:
            raise ValueError("Wrong number of command line arguments.")
        if args[0] != "-c":
            raise ValueError(f"Unexpected command line argument {args[0]}.")
        sh.evaluate(args[1])
    else:
        sh.repl()
