from apps.Stream import Stream
from apps.decorators import _glob, intParam
from apps.Tools import getLines, toList
from apps.Exceptions import MissingStdin
from io import StringIO


@_glob
@intParam("n", required=False, defaultVal=10)
def tail(stream: "Stream"):
    linesNum = stream.getParam("n")
    args = stream.getArgs()
    if len(args) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        if type(stdin) == StringIO:
            lines = toList(stdin.getvalue())
        else:
            lines = stdin.readlines()
    else:
        lines = getLines(stream)
    stdout = stream.getStdout()
    content = ""
    linesNum = min(len(lines), int(linesNum))
    for i in range(0, linesNum):
        content += lines[len(lines) - linesNum + i]
    stdout.write(content)
