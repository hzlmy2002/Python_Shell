from apps.App import App
from Stream import *

from types import MethodType
import apps.tools
import os


class Cd(App):
    def __init__(self) -> None:
        self.stream = None

    def getStream(self) -> "Stream":
        return self.stream

    def init_and_check_stream(self, stream):
        self.stream = stream
        self.args = self.stream.getArgs()
        if len(self.args) == 0 or len(self.args) > 1:
            raise Exception("Cd: Invalid number of command line arguments")
        if self.stream.params:
            raise Exception("Cd: Should not take parameters")

    def exec(self, stream: "Stream") -> "Stream":
        if stream == None:
            raise Exception("Cd: No stream to process")
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
