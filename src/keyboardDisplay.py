from threading import Lock
from pynput import keyboard
from getpass import getpass
import time
import sys
import traceback

class Data:
    def __init__(self):
        self.data = ""
        self.pref=""

    def add(self,char):
        self.data += char

    def setPrefix(self,pref):
        self.pref=pref

    def pop(self):
        self.data = self.data[:-1]

    def clear(self):
        self.data = ""

    def get(self):
        return self.data

    def getWithPrefix(self):
        if len(self.data)==0:
            return self.pref
        else:
            return self.pref+self.data+" ◄"

class State:
    def __init__(self):
        self.alive=True
    def die(self):
        self.alive=False
    def isAlive(self):
        return self.alive

def hideInput(state:"State"):
    while True:
        if not state.isAlive():
            break
        getpass("")

def display(data:"Data",lock:"Lock",state:"State"):
    while True:
        if not state.isAlive():
            break
        length=128
        output=""
        if len(data.getWithPrefix())<length:
            output=data.getWithPrefix()+"".join([" " for _ in range(length-len(data.getWithPrefix()))])
        else:
            output=data.getWithPrefix()
   
        lock.acquire()
        print(output,end="\r")
        lock.release()
        time.sleep(0.1)

def keyboardMonitor(data:"Data",sh,lock:"Lock",state:"State"):
    def wrapper(key:"keyboard.Key"):
        if key == keyboard.Key.tab:
            pass
        elif key== keyboard.Key.backspace:
            data.pop()
        elif key == keyboard.Key.space:
            data.add(" ")
        elif key == keyboard.Key.enter:
            lock.acquire()
            print(data.getWithPrefix())
            try:
                sh.eval(data.get(),sys.stdout)
            except Exception:
                print(traceback.format_exc())
                print("Press Enter to Confirm and Exit.")
                state.die()
                return False
            data.setPrefix(sh.getWorkingDir()+"> ")
            data.clear()
            lock.release()
        else:
            if hasattr(key,"char"):
                data.add(key.char)
    return wrapper