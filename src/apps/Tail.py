from apps.Stream import Stream
from apps.decorators import *
from apps.Tools import getLines


@intParam("n", required=False, defaultVal=10)
@hasOneArgument
def tail(stream: "Stream"):
    linesNum = stream.getParam("n")
    lines = getLines(stream)
    stdout = stream.getStdout()
    display_length = min(len(lines), int(linesNum))
    content = ""
    for i in range(0, display_length):
        content += lines[len(lines) - display_length + i]
    stdout.write(content)
    if stream.getArgs() == 1:
        lines.close()
