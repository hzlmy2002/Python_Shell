from apps.Stream import *
from apps import tools
from appFactory import *
from commandTree import *
from parser import CommandParsers

class AppManager():
    def __init__(self):
        self.outputStream=None
        self.env={}
        self.appFactory=appFactory()
    
    def call2stream(self,call:"Call")->"Stream":
        singleOptionApps={"uniq","sort","_uniq","_sort"} # They can be zero args as well
        zeroOptionApps={"pwd","ls","cat","head","_pwd","_ls","_cat","_head"}

        s=Stream.Stream(sType=Stream.streamType.input,app="",params={},env=self.env)
        s.app=call.getApp()

        if s.app in singleOptionApps: # app that has parameters but without corresponding args
            for i in call.getArgs():
                if type(i)==Parameter:
                    s.params[i.getParam()]=[]
                else:
                    s.params["main"].append(i.getArg())
        elif s.app == "grep" or s.app == "_grep": # find can only have args
            if len(call.getArgs()) <= 0:
                raise stdStreamExceptions(appName.grep).raiseException(exceptionType.paramNum)
            elif len(call.getArgs()) <= 2:
                s.params["pattern"]=[call.getArgs()[0].getArg()]
                if len(call.getArgs()) == 2:
                    s.params["main"].append(call.getArgs()[1].getArg())
            else:
                raise stdStreamExceptions(appName.grep).raiseException(exceptionType.paramNum)
        elif s.app == "find" or s.app == "_find":
            if len(call.getArgs()) == 2 and type(call.getArgs()[0])==Parameter and call.getArgs()[0].getParam()=="-name":
                s.params["pattern"]=[call.getArgs()[1].getArg()]
            elif len(call.getArgs()) == 3 and type(call.getArgs()[1])==Parameter and call.getArgs()[1].getParam()=="-name":
                s.params["pattern"]=[call.getArgs()[2].getArg()]
                s.params["main"].append(call.getArgs()[0].getArg())
            else:
                raise stdStreamExceptions(appName.find).raiseException(exceptionType.paramNum)
        elif len(call.getArgs()) <= 3 and len(call.getArgs()) >=2 and type(call.getArgs()[0])==Parameter:
            if len(call.getArgs()) == 3:
                s.params[call.getArgs()[0].getParam()]=[call.getArgs()[1].getArg()]
                s.params["main"].append(call.getArgs()[2].getArg())
            else:
                s.params[call.getArgs()[0].getParam()]=[call.getArgs()[1].getArg()]
        elif len(call.getArgs()) == 1 and type(call.getArgs()[0])==Argument:
            s.params["main"].append(call.getArgs()[0].getArg())
        elif len(call.getArgs()) == 0 and (s.app in zeroOptionApps or s.app in singleOptionApps):
            pass
        else:
            raise SyntaxError(f"{s.app}: Illegal syntax!")
        return s

def test():
    cmd=CommandParsers.command.parse("tail -n 16 ./*").or_die()
    call=cmd.getCommands()[0]

    am=AppManager()
    s=am.call2stream(call)
    pass

test()