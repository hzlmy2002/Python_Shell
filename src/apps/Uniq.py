from apps.Stream import Stream
from apps.decorators import getFlag, _glob
from apps.Exceptions import MissingStdin
from apps.Tools import getLines, toList
from io import StringIO


@_glob
@getFlag("i")
def uniq(stream: "Stream"):
    caseSensitive = stream.getFlag("i")
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
    res = ""
    last = ""
    for i in range(0, len(lines)):
        line = lines[i]
        compLine = line
        if caseSensitive:
            compLine = compLine.upper()
        if not compLine == last:
            last = compLine
            res += line
    stdout = stream.getStdout()
    stdout.write(res)
