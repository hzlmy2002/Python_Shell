import sys
import os
from shellParser import parseCommand
from typing import TextIO
from apps.stream import Stream
from commandTreeVisitor import CommandTreeVisitor
import traceback


class Shell:
    def __init__(self, workingDir: str):
        self.stream = Stream(workingDir)

    def eval(self, cmdline: str, stdout: TextIO):
        if len(cmdline.strip()) == 0:
            return
        commandTree = parseCommand(cmdline, self)
        self.stream.setStdout(stdout)

        commandTreeVisitor = CommandTreeVisitor(self.stream)
        commandTreeVisitor.visit(commandTree)

    def getWorkingDir(self) -> str:
        return self.stream.getWorkingDir()


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
        mode = "advanced"
        if os.name != "posix":
            print("Entering basic mode. Extra features are not available.")
            print("Please use Linux. (not in container)")
            mode = "basic"
        try:
            from keyboardDisplay import hideInput, display, keyboardMonitor
            from keyboardDisplay import Data, State
            from threading import Thread, Lock
            from pynput import keyboard
        except ImportError:
            mode = "basic"
            print(
                "Entering basic mode. Extra features are not available in Docker containers."
            )
            print("Check https://pynput.readthedocs.io/en/latest/limitations.html")

        if mode == "advanced":
            try:
                print("Entering advanced mode.")
                lock = Lock()
                data = Data()
                state = State()
                data.setPrefix(sh.getWorkingDir() + "> ")
                t1 = Thread(target=hideInput, args=(state,))
                t2 = Thread(target=display, args=(data, lock, state,))
                t3 = keyboard.Listener(on_press=keyboardMonitor(data, sh, lock, state))
                t1.start()
                t2.start()
                t3.start()
            except Exception:
                print(traceback.format_exc())
                exit(-1)
        else:
            while True:
                cmdline = input(sh.getWorkingDir() + "> ")
                sh.eval(cmdline, sys.stdout)
