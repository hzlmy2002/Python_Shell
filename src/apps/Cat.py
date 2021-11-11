from apps.App import App
from typing import List, Dict
from Stream import Stream
import apps.tools
from types import MethodType
from StreamType import streamType
import os
from standardStreamExceptions import standardStreamExceptions


class Cat(App):
    def __init__(self) -> None:
        self.exceptions = standardStreamExceptions("Cat")

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
        self.exceptions.notNoneCheck(stream)
        self.exceptions.argsLenCheck(self.stream.getArgs(), notEmpty=True)
        self.exceptions.paramsLenCheck(self.stream.getParams(), empty=True)
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
