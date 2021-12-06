from enum import Enum
from apps import Stream

class stdout(Enum):
    """
    Enum for the stdout of the shell
    """
    std="standard"
    pipe="pipe"
    subs="substitution"
    redir="redirection" # one off type, reset after write

    def __str__(self):
        return self.value

class shellOutput:
    def __init__(self,globalStream) -> None:
        self.stream=globalStream
        self.mode=stdout.std

        self.sandbox=[]
        self.redirFileName=""

    def reset(self):
        self.mode=stdout.std
        self.sandbox.clear()
        self.redirFileName=""

    def cleanBuffer(self):
        self.sandbox.clear()

    def write(self,content):
        # Write redirection will be automatically reset afterwards
        if self.mode==stdout.std:
            print(content,end="")

        elif self.mode==stdout.pipe:
            if len(self.sandbox)==0:
                self.sandbox.append(content)
            else:
                self.cleanBuffer()
                self.sandbox.append(content)
        elif self.mode==stdout.subs:
            self.sandbox.append(content)
        elif self.mode==stdout.redir:
            with open(self.redirFileName,"w") as f:
                f.write(content)
            self.reset()
        else:
            raise Exception("Unknown output mode")
    
    def getBuffer(self,reset=False):
        if self.mode==stdout.pipe:
            output=""
            if len(self.sandbox)==0:
                return output
            else:
                output=self.sandbox[0]
            if reset:
                self.reset()
            return output
                
        elif self.mode==stdout.subs:
            output=self.sandbox.copy()
            if reset:
                self.reset()
            return output
        else:
            raise Exception(f"Inadequate output mode {self.mode}")

    def setMode(self,mode):
        self.reset()
        self.mode=mode

    def setRedirFileName(self,filename):
        self.redirFileName=filename

    def getMode(self):
        return self.mode