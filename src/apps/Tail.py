from apps.Stream import Stream
from apps.decorators import glob, hasParam
from apps.Tools import getLines
from apps.Exceptions import MissingStdin


@glob
@hasParam("n", required=False, defaultVal=10, numeric=True)
def tail(stream: "Stream"):
    linesNum = stream.getParam("n")
    args = stream.getArgs()
    if len(args) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        lines = stdin.readlines()
    else:
        lines = getLines(stream)
    stdout = stream.getStdout()
    content = ""
    linesNum = min(len(lines), int(linesNum))
    for i in range(0, linesNum):
        content += lines[len(lines) - linesNum + i]
    stdout.write(content)
