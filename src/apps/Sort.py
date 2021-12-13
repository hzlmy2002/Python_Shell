from io import StringIO
from apps.Stream import Stream
from apps.decorators import getFlag, _glob, hasOneArgument
from apps.Tools import getLines, toList
from apps.Exceptions import MissingStdin


def fixNewLine(li):
    for i in range(len(li) - 1):
        if not li[i].endswith("\n"):
            li[i] = li[i] + "\n"


@_glob
@getFlag("r")
def sort(stream: "Stream"):
    doReverse = stream.getFlag("r")
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
    lines.sort(reverse=doReverse)
    fixNewLine(lines)
    stdout = stream.getStdout()
    stdout.write("".join(lines))
