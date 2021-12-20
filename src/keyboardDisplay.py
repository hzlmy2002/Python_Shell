from threading import Lock
from pynput import keyboard
from getpass import getpass
import time
import sys
import traceback

# this file contains the extra functionality implementation


class Data:
    def __init__(self):
        self.data = ""
        self.history = []
        self.pointer = 0
        self.pref = ""
        self.pressedUp = -1

    def pressUp(self):
        self.pressedUp *= -1

    def isUpPressed(self):
        return self.pressedUp == 1

    def add(self, char):
        self.data += char

    def update(self, data):
        self.data = data

    def addHistory(self):
        self.history.append(self.data)

    def getHistory(self):
        return self.history[:]

    def setPrefix(self, pref):
        self.pref = pref

    def setCounter(self, counter):
        self.pointer = counter

    def pop(self):
        self.data = self.data[:-1]

    def clear(self):
        self.data = ""

    def get(self):
        return self.data

    def getCounter(self):
        return self.pointer

    def getWithPrefix(self):
        if len(self.data) == 0:
            return self.pref
        else:
            return self.pref + self.data + " ◄"


class State:
    def __init__(self):
        self.alive = True

    def die(self):
        self.alive = False

    def isAlive(self):
        return self.alive


def hideInput(state: "State"):
    while True:
        if not state.isAlive():
            break
        try:
            getpass("")
        except KeyboardInterrupt:
            state.die()
            break
        except EOFError:
            state.die()
            break


def display(data: "Data", lock: "Lock", state: "State"):
    while True:
        if not state.isAlive():
            break
        length = 128
        output = ""
        if len(data.getWithPrefix()) < length:
            output = data.getWithPrefix() + "".join(
                [" " for _ in range(length - len(data.getWithPrefix()))]
            )
        else:
            output = data.getWithPrefix()

        lock.acquire()
        print(output, end="\r", flush=True)
        lock.release()
        time.sleep(0.1)


def keyboardMonitor(data: "Data", sh, lock: "Lock", state: "State"):
    def wrapper(key: "keyboard.Key"):
        if not state.isAlive():
            return False
        if key == keyboard.Key.tab:
            pass
        elif key == keyboard.Key.backspace:
            data.pop()
        elif key == keyboard.Key.space:
            data.add(" ")
        elif key == keyboard.Key.up:
            history = data.getHistory()
            history.reverse()
            if len(history) > 0 and data.getCounter() <= len(history) - 1:
                data.update(history[data.getCounter()])
                data.setCounter(data.getCounter() + 1)
                data.pressUp()

        elif key == keyboard.Key.down:
            history = data.getHistory()
            history.reverse()
            if len(history) > 0 and data.getCounter() >= 0:
                if data.getCounter() >= 1:
                    data.setCounter(data.getCounter() - 1)
                    data.update(history[data.getCounter()])

        elif key == keyboard.Key.enter:
            lock.acquire()
            print(data.getWithPrefix())
            try:
                sh.eval(data.get(), sys.stdout)
                data.setCounter(0)
                data.addHistory()
            except Exception:
                print(traceback.format_exc())
                print("Press Enter to Confirm and Exit.")
                state.die()
                return False
            data.setPrefix(sh.getWorkingDir() + "> ")
            data.clear()
            lock.release()
        else:
            if hasattr(key, "char"):
                data.add(key.char)

    return wrapper
