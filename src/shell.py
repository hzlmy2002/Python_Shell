import sys
import os
import re
from collections import deque
from Parser import Parser
from AppManager import AppManager
from Stream import Stream


class Shell:
    def __init__(self) -> None:
        self.manager = AppManager()
        self.parser = Parser()
        self.env = None

    def get_raw(self, cmdline):
        raw_commands = []
        for m in re.finditer("([^\"';]+|\"[^\"]*\"|'[^']*')", cmdline):
            if m.group(0):
                raw_commands.append(m.group(0))
        return raw_commands

    def evaluate(self, cmdline):
        # Returns list of outputs or error message if required
        command_list = self.parser.parse(self.get_raw(cmdline), self.env)
        output_list = self.manager.run_app(command_list)
        return output_list


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    sh = Shell()
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        sh.evaluate(sys.argv[2])
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque(sh.evaluate(cmdline))
            while len(out) > 0:
                print(out.popleft(), end="")
