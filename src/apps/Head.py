from apps.Exceptions import MissingStdin
from apps.Stream import Stream
from apps.decorators import hasParam
from apps.Tools import getLines


@hasParam("n", required=False, defaultVal=10, numeric=True)
def head(stream: "Stream"):
    linesNum = stream.getParam("n")
    if len(stream.getArgs()) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        lines = stdin.readlines()
    else:
        lines = getLines(stream)
    stdout = stream.getStdout()
    content = ""
    linesNum = min(len(lines), int(linesNum))
    for i in range(0, int(linesNum)):
        content += lines[i]
    stdout.write(content)
