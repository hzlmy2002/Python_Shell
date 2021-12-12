from apps.Stream import Stream
from apps.decorators import intParam, hasOneArgument
from apps.Tools import getLines


@intParam("n", required=False, defaultVal=10)
@hasOneArgument
def tail(stream: "Stream"):
    linesNum = stream.getParam("n")
    lines = getLines(stream)
    stdout = stream.getStdout()
    content = ""
    linesNum = min(len(lines), int(linesNum))
    for i in range(0, linesNum):
        content += lines[len(lines) - linesNum + i]
    stdout.write(content)
