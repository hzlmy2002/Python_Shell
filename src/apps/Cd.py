from apps.App import App
from Stream import Stream
from StreamType import streamType
from types import MethodType
import apps.tools
import os
from standardStreamExceptions import standardStreamExceptions


class Cd(App):
    def __init__(self) -> None:
        self.exceptions = standardStreamExceptions("Cd")

    def getStream(self) -> "Stream":
        return self.stream

    def init_and_check_stream(self, stream):
        self.stream = stream
        self.args = self.stream.getArgs()
        self.exceptions.argsLenCheck(self.args, equalOne=True)
        self.exceptions.paramsLenCheck(self.stream.getParams(), empty=True)

    def exec(self, stream: "Stream") -> "Stream":
        self.exceptions.notNoneCheck(stream)
        self.init_and_check_stream(stream)
        try:
            os.chdir(self.args[0])
        except:
            raise Exception("Invalid Directory")
        new_env = self.stream.getEnv()
        new_env["working_dir"] = os.getcwd()
        return Stream(
            sType=streamType.output,
            app="",
            params=[],
            args=[],
            env=new_env,
        )


class CdUnsafe(Cd):
    def exec(self, stream: "Stream") -> "Stream":
        c = Cd()
        c.exec = MethodType(apps.tools.unsafeDecorator(c.exec), c)
        return c.exec(stream)
