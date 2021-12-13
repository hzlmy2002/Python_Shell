import sys
import os
from _parser import parseCommand
from typing import TextIO
from apps.Stream import Stream
from commandTreeVisitor import CommandTreeVisitor


class Shell:
    def __init__(self, workingDir: str):
        self.stream = Stream(workingDir)

    def eval(self, cmdline: str, stdout: TextIO):
        commandTree = parseCommand(cmdline, self)
        self.stream.setStdout(stdout)

        commandTreeVisitor = CommandTreeVisitor(self.stream)
        commandTreeVisitor.visit(commandTree)

    def repl(self):
        try:
            while True:
                workingDir = self.stream.getWorkingDir()
                self.eval(input(f"{workingDir}> "), sys.stdout)
        except KeyboardInterrupt:
            exit(0)
        except EOFError:
            exit(0)


if __name__ == "__main__":  # pragma: no cover
    workingDir = os.getcwd()
    sh = Shell(workingDir)

    args = sys.argv[1:]
    argsNum = len(args)

    if argsNum > 0:
        if argsNum != 2:
            raise ValueError("Wrong number of command line arguments.")
        if args[0] != "-c":
            raise ValueError(f"Unexpected command line argument {args[0]}.")
        sh.eval(args[1], sys.stdout)
    else:
        sh.repl()
