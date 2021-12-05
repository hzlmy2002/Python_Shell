from apps.Stream import Stream
from apps.decorators import *
from apps.Tools import getLines


@intParam("n", required=False, defaultVal=10)
@hasOneArgument
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    lines = getLines(stream)
    stdout = stream.getStdout()
    i = 0
    for l in lines:
        stdout.write(l)
        i += 1
        if i == int(linesNum):
            break
    if stream.getArgs() == 1:
        lines.close()
