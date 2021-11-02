import sys
import os
import re
from collections import deque
from Parser import Parser
from app_manager import AppManager


class Shell:
    def __init__(self) -> None:
        self.manager = AppManager()
        self.parser = Parser()

    def evaluate(self, cmdline, out):
        raw_commands = []
        for m in re.finditer("([^\"';]+|\"[^\"]*\"|'[^']*')", cmdline):
            if m.group(0):
                raw_commands.append(m.group(0))
        for command in raw_commands:
            tokens = self.parser.parse_token(command)
            args = tokens[1:]
            # Using appManager to manage which app to exectue
            app = self.manager.extract_app(tokens[0], out, args)
            app.exec()


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    sh = Shell()
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        sh.evaluate(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            sh.evaluate(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
