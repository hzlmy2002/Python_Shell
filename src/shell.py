import sys
import os
from _parser import parseCommand
from typing import TextIO
from apps.Stream import Stream
from commandTreeVisitor import CommandTreeVisitor
from keyboardDisplay import hideInput,display,keyboardMonitor
from keyboardDisplay import Data,State
from threading import Thread,Lock
from pynput import keyboard

class Shell:
    def __init__(self, workingDir: str):
        self.stream = Stream(workingDir)

    def eval(self, cmdline: str, stdout: TextIO):
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
        try:
            lock=Lock()
            data=Data()
            state=State()
            t1=Thread(target=hideInput,args=(state,))
            t2=Thread(target=display,args=(data,lock,state,))
            t3=keyboard.Listener(on_press=keyboardMonitor(data,sh,lock,state))
            t1.start()
            t2.start()
            t3.start()
        except KeyboardInterrupt:
            exit(0)
        except EOFError:
            exit(0)
