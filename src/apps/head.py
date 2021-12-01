from apps.stream import Stream
from apps.decorators import intParam


@intParam("n", required=False, defaultVal=10)
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    args = stream.getArgs()
    if len(args) == 0:  # no file specified
        lines = stream.getStdin()
    else:
        fileName = args[0]
        lines = open(fileName, "r")

    stdout = stream.getStdout()
    i = 0
    for l in lines:
        stdout.write(l)
        i += 1
        if i == linesNum:
            break
