from apps.stream import Stream
from apps.decorators import getFlag, glob
from apps.tools import getLines
from apps.exceptions import MissingStdin


def fixNewLine(li):
    for i in range(len(li) - 1):
        if not li[i].endswith("\n"):
            li[i] = li[i] + "\n"


@glob
@getFlag("r")
def sort(stream: "Stream"):
    doReverse = stream.getFlag("r")
    args = stream.getArgs()
    if len(args) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        lines = stdin.readlines()
    else:
        lines = getLines(stream)
    lines.sort(reverse=doReverse)
    fixNewLine(lines)
    stdout = stream.getStdout()
    stdout.write("".join(lines))
