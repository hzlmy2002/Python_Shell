from apps.Stream import Stream
from apps.decorators import *
from apps.Tools import getLines


def fixNewLine(li):
    for i in range(len(li) - 1):
        if not li[i].endswith("\n"):
            li[i] = li[i] + "\n"


@getFlag("r")
@atMostOneArgument
def sort(stream: "Stream"):
    doReverse = stream.getFlag("r")
    lines = getLines(stream)
    lines.sort(reverse=doReverse)
    fixNewLine(lines)
    stdout = stream.getStdout()
    stdout.write("".join(lines))
