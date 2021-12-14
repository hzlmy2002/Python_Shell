import os
from threading import Lock
from pynput import keyboard
from getpass import getpass
import time
import sys

class Data:
    def __init__(self):
        self.data = ""

    def add(self,char):
        self.data += char

    def pop(self):
        self.data = self.data[:-1]

    def clear(self):
        self.data = ""

    def get(self):
        return self.data

    def getWithPrefix(self):
        pref=os.getcwd()+"> "
        return pref+self.data

def hideInput():
    while True:
        getpass("")

def display(data:"Data",lock:"Lock"):
    while True:
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

def keyboardMonitor(data:"Data",sh,lock:"Lock"):
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

            sh.eval(data.get(),sys.stdout)

            data.clear()
            lock.release()
        else:
            if hasattr(key,"char"):
                data.add(key.char)
    return wrapper