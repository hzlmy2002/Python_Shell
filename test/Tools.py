import io
import sys
from shell import eval


def getStdOut(cmdLine):
    old = sys.stdout
    new = io.StringIO()
    sys.stdout = new
    eval(cmdLine)
    output = new.getvalue()
    sys.stdout = old
    return output
