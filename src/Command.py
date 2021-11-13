from enum import Enum
import os
from typing import List, Dict

from Stream import *

class CommandFlag(Enum):
    std=0 # cmd1
    seq=1 # cmd1|cmd2
    pipe=2 # cmd1;cmd2
    subs=3 # cmd1 `cmd2`
    glob=4 # cmd1 cmd2/*
    redirOut=5 # cmd1 > cmd2
    redirIn=6 # cmd1 < cmd2

class Command:
    def __init__(self,type:"CommandFlag"=CommandFlag.std):
        self.flag = type
        self.next:List[Command] = []
        self.prev:"Command" = None
        self.stream:"Stream"=None
        self.redirOut = None
        self.redirIn = None
    
    def addNode(self,cmd:"Command"):
        self.next.append(cmd)
        cmd.prev = self

    def popNode(self)->"Command":
        if len(self.next) > 0:
            target=self.next.pop()
            target.prev = None
            return target
        return None

    def accept(self,visitor):
        visitor.visit(self)
        for cmd in self.next:
            cmd.accept(visitor)
