import sys
import os
from parser import parseCommand
from apps.Stream import Stream
from commandTreeVisitor import CommandTreeVisitor
from shellOutput import ShellOutput


class Shell:
    def __init__(self, workingDir):
        env = {"workingDir": workingDir}

        self.stream = Stream(env)
        self.stdout = ShellOutput(self.stream)
        self.stream.alterStdout(self.stdout)
        self.commandTreeVisitor = CommandTreeVisitor(self.stream)

    def evaluate(self, cmdline):
        commandTree = parseCommand(cmdline)
        self.commandTreeVisitor.visit(commandTree)


def eval(cmdline) -> None:  # adjust original syntax
    shell = Shell(os.getcwd())
    shell.evaluate(cmdline)
    return shell.stdout


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
        sh.evaluate(args[1])
    else:
        try:
            while True:
                eval(input("{}> ".format(os.getcwd())))
        except KeyboardInterrupt:
            print("\nbye")
            exit(0)
        except EOFError:
            print("\nbye")
            exit(0)
