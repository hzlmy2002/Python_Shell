from apps.App import App
from typing import List, Dict
from Stream import Stream
import apps.tools
from types import MethodType

class Cat(App):
    def __init__(self, stream: "Stream") -> None:
        self.stream = stream

    def exec(self) -> "Stream":
        if len(self.stream.params) != 0:
            raise Exception("Cat: Invalid number of parameters")
        output = []
        args=self.stream.args
        for arg in args:
            if apps.tools.isStdin(arg):
                output.append(apps.tools.stdin2str(arg))
                break
            with open(arg, "r") as f:
                content=f.read()
                if len(content) > 1:
                    output.append(content[:-1]) # remove newline                 
                else:
                    output.append(content)
        ouputStream = Stream(streamType=1, app="", params=[], args=["\n".join(output)], env={})
        return ouputStream
    
    def getStream(self) -> "Stream":
        return self.stream
    
class CatUnsafe(Cat):
    def exec(self) -> "Stream":
        c=Cat(self.stream)
        c.exec=MethodType(apps.tools.unsafeDecorator(c.exec),c)
        return c.exec()
