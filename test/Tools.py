import io
import sys
from shell import Shell


def getStdOut(cmdLine):
    sh = Shell("")
    old = sys.stdout
    new = io.StringIO()
    sys.stdout = new
    sh.eval(cmdLine, new)
    output = new.getvalue()
    sys.stdout = old
    return output
