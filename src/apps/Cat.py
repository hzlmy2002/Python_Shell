from apps.App import App
from typing import List, Dict
from Stream import *
import apps.tools
from types import MethodType

import os


class Cat(App):
    def __init__(self) -> None:
        self.stream = None

    def processStdin(self):
        if len(self.stream.args) != 1:
            raise Exception("Cat: Ilegal stdin")

        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[apps.tools.stdin2str(self.stream.args[0])],
            env={},
        )

    def processFiles(self):
        output = []
        for arg in self.stream.args:
            if os.path.exists(arg):
                with open(arg, "r") as f:
                    output.append(f.read())
            else:
                raise FileNotFoundError("Cat: File not found")
        ouputStream = Stream(
            sType=streamType.output, app="", params=[], args=["".join(output)], env={}
        )
        return ouputStream

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
        if self.stream == None:
            raise Exception("Cat: No stream to process")
        if len(self.stream.params) != 0 or len(self.stream.getArgs()) == 0:
            raise Exception("Cat: Invalid number of parameters")
        if apps.tools.isStdin(self.stream.getArgs()[0]):
            return self.processStdin()
        else:
            return self.processFiles()

    def getStream(self) -> "Stream":
        return self.stream


class CatUnsafe(Cat):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cat()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
