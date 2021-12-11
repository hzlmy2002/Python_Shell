from apps.Stream import Stream
from apps.decorators import *
from apps.Exceptions import InvalidArgumentError
from apps.Tools import getLines
import os


@getFlag("i")
@atMostOneArgument
def uniq(stream: "Stream"):
    caseSensitive = stream.getFlag("i")
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
