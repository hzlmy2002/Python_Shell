from io import StringIO
from apps.Exceptions import MissingStdin
from apps.Stream import Stream
from apps.decorators import _glob, intParam
from apps.Tools import getLines, toList


@_glob
@intParam("n", required=False, defaultVal=10)
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    if len(stream.getArgs()) == 0:
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
    for i in range(0, int(linesNum)):
        content += lines[i]
    content += "\n"
    stdout.write(content)
