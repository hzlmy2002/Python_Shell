from apps.Stream import Stream
from apps.decorators import intParam, hasOneArgument
from apps.Tools import getLines


@intParam("n", required=False, defaultVal=10)
@hasOneArgument
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    lines = getLines(stream)
    stdout = stream.getStdout()
    content = ""
    linesNum = min(len(lines), int(linesNum))
    for i in range(0, int(linesNum)):
        content += lines[i]
    stdout.write(content)
