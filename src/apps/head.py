from apps.Stream import Stream
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir


@paramTag("n")
@intParam("n", required=False, defaultVal=10)
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    args = stream.getArgs()
    isFile = False
    if len(args) == 0:  # no file specified
        lines = stream.getStdin()
    elif len(args) != 1:
        raise InvalidArgumentError("Too many arguments specified")
    else:
        isFile = True
        fileName = args[0]
        try:
            lines = open(fileName, "r")
        except:
            raise InvalidFileOrDir("File does not exist")

    stdout = stream.getStdout()
    i = 0
    for l in lines:
        stdout.write(l)
        i += 1
        if i == int(linesNum):
            break
    if isFile:
        lines.close()
